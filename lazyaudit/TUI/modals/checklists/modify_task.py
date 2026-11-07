from textual.screen import ModalScreen
from textual.binding import Binding
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal

class ModifyTaskModal(ModalScreen):

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
        with Vertical(id="model_modify_command"):
            yield Label(f"EDITAR TAREA - {self.current_task.group}", id="model_title")

            yield Label(" Tarea:")
            yield Input(value=self.current_task.task, id="inp_title")

            with Horizontal(id="modal_btns"):
                yield Button("Guardar", variant="primary", id="save_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_btn":
            group = self.current_task.group
            task = self.query_one("#inp_title", Input).value.strip()
            done = self.current_task.done
            scope = self.current_task.scope
            
            self.dismiss({
                "group": group,
                "task": task,
                "done": done,
                "scope": scope,
            })

        elif event.button.id == "cancel_btn":
            self.dismiss(None)