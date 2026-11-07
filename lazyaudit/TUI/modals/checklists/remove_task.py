from textual.screen import ModalScreen
from textual.binding import Binding
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal

from utils.actions import Checklist

class RemoveTaskModal(ModalScreen):

    BINDINGS = [
        Binding("escape", "cancel", "Cancelar", key_display="ESC"),
        Binding("left", "app.focus_previous", "Anterior", key_display="←"),
        Binding("right", "app.focus_next", "Siguiente", key_display="→"),
    ]

    def action_cancel(self) -> None:
        self.dismiss(None)
    def __init__(self, current_task):
        super().__init__()
        self.current_task = current_task

    def compose(self) -> ComposeResult:
        with Vertical(id="model_remove_checklist_task"):
            tasks_list = Checklist.read_all()
            tasks_list = [c for c in tasks_list if c.group == self.current_task.group]
            
            yield Label(f"BORRAR? - {self.current_task.group} ({len(tasks_list)})", id="model_title")

            yield Label(f"{self.current_task.task}", id="lbl_group_task")

            with Horizontal(id="modal_btns"):
                yield Button("Confirmar", variant="error", id="confirm_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm_btn":
            confirmed = True
            self.dismiss(confirmed)

        elif event.button.id == "cancel_btn":
            self.dismiss(None)