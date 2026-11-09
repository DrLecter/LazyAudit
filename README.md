# 🛡️ LazyAudit

**LazyAudit** es un entorno de trabajo integral basado en una Interfaz de Usuario de Texto (TUI) y CLI diseñado para optimizar el flujo de tareas en auditorías de ciberseguridad ofensiva (Pentesting, Red Teaming, Ethical Hacking). Permite aislar proyectos, gestionar comandos con interpolación automática de variables, ejecutar flujos de trabajo (workflows) y mantener una trazabilidad inmutable mediante logs automáticos.

---

## ⚙️ Características Clave

- **Aislamiento de Proyectos:** Gestión de contextos separados. Los hosts, variables y hallazgos no se cruzan entre auditorías.
- **Interpolación Dinámica:** Biblioteca de comandos reutilizables que interpolan automáticamente variables locales (ej. `{RHOST}`, `{DOMAIN}`).
- **Workflows Automatizados:** Ejecución de scripts (`.sh` o `.py`) con streaming de salida en vivo y control estricto de timeout.
- **Gestión de Auditoría:** Registro centralizado de hosts comprometidos, vulnerabilidades (hallazgos) y seguimiento de metodologías mediante Checklists (OWASP, Active Directory, Infraestructura).
- **Trazabilidad (Logs Inmutables):** Registro automático en formato JSONL (`0o600`) de cada comando ejecutado, host añadido, workflow invocado y proyecto modificado.
- **Despliegue Seguro:** Contenerización con Podman/Docker ejecutándose bajo usuario sin privilegios (`audit`, UID 1000) y capacidades de red específicas para escaneo (`setcap`).

---

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Linux, Bash y un usuario regular (no ejecutar el instalador como `root`).
- Permisos `sudo` para instalar paquetes, configurar Docker cuando sea necesario y copiar el ejecutable a `/usr/local/bin`.
- **Podman** (recomendado para ejecución rootless y sin daemon permanente) o **Docker**.

Si no hay ningún motor instalado, el instalador puede instalarlo desde los repositorios nativos en Debian/Ubuntu, Fedora/RHEL, Arch y openSUSE, según disponibilidad. También permite salir y mostrar los comandos para hacerlo manualmente. No añade repositorios de terceros automáticamente.

### 1. Clonar el repositorio
```bash
git clone https://github.com/franlumer/LazyAudit.git
cd LazyAudit
```

### 2. Instalar
Ejecutá el script de instalación automatizado con tu usuario regular:
```bash
chmod +x install.sh uninstall.sh
./install.sh
```

**No uses `sudo ./install.sh`**: la imagen y los datos deben pertenecer al usuario que ejecutará LazyAudit. El script solicitará `sudo` únicamente para instalar paquetes, aplicar la configuración de Docker que confirmes y copiar el ejecutable.

El script se encargará de:
1. Detectar Podman o Docker y comprobar que el usuario pueda utilizarlo. Si ambos están disponibles, prioriza Podman.
2. Ofrecer instalar un motor si no hay ninguno, explicando las implicaciones de seguridad, o mostrar los comandos manuales.
3. Compilar la imagen del contenedor `lazyaudit:1.0.0` con el motor seleccionado.
4. Instalar el wrapper ejecutable `lazyaudit` en `/usr/local/bin/`. La carpeta `$HOME/.lazyaudit/inbox` se crea al ejecutarlo.

Podés forzar el motor cuando ambos están instalados:
```bash
LAZYAUDIT_ENGINE=podman ./install.sh
LAZYAUDIT_ENGINE=docker ./install.sh
```

Si un motor está instalado pero no accesible, ejecutá `podman info` o `docker info` para ver el diagnóstico. En Docker puede ser necesario habilitar el servicio (`sudo systemctl enable --now docker`) y añadir el usuario al grupo `docker`. Esta última acción otorga privilegios equivalentes a `root` y requiere iniciar una nueva sesión. El instalador nunca utiliza `sudo docker` para eludir estos controles.

---

## 💻 Uso

Podés utilizar LazyAudit tanto en modo interactivo (TUI) como directamente por línea de comandos (CLI).

