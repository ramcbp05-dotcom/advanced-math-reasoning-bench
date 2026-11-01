# The 2-norm condition number is the ratio of extreme singular values

## Assumptions

Let $A \in \mathbb{C}^{n\times n}$ be **nonsingular**, with singular values

$$\sigma_1 \ge \sigma_2 \ge \cdots \ge \sigma_n > 0.$$

Throughout, $\|\cdot\|_2$ is the operator norm induced by the Euclidean vector
norm, and

$$\kappa_2(A) := \|A\|_2\,\|A^{-1}\|_2 .$$

Nonsingularity is what makes $\sigma_n > 0$ and $A^{-1}$ exist; without it
$\kappa_2$ is conventionally $+\infty$.

## Part 1 (universal)

Prove that

$$\boxed{\ \kappa_2(A) = \frac{\sigma_1}{\sigma_n}\ }$$

and deduce the two properties that make $\kappa_2$ a measure of *conditioning*
rather than of size:

* $\kappa_2(A) \ge 1$ for every nonsingular $A$, with equality **iff** $A$ is a
  scalar multiple of a unitary matrix;
* $\kappa_2(cA) = \kappa_2(A)$ for every scalar $c \neq 0$.

## Part 2 (existential)

Two statements appear constantly in informal discussion. Decide each, and where
it is false exhibit an explicit counterexample:

**(a)** "If $|\det A|$ is not small, then $A$ is well conditioned."

**(b)** "If $|\det A|$ is small, then $A$ is ill conditioned."

A counterexample must be *exact*: give the matrix, its singular values and its
determinant in closed form, not as floating-point output.

## What a complete answer contains

1. A proof of the boxed identity from the singular value decomposition,
   including the step that $\|A\|_2 = \sigma_1$.
2. The equality case of $\kappa_2 \ge 1$, stated as an "if and only if".
3. The scale invariance, with the one-line computation.
4. For Part 2, an exact witness for each false statement, and an explanation of
   *why* the determinant cannot do this job: not merely a demonstration that it
   fails.
