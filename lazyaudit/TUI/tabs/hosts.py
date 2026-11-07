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

from TUI.modals.hosts.modify import ModifyHostModal
from TUI.modals.hosts.add import AddHostModal
from TUI.modals.hosts.remove import RemoveHostModal

class HostsTab(TabPane):

    BINDINGS = [Binding("n", "add_host", "Nuevo host", key_display="N"),
                Binding("e", "modify_host", "Editar host", key_display="E"),
                Binding("r", "remove_host", "Eliminar host", key_display="R")]
    
    def __init__(self):
        super().__init__("Hosts", id="hosts_tab")
        
    def compose(self):
        with Horizontal():
            #Columna izq.
            with Vertical():
                yield Label(f"HOSTS")
                yield DataTable(show_header=False, id="hosts_table")

            #Columna der.
            with Vertical():
                yield Label(f"HOSTNAME: ", id="lbl_host_host") 
                yield Label("IP", id="lbl_host_ip") 

                yield Label(f"Puertos: ", id="lbl_host_ports")
                yield Label(f"Servicios: ", id="lbl_host_services") 


    def load_hosts_table(self):
        table = self.query_one("#hosts_table", DataTable)
        table.cursor_type = "row"

        if not table.columns:
            table.add_columns("hostname", "ip")
        table.clear() # Limpia las filas anteriores
        
        hosts = Host.read_all()
        hosts.sort(key=lambda x: x.ip)

        for h in hosts:
            table.add_row(h.hostname[:15].strip(), h.ip, key=h.ip)

    def on_data_table_row_highlighted(self, event: DataTable.RowSelected) -> None:
        if event.data_table.id == "hosts_table":
            host_ip = str(event.row_key.value)
            self.current_host = next((h for h in Host.read_all() if h.ip == host_ip), None)

            self.update_host_info(self.current_host) # Command()

    def update_host_info(self, host : "Host") -> None:
        if host:
            self.query_one("#lbl_host_host", Label).update(f"{host.hostname}")
            self.query_one("#lbl_host_ip", Label).update(f"{host.ip}")

            ports = ", ".join(p if isinstance(p, str) else str(p[0]) for p in host.ports) # Parche para no crashear, convierte todo a string antes de join()
            self.query_one("#lbl_host_ports", Label).update(f"Puertos: {ports}")

            services = ", ".join(s if isinstance(s, str) else str(s[0]) for s in host.services)
            self.query_one("#lbl_host_services", Label).update(f"Servicios: {services}")

    def action_add_host(self) -> None:
        self.app.push_screen(AddHostModal(), self.add_host)

    def add_host(self, data) -> None:
        if data is not None:
            data["ports"] = [p.strip() for p in data["ports"].split(",") if p.strip()] if data["ports"] else []
            data["services"] = [s.strip() for s in data["services"].split(",") if s.strip()] if data["services"] else []
            host = Host(**data)
            Host.add(host)
            self.load_hosts_table()
            self.update_host_info(host)
            self.app.notify("Host creado con éxito!")

    def action_modify_host(self) -> None:
        if self.current_host:
            self.app.push_screen(ModifyHostModal(self.current_host), self.modify_host)
        else:
            self.app.notify("Comando no seleccionado!")

    def modify_host(self, data) -> None:
        if data is not None:
            clean_ports = [p.strip() for p in data["ports"].split(",") if p.strip()] if data["ports"] else []
            clean_services = [s.strip() for s in data["services"].split(",") if s.strip()] if data["services"] else []
            new_host = Host(**data)
            new_host.ports = clean_ports
            new_host.services = clean_services
            Host.modify(self.current_host, new_host)
            self.load_hosts_table()
            self.update_host_info(new_host)
            self.app.notify("¡Host actualizado con éxito!")

    def action_remove_host(self) -> None:
        self.app.push_screen(RemoveHostModal(self.current_host), self.remove_host)

    def remove_host(self, host) -> None:
        if host != None:
            Host.remove(host)     
            hosts = Host.read_all()
            if hosts:
                self.update_host_info(hosts[0])
            self.load_hosts_table()
            self.app.notify("Host eliminado con éxito!")

    def on_show(self) -> None:
        self.load_hosts_table()
        hosts = Host.read_all()
        if hosts:
            self.update_host_info(hosts[0])
        self.query_one("#hosts_table", DataTable)
         