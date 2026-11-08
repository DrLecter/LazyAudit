from models import *
import PATHS
import common
import json
from pathlib import Path
import re

# Los modelos heredan common.CommonActions que es donde está add, modify, delete y remove
# permite que se los llame directamente con la acción y se evita pasar el Path. 
# Command.reead_all(), Variable.add(), etc.
def _is_safe(name :str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9_\- ]+$", name)) and ".." not in name and "/" not in name and "\\" not in name


class Scope(ScopeData):
    pass

class Status(StatusData):
    pass

class Severity(SeverityData): 
    pass

class Command(CommandData, common.CommonActions):
    file_path = PATHS.COMMANDS_FILE      

    # Recibe un Command y devuelve el Command.command con las variables interpoladas
    @classmethod
    def interpolate(cls, command : "Command") -> str:
        modified_comand = command.command
        for i in Variable.read_all():
            modified_comand = modified_comand.replace("{" + i.key +"}", i.value)
        return modified_comand

class Variable(VariableData, common.CommonActions):
    file_path = PATHS.VARIABLES_FILE

class Project(ProjectData, common.CommonActions):

    # Recibe el status nuevo y lo cambia en el proyecto activo
    @classmethod
    def change_status(cls, new_status : str) -> None:
        project = cls.read_all()[0]
        if project.status != new_status:
            project.status = new_status
            cls.modify(project)
            #print(f"[+] Estado cambiado a {new_status}")
        #else:
            #print(f"[!] El estado ya es {new_status}")

    # Recibe un nombre de proyecto y borra el directorio de ese proyecto
    @classmethod
    def remove(cls, project_name : str) -> None:
        if not _is_safe(project_name):
            return
        project_dir = PATHS.PROJECTS_DIR/project_name

        if project_dir.exists(): 
            if project_name != PATHS.ACTIVE_PROJECT:
                from shutil import rmtree
                rmtree(project_dir)
            else:
                pass
        else:
            print("[!] Proyecto inexistente")

    # Recibe el Project completo y lo sobreescribe al viejo
    @classmethod
    def modify(cls, new_project) -> None:
        old_project = cls.read_all()

        if old_project[0] != new_project:
            common._save(cls.file_path, new_project)

        if cls.file_path.parent.name != new_project.name:
            project_dir = cls.file_path.parent
            project_dir.rename(project_dir.parent/new_project.name)
            cls.change(new_project.name)

    # Recibe un Project y crea el directorio, los archivos y llena el project.json 
    @classmethod
    def add(cls, new_project : "Project") -> None:
        if not _is_safe(new_project.name):
            raise ValueError("Nombre de proyecto inválido (solo se permite letras, números y guiones.)")
        base_files = ["commands.json", "findings.json", "hosts.json", "variables.json", "checklists.json"]
        project_dir = Path(PATHS.PROJECTS_DIR/new_project.name)
        project_dir.mkdir(parents=True, exist_ok=True)
        (project_dir / "workflows").mkdir(exist_ok=True)
        for path in base_files: 
            Path(project_dir/path).touch()
        common._save(project_dir/"project.json", new_project)

    # Devuelve una lista de Models de los poyectos disponibles
    @classmethod
    def show(cls):
        if not PATHS.PROJECTS_DIR.exists():
            return []
        projects = PATHS.PROJECTS_DIR.iterdir()
        projects_list = []
        for i in projects:
            project_file = i / "project.json"
            if i.is_dir() and project_file.exists():
                item = common._extract_data(project_file)
                projects_list.extend(item)
        return sorted([cls(**item) for item in projects_list], key=lambda x: x.name)


    # Recibe un nombre de proyecto y setea la variable ACTIVE_PROJECT
    @classmethod
    def change(cls, new_project : str) -> None:
        if not _is_safe(new_project):
            return
        with open(PATHS.CONFIG_FILE, "r") as f:
            data = json.load(f)
            active_project = data["project"]

        if active_project != new_project:
            # Verifica que el pryecto al que se quiere cambiar exista
            if (PATHS.PROJECTS_DIR / new_project).exists():
                with open(PATHS.CONFIG_FILE, "w") as f:
                    json.dump({"project": new_project}, f, indent=4, ensure_ascii=False)

                PATHS.reload_paths()

                Command.file_path = PATHS.COMMANDS_FILE
                Variable.file_path = PATHS.VARIABLES_FILE
                Project.file_path = PATHS.PROJECT_FILE
                Finding.file_path = PATHS.FINDINGS_FILE
                Host.file_path = PATHS.HOSTS_FILE
                Checklist.file_path = PATHS.CHECKLISTS_FILE
        #        print(f"[+] Proyecto cambiado a: {new_project}")
        #else: 
        #    print(f"[!] Proyecto no existente")

    file_path = PATHS.PROJECT_FILE # No borrar

