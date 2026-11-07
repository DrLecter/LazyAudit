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

from TUI.modals.projects.modify import ModifyProjectModal
from TUI.modals.projects.add import AddProjectModal
from TUI.modals.projects.remove import RemoveProjectModal

class ProjectsTab(TabPane):

    BINDINGS = [Binding("n", "add_project", "Nuevo proyecto", key_display="N"),
                Binding("e", "modify_project", "Editar proyecto", key_display="E"),
                Binding("r", "remove_project", "Eliminar proyecto", key_display="R")]
    
    def __init__(self):
        super().__init__("Proyecto", id="projects_tab")
        
    def compose(self):
        with Horizontal():
            #Columna izq.
            with Vertical():
                yield Label(f"PROYECTOS")
                yield DataTable(show_header=False, id="projects_table")

            #Columna der.
            with Vertical():
                yield Label(f"{PATHS.ACTIVE_PROJECT}", id="lbl_nombre_proyecto")

                # Cantidad de:
                with Horizontal():
                    yield Label("Hosts", id="count_hosts")
                    yield Label("Hallazgos", id="count_findings")
                    yield Label("Variables", id="count_variables")
                    yield Label("Comandos", id="count_commands")

                # Grid de detalles
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

        for p in projects:
            table.add_row(p.name, p.created, key=p.name)

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

    def action_modify_project(self) -> None:
        proyectos = Project.show()
        project = next((proj for proj in proyectos if proj.name == PATHS.ACTIVE_PROJECT), None)

        if project:
            self.app.push_screen(ModifyProjectModal(project), self.modify_project)

    def action_add_project(self) -> None:
        self.app.push_screen(AddProjectModal(), self.add_project)

    def action_remove_project(self) -> None:
        proyectos = Project.show()
        project = next((proj for proj in proyectos if proj.name == PATHS.ACTIVE_PROJECT), None)

        self.app.push_screen(RemoveProjectModal(project), self.remove_project)

    def modify_project(self, data) -> None:
        if data is not None:
            Project.modify(Project(**data))
            self.load_projects_table()
            self.update_project_info(data["name"])
            self.app.notify("¡Proyecto actualizado con éxito!")

    def add_project(self, data) -> None:
        if data is not None:
            Project.add(Project(name=data["name"], description=data["description"], status=data["status"]))
            Project.change(data["name"])
            self.load_projects_table()
            self.update_project_info(data["name"])
            self.app.notify("¡Proyecto creado con éxito!")

    def remove_project(self, project_name) -> None:
        if project_name is not None:
            project_name = project_name["name"]

            available_projects = [p.name for p in Project.show() if p.name != project_name]

            if available_projects:
                Project.change(available_projects[0])
                Project.remove(project_name)     
                self.load_projects_table()
                self.update_project_info(available_projects[0])
                self.app.notify("¡Proyecto eliminado con éxito!")
            else:
                self.app.notify("No podés eliminar el único proyecto existente", severity="warning")

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
            self.query_one("#count_findings", Label).update(f"Hallazgos\n{self._count(Finding)}")
            self.query_one("#count_variables", Label).update(f"Variables\n{self._count(Variable)}")
            self.query_one("#count_commands", Label).update(f"Comandos\n{self._count(Command)}")

    def on_show(self) -> None:
        self.load_projects_table()
        self.update_project_info(PATHS.ACTIVE_PROJECT)
        self.query_one("#projects_table", DataTable)
         

