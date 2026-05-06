import argparse
import json
from pathlib import Path

from .compare import compare_runs
from .io import load_run


def cmd_compare(args: argparse.Namespace) -> int:
    baseline = load_run(args.run_a)
    candidate = load_run(args.run_b)
    result = compare_runs(baseline, candidate)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "summary.json"
    out_file.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=== DriveScenarioDiff Summary ===")
    print(f"run_a: {result['run_a']}")
    print(f"run_b: {result['run_b']}")
    for key, value in result["counts"].items():
        print(f"{key}: {value}")
    print(f"saved: {out_file}")

    if args.fail_on_regression and result["counts"]["regressed"] > 0:
        return 2
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="drivediff", description="DriveScenarioDiff CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    compare_parser = subparsers.add_parser("compare", help="Compare two run JSON files")
    compare_parser.add_argument("run_a", help="Path to baseline run JSON")
    compare_parser.add_argument("run_b", help="Path to candidate run JSON")
    compare_parser.add_argument("-o", "--output-dir", default="outputs", help="Output directory")
    compare_parser.add_argument("--fail-on-regression", action="store_true", help="Exit with code 2 if regressions found")
    compare_parser.set_defaults(func=cmd_compare)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
