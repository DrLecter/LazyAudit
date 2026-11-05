from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal

class EditCommandModal(ModalScreen):

    def __init__(self, proyecto):
        super().__init__()
        self.proyecto = proyecto

    def compose(self) -> ComposeResult:
        with Vertical(id="model_edit_project"):
            yield Label(f"Editar: {self.proyecto.name}", id="model_title")

            yield Label(" Nombre:")
            yield Input(value=self.proyecto.name, id="inp_name")

            yield Label(" Descripción:")
            yield Input(value=self.proyecto.description, id="inp_desc")

            yield Label(" Estado:")

            yield Select([("Activo", "active"), ("Pausado", "paused"), ("Finalizado", "finished")],
                            value=self.proyecto.status, id="sel_status")

            with Horizontal(id="modal_btns"):
                yield Button("Guardar", variant="primary", id="save_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_btn":
            new_name = self.query_one("#inp_name", Input).value
            new_desc = self.query_one("#inp_desc", Input).value
            new_status = self.query_one("#sel_status", Select).value
            date = self.proyecto.created

            self.dismiss({
                "name": new_name,
                "description": new_desc,
                "status": new_status,
                "created": date
            })

        elif event.button.id == "cancel_btn":
            self.dismiss(None)