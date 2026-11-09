#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="lazyaudit:1.0.0"
WRAPPER_PATH="/usr/local/bin/lazyaudit"
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ENGINE=""
PKG_MANAGER=""
PODMAN_PACKAGE=""
DOCKER_PACKAGE=""
WRAPPER_TMP=""
USER_NAME=$(id -un)

cleanup() {
    if [[ -n "$WRAPPER_TMP" ]]; then
        rm -f "$WRAPPER_TMP"
    fi
}
trap cleanup EXIT

die() {
    echo "[!] $*" >&2
    exit 1
}

require_sudo() {
    command -v sudo >/dev/null 2>&1 || die "Se requiere sudo para instalar paquetes y el ejecutable."
    sudo -v
}

engine_works() {
    local engine=$1
    command -v "$engine" >/dev/null 2>&1 && "$engine" info >/dev/null 2>&1
}

load_distro() {
    [[ $(uname -s) == "Linux" ]] || die "LazyAudit solo admite la instalación en Linux."
    [[ -r /etc/os-release ]] || die "No se pudo identificar la distribución: falta /etc/os-release."

    # shellcheck disable=SC1091
    source /etc/os-release
    local distro_ids=" ${ID:-} ${ID_LIKE:-} "

    if [[ "$distro_ids" == *" debian "* || "$distro_ids" == *" ubuntu "* ]]; then
        PKG_MANAGER="apt-get"
        PODMAN_PACKAGE="podman"
        DOCKER_PACKAGE="docker.io"
    elif [[ "$distro_ids" == *" fedora "* || "$distro_ids" == *" rhel "* || "$distro_ids" == *" centos "* ]]; then
        PKG_MANAGER="dnf"
        PODMAN_PACKAGE="podman"
        # RHEL y derivados no incluyen Docker en sus repositorios nativos.
        if [[ ${ID:-} == "fedora" ]]; then
            DOCKER_PACKAGE="moby-engine"
        fi
    elif [[ "$distro_ids" == *" arch "* ]]; then
        PKG_MANAGER="pacman"
        PODMAN_PACKAGE="podman"
        DOCKER_PACKAGE="docker"
    elif [[ "$distro_ids" == *" suse "* || "$distro_ids" == *" opensuse "* ]]; then
        PKG_MANAGER="zypper"
        PODMAN_PACKAGE="podman"
        DOCKER_PACKAGE="docker"
    fi
}

build_install_command() {
    local package=$1

    case "$PKG_MANAGER" in
        apt-get)
            INSTALL_COMMAND=(sudo apt-get install -y "$package")
            ;;
        dnf)
            INSTALL_COMMAND=(sudo dnf install -y "$package")
            ;;
        pacman)
            INSTALL_COMMAND=(sudo pacman -S --needed --noconfirm "$package")
            ;;
        zypper)
            INSTALL_COMMAND=(sudo zypper --non-interactive install "$package")
            ;;
        *)
            return 1
            ;;
    esac
}

print_manual_instructions() {
    echo
    echo "[i] Instalación manual sugerida para ${NAME:-esta distribución}:"

    if [[ -n "$PODMAN_PACKAGE" ]]; then
        build_install_command "$PODMAN_PACKAGE"
        printf '  Podman: '
        printf '%q ' "${INSTALL_COMMAND[@]}"
        printf '\n'
    else
        echo "  Podman: https://podman.io/docs/installation"
    fi

    if [[ -n "$DOCKER_PACKAGE" ]]; then
        build_install_command "$DOCKER_PACKAGE"
        printf '  Docker: '
        printf '%q ' "${INSTALL_COMMAND[@]}"
        printf '\n'
    else
        echo "  Docker: https://docs.docker.com/engine/install/"
    fi
    echo "  Si Docker no está activo: sudo systemctl enable --now docker"
    echo "  Si falta acceso: sudo usermod -aG docker $USER_NAME"
    echo "    El grupo docker equivale a acceso root; después de añadirlo, inicie una nueva sesión."

    echo "  Después de instalar el motor, vuelva a ejecutar ./install.sh."
}

confirm_command() {
    local prompt=$1
    shift
    local reply

    printf '\n[i] Comando: '
    printf '%q ' "$@"
    printf '\n'
    read -r -p "$prompt [s/N]: " reply || reply=""
    [[ "$reply" =~ ^[sSyY]$ ]]
}

install_engine() {
    local selected=$1
    local package

    if [[ "$selected" == "podman" ]]; then
        package=$PODMAN_PACKAGE
    else
        package=$DOCKER_PACKAGE
    fi

    if [[ -z "$package" ]] || ! build_install_command "$package"; then
        echo "[!] No hay instalación automática de $selected para esta distribución." >&2
        print_manual_instructions
        exit 1
    fi

    command -v "$PKG_MANAGER" >/dev/null 2>&1 || die "No se encontró el gestor de paquetes $PKG_MANAGER."
    require_sudo

    if ! confirm_command "¿Ejecutar la instalación de $selected?" "${INSTALL_COMMAND[@]}"; then
        print_manual_instructions
        exit 0
    fi

    "${INSTALL_COMMAND[@]}"
    ENGINE=$selected

    if [[ "$selected" == "podman" ]]; then
        engine_works podman || die "Podman se instaló, pero 'podman info' falló. Revise la configuración rootless y vuelva a intentarlo."
    else
        configure_docker
    fi
}

