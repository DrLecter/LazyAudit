import argparse
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "utils"))
from actions import Project, Command, Variable, Host, Finding, Scope, Checklist, Workflow

from logger import log, Event

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

# ============ Checklist ============
checklist_args = parser.add_argument_group("Checklist")

checklist_args.add_argument("-lck", "--list-checklists", action="store_true", help="Mostrar los checklists disponibles.")

checklist_args.add_argument("-ack", "--add-checklist", nargs=2, metavar=("GROUP", "TASK"), help="Crear un checklist nuevo.")

checklist_args.add_argument("-rck", "--remove-checklist",  nargs="+", metavar=("GROUP"), help="Eliminar un checklist.")

checklist_args.add_argument("-mck", "--modify-checklist", nargs="+", metavar=("GROUP", "INDEX"), help="Modificar un checklist.")

# ========== Workflows ==========
workflows = parser.add_argument_group("Workflow")

workflows.add_argument("-lw", "--list-workflows", action="store_true", help="Mostrar los workflows disponibles.")

workflows.add_argument("-aw", "--add-workflow", nargs=1, metavar=("PATH"), help="Crear un workflow nuevo.")

workflows.add_argument("-rw", "--remove-workflow",  nargs=1, type=int, metavar=("INDEX"), help="Eliminar un workflow.")

workflows.add_argument("-xw", "--run", nargs=1, type=int, metavar=("INDEX"), help="Ejecutar un workflow.")

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

modifiers_args.add_argument("--group", metavar="GROUP")
modifiers_args.add_argument("--item", type=int, metavar="ITEM")
modifiers_args.add_argument("--task", metavar="TASK")
modifiers_args.add_argument("--toggle", action="store_true")
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

    log(Event.COMMAND_CREATED, command)

# --remove-command
elif args.remove_command:
    command_to_remove = Command.read_all()[args.remove_command[0]]
    Command.remove(command_to_remove)

    log(Event.COMMAND_REMOVED, command_to_remove)

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

    log(Event.COMMAND_MODIFIED, {"old": old_cmd, "new":new_cmd})

# --list-commands
elif args.list_commands:
    all_commands = Command.read_all()
    if args.search:
        commands_list = Command.search(args.search[0])
    else:
        commands_list = all_commands

    for i in commands_list:
        index = all_commands.index(i)
        if args.raw:
            command = i.command
        else:
            command = Command.interpolate(i)
        print(f"[{index}] - {i.title}: {command} - [{i.scope.upper()}]")
        index += 1

# ========== Proyectos ==========
# --list-projects
elif args.list_projects:
    from PATHS import ACTIVE_PROJECT
    all_projects = Project.show()
    index=0
    if args.search:
        projects_list = Project.search(args.search[0])
    else:
        projects_list = all_projects

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
            for i in projects_list:
                index = all_projects.index(i)
                if i.name == ACTIVE_PROJECT:
                    print(f"[{index}] - {i.name} (ACTIVE)")
                else:
                    print(f"[{index}] - {i.name}")
                

# --add-project
elif args.add_project:
    project = Project(*args.add_project)
    Project.add(project)

    log(Event.PROJECT_CREATED, project)

# --remove-project
elif args.remove_project:
    projects = Project.show()
    for i in projects:
        if i.name == args.remove_project[0]:
            removed_project = i
            break

    project = args.remove_project[0]
    Project.remove(project)

    log(Event.PROJECT_REMOVED, removed_project)

# --modify-project
elif args.modify_project:
    import copy
    projects = Project.read_all()
    project = projects[0]
    old_project = copy.copy(project)
    if args.name:
        project.name = args.name
    if args.description:
        project.description = args.description
    if args.status:
        project.status = args.status
    Project.modify(project)

    log(Event.PROJECT_MODIFIED, {"old":old_project, "new":project})

# --change-project
elif args.change_project:
    project = args.change_project[0]
    Project.change(project)

    log(Event.PROJECT_CHANGED, project)

# ========== Findings ==========
# --list-findings
elif args.list_findings:
    all_findings = Finding.read_all()
    if args.search:
        findings_list = Finding.search(args.search[0])
    else:
        findings_list = all_findings

    for i in findings_list:
        index = all_findings.index(i)
        print(f"[{index}] - {i.host} // {i.description}.")
        print(f"({i.severity.upper()}). Vulns: {', '.join(i.vulns)}")

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

    log(Event.FINDING_MODIFIED, {"old":old_fng,"new":new_fng})

# --remove-finding
elif args.remove_finding:
    fng = Finding.read_all()[args.remove_finding[0]]
    Finding.remove(fng)
    log(Event.FINDING_REMOVED, fng)


# --add-finding
elif args.add_finding: 
    fng = Finding(*args.add_finding)
    fng.vulns = fng.vulns.split(",")
    Finding.add(fng)

    log(Event.FINDING_CREATED, fng)

# ========== Variables ==========
# --list-variable
elif args.list_variables:
    all_vars = Variable.read_all()
    if args.search:
        variables_list = Variable.search(args.search[0])
    else:
        variables_list = all_vars

    for i in variables_list:
        index = all_vars.index(i)
        print(f"[{index}] - {i.key} : {i.value} // {i.description} - [{i.scope.upper()}]. ")

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
    log(Event.VARIABLE_MODIFIED, {"old":old_var,"new":new_var})


# --remove-variable
elif args.remove_variable:
    var = Variable.read_all()[args.remove_variable[0]]
    Variable.remove(var)

    log(Event.VARIABLE_REMOVED, var)

