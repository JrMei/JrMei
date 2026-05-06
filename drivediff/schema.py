from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class ScenarioRecord:
    scenario_id: str
    passed: bool
    metrics: Dict[str, float]
    tags: List[str]


@dataclass
class RunData:
    run_id: str
    timestamp: str
    scenarios: List[ScenarioRecord]
    meta: Dict[str, Any]
