#!/usr/bin/env python3
"""Verification for `eigenvectors-are-discontinuous-at-a-degenerate-eigenvalue`.

Part 2 is an existential claim settled by an exact witness, so the symbolic
checks here do establish it. The Davis-Kahan table in Part 4 is illustration.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from bench.verify_support import (check, report, run_checks,  # noqa: E402
                                  symbolically_zero)

PROBLEM = "eigenvectors-are-discontinuous-at-a-degenerate-eigenvalue"


def _top_eigenvector(m):
    w, v = np.linalg.eigh(m)
    return v[:, int(np.argmax(w))]


def perturbations_have_equal_norm():
    eps = sp.Symbol("epsilon", positive=True)
    b_minus_a = sp.diag(eps, -eps)
    c_minus_a = sp.Matrix([[0, eps], [eps, 0]])
    sv_b = sorted(b_minus_a.singular_values(), key=str)
    sv_c = sorted(c_minus_a.singular_values(), key=str)
    ok = all(symbolically_zero(s - eps) for s in sv_b + sv_c)
    return check("||B(eps) - I||_2 = ||C(eps) - I||_2 = eps exactly",
                 ok, "sympy-identity",
                 f"singular values of B - I: {[str(s) for s in sv_b]}; "
                 f"of C - I: {[str(s) for s in sv_c]}")


def spectra_are_identical():
    eps = sp.Symbol("epsilon", positive=True)
    b = sp.eye(2) + sp.diag(eps, -eps)
    c = sp.Matrix([[1, eps], [eps, 1]])
    spec_b = {sp.simplify(e) for e in b.eigenvals()}
    spec_c = {sp.simplify(e) for e in c.eigenvals()}
    return check("both families have spectrum {1+eps, 1-eps}",
                 spec_b == spec_c == {1 + eps, 1 - eps}, "sympy-identity",
                 f"spec(B) = {sorted(map(str, spec_b))}, "
                 f"spec(C) = {sorted(map(str, spec_c))}; "
                 "each eigenvalue moves by exactly ||E||_2, attaining Weyl")


def eigenvectors_are_constant_in_epsilon():
    eps = sp.Symbol("epsilon", positive=True)
    b = sp.eye(2) + sp.diag(eps, -eps)
    c = sp.Matrix([[1, eps], [eps, 1]])
    vb = b.eigenvects()
    vc = c.eigenvects()
    top_b = [v for (val, _, vs) in vb if symbolically_zero(val - (1 + eps)) for v in vs]
    top_c = [v for (val, _, vs) in vc if symbolically_zero(val - (1 + eps)) for v in vs]
    b_is_e1 = symbolically_zero(top_b[0].normalized() - sp.Matrix([1, 0]))
    c_is_diag = symbolically_zero(top_c[0].normalized()
                                  - sp.Matrix([1, 1]) / sp.sqrt(2))
    return check("top eigenvectors are e_1 and (1,1)/sqrt2 for every eps",
                 b_is_e1 and c_is_diag, "witness",
                 f"B: {top_b[0].T.tolist()} -> e_1;  "
                 f"C: {top_c[0].T.tolist()} -> (1,1)/sqrt(2)\n"
                 "both independent of eps, so the limit depends on the path")


def the_angle_is_exactly_45_degrees():
    rows = []
    ok = True
    for eps in (1e-2, 1e-4, 1e-6, 1e-8, 1e-12):
        b = np.eye(2) + np.diag([eps, -eps])
        c = np.array([[1.0, eps], [eps, 1.0]])
        vb, vc = _top_eigenvector(b), _top_eigenvector(c)
        overlap = abs(float(np.dot(vb, vc)))
        angle = np.degrees(np.arccos(min(overlap, 1.0)))
        rows.append(f"eps = {eps:.0e}: |<v_B, v_C>| = {overlap:.7f}, "
                    f"angle = {angle:.6f} deg")
        ok = ok and abs(angle - 45.0) < 1e-4
    return check("the two eigenvectors stay 45 degrees apart as eps -> 0",
                 ok, "witness", "\n".join(rows)
                 + "\nnot 0 and not 180, so this is not the sign ambiguity")


def every_unit_vector_is_a_limit_point():
    """Perturbing I by eps(2vv^T - I) gives top eigenvector v, for any v."""
    rng = np.random.default_rng(20260605)
    worst = 0.0
    for _ in range(50):
        theta = rng.uniform(0, np.pi)
        v = np.array([np.cos(theta), np.sin(theta)])
        eps = 1e-9
        m = np.eye(2) + eps * (2 * np.outer(v, v) - np.eye(2))
        got = _top_eigenvector(m)
        worst = max(worst, 1.0 - abs(float(np.dot(got, v))))
    return check("every unit vector arises as a limit of top eigenvectors",
                 worst < 1e-8, "witness",
                 f"over 50 random directions at eps = 1e-9, the worst "
                 f"1 - |<v_computed, v_target>| is {worst:.3e}\n"
                 "so the set of limit points is the entire unit circle")


def the_spectral_projector_is_continuous():
    """Part 3: what is continuous is the projector onto the cluster."""
    rows = []
    ok = True
    for eps in (1e-2, 1e-4, 1e-8):
        b = np.eye(2) + np.diag([eps, -eps])
        c = np.array([[1.0, eps], [eps, 1.0]])
        # the whole spectrum is the cluster, so the projector is I for both
        pb = sum(np.outer(v, v) for v in np.linalg.eigh(b)[1].T)
        pc = sum(np.outer(v, v) for v in np.linalg.eigh(c)[1].T)
        err = max(np.max(np.abs(pb - np.eye(2))), np.max(np.abs(pc - np.eye(2))))
        rows.append(f"eps = {eps:.0e}: ||P - I||_max = {err:.3e} for both families")
        ok = ok and err < 1e-12
    return check("the spectral projector of the cluster is continuous",
                 ok, "illustration", "\n".join(rows)
                 + "\nthe invariant subspace behaves; the individual eigenvectors "
                   "inside it do not")


def davis_kahan_gap_dependence():
    """Part 4: eigenvector sensitivity is governed by the eigenvalue gap."""
    rows = []
    ok = True
    norm_e = 1e-6
    for gap in (1e-1, 1e-3, 1e-5):
        a = np.diag([1.0 + gap, 1.0])
        e = norm_e * np.array([[0.0, 1.0], [1.0, 0.0]])
        va, vb = _top_eigenvector(a), _top_eigenvector(a + e)
        sin_theta = float(np.sqrt(max(0.0, 1.0 - np.dot(va, vb) ** 2)))
        predicted = norm_e / gap
        rows.append(f"gap = {gap:.0e}: sin(theta) = {sin_theta:.3e}, "
                    f"||E||/gap = {predicted:.3e}")
        ok = ok and sin_theta <= predicted * 1.5 + 1e-12
    return check("eigenvector perturbation is bounded by ||E|| / gap",
                 ok, "illustration", "\n".join(rows)
                 + "\nthe gap, not the eigenvalue condition number, governs the "
                   "eigenvector; for a symmetric matrix the latter is always 1")


def eigenvalues_themselves_are_well_behaved():
    """The contrast: the eigenvalues of both families converge identically."""
    rows = []
    ok = True
    for eps in (1e-2, 1e-6, 1e-10):
        b = np.eye(2) + np.diag([eps, -eps])
        c = np.array([[1.0, eps], [eps, 1.0]])
        wb = np.sort(np.linalg.eigvalsh(b))
        wc = np.sort(np.linalg.eigvalsh(c))
        diff = float(np.max(np.abs(wb - wc)))
        rows.append(f"eps = {eps:.0e}: spec(B) = {np.round(wb, 12)}, "
                    f"spec(C) = {np.round(wc, 12)}, difference {diff:.1e}")
        ok = ok and diff < 1e-14
    return check("the eigenvalues of the two families are identical",
                 ok, "illustration", "\n".join(rows)
                 + "\nsame matrices in the limit, same eigenvalues throughout, "
                   "eigenvectors 45 degrees apart")


CHECKS = [
    perturbations_have_equal_norm,
    spectra_are_identical,
    eigenvectors_are_constant_in_epsilon,
    the_angle_is_exactly_45_degrees,
    every_unit_vector_is_a_limit_point,
    the_spectral_projector_is_continuous,
    davis_kahan_gap_dependence,
    eigenvalues_themselves_are_well_behaved,
]

if __name__ == "__main__":
    raise SystemExit(report(PROBLEM, run_checks(CHECKS)))
