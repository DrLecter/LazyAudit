import sys
from pathlib import Path

from textual.app import ComposeResult
from textual.widgets import Label, TabPane, ListView, ListItem, RichLog
from textual.containers import Horizontal, Vertical
from textual import work
from textual.binding import Binding

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))
sys.path.append(str(ROOT_DIR / "utils"))
sys.path.append(str(ROOT_DIR / "TUI"))

from utils.actions import Workflow
from utils.logger import log, Event

from TUI.modals.workflows.add import AddWorkflowModal
from TUI.modals.workflows.remove import RemoveWorkflowModal


class WorkflowItem(ListItem):
    def __init__(self, workflow: Workflow) -> None:
        super().__init__()
        self.workflow = workflow

    def compose(self) -> ComposeResult:
        tipo = "PYTHON" if self.workflow.name.endswith(".py") else "BASH"
        yield Label(f"[{tipo}] {self.workflow.name}")
        yield Label(f"{self.workflow.scope.upper()}")


class WorkflowsTab(TabPane):

    BINDINGS = [
        Binding("n", "add_workflow", "Añadir", key_display="N"),
        Binding("r", "remove_workflow", "Eliminar", key_display="R"),
        Binding("x", "run_workflow", "Ejecutar", key_display="X"),
        Binding("c", "clear_console", "Limpiar Consola", key_display="C")
    ]

    def __init__(self) -> None:
        super().__init__("Workflows", id="workflows_tab")
        self.current_workflow: Workflow | None = None
        self.running_process: bool = False

    def compose(self) -> ComposeResult:
        with Horizontal():
            # Columna izquierda - Lista de Workflows
            with Vertical():
                yield Label("WORKFLOWS")
                yield ListView(id="workflows_list")

            # Columna derecha - Detalle y Consola de salida
            with Vertical():
                yield Label("DETALLE DEL WORKFLOW", id="lbl_wf_title")
                yield Label("Ruta: -", id="lbl_wf_path")
                yield Label("Scope: -", id="lbl_wf_scope")
                yield Label("SALIDA EN VIVO (RichLog)", id="lbl_wf_output_title")
                yield RichLog(id="wf_console", highlight=True, markup=True)

    def load_workflows(self, target_name: str | None = None):
        wf_lv = self.query_one("#workflows_list", ListView)
        wf_lv.clear()

        all_items = Workflow.read_all()
        if not all_items:
            self.current_workflow = None
            self.query_one("#lbl_wf_title", Label).update("WORKFLOWS (Sin datos)")
            self.query_one("#lbl_wf_path", Label).update("Ruta: -")
            self.query_one("#lbl_wf_scope", Label).update("Scope: -")
            return

        items_to_add = [WorkflowItem(wf) for wf in all_items]
        wf_lv.extend(items_to_add)

        selected_name = target_name or (self.current_workflow.name if self.current_workflow else None)
        idx = next((i for i, item in enumerate(all_items) if item.name == selected_name), 0)

        wf_lv.index = None
        wf_lv.index = idx
        self.current_workflow = all_items[idx]
        self.update_details(self.current_workflow)

    def update_details(self, wf: Workflow) -> None:
        self.query_one("#lbl_wf_title", Label).update(f"WORKFLOW: {wf.name}")
        self.query_one("#lbl_wf_path", Label).update(f"Ruta: {wf.path}")
        self.query_one("#lbl_wf_scope", Label).update(f"Scope: {wf.scope.upper()}")

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        if event.list_view.id == "workflows_list" and event.item:
            self.current_workflow = event.item.workflow
            self.update_details(self.current_workflow)

    # ========== Actions ==========

    def action_run_workflow(self) -> None:
        if not self.current_workflow:
            self.app.notify("Selecciona un workflow primero", severity="warning")
            return

        if self.running_process:
            self.app.notify("Ya hay un workflow en ejecución", severity="warning")
            return

        self._run_workflow_worker(self.current_workflow)

    @work(thread=True)
    def _run_workflow_worker(self, wf: Workflow) -> None:
        import time
        self.running_process = True
        console = self.query_one("#wf_console", RichLog)
        console.write(f"\n[bold cyan]═══ Iniciando: {wf.name} ({wf.scope.upper()}) ═══[/bold cyan]")

        start_time = time.time()
        output_lines = []
        final_code = 0

        try:
            for code, line in Workflow.run(wf):
                if line is not None:
                    console.write(line.rstrip())
                    output_lines.append(line)
                if code is not None:
                    final_code = code
                    color = "bold green" if code == 0 else "bold red"
                    console.write(f"[{color}]═══ Proceso finalizado. Codigo: {code} ═══[/{color}]\n")
                    self.app.notify(f"{wf.name} finalizó (código {code})")

            # Se loguea UNA SOLA VEZ al terminar el proceso
            duration_ms = int((time.time() - start_time) * 1000)
            log(Event.WORKFLOW_EXECUTED, {
                "workflow": wf.name,
                "path": str(wf.path),
                "exit_code": final_code,
                "duration_ms": duration_ms,
                "output": "".join(output_lines).strip()
            })

        except Exception as e:
            console.write(f"[bold red]Error al ejecutar: {e}[/bold red]\n")
            self.app.notify(f"Error al ejecutar: {e}", severity="error")
        finally:
            self.running_process = False

    def action_add_workflow(self) -> None:
        self.app.push_screen(AddWorkflowModal(), self.add_workflow)

    def add_workflow(self, data) -> None:
            if data is not None:
                script_path = data["path"]
                scope = data["scope"]
                Workflow.add(script_path, scope)
                log(Event.WORKFLOW_ADDED, {
                    "name": Path(script_path).name,
                    "path": script_path,
                    "scope": scope
                })
                added_name = Path(script_path).name
                self.load_workflows(added_name)
                self.app.notify("Workflow añadido con éxito!")

    def action_remove_workflow(self) -> None:
        if not self.current_workflow:
            self.app.notify("Selecciona un workflow para eliminar", severity="warning")
            return
        self.app.push_screen(RemoveWorkflowModal(self.current_workflow), self.remove_workflow)

    def remove_workflow(self, confirmed) -> None:
        if confirmed and self.current_workflow:
            Workflow.remove(self.current_workflow)
            log(Event.WORKFLOW_REMOVED, self.current_workflow)
            self.current_workflow = None
            self.load_workflows()
            self.app.notify("Workflow eliminado")

    def action_clear_console(self) -> None:
        self.query_one("#wf_console", RichLog).clear()
        self.app.notify("Consola limpia")

    def on_show(self) -> None:
        self.load_workflows()
