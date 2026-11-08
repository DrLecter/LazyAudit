from pathlib import Path
import sys
from utils.PATHS import LAZYAUDIT_DIR, UTILS_DIR, TUI_DIR

from utils.logger import log, Event

sys.path.append(str(LAZYAUDIT_DIR))
sys.path.append(str(UTILS_DIR))
sys.path.append(str(TUI_DIR))


def main():
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] in ("--tui", "-t")):
        from TUI.main import LazyAudit
        app = LazyAudit()
        log(Event.LOGGED_IN, {"mode": "tui"})
        app.run()
    else:
        cli_command = " ".join(sys.argv[1:])
        log(Event.USED_CLI, {"mode": "cli", "command": cli_command})
        from utils.main import parser
        parser.parse_args()

if __name__ == "__main__":
    main()