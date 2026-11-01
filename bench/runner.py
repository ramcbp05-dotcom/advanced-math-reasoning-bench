"""Run every problem's verification script and collect the outcomes."""

from __future__ import annotations

import dataclasses
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from .models import ProblemSpec

PACKAGE_ROOT = Path(__file__).resolve().parent
IMPORT_ROOT = PACKAGE_ROOT.parent
REPO_ROOT = IMPORT_ROOT if (IMPORT_ROOT / "problems").is_dir() else PACKAGE_ROOT / "_data"


@dataclasses.dataclass
class VerifyResult:
    problem_id: str
    area: str
    passed: bool
    returncode: int
    duration_sec: float
    n_checks: int
    n_failed: int
    output: str

    def as_dict(self) -> dict:
        data = dataclasses.asdict(self)
        data.pop("output")
        return data


def _parse_counts(text: str) -> tuple[int, int]:
    import re
    match = re.search(r"(\d+)/(\d+) checks passed", text)
    if not match:
        return 0, 0
    passed, total = int(match.group(1)), int(match.group(2))
    return total, total - passed


def verify(spec: ProblemSpec, timeout: int = 300) -> VerifyResult:
    """Execute one ``verify.py`` as a subprocess and record what it reported."""
    started = time.perf_counter()
    env = {**_clean_env(), "PYTHONPATH": str(IMPORT_ROOT)}
    proc = subprocess.run(
        [sys.executable, str(spec.verify_path)],
        cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=timeout, env=env,
    )
    output = proc.stdout + proc.stderr
    n_checks, n_failed = _parse_counts(output)
    return VerifyResult(
        problem_id=spec.problem_id, area=spec.area,
        passed=proc.returncode == 0, returncode=proc.returncode,
        duration_sec=round(time.perf_counter() - started, 2),
        n_checks=n_checks, n_failed=n_failed, output=output,
    )


def _clean_env() -> dict:
    import os
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.pop("PYTHONPATH", None)
    return env


def summarise(results: list[VerifyResult]) -> dict:
    by_area: dict[str, dict] = {}
    for r in results:
        bucket = by_area.setdefault(r.area, {"problems": 0, "checks": 0, "failed": 0})
        bucket["problems"] += 1
        bucket["checks"] += r.n_checks
        bucket["failed"] += r.n_failed
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "n_problems": len(results),
        "n_passed": sum(r.passed for r in results),
        "total_checks": sum(r.n_checks for r in results),
        "total_failed": sum(r.n_failed for r in results),
        "by_area": by_area,
        "failures": [r.problem_id for r in results if not r.passed],
        "results": [r.as_dict() for r in results],
    }


def write_report(summary: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2) + "\n")
