# Solution

## Part 1: proof

If $\mu \in \operatorname{spec}(A)$ the left side is 0 and there is nothing to
prove. So assume $\mu \notin \operatorname{spec}(A)$; then $\mu I - \Lambda$ is
invertible.

Since $\mu$ is an eigenvalue of $A + E$, the matrix $\mu I - A - E$ is
singular. Write

$$\mu I - A - E = V(\mu I - \Lambda)V^{-1} - E
  = V(\mu I - \Lambda)\Big[I - (\mu I - \Lambda)^{-1}V^{-1}EV\Big]V^{-1}.$$

$V$ and $\mu I - \Lambda$ are invertible, so the bracketed factor must be
singular. Hence there is a unit vector $z$ with

$$z = (\mu I - \Lambda)^{-1}V^{-1}EVz ,$$

and taking norms,

$$1 = \|z\|_2 \le \|(\mu I - \Lambda)^{-1}\|_2\,\|V^{-1}\|_2\,\|E\|_2\,\|V\|_2
      = \frac{\kappa_2(V)\,\|E\|_2}{\min_i|\mu - \lambda_i|},$$

using that $(\mu I-\Lambda)^{-1}$ is diagonal with entries
$(\mu-\lambda_i)^{-1}$, so its 2-norm is $1/\min_i|\mu - \lambda_i|$.
Rearranging gives the theorem. $\blacksquare$

**Note on $\kappa_2(V)$.** $V$ is determined only up to column scaling, and
$\kappa_2(V)$ depends on that scaling; the sharp statement takes the infimum
over admissible $V$. This is the same gauge freedom as in
`row-scaling-changes-the-condition-number`, and the usual convention is unit
columns.

For **normal** $A$, $V$ may be taken unitary, $\kappa_2(V) = 1$, and the
theorem reduces to the statement behind
`hermitian-eigenvalues-are-perfectly-conditioned`.

## Part 2: sharpness

Take

$$A = \begin{pmatrix}1 & t\\ 0 & 2\end{pmatrix},
\qquad E = \delta\begin{pmatrix}0 & 0\\ 1 & 0\end{pmatrix}.$$

$A$ is diagonalisable (distinct eigenvalues 1, 2) with $\kappa_2(V) \approx
2t$. Measured at $\delta = 10^{-10}$:

| $t$ | $\kappa_2(V)$ | bound $\kappa_2(V)\delta$ | measured shift | ratio |
|---|---|---|---|---|
| $10^{2}$ | $2.0\times10^{2}$ | $2.0\times10^{-8}$ | $1.0\times10^{-8}$ | 0.50 |
| $10^{4}$ | $2.0\times10^{4}$ | $2.0\times10^{-6}$ | $1.0\times10^{-6}$ | 0.50 |
| $10^{6}$ | $2.0\times10^{6}$ | $2.0\times10^{-4}$ | $1.0\times10^{-4}$ | 0.50 |

The true shift is exactly half the bound in this family, so the bound is sharp
to a factor of 2 and the amplification $\kappa_2(V)$ is **real**, not an
artefact of a loose estimate. $\blacksquare$

## Part 3: degeneration

Now take the **same** family but a perturbation that does not excite the
ill-conditioned direction:

$$A_t = \begin{pmatrix}1 & t\\ 0 & 2\end{pmatrix},
\qquad E = \delta\begin{pmatrix}1 & 0\\ 0 & -1\end{pmatrix}, \qquad \delta =
10^{-10}.$$

$A_t$ is diagonalisable for every $t$, and $\kappa_2(V_t) \to \infty$, so the
Bauer-Fike bound $\kappa_2(V_t)\delta \to \infty$.

Measured:

| $t$ | bound | measured shift | bound / shift |
|---|---|---|---|
| $10^{2}$ | $2.0\times10^{-8}$ | $1.0\times10^{-10}$ | $2.0\times10^{2}$ |
| $10^{4}$ | $2.0\times10^{-6}$ | $1.0\times10^{-10}$ | $2.0\times10^{4}$ |
| $10^{6}$ | $2.0\times10^{-4}$ | $1.0\times10^{-10}$ | $2.0\times10^{6}$ |
| $10^{8}$ | $2.0\times10^{-2}$ | $1.0\times10^{-10}$ | $2.0\times10^{8}$ |

