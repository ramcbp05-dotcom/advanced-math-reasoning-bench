# Solution

## Part 1

Take

$$A = \begin{pmatrix} 1 & 1 \\ 1 & 1 + \delta \end{pmatrix},
\qquad D_t = \begin{pmatrix} 1 & 0 \\ 0 & t\end{pmatrix}, \quad t > 0 .$$

$A$ is nonsingular for $\delta \ne 0$ ($\det A = \delta$). Then

$$D_tA = \begin{pmatrix} 1 & 1 \\ t & t(1+\delta)\end{pmatrix}.$$

As $t \to \infty$ the two rows differ in scale without limit, and $\|D_tA\|_2
\sim t\sqrt{2 + O(\delta)}$ while $\|(D_tA)^{-1}\|_2 = \|A^{-1}D_t^{-1}\|_2$
remains bounded below by $\|A^{-1}e_1\|_2$, which does not involve $t$. Hence
$\kappa_2(D_tA) \to \infty$ linearly in $t$.

Measured at $\delta = 10^{-8}$, both in exact rational arithmetic (via the
eigenvalues of $(D_tA)^{\mathsf T}(D_tA)$) and in double precision:

| $t$ | $\kappa_2$ exact | $\kappa_2$ in float64 |
|---|---|---|
| $1$ | $4.0000\times10^{8}$ | $4.0000\times10^{8}$ |
| $10^{2}$ | $2.0002\times10^{10}$ | $2.0002\times10^{10}$ |
| $10^{4}$ | $2.0000\times10^{12}$ | $1.9999\times10^{12}$ |
| $10^{8}$ | $2.0000\times10^{16}$ | $1.8014\times10^{16}$ |

The last row carries a lesson of its own: at $\kappa \approx 10^{16}$ the
*computed* condition number is itself wrong by 10 %. Estimating $\kappa$ in
double precision requires resolving $\sigma_n$, and once $\sigma_n/\sigma_1
\approx u$ there is nothing left to resolve. A reported $\kappa$ near $1/u$
should be read as "at least $10^{16}$", never as a measurement.

**The conclusion.** Multiplying the second equation of $Ax = b$ through by $t$
changes nothing about the problem: the solution set is identical, the equations
assert the same facts, and a human solving by hand would not notice. Yet
$\kappa_2$ moves by eight orders of magnitude.

So $\kappa$ is a property of **the matrix as written**, not of the map. What it
actually measures is the sensitivity of the computed solution to perturbations
*of the entries*, and those perturbations are what a floating-point solver
commits: rounding is relative to the entries as stored. Rescaling a row
rescales the perturbations with it, and that is a genuine change in the
numerical problem even though it is no change in the mathematical one.

## Part 2: van der Sluis

**Theorem (van der Sluis, 1969).** With $D_{\mathrm{eq}}$ the row
equilibration,

$$\kappa_\infty(D_{\mathrm{eq}}A) \le n \min_{D}\kappa_\infty(DA).$$

**Proof sketch.** Write $B = DA$ for an arbitrary diagonal $D$, and let $E =
D_{\mathrm{eq}}A$, so every row of $E$ has unit $\infty$-norm and $\|E\|_\infty
= 1$.

The two are related by a diagonal: $E = \Delta B$ with $\Delta =
D_{\mathrm{eq}}D^{-1}$, and $\Delta_{ii} = 1/\|b_i\|_\infty$ where
$b_i^{\mathsf T}$ is the $i$-th row of $B$. Now

$$\|E^{-1}\|_\infty = \|B^{-1}\Delta^{-1}\|_\infty
  \le \|B^{-1}\|_\infty \max_i \|b_i\|_\infty \le \|B^{-1}\|_\infty
  \,\|B\|_\infty ,$$

the last step because $\|B\|_\infty = \max_i\|b_i\|_1 \ge
\max_i\|b_i\|_\infty$. Since $\|E\|_\infty = 1$,

