from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal

class AddCommandModal(ModalScreen):

    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical(id="model_add_project"):
            yield Label(f"Nuevo comando", id="model_title")

            yield Label(" Título:")
            yield Input(id="inp_title")

            yield Label(" Descripción:")
            yield Input(id="inp_desc")

            yield Label(" Comando:")
            yield Input(id="inp_comm")

            yield Label(" Tags:")
            yield Input(id="inp_tags")

            yield Label(" Scope:")

            yield Select([("Privado", "private"), ("Global", "global")],
                            value="private", id="sel_scope")

            with Horizontal(id="modal_btns"):
                yield Button("Guardar", variant="primary", id="save_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_btn":
            title = self.query_one("#inp_title", Input).value.strip()
            desc = self.query_one("#inp_desc", Input).value.strip()
            command = self.query_one("#inp_comm", Input).value.strip()
            tags = self.query_one("#inp_tags", Input).value.strip()
            scope = self.query_one("#sel_scope", Select).value.strip()

            # Devuelve los valores
            self.dismiss({
                "title": title,
                "description": desc,
                "command": command,
                "tags": tags,
                "scope": scope
            })

        elif event.button.id == "cancel_btn":
            self.dismiss(None)