configure_docker() {
    if engine_works docker; then
        return
    fi

    if command -v systemctl >/dev/null 2>&1 && ! systemctl is-active --quiet docker; then
        require_sudo
        if confirm_command "¿Habilitar e iniciar el servicio Docker?" sudo systemctl enable --now docker; then
            sudo systemctl enable --now docker
        else
            die "Inicie el servicio Docker y vuelva a ejecutar el instalador."
        fi
    fi

    if ! id -nG "$USER_NAME" | grep -qw docker; then
        echo
        echo "[!] Pertenecer al grupo 'docker' equivale a conceder privilegios de root."
        require_sudo
        if confirm_command "¿Añadir $USER_NAME al grupo docker?" sudo usermod -aG docker "$USER_NAME"; then
            sudo usermod -aG docker "$USER_NAME"
        else
            die "Añada el usuario al grupo docker manualmente o configure Docker rootless."
        fi
    fi

    if engine_works docker; then
        return
    fi

    if ! id -nG | grep -qw docker && id -nG "$USER_NAME" | grep -qw docker; then
        die "La pertenencia al grupo docker se aplicará al iniciar una nueva sesión. Cierre sesión, vuelva a entrar y ejecute ./install.sh otra vez."
    fi

    die "Docker se instaló, pero 'docker info' sigue fallando. Revise el servicio y los permisos antes de volver a intentarlo."
}

handle_missing_engine() {
    local choice

    echo
    echo "[i] No se encontró Podman ni Docker."
    echo "    Podman es la opción recomendada: funciona sin root y normalmente no requiere un daemon permanente."
    echo "    Docker también es compatible, pero suele usar un daemon; su grupo 'docker' concede privilegios equivalentes a root."
    echo
    echo "    1) Instalar Podman (recomendado)"
    echo "    2) Instalar Docker"
    echo "    3) Mostrar comandos y salir (predeterminado)"

    if [[ ! -t 0 ]]; then
        print_manual_instructions
        exit 1
    fi

    read -r -p "Seleccione una opción [1/2/3]: " choice || choice="3"
    case "${choice:-3}" in
        1)
            install_engine podman
            ;;
        2)
            install_engine docker
            ;;
        3)
            print_manual_instructions
            exit 0
            ;;
        *)
            die "Opción no válida."
            ;;
    esac
}

select_engine() {
    local candidate
    local found=0

    if [[ -n ${LAZYAUDIT_ENGINE:-} ]]; then
        ENGINE=$LAZYAUDIT_ENGINE
        [[ "$ENGINE" == "podman" || "$ENGINE" == "docker" ]] || die "LAZYAUDIT_ENGINE debe ser 'podman' o 'docker'."
        command -v "$ENGINE" >/dev/null 2>&1 || die "No se encontró el ejecutable $ENGINE."
        if ! "$ENGINE" info >/dev/null; then
            die "$ENGINE está instalado, pero no es accesible. Revise su servicio, permisos o configuración rootless."
        fi
        return
    fi

    for candidate in podman docker; do
        if command -v "$candidate" >/dev/null 2>&1; then
            found=1
            if engine_works "$candidate"; then
                ENGINE=$candidate
                return
            fi
        fi
    done

    if [[ $found -eq 0 ]]; then
        handle_missing_engine
        return
    fi

    for candidate in podman docker; do
        if command -v "$candidate" >/dev/null 2>&1; then
            echo "[!] Diagnóstico de $candidate:" >&2
            "$candidate" info >/dev/null || true
        fi
    done
    die "Hay motores instalados, pero ninguno es accesible para $USER_NAME."
}

generate_wrapper() {
    WRAPPER_TMP=$(mktemp)
    cat >"$WRAPPER_TMP" <<EOF
#!/usr/bin/env bash
set -eu

CONTAINER_ENGINE="$ENGINE"
IMAGE_NAME="$IMAGE_NAME"
INBOX_DIR="\$HOME/.lazyaudit/inbox"
mkdir -p "\$INBOX_DIR"

if [ \$# -eq 0 ]; then
    exec "\$CONTAINER_ENGINE" run -it --rm \\
        -v lazyaudit_data:/app/lazyaudit/data \\
        -v "\$INBOX_DIR":/app/inbox:ro,Z \\
        "\$IMAGE_NAME"
else
    exec "\$CONTAINER_ENGINE" run -i --rm \\
        -v lazyaudit_data:/app/lazyaudit/data \\
        -v "\$INBOX_DIR":/app/inbox:ro,Z \\
        "\$IMAGE_NAME" "\$@"
fi
EOF
}

main() {
    [[ $EUID -ne 0 ]] || die "No ejecute el instalador como root ni con sudo. Use un usuario regular; sudo se solicitará solo cuando sea necesario."
    [[ -f "$SCRIPT_DIR/Dockerfile" && -f "$SCRIPT_DIR/lazyaudit/requirements.txt" ]] || die "No se encontraron los archivos necesarios junto a install.sh."
    command -v install >/dev/null 2>&1 || die "No se encontró el comando 'install'."

    load_distro
    select_engine
    require_sudo

    echo "[+] Compilando imagen $IMAGE_NAME con $ENGINE..."
    "$ENGINE" build -t "$IMAGE_NAME" "$SCRIPT_DIR"

    echo "[+] Instalando ejecutable 'lazyaudit' en /usr/local/bin..."
    generate_wrapper
    sudo install -m 0755 "$WRAPPER_TMP" "$WRAPPER_PATH"

    echo "[+] Instalación finalizada con éxito usando $ENGINE."
}

main "$@"
