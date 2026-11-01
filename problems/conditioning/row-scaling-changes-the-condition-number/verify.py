#!/usr/bin/env python3
"""Verification for `row-scaling-changes-the-condition-number`."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from bench.verify_support import (check, report, run_checks,  # noqa: E402
                                  symbolically_zero)

PROBLEM = "row-scaling-changes-the-condition-number"


def _skeel(m):
    return float(np.linalg.norm(np.abs(np.linalg.inv(m)) @ np.abs(m), np.inf))


def witness_scaling_moves_kappa_without_limit():
    a = np.array([[1.0, 1.0], [1.0, 1.0 + 1e-8]])
    rows = []
    kappas = []
    for t in (1.0, 1e2, 1e4, 1e8):
        k = np.linalg.cond(np.diag([1.0, t]) @ a, 2)
        kappas.append(k)
        rows.append(f"t = {t:.0e}: kappa_2 = {k:.4e}")
    return check("kappa_2(D_t A) grows without bound (Part 1 witness)",
                 kappas[-1] / kappas[0] > 1e7, "witness",
                 "\n".join(rows) + f"\nratio over the family: {kappas[-1] / kappas[0]:.2e}")


def scaled_systems_have_the_same_solution():
    """The mathematical problem really is unchanged. That is the point."""
    rng = np.random.default_rng(20260504)
    worst = 0.0
    for _ in range(20):
        a = rng.normal(size=(5, 5))
        b = rng.normal(size=5)
        d = np.diag(10 ** rng.uniform(-4, 4, 5))
        x1 = np.linalg.solve(a, b)
        x2 = np.linalg.solve(d @ a, d @ b)
        worst = max(worst, np.linalg.norm(x1 - x2) / np.linalg.norm(x1))
    return check("Ax = b and (DA)x = Db have the same solution",
                 worst < 1e-8, "illustration",
                 f"worst relative difference over 20 random systems: {worst:.3e}")


def exact_kappa_of_the_witness():
    """Exact rational arithmetic, so Part 1 is not a floating-point claim.

    The singular values of D_t A are the square roots of the eigenvalues of
    (D_t A)^T (D_t A), computed here over the rationals and only converted to a
    float for display.
    """
    delta = sp.Rational(1, 10 ** 8)
    rows = []
    kappas = []
    for t_exp in (0, 2, 4, 8):
        t = sp.Integer(10) ** t_exp
        a = sp.Matrix([[1, 1], [t, t * (1 + delta)]])
        gram = a.T * a
        eigen = sorted(sp.nsimplify(v) for v in gram.eigenvals())
        kappa_sq = sp.simplify(eigen[-1] / eigen[0])
        kappa = sp.sqrt(kappa_sq)
        kappas.append(float(kappa))
        rows.append(f"t = 1e{t_exp}: kappa_2 = {float(kappa):.6e} "
                    f"(exact, from rational eigenvalues of A^T A)")
    return check("exact kappa of the witness family", kappas[-1] > 1e15,
                 "witness",
                 "\n".join(rows)
                 + f"\ngrowth over the family: {kappas[-1] / kappas[0]:.3e}")


def equilibration_helps_a_lot():
    rng = np.random.default_rng(3)
    rows = []
    ok = True
    for _ in range(4):
        m = rng.normal(size=(6, 6)) * (10 ** rng.uniform(-5, 5, (6, 1)))
        before = np.linalg.cond(m, np.inf)
        scale = np.max(np.abs(m), axis=1)
        after = np.linalg.cond((m.T / scale).T, np.inf)
        rows.append(f"kappa_inf {before:.3e} -> {after:.3e} "
                    f"(factor {before / after:.2e})")
        ok = ok and after < before
    return check("row equilibration reduces kappa_inf (van der Sluis)",
                 ok, "illustration", "\n".join(rows))


def equilibration_is_not_optimal():
    """Search a coarse grid of diagonal scalings for something better.

    Finding *any* D that beats equilibration refutes the `equilibration-is-
    optimal` claim. The search is over a grid, so a failure to find one would
    prove nothing, but a success does.
    """
    rng = np.random.default_rng(20260505)
    best_gain = 1.0
    detail = ""
    for trial in range(40):
        m = rng.normal(size=(3, 3))
        scale = np.max(np.abs(m), axis=1)
        eq = np.linalg.cond((m.T / scale).T, np.inf)
        for _ in range(400):
            d = 10 ** rng.uniform(-1.5, 1.5, 3)
            cand = np.linalg.cond((m.T * (d / scale)).T, np.inf)
            if eq / cand > best_gain:
                best_gain = eq / cand
                detail = (f"equilibrated kappa_inf = {eq:.4f}, a grid-searched "
                          f"diagonal gives {cand:.4f} (better by {eq / cand:.3f}x)")
    return check("equilibration is not the minimiser", best_gain > 1.05, "witness",
                 detail or "no better scaling found in the search")


def skeel_is_invariant_under_row_scaling():
    base = np.array([[1.0, 2.0], [3.0, 4.0]])
    rows = []
    skeels = []
    for t in (1.0, 1e3, 1e6, 1e9):
        m = np.diag([1.0, t]) @ base
        s = _skeel(m)
        skeels.append(s)
        rows.append(f"t = {t:.0e}: kappa_inf = {np.linalg.cond(m, np.inf):.4e}, "
                    f"Skeel cond = {s:.6f}")
    spread = max(skeels) - min(skeels)
    return check("Skeel cond(DA) = cond(A) (Part 3)",
                 spread < 1e-10, "illustration",
                 "\n".join(rows) + f"\nspread across four decades of scaling: "
                                   f"{spread:.3e}")


def skeel_invariance_symbolically():
    """|D|^{-1}|D| = I is the whole proof; check it on a symbolic 3x3."""
    d1, d2, d3 = sp.symbols("d1 d2 d3", positive=True)
    entries = sp.symbols("a0:9", real=True)
    a = sp.Matrix(3, 3, list(entries))
    d = sp.diag(d1, d2, d3)
    lhs = sp.simplify((d * a).applyfunc(sp.Abs))
    rhs = sp.simplify(d.applyfunc(sp.Abs) * a.applyfunc(sp.Abs))
    return check("|DA| = |D||A| for diagonal D (the proof's one step)",
                 symbolically_zero(lhs - rhs), "sympy-identity",
                 "entrywise absolute value is multiplicative across a diagonal "
                 "factor, which is exactly why the Skeel number cancels it")


def skeel_bounds_componentwise_sensitivity():
    """The reason Part 3 matters: cond(A) governs relative entrywise errors."""
    rng = np.random.default_rng(99)
    worst_ratio = 0.0
    for _ in range(50):
        a = rng.normal(size=(4, 4))
        if np.linalg.cond(a) > 1e6:
            continue
        b = rng.normal(size=4)
        x = np.linalg.solve(a, b)
        eps = 1e-10
        pert = a * (1.0 + eps * rng.uniform(-1, 1, a.shape))
        x_pert = np.linalg.solve(pert, b)
        observed = np.linalg.norm(x_pert - x, np.inf) / np.linalg.norm(x, np.inf)
        predicted = eps * _skeel(a)
        if predicted > 0:
            worst_ratio = max(worst_ratio, observed / predicted)
    return check("observed componentwise sensitivity <= eps * Skeel cond",
                 worst_ratio <= 1.5, "illustration",
                 f"worst observed/predicted ratio over 50 systems: "
                 f"{worst_ratio:.4f} (the bound is first order, so a ratio "
                 "slightly above 1 would not be a contradiction)")


CHECKS = [
    witness_scaling_moves_kappa_without_limit,
    scaled_systems_have_the_same_solution,
    exact_kappa_of_the_witness,
    equilibration_helps_a_lot,
    equilibration_is_not_optimal,
    skeel_is_invariant_under_row_scaling,
    skeel_invariance_symbolically,
    skeel_bounds_componentwise_sensitivity,
]

if __name__ == "__main__":
    raise SystemExit(report(PROBLEM, run_checks(CHECKS)))
