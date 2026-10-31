# The condition number of a simple eigenvalue is $1/|y^{*}x|$

## Assumptions

$A \in \mathbb{C}^{n\times n}$ with a **simple** eigenvalue $\lambda$ (algebraic
multiplicity 1). Let $x$ be a right eigenvector ($Ax = \lambda x$) and $y$ a
left eigenvector ($y^{*}A = \lambda y^{*}$), both normalised to
$\|x\|_2 = \|y\|_2 = 1$.

A standard fact used without proof: for a simple eigenvalue, $y^{*}x \neq 0$.

## Part 1

Let $A(t) = A + tE$ with $E$ fixed. Prove that the eigenvalue $\lambda(t)$ of
$A(t)$ with $\lambda(0) = \lambda$ is differentiable at $t = 0$ with

$$\boxed{\ \lambda'(0) = \frac{y^{*}Ex}{y^{*}x}\ }$$

and deduce

$$|\lambda(t) - \lambda| \le \frac{\|E\|_2}{|y^{*}x|}\,|t| + O(t^2),$$

so that $\kappa(\lambda) := 1/|y^{*}x|$ is the **eigenvalue condition number**.

## Part 2

Prove $\kappa(\lambda) \ge 1$ always, and $\kappa(\lambda) = 1$ for every
eigenvalue of a **normal** matrix. Relate this to
`hermitian-eigenvalues-are-perfectly-conditioned`.

## Part 3

Show that $\kappa(\lambda)$ is genuinely a property of the **eigenvalue** and
not of the matrix: exhibit a single matrix with one eigenvalue of condition
number close to 1 and another of condition number above $10^{8}$.

Then compare with $\kappa_2(V)$ from Bauer-Fike, and say which of the two a
user wanting one particular eigenvalue should consult.

## Part 4

What happens to $\kappa(\lambda)$ as the eigenvalue approaches a defective one?
Connect to `jordan-block-perturbation-is-epsilon-to-the-one-over-n`.

## What a complete answer contains

1. A derivation of Part 1, including why $\lambda(t)$ is differentiable.
2. A proof of both halves of Part 2.
3. An explicit matrix for Part 3 with both condition numbers computed.
