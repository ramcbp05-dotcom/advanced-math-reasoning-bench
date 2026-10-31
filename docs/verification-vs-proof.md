# Verification is not proof

This repository keeps two things in separate files on purpose. `solution.md`
carries the **argument**; `verify.py` carries **evidence at instances**. The
distinction is enforced by the harness, not left to taste, because it is the
single easiest thing to lose.

## The asymmetry

| claim | can computation settle it? |
|---|---|
| **universal** — "for every matrix A, ..." | **No.** Finitely many instances, however many, do not cover a continuum. The check can only fail to contradict. |
| **existential** — "there is an A for which ..." | **Yes**, if the witness is exact. One counterexample refutes a universal claim outright. |

So `bench/verify_support.py` tags every check with a `role`:

* `illustration` — sampled evidence; the proof is elsewhere;
* `witness` — an exact counterexample, which *does* settle its claim;
* `sympy-identity` — a symbolic identity, settled for the symbols quantified;
* `consistency` — arithmetic internal to the repository.

Every `verify.py` prints the disclaimer before its results. The integrity tests
require it.

## Three traps this repository actually fell into

**1. `simplify(e) == 0` is not a zero test.** For

```
e = (mu**2 - mu*t**2 - 2*mu + 1) - (mu**2 - (2 + t**2)*mu + 1)
```

SymPy's `simplify` returns the unevaluated
`-mu**2 + mu*t**2 + 2*mu + mu**2 - mu*t**2 - 2*mu`, so `== 0` is False although
the expression vanishes identically. `expand` settles it immediately.
`symbolically_zero()` tries three routes. **A CAS failing to show that
something is zero is not evidence that it is nonzero.**

**2. Two expressions that print identically need not be equal.**
`Matrix.charpoly(mu).as_expr()` returns the polynomial in an internal `Dummy`
that *prints* as `mu` and is a different object. Subtracting the expected
polynomial gives a visibly-cancelling sum that does not cancel. Printed output
is not an identity check.

**3. A measurement can saturate.** Fitting the Hilbert condition number over
`n = 2..20` in float64 gives a growth constant of 2.35 against the theoretical
3.53 — because `kappa` saturates at `1/u` beyond `n ~ 13` and the saturated
points drag the fit down. The first draft of that problem reported 0.15 %
agreement from eigenvalues that had silently saturated. The honest figure,
from 60-digit arithmetic, is 1.77 % for a plain fit and 0.22 % once the
`sqrt(n)` term in the asymptotic law is accounted for.

**An agreement that is too good deserves as much suspicion as one that is too
bad.**

## What a flawed solution records

Each problem ships two `flawed/*.md` files. Each names the **exact step** where
the reasoning fails, classifies the failure, and — where the flawed answer
happens to be *numerically correct* — says so, because that is the case a
reviewer waves through.

Recurring failure modes across the collection:

* `missing-hypothesis` / `wrong-hypothesis` — a theorem about normal matrices
  applied to general ones; diagonalisability substituted for normality;
* `bound-reported-as-estimate` — `<=` read as `~`;
* `inequality-reported-as-equality` — the half of the claim with the content
  silently dropped;
* `continuity-is-not-conditioning` — a qualitative property used where a
  quantitative one is needed;
* `finite-horizon-mistaken-for-asymptotics` — an integration to `t = 5` on a
  problem whose blow-up time is 50;
* `measurement-beyond-precision` — a quantity measured in arithmetic that
  cannot represent it.

## Setting a tolerance

Where a threshold decides pass from fail, it is set from measurement and the
measurement is recorded next to it. Examples in this repository:

* `kappa(A^T A) = kappa(A)^2` is checked at `1e-5`, not `1e-12`, because
  computing `kappa` of the Gram matrix is itself accurate only to
  `u * kappa(A^T A)`;
* the Welford-vs-sum-of-squares variance bounds come from a measured table of
  relative error against condition number;
* the Weyl check perturbs by `1e-10`, not `1e-16`, because at `1e-16` the
  perturbation is the same size as the eigensolver's own backward error and the
  measurement would be of LAPACK rather than of the theorem.

Demanding more accuracy than the arithmetic can deliver turns a correct
implementation into a failing test. Demanding less turns a verification suite
into decoration.
