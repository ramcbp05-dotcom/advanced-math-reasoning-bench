#!/usr/bin/env python3
"""Verification for `hermitian-eigenvalues-are-perfectly-conditioned`."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from bench.verify_support import (check, random_matrix, report,  # noqa: E402
                                  run_checks, symbolically_zero)

PROBLEM = "hermitian-eigenvalues-are-perfectly-conditioned"


def _hermitian(rng, n, scale=1.0):
    a = rng.normal(size=(n, n))
    return scale * 0.5 * (a + a.T)


def weyl_bound_is_never_violated():
    rng = np.random.default_rng(20260601)
    worst = 0.0
    violations = 0
    for n in (2, 3, 6, 12, 25):
        for _ in range(40):
            a = _hermitian(rng, n)
            e = _hermitian(rng, n)
            e *= 1e-6 / np.linalg.norm(e, 2)
            shift = np.max(np.abs(np.sort(np.linalg.eigvalsh(a + e))
                                  - np.sort(np.linalg.eigvalsh(a))))
            ratio = shift / np.linalg.norm(e, 2)
            worst = max(worst, ratio)
            if ratio > 1.0 + 1e-9:
                violations += 1
    return check("|dlambda_k| <= ||E||_2 over 200 Hermitian pairs",
                 violations == 0, "illustration",
                 f"violations: {violations}; worst observed ratio "
                 f"|dlambda|/||E||_2 = {worst:.6f}")


def the_bound_is_attained():
    """A shift E = eps*I moves every eigenvalue by exactly eps."""
    rng = np.random.default_rng(3)
    worst_gap = 0.0
    for n in (2, 5, 9):
        a = _hermitian(rng, n)
        eps = 1e-3
        before = np.sort(np.linalg.eigvalsh(a))
        after = np.sort(np.linalg.eigvalsh(a + eps * np.eye(n)))
        worst_gap = max(worst_gap, np.max(np.abs((after - before) - eps)) / eps)
    return check("E = eps*I attains the bound exactly",
                 worst_gap < 1e-10, "witness",
                 f"every eigenvalue shifts by exactly eps; worst relative "
                 f"deviation {worst_gap:.3e}, so the constant 1 cannot be reduced")


def exact_two_by_two_attainment():
    """Symbolic: diag(1,0) perturbed by diag(eps,0)."""
    eps = sp.Symbol("epsilon", positive=True)
    a = sp.diag(1, 0)
    e = sp.diag(eps, 0)
    top_before = max(a.eigenvals(), key=lambda v: sp.re(v))
    top_after = max((a + e).eigenvals(), key=lambda v: sp.limit(sp.re(v), eps, 1))
    norm_e = eps  # ||diag(eps, 0)||_2 = eps for eps > 0
    return check("exact attainment for diag(1,0) + diag(eps,0)",
                 symbolically_zero((top_after - top_before) - norm_e),
                 "sympy-identity",
                 f"lambda_1 moves from {top_before} to {top_after}, "
                 f"a shift of exactly ||E||_2 = {norm_e}")


def hermiticity_is_needed_jordan_block():
    """The hypothesis is not decorative: a non-normal matrix breaks the bound."""
    rows = []
    ok = True
    for n in (2, 8, 16):
        eps = 1e-16
        j = np.diag(np.ones(n - 1), 1)
        j[-1, 0] = eps
        shift = float(np.max(np.abs(np.linalg.eigvals(j))))
        rows.append(f"n = {n:2d}: ||E||_2 = {eps:.0e} moves eigenvalues by "
                    f"{shift:.3e} (ratio {shift / eps:.1e})")
        ok = ok and shift > 1e6 * eps
    return check("a non-normal matrix violates the Weyl bound enormously",
                 ok, "witness", "\n".join(rows)
                 + "\nso any proof of Weyl that does not use Hermiticity is wrong")


def diagonalisable_is_not_enough():
    """The `diagonalisable-is-enough` claim, refuted with distinct eigenvalues."""
    rows = []
    ok = True
    for t in (1e2, 1e4, 1e6):
        a = np.array([[1.0, t], [0.0, 2.0]])
        _, v = np.linalg.eig(a)
        v = v / np.linalg.norm(v, axis=0)       # unit columns, as the flaw proposes
        e = 1e-10 * np.array([[0.0, 0.0], [1.0, 0.0]])
        before = np.sort(np.linalg.eigvals(a).real)
        after = np.sort(np.linalg.eigvals(a + e).real)
        shift = float(np.max(np.abs(after - before)))
        rows.append(f"t = {t:.0e}: kappa_2(V) = {np.linalg.cond(v, 2):.3e}, "
                    f"||E||_2 = 1e-10, shift = {shift:.3e} "
                    f"(amplification {shift / 1e-10:.1e})")
        ok = ok and shift >= 50 * 1e-10
    return check("diagonalisable with unit eigenvectors still amplifies",
                 ok, "witness", "\n".join(rows)
                 + "\nnormalising the columns of V does not bound ||V^{-1}||")


def normality_is_the_right_hypothesis():
    """kappa_2(V) = 1 exactly for normal A, and that is what gives constant 1."""
    rng = np.random.default_rng(11)
    rows = []
    ok = True
    for kind in ("symmetric", "normal", "general"):
        a = random_matrix(rng, 6, kind=kind)
        _, v = np.linalg.eig(a)
        kv = np.linalg.cond(v, 2)
        rows.append(f"{kind:10s}: kappa_2(V) = {kv:.4f}")
        if kind in ("symmetric", "normal"):
            ok = ok and kv < 1.0 + 1e-6
    return check("kappa_2(V) = 1 for normal A, > 1 in general",
                 ok, "illustration", "\n".join(rows))


def absolute_not_relative():
    """Part 3: the bound is absolute, so a small eigenvalue loses relative digits.

    ||E||_2 is taken as 1e-10 rather than 1e-16 deliberately. At 1e-16 the
    perturbation is the same size as the eigensolver's own backward error
    (u ||A||_2), so the measured shifts would be the solver's noise rather than
    the response to E, and the ratio would exceed 1 without that meaning
    anything. Measuring a response requires a signal above the noise floor of
    the instrument, which here is LAPACK.
    """
    n = 6
    rng = np.random.default_rng(7)
    q, _ = np.linalg.qr(rng.normal(size=(n, n)))
    spectrum = np.array([1.0, 0.5, 0.1, 1e-4, 1e-9, 1e-14])
    a = (q * spectrum) @ q.T

    e = _hermitian(rng, n)
    norm_e = 1e-10
    e *= norm_e / np.linalg.norm(e, 2)

    before = np.sort(np.linalg.eigvalsh(a))
    after = np.sort(np.linalg.eigvalsh(a + e))
    absolute = np.abs(after - before)
    relative = absolute / np.maximum(np.abs(before), 1e-300)

    rows = [f"lambda = {b:>10.3e}: absolute shift {ab:.3e}, relative {rel:.3e}"
            for b, ab, rel in zip(before, absolute, relative)]

    weyl_respected = np.max(absolute) <= norm_e * 1.01
    relative_blows_up = np.max(relative) > 1.0
    return check("the Weyl bound is absolute; small eigenvalues lose relative digits",
                 weyl_respected and relative_blows_up, "illustration",
                 "\n".join(rows)
                 + f"\n||E||_2 = {norm_e:.0e}; every absolute shift respects it "
                   f"(max {np.max(absolute):.3e}), while the smallest eigenvalue's "
                   f"relative error reaches {np.max(relative):.3e}")


def singular_values_obey_weyl_for_every_matrix():
    """The contrast worth knowing: singular values need no hypothesis."""
    rng = np.random.default_rng(20260602)
    worst = 0.0
    for n in (3, 7, 15):
        for _ in range(30):
            a = rng.normal(size=(n, n))          # no symmetry at all
            e = rng.normal(size=(n, n))
            e *= 1e-6 / np.linalg.norm(e, 2)
            shift = np.max(np.abs(np.linalg.svd(a + e, compute_uv=False)
                                  - np.linalg.svd(a, compute_uv=False)))
            worst = max(worst, shift / np.linalg.norm(e, 2))
    return check("singular values satisfy the same bound for ANY matrix",
                 worst <= 1.0 + 1e-9, "illustration",
                 f"worst ratio over 90 general matrices: {worst:.6f}; this is why "
                 "SVD-based algorithms are robust where eigenvalue-based ones are not")


CHECKS = [
    weyl_bound_is_never_violated,
    the_bound_is_attained,
    exact_two_by_two_attainment,
    hermiticity_is_needed_jordan_block,
    diagonalisable_is_not_enough,
    normality_is_the_right_hypothesis,
    absolute_not_relative,
    singular_values_obey_weyl_for_every_matrix,
]

if __name__ == "__main__":
    raise SystemExit(report(PROBLEM, run_checks(CHECKS)))
