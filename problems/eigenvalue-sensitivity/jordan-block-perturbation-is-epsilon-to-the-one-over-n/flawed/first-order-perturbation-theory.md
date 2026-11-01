# Flawed solution: `first-order-perturbation-theory`

## The submitted argument

> **Step 1.** Perturbation theory for eigenvalues gives
> $\delta\lambda = \dfrac{y^{*}Ex}{y^{*}x}$ to first order.
>
> **Step 2.** Here $E = \epsilon\,e_ne_1^{\mathsf T}$, with $\|E\|_2 = \epsilon$.
>
> **Step 3.** Taking unit $x$ and $y$, the condition number $1/|y^{*}x|$ is some
> finite constant $C$ depending on $n$ but not on $\epsilon$, so
> $|\delta\lambda| \le C\epsilon$.
>
> **Step 4.** Therefore the eigenvalues move by $O(\epsilon)$: at
> $\epsilon = 10^{-16}$, by about $10^{-16}$ times a modest constant.

## Where it breaks

**Step 3**, at "some finite constant $C$".

The right eigenvector of $J_n$ for $\lambda = 0$ is $x = e_1$ and the left
eigenvector is $y = e_n$. Therefore

$$y^{*}x = e_n^{\mathsf T}e_1 = 0 ,$$

and $C = 1/|y^{*}x|$ is **infinite**. Step 1's formula divides by zero, so
Steps 3 and 4 are not approximations with a large constant: they are statements
about an expansion that does not exist.

The underlying hypothesis, left unstated in Step 1, is that the eigenvalue is
**simple**. Here it has algebraic multiplicity $n$ and geometric multiplicity
1.

## How wrong the conclusion is

The exact answer is $|\lambda| = \epsilon^{1/n}$:

| $n$ | predicted by Step 4 | actual |
|---|---|---|
| 2 | $\sim10^{-16}$ | $10^{-8}$ |
| 8 | $\sim10^{-16}$ | $10^{-2}$ |
| 16 | $\sim10^{-16}$ | $10^{-1}$ |

Off by fifteen orders of magnitude at $n = 16$.

## The check that catches it

Compute $y^{*}x$ before using the formula. It costs one inner product, it is
the quantity the formula divides by, and it is exactly the diagnostic for the
situation: $y^{*}x \to 0$ means a defective eigenvalue is being approached and
the expansion is losing validity continuously as it does.

## The correct statement

At a defective eigenvalue the expansion is a **Puiseux series** in $t^{1/n}$,
not a Taylor series in $t$:

$$\lambda(t) = \lambda_0 + c_1t^{1/n} + \cdots$$

$d\lambda/dt$ is unbounded at $t = 0$. "Infinite condition number" is the
statement that the function is not differentiable there, not that a large
constant has been encountered.

## Failure mode

`expansion-invalid-at-a-defective-eigenvalue`: a first-order expansion valid
for simple eigenvalues is applied where the quantity it divides by is exactly
zero.
