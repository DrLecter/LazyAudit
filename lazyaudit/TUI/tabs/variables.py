from rich.text import Text

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, DataTable, Label, TabbedContent, TabPane
from textual.containers import Horizontal, Vertical, Grid
from textual.binding import Binding

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))
sys.path.append(str(ROOT_DIR / "utils"))
sys.path.append(str(ROOT_DIR / "TUI"))

import utils.PATHS as PATHS
from utils.actions import Command, Scope, Project, Variable, Finding, Host, Checklist, Workflow

from TUI.modals.variables.modify import ModifyVariableModal
from TUI.modals.variables.add import AddVariableModal
from TUI.modals.variables.remove import RemoveVariableModal

class VariablesTab(TabPane):

    BINDINGS = [Binding("n", "add_var", "Nueva variable",key_display="N"),
                Binding("e", "modify_var", "Editar variable",key_display="E"),
                Binding("r", "remove_var", "Eliminar variable",key_display="R")]
    
    def __init__(self):
        super().__init__("Variables", id="vars_tab")
        
    def compose(self):
        with Horizontal():
            #Columna izq.
            with Vertical():
                yield Label(f"VARIABLES")
                yield DataTable(show_header=False, id="vars_table") # Mostrar variables y host

            #Columna der.
            with Vertical():
                yield Label(f"RHOST", id="lbl_var_key") 
                yield Label(f"", id="lbl_var_desc") 

                with Horizontal():
                    yield Label(f"Valor: ", id="lbl_var_value_title") 
                    yield Label(" {RHOST}", id="lbl_var_value")

                with Horizontal():
                    yield Label(f"Scope: ", id="lbl_var_scope_title") 
                    yield Label(" {RHOST}", id="lbl_var_scope")

                #yield Label(f"DESCRIPTION", id="lbl_var_desc_title") 
                #yield Label(f"", id="lbl_var_desc") 

    def load_vars_table(self):
        table = self.query_one("#vars_table", DataTable)
        table.cursor_type = "row"

        if not table.columns:
            table.add_columns("Variable", "Host")
        table.clear() # Limpia las filas anteriores
        
        variables = Variable.read_all()
        variables.sort(key=lambda x: x.key.casefold())

        for c in variables:
            table.add_row(c.key, c.value, key=c.key)

    def on_data_table_row_highlighted(self, event: DataTable.RowSelected) -> None:
        if event.data_table.id == "vars_table":
            var_name = str(event.row_key.value)

            self.current_var = next((c for c in Variable.read_all() if c.key == var_name), None)

            self.update_var_info(self.current_var) # Command()

    def update_var_info(self, var : "Variable") -> None:
        if var:
            self.query_one("#lbl_var_key", Label).update(f"{var.key}")
            self.query_one("#lbl_var_desc", Label).update(f"{var.description}")
            self.query_one("#lbl_var_value", Label).update(f"{var.value}")

            self.query_one("#lbl_var_scope", Label).update(f"{var.scope}")

            #self.query_one("#lbl_var_desc", Label).update(f"{var}")


    def action_add_var(self) -> None:
        self.app.push_screen(AddVariableModal(), self.add_var)

    def add_var(self, data) -> None:
        if data is not None:
            variable = Variable(**data)
            Variable.add(variable)
            self.load_vars_table()
            self.update_var_info(variable)
            self.app.notify("Variable creada con éxito!")

    def action_modify_var(self) -> None:
        if self.current_var:
            self.app.push_screen(ModifyVariableModal(self.current_var), self.modify_var)
        else:
            self.app.notify("Comando no seleccionado!")

    def modify_var(self, data) -> None:
        if data is not None:
            new_var = Variable(**data)
            Variable.modify(self.current_var, new_var)
            self.load_vars_table()
            self.update_var_info(new_var)
            self.app.notify("¡Variable creada con éxito!")

    def action_remove_var(self) -> None:
        self.app.push_screen(RemoveVariableModal(self.current_var), self.remove_var)

    def remove_var(self, variable) -> None:
        if variable != None:
            Variable.remove(variable)     
            variables = Variable.read_all()
            if variables:
                self.update_var_info(variables[0])
            self.load_vars_table()
            self.app.notify("Variable eliminada con éxito!")

    def on_show(self) -> None:
        self.load_vars_table()
        variables = Variable.read_all()
        if variables:
            self.update_var_info(variables[0])
        self.query_one("#vars_table", DataTable)
        