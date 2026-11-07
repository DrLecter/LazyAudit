from textual.screen import ModalScreen
from textual.binding import Binding
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal

class ModifyFindingModal(ModalScreen):

    BINDINGS = [
        Binding("escape", "cancel", "Cancelar", key_display="ESC"),
        Binding("left", "app.focus_previous", "Anterior", key_display="←"),
        Binding("right", "app.focus_next", "Siguiente", key_display="→"),
    ]

    def action_cancel(self) -> None:
        self.dismiss(None)


    def __init__(self, current_finding):
        super().__init__()
        self.current_finding = current_finding

    def compose(self) -> ComposeResult:
        with Vertical(id="model_modify_finding"):
            yield Label(f"Editar hallazgo", id="model_key")

            yield Label(" Host:")
            yield Input(value=self.current_finding.host, id="inp_host")

            yield Label(" Descripción:")
            yield Input(value=self.current_finding.description, id="inp_desc")

            yield Label(" Vulnerabilidades:")
            yield Input(value=f"{", ".join(self.current_finding.vulns)}", id="inp_vulns")

            yield Label(" Criticidad:")
            yield Select([("Alta", "high"), ("Media", "medium"), ("Baja", "low")], value=self.current_finding.severity, id="sel_sev")

            with Horizontal(id="modal_btns"):
                yield Button("Guardar", variant="primary", id="save_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_btn":
            new_host = self.query_one("#inp_host", Input).value.strip()
            new_desc = self.query_one("#inp_desc", Input).value.strip()
            new_vulns = self.query_one("#inp_vulns", Input).value.strip()
            new_sev =self.query_one("#sel_sev", Select).value.strip()
            
            self.dismiss({
                "host": new_host,
                "description": new_desc,
                "vulns": new_vulns,
                "severity": new_sev
            })

        elif event.button.id == "cancel_btn":
            self.dismiss(None)