**The answer to the question is no.** The bound grows without limit while the
true shift stays pinned at $\delta$, because this $E$ is diagonal and commutes
with the eigenvalue structure in the relevant way: the eigenvalues of $A_t + E$
are exactly $1 + \delta$ and $2 - \delta$ for every $t$.

So Bauer-Fike is **simultaneously sharp and vacuous**, depending on $E$: sharp
for the worst-case $E$ (Part 2), and arbitrarily loose for a specific one (Part
3). It is a worst-case bound over all perturbations of a given norm, and
quoting it for a particular $E$ says only that *some* perturbation of that size
could do that much damage.

## Part 4: the defective case

For $J_n$ nilpotent, **Bauer-Fike asserts nothing at all**: not "the bound is
large", but that the theorem has no hypothesis to apply. $J_n$ is not
diagonalisable: its geometric multiplicity is 1 and its algebraic multiplicity
is $n$, so there is no $V$ with $J_n = V\Lambda V^{-1}$.

### What `eig` returns

`numpy.linalg.eig(J_n)` does not fail. It returns $n$ eigenvalues (all exactly
0 here) and an $n\times n$ matrix $V$ whose columns are **exactly** $e_1$:
because $e_1$ really is the only eigenvector direction. That $V$ is therefore
exactly singular:

| $n$ | $\kappa_2(V)$ from `numpy.linalg.eig(J_n)` | resulting Bauer-Fike "bound" at $\|E\|_2 = 10^{-16}$ |
|---|---|---|
| 2 | $\sim10^{291}$ | $\sim10^{275}$ |
| 8 | $\infty$ | $\infty$ |
| 16 | $\infty$ | $\infty$ |

The bound is infinite. That is a true statement and an empty one: it is
consistent with every possible behaviour, and in particular it does not
distinguish $n = 2$ from $n = 16$, whose true shifts under the same $\|E\|_2 =
10^{-16}$ are $10^{-8}$ and $10^{-1}$: seven orders of magnitude apart.

### The case that actually arises

An exactly defective matrix is a measure-zero event; what one meets is a
**nearly** defective one, where the eigenvalues are distinct, `eig` returns a
genuine $V$, and Bauer-Fike formally applies. There $\kappa_2(V)$ is finite and
enormous:

| $n$ | eigenvalue gap | $\kappa_2(V)$ |
|---|---|---|
| 4 | $10^{-4}$ | $1.5\times10^{12}$ |
| 4 | $10^{-8}$ | $1.5\times10^{24}$ |
| 8 | $10^{-4}$ | $3.3\times10^{26}$ |
| 8 | $10^{-8}$ | $3.3\times10^{54}$ |

The theorem is valid and the bound is useless long before the matrix becomes
defective. There is no threshold at which it stops working; it degrades
continuously as the eigenvectors align.

**The lesson.** The hypothesis of a theorem must be *checked*, not inferred
from a routine returning a value. `eig` returning a `V` is not evidence that
$A$ is diagonalisable; the diagnostic is $\kappa_2(V)$ approaching $1/u$, or
better, a left/right eigenvector inner product $y^{*}x$ approaching 0.

## Remarks

* The correct tool for the defective and nearly-defective case is the
  **pseudospectrum**: $\Lambda_\epsilon(A) = \{z : \|(zI-A)^{-1}\|_2 \ge
  1/\epsilon\}$, which is exactly the set of eigenvalues reachable under
  perturbations of norm $\le \epsilon$ and needs no diagonalisability.
  Bauer-Fike is the statement that $\Lambda_\epsilon(A)$ is contained in the
  union of discs of radius $\kappa_2(V)\epsilon$ about the eigenvalues.
* Bauer-Fike has a *per-eigenvalue* refinement using the individual condition
  numbers $1/|y_i^{*}x_i|$: see
  `eigenvalue-condition-number-is-one-over-the-inner-product`: which is often
  far sharper, because $\kappa_2(V)$ is a single global constant governed by
  the worst eigenvector pair.
