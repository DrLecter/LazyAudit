from rich.text import Text

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, DataTable, Label, TabbedContent, TabPane
from textual.containers import Horizontal, Vertical, Grid

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))
sys.path.append(str(ROOT_DIR / "utils"))
sys.path.append(str(ROOT_DIR / "TUI"))

import utils.PATHS as PATHS
from utils.actions import Command, Scope, Project, Variable, Finding, Host, Checklist, Workflow

from TUI.modals.commands.edit import EditCommandModal
from TUI.modals.commands.add import AddCommandModal
from TUI.modals.commands.remove import RemoveCommandModal

class CommandsTab(TabPane):

    BINDINGS = [("e", "modify_command", "Editar comando"),
                ("n", "add_command", "Nuevo comando"),
                ("r", "remove_command", "Eliminar comando")]
    
    def __init__(self):
        super().__init__("Comandos", id="commands_tab")
        
    def compose(self):
        with Horizontal():
            #Columna izq.
            with Vertical():
                yield Label(f"COMANDOS")
                yield DataTable(id="commands_table") # Mostrar title y scope

            #Columna der.
            with Vertical():
                yield Label(f"Nmap todos los puertos", id="lbl_command_title_name") # Nombre del comando
                yield Label(f"Nmap de todos los puertos", id="lbl_command_description") # Descripcion

                yield Label(f"PLANTILLA", id="lbl_command_title_plantilla") # PLANTILLA
                yield Label("nmap -p- -sV -oX out.xml {RHOST}", id="lbl_command_raw") # raw

                yield Label(f"RENDERIZADO", id="lbl_command_title_renderizado") # RENDERIZADO
                yield Label(f"nmap -p- -sV -oX out.xml 10.20.4.5", id="lbl_command_interpolated") # interpolado

                yield Label(f"TAGS", id="lbl_command_title_tags") # RENDERIZADO
                yield Label(f"tags, tags, tags", id="lbl_command_tags") # interpolado

    def load_commands_table(self):
        table = self.query_one("#commands_table", DataTable)
        table.cursor_type = "row"

        if not table.columns:
            table.add_columns("Título", "Scope")
        table.clear() # Limpia las filas anteriores
        
        commands = Command.read_all()

        for c in commands:
            table.add_row(c.title, c.scope, key=c.title)

    def on_data_table_row_highlighted(self, event: DataTable.RowSelected) -> None:
        if event.data_table.id == "commands_table":
            command_name = str(event.row_key.value)

            command = next((c for c in Command.read_all() if c.title == command_name), None)

            self.update_command_info(command) # Command()

    def update_command_info(self, command : "Command") -> None:
        if command:
            self.query_one("#lbl_command_title_name", Label).update(f"{command.title}")
            self.query_one("#lbl_command_description", Label).update(f"{command.description}")

            self.query_one("#lbl_command_raw", Label).update(f"{command.command}")

            self.query_one("#lbl_command_interpolated", Label).update(f"{Command.interpolate(command)}")

            tags_str = ", ".join(t if isinstance(t, str) else str(t[0]) for t in command.tags) # Parch para no crashear, convierte todo a string antes de join()
            self.query_one("#lbl_command_tags", Label).update(tags_str)

    def action_add_command(self) -> None:
        self.app.push_screen(AddCommandModal(), self.add_command)

    def add_command(self, data) -> None:
        if data is not None:
            clean_tags = [t.strip() for t in data["tags"].split(",") if t.strip()] if data["tags"] else []
            command = Command(title=data["title"], description=data["description"], command=data["command"], scope=data["scope"], tags=clean_tags)
            Command.add(command)
            self.load_commands_table()
            self.update_command_info(command)
            self.app.notify("Comando creado con éxito!")

    #def action_modify_project(self) -> None:
    #    proyectos = Project.show()
    #    project = next((proj for proj in proyectos if proj.name == PATHS.ACTIVE_PROJECT), None)

    #    if project:
    #        self.app.push_screen(EditCommandModal(project), self.modify_project)

    #def modify_project(self, data) -> None:
    #    if data is not None:
    #        Project.modify(Project(name=data["name"], description=data["description"], status=data["status"], created=data["created"]))
    #        self.load_projects_table()
    #        self.update_project_info(data["name"])
    #        self.app.notify("¡Proyecto actualizado con éxito!")

    #def action_remove_project(self) -> None:
    #    proyectos = Project.show()
    #    project = next((proj for proj in proyectos if proj.name == PATHS.ACTIVE_PROJECT), None)

    #    self.app.push_screen(RemoveCommandModal(project), self.remove_project)

    #def remove_project(self, project_name) -> None:
    #    if project_name is not None:
    #        project_name = project_name["name"]

    #        available_projects = [p.name for p in Project.show() if p.name != project_name]

    #        if available_projects:
    #            Project.change(available_projects[0])
    #            Project.remove(project_name)     
    #            self.load_projects_table()
    #            self.update_project_info(available_projects[0])
    #            self.app.notify("¡Proyecto eliminado con éxito!")
    #        else:
    #            self.app.notify("No podés eliminar el único proyecto existente", severity="warning")

    def on_show(self) -> None:
        self.load_commands_table()
        cmds = Command.read_all()
        if cmds:
            self.update_command_info(cmds[0])
        self.query_one("#commands_table", DataTable).focus()
         

