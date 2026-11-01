# Flawed solution: `search-proves-the-barrier`

## The submitted argument

> **Steps 1-2.** [Order conditions derived; the trapezoidal rule confirmed at
> order 2.]
>
> **Step 3.** To establish the barrier, search. For $k = 1,\dots,4$, sample the
> coefficient space on a grid of spacing $0.05$ in each of the $2k+1$ free
> parameters, keep the methods of order $\ge 3$, and test each for A-stability
> by checking the root condition at 2000 points $z$ in the left half-plane.
>
> **Step 4.** After $4\times10^{8}$ candidates, nothing of order $\ge 3$ is
> A-stable.
>
> **Step 5.** The second Dahlquist barrier is therefore established: no A-stable
> LMM has order above 2.

## Where it breaks

**Step 5.** Steps 3 and 4 describe a real and useful computation; Step 5 draws
from it a conclusion of a kind it cannot support.

The barrier is a **universal** statement over an uncountable coefficient space
and over all $k \ge 1$. A finite search establishes only "nothing was found in
the region searched, at the resolution searched".

Three independent gaps:

1. **Uncountability.** A grid of spacing $0.05$ meets a measure-zero subset of
   $\mathbb{R}^{2k+1}$. The barrier concerns every real coefficient vector,
   including every one between grid points.
2. **$k$ is unbounded.** $k \le 4$ says nothing about $k = 17$. The theorem has
   no largest $k$.
3. **The A-stability test is itself a sampled universal claim.** Checking 2000
   points $z$ can only fail to find instability. A method passing it may be
   unstable at an untested $z$: and the gaps can be thin: BDF3's stability
   region misses only a $3.97°$ sliver near the imaginary axis, which a grid
   concentrated on the negative real axis would not see.

Gap 3 is the one that persists even for a single candidate, and it has a fix:
A-stability of a *given* method is decidable by a Schur-Cohn or Routh-Hurwitz
test on $\rho(\zeta) - z\sigma(\zeta)$, which is exact and finite. Gaps 1 and 2
have no such fix.

## The direction the search does support

**Refutation.** A single candidate that is provably of order $\ge 3$ and
provably A-stable would disprove the barrier, and both halves of "provably" are
finite exact computations: the order conditions over the rationals, and an
algebraic root-location test. So the search is a valid *refutation* procedure
that happened to return nothing.

Reporting it as a proof inverts the only direction it has.

## What would be honest

> "A grid search over $k \le 4$ at resolution $0.05$, with A-stability tested
> at 2000 points in the left half-plane, produced no counterexample. This is
> consistent with the barrier and does not establish it; the theorem is
> Dahlquist (1963), proved via the order star of
> $\rho(\zeta) - z\sigma(\zeta)$."

## Failure mode

`finite-search-for-a-universal-claim`: an exhausted search is reported as a
proof, when its only valid output is a counterexample.