### Modo Interactivo (TUI)
Para iniciar la interfaz gráfica de terminal:
```bash
lazyaudit
```
**Atajos dentro de la TUI:**
- `1` a `7` / flechas: Navegación entre solapas (Proyectos, Comandos, Variables, Hallazgos, Hosts, Checklists, Workflows).
- `N`: Añadir nuevo elemento (proyecto, comando, host, workflow, etc.).
- `E`: Editar elemento seleccionado.
- `R`: Eliminar elemento.
- `X`: Ejecutar workflow seleccionado.
- `ESPACIO`: Marcar / desmarcar tarea en Checklists.
- `D`: Alternar tema claro / oscuro.
- `ESC`: Cancelar o cerrar modal.

---

### Modo Línea de Comandos (CLI)
LazyAudit incluye soporte completo para scripts y automatizaciones por terminal:

```bash
# Ver ayuda completa de comandos
lazyaudit --help

# Proyectos
lazyaudit -lp                                      # Listar proyectos
lazyaudit -ap "Cliente_ACME" "Auditoría interna" active   # Crear proyecto
lazyaudit -cp "Cliente_ACME"                       # Cambiar proyecto activo

# Hosts
lazyaudit -lh                                      # Listar hosts
lazyaudit -ah "192.168.1.10" "dc01.local" "88,389,445" "kerberos,ldap,smb"  # Agregar host

# Variables
lazyaudit -lv                                      # Listar variables
lazyaudit -av "RHOST" "192.168.1.10" "Target principal"  # Variable privada
lazyaudit -av "LHOST" "10.10.14.5" "IP local atacante" --global  # Variable global

# Comandos
lazyaudit -lc                                      # Listar comandos disponibles
lazyaudit -ac "Nmap Full" "nmap -p- -sV {RHOST}" "Escaneo completo" "nmap,recon"

# Workflows
lazyaudit -lw                                      # Listar workflows
lazyaudit -aw mi_script.py                         # Importar workflow desde inbox
lazyaudit -xw 0                                    # Ejecutar workflow por índice

# Checklists
lazyaudit -lck                                     # Listar tareas y progreso
```

---

## 📥 Importar Scripts y Workflows (Buzón Inbox)

Para añadir scripts `.sh` o `.py` de forma segura dentro del entorno aislado:

1. Copiá tu archivo en tu carpeta inbox local:
   ```bash
   cp mi_script.py ~/.lazyaudit/inbox/
   ```
2. Importalo en LazyAudit usando solo su nombre:
   - Desde la **TUI**: Solapa *Workflows* -> <kbd>N</kbd> -> ingresá `mi_script.py`.
   - Desde la **CLI**:
     ```bash
     lazyaudit -aw mi_script.py
     ```

---

## 🗑️ Desinstalación

Si deseás desinstalar LazyAudit de tu sistema:
```bash
./uninstall.sh
```
El script detectará el motor que contiene la imagen o el volumen persistente y te preguntará si querés conservar o eliminar los datos de `lazyaudit_data`. Si hay recursos en ambos motores, te pedirá una selección explícita; también podés indicarla manualmente:
```bash
LAZYAUDIT_ENGINE=docker ./uninstall.sh
```
Ejecutá el desinstalador con el mismo usuario regular que instaló LazyAudit, sin `sudo` delante del comando.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.12+
- **Interfaz (TUI):** Textual & Rich
- **Almacenamiento:** JSON / JSONL (auditoría estructurada inmutable)
- **Contenerización:** Podman & Docker (rootless, capacidades de red acotadas)

---

## 🔐 Consideraciones de Seguridad

LazyAudit aplica el principio de **mínimo privilegio**:
- Sanitización de entradas contra vulnerabilidades de *Path Traversal* (`..`, `/`, `\`).
- Contenedores ejecutados bajo usuario no-root (`audit`).
- Binarios de red acotados vía `setcap` (evitando otorgar permisos de `root` para escaneos de paquetes crudos como Nmap SYN scan).
- Logs protegidos con permisos restrictivos `0o600` para garantizar confidencialidad e integridad del registro de auditoría.

---

## 👨‍💻 Autor
**Franco Luciano Merlo** (franlumer)  
*Licenciatura en Seguridad Informática - Universidad Siglo 21*
