from textual.screen import ModalScreen
from textual.binding import Binding
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal

class AddGroupModal(ModalScreen):

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
        with Vertical(id="model_add_checklist_group"):
            yield Label(f"Nuevo grupo", id="model_title")

            yield Label(" Nombre:")
            yield Input(id="inp_group")

            yield Label(" Primer tarea:")
            yield Input(id="inp_task")

            yield Label(" Scope:")
            yield Select([("Privado", "private"), ("Global", "global")], value="private", id="sel_scope")

            with Horizontal(id="modal_btns"):
                yield Button("Guardar", variant="primary", id="save_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_btn":
            group = self.query_one("#inp_group", Input).value.strip()
            task = self.query_one("#inp_task", Input).value.strip()
            scope = self.query_one("#sel_scope", Select).value.strip()

            self.dismiss({
                "group" : group,
                "task" : task,
                "done" : False,
                "scope" : scope
            })

        elif event.button.id == "cancel_btn":
            self.dismiss(None)