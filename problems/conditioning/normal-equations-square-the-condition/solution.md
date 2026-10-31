# Solution

## Part 1

### The singular values of $A^{\mathsf T}A$

Let $A = U\Sigma V^{\mathsf T}$ be a thin SVD, $U \in \mathbb{R}^{m\times n}$
with orthonormal columns, $V \in \mathbb{R}^{n\times n}$ orthogonal, and
$\Sigma = \operatorname{diag}(\sigma_1,\dots,\sigma_n)$. Then

$$A^{\mathsf T}A = V\Sigma U^{\mathsf T}U\Sigma V^{\mathsf T}
                 = V\Sigma^2 V^{\mathsf T},$$

using $U^{\mathsf T}U = I_n$.

This is a **symmetric eigendecomposition** of $A^{\mathsf T}A$ with eigenvalues
$\sigma_i^2 \ge 0$. Because $A^{\mathsf T}A$ is symmetric positive semidefinite,
its singular values coincide with its eigenvalues, so they are exactly
$\sigma_1^2 \ge \cdots \ge \sigma_n^2$.

**Where full rank is used.** Full column rank gives $\sigma_n > 0$, hence
$\sigma_n^2 > 0$, so $A^{\mathsf T}A$ is positive *definite* and invertible and
$\kappa_2(A^{\mathsf T}A)$ is finite. Without it both sides are $+\infty$ and
the identity is vacuous.

### The identity

$$\kappa_2(A^{\mathsf T}A)
  = \frac{\sigma_1^2}{\sigma_n^2}
  = \left(\frac{\sigma_1}{\sigma_n}\right)^{\!2}
  = \kappa_2(A)^2 . \qquad\blacksquare$$

Note this is an **equality**, not a bound. Submultiplicativity gives only
$\kappa(A^{\mathsf T}A) \le \kappa(A^{\mathsf T})\kappa(A) = \kappa(A)^2$; the
reverse inequality is what the singular values supply, and it is the half that
matters, because it says the squaring cannot be avoided by a lucky $A$.

## Part 2

A backward-stable solver applied to a matrix $M$ returns $\hat x$ with

$$\frac{\|\hat x - x\|}{\|x\|} \lesssim u\,\kappa_2(M).$$

### (a)

**Cholesky on the normal equations.** The matrix actually factorised is
$M = A^{\mathsf T}A$, with $\kappa_2(M) = \kappa_2(A)^2 = 10^{16}$:

$$\frac{\|\hat x - x\|}{\|x\|} \lesssim 1.1\times10^{-16} \cdot 10^{16}
   \approx 1 .$$

No correct digits. The computation would have formed $A^{\mathsf T}A$ and found
it numerically indefinite, so Cholesky may well fail outright --- which is the
better outcome, since it is visible.

**Householder QR on $A$.** QR factorises $A$ itself, so $\kappa_2(M) = 10^{8}$:

$$\frac{\|\hat x - x\|}{\|x\|} \lesssim 1.1\times10^{-16}\cdot 10^{8}
   \approx 10^{-8},$$

about eight correct digits. Same problem, same arithmetic, eight digits against
none.

The rule of thumb: **the normal equations lose twice as many digits.** With $u
\approx 10^{-16}$ there are about 16 to spend; QR spends
$\log_{10}\kappa_2(A)$ of them and Cholesky spends $2\log_{10}\kappa_2(A)$.

### (b)

The Cholesky route exhausts the budget when
$u\,\kappa_2(A)^2 \approx 1$, i.e.

$$\kappa_2(A) \approx u^{-1/2} \approx 10^{8}.$$

The QR route exhausts it at $\kappa_2(A) \approx u^{-1} \approx 10^{16}$.

At $\kappa_2(A) = 10^{8}$ the QR route is still at $10^{-8}$ relative error
because it never forms $A^{\mathsf T}A$: the information in the small singular
values is destroyed by the *rounding of the product*, not by the conditioning
of the original problem. Once $\sigma_n^2$ falls below $u\,\sigma_1^2$ it is
lost in the entries of $A^{\mathsf T}A$ regardless of how it is subsequently
solved.

This is the key point. The squaring is a property of the **algorithm**, not of
the problem. The least-squares problem has sensitivity $\kappa_2(A)$ (for a
consistent system); the normal equations are a route that gratuitously doubles
the exponent.

## Part 3: residual and error

Let $\hat x$ be any computed solution of a square nonsingular system $Ax = b$,
with residual $r = b - A\hat x$. Then $x - \hat x = A^{-1}r$, so

$$\|x - \hat x\| \le \|A^{-1}\|\,\|r\|,
\qquad
\|b\| \le \|A\|\,\|x\| ,$$

and dividing,

$$\boxed{\ \frac{\|x - \hat x\|}{\|x\|}
   \le \kappa(A)\,\frac{\|r\|}{\|b\|}\ }$$

So a relative residual of $10^{-16}$ guarantees a relative error of only
$10^{-16}\kappa(A)$. At $\kappa = 10^{16}$ that is a bound of 1: the residual
says nothing at all about the solution.

**The bound is attained**, so this is not pessimism. Take $r$ aligned with the
left singular vector $u_n$ belonging to $\sigma_n$ and $b$ aligned with $u_1$:
then $\|A^{-1}r\| = \|r\|/\sigma_n$ and $\|x\| = \|b\|/\sigma_1$, giving
equality.

**The asymmetry to remember.** A backward-stable algorithm guarantees a small
*residual* --- that is what backward stability means. It does not and cannot
guarantee a small *error*. The user almost always wants the error. The factor
between the two is $\kappa$, which is exactly the quantity the normal equations
have just squared, so the two parts of this problem are the same observation
twice.

## Remarks

* For an **inconsistent** least-squares problem the sensitivity is not
  $\kappa_2(A)$ but $\kappa_2(A) + \kappa_2(A)^2\tan\theta$, where $\theta$ is
  the angle between $b$ and the range of $A$. So the squaring reappears for a
  genuine reason when the residual is large; what the normal equations do is
  incur it even when $\theta = 0$.
* $A^{\mathsf T}A$ is also $n^2/2$ inner products of length $m$: the normal
  equations are cheaper, roughly $mn^2$ flops against $2mn^2$ for Householder
  QR. The factor of two in cost is the whole case for them, against a factor of
  two in *digits*.
* Seminormal equations (solving $R^{\mathsf T}Rx = A^{\mathsf T}b$ with $R$
  from a QR of $A$) recover most of the accuracy at the lower cost, and one
  step of iterative refinement recovers the rest.
