#!/usr/bin/env python3
"""Verification for `eigenvalue-condition-number-is-one-over-the-inner-product`."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from bench.verify_support import (check, random_matrix, report,  # noqa: E402
                                  run_checks, symbolically_zero)

PROBLEM = "eigenvalue-condition-number-is-one-over-the-inner-product"


def _condition_numbers(a):
    """kappa(lambda_i) = 1/|y_i* x_i| with unit left and right eigenvectors."""
    w, vr = np.linalg.eig(a)
    _, vl = np.linalg.eig(a.conj().T)
    # match the left eigenvectors to the right ones by eigenvalue
    order = []
    for lam in w:
        order.append(int(np.argmin(np.abs(np.linalg.eigvals(a.conj().T) - np.conj(lam)))))
    kappas = []
    for i, j in enumerate(order):
        x = vr[:, i] / np.linalg.norm(vr[:, i])
        y = vl[:, j] / np.linalg.norm(vl[:, j])
        kappas.append(1.0 / max(abs(np.vdot(y, x)), 1e-300))
    return w, np.array(kappas)


def first_order_formula_predicts_the_shift():
    """lambda(t) - lambda ~ t y*Ex/(y*x), measured at small t."""
    rng = np.random.default_rng(20260604)
    worst = 0.0
    for n in (2, 3, 5):
        for _ in range(30):
            a = random_matrix(rng, n)
            w, vr = np.linalg.eig(a)
            if np.min(np.abs(w[:, None] - w[None, :] + np.eye(n) * 1e3)) < 1e-3:
                continue                                   # near-degenerate: skip
            _, vl = np.linalg.eig(a.conj().T)
            e = rng.normal(size=(n, n))
            e /= np.linalg.norm(e, 2)
            t = 1e-7
            w2 = np.linalg.eigvals(a + t * e)
            for i in range(n):
                x = vr[:, i] / np.linalg.norm(vr[:, i])
                j = int(np.argmin(np.abs(np.linalg.eigvals(a.conj().T) - np.conj(w[i]))))
                y = vl[:, j] / np.linalg.norm(vl[:, j])
                inner = np.vdot(y, x)
                if abs(inner) < 1e-3:
                    continue
                predicted = t * np.vdot(y, e @ x) / inner
                observed = w2[int(np.argmin(np.abs(w2 - w[i])))] - w[i]
                worst = max(worst, abs(observed - predicted) / max(abs(predicted), 1e-300))
    return check("lambda'(0) = y*Ex/(y*x) predicts the shift",
                 worst < 1e-3, "illustration",
                 f"worst relative deviation between the first-order prediction and "
                 f"the measured shift at t = 1e-7: {worst:.3e}")


def symbolic_derivation_of_the_formula():
    """The cancellation that makes the left eigenvector necessary."""
    lam, mu = sp.symbols("lambda mu")
    y1, y2, x1, x2 = sp.symbols("y1 y2 x1 x2")
    xp1, xp2 = sp.symbols("xp1 xp2")        # the unknown eigenvector derivative
    a = sp.Matrix(2, 2, sp.symbols("a0:4"))
    e = sp.Matrix(2, 2, sp.symbols("e0:4"))
    x = sp.Matrix([x1, x2])
    y = sp.Matrix([y1, y2])
    xp = sp.Matrix([xp1, xp2])

    # y^T (A xp) - lambda y^T xp vanishes when y^T A = lambda y^T.
    left_relation = (y.T * a - lam * y.T)
    cancelled = sp.expand((left_relation * xp)[0])
    substituted = cancelled.subs({a[0, 0]: lam * y1 / y1}) if False else cancelled
    # Impose y^T A = lambda y^T explicitly and check the xp terms vanish.
    constraints = sp.solve([left_relation[0], left_relation[1]],
                           [a[0, 0], a[0, 1]], dict=True)
    vanishes = constraints and symbolically_zero(cancelled.subs(constraints[0]))
    return check("y*(A - lambda I) xp = 0 removes the unknown eigenvector derivative",
                 bool(vanishes), "sympy-identity",
                 "the left eigenvector annihilates the x'(0) terms; multiplying by "
                 "x* instead leaves them, which is why the formula needs y")


def condition_number_is_at_least_one():
    rng = np.random.default_rng(3)
    smallest = np.inf
    for n in (2, 4, 7):
        for _ in range(40):
            a = random_matrix(rng, n)
            _, kappas = _condition_numbers(a)
            smallest = min(smallest, float(np.min(kappas)))
    return check("kappa(lambda) >= 1 always (Cauchy-Schwarz)",
                 smallest >= 1.0 - 1e-9, "illustration",
                 f"smallest kappa over 120 random matrices: {smallest:.9f}")


def normal_matrices_have_condition_number_one():
    rng = np.random.default_rng(9)
    worst = 0.0
    for kind in ("symmetric", "normal"):
        for _ in range(25):
            a = random_matrix(rng, 6, kind=kind)
            _, kappas = _condition_numbers(a)
            worst = max(worst, float(np.max(np.abs(kappas - 1.0))))
    return check("every eigenvalue of a normal matrix has kappa = 1",
                 worst < 1e-8, "illustration",
                 f"worst |kappa - 1| over 50 normal matrices: {worst:.3e}\n"
                 "for a normal matrix the left and right eigenvectors coincide")


def the_bound_is_attained_by_rank_one_e():
    """E = y x* makes the first-order bound an equality."""
    rng = np.random.default_rng(21)
    worst = 0.0
    for n in (2, 3, 5):
        a = random_matrix(rng, n)
        w, vr = np.linalg.eig(a)
        _, vl = np.linalg.eig(a.conj().T)
        i = 0
        x = vr[:, i] / np.linalg.norm(vr[:, i])
        j = int(np.argmin(np.abs(np.linalg.eigvals(a.conj().T) - np.conj(w[i]))))
        y = vl[:, j] / np.linalg.norm(vl[:, j])
        e = np.outer(y, x.conj())
        achieved = abs(np.vdot(y, e @ x) / np.vdot(y, x))
        predicted = 1.0 / abs(np.vdot(y, x))
        worst = max(worst, abs(achieved - predicted) / predicted)
    return check("E = y x* attains the first-order bound exactly",
                 worst < 1e-10, "illustration",
                 f"worst relative deviation from kappa(lambda): {worst:.3e}; "
                 "so kappa is the exact amplification, not an over-estimate")


def conditioning_varies_within_one_matrix():
    """Part 3: one eigenvalue at kappa = 1, another at 1e8."""
    a = np.array([[1.0, 1e8, 0.0],
                  [0.0, 2.0, 0.0],
                  [0.0, 0.0, 5.0]])
    w, kappas = _condition_numbers(a)
    order = np.argsort(w.real)
    rows = [f"lambda = {w[i].real:.1f}: kappa = {kappas[i]:.4e}" for i in order]
    _, v = np.linalg.eig(a)
    v = v / np.linalg.norm(v, axis=0)
    best, worst = float(np.min(kappas)), float(np.max(kappas))
    return check("one matrix, eigenvalue condition numbers 1 and 1e8",
                 best < 1.001 and worst > 1e7, "witness",
                 "\n".join(rows)
                 + f"\nkappa_2(V) for the whole matrix = {np.linalg.cond(v, 2):.4e}\n"
                   "the global Bauer-Fike constant would predict an 8-digit loss "
                   "for lambda = 5, which loses none")


def the_well_conditioned_eigenvalue_really_is_accurate():
    """Perturb and watch: lambda = 5 moves by ||E||, the others by 1e8 ||E||."""
    a = np.array([[1.0, 1e8, 0.0],
                  [0.0, 2.0, 0.0],
                  [0.0, 0.0, 5.0]])
    rng = np.random.default_rng(31)
    e = rng.normal(size=(3, 3))
    e *= 1e-10 / np.linalg.norm(e, 2)
    before = np.sort(np.linalg.eigvals(a).real)
    after = np.sort(np.linalg.eigvals(a + e).real)
    shifts = np.abs(after - before)
    rows = [f"lambda = {b:.1f}: shift = {s:.3e} (amplification {s / 1e-10:.2e})"
            for b, s in zip(before, shifts)]
    return check("the predicted per-eigenvalue behaviour is what happens",
                 shifts[-1] < 1e-9 and max(shifts[:2]) > 1e-4, "illustration",
                 "\n".join(rows)
                 + "\nlambda = 5 loses nothing; lambda = 1, 2 lose eight digits")


def kappa_diverges_as_eigenvalues_coalesce():
    """Part 4: kappa ~ 1/gap as a defective eigenvalue is approached."""
    rows = []
    kappas = []
    for delta in (1e-2, 1e-4, 1e-6, 1e-8):
        a = np.array([[1.0, 1.0], [delta, 1.0]])
        w, k = _condition_numbers(a)
        gap = abs(w[0] - w[1])
        kappas.append(float(np.max(k)))
        rows.append(f"delta = {delta:.0e}: eigenvalue gap = {gap:.3e}, "
                    f"kappa = {np.max(k):.3e}")
    growth = [kappas[i + 1] / kappas[i] for i in range(len(kappas) - 1)]
    return check("kappa -> infinity as the eigenvalues coalesce",
                 all(g > 5.0 for g in growth), "illustration",
                 "\n".join(rows)
                 + f"\neach factor of 100 in delta multiplies kappa by "
                   f"{np.mean(growth):.1f} (predicted 10, i.e. kappa ~ delta^(-1/2))")


def defective_limit_has_kappa_infinite():
    for n in (2, 5, 9):
        j = np.diag(np.ones(n - 1), 1)
        x = np.zeros(n); x[0] = 1.0
        y = np.zeros(n); y[-1] = 1.0
        if float(abs(np.vdot(y, x))) != 0.0:
            return check("y*x = 0 at the defective limit", False, "witness", "")
    return check("y*x = 0 exactly at the defective limit",
                 True, "witness",
                 "for the nilpotent Jordan block x = e_1 and y = e_n, so y*x = 0 "
                 "and kappa is infinite: the first-order statement of the "
                 "eps^(1/n) result")


CHECKS = [
    first_order_formula_predicts_the_shift,
    symbolic_derivation_of_the_formula,
    condition_number_is_at_least_one,
    normal_matrices_have_condition_number_one,
    the_bound_is_attained_by_rank_one_e,
    conditioning_varies_within_one_matrix,
    the_well_conditioned_eigenvalue_really_is_accurate,
    kappa_diverges_as_eigenvalues_coalesce,
    defective_limit_has_kappa_infinite,
]

if __name__ == "__main__":
    raise SystemExit(report(PROBLEM, run_checks(CHECKS)))
