# Flawed solution: `eigenvalue-ratio-always`

## The submitted argument

> **Step 1.** Diagonalise $A = V\Lambda V^{-1}$.
>
> **Step 2.** Then $\|A\|_2 = \|V\Lambda V^{-1}\|_2 = \|\Lambda\|_2 =
> \max_i|\lambda_i|$, since a similarity transformation does not change the
> norm.
>
> **Step 3.** Likewise $\|A^{-1}\|_2 = 1/\min_i|\lambda_i|$.
>
> **Step 4.** Hence $\kappa_2(A) = |\lambda_1|/|\lambda_n|$ for every
> diagonalisable $A$, and Part 2 has no counterexample.

## Where it breaks

**Step 2**, at "a similarity transformation does not change the norm". A
*unitary* similarity does not change the 2-norm; a general similarity does.
Explicitly,

$$\|V\Lambda V^{-1}\|_2 \le \|V\|_2\|\Lambda\|_2\|V^{-1}\|_2
  = \kappa_2(V)\max_i|\lambda_i|,$$

and the inequality is generally strict in both directions: there is no equality
to recover.

The statement in Step 2 is true exactly when $V$ can be chosen unitary, which
by the spectral theorem is exactly when $A$ is normal. The submission has
silently assumed normality.

## The witness it misses

$A_t = \begin{pmatrix}1&t\\0&1\end{pmatrix}$ has both eigenvalues equal to 1,
so Steps 2-4 predict $\kappa_2 = 1$ for every $t$. The true value is

$$\kappa_2(A_t) = \frac{2 + t^2 + t\sqrt{t^2+4}}{2} \sim t^2 ,$$

which is $10^{12}$ at $t = 10^{6}$.

$A_t$ is also not diagonalisable, so Step 1 fails for it as well: but that is a
second, separate problem. Taking $A = \begin{pmatrix}1&t\\0&2\end{pmatrix}$
gives a diagonalisable matrix with eigenvalue ratio exactly 2 and $\kappa_2$
again growing like $t^2$, so the error survives the repair.

## What the invariance claim should have been

The quantity that is invariant under similarity is the **spectrum**, and the
quantity that is invariant under *unitary* similarity is the whole set of
singular values. $\kappa_2$ is a function of the singular values, so it is a
unitary invariant and not a similarity invariant. Since the eigenvalues are a
similarity invariant, no function of the eigenvalues alone can equal $\kappa_2$
for all matrices: which refutes Step 4 without any example at all.

## Failure mode

`missing-hypothesis`: a theorem about normal matrices is applied to general
ones, with the hypothesis dropped at the step that uses it.
