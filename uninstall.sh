#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="lazyaudit:1.0.0"
VOLUME_NAME="lazyaudit_data"
WRAPPER_PATH="/usr/local/bin/lazyaudit"
ENGINE=""

die() {
    echo "[!] $*" >&2
    exit 1
}

engine_works() {
    local engine=$1
    command -v "$engine" >/dev/null 2>&1 && "$engine" info >/dev/null 2>&1
}

select_engine() {
    local candidate
    local fallback=""
    local resource_engine=""

    if [[ -n ${LAZYAUDIT_ENGINE:-} ]]; then
        ENGINE=$LAZYAUDIT_ENGINE
        [[ "$ENGINE" == "podman" || "$ENGINE" == "docker" ]] || die "LAZYAUDIT_ENGINE debe ser 'podman' o 'docker'."
        engine_works "$ENGINE" || die "$ENGINE no está instalado o no es accesible para este usuario."
        return
    fi

    # Buscar tanto la imagen como un volumen conservado de una desinstalación anterior.
    for candidate in podman docker; do
        if engine_works "$candidate"; then
            if [[ -z "$fallback" ]]; then
                fallback=$candidate
            fi
            if "$candidate" image inspect "$IMAGE_NAME" >/dev/null 2>&1 ||
                "$candidate" volume inspect "$VOLUME_NAME" >/dev/null 2>&1; then
                if [[ -n "$resource_engine" && "$resource_engine" != "$candidate" ]]; then
                    die "Hay recursos de LazyAudit en Podman y Docker. Use LAZYAUDIT_ENGINE para elegir cuál desinstalar."
                fi
                resource_engine=$candidate
            fi
        fi
    done

    if [[ -n "$resource_engine" ]]; then
        ENGINE=$resource_engine
    else
        ENGINE=$fallback
    fi
}

main() {
    local confirm=""

    [[ $EUID -ne 0 ]] || die "No ejecute el desinstalador como root ni con sudo. Use el mismo usuario que instaló LazyAudit."

    echo "[+] Desinstalando LazyAudit..."

    select_engine

    if [[ -f "$WRAPPER_PATH" ]]; then
        echo "[+] Eliminando $WRAPPER_PATH..."
        command -v sudo >/dev/null 2>&1 || die "Se requiere sudo para eliminar $WRAPPER_PATH."
        sudo rm -f "$WRAPPER_PATH"
    fi

    if [[ -z "$ENGINE" ]]; then
        echo "[!] No se encontró un motor accesible; no se eliminaron la imagen ni el volumen." >&2
        echo "[+] Desinstalación del ejecutable finalizada."
        return
    fi

    echo "[+] Usando $ENGINE..."
    if "$ENGINE" image inspect "$IMAGE_NAME" >/dev/null 2>&1; then
        echo "[+] Eliminando imagen de contenedor $IMAGE_NAME..."
        "$ENGINE" rmi "$IMAGE_NAME"
    fi

    if "$ENGINE" volume inspect "$VOLUME_NAME" >/dev/null 2>&1; then
        read -r -p "[?] ¿Desea eliminar el volumen de datos persistente ($VOLUME_NAME)? [s/N]: " confirm || confirm=""
        if [[ "$confirm" =~ ^[sSyY]$ ]]; then
            echo "[+] Eliminando volumen $VOLUME_NAME..."
            "$ENGINE" volume rm -f "$VOLUME_NAME"
            echo "[+] Volumen eliminado."
        else
            echo "[+] Volumen de datos conservado."
        fi
    fi

    echo "[+] LazyAudit desinstalado por completo."
}

main "$@"
