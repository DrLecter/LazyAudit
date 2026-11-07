from textual.screen import ModalScreen
from textual.binding import Binding
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal

class RemoveVariableModal(ModalScreen):

    BINDINGS = [
        Binding("escape", "cancel", "Cancelar", key_display="ESC"),
        Binding("left", "app.focus_previous", "Anterior", key_display="←"),
        Binding("right", "app.focus_next", "Siguiente", key_display="→"),
    ]

    def action_cancel(self) -> None:
        self.dismiss(None)


    def __init__(self, variable):
        super().__init__()
        self.variable = variable

    def compose(self) -> ComposeResult:
        with Vertical(id="model_remove_var"):
            yield Label(f"Borrar?", id="model_title")

            yield Label(" Nombre:")
            yield Label(f"{self.variable.key}", id="lbl_name")

            yield Label(" Valor:")
            yield Label(f"{self.variable.value}", id="lbl_desc")

            yield Label(" Scope:")

            yield Label(f"{self.variable.scope}", id="lbl_status")

            with Horizontal(id="modal_btns"):
                yield Button("Confirmar", variant="error", id="confirm_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm_btn":
            self.dismiss(self.variable)

        elif event.button.id == "cancel_btn":
            self.dismiss(None)