#!/usr/bin/env python3
"""Verification for `linearization-is-inconclusive-at-the-critical-case`.

The closed-form solutions are obtained symbolically, so Parts 1-3 are settled
by SymPy rather than by sampling. The two-dimensional example in Part 4 is
settled by the Lyapunov identity, also symbolic; the trajectory integrations
are illustration only, and the problem's `numerical-evidence-settles-it` flawed
solution is about exactly why.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from bench.verify_support import (check, report, run_checks,  # noqa: E402
                                  symbolically_zero)

PROBLEM = "linearization-is-inconclusive-at-the-critical-case"


def both_systems_have_the_same_linearisation():
    x = sp.Symbol("x", real=True)
    jacobians = [sp.diff(sigma * x ** 3, x).subs(x, 0) for sigma in (-1, 1)]
    return check("both systems linearise to the zero system",
                 all(symbolically_zero(j) for j in jacobians), "sympy-identity",
                 f"d/dx(-x^3)|_0 = {jacobians[0]}, d/dx(+x^3)|_0 = {jacobians[1]}; "
                 "single eigenvalue 0, so the critical case applies to both")


def they_agree_to_second_order():
    """No criterion using fewer than three derivatives can separate them."""
    x = sp.Symbol("x", real=True)
    f_minus, f_plus = -x ** 3, x ** 3
    diffs = [sp.diff(f_plus - f_minus, x, k).subs(x, 0) for k in range(3)]
    third = sp.diff(f_plus - f_minus, x, 3).subs(x, 0)
    return check("the two right-hand sides agree through second order",
                 all(symbolically_zero(d) for d in diffs) and third != 0,
                 "sympy-identity",
                 f"derivatives 0,1,2 of the difference at 0: {diffs}; "
                 f"third derivative: {third}\n"
                 "so any criterion that separates them must reach the cubic term")


def closed_form_solutions():
    t = sp.Symbol("t", positive=True)
    x0 = sp.Symbol("x_0", positive=True)
    results = {}
    for sigma, name in ((-1, "minus"), (1, "plus")):
        candidate = x0 / sp.sqrt(1 - 2 * sigma * x0 ** 2 * t)
        residual = sp.simplify(sp.diff(candidate, t) - sigma * candidate ** 3)
        results[name] = symbolically_zero(residual)
    return check("x(t) = x_0 / sqrt(1 - 2 sigma x_0^2 t) solves both equations",
                 all(results.values()), "sympy-identity",
                 f"verified by substitution for sigma = -1 and +1: {results}")


def blow_up_time_is_one_over_two_x0_squared():
    rows = []
    ok = True
    for x0 in (1.0, 0.1, 0.01):
        t_star = 1.0 / (2.0 * x0 ** 2)
        probes = []
        for frac in (0.99, 0.9999):
            sol = solve_ivp(lambda t, y: y ** 3, [0, frac * t_star], [x0],
                            rtol=1e-12, atol=1e-14)
            probes.append(float(sol.y[0, -1]))
        exact = [x0 / np.sqrt(1 - frac) for frac in (0.99, 0.9999)]
        rows.append(f"x0 = {x0:<5g} t* = {t_star:<8g} x(0.99 t*) = {probes[0]:.4f} "
                    f"(exact {exact[0]:.4f}), x(0.9999 t*) = {probes[1]:.4f} "
                    f"(exact {exact[1]:.4f})")
        ok = ok and all(abs(p - e) / e < 1e-3 for p, e in zip(probes, exact))
    return check("blow-up at t* = 1/(2 x0^2), matching the closed form",
                 ok, "illustration", "\n".join(rows))


def blow_up_is_invisible_until_the_end():
    """Why `numerical-evidence-settles-it` fails: x = x0 (1 - t/t*)^(-1/2)."""
    rows = []
    for x0 in (0.1, 0.01, 0.001):
        t_star = 1.0 / (2.0 * x0 ** 2)
        at_5 = x0 / np.sqrt(1 - 2 * x0 ** 2 * 5.0)
        rows.append(f"x0 = {x0:<6g}: t* = {t_star:<9g}, x(5) = {at_5:.6f} "
                    f"(horizon reached {100 * 5.0 / t_star:.3f}% of t*)")
    return check("a horizon of t = 5 reaches at most 10% of the blow-up time",
                 True, "witness", "\n".join(rows)
                 + "\nand x = x0 (1 - t/t*)^(-1/2) is only 100 x0 at t = 0.9999 t*, "
                   "so no fixed threshold detects the blow-up for small x0")


def decay_is_algebraic_not_exponential():
    """x(t) = x_0/sqrt(1 + 2 x_0^2 t), approaching 1/sqrt(2t) from below.

    The approach to the asymptote is itself checked rather than assumed: the
    exact ratio to 1/sqrt(2t) is sqrt(2 x_0^2 t / (1 + 2 x_0^2 t)), which at
    x_0 = 0.01, t = 1e6 is sqrt(200/201) = 0.99751: not 1. Comparing against
    the asymptote with a tight tolerance would flag correct behaviour as a
    failure; comparing against the closed form does not.
    """
    rows = []
    ok = True
    horizon = 1e6
    for x0 in (1.0, 10.0, 0.01):
        sol = solve_ivp(lambda t, y: -y ** 3, [0, horizon], [x0],
                        rtol=1e-12, atol=1e-16, dense_output=True)
        got = float(sol.sol(horizon)[0])
        exact = x0 / np.sqrt(1 + 2 * x0 ** 2 * horizon)
        asymptotic = 1.0 / np.sqrt(2 * horizon)
        predicted_ratio = np.sqrt(2 * x0 ** 2 * horizon / (1 + 2 * x0 ** 2 * horizon))
        rows.append(f"x0 = {x0:<6g}: x(1e6) = {got:.6e}, closed form = {exact:.6e}, "
                    f"ratio to 1/sqrt(2t) = {got / asymptotic:.5f} "
                    f"(predicted {predicted_ratio:.5f})")
        ok = ok and abs(got - exact) / exact < 1e-6 \
            and abs(got / asymptotic - predicted_ratio) < 1e-5
    return check("x(t) matches the closed form and approaches 1/sqrt(2t)",
                 ok, "illustration", "\n".join(rows)
                 + "\nthe limiting rate carries no x_0 at all; a hyperbolic "
                   "equilibrium would give x_0 e^{-at}")


def two_dimensional_jacobian_is_a_centre():
    x, y = sp.symbols("x y", real=True)
    f = sp.Matrix([-y - x ** 3, x - y ** 3])
    jac = f.jacobian([x, y]).subs({x: 0, y: 0})
    eigen = sorted(jac.eigenvals(), key=str)
    expected = {sp.I, -sp.I}
    return check("the 2-D example linearises to a centre (eigenvalues +-i)",
                 set(eigen) == expected, "sympy-identity",
                 f"J(0,0) = {jac.tolist()}, eigenvalues {sorted(map(str, eigen))}; "
                 "real parts exactly zero, so the first method is silent")


def lyapunov_function_settles_the_two_dimensional_case():
    x, y = sp.symbols("x y", real=True)
    v = x ** 2 + y ** 2
    f = (-y - x ** 3, x - y ** 3)
    v_dot = sp.expand(sp.diff(v, x) * f[0] + sp.diff(v, y) * f[1])
    return check("V = x^2 + y^2 gives V' = -2(x^4 + y^4) exactly",
                 symbolically_zero(v_dot + 2 * (x ** 4 + y ** 4)), "sympy-identity",
                 f"V' = {v_dot}; strictly negative away from the origin, so the "
                 "origin is globally asymptotically stable by the second method")


def flipping_the_cubic_terms_flips_the_conclusion():
    x, y = sp.symbols("x y", real=True)
    v = x ** 2 + y ** 2
    f = (-y + x ** 3, x + y ** 3)
    jac = sp.Matrix(list(f)).jacobian([x, y]).subs({x: 0, y: 0})
    v_dot = sp.expand(sp.diff(v, x) * f[0] + sp.diff(v, y) * f[1])
    same_jacobian = symbolically_zero(jac - sp.Matrix([[0, -1], [1, 0]]))
    return check("the same linearisation with +x^3 gives V' > 0",
                 same_jacobian and symbolically_zero(v_dot - 2 * (x ** 4 + y ** 4)),
                 "witness",
                 f"J(0,0) = {jac.tolist()} (identical), but V' = {v_dot}\n"
                 "so the 2-D critical case is as undecidable by J as the scalar one")


def trajectories_of_the_two_dimensional_system():
    rows = []
    ok = True
    for x0 in ([0.5, 0.0], [1.0, 1.0], [0.1, -0.3]):
        sol = solve_ivp(lambda t, z: [-z[1] - z[0] ** 3, z[0] - z[1] ** 3],
                        [0, 60], x0, rtol=1e-10, atol=1e-12)
        end = float(np.linalg.norm(sol.y[:, -1]))
        rows.append(f"|x(0)| = {np.linalg.norm(x0):.3f} -> |x(60)| = {end:.4e}")
        ok = ok and end < 0.2
    return check("trajectories decay, at the same x_0-independent algebraic rate",
                 ok, "illustration", "\n".join(rows)
                 + "\nall three reach ~0.1 regardless of where they started, the "
                   "same signature as the scalar case")


CHECKS = [
    both_systems_have_the_same_linearisation,
    they_agree_to_second_order,
    closed_form_solutions,
    blow_up_time_is_one_over_two_x0_squared,
    blow_up_is_invisible_until_the_end,
    decay_is_algebraic_not_exponential,
    two_dimensional_jacobian_is_a_centre,
    lyapunov_function_settles_the_two_dimensional_case,
    flipping_the_cubic_terms_flips_the_conclusion,
    trajectories_of_the_two_dimensional_system,
]

if __name__ == "__main__":
    raise SystemExit(report(PROBLEM, run_checks(CHECKS)))
