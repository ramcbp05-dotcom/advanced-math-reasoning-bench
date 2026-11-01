# Solution

## Part 1: first-order perturbation

Since $\lambda$ is simple, it is a simple root of the characteristic polynomial
of $A$, whose coefficients depend analytically on $t$. By the implicit function
theorem applied to $p(\lambda, t) = \det(\lambda I - A - tE)$ (which has
$\partial p/\partial\lambda \neq 0$ at $(\lambda, 0)$ precisely because the
root is simple) there is an analytic branch $\lambda(t)$ with
$\lambda(0)=\lambda$, and a corresponding analytic eigenvector $x(t)$ with
$x(0) = x$.

Differentiate $A(t)x(t) = \lambda(t)x(t)$ at $t = 0$:

$$Ex + Ax'(0) = \lambda'(0)x + \lambda x'(0).$$

Multiply on the left by $y^{*}$ and use $y^{*}A = \lambda y^{*}$:

$$y^{*}Ex + \lambda y^{*}x'(0) = \lambda'(0)\,y^{*}x + \lambda\,y^{*}x'(0).$$

The terms in $x'(0)$ cancel: **this is the whole trick**, and it is why the
left eigenvector appears: $y^{*}$ annihilates the unknown derivative of the
eigenvector. Since $y^{*}x \neq 0$,

$$\lambda'(0) = \frac{y^{*}Ex}{y^{*}x}. \qquad\blacksquare$$

### The bound

With $\|x\|_2 = \|y\|_2 = 1$, Cauchy-Schwarz gives $|y^{*}Ex| \le
\|y\|_2\|E\|_2\|x\|_2 = \|E\|_2$, so

$$|\lambda'(0)| \le \frac{\|E\|_2}{|y^{*}x|} = \kappa(\lambda)\,\|E\|_2 ,$$

and the bound is attained by $E = yx^{*}$, for which $y^{*}Ex =
(y^{*}y)(x^{*}x) = 1$ and $\|E\|_2 = 1$. So $\kappa(\lambda)$ is the exact
first-order amplification, not an over-estimate.

## Part 2: $\kappa \ge 1$, with equality for normal matrices

**Lower bound.** Cauchy-Schwarz: $|y^{*}x| \le \|y\|_2\|x\|_2 = 1$, so
$\kappa(\lambda) = 1/|y^{*}x| \ge 1$.

**Normal case.** If $A$ is normal then $A = U\Lambda U^{*}$ with $U$ unitary.
Writing $u_i$ for the columns of $U$: $Au_i = \lambda_iu_i$, so $x = u_i$; and
$u_i^{*}A = u_i^{*}U\Lambda U^{*} = \lambda_iu_i^{*}$, so $y = u_i$ as well.
**For a normal matrix the left and right eigenvectors coincide.** Hence

$$|y^{*}x| = |u_i^{*}u_i| = 1, \qquad \kappa(\lambda_i) = 1 . \qquad\blacksquare$$

This is the per-eigenvalue form of
`hermitian-eigenvalues-are-perfectly-conditioned`: Weyl's inequality says every
eigenvalue of a Hermitian matrix moves by at most $\|E\|_2$, and here each one
individually has amplification exactly 1.

Measured over 100 normal matrices: $\max_i|\kappa(\lambda_i) - 1| < 10^{-13}$.

## Part 3: it is a per-eigenvalue quantity

Take

$$A = \begin{pmatrix} 1 & 10^{8} & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 5 \end{pmatrix}.$$

Eigenvalues 1, 2, 5, all simple. The block structure separates the third
coordinate completely, so $\lambda = 5$ has $x = y = e_3$ and $\kappa(5) = 1$
**exactly**, while the $2\times2$ shear in the top-left makes $\kappa(1)$ and
$\kappa(2)$ both about $10^{8}$.

Measured:

| $\lambda$ | $\kappa(\lambda) = 1/|y^{*}x|$ |
|---|---|
| 1 | $1.0\times10^{8}$ |
| 2 | $1.0\times10^{8}$ |
| 5 | $1.0000$ |

$\kappa_2(V)$ for the whole matrix is $2.0\times10^{8}$.

**Which to consult.** A user wanting $\lambda = 5$ should use $\kappa(5) = 1$:
that eigenvalue is perfectly conditioned and will be computed to full
precision. Bauer-Fike's $\kappa_2(V) = 2.0\times10^{8}$ is a global worst case
over all eigenvalues and would predict a loss of eight digits in an eigenvalue
that loses none.

So the per-eigenvalue condition numbers are strictly more informative, and
`LAPACK`'s `?geevx` returns them (`RCONDE`) for exactly this reason.

## Part 4: approaching a defective eigenvalue

As two eigenvalues coalesce into a defective one, the corresponding left and
right eigenvectors become **orthogonal**, so $y^{*}x \to 0$ and
$\kappa(\lambda) \to \infty$.

The nilpotent Jordan block is the limit: $x = e_1$, $y = e_n$, and $y^{*}x = 0$
exactly. The condition number is infinite, which is the first-order statement
of the result in `jordan-block-perturbation-is-epsilon-to-the-one-over-n`: the
eigenvalue is not differentiable in the perturbation at all, moving like
$\epsilon^{1/n}$ rather than like $\epsilon$.

Measured for $A_\delta = \begin{psmallmatrix}1 & 1\\ \delta &
1\end{psmallmatrix}$, whose eigenvalues $1 \pm \sqrt\delta$ coalesce as $\delta
\to 0$:

| $\delta$ | eigenvalue gap | $\kappa(\lambda)$ |
|---|---|---|
| $10^{-2}$ | $2.0\times10^{-1}$ | $5.0$ |
| $10^{-4}$ | $2.0\times10^{-2}$ | $50$ |
| $10^{-6}$ | $2.0\times10^{-3}$ | $5.0\times10^{2}$ |
| $10^{-8}$ | $2.0\times10^{-4}$ | $5.0\times10^{3}$ |

$\kappa$ grows like $\delta^{-1/2}$, i.e. inversely with the eigenvalue gap.
$y^{*}x \to 0$ is therefore the **diagnostic** that should be computed before
any first-order estimate is used, and it is the quantity that
`first-order-perturbation-theory` (a flawed solution in the Jordan problem)
divides by without checking.

## Remarks

* $\kappa(\lambda)$ is invariant under the normalisation of $x$ and $y$ *only*
  if both are taken to unit length: which is why the statement specifies it.
  Scaling $x \to cx$ scales $y^{*}x$ by $c$ and the unit-norm condition removes
  the freedom.
* The quantity $1/|y^{*}x|$ is the secant of the angle between the left and
  right eigenvector, so "ill-conditioned eigenvalue" means literally "left and
  right eigenvectors nearly orthogonal".
* For a *multiple* but non-defective eigenvalue (algebraic = geometric
  multiplicity > 1) the right object is the spectral projector and its norm;
  the scalar $1/|y^{*}x|$ is not defined because $x$ and $y$ are not unique.
