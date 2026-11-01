# Flawed solution: `right-eigenvectors-suffice`

## The submitted argument

> **Step 1.** Differentiate $A(t)x(t) = \lambda(t)x(t)$ at $t = 0$:
> $Ex + Ax'(0) = \lambda'(0)x + \lambda x'(0)$.
>
> **Step 2.** Multiply on the left by $x^{*}$ to isolate $\lambda'(0)$:
> $$x^{*}Ex + x^{*}Ax'(0) = \lambda'(0)\,x^{*}x + \lambda\,x^{*}x'(0).$$
>
> **Step 3.** Since $Ax = \lambda x$, we have
> $x^{*}A = \lambda x^{*}$, so the $x'(0)$ terms cancel.
>
> **Step 4.** With $x^{*}x = 1$, $\lambda'(0) = x^{*}Ex$ and the condition
> number is $1/|x^{*}x| = 1$. Every simple eigenvalue is perfectly conditioned.

## Where it breaks

**Step 3**, at "$Ax = \lambda x$, so $x^{*}A = \lambda x^{*}$".

Taking the conjugate transpose of $Ax = \lambda x$ gives $x^{*}A^{*} =
\bar\lambda x^{*}$: a statement about $A^{*}$, not about $A$. The vector
satisfying $y^{*}A = \lambda y^{*}$ is the **left** eigenvector, and it equals
$x$ only when $A = A^{*}$ (or more generally when $A$ is normal, where the
eigenvectors of $A$ and $A^{*}$ coincide).

Without that cancellation, Step 2 leaves the unknown $x'(0)$ in the equation
and $\lambda'(0)$ cannot be isolated at all. Multiplying by $y^{*}$ instead is
exactly what makes the $x'(0)$ terms vanish, and that is the reason the left
eigenvector appears in the formula.

## How wrong Step 4 is

$A = \begin{pmatrix}1 & t\\ 0 & 2\end{pmatrix}$ has simple eigenvalues and, for
unit $x$ and $y$,

| $t$ | $x^{*}x$ | $|y^{*}x|$ | true $\kappa(\lambda)$ |
|---|---|---|---|
| $10^{2}$ | 1 | $1.0\times10^{-2}$ | $1.0\times10^{2}$ |
| $10^{4}$ | 1 | $1.0\times10^{-4}$ | $1.0\times10^{4}$ |
| $10^{6}$ | 1 | $1.0\times10^{-6}$ | $1.0\times10^{6}$ |

Step 4 predicts 1 in every row. The quantity it uses, $x^{*}x$, is 1 by
construction: which is the tell: a "condition number" that equals 1 because the
vectors were normalised is measuring the normalisation, not the matrix.

## The geometric reading

$|y^{*}x| = \cos\theta$ where $\theta$ is the angle between the left and right
eigenvectors. Step 4 effectively asserts $\theta = 0$ always. For a normal
matrix that is true, and for the shear above $\theta \to \pi/2$ as $t$ grows:
the eigenvalue is ill-conditioned exactly because its left and right
eigenvectors become orthogonal.

## Failure mode

`conflating-left-and-right`: the left eigenvector is replaced by the right one,
which is valid only for normal matrices, and the resulting condition number is
identically 1 by construction.
