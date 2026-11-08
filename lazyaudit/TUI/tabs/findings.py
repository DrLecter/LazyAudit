from rich.text import Text

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, DataTable, Label, TabbedContent, TabPane
from textual.containers import Horizontal, Vertical, Grid
from textual.binding import Binding

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))
sys.path.append(str(ROOT_DIR / "utils"))
sys.path.append(str(ROOT_DIR / "TUI"))

import utils.PATHS as PATHS
from utils.actions import Command, Scope, Project, Variable, Finding, Host, Checklist, Workflow
from utils.logger import log, Event

from TUI.modals.findings.modify import ModifyFindingModal
from TUI.modals.findings.add import AddFindingModal
from TUI.modals.findings.remove import RemoveFindingModal

class FindingsTab(TabPane):

    BINDINGS = [Binding("n", "add_finding", "Nuevo hallazgo", key_display="N"),
                Binding("e", "modify_finding", "Editar hallazgo", key_display="E"),
                Binding("r", "remove_finding", "Eliminar hallazgo", key_display="R")]
    
    def __init__(self):
        super().__init__("Hallazgos", id="findings_tab")
        
    def compose(self):
        with Horizontal():
            #Columna izq.
            with Vertical(id="col_findings_list"):
                yield DataTable(show_header=False, id="findings_table")

            #Columna der.
            with Vertical(id="col_findings_detail"):
                yield Label("HOST", id="lbl_finding_host_title") 
                yield Label("", id="lbl_finding_host") 
                yield Label(f"", id="lbl_finding_description") 

                with Vertical():
                    yield Label(f"VULNS", id="lbl_finding_title_vulns")
                #yield Label(f"", id="lbl_finding_vulns") 
                    yield Label(f"CRITICIDAD: ", id="lbl_finding_title_sev") 
                    #yield Label(f"", id="lbl_finding_sev") 

    def on_mount(self) -> None:
        self.query_one("#col_findings_list").border_title = "HALLAZGOS"
        self.query_one("#col_findings_detail").border_title = "DETALLES" 

    def load_findings_table(self):
        table = self.query_one("#findings_table", DataTable)
        table.cursor_type = "row"

        if not table.columns:
            table.add_columns("a", "b", "c")
        table.clear() # Limpia las filas anteriores
        
        findings = Finding.read_all()
        findings.sort(key=lambda x: x.host.casefold())

        for ID, f in enumerate(findings):
            table.add_row(f.description[:15].strip() + "...", f.host, f.severity, key=str(ID))

    def on_data_table_row_highlighted(self, event: DataTable.RowSelected) -> None:
        if event.data_table.id == "findings_table":
            finding_host = str(event.row_key.value)

            index = int(event.row_key.value)
            findings = Finding.read_all()
            findings.sort(key=lambda x: x.host.casefold())
            if 0 <= index < len(findings):
                self.current_finding = findings[index]

            self.update_finding_info(self.current_finding) 

    def update_finding_info(self, finding : "Finding") -> None:
        if finding:
            self.query_one("#lbl_finding_host", Label).update(f"{finding.host}")
            self.query_one("#lbl_finding_description", Label).update(f"{finding.description}")

            vulns_str = ", ".join(t if isinstance(t, str) else str(t[0]) for t in finding.vulns) # Parch para no crashear, convierte todo a string antes de join()
            self.query_one("#lbl_finding_title_vulns", Label).update(f"Vulnerabilidades: {vulns_str}")

            self.query_one("#lbl_finding_title_sev", Label).update(f"Criticidad: {finding.severity}")


    def action_add_finding(self) -> None:
        self.app.push_screen(AddFindingModal(), self.add_finding)

    def add_finding(self, data) -> None:
        if data is not None:
            clean_vulns = [t.strip() for t in data["vulns"].split(",") if t.strip()] if data["vulns"] else []
            finding = Finding(host=data["host"], description=data["description"], vulns=clean_vulns, severity=data["severity"])
            Finding.add(finding)
            log(Event.FINDING_CREATED, finding)
            self.load_findings_table()
            self.update_finding_info(finding)
            self.app.notify("Hallazgo creado con éxito!")

    def action_modify_finding(self) -> None:
        if self.current_finding:
            self.app.push_screen(ModifyFindingModal(self.current_finding), self.modify_finding)
        else:
            self.app.notify("Comando no seleccionado!")

    def modify_finding(self, data) -> None:
        if data is not None:
            clean_vulns = [v.strip() for v in data["vulns"].split(",") if v.strip()] if data["vulns"] else []
            new_finding = Finding(host=data["host"], description=data["description"], vulns=clean_vulns, severity=data["severity"])
            Finding.modify(self.current_finding, new_finding)
            log(Event.FINDING_MODIFIED, {"old":self.current_finding, "new":new_finding})
            self.load_findings_table()
            self.update_finding_info(new_finding)
            self.app.notify("¡Hallazgo actualizado con éxito!")

    def action_remove_finding(self) -> None:
        self.app.push_screen(RemoveFindingModal(self.current_finding), self.remove_finding)

    def remove_finding(self, finding) -> None:
        if finding != None:
            Finding.remove(finding)     
            log(Event.FINDING_REMOVED, finding)
            findings = Finding.read_all()
            if findings:
                self.update_finding_info(findings[0])
            self.load_findings_table()
            self.update_finding_info(findings[0])
            self.app.notify("Hallazgo eliminado con éxito!")

    def on_show(self) -> None:
        self.load_findings_table()
        findings = Finding.read_all()
        if findings:
            self.update_finding_info(findings[0])
        self.query_one("#findings_table", DataTable)
         