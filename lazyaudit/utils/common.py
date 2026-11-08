from rapidfuzz import fuzz
from pathlib import Path
import json
from dataclasses import asdict
import PATHS
# ==============================

# Recibe un query (para buscar), los lugares donde buscar y devuelve bool 
def _fuzzy_matches(query: str, text_fields: list[str], threshold: int = 86) -> bool:
        query = query.lower()
        for field_val in text_fields:
            text_field = (field_val or "").lower()
            if query in text_field:
                return True
            if fuzz.partial_ratio(query, text_field) >= threshold:
                return True
        return False

# Recibe el path donde guardar y una lista de objetos y los escribe en JSON
def _write_json(file_path: Path, data : list) -> None:
    # Asegura que el directorio exista antes de escribir el archivo
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump([asdict(item) for item in data], f, indent=4, ensure_ascii=False)

# Recibe el path donde guardar y una lista de models 
# y los guarda en global o private si es que tienen 
def _save(file_path : Path, data : list) -> None:
    if not isinstance(data, list): 
        data = [data]

    if file_path.name in ("commands.json", "variables.json", "checklists.json"):
        from models import ScopeData
        global_list = []
        private_list = []

        # Separa los elementos entre globales y privados
        for i in data:
            if i.scope == ScopeData.GLOBAL:
                global_list.append(i)
            if i.scope == ScopeData.PRIVATE:
                private_list.append(i)

        if file_path.name == "commands.json":
            _write_json(PATHS.GLOBAL_COMMANDS_FILE, global_list)
        elif file_path.name == "variables.json":
            _write_json(PATHS.GLOBAL_VARS_FILE, global_list)
        elif file_path.name == "checklists.json":
            _write_json(PATHS.GLOBAL_CHECKLISTS_FILE, global_list)        
        _write_json(file_path, private_list)
    else:
        _write_json(file_path, data)

# Recibe un json y extrae la info, devuelve una lista con dict.
def _extract_data(json_file):
    if not Path(json_file).exists():
        return []
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            return data
    except (json.JSONDecodeError, FileNotFoundError):
        return []

# Acciones generales de los modelos (read, add, remove, modify, delete)
class CommonActions():

    # Recibe un query y devuelve una lista de modelos.
    # Command.search(query)
    @classmethod
    def search(cls, query: str, threshold: int = 86) -> list:
        if cls.__name__ == "Project":
            data = cls.show()
        else:
            data = cls.read_all()
        resultados = []

        for item in data:
            campos = []
            for valor in asdict(item).values():
                if isinstance(valor, list):
                    campos.extend([str(v) for v in valor])
                else:
                    campos.append(str(valor))

            if _fuzzy_matches(query, campos, threshold):
                resultados.append(item)

        return resultados

    # Cambia el Scope de los modelos con Scope.
    # Command.change_scope(Command)
    @classmethod
    def change_scope(cls, item):
        from actions import Scope
        if item.scope == Scope.PRIVATE:
            item.scope = Scope.GLOBAL
        else:
            item.scope = Scope.PRIVATE
        return item

    # Lee el json y devuelve una lista de objetos
    # Command/Host/Variable.read_all()
    @classmethod
    def read_all(cls) -> list:
        data_file : Path = cls.file_path
        global_file = None
        data = []

        if data_file.name == "commands.json":
            global_file = PATHS.GLOBAL_COMMANDS_FILE
        elif data_file.name == "variables.json":
            global_file = PATHS.GLOBAL_VARS_FILE
        elif data_file.name == "checklists.json":
            global_file = PATHS.GLOBAL_CHECKLISTS_FILE

        # Si el archivo no existe o pesa 0 retorna la lista vacía
        if data_file.exists() and data_file.stat().st_size != 0:
            data.extend(_extract_data(data_file))

        if global_file and global_file.exists() and global_file.stat().st_size != 0:
            data.extend(_extract_data(global_file))

        return [cls(**item) for item in data]


    # Recibe el dato viejo y el dato nuevo
    # La idea por ahora que no hay TUI es sacarlo de ahí, mediante selección
    # se busca en la lista completa y se lo modifica
    @classmethod
    def modify(cls, old_model, new_model) -> None:
        project_file: Path = cls.file_path
        data = cls.read_all()

        for model in data:
            if model == old_model:
                index = data.index(model)
                data[index] = new_model
                break

        
        _save(project_file, data)

    # Recibe el model para agregar y lo guarda en el json
    @classmethod
    def add(cls, command):
        project_command_file : Path = cls.file_path

        data = cls.read_all()
        data.append(command)

        _save(project_command_file, data)

    # Recibe el modelo completo a borrar y lo elimina.  
    @classmethod
    def remove(cls, model_to_remove) -> None:
        project_file: Path = cls.file_path
        data = cls.read_all()

        if model_to_remove in data:
            data.remove(model_to_remove)

        _save(project_file, data)

        
        