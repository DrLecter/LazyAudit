from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal

class ModifyHostModal(ModalScreen):

    def __init__(self, current_host):
        super().__init__()
        self.current_host = current_host

    def compose(self) -> ComposeResult:
        with Vertical(id="model_modify_host"):
            yield Label(f"Editar host", id="model_key")

            yield Label(" Host:")
            yield Input(value=self.current_host.hostname, id="inp_hostname")

            yield Label(" IP:")
            yield Input(value=self.current_host.ip, id="inp_ip")

            yield Label(" Puertos:")
            yield Input(value=f"{", ".join(self.current_host.ports)}", id="inp_ports")

            yield Label(" Servicios:")
            yield Input(value=f"{", ".join(self.current_host.services)}", id="inp_services")

            with Horizontal(id="modal_btns"):
                yield Button("Guardar", variant="primary", id="save_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_btn":
            new_hostname = self.query_one("#inp_hostname", Input).value.strip()
            new_ip = self.query_one("#inp_ip", Input).value.strip()
            new_ports = self.query_one("#inp_ports", Input).value.strip()
            new_services =self.query_one("#inp_services", Input).value.strip()
            
            self.dismiss({
                "hostname": new_hostname,
                "ip": new_ip,
                "ports": new_ports,
                "services": new_services
            })

        elif event.button.id == "cancel_btn":
            self.dismiss(None)