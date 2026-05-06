from drivediff.compare import compare_runs
from drivediff.io import load_run


def test_compare_counts():
    run_a = load_run("examples/runA_sample.json")
    run_b = load_run("examples/runB_sample.json")

    summary = compare_runs(run_a, run_b)

    assert summary["counts"]["common"] == 2
    assert summary["counts"]["only_in_a"] == 0
    assert summary["counts"]["only_in_b"] == 1
    assert summary["counts"]["regressed"] == 1
    assert summary["regressed"][0]["scenario_id"] == "scene_001"
