#!/usr/bin/env python3
"""Verification for `eigenvalues-do-not-determine-the-condition-number`."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from bench.verify_support import (check, random_matrix, relative_error,  # noqa: E402
                                  report, run_checks, symbolically_zero)

PROBLEM = "eigenvalues-do-not-determine-the-condition-number"


def normal_matrices_satisfy_the_identity():
    rng = np.random.default_rng(20260506)
    worst = 0.0
    for n in (2, 4, 6, 8):
        for _ in range(25):
            a = random_matrix(rng, n, kind="normal")
            if np.linalg.cond(a, 2) > 1e8:
                continue
            assert np.max(np.abs(a.conj().T @ a - a @ a.conj().T)) < 1e-10
            eig = np.abs(np.linalg.eigvals(a))
            worst = max(worst, relative_error(np.linalg.cond(a, 2),
                                              eig.max() / eig.min()))
    return check("kappa_2 = |lambda_max|/|lambda_min| for normal A",
                 worst < 1e-9, "illustration",
                 f"worst relative deviation over 100 normal matrices: {worst:.3e}")


def hermitian_case():
    rng = np.random.default_rng(2)
    worst = 0.0
    for n in (3, 7, 12):
        for _ in range(20):
            a = random_matrix(rng, n, kind="symmetric")
            if np.linalg.cond(a, 2) > 1e8:
                continue
            eig = np.abs(np.linalg.eigvalsh(a))
            worst = max(worst, relative_error(np.linalg.cond(a, 2),
                                              eig.max() / eig.min()))
    return check("the identity holds for Hermitian A (a normal subclass)",
                 worst < 1e-10, "illustration",
                 f"worst relative deviation: {worst:.3e}")


def exact_singular_values_of_the_shear():
    """Closed form: kappa_2 = (2 + t^2 + t sqrt(t^2+4))/2, exactly.

    Verified by showing the closed form is a root of the characteristic
    polynomial of A^T A, and that the product of the two roots is 1 (so the
    larger root *is* kappa_2, because sigma_+ sigma_- = |det A| = 1).
    SymPy will not flatten the nested radical directly, so the identity is
    checked in the polynomial rather than in the radical.

    One implementation note worth recording, because it is the kind of thing
    this benchmark exists to catch. ``Matrix.charpoly(mu).as_expr()`` returns the
    polynomial in an internal **Dummy** symbol that *prints* as ``mu`` but is not
    the ``mu`` passed in. Subtracting the expected polynomial therefore gives an
    expression that displays as an obviously cancelling sum and does not cancel,
    because the two ``mu``s are different objects. The determinant form
    ``det(mu I - G)`` has no such ambiguity and is used instead. Two expressions
    printing identically is not evidence that they are equal.
    """
    t, mu = sp.symbols("t mu", positive=True)
    a = sp.Matrix([[1, t], [0, 1]])
    gram = sp.expand(a.T * a)

    char = sp.expand((mu * sp.eye(2) - gram).det())
    expected_char = sp.expand(mu ** 2 - (2 + t ** 2) * mu + 1)
    char_ok = symbolically_zero(char - expected_char)

    closed = (2 + t ** 2 + t * sp.sqrt(t ** 2 + 4)) / 2
    root_ok = symbolically_zero(char.subs(mu, closed))

    # product of roots = constant term = 1 = |det A|^2, so sigma_+ sigma_- = 1
    product_ok = symbolically_zero(gram.det() - 1)

    rows = []
    for exponent in (2, 4, 6):
        tv = sp.Integer(10) ** exponent
        value = float(closed.subs(t, tv))
        rows.append(f"t = 1e{exponent}: kappa_2 = {value:.6e}, "
                    f"t^2 = {float(tv ** 2):.1e}, ratio = {value / float(tv) ** 2:.6f}")

    return check("exact kappa_2 of the shear equals the closed form",
                 char_ok and root_ok and product_ok, "sympy-identity",
                 f"char poly of A^T A is mu^2 - (2+t^2)mu + 1: {char_ok}\n"
                 f"the closed form is a root of it: {root_ok}\n"
                 f"det(A^T A) = 1, so sigma_+ sigma_- = 1 and kappa_2 = sigma_+^2: "
                 f"{product_ok}\n" + "\n".join(rows))


def witness_spectrum_is_a_single_point():
    """Both eigenvalues exactly 1 for every t -- checked over the rationals."""
    t = sp.Symbol("t")
    a = sp.Matrix([[1, t], [0, 1]])
    char = sp.factor(a.charpoly(sp.Symbol("x")).as_expr())
    eigen = a.eigenvals()
    ok = list(eigen) == [sp.Integer(1)] and eigen[sp.Integer(1)] == 2
    return check("spec(A_t) = {1} with multiplicity 2, for every t",
                 ok, "witness",
                 f"characteristic polynomial factors as {char}; "
                 f"eigenvalues {dict(eigen)}\n"
                 "so |lambda_max|/|lambda_min| = 1 identically while kappa_2 ~ t^2")


def witness_numerically():
    rows = []
    ok = True
    for t in (1e2, 1e4, 1e6):
        a = np.array([[1.0, t], [0.0, 1.0]])
        eig = np.abs(np.linalg.eigvals(a))
        kappa = np.linalg.cond(a, 2)
        rows.append(f"t = {t:.0e}: eigenvalue ratio = {eig.max() / eig.min():.6f}, "
                    f"kappa_2 = {kappa:.4e}")
        ok = ok and abs(eig.max() / eig.min() - 1.0) < 1e-9 and kappa > 0.9 * t ** 2
    return check("eigenvalue ratio pinned at 1 while kappa_2 ~ t^2",
                 ok, "illustration", "\n".join(rows))


def diagonalisable_version_of_the_witness():
    """The error survives repairing defectiveness: distinct eigenvalues, same growth."""
    rows = []
    ok = True
    for t in (1e2, 1e4, 1e6):
        a = np.array([[1.0, t], [0.0, 2.0]])
        eig = np.abs(np.linalg.eigvals(a))
        kappa = np.linalg.cond(a, 2)
        rows.append(f"t = {t:.0e}: eigenvalue ratio = {eig.max() / eig.min():.4f}, "
                    f"kappa_2 = {kappa:.4e}")
        ok = ok and abs(eig.max() / eig.min() - 2.0) < 1e-9 and kappa > 0.1 * t ** 2
    return check("a diagonalisable witness with eigenvalue ratio fixed at 2",
                 ok, "witness", "\n".join(rows)
                 + "\nso the gap is not an artefact of defectiveness")


def the_sandwich_holds():
    """|l1|/|ln| <= kappa_2(A) <= kappa_2(V)^2 |l1|/|ln| (Part 3)."""
    rng = np.random.default_rng(20260507)
    violations = 0
    worst_slack = 0.0
    for n in (2, 3, 5):
        for _ in range(60):
            a = random_matrix(rng, n)
            eigvals, v = np.linalg.eig(a)
            if np.linalg.cond(v) > 1e10 or np.min(np.abs(eigvals)) < 1e-8:
                continue
            ratio = np.max(np.abs(eigvals)) / np.min(np.abs(eigvals))
            kappa = np.linalg.cond(a, 2)
            upper = np.linalg.cond(v, 2) ** 2 * ratio
            if not (ratio <= kappa * (1 + 1e-8) and kappa <= upper * (1 + 1e-8)):
                violations += 1
            worst_slack = max(worst_slack, upper / kappa)
    return check("the sandwich is never violated over 180 random matrices",
                 violations == 0, "illustration",
                 f"violations: {violations}; the upper bound is loose by up to "
                 f"{worst_slack:.2e}x, which is kappa_2(V)^2 doing the work")


def kappa_of_v_is_the_missing_quantity():
    """kappa_2(V) = 1 exactly when the identity of Part 1 is tight."""
    rng = np.random.default_rng(5)
    rows = []
    ok = True
    for kind, label in (("symmetric", "symmetric (normal)"), ("general", "general")):
        a = random_matrix(rng, 5, kind=kind)
        eigvals, v = np.linalg.eig(a)
        ratio = np.max(np.abs(eigvals)) / np.min(np.abs(eigvals))
        gap = np.linalg.cond(a, 2) / ratio
        rows.append(f"{label:20s}: kappa_2(V) = {np.linalg.cond(v, 2):.4e}, "
                    f"kappa_2(A)/eigenvalue ratio = {gap:.4e}")
        if kind == "symmetric":
            ok = ok and abs(gap - 1.0) < 1e-8
    return check("kappa_2(V) is exactly what the eigenvalue ratio is missing",
                 ok, "illustration", "\n".join(rows))


CHECKS = [
    normal_matrices_satisfy_the_identity,
    hermitian_case,
    exact_singular_values_of_the_shear,
    witness_spectrum_is_a_single_point,
    witness_numerically,
    diagonalisable_version_of_the_witness,
    the_sandwich_holds,
    kappa_of_v_is_the_missing_quantity,
]

if __name__ == "__main__":
    raise SystemExit(report(PROBLEM, run_checks(CHECKS)))
