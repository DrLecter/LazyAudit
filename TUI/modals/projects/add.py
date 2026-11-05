from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal

class AddProjectModal(ModalScreen):

    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical(id="model_add_project"):
            yield Label(f"Nuevo proyecto", id="model_title")

            yield Label(" Nombre:")
            yield Input(id="inp_name")

            yield Label(" Descripción:")
            yield Input(id="inp_desc")

            yield Label(" Estado:")

            yield Select([("Activo", "active"), ("Pausado", "paused"), ("Finalizado", "finished")],
                            value="active", id="sel_status")

            with Horizontal(id="modal_btns"):
                yield Button("Guardar", variant="primary", id="save_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_btn":
            new_name = self.query_one("#inp_name", Input).value
            new_desc = self.query_one("#inp_desc", Input).value
            new_status = self.query_one("#sel_status", Select).value

            # Devuelve los valores
            self.dismiss({
                "name": new_name,
                "description": new_desc,
                "status": new_status
            })

        elif event.button.id == "cancel_btn":
            self.dismiss(None)