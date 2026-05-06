import json
from pathlib import Path
from typing import Any, Dict, List

from .schema import RunData, ScenarioRecord


def _validate_scenario(obj: Dict[str, Any], idx: int) -> None:
    required = ["scenario_id", "passed", "metrics"]
    for key in required:
        if key not in obj:
            raise ValueError(f"scenario[{idx}] missing required field: {key}")

    if not isinstance(obj["scenario_id"], str) or not obj["scenario_id"].strip():
        raise ValueError(f"scenario[{idx}] scenario_id must be non-empty string")

    if not isinstance(obj["passed"], bool):
        raise ValueError(f"scenario[{idx}] passed must be bool")

    if not isinstance(obj["metrics"], dict) or len(obj["metrics"]) == 0:
        raise ValueError(f"scenario[{idx}] metrics must be non-empty object")

    for metric_name, metric_value in obj["metrics"].items():
        if not isinstance(metric_value, (int, float)):
            raise ValueError(
                f"scenario[{idx}] metric '{metric_name}' must be number"
            )


def load_run(path: str) -> RunData:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))

    for key in ["run_id", "timestamp", "scenarios"]:
        if key not in raw:
            raise ValueError(f"missing top-level field: {key}")

    if not isinstance(raw["scenarios"], list) or len(raw["scenarios"]) == 0:
        raise ValueError("scenarios must be a non-empty list")

    scenarios: List[ScenarioRecord] = []
    for i, item in enumerate(raw["scenarios"]):
        _validate_scenario(item, i)
        scenarios.append(
            ScenarioRecord(
                scenario_id=item["scenario_id"],
                passed=item["passed"],
                metrics={k: float(v) for k, v in item["metrics"].items()},
                tags=item.get("tags", []),
            )
        )

    return RunData(
        run_id=raw["run_id"],
        timestamp=raw["timestamp"],
        scenarios=scenarios,
        meta=raw.get("meta", {}),
    )
