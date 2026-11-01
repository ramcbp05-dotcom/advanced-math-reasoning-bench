#!/usr/bin/env python3
"""Verification for `hilbert-matrix-exponential-growth`.

Part 2 is checked in exact rational arithmetic, so those checks are proof of
what they assert about particular n. Part 3 fits a growth constant over
2 <= n <= 13, which is evidence and not proof: the asymptotic law is Szego's
theorem and is not established here.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from bench.verify_support import (check, report, run_checks,  # noqa: E402
                                  symbolically_zero)

PROBLEM = "hilbert-matrix-exponential-growth"
UNIT_ROUNDOFF = np.finfo(float).eps / 2
THEORETICAL_SLOPE = 4.0 * math.log(1.0 + math.sqrt(2.0))


def _hilbert_exact(n):
    return sp.Matrix(n, n, lambda i, j: sp.Rational(1, i + j + 1))


def _eigenvalues_high_precision(n, digits=60):
    """Eigenvalues of H_n from its exact rational entries, at `digits` precision.

    The entries are built as exact rationals and only then rounded to the
    working precision, so the matrix handed to the eigensolver is H_n to
    `digits` places rather than to 16. That is what lets the n = 13 point be
    meaningful; see Part 4 of solution.md.
    """
    with mp.workdps(digits):
        h = mp.matrix(n, n)
        for i in range(n):
            for j in range(n):
                h[i, j] = mp.mpf(1) / mp.mpf(i + j + 1)
        eigenvalues, _ = mp.eigsy(h)
        return sorted(float(v) for v in eigenvalues)


def _kappa_exact(n, digits=60):
    eig = _eigenvalues_high_precision(n, digits)
    return eig[-1] / eig[0]


def positive_definite_gram_identity():
    """c^T H c = integral of p^2, symbolically for n = 4."""
    n = 4
    x = sp.Symbol("x")
    c = sp.symbols(f"c1:{n + 1}", real=True)
    p = sum(c[k] * x ** k for k in range(n))
    integral = sp.integrate(sp.expand(p ** 2), (x, 0, 1))
    quadratic = sp.expand((sp.Matrix([c]) * _hilbert_exact(n) * sp.Matrix(c))[0])
    return check("c^T H_4 c equals the integral of p(x)^2 on [0,1]",
                 symbolically_zero(sp.expand(integral) - quadratic),
                 "sympy-identity",
                 "the Gram-matrix identity that makes H_n positive definite, "
                 "verified symbolically in the four coefficients")


def eigenvalues_are_positive():
    rows = []
    ok = True
    for n in (2, 4, 6, 8, 10):
        eig = _eigenvalues_high_precision(n)
        ok = ok and eig[0] > 0
        rows.append(f"n = {n:2d}: lambda_min = {eig[0]:.6e}, lambda_max = {eig[-1]:.6f}")
    return check("every eigenvalue of H_n is strictly positive",
                 ok, "illustration", "\n".join(rows))


def cauchy_determinant_formula():
    """det H_n = (prod_{k<n} k!)^4 / prod_{k<2n} k!, over the rationals."""
    rows = []
    ok = True
    for n in range(2, 9):
        direct = _hilbert_exact(n).det()
        cauchy = (sp.prod([sp.factorial(k) for k in range(1, n)]) ** 4
                  / sp.prod([sp.factorial(k) for k in range(1, 2 * n)]))
        ok = ok and symbolically_zero(direct - cauchy)
        if n in (4, 5, 8):
            rows.append(f"n = {n}: det = 1/{sp.denom(direct)}  "
                        f"(~{float(direct):.3e})")
    return check("Cauchy determinant formula, exactly for n = 2..8",
                 ok, "sympy-identity", "\n".join(rows))


def exact_determinant_of_h12():
    det = _hilbert_exact(12).det()
    return check("det H_12 computed exactly", det > 0, "witness",
                 f"det H_12 = 1/{sp.denom(det)}\n"
                 f"        ~ {float(det):.4e}, and strictly positive, so H_12 "
                 "is nonsingular despite the tiny determinant")


def small_determinant_does_not_mean_ill_conditioned():
    """The two-line disproof from the flawed solution, in exact arithmetic."""
    rows = []
    ok = True
    for n in (2, 6, 12, 40):
        a = sp.Rational(1, 2) * sp.eye(n)
        det = a.det()
        kappa = 1.0  # a scalar multiple of the identity
        ok = ok and det < sp.Rational(1, 2) and kappa == 1.0
        rows.append(f"n = {n:2d}: det((1/2)I) = 1/{sp.denom(det)}, kappa_2 = 1")
    return check("det -> 0 with kappa_2 identically 1", ok, "witness",
                 "\n".join(rows) + "\nso 'det -> 0' cannot imply ill-conditioning")


def inverse_entries_grow():
    rows = []
    previous = 0.0
    ok = True
    for n in (4, 5, 8, 12):
        inv = _hilbert_exact(n).inv()
        biggest = float(max(abs(v) for v in inv))
        ok = ok and biggest > previous
        previous = biggest
        rows.append(f"n = {n:2d}: max |(H^-1)_ij| = {biggest:.4e}")
    return check("entries of H_n^{-1} grow explosively", ok, "illustration",
                 "\n".join(rows) + "\nthis, not the determinant, is what "
                                   "ill-conditioning means")


def growth_constant_matches_the_asymptotic_law():
    """Evidence over a finite range, with the pre-asymptotic correction shown.

    The asymptotic law is kappa ~ C (1+sqrt2)^{4n} / sqrt(n), so

        ln kappa = 4 ln(1+sqrt2) n  -  (1/2) ln n  +  const.

    A plain linear fit absorbs the -(1/2) ln n term into the slope and therefore
    *underestimates* it. Both fits are reported, because the gap between them is
    the size of the pre-asymptotic effect and hiding it would make a weaker
    result look like a stronger one.
    """
    ns = list(range(2, 16))
    kappas = [_kappa_exact(n) for n in ns]
    n_arr = np.array(ns, dtype=float)
    log_k = np.log(kappas)

    slope_plain = float(np.polyfit(n_arr, log_k, 1)[0])
    slope_corrected = float(np.polyfit(n_arr, log_k + 0.5 * np.log(n_arr), 1)[0])

    off_plain = abs(slope_plain - THEORETICAL_SLOPE) / THEORETICAL_SLOPE
    off_corrected = abs(slope_corrected - THEORETICAL_SLOPE) / THEORETICAL_SLOPE

    rows = [f"n = {n:2d}: kappa_2 = {k:.4e}" for n, k in zip(ns, kappas)
            if n in (2, 4, 8, 12, 15)]
    return check("fitted growth constant over 2 <= n <= 15",
                 off_corrected < 0.005 and off_plain < 0.03, "illustration",
                 "\n".join(rows)
                 + f"\nplain fit of ln kappa vs n      : {slope_plain:.4f} "
                   f"({100 * off_plain:.2f}% below the asymptotic value)"
                 + f"\nfit of ln kappa + (1/2) ln n    : {slope_corrected:.4f} "
                   f"({100 * off_corrected:.2f}% from {THEORETICAL_SLOPE:.4f})"
                 + "\nthe gap between the two fits is the sqrt(n) factor in the "
                   "asymptotic law, not an error"
                 + "\nNOTE: fourteen points are consistent with the law; they do "
                   "not establish it.")


def successive_ratios_climb_towards_the_limit():
    """A sharper form of the same evidence: ln(kappa_{n+1}/kappa_n) -> 4ln(1+sqrt2).

    A fitted slope averages over the range and can hide a trend. The successive
    ratios show the approach directly, and monotone convergence towards the
    predicted limit is stronger evidence than a single fitted number.
    """
    ns = list(range(2, 16))
    kappas = [_kappa_exact(n) for n in ns]
    ratios = [math.log(kappas[i + 1] / kappas[i]) for i in range(len(ns) - 1)]

    increasing = all(b >= a - 1e-9 for a, b in zip(ratios, ratios[1:]))
    approaching = ratios[-1] < THEORETICAL_SLOPE and \
        abs(ratios[-1] - THEORETICAL_SLOPE) < abs(ratios[0] - THEORETICAL_SLOPE)

    rows = [f"n = {ns[i]:2d} -> {ns[i] + 1:2d}: ln(kappa ratio) = {r:.4f}"
            for i, r in enumerate(ratios) if ns[i] in (2, 4, 8, 11, 14)]
    return check("successive ratios increase towards 4 ln(1+sqrt2)",
                 increasing and approaching, "illustration",
                 "\n".join(rows)
                 + f"\nlimit predicted by the asymptotic law: {THEORETICAL_SLOPE:.4f}"
                 + f"\nmonotone increasing: {increasing}; still "
                   f"{THEORETICAL_SLOPE - ratios[-1]:.4f} short at n = 14, which "
                   "is the 1/(2n) correction")


def double_precision_measurement_saturates():
    """The failure in `double-precision-measurement-of-kappa`, reproduced."""
    ns = list(range(2, 21))
    float_kappa = []
    for n in ns:
        h = np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)])
        float_kappa.append(np.linalg.cond(h, 2))
    slope_all = np.polyfit(ns, np.log(float_kappa), 1)[0]
    slope_safe = np.polyfit(ns[:12], np.log(float_kappa[:12]), 1)[0]
    saturated = [k for n, k in zip(ns, float_kappa) if n >= 15]
    spread = max(saturated) / min(saturated)
    return check("float64 kappa saturates near 1/u and corrupts the fit",
                 slope_all < 0.8 * THEORETICAL_SLOPE and spread < 1e3,
                 "witness",
                 f"fit over n = 2..20 in float64 gives slope {slope_all:.3f}; "
                 f"restricting to n = 2..13 gives {slope_safe:.3f}\n"
                 f"for n >= 15 the computed kappa only varies by a factor of "
                 f"{spread:.1f} (it has saturated at ~1/u = {1 / UNIT_ROUNDOFF:.2e})\n"
                 "so the low slope is an artefact of the arithmetic")


def digits_lost_in_a_double_precision_solve():
    rows = []
    ok = True
    for n in (6, 8, 10, 12):
        kappa = _kappa_exact(n)
        predicted = UNIT_ROUNDOFF * kappa
        h = np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)])
        x_exact = np.ones(n)
        b = h @ x_exact
        x_hat = np.linalg.solve(h, b)
        observed = np.linalg.norm(x_hat - x_exact, np.inf)
        rows.append(f"n = {n:2d}: u*kappa = {predicted:.2e}, "
                    f"observed error = {observed:.2e}")
        ok = ok and observed <= max(predicted * 50, 1e-12)
    return check("double-precision solve loses u*kappa (Part 4)",
                 ok, "illustration",
                 "\n".join(rows) + "\nat n = 12 the last digit is gone")


CHECKS = [
    positive_definite_gram_identity,
    eigenvalues_are_positive,
    cauchy_determinant_formula,
    exact_determinant_of_h12,
    small_determinant_does_not_mean_ill_conditioned,
    inverse_entries_grow,
    growth_constant_matches_the_asymptotic_law,
    successive_ratios_climb_towards_the_limit,
    double_precision_measurement_saturates,
    digits_lost_in_a_double_precision_solve,
]

if __name__ == "__main__":
    raise SystemExit(report(PROBLEM, run_checks(CHECKS)))
