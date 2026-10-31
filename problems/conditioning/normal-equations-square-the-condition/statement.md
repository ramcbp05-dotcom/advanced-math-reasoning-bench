# The normal equations square the condition number

## Assumptions

Let $A \in \mathbb{R}^{m\times n}$ with $m \ge n$ and
$\operatorname{rank}(A) = n$ (full column rank), with singular values

$$\sigma_1 \ge \cdots \ge \sigma_n > 0 .$$

For a rectangular matrix of full column rank define
$\kappa_2(A) := \sigma_1/\sigma_n$; this agrees with
$\|A\|_2\|A^{-1}\|_2$ when $A$ is square and nonsingular, and equals
$\|A\|_2\|A^{+}\|_2$ in general, where $A^{+}$ is the Moore-Penrose
pseudoinverse.

## Part 1

Prove that the singular values of $A^{\mathsf T}A$ are exactly
$\sigma_1^2, \dots, \sigma_n^2$, and deduce

$$\boxed{\ \kappa_2(A^{\mathsf T}A) = \kappa_2(A)^2\ }$$

State clearly where full column rank is used.

## Part 2

The least-squares problem $\min_x \|Ax - b\|_2$ has the normal equations

$$A^{\mathsf T}A\,x = A^{\mathsf T}b$$

as its first-order condition. Suppose $\kappa_2(A) = 10^{8}$ and the arithmetic
has unit roundoff $u \approx 1.1\times 10^{-16}$.

**(a)** Estimate the relative error in $x$ from solving the normal equations by
Cholesky factorisation, and from solving the same problem by Householder QR
applied to $A$ directly. A standard backward-stable solver returns a solution
whose relative error is bounded by roughly $u\,\kappa_2(M)$ for the matrix $M$
it actually factorises.

**(b)** At what $\kappa_2(A)$ does the Cholesky route lose all significance,
and why does the QR route still return several correct digits there?

## Part 3

Explain why the *residual* $\|A\hat x - b\|_2$ can be small --- even at its
minimum to many digits --- while $\hat x$ itself has no correct digits. State
the relation between the two.

## What a complete answer contains

1. A proof of the boxed identity in both directions. An upper bound alone is
   not the claim.
2. The explicit arithmetic for Part 2, with the digit counts.
3. For Part 3, the inequality connecting the forward and backward errors, and
   an explanation of which of the two a user actually cares about.
