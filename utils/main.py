import argparse
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "utils"))
from actions import Project, Command, Variable, Host, Finding, Scope, Status

# 1. Sin parámetros (ej. -lp): lleva action="store_true".
# 2. Con 1 parámetro (ej. -sp audit_test1): no lleva action (es el comportamiento por defecto, te guarda el string que escribas en args.set_project).
# 3. Con 2 o más parámetros (ej. -sv RHOST 10.10.10.5): lleva nargs=2 (y te guarda una lista de 2 elementos ["RHOST", "10.10.10.5"] en args.set_var).

parser = argparse.ArgumentParser(description='LazyAudit')

# ========== Comandos ===========
commands_args = parser.add_argument_group("Commands")

commands_args.add_argument("-lc","--list-commands", action="store_true", help="Lista los comandos disponibles, tanto globales como privados")

commands_args.add_argument("-ac", "--add-command", nargs=4, metavar=("TITLE", "COMMAND", "DESCRIPTION", "TAGS"), help="Agrega un comando a la lista (PRIVATE por defecto).")

commands_args.add_argument("-rc", "--remove-command", nargs=1, type=int, metavar="INDEX", help="Eliminar un comando.")

commands_args.add_argument("-mc", "--modify-command", nargs=1, type=int, metavar="INDEX", help="Modificar un comando.")

# ========== Variables ==========
vars_args = parser.add_argument_group("Variables")

vars_args.add_argument("-lv", "--list-variables", action="store_true", help="Mostrar las variables disponibles.")

vars_args.add_argument("-av", "--add-variable", nargs=3, metavar=("KEY", "VALUE", "DESCRIPTION"), help="Crear una variable nueva.")

vars_args.add_argument("-rv", "--remove-variable",  nargs=1, type=int, metavar="INDEX", help="Eliminar una variable.")

vars_args.add_argument("-mv", "--modify-variable", nargs=1, type=int, metavar="INDEX", help="Modificar una variable.")

# ========== Proyectos ==========
project_args = parser.add_argument_group("Projects")

project_args.add_argument("-lp", "--list-projects", action="store_true", help="Mostrar los proyectos disponibles.")

project_args.add_argument("-ap", "--add-project", nargs=3, metavar=("NAME", "DESCRIPTION", "STATUS"), help="Crear un proyecto nuevo.")

project_args.add_argument("-rp", "--remove-project", nargs=1, metavar="NAME", help="Eliminar un proyecto.")

project_args.add_argument("-mp", "--modify-project", action="store_true", help="Modificar el proyecto actual.")

project_args.add_argument("-cp", "--change-project", nargs=1, metavar="NAME", help="Cambiar de proyecto.")


# ========== Findings ===========
findings_args = parser.add_argument_group("Findings")

findings_args.add_argument("-lf", "--list-findings", action="store_true", help="Mostrar los hallazgos disponibles.")

findings_args.add_argument("-af", "--add-finding", nargs=4, metavar=("HOST", "DESCRIPTION", "VULNS", "SEVERITY"), help="Crear un hallazgo nuevo.")

findings_args.add_argument("-rf", "--remove-finding",  nargs=1, type=int, metavar="INDEX", help="Eliminar un hallazgo.")

findings_args.add_argument("-mf", "--modify-finding", nargs=1, type=int, metavar="INDEX", help="Modificar un hallazgo.")

# ============ Hosts ============
hosts_args = parser.add_argument_group("Hosts")

hosts_args.add_argument("-lh", "--list-hosts", action="store_true", help="Mostrar los clientes disponibles.")

hosts_args.add_argument("-ah", "--add-host", nargs=4, metavar=("IP", "HOSTNAME", "PORTS", "SERVICES"), help="Crear un cliente nuevo.")

hosts_args.add_argument("-rh", "--remove-host",  nargs=1, type=int, metavar="INDEX", help="Eliminar un cliente.")

hosts_args.add_argument("-mh", "--modify-host", nargs=1, type=int, metavar="INDEX", help="Modificar un cliente.")

