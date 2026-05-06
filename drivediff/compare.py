from typing import Any, Dict, List

from .schema import RunData, ScenarioRecord


def _to_map(run: RunData) -> Dict[str, ScenarioRecord]:
    return {scenario.scenario_id: scenario for scenario in run.scenarios}


def compare_runs(run_a: RunData, run_b: RunData) -> Dict[str, Any]:
    a_map = _to_map(run_a)
    b_map = _to_map(run_b)

    common_ids = sorted(set(a_map.keys()) & set(b_map.keys()))
    only_a = sorted(set(a_map.keys()) - set(b_map.keys()))
    only_b = sorted(set(b_map.keys()) - set(a_map.keys()))

    regressed: List[Dict[str, Any]] = []
    improved: List[Dict[str, Any]] = []
    unchanged: List[str] = []

    for scenario_id in common_ids:
        sa = a_map[scenario_id]
        sb = b_map[scenario_id]

        if sa.passed and not sb.passed:
            regressed.append({"scenario_id": scenario_id, "reason": "pass_to_fail"})
        elif not sa.passed and sb.passed:
            improved.append({"scenario_id": scenario_id, "reason": "fail_to_pass"})
        else:
            unchanged.append(scenario_id)

    return {
        "run_a": run_a.run_id,
        "run_b": run_b.run_id,
        "counts": {
            "common": len(common_ids),
            "only_in_a": len(only_a),
            "only_in_b": len(only_b),
            "regressed": len(regressed),
            "improved": len(improved),
            "unchanged": len(unchanged),
        },
        "regressed": regressed,
        "improved": improved,
        "only_in_a": only_a,
        "only_in_b": only_b,
    }
