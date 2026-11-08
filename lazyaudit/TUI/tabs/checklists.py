import sys
from pathlib import Path

from textual.app import ComposeResult
from textual.widgets import Label, TabPane, ListView, ListItem
from textual.containers import Horizontal, Vertical
from textual.binding import Binding

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))
sys.path.append(str(ROOT_DIR / "utils"))
sys.path.append(str(ROOT_DIR / "TUI"))

from utils.actions import Checklist
from utils.common import _save
from utils.logger import log, Event

from TUI.modals.checklists.modify_group import ModifyGroupModal
from TUI.modals.checklists.modify_task import ModifyTaskModal
from TUI.modals.checklists.add_group import AddGroupModal
from TUI.modals.checklists.add_task import AddTaskModal
from TUI.modals.checklists.remove_group import RemoveGroupModal
from TUI.modals.checklists.remove_task import RemoveTaskModal

class GroupItem(ListItem):
    def __init__(self, group_name: str, total: int, done: int, scope: str) -> None:
        super().__init__()
        self.group_name = group_name
        self.total = total
        self.done = done
        self.scope = scope

    def compose(self) -> ComposeResult:
        yield Label(f"{self.group_name}  [{self.done}/{self.total}]")
        yield Label(f"{self.scope.upper()}")


class TaskItem(ListItem):
    def __init__(self, checklist_obj: Checklist) -> None:
        super().__init__()
        self.checklist_obj = checklist_obj

    def compose(self) -> ComposeResult:
        mark = "\\[X]"
        if self.checklist_obj.done == False:
            mark = "\\[ ]"
        
        yield Label(f"{mark} - {self.checklist_obj.task}")

class ChecklistsTab(TabPane):

    BINDINGS = [
        Binding("n", "add_checklist", "Nuevo checklist", key_display="N"),
        Binding("e", "modify_checklist", "Editar checklist", key_display="E"),
        Binding("r", "remove_checklist", "Eliminar checklist", key_display="R"),
        Binding("space", "toggle_task", "Marcar/Desmarcar", key_display="SPACE"),
        Binding("right", "app.focus_next", "Siguiente", show=False),
        Binding("left", "app.focus_previous", "Anterior", show=False)
    ]

    def __init__(self) -> None:
        super().__init__("Checklists", id="checklists_tab")
        self.current_group : str | None = None
        self.current_task : Checklist | None = None

    def compose(self) -> ComposeResult:
        with Horizontal():
            # Columna izquierda - Lista de Grupos
            with Vertical(id="col_checklists_list"):
                yield ListView(id="groups_list")

            # Columna derecha - Tareas del grupo
            with Vertical(id="col_checklists_detail"):
                yield ListView(id="tasks_list")

    def on_mount(self) -> None:
        self.query_one("#col_checklists_list").border_title = "CHECKLISTS"
        self.query_one("#col_checklists_detail").border_title = "TAREAS"

    def load_groups(self, target_group : str | None = None) -> None:
        groups_lv = self.query_one("#groups_list", ListView)
        groups_lv.clear()

        all_items = Checklist.read_all()
        if not all_items:
            self.query_one("#tasks_list", ListView).clear()
            self.query_one("#col_checklists_detail").border_title = "TAREAS (Sin datos)"
            return

        groups_dict = {}
        for item in all_items:
            groups_dict.setdefault(item.group, []).append(item)

        items_to_add = []
        for group_name in sorted(groups_dict.keys()):
            tasks = groups_dict[group_name]
            total = len(tasks)

            done_count = 0
            for task in tasks:
                if task.done:
                    done_count += 1

            scopes = {t.scope for t in tasks}
            scope_str = "global" if scopes == {"global"} else "private"
            items_to_add.append(GroupItem(group_name, total, done_count, scope_str))

        groups_lv.extend(items_to_add)

        if items_to_add:
            selected_name = target_group or self.current_group
            idx = next((i for i, item in enumerate(items_to_add) if item.group_name == selected_name), 0)

            groups_lv.index = None
            groups_lv.index = idx
            self.current_group = items_to_add[idx].group_name
            self.load_tasks(self.current_group)

    def load_tasks(self, group_name: str) -> None:
        tasks_lv = self.query_one("#tasks_list", ListView)
        tasks_lv.clear()

        all_items = Checklist.read_all()
        group_tasks = [item for item in all_items if item.group == group_name]

        self.query_one("#col_checklists_detail").border_title = f"{group_name.upper()} ({len(group_tasks)})"

        if group_tasks:
            tasks_lv.extend(TaskItem(t) for t in group_tasks)
            tasks_lv.index = None
            self.current_task = group_tasks[0]
        else:
            self.current_task = None

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
                if event.list_view.id == "groups_list":
                    if event.item:
                        self.current_group = event.item.group_name
                        self.load_tasks(self.current_group)

                elif event.list_view.id == "tasks_list":
                    if event.item:
                        self.current_task = event.item.checklist_obj

    def get_selected_target(self):
        # Devuelve ('group', group_name) o ('task', checklist_obj) según la lista enfocada
        if self.query_one("#groups_list", ListView).has_focus:
            return "group", self.current_group
        elif self.query_one("#tasks_list", ListView).has_focus:
            return "task", self.current_task
        return None, None

