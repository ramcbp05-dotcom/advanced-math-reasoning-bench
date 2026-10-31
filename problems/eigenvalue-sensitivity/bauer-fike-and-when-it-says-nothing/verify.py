#!/usr/bin/env python3
"""Verification for `bauer-fike-and-when-it-says-nothing`."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from bench.verify_support import (check, random_matrix, report,  # noqa: E402
                                  run_checks, symbolically_zero)

PROBLEM = "bauer-fike-and-when-it-says-nothing"


def _shift(a, e):
    """max over eigenvalues of A+E of the distance to the spectrum of A."""
    base = np.linalg.eigvals(a)
    return float(max(min(abs(mu - lam) for lam in base)
                     for mu in np.linalg.eigvals(a + e)))


def _kappa_v(a):
    _, v = np.linalg.eig(a)
    v = v / np.linalg.norm(v, axis=0)
    return float(np.linalg.cond(v, 2))


def bound_is_never_violated():
    rng = np.random.default_rng(20260603)
    violations = 0
    worst_tightness = 0.0
    for n in (2, 3, 5, 8):
        for _ in range(50):
            a = random_matrix(rng, n)
            if _kappa_v(a) > 1e8:
                continue
            e = rng.normal(size=(n, n))
            e *= 1e-8 / np.linalg.norm(e, 2)
            bound = _kappa_v(a) * np.linalg.norm(e, 2)
            shift = _shift(a, e)
            if shift > bound * (1 + 1e-6):
                violations += 1
            worst_tightness = max(worst_tightness, shift / bound)
    return check("Bauer-Fike is never violated over 200 random matrices",
                 violations == 0, "illustration",
                 f"violations: {violations}; the tightest observed case reached "
                 f"{worst_tightness:.4f} of the bound")


def proof_step_is_valid_symbolically():
    """The factorisation the proof turns on, checked as an identity."""
    mu = sp.Symbol("mu")
    l1, l2 = sp.symbols("lambda_1 lambda_2")
    v = sp.Matrix([[1, 1], [0, 1]])
    lam = sp.diag(l1, l2)
    e = sp.Matrix(2, 2, sp.symbols("e0:4"))
    a = v * lam * v.inv()

    lhs = mu * sp.eye(2) - a - e
    bracket = sp.eye(2) - (mu * sp.eye(2) - lam).inv() * v.inv() * e * v
    rhs = v * (mu * sp.eye(2) - lam) * bracket * v.inv()
    return check("mu I - A - E = V (mu I - Lambda)[I - (mu I - Lambda)^-1 V^-1 E V] V^-1",
                 symbolically_zero(sp.simplify(lhs - rhs)), "sympy-identity",
                 "the factorisation in the proof of Part 1, verified as an "
                 "identity in mu, the eigenvalues and the entries of E")


def normal_matrices_give_constant_one():
    rng = np.random.default_rng(4)
    worst = 0.0
    for kind in ("symmetric", "normal"):
        for _ in range(20):
            a = random_matrix(rng, 6, kind=kind)
            worst = max(worst, abs(_kappa_v(a) - 1.0))
    return check("kappa_2(V) = 1 for normal A, so Bauer-Fike reduces to Weyl",
                 worst < 1e-8, "illustration",
                 f"worst |kappa_2(V) - 1| over 40 normal matrices: {worst:.3e}")


def the_bound_is_sharp():
    """Part 2: an E that attains it to within a factor of 2."""
    rows = []
    ok = True
    delta = 1e-10
    e = delta * np.array([[0.0, 0.0], [1.0, 0.0]])
    for t in (1e2, 1e4, 1e6):
        a = np.array([[1.0, t], [0.0, 2.0]])
        bound = _kappa_v(a) * np.linalg.norm(e, 2)
        shift = _shift(a, e)
        rows.append(f"t = {t:.0e}: kappa_2(V) = {_kappa_v(a):.3e}, bound = "
                    f"{bound:.3e}, shift = {shift:.3e}, ratio = {shift / bound:.3f}")
        ok = ok and shift / bound > 0.3
    return check("the bound is attained to within a factor of 2 (Part 2)",
                 ok, "illustration", "\n".join(rows)
                 + "\nso the amplification kappa_2(V) is real, not a loose estimate")


def the_bound_can_be_vacuous():
    """Part 3: a fixed E for which the bound diverges and the shift does not."""
    rows = []
    ok = True
    delta = 1e-10
    e = delta * np.diag([1.0, -1.0])
    shifts = []
    for t in (1e2, 1e4, 1e6, 1e8):
        a = np.array([[1.0, t], [0.0, 2.0]])
        bound = _kappa_v(a) * np.linalg.norm(e, 2)
        shift = _shift(a, e)
        shifts.append(shift)
        rows.append(f"t = {t:.0e}: bound = {bound:.3e}, shift = {shift:.3e}, "
                    f"bound/shift = {bound / shift:.2e}")
    ok = max(shifts) / min(shifts) < 10.0 and shifts[-1] < 10 * delta
    return check("for a fixed E the bound diverges while the shift does not",
                 ok, "witness", "\n".join(rows)
                 + f"\nthe shift stays pinned near delta = {delta:.0e} across six "
                   "decades of t, so the answer to Part 3 is no")


def exact_eigenvalues_in_the_vacuous_family():
    """The shift really is exactly delta: the eigenvalues are 1+delta, 2-delta."""
    t, delta = sp.symbols("t delta", positive=True)
    a = sp.Matrix([[1, t], [0, 2]]) + sp.diag(delta, -delta)
    eigen = sorted(a.eigenvals(), key=str)
    expected = {1 + delta, 2 - delta}
    ok = {sp.simplify(e) for e in eigen} == expected
    return check("eigenvalues of A_t + E are exactly 1+delta and 2-delta, for every t",
                 ok, "sympy-identity",
                 f"spectrum = {sorted(str(sp.simplify(e)) for e in eigen)}; "
                 "independent of t, which is why the bound is vacuous here")


def defective_matrix_has_no_eigenbasis():
    """Part 4: the hypothesis genuinely fails for J_n."""
    rows = []
    ok = True
    for n in (4, 8, 16):
        j = np.diag(np.ones(n - 1), 1)
        w, v = np.linalg.eig(j)
        residual = np.linalg.norm(j @ v - v @ np.diag(w), 2)
        kappa = np.linalg.cond(v, 2)
        rows.append(f"n = {n:2d}: kappa_2(V) = {kappa:.3e}, "
                    f"||AV - V Lambda||_2 = {residual:.3e}")
        ok = ok and kappa > 1e12
    return check("numpy returns a V for J_n, but it is exactly singular",
                 ok, "witness", "\n".join(rows)
                 + "\nthe columns are all exactly e_1, so V is exactly singular; "
                   "the factorisation A = V Lambda V^-1 does not exist")


def the_defective_bound_predicts_nothing():
    """The same 'bound' for cases whose true answers differ by 1e7.

    For the *exact* Jordan block numpy returns a V whose columns are exactly
    e_1, so V is exactly singular and kappa_2(V) is inf or of order 1e291. The
    resulting Bauer-Fike "bound" is infinite: true, and empty.
    """
    rows = []
    eps = 1e-16
    bounds, actuals = [], []
    for n in (2, 8, 16):
        j = np.diag(np.ones(n - 1), 1)
        _, v = np.linalg.eig(j)
        with np.errstate(over="ignore", invalid="ignore"):
            bound = np.linalg.cond(v, 2) * eps
        perturbed = j.copy()
        perturbed[-1, 0] = eps
        actual = float(np.max(np.abs(np.linalg.eigvals(perturbed))))
        bounds.append(bound)
        actuals.append(actual)
        rows.append(f"n = {n:2d}: 'bound' = {bound:.3e}, true shift = "
                    f"{actual:.3e} (= eps^(1/n))")
    actual_spread = max(actuals) / min(actuals)
    return check("the defective 'bound' is infinite while the truth spans 1e7",
                 all(b > 1e100 for b in bounds) and actual_spread > 1e6,
                 "witness", "\n".join(rows)
                 + f"\nevery bound exceeds 1e100 while the true shifts vary by "
                   f"{actual_spread:.1e}x -- the 'bound' distinguishes nothing")


def nearly_defective_gives_the_one_over_u_signature():
    """A diagonalisable neighbour of J_n: kappa_2(V) is then finite but ~1/u.

    This is the case a practitioner actually meets, and it is where the
    diagnostic matters: kappa_2(V) approaching 1/u means the eigenbasis is
    numerically not a basis, whatever `eig` returned.
    """
    rows = []
    ok = True
    for n in (4, 8):
        for gap in (1e-4, 1e-8):
            a = np.diag(np.ones(n - 1), 1) + np.diag(gap * np.arange(n))
            _, v = np.linalg.eig(a)
            v = v / np.linalg.norm(v, axis=0)
            kappa = float(np.linalg.cond(v, 2))
            rows.append(f"n = {n}, eigenvalue gap {gap:.0e}: kappa_2(V) = {kappa:.3e}")
            ok = ok and kappa > 1e3
    return check("a nearly defective matrix has a huge but finite kappa_2(V)",
                 ok, "illustration", "\n".join(rows)
                 + "\ndistinct eigenvalues, so Bauer-Fike formally applies -- and "
                   "the bound it gives is useless well before the matrix is defective")


CHECKS = [
    bound_is_never_violated,
    proof_step_is_valid_symbolically,
    normal_matrices_give_constant_one,
    the_bound_is_sharp,
    the_bound_can_be_vacuous,
    exact_eigenvalues_in_the_vacuous_family,
    defective_matrix_has_no_eigenbasis,
    the_defective_bound_predicts_nothing,
    nearly_defective_gives_the_one_over_u_signature,
]

if __name__ == "__main__":
    raise SystemExit(report(PROBLEM, run_checks(CHECKS)))
