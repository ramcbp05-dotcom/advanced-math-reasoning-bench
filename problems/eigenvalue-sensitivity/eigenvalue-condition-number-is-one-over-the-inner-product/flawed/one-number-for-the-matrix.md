# Flawed solution: `one-number-for-the-matrix`

## The submitted argument

> **Steps 1-2.** [Part 1 derived correctly, $\kappa(\lambda) = 1/|y^{*}x|$.]
>
> **Step 3.** By Bauer-Fike the eigenvalues of $A + E$ satisfy
> $\min_i|\mu - \lambda_i| \le \kappa_2(V)\|E\|_2$, so the eigenvalue
> conditioning of $A$ is $\kappa_2(V)$.
>
> **Step 4.** For Part 3, no such matrix exists: a matrix has one eigenvalue
> conditioning, namely $\kappa_2(V)$, and it applies to all of its eigenvalues
> equally.

## Where it breaks

**Step 3-4**, which replaces a per-eigenvalue quantity by a global one and then
concludes the per-eigenvalue quantity does not vary.

$\kappa_2(V)$ is a single number governed by the *worst* eigenvector pair in
the matrix. It gives a valid bound for every eigenvalue, and it is the right
bound for none of them individually unless they happen to be equally
conditioned.

## The witness Step 4 denies

$$A = \begin{pmatrix} 1 & 10^{8} & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 5\end{pmatrix}$$

| $\lambda$ | $\kappa(\lambda)$ |
|---|---|
| 1 | $1.0\times10^{8}$ |
| 2 | $1.0\times10^{8}$ |
| 5 | $1.0000$ |

$\kappa_2(V) \approx 2.0\times10^{8}$. The third eigenvalue sits in a decoupled
$1\times1$ block: its left and right eigenvectors are both $e_3$, so
$y^{*}x = 1$ and $\kappa(5) = 1$ exactly. Nothing about the shear in the
top-left corner touches it.

Step 4's prediction for $\lambda = 5$ is a loss of eight digits. The true loss
is zero, and this is verifiable directly: perturb $A$ by $10^{-10}$ and watch
$\lambda = 5$ move by $10^{-10}$ while $\lambda = 1, 2$ move by $10^{-2}$.

## Why the global quantity exists at all

$\kappa_2(V)$ is cheaper and requires no eigenvector pairing: it bounds every
eigenvalue at once and is the natural statement when the question is about the
spectrum as a whole. The relation between the two is

$$\max_i \kappa(\lambda_i) \;\le\; \kappa_2(V) \;\le\; n\max_i\kappa(\lambda_i)$$

(for unit-column $V$), so the global constant is controlled by the worst local
one and says nothing about the best.

`LAPACK`'s `?geevx` returns the per-eigenvalue numbers in `RCONDE` precisely
because the aggregate is so often the wrong thing to report.

## Failure mode

`global-bound-for-a-local-quantity`: a bound valid for all eigenvalues is
treated as the value for each, so a well-conditioned eigenvalue inherits the
worst case of its neighbours.
