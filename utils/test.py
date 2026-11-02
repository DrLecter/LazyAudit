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

# ========== Variables ==========

# ========== Proyectos ==========
project_args = parser.add_argument_group("Projects")

project_args.add_argument("-lp", "--list-projects", action="store_true", help="Mostrar los proyectos disponibles.")
project_args.add_argument("--active", action="store_true", help="Mostrar el proyecto activo (uso en --list-projects).")

project_args.add_argument("-ap", "--add-project", nargs=3, metavar=("NAME", "DESCRIPTION", "STATUS"), help="Crear un prpyecto nuevo.")

project_args.add_argument("-rp", "--remove-project", nargs=1, metavar="NAME", help="Eliminar un proyecto.")

project_args.add_argument("-mp", "--modify-project", action="store_true", help="Modificar el proyecto actual.")
project_args.add_argument("--name", metavar="NAME", help="Indicador de nombre (uso en -m / --modify-project).")
project_args.add_argument("--description", metavar="NAME", help="Indicador de descripción (uso en -m / --modify-project).")
project_args.add_argument("--status", metavar="NAME", help="Indicador de estado (uso en -m / --modify-project).")

project_args.add_argument("-cp", "--change-project", nargs=1, metavar="NAME", help="Cambiar de proyecto.")

# ========== Findings ===========

# ============ Hosts ============

# ========== Funciones ==========
args = parser.parse_args()

# ========== Comandos ===========
# --list-projects
if args.list_projects:
    if not args.active:
        for i in Project.show():
            print(i)
    else:
        for i in Project.show():
            if i == Project.file_path.parent.name:
                print(i)

# --add-project
elif args.add_project:
    project = Project(*args.add_project)
    print(project)
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
elif args.change_project:
    project = args.change_project[0]
    Project.change(project)