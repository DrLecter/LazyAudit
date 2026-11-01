from pathlib import Path
import json

# ========== LAZYAUDIT PATHS ==========
LAZYAUDIT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = LAZYAUDIT_DIR/"data"
GLOBAL_DIR = LAZYAUDIT_DIR/"data"/"globals"
CONFIG_FILE = DATA_DIR/"config.json"

# Lee el config.json para seetear el ACTIVE_PROJECT
with open(CONFIG_FILE, "r") as f:
    data = json.load(f)
    ACTIVE_PROJECT = data["project"]

# ========== PROJECTS PATHS ===========
PROJECTS_DIR = DATA_DIR / "projects"

ACTIVE_PROJECT_DIR = DATA_DIR/"projects"/ACTIVE_PROJECT 
COMMANDS_FILE = ACTIVE_PROJECT_DIR/"commands.json"
VARIABLES_FILE = ACTIVE_PROJECT_DIR/"variables.json"
PROJECT_FILE = ACTIVE_PROJECT_DIR/"project.json"
FINDINGS_FILE = ACTIVE_PROJECT_DIR/"findings.json"
HOSTS_FILE = ACTIVE_PROJECT_DIR/"hosts.json"
#CHECKLISTS_DIR = ACTIVE_PROJECT_DIR/"checklists"
#WORKFLOWS_DIR = ACTIVE_PROJECT_DIR/"workflows"

# ========== GLOBAL PATHS ==========
GLOBAL_COMMANDS_FILE = GLOBAL_DIR/"global_commands.json"
GLOBAL_VARS_FILE = GLOBAL_DIR/"global_vars.json"
#GLOBAL_CHECKLISTS_DIR = DATA_DIR / "checklists"
#GLOBAL_WORKFLOWS_DIR = DATA_DIR / "workflows"



