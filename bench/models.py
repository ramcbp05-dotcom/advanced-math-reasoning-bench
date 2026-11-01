"""Problem specification: the on-disk contract for one benchmark problem.

Layout of ``problems/<area>/<problem-id>/``::

    problem.yaml        metadata parsed into :class:`ProblemSpec`
    statement.md        assumptions and the claim, in LaTeX
    solution.md         the proof, plus counterexamples where they sharpen it
    flawed/*.md         plausible wrong solutions, each naming the broken step
    verify.py           numerical / symbolic evidence: NOT the proof
"""

from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Any

import yaml

AREAS = ("conditioning", "eigenvalue-sensitivity", "ode-stability")
DIFFICULTIES = ("undergraduate", "graduate", "research-adjacent")
CLAIM_TYPES = ("universal", "existential", "mixed")
PROOF_METHODS = ("analytic", "sympy-assisted", "analytic-with-witness")


class ProblemSpecError(ValueError):
    """Raised when a ``problem.yaml`` is malformed or the layout is incomplete."""


@dataclasses.dataclass(frozen=True)
class FlawedSolution:
    name: str
    summary: str
    breaks_at: str       # the step where the reasoning fails
    failure_mode: str    # a short classification


@dataclasses.dataclass(frozen=True)
class ProblemSpec:
    problem_id: str
    area: str
    title: str
    difficulty: str
    claim_type: str
    proof_method: str
    summary: str
    tags: tuple[str, ...]
    flawed: tuple[FlawedSolution, ...]
    root: Path

    @property
    def statement_path(self) -> Path:
        return self.root / "statement.md"

    @property
    def solution_path(self) -> Path:
        return self.root / "solution.md"

    @property
    def verify_path(self) -> Path:
        return self.root / "verify.py"

    @property
    def flawed_dir(self) -> Path:
        return self.root / "flawed"

    def flawed_path(self, name: str) -> Path:
        return self.flawed_dir / f"{name}.md"

    @classmethod
    def load(cls, root: Path) -> "ProblemSpec":
        root = Path(root)
        meta_path = root / "problem.yaml"
        if not meta_path.is_file():
            raise ProblemSpecError(f"{root}: missing problem.yaml")
        data: dict[str, Any] = yaml.safe_load(meta_path.read_text()) or {}

        required = ("id", "area", "title", "difficulty", "claim_type",
                    "proof_method", "summary", "flawed")
        missing = [k for k in required if k not in data]
        if missing:
            raise ProblemSpecError(f"{meta_path}: missing keys {missing}")
        if data["id"] != root.name:
            raise ProblemSpecError(f"{meta_path}: id {data['id']!r} != dir {root.name!r}")
        if data["area"] != root.parent.name:
            raise ProblemSpecError(
                f"{meta_path}: area {data['area']!r} != directory {root.parent.name!r}"
            )
        for key, allowed in (("area", AREAS), ("difficulty", DIFFICULTIES),
                             ("claim_type", CLAIM_TYPES),
                             ("proof_method", PROOF_METHODS)):
            if data[key] not in allowed:
                raise ProblemSpecError(
                    f"{meta_path}: {key}={data[key]!r} not in {allowed}"
                )

        flawed = []
        for entry in data["flawed"]:
            for key in ("name", "summary", "breaks_at", "failure_mode"):
                if key not in entry:
                    raise ProblemSpecError(
                        f"{meta_path}: flawed entry {entry.get('name')!r} missing {key!r}"
                    )
            flawed.append(FlawedSolution(**{k: entry[k] for k in
                                            ("name", "summary", "breaks_at",
                                             "failure_mode")}))
        if not flawed:
            raise ProblemSpecError(
                f"{meta_path}: no flawed solutions. A problem without a recorded "
                "wrong turn does not say where reasoning actually breaks."
            )

        spec = cls(
            problem_id=data["id"], area=data["area"], title=data["title"],
            difficulty=data["difficulty"], claim_type=data["claim_type"],
            proof_method=data["proof_method"], summary=data["summary"],
            tags=tuple(data.get("tags", ())), flawed=tuple(flawed), root=root,
        )
        spec.validate_layout()
        return spec

    def validate_layout(self) -> None:
        for path in (self.statement_path, self.solution_path, self.verify_path):
            if not path.is_file():
                raise ProblemSpecError(
                    f"{self.problem_id}: missing {path.relative_to(self.root)}"
                )
        for flaw in self.flawed:
            if not self.flawed_path(flaw.name).is_file():
                raise ProblemSpecError(
                    f"{self.problem_id}: missing flawed/{flaw.name}.md"
                )


def discover(problems_dir: Path) -> list[ProblemSpec]:
    """Load every problem under ``problems_dir``, sorted by area then id."""
    problems_dir = Path(problems_dir)
    specs = []
    for area_dir in sorted(problems_dir.iterdir()):
        if not area_dir.is_dir():
            continue
        for child in sorted(area_dir.iterdir()):
            if child.is_dir() and (child / "problem.yaml").is_file():
                specs.append(ProblemSpec.load(child))
    return specs