# --add-variable
elif args.add_variable: 
    var = Variable(*args.add_variable)
    if args.is_global: 
        var.scope = Scope.GLOBAL
    Variable.add(var)

    log(Event.VARIABLE_CREATED, var)

# ========== Hosts ==========
# --list-hosts
elif args.list_hosts:
    all_hosts = Host.read_all()
    if args.search:
        hosts_list = Host.search(args.search[0])
    else:
        hosts_list = Host.read_all()

    for i in hosts_list:
        index = all_hosts.index(i)
        print(f"[{index}] - {i.hostname} ({i.ip}) - Ports: {', '.join(i.ports)} - Services: {', '.join(i.services)}")

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

    log(Event.HOST_MODIFIED, {"old":old_host,"new":new_host})

# --remove-host
elif args.remove_host:
    host = Host.read_all()[args.remove_host[0]]
    Host.remove(host)

    log(Event.HOST_REMOVED, host)

# --add-host
elif args.add_host: 
    host = Host(*args.add_host)
    host.ports = host.ports.split(",")
    host.services = host.services.split(",")
    Host.add(host)

    log(Event.HOST_CREATED, host)

# ========== Checklist ==========
# --list-checklists
elif args.list_checklists:
    all_checklists = Checklist.read_all()
    if args.search:
        checklists_list = Checklist.search(args.search[0])
    else:
        checklists_list = Checklist.read_all()

    checklists_list.sort(key=lambda x: x.group)
    index = 1
    active_group = ""
    done = ""
    for i in checklists_list:
        if i.group != active_group:
            if active_group != "":
                print()
            active_group = i.group
            print(f"{i.group.upper()} ({i.scope.upper()})")
            group_list = [x for x in all_checklists if x.group == i.group]
        index = group_list.index(i) + 1
        if i.done:
            done = "[x]"
            print(f"[{index}] {done} - {i.task}")
        else:
            done = "[ ]"
            print(f"[{index}] {done} - {i.task}")
        
# --modify-checklist
elif args.modify_checklist:
        import copy
        group_name = args.modify_checklist[0].lower()
        filtered_list = [i for i in Checklist.read_all() if i.group.lower() == group_name]

        if args.item:
            old_checklist = filtered_list[args.item - 1]
            new_checklist = copy.copy(old_checklist)

            if args.group:
                new_checklist.group = args.group.lower()
            if args.task:
                new_checklist.task = args.task
            if args.toggle:
                new_checklist = Checklist.toggle(new_checklist)

            Checklist.modify(old_checklist, new_checklist)
            log(Event.CHECKLIST_MODIFIED, {"old": old_checklist, "new": new_checklist})
        else:
            if args.scope:
                Checklist.change_scope(group_name, args.scope)
                log(Event.CHECKLIST_MODIFIED, {"group": group_name, "new_scope": args.scope})
            if args.group:
                for i in filtered_list:
                    new_i = copy.copy(i)
                    new_i.group = args.group.lower()
                    Checklist.modify(i, new_i)
                log(Event.CHECKLIST_MODIFIED, {"old_group": group_name, "new_group": args.group.lower()})

# --remove-checklist
elif args.remove_checklist:
    filtered_list = [i for i in Checklist.read_all() if i.group.lower() == args.remove_checklist[0].lower()]
    if args.item:
        item_to_remove = filtered_list[args.item - 1]
        Checklist.remove(filtered_list[args.item-1])
        log(Event.CHECKLIST_REMOVED, item_to_remove)
    else: 
        for checklist in filtered_list:
            Checklist.remove(checklist)
            log(Event.CHECKLIST_REMOVED, checklist)


# --add-checklist
elif args.add_checklist: 
    checklist = Checklist(*args.add_checklist)
    checklist.group = checklist.group.lower()
    if args.is_global: 
        checklist.scope = Scope.GLOBAL
    Checklist.add(checklist)

    log(Event.CHECKLIST_CREATED, checklist)

# ========== Workflows ==========
# --list-workflow
elif args.list_workflows:
    all_wf = Workflow.read_all()
    if args.search:
        wf_list = Workflow.search(args.search[0])
    else:
        wf_list = all_wf

    wf_list.sort(key=lambda x: x.scope)
    for i in wf_list:
        index = all_wf.index(i)
        print(f"[{index}] {i.name} ({i.scope.upper()})")
        
# --run
elif args.run:
    import time
    wf_list = Workflow.read_all()
    wf = wf_list[args.run[0]]

    start_time = time.time()
    output = []
    exit_code = 0

    for code, line in Workflow.run(wf):
        if line is not None:
            print(line, end="", flush=True)
            output.append(line)
        if code is not None:
            exit_code = code
            print(f"ejecutado (código {code})")

    duration = int((time.time() - start_time) * 1000)

    log(Event.WORKFLOW_EXECUTED, {
        "workflow": wf.name,
        "path": str(wf.path),
        "exit_code": exit_code,
        "duration_ms": duration,
        "output": "".join(output).strip()
    })

# --remove-workflow
elif args.remove_workflow:
    wf_list = Workflow.read_all()
    wf = wf_list[args.remove_workflow[0]]
    Workflow.remove(wf)

    log(Event.WORKFLOW_REMOVED, wf)

# --add-workflow
elif args.add_workflow:
    # Al llamar se pasa PATH y --global si es global
    if args.is_global: 
        scope = Scope.GLOBAL
    else: 
        scope = Scope.PRIVATE
    script_path = str(args.add_workflow[0])
    Workflow.add(script_path, scope)

    log(Event.WORKFLOW_ADDED, {
            "name": Path(script_path).name,
            "path": script_path,
            "scope": scope
            })