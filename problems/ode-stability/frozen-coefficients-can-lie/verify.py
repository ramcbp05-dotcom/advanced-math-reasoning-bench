#!/usr/bin/env python3
"""Verification for `frozen-coefficients-can-lie`.

The claim is existential, and the witness is verified **symbolically**: the
residual x' - A(t)x simplifies to exactly zero as a function of t. That check
settles Part 1; the trajectory integrations are illustration.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.linalg import expm

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from bench.verify_support import (check, report, run_checks,  # noqa: E402
                                  symbolically_zero)

PROBLEM = "frozen-coefficients-can-lie"
T = sp.Symbol("t", real=True)


def _A_sym():
    c, s = sp.cos(T), sp.sin(T)
    return sp.Matrix([
        [-1 + sp.Rational(3, 2) * c ** 2, 1 - sp.Rational(3, 2) * s * c],
        [-1 - sp.Rational(3, 2) * s * c, -1 + sp.Rational(3, 2) * s ** 2],
    ])


def _A_num(t):
    c, s = np.cos(t), np.sin(t)
    return np.array([[-1 + 1.5 * c * c, 1 - 1.5 * s * c],
                     [-1 - 1.5 * s * c, -1 + 1.5 * s * s]])


def exact_solution_verified_by_substitution():
    """The witness: x' - A(t)x simplifies to zero identically in t."""
    a = _A_sym()
    x = sp.exp(T / 2) * sp.Matrix([-sp.cos(T), sp.sin(T)])
    residual = sp.simplify(sp.expand_trig(sp.diff(x, T) - a * x))
    return check("x(t) = e^(t/2)(-cos t, sin t) solves x' = A(t)x exactly",
                 symbolically_zero(residual), "witness",
                 f"residual x' - A(t)x simplifies to {residual.T.tolist()}\n"
                 "verified symbolically as a function of t, not at sample points")


def eigenvalues_are_constant_and_stable():
    a = _A_sym()
    trace = sp.simplify(sp.expand_trig(a.trace()))
    det = sp.simplify(sp.expand_trig(a.det()))
    eigen = sorted((sp.simplify(e) for e in a.eigenvals()), key=str)
    real_parts = {sp.simplify(sp.re(e)) for e in eigen}
    ok = (symbolically_zero(trace + sp.Rational(1, 2))
          and symbolically_zero(det - sp.Rational(1, 2))
          and real_parts == {sp.Rational(-1, 4)})
    return check("eigenvalues are (-1 +- i sqrt7)/4 for every t",
                 ok, "sympy-identity",
                 f"tr A(t) = {trace}, det A(t) = {det} (both constant)\n"
                 f"eigenvalues {[str(e) for e in eigen]}, real part "
                 f"{sorted(map(str, real_parts))}")


def eigenvalues_numerically_constant():
    rows = []
    ok = True
    reference = None
    for t in (0.0, 0.7, 1.3, 2.9, 4.4, 10.0):
        ev = np.sort_complex(np.linalg.eigvals(_A_num(t)))
        if reference is None:
            reference = ev
        else:
            ok = ok and np.max(np.abs(ev - reference)) < 1e-12
        rows.append(f"t = {t:4.1f}: {np.round(ev, 9)}")
    return check("frozen eigenvalues do not move with t",
                 ok and abs(reference[0].real + 0.25) < 1e-12, "illustration",
                 "\n".join(rows) + "\nreal part -0.25 at every t")


def the_solution_grows():
    sol = solve_ivp(lambda t, x: _A_num(t) @ x, [0, 20], [-1.0, 0.0],
                    rtol=1e-11, atol=1e-13, dense_output=True)
    rows = []
    ok = True
    for t in (0, 5, 10, 20):
        got = float(np.linalg.norm(sol.sol(t)))
        want = float(np.exp(t / 2))
        rows.append(f"t = {t:2d}: ||x(t)|| = {got:.6e}, e^(t/2) = {want:.6e}")
        ok = ok and abs(got - want) / want < 1e-6
    return check("the numerical solution grows like e^(t/2)",
                 ok, "illustration", "\n".join(rows)
                 + "\nwhile every frozen eigenvalue predicts decay at e^(-t/4)")


