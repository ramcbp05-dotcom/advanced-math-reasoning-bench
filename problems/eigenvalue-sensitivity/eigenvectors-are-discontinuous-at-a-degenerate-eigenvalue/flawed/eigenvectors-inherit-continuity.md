# Flawed solution: `eigenvectors-inherit-continuity`

## The submitted argument

> **Step 1.** Eigenvalues depend continuously on the entries of $A$.
>
> **Step 2.** An eigenvector for $\lambda$ solves the linear system
> $(A - \lambda I)v = 0$.
>
> **Step 3.** The matrix $A - \lambda I$ depends continuously on $A$ (by Step 1
> and continuity of subtraction), and the solution set of a linear system
> depends continuously on the matrix.
>
> **Step 4.** So eigenvectors are continuous too, and Part 2 has no
> counterexample.

## Where it breaks

**Step 3**, at "the solution set of a linear system depends continuously on the
matrix".

The solution set of $(A - \lambda I)v = 0$ is a **subspace**, and its dimension
is $n - \operatorname{rank}(A - \lambda I)$. Rank is upper semicontinuous, not
continuous: it can **drop** in the limit, and when it does the null space jumps
in dimension.

That is exactly what happens here. For $\epsilon > 0$,
$\operatorname{rank}(B(\epsilon) - (1+\epsilon)I) = 1$ and the null space is a
line. At $\epsilon = 0$ the rank drops to 0 and the null space is the whole
plane. A line does not converge to a plane in any sense that makes "choose a
unit vector from it" continuous.

## Where the argument would be correct

If $\lambda$ is a **simple** eigenvalue of $A$, then for nearby $A'$ the
corresponding eigenvalue stays simple, the null space stays one-dimensional,
and the eigenvector (up to sign) *is* continuous. The missing hypothesis is
simplicity, and the correct quantitative version is the Davis-Kahan theorem,
whose constant is $1/\text{gap}$ — unbounded as the gap closes.

## The witness

$B(\epsilon) = \operatorname{diag}(1+\epsilon, 1-\epsilon)$ and
$C(\epsilon) = \begin{psmallmatrix}1 & \epsilon\\ \epsilon & 1\end{psmallmatrix}$
have:

* the same distance to $I$: $\|\cdot\|_2 = \epsilon$ for both;
* the same spectrum: $\{1+\epsilon, 1-\epsilon\}$ for both;
* top eigenvectors $45°$ apart, for every $\epsilon > 0$.

Measured at $\epsilon = 10^{-8}$: the angle is $45.000000°$. Step 4 requires it
to tend to $0°$.

## Failure mode

`continuity-of-a-set-valued-map`: continuity of a matrix-valued function is
transferred to its null space, across a point where the null-space dimension
jumps.