# ========== Modyfiers ==========
modifiers_args = parser.add_argument_group("Modifiers")

modifiers_args.add_argument("--title", metavar="TITLE")
modifiers_args.add_argument("--command", metavar="COMMAND")
modifiers_args.add_argument("--description", metavar="DESCRIPTION")
modifiers_args.add_argument("--tags", metavar="TAGS")
modifiers_args.add_argument("--name", metavar="NAME")
modifiers_args.add_argument("--status", metavar="STATUS", choices=["active", "paused", "finished"])
modifiers_args.add_argument("--host", metavar="HOST")
modifiers_args.add_argument("--vulns", metavar="VULNERABILITIES")
modifiers_args.add_argument("--severity", metavar="SEVERITY", choices=["low", "medium", "high"])
modifiers_args.add_argument("--key", metavar="KEY")
modifiers_args.add_argument("--value", metavar="VALUE")
modifiers_args.add_argument("--scope", metavar="SCOPE", choices=["global","private"])
modifiers_args.add_argument("--ip", metavar="IP")
modifiers_args.add_argument("--hostname", metavar="HOSTNAME")
modifiers_args.add_argument("--ports", metavar="PORTS")
modifiers_args.add_argument("--services", metavar="SERVICES")

modifiers_args.add_argument("-v", "--verbose", action="store_true")
modifiers_args.add_argument("--active", action="store_true")
modifiers_args.add_argument("--raw", action="store_true")
modifiers_args.add_argument("--global", dest="is_global", action="store_true", help="Agrega un comando a la lista global de variables.")
modifiers_args.add_argument("-s", "--search", nargs=1, metavar="QUERY", help="Filtra por búsqueda difusa (usar con -lp, -lc, -lv, -lh, -lf).")

# ==================== Funciones ====================
args = parser.parse_args()

# ========== Comandos ===========
# --add-command
if args.add_command:
    command = Command(*args.add_command)
    command.tags = command.tags.split(",")
    if args.is_global:
        command.scope = Scope.GLOBAL
    Command.add(command)

# --remove-command
elif args.remove_command:
    command_to_remove = Command.read_all()[args.remove_command[0]]
    Command.remove(command_to_remove)

# --modify-command
elif args.modify_command:
    old_cmd = Command.read_all()[args.modify_command[0]]
    new_cmd = Command.read_all()[args.modify_command[0]]

    if args.title:
        new_cmd.title = args.title
    if args.command:
        new_cmd.command = args.command
    if args.description:
        new_cmd.description = args.description
    if args.tags:
        new_cmd.tags = args.tags.split(",")
    if args.scope: 
        new_cmd.scope = args.scope

    Command.modify(old_cmd, new_cmd)

# --list-commands
elif args.list_commands:
    if args.search:
        commands_list = Command.search(args.search[0])
    else:
        commands_list = Command.read_all()

    index = 0
    for i in commands_list:
        if args.raw:
            command = i.command
        else:
            command = Command.interpolate(i).replace("Global", "")
        print(f"[{index}] - {i.title}: {command} - [{i.scope.upper()}]")
        index += 1

# ========== Proyectos ==========
# --list-projects
elif args.list_projects:
    if args.search:
        projects_list = Project.search(args.search[0])
    else:
        projects_list = Project.show()

    if args.active:
        if args.verbose:
            for i in projects_list:
                if i.name == Project.file_path.parent.name:
                    print("----------")
                    print(f"Nombre: {i.name}")
                    print(f"Descripcion: {i.description}")
                    print(f"Estado: {i.status.upper()}")
                    print(f"Fecha de creación: {i.created}\n")
        else:
            for i in projects_list:
                if i.name == Project.file_path.parent.name:
                    print(i.name)
    else:
        if args.verbose:
            for i in projects_list:
                print("----------")
                print(f"Nombre: {i.name}")
                print(f"Descripcion: {i.description}")
                print(f"Estado: {i.status.upper()}")
                print(f"Fecha de creación: {i.created}\n")
        else:
            index = 0
            for i in projects_list:
                print(f"[{index}] - {i.name}")
                index += 1

