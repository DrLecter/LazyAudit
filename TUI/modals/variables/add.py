from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal

class AddVariableModal(ModalScreen):

    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical(id="model_add_var"):
            yield Label(f"Nueva variable", id="model_var")

            yield Label(" Nombre:")
            yield Input(id="inp_key")

            yield Label(" Valor:")
            yield Input(id="inp_value")

            yield Label(" Descripción:")
            yield Input(id="inp_desc")

            yield Label(" Scope:")
            yield Select([("Privado", "private"), ("Global", "global")], value="private", id="sel_scope")

            with Horizontal(id="modal_btns"):
                yield Button("Guardar", variant="primary", id="save_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_btn":
            key = self.query_one("#inp_key", Input).value.strip()
            value = self.query_one("#inp_value", Input).value.strip()
            desc = self.query_one("#inp_desc", Input).value.strip()
            scope = self.query_one("#sel_scope", Select).value.strip()

            # Devuelve los valores
            self.dismiss({
                "key": key,
                "value": value,
                "description": desc,
                "scope": scope
            })

        elif event.button.id == "cancel_btn":
            self.dismiss(None)