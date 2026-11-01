"""Helpers for the per-problem ``verify.py`` scripts.

What these scripts are for
--------------------------
A verification script supplies **evidence at specific instances**: it evaluates
a bound at a few hundred random matrices, confirms a symbolic identity with
SymPy, or exhibits a concrete counterexample. That is useful and it is not a
proof.

The asymmetry matters and the harness encodes it:

* A **universal** claim ("for every matrix A, ...") cannot be established by
  computation over finitely many instances, however many. The argument in
  ``solution.md`` is what establishes it; the script only looks for a
  contradiction.
* An **existential** claim ("there exists an A for which the bound fails")
  *can* be settled by exhibiting one witness: provided the witness is checked
  exactly, which usually means symbolically rather than in floating point.

:class:`Check` therefore carries a ``role``, and :func:`report` prints the
disclaimer that goes with it. ``tests/test_problem_integrity.py`` requires
every script to use them.
"""

from __future__ import annotations

import dataclasses
from typing import Callable, Iterable

import numpy as np
import sympy as sp

__all__ = ["Check", "ROLES", "check", "report", "run_checks", "relative_error",
           "random_matrix", "DISCLAIMER", "symbolically_zero"]

ROLES = (
    "illustration",   # evidence at instances; the proof is in solution.md
    "witness",        # an exact counterexample, which does settle its claim
    "sympy-identity",  # a symbolic identity verified by CAS, not sampled
    "consistency",    # internal consistency of the repository's own numbers
)

DISCLAIMER = (
    "These checks are evidence at specific instances, not a proof.\n"
    "A universal claim is established by the argument in solution.md; the\n"
    "checks below can only fail to contradict it. The exception is a check\n"
    "marked 'witness': exhibiting one exact counterexample does settle an\n"
    "existential claim."
)


@dataclasses.dataclass
class Check:
    name: str
    role: str
    passed: bool
    detail: str = ""

    def __post_init__(self) -> None:
        if self.role not in ROLES:
            raise ValueError(f"role must be one of {ROLES}, got {self.role!r}")


def check(name: str, condition: bool, role: str = "illustration",
          detail: str = "") -> Check:
    """Build a :class:`Check`. ``detail`` should carry the measured numbers."""
    return Check(name=name, role=role, passed=bool(condition), detail=detail)


def relative_error(got: float, want: float, floor: float = 1e-300) -> float:
    return abs(got - want) / max(abs(want), floor)


def symbolically_zero(expression) -> bool:
    """Decide whether a SymPy expression is identically zero.

    ``sympy.simplify(e) == 0`` is **not** a reliable zero test and this
    repository was bitten by it: for

        e = (mu**2 - mu*t**2 - 2*mu + 1) - (mu**2 - (2 + t**2)*mu + 1)

    ``simplify`` returns the unevaluated
    ``-mu**2 + mu*t**2 + 2*mu + mu**2 - mu*t**2 - 2*mu``, which is structurally
    nonzero, so the comparison is False although the expression vanishes
    identically. ``expand`` settles it immediately.

    The general point is the one this benchmark is about: a CAS failing to show
    that something is zero is not evidence that it is nonzero. Three cheap
    routes are tried here, and a *negative* result from all three still means
    only "not established", never "disproved". To disprove an identity, find a
    substitution at which it fails. That is a witness and it does settle the
    question.
    """
    expr = sp.sympify(expression)

    if isinstance(expr, sp.MatrixBase):
        # A zero matrix is not equal to the integer 0, so each entry is tested.
        return all(symbolically_zero(entry) for entry in expr)

    if sp.expand(expr) == 0:
        return True
    if sp.simplify(expr) == 0:
        return True
    verdict = expr.equals(0)
    return bool(verdict) if verdict is not None else False


def random_matrix(rng, n: int, *, kind: str = "general") -> np.ndarray:
    """Random test matrix. ``kind`` is ``general``, ``symmetric`` or ``normal``."""
    a = rng.normal(size=(n, n))
    if kind == "general":
        return a
    if kind == "symmetric":
        return 0.5 * (a + a.T)
    if kind == "normal":
        # A real normal matrix: block-diagonal rotations are normal, and so is
        # Q D Q^T for orthogonal Q. Use the latter for a symmetric-spectrum case
        # and add a skew part scaled to keep normality: Q (D + S) Q^T is normal
        # iff D + S is, so take D diagonal and S skew-symmetric with [D, S] = 0,
        # which for distinct diagonal entries forces S = 0. Use a rotation block
        # construction instead.
        q, _ = np.linalg.qr(rng.normal(size=(n, n)))
        blocks = []
        k = 0
        while k + 1 < n:
            theta = rng.uniform(0, 2 * np.pi)
            r = rng.uniform(0.5, 2.0)
            blocks.append(r * np.array([[np.cos(theta), -np.sin(theta)],
                                        [np.sin(theta), np.cos(theta)]]))
            k += 2
        if k < n:
            blocks.append(np.array([[rng.uniform(0.5, 2.0)]]))
        from scipy.linalg import block_diag
        return q @ block_diag(*blocks) @ q.T
    raise ValueError(f"unknown kind {kind!r}")


def run_checks(builders: Iterable[Callable[[], Check]]) -> list[Check]:
    results = []
    for builder in builders:
        try:
            results.append(builder())
        except Exception as exc:  # noqa: BLE001 - a crashed check is a failed check
            results.append(Check(name=getattr(builder, "__name__", "<anonymous>"),
                                 role="illustration", passed=False,
                                 detail=f"{type(exc).__name__}: {exc}"))
    return results


def report(problem_id: str, checks: list[Check], *, quiet: bool = False) -> int:
    """Print the checks and return a process exit code."""
    width = max((len(c.name) for c in checks), default=10)
    lines = [f"== {problem_id} ==", "", DISCLAIMER, ""]
    for c in checks:
        status = "PASS" if c.passed else "FAIL"
        lines.append(f"[{status}] {c.name.ljust(width)}  ({c.role})")
        if c.detail:
            for piece in c.detail.splitlines():
                lines.append(f"         {piece}")
    n_failed = sum(not c.passed for c in checks)
    lines.append("")
    lines.append(f"{len(checks) - n_failed}/{len(checks)} checks passed")
    if not quiet:
        print("\n".join(lines))
    return 1 if n_failed else 0
