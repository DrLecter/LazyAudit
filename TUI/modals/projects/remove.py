from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal

class RemoveProjectModal(ModalScreen):

    def __init__(self, project):
        super().__init__()
        self.project = project

    def compose(self) -> ComposeResult:
        with Vertical(id="model_edit_project"):
            yield Label(f"Borrar?", id="model_title")

            yield Label(" Nombre:")
            yield Label(f"{self.project.name}", id="lbl_name")

            yield Label(" Descripción:")
            yield Label(f"{self.project.description}", id="lbl_desc")

            yield Label(" Estado:")

            yield Label(f"{self.project.status}", id="lbl_status")

            with Horizontal(id="modal_btns"):
                yield Button("Confirmar", variant="primary", id="confirm_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm_btn":
            project_name = self.project.name

            self.dismiss({
                "name": project_name
            })

        elif event.button.id == "cancel_btn":
            self.dismiss(None)