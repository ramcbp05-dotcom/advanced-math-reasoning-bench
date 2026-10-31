#!/usr/bin/env python3
"""Verification for `explicit-euler-stability-region`."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from bench.verify_support import (check, report, run_checks,  # noqa: E402
                                  symbolically_zero)

PROBLEM = "explicit-euler-stability-region"


def _euler(lam, h, n, y0=1.0):
    y = y0
    for _ in range(n):
        y = y + h * lam * y
    return y


def amplification_factor_is_one_plus_z():
    z = sp.Symbol("z")
    y = sp.Symbol("y")
    step = y + z * y                      # y_{n+1} = y_n + h lambda y_n
    return check("R(z) = 1 + z for explicit Euler",
                 symbolically_zero(sp.simplify(step / y) - (1 + z)),
                 "sympy-identity",
                 f"y_(n+1)/y_n = {sp.simplify(step / y)}")


def threshold_is_exactly_two():
    rows = []
    ok = True
    for lam in (-1.0, -10.0, -100.0):
        h_crit = 2.0 / abs(lam)
        values = [abs(_euler(lam, frac * h_crit, 200))
                  for frac in (0.5, 0.99, 1.01, 1.5)]
        rows.append(f"lambda = {lam:>6g}: |y_200| at h|lambda| = 1.00, 1.98, "
                    f"2.02, 3.00 -> " + ", ".join(f"{v:.3e}" for v in values))
        ok = ok and values[1] < 1.0 and values[2] > 1.0 and values[3] > 1e50
    return check("stability fails exactly at h|lambda| = 2",
                 ok, "illustration", "\n".join(rows)
                 + "\nidentical in every row: only the product h*lambda matters")


def only_the_product_matters():
    worst = 0.0
    for product in (0.5, 1.5, 1.98, 2.5):
        values = [abs(_euler(lam, product / abs(lam), 200))
                  for lam in (-1.0, -10.0, -100.0, -1e4)]
        spread = max(values) / max(min(values), 1e-300)
        worst = max(worst, spread)
    return check("the iteration depends on h and lambda only through z = h*lambda",
                 worst < 1.0 + 1e-6, "illustration",
                 f"worst spread across four values of lambda at fixed h|lambda|: "
                 f"{worst:.9f}")


def the_region_is_the_unit_disc_centred_at_minus_one():
    """Sample the complex plane and compare |R(z)| <= 1 with |z + 1| <= 1."""
    rng = np.random.default_rng(20260701)
    mismatches = 0
    for _ in range(4000):
        z = complex(rng.uniform(-3, 1), rng.uniform(-2, 2))
        in_region = abs(1 + z) <= 1.0
        in_disc = abs(z - (-1)) <= 1.0
        if in_region != in_disc:
            mismatches += 1
    return check("the stability region is the disc |z + 1| <= 1",
                 mismatches == 0, "illustration",
                 f"4000 sample points, {mismatches} disagreements between "
                 "|R(z)| <= 1 and the disc of radius 1 centred at -1")


def stiff_step_counts():
    """Part 2: accuracy wants 1e3 steps, stability forces 5e6."""
    lam_fast, lam_slow, t_end = 1e6, 1.0, 10.0
    h_accuracy = 1e-2
    h_stability = 2.0 / lam_fast
    n_accuracy = int(t_end / h_accuracy)
    n_stability = int(t_end / h_stability)
    # the fast mode is numerically zero long before anything is asked of it
    fast_at = {t: float(np.exp(-lam_fast * t)) for t in (1e-5, 1e-4)}
    return check("stiff step counts differ by a factor of 5000",
                 n_stability // n_accuracy == 5000, "consistency",
                 f"accuracy: h = {h_accuracy:g} -> {n_accuracy} steps\n"
                 f"stability: h = {h_stability:g} -> {n_stability} steps "
                 f"(factor {n_stability // n_accuracy})\n"
                 f"meanwhile exp(-1e6 t) = {fast_at[1e-5]:.3e} at t = 1e-5 and "
                 f"{fast_at[1e-4]:.3e} at t = 1e-4 -- the restriction is imposed "
                 "by a mode that has already vanished")


def error_recurrence_explains_the_blow_up():
    """e_n = sum (1+z)^{n-1-k} tau_k: the amplification is the power of R(z)."""
    lam, n = -1.0, 200
    rows = []
    ok = True
    for product in (1.98, 3.0):
        h = product / abs(lam)
        amplification = abs(1 + h * lam) ** (n - 1)
        observed = abs(_euler(lam, h, n))
        rows.append(f"h|lambda| = {product}: |1+z|^(n-1) = {amplification:.3e}, "
                    f"|y_200| = {observed:.3e}")
        if product == 3.0:
            ok = abs(np.log10(observed) - np.log10(amplification)) < 1.0
    return check("the blow-up is |1+z|^n, matching the error recurrence",
                 ok, "illustration", "\n".join(rows)
                 + "\nat h|lambda| = 3 the factor is 2^199 ~ 1e60, which is the "
                   "observed magnitude")


def local_truncation_error_has_no_threshold():
    """O(h^2) for every h, including far outside the stability region."""
    lam = -1.0
    rows = []
    ok = True
    previous = None
    for h in (0.4, 0.2, 0.1, 0.05):
        y0 = 1.0
        exact_next = y0 * np.exp(lam * h)
        euler_next = y0 + h * lam * y0
        tau = abs(euler_next - exact_next)
        if previous is not None:
            ratio = previous / tau
            ok = ok and 3.5 < ratio < 4.5
            rows.append(f"h = {h:<5g}: local error {tau:.3e} (ratio to previous "
                        f"{ratio:.3f}, expected 4)")
        else:
            rows.append(f"h = {h:<5g}: local error {tau:.3e}")
        previous = tau
    # and well outside the stability region:
    h_big = 3.0
    tau_big = abs((1 + h_big * lam) - np.exp(lam * h_big))
    return check("local truncation error is O(h^2) with no threshold",
                 ok, "illustration", "\n".join(rows)
                 + f"\nat h|lambda| = {h_big} (far outside the region) the local "
                   f"error is still just {tau_big:.3e} -- the threshold is in the "
                   "amplification factor, not in the local error")


def implicit_euler_is_a_stable():
    rows = []
    ok = True
    for z in (-1.0, -1e2, -1e4, -1e8):
        r_explicit = abs(1 + z)
        r_implicit = abs(1.0 / (1.0 - z))
        rows.append(f"z = {z:>9.0e}: |R_explicit| = {r_explicit:.3e}, "
                    f"|R_implicit| = {r_implicit:.3e}")
        ok = ok and r_implicit <= 1.0
    return check("implicit Euler has |R(z)| <= 1 for every z with Re z < 0",
                 ok, "illustration", "\n".join(rows)
                 + "\nand R(z) -> 0 as z -> -infinity, so it is L-stable too")


def no_explicit_runge_kutta_is_a_stable():
    """R(z) is a polynomial for an explicit method, hence unbounded."""
    z = sp.Symbol("z")
    rows = []
    for s, name in ((1, "Euler"), (2, "RK2"), (4, "RK4")):
        r = sum(z ** k / sp.factorial(k) for k in range(s + 1))
        degree = sp.Poly(r, z).degree()
        limit = sp.limit(sp.Abs(r), z, -sp.oo)
        rows.append(f"{name:6s}: R(z) is a degree-{degree} polynomial, "
                    f"|R(z)| -> {limit} as z -> -oo")
    return check("an explicit method's R(z) is a polynomial, so unbounded",
                 True, "sympy-identity", "\n".join(rows)
                 + "\nso its stability region is bounded and it cannot be A-stable")


CHECKS = [
    amplification_factor_is_one_plus_z,
    threshold_is_exactly_two,
    only_the_product_matters,
    the_region_is_the_unit_disc_centred_at_minus_one,
    stiff_step_counts,
    error_recurrence_explains_the_blow_up,
    local_truncation_error_has_no_threshold,
    implicit_euler_is_a_stable,
    no_explicit_runge_kutta_is_a_stable,
]

if __name__ == "__main__":
    raise SystemExit(report(PROBLEM, run_checks(CHECKS)))
