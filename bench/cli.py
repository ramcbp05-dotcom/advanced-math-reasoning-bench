"""``mathbench``: list, read and verify the benchmark problems."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import models, runner

PROBLEMS_DIR = runner.REPO_ROOT / "problems"


def _load(selected: list[str] | None, area: str | None) -> list[models.ProblemSpec]:
    specs = models.discover(PROBLEMS_DIR)
    if area:
        specs = [s for s in specs if s.area == area]
    if not selected:
        return specs
    by_id = {s.problem_id: s for s in specs}
    missing = [p for p in selected if p not in by_id]
    if missing:
        raise SystemExit(f"unknown problem id(s): {missing}\navailable: {sorted(by_id)}")
    return [by_id[p] for p in selected]


def cmd_list(args: argparse.Namespace) -> int:
    specs = _load(None, args.area)
    width = max(len(s.problem_id) for s in specs)
    print(f"{'PROBLEM'.ljust(width)}  AREA                    CLAIM        DIFFICULTY         FLAWED")
    current = None
    for spec in specs:
        if spec.area != current:
            current = spec.area
            print()
        print(f"{spec.problem_id.ljust(width)}  {spec.area:<22}  {spec.claim_type:<11}  "
              f"{spec.difficulty:<17}  {len(spec.flawed)}")
    print(f"\n{len(specs)} problems "
          + " / ".join(f"{sum(s.area == a for s in specs)} {a}" for a in models.AREAS))
    print(f"{sum(len(s.flawed) for s in specs)} recorded flawed solutions")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    for spec in _load(args.problem, None):
        print("=" * 78)
        print(f"{spec.problem_id}  [{spec.area} / {spec.difficulty} / {spec.claim_type}]")
        print("=" * 78)
        print(spec.statement_path.read_text())
        if args.solution:
            print("-" * 78)
            print(spec.solution_path.read_text())
        if args.flawed:
            for flaw in spec.flawed:
                print("-" * 78)
                print(spec.flawed_path(flaw.name).read_text())
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    specs = _load(args.problem, args.area)
    results = []
    for spec in specs:
        result = runner.verify(spec)
        flag = "OK " if result.passed else "BAD"
        print(f"[{flag}] {spec.problem_id:<42} {result.n_checks - result.n_failed}"
              f"/{result.n_checks} checks  {result.duration_sec:>5.2f}s")
        if not result.passed and args.verbose:
            print(result.output)
        results.append(result)

    summary = runner.summarise(results)
    print(f"\n{summary['n_passed']}/{summary['n_problems']} problems verified, "
          f"{summary['total_checks'] - summary['total_failed']}/"
          f"{summary['total_checks']} checks passed")
    for area, bucket in sorted(summary["by_area"].items()):
        print(f"  {area:<24} {bucket['problems']:>2} problems, "
              f"{bucket['checks'] - bucket['failed']:>3}/{bucket['checks']:>3} checks")
    if summary["failures"]:
        print(f"  FAILED: {summary['failures']}")
    if args.report:
        runner.write_report(summary, Path(args.report))
        print(f"report written to {args.report}")
    return 0 if not summary["failures"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mathbench", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="list every problem")
    p_list.add_argument("-a", "--area", choices=models.AREAS)
    p_list.set_defaults(func=cmd_list)

    p_show = sub.add_parser("show", help="print a problem statement")
    p_show.add_argument("problem", nargs="+")
    p_show.add_argument("--solution", action="store_true", help="include the proof")
    p_show.add_argument("--flawed", action="store_true",
                        help="include the recorded wrong solutions")
    p_show.set_defaults(func=cmd_show)

    p_verify = sub.add_parser("verify", help="run the verification scripts")
    p_verify.add_argument("-p", "--problem", action="append")
    p_verify.add_argument("-a", "--area", choices=models.AREAS)
    p_verify.add_argument("-v", "--verbose", action="store_true")
    p_verify.add_argument("--report", default=None)
    p_verify.set_defaults(func=cmd_verify)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
