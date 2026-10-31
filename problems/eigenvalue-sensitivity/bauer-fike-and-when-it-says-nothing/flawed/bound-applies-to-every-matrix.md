# Flawed solution: `bound-applies-to-every-matrix`

## The submitted argument

> **Steps 1-3.** [Parts 1 and 2 answered correctly.]
>
> **Step 4.** For Part 4, apply Bauer-Fike to $J_{16}$. Obtain the eigenvector
> matrix numerically:
>
> ```python
> w, V = np.linalg.eig(J)
> bound = np.linalg.cond(V, 2) * np.linalg.norm(E, 2)
> ```
>
> **Step 5.** This gives $\kappa_2(V) \approx 3\times10^{16}$, so with
> $\|E\|_2 = 10^{-16}$ the bound is about 3. The eigenvalues could move by up
> to 3, which is consistent with the observed $0.1$.
>
> **Step 6.** So Bauer-Fike does apply, and correctly predicts large
> sensitivity.

## Where it breaks

**Step 4**, at the point where $V$ is obtained. Bauer-Fike requires
$A = V\Lambda V^{-1}$ — a genuine diagonalisation. $J_{16}$ is **not
diagonalisable**: its eigenvalue 0 has algebraic multiplicity 16 and geometric
multiplicity 1, so no such $V$ exists.

`np.linalg.eig` does not report this. It returns 16 eigenvalues (all at
rounding level) and a $16\times16$ matrix whose columns are all numerically
parallel to $e_1$, since that is the only eigenvector direction there is. The
returned $V$ does not satisfy $J_{16} = V\Lambda V^{-1}$ to any useful
accuracy; it is the eigensolver's best effort at a factorisation that does not
exist.

## Why the number in Step 5 is meaningless

$\kappa_2(V) \approx 3\times10^{16} \approx 1/u$. That is not a property of
$J_{16}$ — it is the conditioning of a numerically-singular matrix, determined
by the rounding errors that broke the exact parallelism of the columns. Compute
it in a different precision and it changes by whatever that precision is; it
has no limit as the computation is refined.

Step 6's "correctly predicts" is the part worth rejecting hardest. The bound
came out as 3 and the observed shift was 0.1, which looks like agreement within
a factor of 30. But:

* the bound would be 3 for **any** $\|E\|_2 = 10^{-16}$, regardless of $n$,
  since $\kappa_2(V) \approx 1/u$ whatever $n$ is;
* the true shifts are $10^{-8}$, $10^{-2}$ and $10^{-1}$ for $n = 2, 8, 16$ —
  seven orders of magnitude apart, all "predicted" by the same number 3.

A quantity that returns the same answer for cases that differ by $10^{7}$ is
not predicting anything.

## The correct answer to Part 4

Bauer-Fike asserts **nothing** about $J_n$, because its hypothesis fails. The
exact sensitivity is known by other means:
$|\lambda| = \epsilon^{1/n}$ exactly
(`jordan-block-perturbation-is-epsilon-to-the-one-over-n`), and the right
general tool is the pseudospectrum, which requires no diagonalisability.

## The diagnostic

Before using a $V$ from `eig`, check the factorisation it claims:

```
residual = norm(A @ V - V @ diag(w)) / norm(A)
```

For a genuinely diagonalisable matrix this is at rounding level. For $J_{16}$
it is not, and $\kappa_2(V) \approx 1/u$ is the second signal. A routine
returning a value is not a certificate that its output means what the caller
wants it to mean.

## Failure mode

`hypothesis-silently-unverified`: a theorem's hypothesis is assumed because a
numerical routine returned a value, rather than checked.
