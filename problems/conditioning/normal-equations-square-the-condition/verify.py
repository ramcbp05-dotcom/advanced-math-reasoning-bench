#!/usr/bin/env python3
"""Verification for `normal-equations-square-the-condition`.

The identity kappa(A^T A) = kappa(A)^2 is proved in solution.md. The checks
below sample it, and (more usefully) display the forward error and the
residual side by side across a range of condition numbers, which is the table
the `residual-means-accuracy` flawed solution would have needed.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from bench.verify_support import (check, relative_error, report,  # noqa: E402
                                  run_checks, symbolically_zero)

PROBLEM = "normal-equations-square-the-condition"
UNIT_ROUNDOFF = np.finfo(float).eps / 2


def _matrix_with_condition(rng, m, n, kappa):
    """Build an m x n matrix of full column rank with the requested kappa_2."""
    u, _ = np.linalg.qr(rng.normal(size=(m, n)))
    v, _ = np.linalg.qr(rng.normal(size=(n, n)))
    sigma = np.logspace(0, -np.log10(kappa), n)
    return (u * sigma) @ v.T, sigma


def identity_over_shapes_and_conditions():
    rng = np.random.default_rng(20260502)
    worst = 0.0
    for m, n in ((6, 4), (20, 7), (50, 12), (9, 9)):
        for kappa in (1e1, 1e3, 1e5):
            a, _ = _matrix_with_condition(rng, m, n, kappa)
            got = np.linalg.cond(a.T @ a, 2)
            want = np.linalg.cond(a, 2) ** 2
            worst = max(worst, relative_error(got, want))
    # The tolerance is set by the measurement, not by taste: computing
    # kappa(A^T A) numerically is itself accurate only to about u*kappa(A^T A),
    # which at kappa(A) = 1e5 means u*1e10 ~ 1e-6. Demanding more than that
    # would be asking the reference value to be better conditioned than the
    # quantity it measures, which is the very phenomenon under study.
    return check("kappa(A^T A) = kappa(A)^2 over 12 shapes and conditions",
                 worst < 1e-5, "illustration",
                 f"worst relative deviation {worst:.3e}; the floor here is "
                 "u*kappa(A^T A) ~ 1e-6 at kappa(A) = 1e5, so this is at the "
                 "accuracy limit of the measurement itself")


def singular_values_are_squared():
    rng = np.random.default_rng(5)
    worst = 0.0
    for m, n in ((10, 5), (30, 8)):
        a, _ = _matrix_with_condition(rng, m, n, 1e4)
        sv = np.linalg.svd(a, compute_uv=False)
        sv_gram = np.linalg.svd(a.T @ a, compute_uv=False)
        worst = max(worst, np.max(np.abs(sv_gram - sv ** 2) / sv ** 2))
    return check("singular values of A^T A are sigma_i^2 (Step 1)",
                 worst < 1e-7, "illustration",
                 f"worst relative deviation {worst:.3e} at kappa(A) = 1e4, "
                 "where the smallest squared singular value sits at 1e-8 of the "
                 "largest and carries about 8 digits")


def symbolic_gram_eigenvalues():
    """V Sigma^2 V^T exactly, for a symbolic 3x2 thin SVD."""
    s1, s2 = sp.symbols("sigma_1 sigma_2", positive=True)
    theta = sp.Symbol("theta", real=True)
    v = sp.Matrix([[sp.cos(theta), -sp.sin(theta)],
                   [sp.sin(theta), sp.cos(theta)]])
    u = sp.Matrix([[1, 0], [0, 1], [0, 0]])
    a = u * sp.diag(s1, s2) * v.T
    gram = sp.simplify(a.T * a)
    eigen = sorted((sp.simplify(e) for e in gram.eigenvals()), key=str)
    ok = symbolically_zero(gram - v * sp.diag(s1 ** 2, s2 ** 2) * v.T)
    return check("A^T A = V Sigma^2 V^T symbolically (3x2 thin SVD)",
                 ok, "sympy-identity",
                 f"eigenvalues of the Gram matrix: {[str(e) for e in eigen]}")


def submultiplicativity_alone_is_not_enough():
    """The gap the `submultiplicative-bound-as-equality` solution leaves open.

    kappa(AB) <= kappa(A)kappa(B) can be loose by an arbitrary factor, so the
    bound by itself does not imply the identity.
    """
    eps = 1e-6
    a = np.diag([1.0, eps])
    b = np.diag([eps, 1.0])
    bound = np.linalg.cond(a, 2) * np.linalg.cond(b, 2)
    actual = np.linalg.cond(a @ b, 2)
    return check("kappa(AB) <= kappa(A)kappa(B) can be loose by 1/eps^2",
                 actual < 1.5 and bound > 1e11, "witness",
                 f"kappa(A)kappa(B) = {bound:.3e} but kappa(AB) = {actual:.6f}; "
                 "an upper bound of this kind cannot establish an equality")


def forward_error_grows_as_kappa_squared():
    """The table the flawed solution needed: residual vs forward error."""
    rng = np.random.default_rng(20260503)
    rows = []
    ok = True
    for kappa in (1e2, 1e4, 1e6, 1e8, 1e10):
        a, _ = _matrix_with_condition(rng, 40, 10, kappa)
        x_exact = np.ones(10)
        b = a @ x_exact
        gram = a.T @ a
        try:
            x_normal = np.linalg.solve(gram, a.T @ b)
        except np.linalg.LinAlgError:
            x_normal = np.full(10, np.nan)
        x_qr, *_ = np.linalg.lstsq(a, b, rcond=None)

        fwd_normal = np.linalg.norm(x_normal - x_exact) / np.linalg.norm(x_exact)
        fwd_qr = np.linalg.norm(x_qr - x_exact) / np.linalg.norm(x_exact)
        res_normal = np.linalg.norm(a @ x_normal - b) / np.linalg.norm(b)
        rows.append(f"kappa={kappa:.0e}  normal: fwd {fwd_normal:.2e} "
                    f"residual {res_normal:.2e}   |  QR: fwd {fwd_qr:.2e}")
        if kappa >= 1e6 and np.isfinite(fwd_normal) and fwd_qr > 0:
            ok = ok and fwd_normal > 10.0 * fwd_qr
    return check("normal equations lose ~2x the digits QR loses",
                 ok, "illustration", "\n".join(rows))


def residual_bounds_the_error_only_up_to_kappa():
    """The inequality from Part 3, and its attainment."""
    rng = np.random.default_rng(13)
    worst_ratio = 0.0
    for kappa in (1e3, 1e6, 1e9):
        n = 8
        u, _ = np.linalg.qr(rng.normal(size=(n, n)))
        v, _ = np.linalg.qr(rng.normal(size=(n, n)))
        sigma = np.logspace(0, -np.log10(kappa), n)
        a = (u * sigma) @ v.T
        # b along u_1, perturbation along u_n: the attaining configuration.
        b = u[:, 0].copy()
        r = 1e-12 * u[:, -1]
        x = np.linalg.solve(a, b)
        x_hat = np.linalg.solve(a, b - r)
        lhs = np.linalg.norm(x - x_hat) / np.linalg.norm(x)
        rhs = np.linalg.cond(a, 2) * np.linalg.norm(r) / np.linalg.norm(b)
        worst_ratio = max(worst_ratio, lhs / rhs)
    return check("||dx||/||x|| <= kappa ||r||/||b|| is attained",
                 0.99 < worst_ratio <= 1.0 + 1e-4, "illustration",
                 f"the attaining configuration reaches {worst_ratio:.9f} of the "
                 "bound, so the inequality is sharp and not pessimism")


def digit_budget_arithmetic():
    """Part 2 is arithmetic; check it rather than trusting the prose."""
    kappa = 1e8
    normal = UNIT_ROUNDOFF * kappa ** 2
    qr = UNIT_ROUNDOFF * kappa
    breakdown_normal = UNIT_ROUNDOFF ** -0.5
    breakdown_qr = UNIT_ROUNDOFF ** -1.0
    ok = (normal > 0.5 and 1e-9 < qr < 1e-7
          and 5e7 < breakdown_normal < 2e8 and breakdown_qr > 1e15)
    return check("Part 2 digit budget",
                 ok, "consistency",
                 f"u = {UNIT_ROUNDOFF:.3e}; at kappa = 1e8 the normal equations "
                 f"predict {normal:.2e} and QR {qr:.2e}; breakdown at "
                 f"kappa = {breakdown_normal:.2e} and {breakdown_qr:.2e}")


CHECKS = [
    identity_over_shapes_and_conditions,
    singular_values_are_squared,
    symbolic_gram_eigenvalues,
    submultiplicativity_alone_is_not_enough,
    forward_error_grows_as_kappa_squared,
    residual_bounds_the_error_only_up_to_kappa,
    digit_budget_arithmetic,
]

if __name__ == "__main__":
    raise SystemExit(report(PROBLEM, run_checks(CHECKS)))
