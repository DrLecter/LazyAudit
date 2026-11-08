import json
import getpass
from datetime import datetime
from dataclasses import is_dataclass, asdict
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / "utils"))
sys.path.append(str(BASE_DIR / "TUI"))


from PATHS import LOGS_FILE, ACTIVE_PROJECT

class Event:
    COMMAND_CREATED = "COMMAND_CREATED"
    COMMAND_MODIFIED = "COMMAND_MODIFIED"
    COMMAND_REMOVED = "COMMAND_REMOVED"

    VARIABLE_CREATED = "VARIABLE_CREATED"
    VARIABLE_MODIFIED = "VARIABLE_MODIFIED"
    VARIABLE_REMOVED = "VARIABLE_REMOVED"

    PROJECT_CREATED = "PROJECT_CREATED"
    PROJECT_MODIFIED = "PROJECT_MODIFIED"
    PROJECT_REMOVED = "PROJECT_REMOVED"
    PROJECT_STATUS_CHANGED = "PROJECT_STATUS_CHANGED"
    PROJECT_CHANGED = "PROJECT_CHANGED"

    FINDING_CREATED = "FINDING_CREATED"
    FINDING_MODIFIED = "FINDING_MODIFIED"
    FINDING_REMOVED = "FINDING_REMOVED"

    HOST_CREATED = "HOST_CREATED"
    HOST_MODIFIED = "HOST_MODIFIED"
    HOST_REMOVED = "HOST_REMOVED"

    CHECKLIST_CREATED = "CHECKLIST_CREATED"
    CHECKLIST_MODIFIED = "CHECKLIST_MODIFIED"
    CHECKLIST_REMOVED = "CHECKLIST_REMOVED"

    WORKFLOW_ADDED = "WORKFLOW_ADDED"
    WORKFLOW_EXECUTED = "WORKFLOW_EXECUTED"
    WORKFLOW_REMOVED = "WORKFLOW_REMOVED"

    LOGGED_IN = "LOGGED_IN"
    USED_CLI = "USED_CLI"


def _normalize_data(data):
    # dataclass, dict o lista -> dict json 
    if is_dataclass(data):
        return asdict(data)
    if isinstance(data, dict):
            return {
                k: asdict(v) if is_dataclass(v) else v
                for k, v in data.items()
            }
    return {"raw": str(data)}


def log(event, data, user: str = None, project: str = None) -> None:
    static_data = {
        "ts": datetime.now().strftime("%Y-%m-%d|%H:%M:%S"),
        "user": user or getpass.getuser(),
        "project": project or ACTIVE_PROJECT,
        "event": event,
        "data": _normalize_data(data)
    }

    LOGS_FILE.parent.mkdir(parents=True, exist_ok=True)

    file_exists = LOGS_FILE.exists()

    with open(LOGS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(static_data, ensure_ascii=False, default=str) + "\n")

    if not file_exists and LOGS_FILE.exists():
        try:
            os.chmod(LOGS_FILE, 0o600)
        except OSError:
            pass