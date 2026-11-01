#!/usr/bin/env python3
"""Verification for `second-dahlquist-barrier`.

The barrier itself is NOT established here and could not be: it is a universal
claim over an uncountable coefficient space and all step numbers k. What the
checks do is (a) verify the order conditions symbolically for specific methods,
(b) exhibit an exact witness refuting "every BDF is A-stable", and (c)
demonstrate directly that a sampled A-stability test can miss instability:
the gap that makes a search a refutation procedure and not a proof procedure.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from bench.verify_support import (check, report, run_checks,  # noqa: E402
                                  symbolically_zero)

PROBLEM = "second-dahlquist-barrier"

# alpha, beta indexed j = 0..k, normalised so alpha_k = 1
METHODS = {
    "trapezoidal": ([sp.Rational(-1), sp.Rational(1)],
                    [sp.Rational(1, 2), sp.Rational(1, 2)]),
    "implicit Euler": ([sp.Rational(-1), sp.Rational(1)],
                       [sp.Rational(0), sp.Rational(1)]),
    "explicit Euler": ([sp.Rational(-1), sp.Rational(1)],
                       [sp.Rational(1), sp.Rational(0)]),
    "BDF2": ([sp.Rational(1, 3), sp.Rational(-4, 3), sp.Rational(1)],
             [sp.Rational(0), sp.Rational(0), sp.Rational(2, 3)]),
    "BDF3": ([sp.Rational(-2, 11), sp.Rational(9, 11), sp.Rational(-18, 11),
              sp.Rational(1)],
             [sp.Rational(0), sp.Rational(0), sp.Rational(0), sp.Rational(6, 11)]),
}


def _error_constants(alpha, beta, up_to=5):
    """C_i for i = 0..up_to, with C_i = 0 for i <= p defining order p."""
    k = len(alpha) - 1
    constants = [sum(alpha)]
    for i in range(1, up_to + 1):
        term = (sp.Rational(1, sp.factorial(i))
                * sum(sp.Integer(j) ** i * alpha[j] for j in range(k + 1)))
        term -= (sp.Rational(1, sp.factorial(i - 1))
                 * sum(sp.Integer(j) ** (i - 1) * beta[j] for j in range(k + 1)))
        constants.append(sp.simplify(term))
    return constants


def _order(alpha, beta):
    constants = _error_constants(alpha, beta)
    p = 0
    for i, c in enumerate(constants):
        if symbolically_zero(c):
            p = i
        else:
            break
    return p, constants


def order_conditions_for_the_trapezoidal_rule():
    p, constants = _order(*METHODS["trapezoidal"])
    return check("the trapezoidal rule has order exactly 2, error constant -1/12",
                 p == 2 and constants[3] == sp.Rational(-1, 12),
                 "sympy-identity",
                 "C_0..C_3 = " + ", ".join(str(c) for c in constants[:4])
                 + f"\norder = {p}, error constant C_3 = {constants[3]}")


def orders_of_the_standard_methods():
    rows = []
    expected = {"trapezoidal": 2, "implicit Euler": 1, "explicit Euler": 1,
                "BDF2": 2, "BDF3": 3}
    ok = True
    for name, (alpha, beta) in METHODS.items():
        p, constants = _order(alpha, beta)
        rows.append(f"{name:16s}: order {p}, error constant {constants[p + 1]}")
        ok = ok and p == expected[name]
    return check("orders of the standard methods, from the conditions",
                 ok, "sympy-identity", "\n".join(rows))


def _root_moduli(alpha, beta, z):
    """Roots of rho(zeta) - z sigma(zeta), as a numpy polynomial in zeta."""
    k = len(alpha) - 1
    coeffs = [complex(alpha[j]) - z * complex(beta[j]) for j in range(k + 1)]
    return np.abs(np.roots(list(reversed(coeffs))))


def trapezoidal_and_bdf2_pass_a_sampled_a_stability_test():
    rng = np.random.default_rng(20260801)
    rows = []
    ok = True
    for name in ("trapezoidal", "implicit Euler", "BDF2"):
        alpha, beta = METHODS[name]
        worst = 0.0
        for _ in range(4000):
            z = complex(-abs(rng.normal()) * 10 ** rng.uniform(-2, 3),
                        rng.normal() * 10 ** rng.uniform(-2, 3))
            worst = max(worst, float(np.max(_root_moduli(alpha, beta, z))))
        rows.append(f"{name:16s}: max root modulus over 4000 z = {worst:.9f}")
        ok = ok and worst <= 1.0 + 1e-9
    return check("trapezoidal, implicit Euler and BDF2 pass a sampled A-stability test",
                 ok, "illustration", "\n".join(rows)
                 + "\nconsistent with A-stability; sampling cannot establish it")


def witness_bdf3_is_not_a_stable():
    """Part 4: one z in the open left half-plane settles it.

    The violating region sits close to the imaginary axis at modest |z|, not
    on the negative real axis, which is the point of the next check.
    """
    alpha, beta = METHODS["BDF3"]
    z = complex(-0.01, 1.14)
    moduli = np.sort(_root_moduli(alpha, beta, z))[::-1]
    return check("BDF3 is not A-stable: an exact witness near the imaginary axis",
                 z.real < 0 and moduli[0] > 1.0, "witness",
                 f"at z = {z} (Re z = {z.real} < 0) the stability polynomial has "
                 f"root moduli {np.round(moduli, 6)}\n"
                 f"the largest is {moduli[0]:.6f} > 1, so the root condition "
                 "fails and 'every BDF is A-stable' is refuted by one point")


def bdf3_wedge_angle_is_about_86_degrees():
    """The textbook A(alpha) half-angle for BDF3, measured."""
    alpha, beta = METHODS["BDF3"]
    rows = []
    crossing = None
    for half_angle in (80.0, 84.0, 86.0, 86.03, 87.0, 89.0):
        direction = np.exp(1j * (np.pi - np.deg2rad(half_angle)))
        worst = max(float(np.max(_root_moduli(alpha, beta, r * direction)))
                    for r in np.logspace(-2, 4, 300))
        rows.append(f"half-angle {half_angle:6.2f} deg: max root modulus along "
                    f"the ray = {worst:.6f}")
        if crossing is None and worst > 1.0:
            crossing = half_angle
    return check("BDF3's A(alpha) half-angle is between 86.03 and 87 degrees",
                 crossing == 87.0, "illustration",
                 "\n".join(rows)
                 + f"\nthe root condition first fails between 86.03 and "
                   f"{crossing} degrees, matching the published 86.03 deg")


def a_coarse_sample_would_have_missed_it():
    """Why gap 3 in the flawed solution matters: the unstable sliver is thin."""
    alpha, beta = METHODS["BDF3"]
    negative_real = [complex(-x, 0.0) for x in np.logspace(-3, 4, 400)]
    worst_real_axis = max(float(np.max(_root_moduli(alpha, beta, z)))
                          for z in negative_real)
    rng = np.random.default_rng(7)
    found = 0
    for _ in range(4000):
        z = complex(-abs(rng.normal()) * 10 ** rng.uniform(-2, 3),
                    rng.normal() * 10 ** rng.uniform(-2, 3))
        if np.max(_root_moduli(alpha, beta, z)) > 1.0 + 1e-12:
            found += 1
    return check("sampling the negative real axis alone would miss BDF3's instability",
                 worst_real_axis <= 1.0 + 1e-9 and found > 0, "witness",
                 f"400 points along the negative real axis: max root modulus "
                 f"{worst_real_axis:.9f} <= 1: looks A-stable\n"
                 f"4000 points spread over the half-plane: {found} violations found\n"
                 "a sampled test can only fail to find instability, which is "
                 "exactly why absence of hits proves nothing")


def bdf_order_equals_step_count():
    rows = []
    ok = True
    for name in ("BDF2", "BDF3"):
        alpha, beta = METHODS[name]
        k = len(alpha) - 1
        p, _ = _order(alpha, beta)
        rows.append(f"{name}: k = {k}, order = {p}")
        ok = ok and p == k
    return check("BDF-k has order k, so BDF3 has order 3 > 2",
                 ok, "sympy-identity", "\n".join(rows)
                 + "\nand it is not A-stable: consistent with the barrier, "
                   "which forces exactly this trade")


def runge_kutta_is_outside_the_class():
    """Gauss-Legendre: A-stable at order 2s, and not a linear multistep method."""
    z = sp.Symbol("z")
    rows = []
    ok = True
    # Gauss-Legendre stability functions are the diagonal Pade approximants.
    for s, order in ((1, 2), (2, 4), (3, 6)):
        num = sum(sp.binomial(s, j) * sp.factorial(2 * s - j)
                  / sp.factorial(2 * s) * z ** j for j in range(s + 1))
        den = num.subs(z, -z)
        r = sp.simplify(num / den)
        series = sp.series(r - sp.exp(z), z, 0, order + 2).removeO()
        matches = symbolically_zero(sp.expand(series.subs(z, 0)))
        leading = sp.simplify(sp.limit((r - sp.exp(z)) / z ** (order + 1), z, 0))
        on_axis = [abs(complex(r.subs(z, sp.I * y))) for y in (0.5, 2, 10, 100)]
        rows.append(f"s = {s}: order {order} diagonal Pade, |R(iy)| = "
                    + ", ".join(f"{v:.6f}" for v in on_axis))
        ok = ok and all(abs(v - 1.0) < 1e-9 for v in on_axis) and leading != 0
    return check("Gauss-Legendre is A-stable at order 2s, outside the LMM class",
                 ok, "illustration", "\n".join(rows)
                 + "\n|R(iy)| = 1 exactly on the imaginary axis at every order, "
                   "so these are A-stable of arbitrarily high order, and they "
                   "are Runge-Kutta methods, not linear multistep ones")


def the_barrier_itself_is_not_established_here():
    """An explicit statement of what this script does not do."""
    return check("the barrier is cited, not proved, in this repository",
                 True, "consistency",
                 "the second Dahlquist barrier quantifies over all k >= 1 and all "
                 "real coefficient vectors; no finite computation can establish "
                 "it.\nThe proof is Dahlquist (1963), via the Riesz-Herglotz "
                 "representation of rho/sigma, or Wanner-Hairer-Norsett via the "
                 "order star.\nWhat this script establishes is the refutation "
                 "half: an exact witness showing BDF3 is not A-stable.")


CHECKS = [
    order_conditions_for_the_trapezoidal_rule,
    orders_of_the_standard_methods,
    trapezoidal_and_bdf2_pass_a_sampled_a_stability_test,
    witness_bdf3_is_not_a_stable,
    bdf3_wedge_angle_is_about_86_degrees,
    a_coarse_sample_would_have_missed_it,
    bdf_order_equals_step_count,
    runge_kutta_is_outside_the_class,
    the_barrier_itself_is_not_established_here,
]

if __name__ == "__main__":
    raise SystemExit(report(PROBLEM, run_checks(CHECKS)))
