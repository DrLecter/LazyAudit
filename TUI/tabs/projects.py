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
from utils.actions import Command, Scope, Project, Variable, Finding, Host, Checklist, Workflow

from modals.edit_project import EditProjectModal

class ProjectsTab(TabPane):
    BINDINGS = [("e", "edit_project", "Editar proyecto")]
    
    def __init__(self):
        super().__init__("Proyecto", id="projects_tab")
        
    def compose(self):
        with Horizontal():
                            with Vertical():
                                yield Label(f"PROYECTOS")
                                yield DataTable(id="projects_table")
        
                            with Vertical():
                                yield Label(f"{PATHS.ACTIVE_PROJECT}", id="lbl_nombre_proyecto")
                                
        
                                with Horizontal():
                                    yield Label("Hosts", id="count_hosts")
                                    yield Label("Hallazgos", id="count_findings")
                                    yield Label("Variables", id="count_variables")
                                    yield Label("Comandos", id="count_commands")
        
                                yield Label(f"DETALLE")
                                with Grid(id="grid_detalle"):
                                    yield Label("Descripcion:", classes="lbl_clave")
                                    yield Label(f"", id="grid_project_description")
        
                                    yield Label("Fecha inicio:", classes="lbl_clave")
                                    yield Label(f"", id="grid_project_created")
        
                                    yield Label("Estado:", classes="lbl_clave")
                                    yield Label(f"", id="grid_project_status")

    def load_projects_table(self):
        table = self.query_one("#projects_table", DataTable)
        table.cursor_type = "row"

        if not table.columns:
            table.add_columns("Title", "Created")
        table.clear() # Limpia las filas anteriores
        
        projects = Project.show()
        projects.sort(key=lambda x: x.name)

        for p in projects:
            table.add_row(p.name, p.status, key=p.name)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
            if event.data_table.id == "projects_table":
                project_name = str(event.row_key.value)

                Project.change(project_name)

                self.update_project_info(project_name)
                
    def _count(self, model):
        if model == Project:
            total = len(Project.show())
        else:
            total = len(model.read_all())

        return total

    def action_edit_project(self) -> None:
            proyectos = Project.show()
            p = next((proj for proj in proyectos if proj.name == PATHS.ACTIVE_PROJECT), None)

            if p:
                self.app.push_screen(EditProjectModal(p), self.update_project)

    def update_project(self, info) -> None:
        if info is not None:
            # Modificamos el proyecto con Project.modify(...)
            # y refrescamos la tabla y la vista
            Project.modify(Project(name=info["name"], description=info["description"], status=info["status"]))
            self.load_projects_table()
            self.update_project_info(info["name"])
            self.app.notify("¡Proyecto actualizado con éxito!")

    def update_project_info(self, project_name : str) -> None:
        self.app.sub_title = project_name
        proyectos = Project.show()
        p = next((proj for proj in proyectos if proj.name == project_name), None)

        if p:
            self.query_one("#lbl_nombre_proyecto", Label).update(f"{p.name}")
            self.query_one("#grid_project_description", Label).update(f"{p.description}")
            self.query_one("#grid_project_created", Label).update(f"{p.created}")
            self.query_one("#grid_project_status", Label).update(f"{p.status}")

            self.query_one("#count_hosts", Label).update(f"Hosts\n{self._count(Host)}")
            self.query_one("#count_findings", Label).update(f"Findings\n{self._count(Finding)}")
            self.query_one("#count_variables", Label).update(f"Variables\n{self._count(Variable)}")
            self.query_one("#count_commands", Label).update(f"Commands\n{self._count(Command)}")

    def on_show(self) -> None:
            self.load_projects_table()
            self.update_project_info(PATHS.ACTIVE_PROJECT)
         

