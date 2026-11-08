# 🛡️ LazyAudit

**LazyAudit** es un entorno de trabajo integral basado en una Interfaz de Usuario de Texto (TUI) diseñado para optimizar el flujo de tareas en auditorías de ciberseguridad ofensiva (Pentesting, Red Teaming, Ethical Hacking). Permite aislar proyectos, gestionar comandos con interpolación automática de variables, ejecutar flujos de trabajo (workflows) y mantener una trazabilidad inmutable mediante logs automáticos.

## ⚙️ Características Clave

- **Aislamiento de Proyectos:** Gestión de contextos separados. Los hosts, variables y hallazgos no se cruzan entre auditorías.
- **Interpolación Dinámica:** Biblioteca de comandos reutilizables que interpolan automáticamente variables locales (ej. {RHOST}, {DOMAIN}).
- **Workflows Automatizados:** Ejecución secuencial de herramientas de auditoría mediante archivos de configuración (Playbooks).
- **Gestión de Auditoría:** Registro centralizado de hosts comprometidos, vulnerabilidades (hallazgos) y seguimiento de metodologías mediante Checklists (OWASP, PTES).
- **Trazabilidad (Logs):** Registro inmutable en formato JSONL de cada comando ejecutado, herramienta invocada y resultado obtenido.
- **Despliegue Seguro:** Contenerización vía Docker aplicando el principio de mínimo privilegio para aislar el entorno operativo del sistema anfitrión.

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.12+
- **Interfaz (TUI):** Textual & Rich
- **Almacenamiento:** JSON / JSONL (Orientado a archivos locales de alta velocidad)
- **Despliegue:** Docker & Docker Compose

## 🔐 Consideraciones de Seguridad

LazyAudit asume un modelo de **responsabilidad compartida**. La herramienta sanitiza los inputs para prevenir ataques de *path traversal* y gestiona el aislamiento de volúmenes en Docker (configurado en modo de solo lectura con excepciones estrictas). Sin embargo, el auditor es responsable de validar los comandos ejecutados en los *workflows* y de no almacenar secretos en texto plano (como contraseñas o hashes operativos) en las variables globales.

***Carpeta Inbox (Buzón de Entrada de Workflows)***

Colocá acá los scripts `.sh` o `.py` que quieras importar a LazyAudit.
El contenedor los lee en modo solo lectura (`/app/inbox/script.py`) y la herramienta los copia de forma segura
dentro del volumen protegido.

## 👨‍💻 Autor
**Franco Luciano Merlo** (franlumer)
*Licenciatura en Seguridad Informática - Universidad Siglo 21*

___

Actualmente LazyAudit se encuentra en una fase extremadamente temprana dentro de su ciclo de vida, actualmente presentado como un bosquejo de su potencial. LazyAudit prevé la integración de numerosas herramientas y funcionalidades con el objetivo de facilitar la integración de automatizaciones, la organización y estructuración de información recogida durante las auditorías y la información generada para reportes empresariales. Más actualizaciones pronto...
