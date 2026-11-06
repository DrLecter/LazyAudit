from rich.text import Text

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, DataTable, Label, TabbedContent, TabPane, Static   
from textual.containers import Horizontal, Vertical, Grid
 
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))
sys.path.append(str(ROOT_DIR / "utils"))

import utils.PATHS as PATHS

from tabs.projects import ProjectsTab
from tabs.commands import CommandsTab
from tabs.variables import VariablesTab
from tabs.findings import FindingsTab
from tabs.hosts import HostsTab

# ====================

class LazyAudit(App):
     BINDINGS = [("d", "toggle_dark", "Cambiar a modo oscuro/claro")]

     def compose(self) -> ComposeResult:
          yield Header(show_clock=True)
          with TabbedContent():
               yield ProjectsTab()

               yield CommandsTab()

               yield VariablesTab()

               yield FindingsTab()

               yield HostsTab()

               with TabPane("Checklists", id="checklists_tab"):
                    yield Label("Contenido de Checklists")
                    
               with TabPane("Workflows", id="workflows_tab"):
                    yield Label("Contenido de Workflows")
        
          yield Footer()

     def action_dummy(self) -> None:
          pass  # No hace nada, solo existe para que el Footer dibuje el texto

     def action_dummy2(self) -> None:
          pass  # No hace nada, solo existe para que el Footer dibuje el texto

     def on_mount(self) -> None:
          self.title = "LazyAudit"
          self.sub_title = f"{PATHS.ACTIVE_PROJECT}"

app = LazyAudit()
if __name__ == "__main__":
     app.run()