class Finding(FindingData, common.CommonActions):
    file_path = PATHS.FINDINGS_FILE

class Host(HostData, common.CommonActions):
    file_path = PATHS.HOSTS_FILE

class Checklist(ChecklistData, common.CommonActions):
    @classmethod
    def toggle(cls, item):
        old_item = Checklist(**vars(item))
        item.done = not item.done
        cls.modify(old_item, item)

    file_path = PATHS.CHECKLISTS_FILE

    @classmethod
    def change_scope(cls, group: str, new_scope: str):
        items = cls.read_all()
        for i in items:
            if i.group.lower() == group.lower():
                i.scope = new_scope
        common._save(cls.file_path, items)

class Workflow(WorkflowData, common.CommonActions):
    # Devuelve una lista de Models 
    @classmethod
    def read_all(cls):
        workflows_list = []
        if PATHS.GLOBAL_WORKFLOWS_DIR.exists():
            for wf_file in PATHS.GLOBAL_WORKFLOWS_DIR.iterdir():
                if wf_file.is_file():
                    wf = Workflow(name=wf_file.name, path=Path(wf_file), scope=Scope.GLOBAL)
                    workflows_list.append(wf)

        if PATHS.WORKFLOWS_DIR.exists():
            for wf_file in PATHS.WORKFLOWS_DIR.iterdir():
                if wf_file.is_file():
                    wf = Workflow(name=wf_file.name, path=Path(wf_file), scope=Scope.PRIVATE)
                    workflows_list.append(wf)

        workflows_list.sort(key=lambda x: x.scope)
        return workflows_list

    # Recibe un Path (del script a agregar) y el scope y lo agrega a la respectiva carpeta
    @classmethod
    def resolve_script_path(cls, path_or_name: str | Path) -> Path:
        p = Path(path_or_name)
        if p.is_file():
            return p
        inbox_file = PATHS.INBOX_DIR / p.name
        if inbox_file.is_file():
            return inbox_file
        return p

    @classmethod
    def add(cls, script_path, scope=Scope.PRIVATE):
        from shutil import copy
        resolved = cls.resolve_script_path(script_path)
        if not resolved.is_file():
            raise FileNotFoundError(f"No se encontró el script en '{script_path}' ni en '{PATHS.INBOX_DIR / Path(script_path).name}'")
        if scope == Scope.GLOBAL:
            copy(resolved, PATHS.GLOBAL_WORKFLOWS_DIR)
        else:
            copy(resolved, PATHS.WORKFLOWS_DIR)   

    @classmethod
    def remove(cls, workflow : "Workflow"):
        Path(workflow.path).unlink()

    @classmethod
    def run(cls, workflow, timeout: int = 10): #600 = 10 minutos
        import subprocess, sys, time

        if workflow.name.endswith(".sh"):
            cmd = ["bash", str(workflow.path)]
        elif workflow.name.endswith(".py"):
            cmd = [sys.executable, "-u", str(workflow.path)]
        else:
            return

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        start_time = time.time()
        while True:
            # Revisa si se pasó del tiempo
            if time.time() - start_time > timeout:
                process.kill()
                yield -1, f"\n[!] Timeout de {timeout}s excedido. Proceso terminado forzosamente.\n"
                return

            line = process.stdout.readline()
            if line:
                yield None, line
            elif process.poll() is not None:
                # El proceso terminó normalmente
                break
            else:
                time.sleep(0.1)

        yield process.returncode, None