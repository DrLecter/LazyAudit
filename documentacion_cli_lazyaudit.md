# Manual Operativo y Referencia Técnica: CLI de LazyAudit

Documentación integral de la **Interfaz de Línea de Comandos (CLI)** de LazyAudit ([`utils/main.py`](file:///home/luciano/github/LazyAudit/utils/main.py)), basada en `argparse` y conectada con la capa de persistencia y modelos ([`utils/actions.py`](file:///home/luciano/github/LazyAudit/utils/actions.py)).

---

## 1. Convenciones y Estructura de Uso

```bash
python3 utils/main.py [OPERACIÓN] [PARÁMETROS] [MODIFICADORES]
```

### Reglas de Ámbitos (Scope)
- **PRIVATE (por defecto):** Afecta únicamente al proyecto activo (`data/projects/<ACTIVE_PROJECT>/`).
- **GLOBAL (`--global`):** Afecta al almacén global compartido entre auditorías (`data/globals/`).

### Búsqueda Difusa Integrada (`-s` / `--search`)
Cualquier comando de listado admite `-s <QUERY>` para buscar por coincidencia aproximada (`fuzz.partial_ratio >= 86`) en todos los campos de texto y listas.

---

## 2. Referencia de Módulos y Comandos

### 1. Proyectos (`Projects`)
Gestión del contexto de auditoría y proyectos activos.

| Argumento | Parámetros | Descripción |
| :--- | :--- | :--- |
| `-lp`, `--list-projects` | Ninguno | Lista los proyectos registrados. Admite `--active`, `-v` (verbose) y `-s`. |
| `-ap`, `--add-project` | `NAME` `DESC` `STATUS` | Crea un nuevo proyecto (`STATUS`: `active`, `paused`, `finished`). |
| `-cp`, `--change-project`| `NAME` | Cambia el proyecto activo y recarga en caliente los punteros JSON. |
| `-mp`, `--modify-project`| Ninguno | Modifica el proyecto activo usando modificadores (`--name`, `--description`, `--status`). |
| `-rp`, `--remove-project`| `NAME` | Elimina la carpeta del proyecto (no permite borrar el proyecto activo). |

**Ejemplos:**
```bash
# Listar proyectos con detalles
python3 utils/main.py -lp -v

# Ver únicamente el proyecto activo
python3 utils/main.py -lp --active

# Crear un proyecto nuevo
python3 utils/main.py -ap audit_corp "Auditoría interna de red" active

# Cambiar de proyecto activo
python3 utils/main.py -cp audit_corp
```

---

### 2. Comandos (`Commands`)
Biblioteca de comandos con plantillas e interpolación automática de `{VARIABLES}`.

| Argumento | Parámetros | Descripción |
| :--- | :--- | :--- |
| `-lc`, `--list-commands` | Ninguno | Lista comandos interpolados. Con `--raw` muestra la plantilla sin evaluar. |
| `-ac`, `--add-command` | `TITLE` `CMD` `DESC` `TAGS` | Agrega un comando (separar tags por comas). Admite `--global`. |
| `-mc`, `--modify-command` | `INDEX` | Modifica el comando según modificadores (`--title`, `--command`, `--tags`, `--scope`). |
| `-rc`, `--remove-command` | `INDEX` | Elimina el comando según su índice. |

**Ejemplos:**
```bash
# Crear comando privado con interpolación
python3 utils/main.py -ac "Escaneo SMB" "crackmapexec smb {RHOST} -u {USER} -p {PASS}" "Enumera shares" "smb,enum,ad"

# Crear comando global
python3 utils/main.py -ac "Nmap Full" "nmap -p- -sV {RHOST}" "Escaneo total" "recon,nmap" --global

# Listar comandos evaluados con las variables actuales
python3 utils/main.py -lc

# Listar plantillas raw buscando "smb"
python3 utils/main.py -lc --raw -s smb
```

---

### 3. Variables (`Variables`)
Almacén de valores que se sustituyen en los comandos (`{KEY} -> VALUE`).

| Argumento | Parámetros | Descripción |
| :--- | :--- | :--- |
| `-lv`, `--list-variables`| Ninguno | Lista variables disponibles (locales y globales). Admite `-s`. |
| `-av`, `--add-variable` | `KEY` `VALUE` `DESC` | Crea una variable. Por defecto es privada; usar `--global` para compartirla. |
| `-mv`, `--modify-variable`| `INDEX` | Modifica una variable (`--key`, `--value`, `--description`, `--scope`). |
| `-rv`, `--remove-variable`| `INDEX` | Elimina la variable por índice. |

**Ejemplos:**
```bash
# Definir IP objetivo del proyecto activo
python3 utils/main.py -av RHOST 10.10.10.50 "Host bajo auditoría"

# Definir IP atacante global
python3 utils/main.py -av LHOST 192.168.1.100 "IP de interfaz tun0" --global

# Modificar valor de una variable
python3 utils/main.py -mv 0 --value 10.10.10.75
```

---

### 4. Hallazgos / Vulnerabilidades (`Findings`)
Registro estructurado de hallazgos para el informe de pentesting.

| Argumento | Parámetros | Descripción |
| :--- | :--- | :--- |
| `-lf`, `--list-findings` | Ninguno | Lista todos los hallazgos del proyecto activo. |
| `-af`, `--add-finding` | `HOST` `DESC` `VULNS` `SEV` | Registra hallazgo (`SEV`: `low`, `medium`, `high`. `VULNS` separadas por comas). |
| `-mf`, `--modify-finding` | `INDEX` | Modifica hallazgo (`--host`, `--description`, `--vulns`, `--severity`). |
| `-rf`, `--remove-finding` | `INDEX` | Elimina el hallazgo por índice. |

**Ejemplos:**
```bash
# Registrar vulnerabilidad crítica
python3 utils/main.py -af 10.10.10.50 "Servidor Apache expone .git" "Information Disclosure,Git Exposure" high

# Listar buscando vulnerabilidades web
python3 utils/main.py -lf -s Apache
```

---

### 5. Clientes / Activos (`Hosts`)
Inventario de hosts y servicios descubiertos.

| Argumento | Parámetros | Descripción |
| :--- | :--- | :--- |
| `-lh`, `--list-hosts` | Ninguno | Lista los hosts registrados en el proyecto activo. |
| `-ah`, `--add-host` | `IP` `HOSTNAME` `PORTS` `SERVICES` | Añade un host (puertos y servicios separados por coma). |
| `-mh`, `--modify-host` | `INDEX` | Modifica el host (`--ip`, `--hostname`, `--ports`, `--services`). |
| `-rh`, `--remove-host` | `INDEX` | Elimina el host por índice. |

**Ejemplos:**
```bash
python3 utils/main.py -ah 10.10.10.50 srv01.corp.local "80,443,445" "http,https,smb"
python3 utils/main.py -lh
```

---

### 6. Checklists Metodológicos (`Checklists`)
Seguimiento de tareas y marcos de auditoría (OWASP, PTES, Active Directory).

| Argumento | Parámetros | Descripción |
| :--- | :--- | :--- |
| `-lck`, `--list-checklists` | Ninguno | Lista tareas agrupadas por categoría con marcas `[X]` o `[ ]`. |
| `-ack`, `--add-checklist` | `GROUP` `TASK` | Crea una tarea en el grupo especificado. Admite `--global`. |
| `-mck`, `--modify-checklist`| `GROUP` | Modifica el grupo o tarea (`--item <N>`, `--toggle`, `--task`, `--scope`). |
| `-rck`, `--remove-checklist`| `GROUP` | Elimina el grupo entero o una tarea puntual si se pasa `--item <N>`. |

**Ejemplos:**
```bash
# Agregar tarea a un grupo
python3 utils/main.py -ack "Active Directory" "Enumeración de certificados AD CS"

# Conmutar estado de tarea (completar o desmarcar con --toggle)
python3 utils/main.py -mck "Active Directory" --item 1 --toggle

# Eliminar solo la tarea 2 del grupo
python3 utils/main.py -rck "Active Directory" --item 2
```

---

### 7. Workflows Automatizados (`Workflows`)
Automatización mediante ejecución de scripts Python o Bash.

| Argumento | Parámetros | Descripción |
| :--- | :--- | :--- |
| `-lw`, `--list-workflows` | Ninguno | Lista scripts disponibles y su ámbito (`GLOBAL` o `PRIVATE`). |
| `-aw`, `--add-workflow` | `PATH` | Copia un script local al proyecto activo (o global con `--global`). |
| `-xw`, `--run` | `INDEX` | **Ejecuta el workflow en streaming en vivo** imprimiendo la salida en consola. |
| `-rw`, `--remove-workflow`| `INDEX` | Borra el script de la carpeta de workflows. |

**Ejemplos:**
```bash
# Añadir script privado al proyecto activo
python3 utils/main.py -aw /home/auditor/scripts/recon_ad.sh

# Añadir script global para todas las auditorías
python3 utils/main.py -aw /home/auditor/scripts/nmap_parser.py --global

# Ejecutar el workflow con índice 0 en tiempo real
python3 utils/main.py -xw 0
```

---

## 3. Modificadores Globales (`Modifiers`)

| Modificador | Tipo / Opciones | Uso |
| :--- | :--- | :--- |
| `-s`, `--search` | String | Filtro difuso aplicado a cualquier listado. |
| `--global` | Flag booleano | Asigna ámbito `GLOBAL` al crear recursos. |
| `--active` | Flag booleano | Filtra para ver únicamente el proyecto activo en `-lp`. |
| `-v`, `--verbose`| Flag booleano | Muestra salida ampliada de proyectos. |
| `--raw` | Flag booleano | Muestra los comandos sin interpolar sus variables. |
| `--toggle` | Flag booleano | Conmuta `done` en tareas de checklist. |
| `--title`, `--command`, `--description`, `--tags` | String | Modificadores para comandos. |
| `--key`, `--value` | String | Modificadores para variables. |
| `--ip`, `--hostname`, `--ports`, `--services` | String | Modificadores para hosts. |
| `--host`, `--vulns`, `--severity` | String / Choices (`low`, `medium`, `high`) | Modificadores para hallazgos. |
