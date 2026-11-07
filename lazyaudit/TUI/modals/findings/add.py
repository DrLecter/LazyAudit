from textual.screen import ModalScreen
from textual.binding import Binding
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal

class AddFindingModal(ModalScreen):

    BINDINGS = [
        Binding("escape", "cancel", "Cancelar", key_display="ESC"),
        Binding("left", "app.focus_previous", "Anterior", key_display="←"),
        Binding("right", "app.focus_next", "Siguiente", key_display="→"),
    ]

    def action_cancel(self) -> None:
        self.dismiss(None)


    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical(id="model_add_finding"):
            yield Label(f"Nuevo hallazgo", id="model_finding")

            yield Label(" Host:")
            yield Input(id="inp_host")

            yield Label(" Descripción:")
            yield Input(id="inp_desc")

            yield Label(" Vulnerabilidades:")
            yield Input(id="inp_vulns")

            yield Label(" Criticidad:")
            yield Select([("Alta", "high"), ("Media", "medium"), ("Baja", "low")], value="high", id="sel_sev")

            with Horizontal(id="modal_btns"):
                yield Button("Guardar", variant="primary", id="save_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_btn":
            host = self.query_one("#inp_host", Input).value.strip()
            desc = self.query_one("#inp_desc", Input).value.strip()
            vulns = self.query_one("#inp_vulns", Input).value.strip()
            sev = self.query_one("#sel_sev", Select).value.strip()

            # Devuelve los valores
            self.dismiss({
                "host": host,
                "description": desc,
                "vulns": vulns,
                "severity": sev
            })

        elif event.button.id == "cancel_btn":
            self.dismiss(None)