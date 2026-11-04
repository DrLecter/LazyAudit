from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

class ScopeData:
    GLOBAL = "global"
    PRIVATE = "private"

class StatusData:
    ACTIVE = "active"
    PAUSED = "paused"
    FINISHED = "finished"

class SeverityData:
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class CommandData:
    title : str
    command : str
    description : str
    tags : list[str] = field(default_factory=list)
    scope : ScopeData = ScopeData.PRIVATE

@dataclass
class VariableData:
    key : str
    value : str
    description : str = ""
    scope : ScopeData = ScopeData.PRIVATE

@dataclass
class ProjectData:
    name : str
    description : str = ""
    status : StatusData = StatusData.ACTIVE
    created : str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class FindingData: 
    host : str
    description : str
    vulns : list[str] = field(default_factory=list)
    severity : SeverityData = SeverityData.LOW

@dataclass
class HostData: 
    ip : str
    hostname : str
    ports : list[str] = field(default_factory=list)
    services : list[str] = field(default_factory=list)

@dataclass
class ChecklistData:
    group : str
    task : str 
    done : bool = False
    scope : ScopeData = ScopeData.PRIVATE

@dataclass
class WorkflowData:
    name : str
    path : Path # Ruta completa al script
    scope : ScopeData = ScopeData.PRIVATE