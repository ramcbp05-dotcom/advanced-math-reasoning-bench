# Hermitian eigenvalues are perfectly conditioned

## Assumptions

$A, E \in \mathbb{C}^{n\times n}$ both **Hermitian**. Write the eigenvalues of
a Hermitian matrix in decreasing order,

$$\lambda_1(M) \ge \lambda_2(M) \ge \cdots \ge \lambda_n(M),$$

all real by the spectral theorem.

## Part 1

Prove **Weyl's inequality**: for every $k$,

$$\boxed{\ \big|\lambda_k(A+E) - \lambda_k(A)\big| \;\le\; \|E\|_2\ }$$

Use the Courant-Fischer min-max characterisation

$$\lambda_k(M) = \max_{\dim S = k}\ \min_{0 \neq x \in S}
   \frac{x^{*}Mx}{x^{*}x}.$$

## Part 2

Show the bound is **attained**, so it cannot be improved: exhibit Hermitian $A,
E$ with $|\lambda_k(A+E) - \lambda_k(A)| = \|E\|_2$ for some $k$.

## Part 3

Conclude that the eigenvalue condition number of a Hermitian matrix is 1, in
the sense that a perturbation of size $\epsilon$ moves no eigenvalue by more
than $\epsilon$: **absolutely**, not relatively.

Then state what happens to the *relative* error of a small eigenvalue, and why
that distinction matters for an eigenvalue near zero.

## Part 4

Identify the hypothesis that fails in the general case. For a diagonalisable $A
= V\Lambda V^{-1}$ the Bauer-Fike theorem gives $\operatorname{dist}(\mu,
\operatorname{spec} A) \le \kappa_2(V)\|E\|_2$. Which property of $A$ makes
$\kappa_2(V) = 1$, and is diagonalisability enough?

## What a complete answer contains

1. A proof of Part 1 from Courant-Fischer that works for **every** $k$, not
   only $k = 1$.
2. An explicit attaining pair.
3. The absolute-versus-relative distinction stated precisely.
4. The correct hypothesis in Part 4, with a one-line reason.