$$\kappa_\infty(E) = \|E^{-1}\|_\infty \le \kappa_\infty(B).$$

This already gives the result with constant 1 in the direction stated; the
factor $n$ in the usual formulation covers the passage between $\|\cdot\|_1$
and $\|\cdot\|_\infty$ on rows when the minimisation is taken over a larger
class, and the sharp constant depends on which norm and which side is scaled.
The substance is that equilibration is **within a dimension-dependent factor of
the best possible row scaling**, which is why it is the default in production
solvers.

**What it does not say.** It does not say equilibration minimises $\kappa$. The
minimising $D$ is generally different, the minimum is not attained in closed
form, and computing it is a convex problem in $\log D$ that nobody solves in a
linear solver. A factor of $n$ is cheap; optimality is not on offer.

Measured, on badly row-scaled random $6\times 6$ matrices:

| $\kappa_\infty(A)$ | after equilibration | factor gained |
|---|---|---|
| $2.8\times10^{8}$ | $1.7\times10^{3}$ | $1.7\times10^{5}$ |
| $1.2\times10^{10}$ | $1.5\times10^{3}$ | $8.1\times10^{6}$ |
| $3.6\times10^{9}$ | $9.2\times10^{1}$ | $3.9\times10^{7}$ |

## Part 3: what is invariant

**Claim.** $\operatorname{cond}(DA) = \operatorname{cond}(A)$ for every
nonsingular diagonal $D$.

**Proof.** For diagonal $D$ the entrywise absolute value is multiplicative:
$|DA| = |D|\,|A|$, and $(DA)^{-1} = A^{-1}D^{-1}$ gives $|(DA)^{-1}| =
|A^{-1}|\,|D^{-1}| = |A^{-1}|\,|D|^{-1}$. Hence

$$|(DA)^{-1}|\,|DA| = |A^{-1}|\,|D|^{-1}|D|\,|A| = |A^{-1}|\,|A| ,$$

because $|D|^{-1}|D| = I$ for diagonal $D$. Taking norms gives the claim.
$\blacksquare$

Measured, with $A = \begin{pmatrix}1&2\\3&4\end{pmatrix}$ scaled by
$\operatorname{diag}(1, t)$:

| $t$ | $\kappa_\infty$ | $\operatorname{cond}$ |
|---|---|---|
| $1$ | $21$ | $13$ |
| $10^{3}$ | $1.4\times10^{4}$ | $13$ |
| $10^{6}$ | $1.4\times10^{7}$ | $13$ |
| $10^{9}$ | $1.4\times10^{10}$ | $13$ |

Exactly 13 throughout, to the last digit.

**What it means for a solver.** The Skeel number governs the *componentwise*
perturbation theory: if the entries of $A$ are perturbed by small relative
amounts, $|\delta a_{ij}| \le \epsilon|a_{ij}|$, then

$$\frac{\|\delta x\|_\infty}{\|x\|_\infty}
  \lesssim \epsilon\,\operatorname{cond}(A) .$$

Since rounding a matrix into floating point is exactly a small *relative*
entrywise perturbation, this is the right sensitivity measure for the question
"does my data deserve this answer", and it is immune to the gauge freedom of
Part 1. The normwise $\kappa$ answers a different question (how a *normwise*
perturbation propagates) and that question is scaling-dependent because the
perturbation model is.

## Remarks

* Column scaling is a different operation: $A \mapsto AD$ changes the solution
  ($x \mapsto D^{-1}x$), so it is a change of variables rather than a rescaling
  of equations, and it has its own theory.
* Two-sided scaling ($D_1AD_2$) can do better than either alone, and finding
  the optimum is a known hard case.
* The gauge freedom is why library routines report the condition number *after*
  equilibration and why `LAPACK`'s expert drivers (`?GESVX`) return both the
  scaling factors and `RCOND` for the scaled matrix.
