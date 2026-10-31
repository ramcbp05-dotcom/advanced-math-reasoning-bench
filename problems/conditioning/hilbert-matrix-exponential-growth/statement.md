# The Hilbert matrix is ill-conditioned exponentially in its size

## Assumptions

The $n\times n$ **Hilbert matrix** is

$$(H_n)_{ij} = \frac{1}{i + j - 1}, \qquad 1 \le i, j \le n .$$

It is the Gram matrix of the monomials $1, x, \dots, x^{n-1}$ in
$L^2[0,1]$:

$$\int_0^1 x^{i-1}x^{j-1}\,dx = \frac{1}{i+j-1}.$$

## Part 1

Prove that $H_n$ is symmetric **positive definite** for every $n$, and deduce
that it is nonsingular and that $\kappa_2(H_n) = \lambda_{\max}/\lambda_{\min}$.

## Part 2

The Cauchy determinant formula gives

$$\det H_n = \frac{\big(\prod_{k=1}^{n-1}k!\big)^{4}}{\prod_{k=1}^{2n-1}k!} .$$

Verify this in exact arithmetic for $n \le 8$ and compute $\det H_{12}$
exactly. Then answer: does $\det H_n \to 0$ imply that $H_n$ "becomes
singular"? Justify your answer against the results of
`cond2-is-singular-value-ratio`.

## Part 3

It is known that

$$\kappa_2(H_n) \sim \frac{(1+\sqrt2)^{4n}}{2^{15/4}\sqrt{\pi n}}
   \qquad (n \to \infty),$$

so $\ln\kappa_2(H_n) \approx 4\ln(1+\sqrt2)\,n$. Measure the growth constant
numerically for $2 \le n \le 13$ and compare it with
$4\ln(1+\sqrt2) = 3.5255\ldots$

**Then state carefully what your measurement has and has not established.**

## Part 4

At what $n$ does a double-precision solve of $H_nx = b$ stop returning a single
correct digit? What goes wrong if you try to answer Part 3 by measuring
$\kappa_2(H_{20})$ in double precision?

## What a complete answer contains

1. A proof of positive definiteness from the Gram-matrix representation,
   including why the integral is strictly positive for a nonzero polynomial.
2. The exact determinant for at least one $n \ge 10$, as a rational number.
3. A fitted growth constant with its agreement to the asymptotic value stated
   as a percentage.
4. An explicit statement that a fit over $2 \le n \le 13$ is consistent with the
   asymptotic law and does not prove it.
