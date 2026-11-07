# CHANGELOG — LazyAudit

Todos los cambios notables, adiciones y correcciones de LazyAudit están documentados en este archivo.
El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

---

## [Unreleased] - 2026-11-07

### Añadido (Added)
- **TUI Completa con Textual & Rich (`TUI/`):**
  - Implementación de **7 pestañas operativas**:
    - `ProjectsTab`: Gestión de contexto, activación de proyectos en caliente y métricas en vivo.
    - `CommandsTab`: Biblioteca de comandos, visualización de plantillas raw y renderizado con interpolación en vivo.
    - `VariablesTab`: Gestión de variables locales y globales.
    - `FindingsTab`: Registro de hallazgos por host, severidades (`LOW`, `MEDIUM`, `HIGH`) y CVEs.
    - `HostsTab`: Inventario de infraestructura descubierta, puertos y servicios.
    - `ChecklistsTab`: Vista sincronizada jerárquica (Grupos + Tareas) con conteo de avance numérico `[hechas/total]` y alternancia rápida con tecla `Space`.
    - `WorkflowsTab`: Detección automática de scripts Bash/Python y panel de consola de ejecución integrada (`RichLog`).
  - **Ejecución en Streaming Asíncrono para Workflows:**
    - Worker en segundo plano con `@work(thread=True)` conectado a `subprocess.Popen(bufsize=1)`.
    - Emisión en tiempo real línea a línea de `stdout` y `stderr` sin bloquear ni congelar la interfaz.
  - **Catálogo de Modales Interactivos (`TUI/modals/`):**
    - Modales para creación (`add`), edición (`modify`) y eliminación confirmada (`remove`) en todos los módulos.
    - Navegación rápida con teclado (`Left`/`Right` para alternar botones, `Escape` para cancelar).
- **CLI Exhaustiva (`utils/main.py`):**
  - Soporte completo para CRUD de los 7 módulos con `argparse`.
  - Integración de búsqueda difusa (`rapidfuzz`) con el modificador `-s` / `--search` en todos los listados.
  - Ejecución de workflows en vivo desde terminal con `-xw <INDEX>`.
- **Documentación Técnica y Operativa:**
  - `documentacion_tui_lazyaudit.md`: Arquitectura, ciclo de vida de modales y atajos de teclado.
  - `documentacion_cli_lazyaudit.md`: Manual operativo con ejemplos prácticos de comandos y modificadores.

### Cambiado (Changed)
- `utils/actions.py`:
  - `Workflow.run()` refactorizado a generador con `yield` para emitir líneas en streaming tanto a la CLI como a la TUI.
  - Corrección de pase de argumentos (`str(workflow.path)`) evitando abrir strings de representación del modelo.
- `TUI/tabs/projects.py`:
  - Corrección del ID de pestaña a `id="projects_tab"`, resolviendo la colisión `MountError` con `workflows_tab`.
- `TUI/tabs/checklists.py`:
  - Optimización en `load_tasks()` y `load_groups()` para montaje limpio en Textual y retención de cursor.

---

## [0.2.0] - 2026-11-04

### Añadido (Added)
- Módulo de **Checklists** metodológicos en CLI y persistencia JSON (`global_checklists.json` y privados).
- Módulo de **Workflows** para scripts ejecutables locales y globales.
- Script de previsualización estética con Rich en `el_rincon_de_gemini/preview_lazyaudit.py`.

### Cambiado (Changed)
- Normalización de modelos en `utils/models.py` usando `@dataclass` (`CommandData`, `VariableData`, `ProjectData`, `HostData`, `FindingData`, `ChecklistData`, `WorkflowData`).
- Implementación de recarga dinámica de rutas con `PATHS.reload_paths()` al cambiar de proyecto.

---

## [0.1.0] - 2026-10-30

### Añadido (Added)
- Estructura base del proyecto y motor de persistencia local en `utils/common.py`.
- Separación de alcances `GLOBAL` y `PRIVATE` en almacenamiento JSON.
- Interpolación de variables `{VARIABLE}` dentro de los comandos.
- Configuración inicial de despliegue seguro en Docker (`project_info/docker-compose.yaml`).
- Configuración del proyecto activo vía `data/config.json`.
