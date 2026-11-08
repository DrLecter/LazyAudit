from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal
from pathlib import Path
from textual.binding import Binding

class AddWorkflowModal(ModalScreen):

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
        with Vertical(id="modal_add_workflow"):
            yield Label("AÑADIR WORKFLOW", id="model_title")

            yield Label(" Archivo (.py o .sh en /app/inbox o ruta):")
            yield Input(placeholder="script.py o /app/inbox/script.py", id="inp_path")

            yield Label(" Scope:")
            yield Select([("Privado", "private"), ("Global", "global")], value="private", id="sel_scope")

            with Horizontal(id="modal_btns"):
                yield Button("Guardar", variant="primary", id="save_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_btn":
            path_str = self.query_one("#inp_path", Input).value.strip()
            scope = self.query_one("#sel_scope", Select).value

            if not path_str:
                self.app.notify("El nombre de archivo no puede estar vacío", severity="warning")
                return

            from utils.actions import Workflow
            p = Workflow.resolve_script_path(path_str)
            if not p.is_file():
                self.app.notify(f"No existe '{path_str}' ni en '/app/inbox/{path_str}'", severity="error")
                return

            if not (p.name.endswith(".py") or p.name.endswith(".sh")):
                self.app.notify("Solo se admiten archivos .py o .sh", severity="warning")
                return

            self.dismiss({
                "path": str(p),
                "scope": scope
            })

        elif event.button.id == "cancel_btn":
            self.dismiss(None)
