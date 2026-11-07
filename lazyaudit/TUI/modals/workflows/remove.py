from textual.screen import ModalScreen
from textual.binding import Binding
from textual.app import ComposeResult
from textual.widgets import Label, Button
from textual.containers import Vertical, Horizontal

class RemoveWorkflowModal(ModalScreen):

    BINDINGS = [
        Binding("escape", "cancel", "Cancelar", key_display="ESC"),
        Binding("left", "app.focus_previous", "Anterior", key_display="←"),
        Binding("right", "app.focus_next", "Siguiente", key_display="→"),
    ]

    def action_cancel(self) -> None:
        self.dismiss(None)
    def __init__(self, workflow):
        super().__init__()
        self.workflow = workflow

    def compose(self) -> ComposeResult:
        with Vertical(id="modal_remove_workflow"):
            yield Label("¿ELIMINAR WORKFLOW?", id="model_title")

            yield Label(f" Nombre: {self.workflow.name}")
            yield Label(f" Scope: {self.workflow.scope.upper()}")
            yield Label(f" Ruta: {self.workflow.path}")

            with Horizontal(id="modal_btns"):
                yield Button("Confirmar", variant="error", id="confirm_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm_btn":
            self.dismiss(True)
        elif event.button.id == "cancel_btn":
            self.dismiss(None)
