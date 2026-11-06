from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.widgets import Label, Input, Button, Select
from textual.containers import Vertical, Horizontal

class AddHostModal(ModalScreen):

    def __init__(self):
        super().__init__()

    def compose(self) -> ComposeResult:
        with Vertical(id="model_add_host"):
            yield Label(f"Nuevo host", id="model_host")

            yield Label(" Hostname:")
            yield Input(id="inp_hostname")

            yield Label(" IP:")
            yield Input(id="inp_ip")

            yield Label(" Puertos:")
            yield Input(id="inp_ports")

            yield Label(" Servicios:")
            yield Input(id="inp_services")

            with Horizontal(id="modal_btns"):
                yield Button("Guardar", variant="primary", id="save_btn")
                yield Button("Cancelar", variant="default", id="cancel_btn")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_btn":
            hostname = self.query_one("#inp_hostname", Input).value.strip()
            ip = self.query_one("#inp_ip", Input).value.strip()
            ports = self.query_one("#inp_ports", Input).value.strip()
            services = self.query_one("#inp_services", Input).value.strip()
            

            # Devuelve los valores
            self.dismiss({
                "hostname": hostname,
                "ip": ip,
                "ports": ports,
                "services": services
            })

        elif event.button.id == "cancel_btn":
            self.dismiss(None)