from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal

class RemoveFindingModal(ModalScreen):

    def __init__(self, finding):
        super().__init__()
        self.finding = finding

    def compose(self) -> ComposeResult:
        with Vertical(id="model_remove_finding"):
            yield Label(f"Borrar?", id="model_title")

            yield Label(f"{self.finding.description}", id="lbl_desc")

            yield Label(" Host:")
            yield Label(f"{self.finding.host}", id="lbl_host")

            yield Label(" Vulnerabilidades:")
            yield Label(f"{", ".join(self.finding.vulns)}", id="lbl_vulns")

            yield Label(" Criticidad:")
            yield Label(f"{self.finding.severity}", id="lbl_sev")

            with Horizontal(id="modal_btns"):
                yield Button("Confirmar", variant="primary", id="confirm_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm_btn":
            self.dismiss(self.finding)

        elif event.button.id == "cancel_btn":
            self.dismiss(None)