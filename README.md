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
- Linux con **Podman** (recomendado para ejecución rootless) o **Docker**.
- Permisos `sudo` para instalar el ejecutable en `/usr/local/bin`.

### 1. Clonar el repositorio
```bash
git clone https://github.com/franlumer/LazyAudit.git
cd LazyAudit
```

### 2. Instalar
Ejecutá el script de instalación automatizado:
```bash
chmod +x install.sh uninstall.sh
./install.sh
```

El script se encargará de:
1. Compilar la imagen del contenedor `lazyaudit:1.0.0`.
2. Crear la carpeta buzón para importar scripts en `$HOME/.lazyaudit/inbox`.
3. Instalar el wrapper ejecutable `lazyaudit` en `/usr/local/bin/`.

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
El script te preguntará si querés conservar o eliminar el volumen persistente de datos (`lazyaudit_data`).

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
