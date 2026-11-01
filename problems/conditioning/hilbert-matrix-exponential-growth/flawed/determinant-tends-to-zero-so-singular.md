# Flawed solution: `determinant-tends-to-zero-so-singular`

## The submitted argument

> **Step 1.** The Cauchy formula gives $\det H_n > 0$ for all $n$, and the
> values fall off very fast: $\det H_{12} \approx 2.6\times10^{-78}$.
>
> **Step 2.** Since $\det H_n \to 0$ as $n \to \infty$, the Hilbert matrix
> becomes singular in the limit.
>
> **Step 3.** A matrix near a singular matrix is ill-conditioned, so
> $\kappa_2(H_n) \to \infty$, which is what was to be shown.

## Where it breaks

**Step 2**, in two independent ways.

**(i) There is no limit to take.** $H_n$ is $n\times n$: the members of the
sequence live in different spaces. "The Hilbert matrix becomes singular in the
limit" has no referent. The infinite Hilbert *operator* on $\ell^2$ does exist
and is a bounded self-adjoint operator with spectrum $[0,\pi]$ (the Hilbert
matrix inequality), so it is not invertible: but that is a theorem about an
operator, obtained by a different argument, and nothing in Step 2 establishes
it.

**(ii) Within a fixed size, the inference is false anyway.** A small
determinant does not imply ill-conditioning:

$$B = 10^{-5}I_2 : \quad \det B = 10^{-10}, \quad \kappa_2(B) = 1 .$$

This is settled in `cond2-is-singular-value-ratio`. The determinant is the
*product* of the eigenvalues, so it is small whenever the eigenvalues are
collectively small, which is a statement about scale and not about
conditioning.

**Step 3** compounds it. "Near a singular matrix" is correct as a criterion,
but the right measure of nearness is $\sigma_n$ relative to $\sigma_1$: the
Eckart-Young distance to singularity is $\sigma_n$, and the *relative* distance
is $1/\kappa_2$. The determinant does not appear.

## Why the conclusion is nonetheless true

$\kappa_2(H_n)$ does grow like $(1+\sqrt2)^{4n}$, and that makes this a
particularly instructive flawed solution: the final claim is correct and
everything that leads to it is wrong. A reviewer checking the conclusion
against a reference finds agreement and moves on.

The working route is through $\|H_n^{-1}\|$. The entries of $H_n^{-1}$ are
integers growing like $16^n$, and $\|H_n^{-1}\|_2 \ge
\max_{ij}|(H_n^{-1})_{ij}|$, which at $n = 12$ is already $3.7\times10^{15}$.
Combined with $\|H_n\|_2 < \pi$ for all $n$, that gives the lower bound on
$\kappa_2$ directly, with no appeal to the determinant.

## The two-line disproof of Step 2

Take $A_n = \tfrac12 I_n$. Then $\det A_n = 2^{-n} \to 0$ while $\kappa_2(A_n)
= 1$ for every $n$. Any argument of the form "det $\to 0$ therefore
ill-conditioned" must reject this, and it cannot.

## Failure mode

`limit-of-determinants`: a determinant tending to zero is read as approaching
singularity, across a sequence whose members do not even share a space.