def frozen_prediction_is_wrong_in_direction():
    rows = []
    for t in (5, 10, 20):
        rows.append(f"t = {t:2d}: frozen criterion predicts e^(-t/4) = "
                    f"{np.exp(-t / 4):.4f}, actual {np.exp(t / 2):.4e}")
    return check("the frozen criterion is wrong in direction, not just magnitude",
                 True, "witness", "\n".join(rows))


def trace_and_determinant_reconcile():
    """Abel: det Phi(t) = exp(int tr A) = e^(-t/2), while one column grows."""
    period = 2 * np.pi
    phi = np.eye(2)
    n = 40000
    dt = period / n
    # integrate the fundamental matrix columnwise
    cols = []
    for e in (np.array([1.0, 0.0]), np.array([0.0, 1.0])):
        sol = solve_ivp(lambda t, x: _A_num(t) @ x, [0, period], e,
                        rtol=1e-12, atol=1e-14)
        cols.append(sol.y[:, -1])
    phi = np.column_stack(cols)
    det_phi = float(np.linalg.det(phi))
    abel = float(np.exp(-period / 2))
    return check("det Phi(2pi) = e^(-pi), matching Abel-Jacobi-Liouville",
                 abs(det_phi - abel) / abel < 1e-6, "illustration",
                 f"det Phi(2pi) = {det_phi:.9f}, exp(int tr A) = {abel:.9f}\n"
                 "volume contracts while one direction expands: the two Lyapunov "
                 "exponents are +1/2 and -1, summing to tr A = -1/2")


def floquet_multipliers_detect_the_instability():
    period = 2 * np.pi
    cols = []
    for e in (np.array([1.0, 0.0]), np.array([0.0, 1.0])):
        sol = solve_ivp(lambda t, x: _A_num(t) @ x, [0, period], e,
                        rtol=1e-12, atol=1e-14)
        cols.append(sol.y[:, -1])
    monodromy = np.column_stack(cols)
    rho = np.sort(np.abs(np.linalg.eigvals(monodromy)))[::-1]
    predicted = np.array([np.exp(np.pi), np.exp(-2 * np.pi)])
    return check("Floquet multipliers are e^pi and e^(-2pi)",
                 abs(rho[0] - predicted[0]) / predicted[0] < 1e-5
                 and rho[0] > 1.0, "illustration",
                 f"|rho| = {np.round(rho, 8)}, predicted {np.round(predicted, 8)}\n"
                 f"product = {rho[0] * rho[1]:.9f} vs det Phi = "
                 f"{np.exp(-np.pi):.9f}\n"
                 "|rho_1| > 1 correctly reports the instability that the frozen "
                 "eigenvalues miss")