# ========== Actions ==========

    def action_toggle_task(self) -> None:
        target_type, _ = self.get_selected_target()
        if target_type == "task":
            if self.current_task:
                old_task = Checklist(**vars(self.current_task))
                Checklist.toggle(self.current_task)
                log(Event.CHECKLIST_MODIFIED, {"old": old_task, "new": self.current_task})
                if self.current_group:
                    self.load_tasks(self.current_group)
                self.load_groups()

    def action_add_checklist(self) -> None:
        target_type, _ = self.get_selected_target()

        if target_type == "group":
            self.app.push_screen(AddGroupModal(), self.add_checklist) # Para el group, tiene que tener si o si para agergar la primer tarea
        elif target_type == "task":
            self.app.push_screen(AddTaskModal(self.current_group), self.add_checklist)  # Para task, el group se elije con Select.

    def add_checklist(self, data):
        if data is not None:
            new_item = Checklist(**data)
            Checklist.add(new_item)
            log(Event.CHECKLIST_CREATED, new_item)
            self.load_groups(new_item.group)
            self.load_tasks(new_item.group)
            self.app.notify("Checklist agregado con éxito!")

    def action_modify_checklist(self) -> None:
        target_type, _ = self.get_selected_target()

        if target_type == "group":
            self.app.push_screen(ModifyGroupModal(self.current_group), self.rename_group)

        elif target_type == "task":
            self.app.push_screen(ModifyTaskModal(self.current_task), self.modify_task)

    def rename_group(self, new_group_name):
        if new_group_name is not None:
            old_name = self.current_group
            new_name = new_group_name["group"]
            items = Checklist.read_all()
            for item in items:
                if item.group == old_name:
                    item.group = new_name
            _save(Checklist.file_path, items)
            log(Event.CHECKLIST_MODIFIED, {"old_group": old_name, "new_group": new_name})

            self.current_group = new_name
            self.load_groups(new_name)
            self.load_tasks(self.current_group)

    def modify_task(self, data):
        if data is not None:
            old_item = self.current_task
            new_item = Checklist(**data)
            Checklist.modify(old_item, new_item)
            log(Event.CHECKLIST_MODIFIED, {"old": old_item, "new": new_item})

            if self.current_group:
                self.load_tasks(self.current_group)
            self.load_groups()

    def action_remove_checklist(self) -> None:
        target_type, _ = self.get_selected_target()

        if target_type == "group":
            self.app.push_screen(RemoveGroupModal(self.current_group), self.remove_group)

        elif target_type == "task":
            self.app.push_screen(RemoveTaskModal(self.current_task), self.remove_task)
 
    def remove_group(self, group_name):
        all_items = Checklist.read_all()
        count = sum(1 for i in all_items if i.group == group_name)
        items = [item for item in all_items if item.group != group_name]
        _save(Checklist.file_path, items)
        log(Event.CHECKLIST_REMOVED, {"group": group_name, "count": count})
        self.current_group = None
        self.load_groups()

    def remove_task(self, confirmed):
        if confirmed and self.current_task:
            task_to_remove = self.current_task
            Checklist.remove(task_to_remove)
            log(Event.CHECKLIST_REMOVED, task_to_remove)
            if self.current_group:
                self.load_tasks(self.current_group)
            self.load_groups()
            self.app.notify("Tarea eliminada")
            
    def on_show(self) -> None:
        self.load_groups()

