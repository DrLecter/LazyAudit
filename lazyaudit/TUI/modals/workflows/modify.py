from textual.screen import ModalScreen
from textual.binding import Binding
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal

class ModifyVariableModal(ModalScreen):

    BINDINGS = [
        Binding("escape", "cancel", "Cancelar", key_display="ESC"),
        Binding("left", "app.focus_previous", "Anterior", key_display="←"),
        Binding("right", "app.focus_next", "Siguiente", key_display="→"),
    ]

    def action_cancel(self) -> None:
        self.dismiss(None)


    def __init__(self, current_var):
        super().__init__()
        self.current_var = current_var

    def compose(self) -> ComposeResult:
        with Vertical(id="model_modify_command"):
            yield Label(f"Editar: {self.current_var.key}", id="model_key")

            yield Label(" Clave:")
            yield Input(value=self.current_var.key, id="inp_key")

            yield Label(" Valor:")
            yield Input(value=self.current_var.value, id="inp_value")

            yield Label(" Descripción:")
            yield Input(value=self.current_var.description, id="inp_desc")

            yield Label(" Scope:")
            yield Select([("Privado", "private"), ("Global", "global")], value=self.current_var.scope, id="sel_scope")

            with Horizontal(id="modal_btns"):
                yield Button("Guardar", variant="primary", id="save_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_btn":
            new_key = self.query_one("#inp_key", Input).value.strip()
            new_value = self.query_one("#inp_value", Input).value.strip()
            new_desc = self.query_one("#inp_desc", Input).value.strip()
            new_scope =self.query_one("#sel_scope", Select).value.strip()
            
            self.dismiss({
                "key": new_key,
                "value": new_value,
                "description": new_desc,
                "scope": new_scope
            })

        elif event.button.id == "cancel_btn":
            self.dismiss(None)