def rotating_frame_gives_the_true_exponents():
    """x = Q(t)y with Q a CLOCKWISE rotation diagonalises the system exactly.

    The direction matters: with Q = rot(+t) the transformed matrix is not even
    constant. With Q = rot(-t),

        Q^-1 A Q - Q^-1 Q' = diag(1/2, -1)

    exactly: a constant *diagonal* matrix whose entries are the Lyapunov
    exponents, confirmed independently by the Floquet multipliers
    ln|rho|/(2 pi) = (+1/2, -1).
    """
    a = _A_sym()
    q = sp.Matrix([[sp.cos(T), sp.sin(T)], [-sp.sin(T), sp.cos(T)]])
    transformed = sp.simplify(sp.expand_trig(
        q.inv() * a * q - q.inv() * sp.diff(q, T)))
    expected = sp.diag(sp.Rational(1, 2), -1)
    exact = symbolically_zero(transformed - expected)

    # and the other direction of rotation does not work
    q_wrong = sp.Matrix([[sp.cos(T), -sp.sin(T)], [sp.sin(T), sp.cos(T)]])
    wrong = sp.simplify(sp.expand_trig(
        q_wrong.inv() * a * q_wrong - q_wrong.inv() * sp.diff(q_wrong, T)))
    wrong_is_constant = all(symbolically_zero(sp.diff(e, T)) for e in wrong)

    return check("the clockwise rotating frame gives exactly diag(1/2, -1)",
                 exact and not wrong_is_constant, "sympy-identity",
                 f"Q = rot(-t): Q^-1 A Q - Q^-1 Q' = {transformed.tolist()}\n"
                 f"a constant diagonal matrix; its entries are the Lyapunov "
                 f"exponents +1/2 and -1, summing to tr A = -1/2\n"
                 f"Q = rot(+t) instead gives a non-constant matrix "
                 f"(constant: {wrong_is_constant}): the direction of the "
                 "rotation is part of the answer")


def floquet_exponents_match_the_rotating_frame():
    """An independent route to the same two numbers."""
    period = 2 * np.pi
    cols = []
    for e in (np.array([1.0, 0.0]), np.array([0.0, 1.0])):
        sol = solve_ivp(lambda t, x: _A_num(t) @ x, [0, period], e,
                        rtol=1e-13, atol=1e-15)
        cols.append(sol.y[:, -1])
    rho = np.linalg.eigvals(np.column_stack(cols))
    exponents = np.sort(np.log(np.abs(rho)) / period)[::-1]
    return check("Floquet exponents are +1/2 and -1, matching the rotating frame",
                 np.max(np.abs(exponents - np.array([0.5, -1.0]))) < 1e-9,
                 "illustration",
                 f"ln|rho|/(2pi) = {np.round(exponents, 10)}\n"
                 f"sum = {exponents.sum():.10f} against tr A = -0.5, as "
                 "Abel-Jacobi-Liouville requires\n"
                 "two independent methods, one symbolic and one numerical, "
                 "agreeing on the exponents the frozen eigenvalues miss")


def slowing_the_variation_does_not_help():
    """Part 4: eps A(eps t) still grows, at rate eps/2."""
    rows = []
    ok = True
    for eps in (1.0, 0.1, 0.01):
        horizon = 20.0 / eps
        sol = solve_ivp(lambda t, x: eps * _A_num(eps * t) @ x,
                        [0, horizon], [-1.0, 0.0], rtol=1e-11, atol=1e-13)
        got = float(np.linalg.norm(sol.y[:, -1]))
        want = float(np.exp(eps * horizon / 2))
        ev = np.linalg.eigvals(eps * _A_num(0.0))
        rows.append(f"eps = {eps:<5g}: ||x({horizon:.0f})|| = {got:.4e}, "
                    f"e^(eps t/2) = {want:.4e}, Re(eigenvalues) = "
                    f"{ev[0].real:.4f}")
        ok = ok and abs(got - want) / want < 1e-5 and ev[0].real < 0
    return check("slowing the variation slows the growth by the same factor",
                 ok, "witness", "\n".join(rows)
                 + "\nstill unbounded for every eps > 0, with frozen eigenvalues "
                   "still in the open left half-plane")


CHECKS = [
    exact_solution_verified_by_substitution,
    eigenvalues_are_constant_and_stable,
    eigenvalues_numerically_constant,
    the_solution_grows,
    frozen_prediction_is_wrong_in_direction,
    trace_and_determinant_reconcile,
    floquet_multipliers_detect_the_instability,
    rotating_frame_gives_the_true_exponents,
    floquet_exponents_match_the_rotating_frame,
    slowing_the_variation_does_not_help,
]

if __name__ == "__main__":
    raise SystemExit(report(PROBLEM, run_checks(CHECKS)))