# --add-project
elif args.add_project:
    project = Project(*args.add_project)
    Project.add(project)

# --remove-project
elif args.remove_project:
    project = args.remove_project[0]
    Project.remove(project)

# --modify-project
elif args.modify_project:
    project = Project.read_all()[0]
    if args.name:
        project.name = args.name
    if args.description:
        project.description = args.description
    if args.status:
        project.status = args.status
    Project.modify(project)

# --change-project
elif args.change_project:
    project = args.change_project[0]
    Project.change(project)

# ========== Findings ==========
# --list-findings
elif args.list_findings:
    if args.search:
        findings_list = Finding.search(args.search[0])
    else:
        findings_list = Finding.read_all()

    index = 0
    for i in findings_list:
        print(f"[{index}] - {i.host} // {i.description}.")
        print(f"({i.severity.upper()}). Vulns: {', '.join(i.vulns)}")
        index += 1

# --modify-finding
elif args.modify_finding:
    old_fng = Finding.read_all()[args.modify_finding[0]]
    new_fng = Finding.read_all()[args.modify_finding[0]]

    if args.host:
        new_fng.host = args.host
    if args.description:
        new_fng.description = args.description
    if args.vulns:
        new_fng.vulns = args.vulns.split(",")
    if args.severity:
        new_fng.severity = args.severity

    Finding.modify(old_fng, new_fng)

# --remove-finding
elif args.remove_finding:
    fng = Finding.read_all()[args.remove_finding[0]]
    Finding.remove(fng)

# --add-finding
elif args.add_finding: 
    fng = Finding(*args.add_finding)
    fng.vulns = fng.vulns.split(",")
    Finding.add(fng)

# ========== Variables ==========
# --list-variable
elif args.list_variables:
    if args.search:
        variables_list = Variable.search(args.search[0])
    else:
        variables_list = Variable.read_all()

    index = 0
    for i in variables_list:
        print(f"[{index}] - {i.key} : {i.value} // {i.description} - [{i.scope.upper()}]. ")
        index += 1

# --modify-variable
elif args.modify_variable:
    old_var = Variable.read_all()[args.modify_variable[0]]
    new_var = Variable.read_all()[args.modify_variable[0]]

    if args.key:
        new_var.key = args.key
    if args.value:
        new_var.value = args.value
    if args.description:
        new_var.description = args.description
    if args.scope:
        new_var.scope = args.scope

    Variable.modify(old_var, new_var)

# --remove-variable
elif args.remove_variable:
    var = Variable.read_all()[args.remove_variable[0]]
    Variable.remove(var)

# --add-variable
elif args.add_variable: 
    var = Variable(*args.add_variable)
    if args.is_global: 
        var.scope = Scope.GLOBAL
    Variable.add(var)

# ========== Hosts ==========
# --list-hosts
elif args.list_hosts:
    if args.search:
        hosts_list = Host.search(args.search[0])
    else:
        hosts_list = Host.read_all()

    index = 0
    for i in hosts_list:
        print(f"[{index}] - {i.hostname} ({i.ip}) - Ports: {', '.join(i.ports)} - Services: {', '.join(i.services)}")
        index += 1

# --modify-host
elif args.modify_host:
    old_host = Host.read_all()[args.modify_host[0]]
    new_host = Host.read_all()[args.modify_host[0]]

    if args.ip:
        new_host.ip = args.ip
    if args.hostname:
        new_host.hostname = args.hostname
    if args.ports:
        new_host.ports = args.ports.split(",")
    if args.services:
        new_host.services = args.services.split(",")

    Host.modify(old_host, new_host)

# --remove-host
elif args.remove_host:
    host = Host.read_all()[args.remove_host[0]]
    Host.remove(host)

# --add-host
elif args.add_host: 
    host = Host(*args.add_host)
    host.ports = host.ports.split(",")
    host.services = host.services.split(",")
    Host.add(host)