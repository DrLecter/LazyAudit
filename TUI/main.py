from rich.text import Text

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, DataTable, Label, TabbedContent, TabPane
from textual.containers import Horizontal, Vertical, Grid
 
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))
sys.path.append(str(ROOT_DIR / "utils"))

import utils.PATHS as PATHS
from tabs.projects import ProjectsTab
from tabs.commands import CommandsTab


# ====================

class LazyAudit(App):
    BINDINGS = [("d", "toggle_dark", "Cambiar a modo oscuro/claro")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with TabbedContent():
            yield ProjectsTab()

            yield CommandsTab()
                 
            with TabPane("Variables", id="variables_tab"):
                 yield Label("Contenido de Variables")
                 #yield DataTable(id="variables_table")

            with TabPane("Fidings", id="findings_tab"):
                 yield Label("Contenido de Fidings")

            with TabPane("Hosts", id="hosts_tab"):
                 yield Label("Contenido de Hosts")

            with TabPane("Checklists", id="checklists_tab"):
                 yield Label("Contenido de Checklists")
                 
            with TabPane("Workflows", id="workflows_tab"):
                 yield Label("Contenido de Workflows")
        
        yield Footer()

    def on_mount(self) -> None:
        self.title = "LazyAudit"
        self.sub_title = f"{PATHS.ACTIVE_PROJECT}"

app = LazyAudit()
if __name__ == "__main__":
    app.run()