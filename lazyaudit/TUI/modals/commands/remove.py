from textual.screen import ModalScreen
from textual.binding import Binding
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal

class RemoveCommandModal(ModalScreen):

    BINDINGS = [
        Binding("escape", "cancel", "Cancelar", key_display="ESC"),
        Binding("left", "app.focus_previous", "Anterior", key_display="←"),
        Binding("right", "app.focus_next", "Siguiente", key_display="→"),
    ]

    def action_cancel(self) -> None:
        self.dismiss(None)


    def __init__(self, command):
        super().__init__()
        self.command = command

    def compose(self) -> ComposeResult:
        with Vertical(id="model_remove_command"):
            yield Label(f"Borrar?", id="model_title")

            yield Label(" Nombre:")
            yield Label(f"{self.command.title}", id="lbl_name")

            yield Label(" Comando:")
            yield Label(f"{self.command.command}", id="lbl_desc")

            yield Label(" Scope:")

            yield Label(f"{self.command.scope}", id="lbl_status")

            with Horizontal(id="modal_btns"):
                yield Button("Confirmar", variant="error", id="confirm_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm_btn":
            self.dismiss(self.command)

        elif event.button.id == "cancel_btn":
            self.dismiss(None)