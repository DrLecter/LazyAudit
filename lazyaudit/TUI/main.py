from rich.text import Text

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, DataTable, Label, TabbedContent, TabPane, Static   
from textual.containers import Horizontal, Vertical, Grid
from textual.binding import Binding
 
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
from tabs.checklists import ChecklistsTab
from tabs.workflows import WorkflowsTab
#from tabs.workflows import WorkflowsTab

# ====================

class LazyAudit(App):
     CSS_PATH = "styles.tcss"
     BINDINGS = [Binding("d", "toggle_dark", "Cambiar a modo oscuro/claro", key_display="D")]

     def compose(self) -> ComposeResult:
          yield Header(show_clock=True)
          with TabbedContent():
               yield ProjectsTab()

               yield CommandsTab()

               yield VariablesTab()

               yield FindingsTab()

               yield HostsTab()

               yield ChecklistsTab()
                    
               yield WorkflowsTab()
               
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