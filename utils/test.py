from dataclasses import asdict
import json
import common
from pathlib import Path
import PATHS

#old_data = common.read_all(Path("utils/data.json"), CommandData)
#print(old_data)

#print(common.read_all(Path("utils/data.json"), CommandData)) # -> [Model(), Model()]
'''
hosts = common.read_all(PATHS.HOSTS_FILE)

for host in hosts:
    print(host)

old_host = HostData    (
        ip= "10.10.20.15",
        hostname = "dc01.corp.local",
        ports = [
            "53",
            "88",
            "389",
            "445"
        ],
        services = [
            "Simple DNS Plus",
            "Kerberos",
            "Microsoft Windows AD LDAP",
            "Microsoft-DS SMB"
        ]
)

new_host = HostData(
            ip="nuevo",
            hostname="nuevo",
            ports=["nuevo"],
            services=["nuevo"]
        )

# Recibe la [Model(), Model()] a modificar, el dato viejo (sacado de la tui) y el dato nuevo (armado)
def modify(data, old_model, new_model) -> None:
    for model in data:
        if model == old_model:
            index = data.index(model)
            data[index] = new_model

modify(hosts, old_host, new_host)

for host in hosts:
    print(host)


'''
from actions import Variable, Host, Command, Project, Scope, Project
#print(Command.read_all())


comando = Command(title='Global Nikto scan', command='nikto -h http://{RHOST} {LPORT}', description='Escaneo de vulnerabilidades comunes en servidores web', tags=['web', 'vuln-scan'], scope='global')
#Command.add(comando)

#print(Command.read_all())

#from datetime import datetime
#new_project = Project(name="audit_test3")
#Project.add(new_project)

#Project.modify(new_project)

#Project.change("audit_test3")

#Project.remove("audit_test")
#from actions import Status
#Project.change_status(Status.ACTIVE)

#Command.interpolate(comando)

