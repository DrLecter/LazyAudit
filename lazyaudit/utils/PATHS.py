from pathlib import Path
import json

# ========== LAZYAUDIT PATHS ==========
LAZYAUDIT_DIR = Path(__file__).resolve().parent.parent
UTILS_DIR = LAZYAUDIT_DIR/"utils"
TUI_DIR = LAZYAUDIT_DIR/"TUI" 

DATA_DIR = LAZYAUDIT_DIR/"data"
GLOBAL_DIR = LAZYAUDIT_DIR/"data"/"globals"
CONFIG_FILE = DATA_DIR/"config.json"
PROJECTS_DIR = DATA_DIR / "projects"
LOGS_DIR = DATA_DIR/"logs"
LOGS_FILE = LOGS_DIR/"lazyaudit.jsonl"
INBOX_DIR = Path("/app/inbox")
# ========== GLOBAL PATHS ==========
GLOBAL_COMMANDS_FILE = GLOBAL_DIR/"global_commands.json"
GLOBAL_VARS_FILE = GLOBAL_DIR/"global_vars.json"
GLOBAL_CHECKLISTS_FILE = GLOBAL_DIR / "global_checklists.json"
GLOBAL_WORKFLOWS_DIR = DATA_DIR / "globals" / "workflows"

# ========== FUNCTIONS ==========
# recarga los paths cada que se cambia de proyectp (actualiza rutas)
def reload_paths():
    global ACTIVE_PROJECT, ACTIVE_PROJECT_DIR, COMMANDS_FILE, VARIABLES_FILE, PROJECT_FILE, FINDINGS_FILE, HOSTS_FILE, CHECKLISTS_FILE, WORKFLOWS_DIR
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        ACTIVE_PROJECT = data["project"]

    # ========== PROJECT PATHS =========
    ACTIVE_PROJECT_DIR = DATA_DIR / "projects" / ACTIVE_PROJECT
    COMMANDS_FILE = ACTIVE_PROJECT_DIR / "commands.json"
    VARIABLES_FILE = ACTIVE_PROJECT_DIR / "variables.json"
    PROJECT_FILE = ACTIVE_PROJECT_DIR / "project.json"
    FINDINGS_FILE = ACTIVE_PROJECT_DIR / "findings.json"
    HOSTS_FILE = ACTIVE_PROJECT_DIR / "hosts.json"
    CHECKLISTS_FILE = ACTIVE_PROJECT_DIR / "checklists.json"
    WORKFLOWS_DIR = ACTIVE_PROJECT_DIR / "workflows"

reload_paths()