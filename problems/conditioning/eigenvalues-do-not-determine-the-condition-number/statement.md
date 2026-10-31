# Eigenvalues do not determine the condition number

## Assumptions

$A \in \mathbb{C}^{n\times n}$ nonsingular with eigenvalues
$\lambda_1, \dots, \lambda_n$ ordered by modulus,
$|\lambda_1| \ge \cdots \ge |\lambda_n| > 0$.

$A$ is **normal** if $A^{*}A = AA^{*}$; equivalently (spectral theorem) if
$A = U\Lambda U^{*}$ for some unitary $U$.

## Part 1 (universal, with a hypothesis)

Prove that if $A$ is normal then

$$\kappa_2(A) = \frac{|\lambda_1|}{|\lambda_n|}.$$

Identify precisely where normality is used.

## Part 2 (existential)

Show that the hypothesis cannot be dropped: exhibit a family $A_t$ with

* $\operatorname{spec}(A_t) = \{1\}$ for every $t$, so
  $|\lambda_{\max}|/|\lambda_{\min}| = 1$ exactly, and
* $\kappa_2(A_t) \to \infty$ as $t \to \infty$.

Give the singular values of $A_t$ in closed form.

## Part 3

For a diagonalisable $A = V\Lambda V^{-1}$, prove

$$\frac{|\lambda_1|}{|\lambda_n|}
  \;\le\; \kappa_2(A)
  \;\le\; \kappa_2(V)^2\,\frac{|\lambda_1|}{|\lambda_n|}$$

and say what the two bounds become when $A$ is normal. This identifies the
quantity that the eigenvalue ratio is missing.

## What a complete answer contains

1. A proof of Part 1 that names the step where $U^{*}U = I$ is used.
2. An explicit $A_t$ with its singular values in closed form, and the limit.
3. The sandwich in Part 3 with both inequalities proved.
