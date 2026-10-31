#!/usr/bin/env python3
"""Verification for `cond2-is-singular-value-ratio`.

The universal claim kappa_2 = sigma_1/sigma_n is proved in solution.md; the
sampling below can only fail to contradict it. The two counterexamples are
different: they settle *existential* claims, and they are checked symbolically
with exact rationals, so those two checks do constitute proof of what they
assert.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from bench.verify_support import (check, random_matrix, relative_error,  # noqa: E402
                                  report, run_checks, symbolically_zero)

PROBLEM = "cond2-is-singular-value-ratio"


def identity_on_random_matrices():
    """kappa_2(A) == sigma_1/sigma_n, sampled. Evidence, not proof."""
    rng = np.random.default_rng(20260501)
    worst = 0.0
    for n in (2, 3, 5, 8, 13):
        for _ in range(40):
            a = random_matrix(rng, n)
            if abs(np.linalg.det(a)) < 1e-10:
                continue
            svd = np.linalg.svd(a, compute_uv=False)
            worst = max(worst, relative_error(np.linalg.cond(a, 2),
                                              svd[0] / svd[-1]))
    return check("kappa_2 = sigma_1/sigma_n over 200 random matrices",
                 worst < 1e-10, "illustration",
                 f"worst relative deviation {worst:.3e} (n = 2, 3, 5, 8, 13)")


def norm_is_top_singular_value():
    rng = np.random.default_rng(7)
    worst = 0.0
    for n in (2, 4, 9):
        for _ in range(30):
            a = random_matrix(rng, n)
            worst = max(worst, relative_error(
                np.linalg.norm(a, 2), np.linalg.svd(a, compute_uv=False)[0]))
    return check("||A||_2 = sigma_1 (Step 1)", worst < 1e-12, "illustration",
                 f"worst relative deviation {worst:.3e}")


def equality_case_is_exactly_the_unitary_multiples():
    rng = np.random.default_rng(11)
    worst_unitary = 0.0
    for n in (2, 3, 6):
        q, _ = np.linalg.qr(rng.normal(size=(n, n)))
        for c in (1.0, 3.7, 1e-6, 1e6):
            worst_unitary = max(worst_unitary,
                                abs(np.linalg.cond(c * q, 2) - 1.0))
    non_unitary_min = min(
        np.linalg.cond(random_matrix(rng, n), 2) for n in (2, 3, 6)
        for _ in range(20)
    )
    return check("kappa_2 = 1 iff scalar multiple of a unitary",
                 worst_unitary < 1e-12 and non_unitary_min > 1.0,
                 "illustration",
                 f"cQ gives |kappa - 1| <= {worst_unitary:.3e}; "
                 f"smallest kappa over 60 random matrices is {non_unitary_min:.4f}")


def scale_invariance():
    rng = np.random.default_rng(3)
    worst = 0.0
    for n in (2, 4, 7):
        a = random_matrix(rng, n)
        base = np.linalg.cond(a, 2)
        for c in (1e-8, 1e-3, 2.5, 1e4, 1e9):
            worst = max(worst, relative_error(np.linalg.cond(c * a, 2), base))
    return check("kappa_2(cA) = kappa_2(A) (Corollary 2)", worst < 1e-10,
                 "illustration",
                 f"worst relative deviation over c in [1e-8, 1e9]: {worst:.3e}")


def witness_a_large_determinant_ill_conditioned():
    """Exact: diag(1e5, 1e-5) has det 1 and kappa 1e10."""
    a = sp.Matrix([[sp.Integer(10) ** 5, 0], [0, sp.Rational(1, 10 ** 5)]])
    det = a.det()
    sigma = sorted(a.singular_values())
    kappa = sp.simplify(sigma[-1] / sigma[0])
    ok = det == 1 and kappa == sp.Integer(10) ** 10
    return check("witness (a): det = 1 exactly, kappa_2 = 1e10 exactly",
                 ok, "witness",
                 f"det = {det}, singular values = {[str(s) for s in sigma]}, "
                 f"kappa_2 = {kappa}")


def witness_b_small_determinant_well_conditioned():
    """Exact: 1e-5 * I_2 has det 1e-10 and kappa exactly 1."""
    b = sp.Rational(1, 10 ** 5) * sp.eye(2)
    det = sp.simplify(b.det())
    sigma = sorted(b.singular_values())
    kappa = sp.simplify(sigma[-1] / sigma[0])
    ok = det == sp.Rational(1, 10 ** 10) and kappa == 1
    return check("witness (b): det = 1e-10 exactly, kappa_2 = 1 exactly",
                 ok, "witness",
                 f"det = {det}, singular values = {[str(s) for s in sigma]}, "
                 f"kappa_2 = {kappa}")


def determinant_is_not_scale_invariant():
    """The structural reason, symbolically: det scales, the ratio does not.

    Written with the ordering sigma_1 >= sigma_n fixed by construction, so no
    Max/Min survives into the expression and the cancellation is visible.
    """
    c = sp.Symbol("c", positive=True)
    results = []
    for n in (2, 3, 4):
        entries = sp.symbols(f"a0:{n * n}", real=True)
        a = sp.Matrix(n, n, list(entries))
        det_ratio = sp.simplify(sp.expand((c * a).det()) / sp.expand(a.det()))
        results.append(symbolically_zero(det_ratio - c ** n))

    # kappa under scaling: every singular value scales by c, so the ratio of the
    # extremes cancels identically.
    s_top, s_bot = sp.symbols("sigma_1 sigma_n", positive=True)
    kappa_ratio = sp.simplify(((c * s_top) / (c * s_bot)) / (s_top / s_bot))

    return check("det(cA) = c^n det(A) (scale dependent) while kappa cancels",
                 all(results) and kappa_ratio == 1, "sympy-identity",
                 f"det(cA)/det(A) = c^n verified symbolically for n = 2, 3, 4; "
                 f"kappa(cA)/kappa(A) = {kappa_ratio}")


def frobenius_differs_from_two_norm():
    """The lemma the `frobenius-substitution` solution assumes."""
    worst_ratio = 0.0
    for n in (2, 3, 5, 10):
        eye = np.eye(n)
        worst_ratio = max(worst_ratio,
                          np.linalg.norm(eye, "fro") ** 2 / np.linalg.cond(eye, 2))
    return check("||I_n||_F ||I_n^{-1}||_F = n while kappa_2(I_n) = 1",
                 abs(worst_ratio - 10.0) < 1e-12, "illustration",
                 f"at n = 10 the Frobenius condition number is "
                 f"{np.linalg.norm(np.eye(10), 'fro') ** 2:.1f} against kappa_2 = 1")


CHECKS = [
    identity_on_random_matrices,
    norm_is_top_singular_value,
    equality_case_is_exactly_the_unitary_multiples,
    scale_invariance,
    witness_a_large_determinant_ill_conditioned,
    witness_b_small_determinant_well_conditioned,
    determinant_is_not_scale_invariant,
    frobenius_differs_from_two_norm,
]

if __name__ == "__main__":
    raise SystemExit(report(PROBLEM, run_checks(CHECKS)))
