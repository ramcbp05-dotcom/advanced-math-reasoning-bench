#!/usr/bin/env python3
"""Verification for `trapezoidal-is-a-stable-but-not-l-stable`."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from bench.verify_support import (check, report, run_checks,  # noqa: E402
                                  symbolically_zero)

PROBLEM = "trapezoidal-is-a-stable-but-not-l-stable"


def R_trap(z):
    return (1 + z / 2) / (1 - z / 2)


def amplification_factor():
    z, y = sp.symbols("z y")
    y_next = sp.symbols("y_next")
    equation = sp.Eq(y_next, y + z / 2 * (y + y_next))
    solved = sp.solve(equation, y_next)[0]
    return check("R(z) = (1 + z/2)/(1 - z/2)",
                 symbolically_zero(sp.simplify(solved / y) - (1 + z / 2) / (1 - z / 2)),
                 "sympy-identity",
                 f"solving the implicit step gives y_(n+1)/y_n = "
                 f"{sp.simplify(solved / y)}")


def region_is_exactly_the_left_half_plane():
    """|R(z)| <= 1 <=> Re z <= 0, as a symbolic equivalence."""
    x, y = sp.symbols("x y", real=True)
    z = x + sp.I * y
    lhs = sp.simplify(sp.Abs(1 + z / 2) ** 2 - sp.Abs(1 - z / 2) ** 2)
    expanded = sp.simplify(sp.expand(lhs))
    return check("|1+z/2|^2 - |1-z/2|^2 = 2x, so the region is exactly Re z <= 0",
                 symbolically_zero(expanded - 2 * x), "sympy-identity",
                 f"the difference of squared moduli simplifies to {expanded}; "
                 "an equivalence, so both inclusions hold with no slack")


def region_sampled_numerically():
    rng = np.random.default_rng(20260702)
    mismatches = 0
    for _ in range(5000):
        z = complex(rng.uniform(-50, 50), rng.uniform(-50, 50))
        if abs(z.real) < 1e-9:
            continue
        if (abs(R_trap(z)) <= 1.0) != (z.real <= 0.0):
            mismatches += 1
    return check("sampled region agrees with the left half-plane",
                 mismatches == 0, "illustration",
                 f"5000 sample points across Re z in [-50, 50], "
                 f"{mismatches} disagreements")


def imaginary_axis_is_non_dissipative():
    """|R(iy)| = 1 exactly: the trapezoidal rule preserves oscillation amplitude."""
    worst = 0.0
    for y in (0.1, 1.0, 10.0, 1e3, 1e6):
        worst = max(worst, abs(abs(R_trap(1j * y)) - 1.0))
    return check("|R(iy)| = 1 exactly on the imaginary axis",
                 worst < 1e-12, "illustration",
                 f"worst |{'|R|'} - 1| over five frequencies: {worst:.3e}; "
                 "this is a virtue for wave problems and the cause of the "
                 "trouble for stiff ones")


def limit_is_minus_one_not_zero():
    z = sp.Symbol("z", real=True)
    limit = sp.limit((1 + z / 2) / (1 - z / 2), z, -sp.oo)
    rows = [f"z = {zv:>9.0e}: R(z) = {R_trap(float(zv)):+.10f}"
            for zv in (-1, -10, -1e2, -1e4, -1e8)]
    return check("R(z) -> -1 as z -> -infinity, so the method is not L-stable",
                 limit == -1, "sympy-identity",
                 f"symbolic limit = {limit}\n" + "\n".join(rows))


def implicit_euler_is_l_stable():
    z = sp.Symbol("z", real=True)
    limit = sp.limit(1 / (1 - z), z, -sp.oo)
    rows = [f"z = {zv:>9.0e}: R_BE(z) = {1 / (1 - float(zv)):.3e}"
            for zv in (-1, -1e2, -1e4, -1e8)]
    return check("implicit Euler has R(z) -> 0, so it is L-stable",
                 limit == 0, "sympy-identity",
                 f"symbolic limit = {limit}\n" + "\n".join(rows))


def the_stiff_oscillation():
    """Part 3: the eight steps."""
    lam, h = -1e6, 0.1
    z = h * lam
    r = R_trap(z)
    y = 1.0
    values = []
    for _ in range(8):
        y = r * y
        values.append(y)
    exact = float(np.exp(lam * h))
    signs_alternate = all(values[i] * values[i + 1] < 0 for i in range(7))
    magnitude_stays = abs(values[-1]) > 0.999
    return check("the stiff mode oscillates at amplitude 1 instead of decaying",
                 signs_alternate and magnitude_stays and abs(r) < 1.0,
                 "witness",
                 f"z = {z:.0e}, R(z) = {r:.10f}\n"
                 + "y_n = " + ", ".join(f"{v:+.4f}" for v in values)
                 + f"\nexact e^(lambda h) = {exact:.3e} (zero to any precision)\n"
                   f"|R(z)| = {abs(r):.8f} < 1, so A-stability is NOT violated; "
                   "the transient is reflected, not damped")


def the_artefact_worsens_with_stiffness():
    rows = []
    ok = True
    previous = None
    for lam in (-1e2, -1e4, -1e6, -1e8):
        z = 0.1 * lam
        r = R_trap(z)
        steps_to_decay_by_e = int(np.ceil(-1.0 / np.log(abs(r)))) if abs(r) < 1 else -1
        rows.append(f"lambda = {lam:>8.0e}: R = {r:+.8f}, steps to decay by e: "
                    f"{steps_to_decay_by_e:,}")
        if previous is not None:
            ok = ok and steps_to_decay_by_e > previous
        previous = steps_to_decay_by_e
    return check("the spurious oscillation persists longer the stiffer the problem",
                 ok, "illustration", "\n".join(rows)
                 + "\nthe opposite of the usual intuition about stiffness")


def implicit_euler_kills_it_in_one_step():
    lam, h = -1e6, 0.1
    z = h * lam
    y_trap, y_be = 1.0, 1.0
    for _ in range(8):
        y_trap = R_trap(z) * y_trap
        y_be = (1.0 / (1.0 - z)) * y_be
    return check("implicit Euler annihilates the same transient",
                 abs(y_be) < 1e-30 and abs(y_trap) > 0.99, "illustration",
                 f"after 8 steps at z = {z:.0e}: trapezoidal {y_trap:+.4f}, "
                 f"implicit Euler {y_be:.3e}\n"
                 "the price is order: trapezoidal is 2nd order, implicit Euler 1st")


def orders_of_accuracy():
    """Confirm the order claim in Part 4 by measuring it."""
    lam = -1.0
    rows = []
    ok = True
    for name, step in (("trapezoidal", lambda z, y: R_trap(z) * y),
                       ("implicit Euler", lambda z, y: y / (1 - z))):
        errors = []
        for n in (100, 200, 400, 800):
            h = 1.0 / n
            y = 1.0
            for _ in range(n):
                y = step(h * lam, y)
            errors.append(abs(y - np.exp(lam)))
        order = float(np.polyfit(np.log([1.0 / n for n in (100, 200, 400, 800)]),
                                 np.log(errors), 1)[0])
        rows.append(f"{name:15s}: fitted order {order:.3f}")
        ok = ok and (abs(order - 2.0) < 0.1 if "trap" in name
                     else abs(order - 1.0) < 0.1)
    return check("trapezoidal is 2nd order, implicit Euler 1st",
                 ok, "illustration", "\n".join(rows)
                 + "\nL-stability costs an order, which is why TR-BDF2 exists")


CHECKS = [
    amplification_factor,
    region_is_exactly_the_left_half_plane,
    region_sampled_numerically,
    imaginary_axis_is_non_dissipative,
    limit_is_minus_one_not_zero,
    implicit_euler_is_l_stable,
    the_stiff_oscillation,
    the_artefact_worsens_with_stiffness,
    implicit_euler_kills_it_in_one_step,
    orders_of_accuracy,
]

if __name__ == "__main__":
    raise SystemExit(report(PROBLEM, run_checks(CHECKS)))
