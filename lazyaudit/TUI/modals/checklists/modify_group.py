from textual.screen import ModalScreen
from textual.binding import Binding
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal

class ModifyGroupModal(ModalScreen):

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
        with Vertical(id="model_modify_checklist_group"):
            yield Label(f"EDITAR GRUPO - {self.current_group}", id="model_title")

            yield Label(" Grupo nuevo: ")
            yield Input(value=self.current_group, id="inp_group")

            with Horizontal(id="modal_btns"):
                yield Button("Guardar", variant="primary", id="save_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_btn":
            new_group = self.query_one("#inp_group", Input).value.strip()
            
            self.dismiss({
                "group" : new_group
            })

        elif event.button.id == "cancel_btn":
            self.dismiss(None)