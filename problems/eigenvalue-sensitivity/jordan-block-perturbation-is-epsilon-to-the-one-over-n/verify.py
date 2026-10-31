#!/usr/bin/env python3
"""Verification for `jordan-block-perturbation-is-epsilon-to-the-one-over-n`.

The characteristic-polynomial identity is checked symbolically for n = 2..10,
which proves it for those n. The general n is proved in solution.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from bench.verify_support import (check, report, run_checks,  # noqa: E402
                                  symbolically_zero)

PROBLEM = "jordan-block-perturbation-is-epsilon-to-the-one-over-n"


def _jordan(n, eps=0.0, symbolic=False):
    if symbolic:
        m = sp.zeros(n, n)
        for i in range(n - 1):
            m[i, i + 1] = 1
        m[n - 1, 0] = eps
        return m
    m = np.diag(np.ones(n - 1), 1)
    m[-1, 0] = eps
    return m


def characteristic_polynomial_is_lambda_n_minus_eps():
    lam, eps = sp.symbols("lambda epsilon")
    results = []
    for n in range(2, 11):
        m = _jordan(n, eps, symbolic=True)
        char = sp.expand((lam * sp.eye(n) - m).det())
        results.append(symbolically_zero(char - (lam ** n - eps)))
    return check("det(lambda I - J_n(eps)) = lambda^n - eps for n = 2..10",
                 all(results), "sympy-identity",
                 "checked symbolically at each n; the determinant expansion in "
                 "solution.md covers general n")


def roots_are_the_nth_roots_of_eps():
    eps = sp.Rational(1, 10 ** 6)
    rows = []
    ok = True
    for n in (2, 3, 5):
        m = _jordan(n, eps, symbolic=True)
        roots = sp.Matrix(m).eigenvals()
        moduli = {sp.simplify(sp.Abs(r)) for r in roots}
        expected = sp.root(eps, n)
        same = all(symbolically_zero(mod - expected) for mod in moduli)
        ok = ok and same and sum(roots.values()) == n
        rows.append(f"n = {n}: {len(roots)} distinct roots, all of modulus "
                    f"{expected} = {float(expected):.6e}")
    return check("every root has modulus exactly eps^(1/n)",
                 ok, "sympy-identity", "\n".join(rows))


def roots_lie_on_a_regular_polygon():
    """The perturbation resolves the defective eigenvalue into an n-gon."""
    n, eps = 8, 1e-8
    roots = np.linalg.eigvals(_jordan(n, eps))
    moduli = np.abs(roots)
    angles = np.sort(np.angle(roots))
    gaps = np.diff(np.concatenate([angles, [angles[0] + 2 * np.pi]]))
    return check("the perturbed eigenvalues form a regular n-gon",
                 np.ptp(moduli) / moduli.mean() < 1e-10
                 and np.ptp(gaps) < 1e-9, "illustration",
                 f"n = {n}, eps = {eps:.0e}: moduli spread "
                 f"{np.ptp(moduli) / moduli.mean():.3e}, angular gaps all "
                 f"{gaps.mean():.6f} = 2pi/{n} (spread {np.ptp(gaps):.3e})")


def amplification_table():
    rows = []
    ok = True
    eps = 1e-16
    for n in (2, 4, 8, 16):
        moved = float(np.max(np.abs(np.linalg.eigvals(_jordan(n, eps)))))
        predicted = eps ** (1.0 / n)
        rows.append(f"n = {n:2d}: |lambda| = {moved:.6e}, eps^(1/n) = "
                    f"{predicted:.6e}, ratio = {moved / predicted:.4f}, "
                    f"amplification = {moved / eps:.1e}")
        ok = ok and abs(moved / predicted - 1.0) < 1e-6
    return check("amplification at double-rounding eps (Part 2)",
                 ok, "illustration", "\n".join(rows))


def left_and_right_eigenvectors_are_orthogonal():
    """The quantity first-order theory divides by is exactly zero."""
    rows = []
    ok = True
    for n in (2, 5, 9):
        j = _jordan(n)
        x = np.zeros(n)
        x[0] = 1.0                      # right eigenvector:  J e_1 = 0
        y = np.zeros(n)
        y[-1] = 1.0                     # left eigenvector:   e_n^T J = 0
        rows.append(f"n = {n}: ||J x|| = {np.linalg.norm(j @ x):.1e}, "
                    f"||y^T J|| = {np.linalg.norm(y @ j):.1e}, "
                    f"y^T x = {float(y @ x):.1f}")
        ok = ok and np.linalg.norm(j @ x) == 0 and np.linalg.norm(y @ j) == 0 \
            and float(y @ x) == 0.0
    return check("y*x = 0, so the first-order condition number is infinite",
                 ok, "witness", "\n".join(rows)
                 + "\nthe formula dlambda = y*Ex/(y*x) divides by zero here")


def first_order_prediction_is_wrong_by_orders_of_magnitude():
    """The `first-order-perturbation-theory` claim, measured."""
    rows = []
    ok = True
    eps = 1e-16
    for n in (2, 8, 16):
        actual = float(np.max(np.abs(np.linalg.eigvals(_jordan(n, eps)))))
        rows.append(f"n = {n:2d}: first-order predicts O({eps:.0e}), "
                    f"actual {actual:.3e} (wrong by {actual / eps:.1e}x)")
        ok = ok and actual / eps > 1e6
    return check("first-order theory is wrong by up to 1e15",
                 ok, "illustration", "\n".join(rows))


def the_matrix_is_defective():
    """Algebraic multiplicity n, geometric multiplicity 1."""
    rows = []
    ok = True
    for n in (2, 4, 7):
        m = _jordan(n, 0, symbolic=True)
        eigen = m.eigenvals()
        algebraic = eigen[sp.Integer(0)]
        geometric = n - m.rank()
        rows.append(f"n = {n}: algebraic multiplicity {algebraic}, "
                    f"geometric multiplicity {geometric}")
        ok = ok and algebraic == n and geometric == 1
    return check("J_n is defective: geometric multiplicity 1",
                 ok, "sympy-identity", "\n".join(rows)
                 + "\nso there is no eigenbasis and no first-order expansion")


def no_contradiction_with_weyl():
    """J_n is maximally non-Hermitian: spectral radius 0, norm 1."""
    rows = []
    ok = True
    for n in (2, 8, 16):
        j = _jordan(n)
        radius = float(np.max(np.abs(np.linalg.eigvals(j))))
        norm = float(np.linalg.norm(j, 2))
        asymmetry = float(np.max(np.abs(j - j.T)))
        rows.append(f"n = {n:2d}: spectral radius {radius:.1e}, ||J||_2 = "
                    f"{norm:.1f}, ||J - J^T||_max = {asymmetry:.1f}")
        ok = ok and radius < 1e-12 and norm > 0.9 and asymmetry > 0.9
    return check("J_n is not Hermitian, so Weyl does not apply (Part 4)",
                 ok, "illustration", "\n".join(rows)
                 + "\na Hermitian matrix with spectral radius 0 is the zero matrix")


CHECKS = [
    characteristic_polynomial_is_lambda_n_minus_eps,
    roots_are_the_nth_roots_of_eps,
    roots_lie_on_a_regular_polygon,
    amplification_table,
    left_and_right_eigenvectors_are_orthogonal,
    first_order_prediction_is_wrong_by_orders_of_magnitude,
    the_matrix_is_defective,
    no_contradiction_with_weyl,
]

if __name__ == "__main__":
    raise SystemExit(report(PROBLEM, run_checks(CHECKS)))
