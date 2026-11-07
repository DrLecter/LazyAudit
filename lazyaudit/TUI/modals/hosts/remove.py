from textual.screen import ModalScreen
from textual.binding import Binding
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal

class RemoveHostModal(ModalScreen):

    BINDINGS = [
        Binding("escape", "cancel", "Cancelar", key_display="ESC"),
        Binding("left", "app.focus_previous", "Anterior", key_display="←"),
        Binding("right", "app.focus_next", "Siguiente", key_display="→"),
    ]

    def action_cancel(self) -> None:
        self.dismiss(None)


    def __init__(self, host):
        super().__init__()
        self.host = host

    def compose(self) -> ComposeResult:
        with Vertical(id="model_remove_host"):
            yield Label(f"Borrar?", id="model_title")

            yield Label(f"{self.host.hostname}", id="lbl_hostname")

            yield Label(" Host:")
            yield Label(f"{self.host.ip}", id="lbl_ip")

            yield Label(" Puertos:")
            yield Label(f"{", ".join(self.host.ports)}", id="lbl_vulns")

            yield Label(" Servicios:")
            yield Label(f"{", ".join(self.host.services)}", id="lbl_services")

            with Horizontal(id="modal_btns"):
                yield Button("Confirmar", variant="error", id="confirm_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm_btn":
            self.dismiss(self.host)

        elif event.button.id == "cancel_btn":
            self.dismiss(None)