from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal

class ModifyCommandModal(ModalScreen):

    def __init__(self, current_command):
        super().__init__()
        self.current_command = current_command

    def compose(self) -> ComposeResult:
        with Vertical(id="model_modify_command"):
            yield Label(f"Editar: {self.current_command.title}", id="model_title")

            yield Label(" Título:")
            yield Input(value=self.current_command.title, id="inp_title")

            yield Label(" Comando:")
            yield Input(value=self.current_command.command, id="inp_comm")

            yield Label(" Descripción:")
            yield Input(value=self.current_command.description, id="inp_desc")

            clean_tags = ", ".join(self.current_command.tags)
            yield Label(" Tags:")
            yield Input(value=clean_tags, id="inp_tags")

            yield Label(" Scope:")
            yield Select([("Privado", "private"), ("Global", "global")], value="private", id="sel_scope")

            with Horizontal(id="modal_btns"):
                yield Button("Guardar", variant="primary", id="save_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_btn":
            new_title = self.query_one("#inp_title", Input).value.strip()
            new_comm = self.query_one("#inp_comm", Input).value.strip()
            new_desc = self.query_one("#inp_desc", Input).value.strip()
            new_tags = self.query_one("#inp_tags", Input).value.strip()
            new_scope =self.query_one("#sel_scope", Select).value.strip()
            
            self.dismiss({
                "title": new_title,
                "command": new_comm,
                "description": new_desc,
                "tags": new_tags,
                "scope": new_scope
            })

        elif event.button.id == "cancel_btn":
            self.dismiss(None)