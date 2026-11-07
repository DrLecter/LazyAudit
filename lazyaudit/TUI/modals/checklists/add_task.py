from textual.screen import ModalScreen
from textual.binding import Binding
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal

from utils.actions import Checklist

class AddTaskModal(ModalScreen):

    BINDINGS = [
        Binding("escape", "cancel", "Cancelar", key_display="ESC"),
        Binding("left", "app.focus_previous", "Anterior", key_display="←"),
        Binding("right", "app.focus_next", "Siguiente", key_display="→"),
    ]

    def action_cancel(self) -> None:
        self.dismiss(None)
    def __init__(self, current_group):
        super().__init__()
        self.current_group = current_group

    def compose(self) -> ComposeResult:
        with Vertical(id="model_add_project"):

            all_groups = Checklist.read_all()
            group_names = sorted({item.group for item in all_groups}) # Lista de los nombres de grupos sin duplicados y ordenada

            yield Label(f"NUEVA TAREA - {self.current_group}", id="model_task")

            yield Label(" Tarea:")
            yield Input(id="inp_task")

            #yield Label(f" Grupo: ", id="task_group")
            #yield Select([(g, g) for g in group_names], value=f"{self.current_group}", id="sel_group")

            with Horizontal(id="modal_btns"):
                yield Button("Guardar", variant="primary", id="save_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:

        if event.button.id == "save_btn":
            task = self.query_one("#inp_task", Input).value.strip()
            #group = self.query_one("#inp_task", Input).value.strip()
            group = self.current_group
            all_checklists = Checklist.read_all()
            checklist_group = [f for f in all_checklists if f.group == group]
            scope = str(checklist_group[0].scope)

            # Devuelve los valores
            self.dismiss({
                "task": task,
                "group": group,
                "scope": scope
            })

        elif event.button.id == "cancel_btn":
            self.dismiss(None)