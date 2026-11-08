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

from TUI.modals.commands.modify import ModifyCommandModal
from TUI.modals.commands.add import AddCommandModal
from TUI.modals.commands.remove import RemoveCommandModal

class CommandsTab(TabPane):

    BINDINGS = [Binding("n", "add_command", "Nuevo comando", key_display="N"),
                Binding("e", "modify_command", "Editar comando", key_display="E"),
                Binding("r", "remove_command", "Eliminar comando", key_display="R")]
    
    def __init__(self):
        super().__init__("Comandos", id="commands_tab")
        
    def compose(self):
        with Horizontal():
            #Columna izq.
            with Vertical(id="col_commands_list"):
                yield DataTable(show_header=False, id="commands_table") # Mostrar title y scope

            #Columna der.
            with Vertical(id="col_commands_detail"):
                yield Label(f"Nmap todos los puertos", id="lbl_command_title_name") # Nombre del comando
                yield Label(f"Nmap de todos los puertos", id="lbl_command_description") # Descripcion

                with Vertical(id="box_command_raw"):
                    yield Label("nmap -p- -sV -oX out.xml {RHOST}", id="lbl_command_raw")

                with Vertical(id="box_command_interpolated"):
                    yield Label(f"nmap -p- -sV -oX out.xml 10.20.4.5", id="lbl_command_interpolated")

                yield Label(f"TAGS: ", id="lbl_command_title_tags")

    def on_mount(self) -> None:
        self.query_one("#col_commands_list").border_title = "COMANDOS"
        self.query_one("#col_commands_detail").border_title = "DETALLES"
        self.query_one("#box_command_raw").border_title = "PLANTILLA"
        self.query_one("#box_command_interpolated").border_title = "RENDERIZADO"

    def load_commands_table(self):
        table = self.query_one("#commands_table", DataTable)
        table.cursor_type = "row"

        if not table.columns:
            table.add_columns("Título", "Scope")
        table.clear() # Limpia las filas anteriores
        
        commands = Command.read_all()
        commands.sort(key=lambda x: x.title.casefold())

        self._commands_cache = commands
        for idx, c in enumerate(commands):
            table.add_row(c.title, c.scope, key=str(idx))

    def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        if event.data_table.id == "commands_table":
            idx = int(event.row_key.value)
            if hasattr(self, "_commands_cache") and idx < len(self._commands_cache):
                self.current_command = self._commands_cache[idx]
                self.update_command_info(self.current_command)

    def update_command_info(self, command : "Command") -> None:
        if command:
            self.query_one("#lbl_command_title_name", Label).update(f"{command.title}")
            self.query_one("#lbl_command_description", Label).update(f"{command.description}")

            self.query_one("#lbl_command_raw", Label).update(f"{command.command}")

            self.query_one("#lbl_command_interpolated", Label).update(f"{Command.interpolate(command)}")

            tags_str = ", ".join(t if isinstance(t, str) else str(t[0]) for t in command.tags) # Parch para no crashear, convierte todo a string antes de join()
            self.query_one("#lbl_command_title_tags", Label).update(f"TAGS: {tags_str}")

    def action_add_command(self) -> None:
        self.app.push_screen(AddCommandModal(), self.add_command)

    def add_command(self, data) -> None:
        if data is not None:
            data["tags"] = [t.strip() for t in data["tags"].split(",") if t.strip()] if data.get("tags") else []
            command = Command(**data)
            Command.add(command)
            log(Event.COMMAND_CREATED, command)
            self.load_commands_table()
            self.update_command_info(command)
            self.app.notify("Comando creado con éxito!")

    def action_modify_command(self) -> None:
        if self.current_command:
            self.app.push_screen(ModifyCommandModal(self.current_command), self.modify_command)
        else:
            self.app.notify("Comando no seleccionado!")

    def modify_command(self, data) -> None:
        if data is not None:
            old_command = self.current_command
            clean_tags = [t.strip() for t in data["tags"].split(",") if t.strip()] if data.get("tags") else []
            new_command = Command(title=data["title"], description=data["description"], command=data["command"], scope=data["scope"], tags=clean_tags)
            Command.modify(self.current_command, new_command)
            log(Event.COMMAND_MODIFIED, {"old": old_command,"new":new_command})
            self.load_commands_table()
            self.update_command_info(new_command)
            self.app.notify("¡Proyecto actualizado con éxito!")


    def action_remove_command(self) -> None:
        self.app.push_screen(RemoveCommandModal(self.current_command), self.remove_command)

    def remove_command(self, command) -> None:
        if command != None:
            Command.remove(command)    
            log(Event.COMMAND_REMOVED, command) 
            commands = Command.read_all()
            if commands:
                self.update_command_info(commands[0])
            self.load_commands_table()
            self.update_command_info(commands[0])
            self.app.notify("¡Comando eliminado con éxito!")

    def on_show(self) -> None:
        self.load_commands_table()
        commands = Command.read_all()
        if commands:
            self.update_command_info(commands[0])
        self.query_one("#commands_table", DataTable)
         

