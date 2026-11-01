# Flawed solution: `continuity-is-enough`

## The submitted argument

> **Step 1.** The eigenvalues of a matrix are the roots of its characteristic
> polynomial, whose coefficients are polynomials in the entries.
>
> **Step 2.** The roots of a polynomial depend continuously on its
> coefficients. Hence the eigenvalues depend continuously on the entries of the
> matrix.
>
> **Step 3.** A continuous function of the entries is well conditioned: small
> changes in the input produce small changes in the output.
>
> **Step 4.** So $|\lambda_k(A+E) - \lambda_k(A)| \le \|E\|_2$, and the
> Hermitian hypothesis was never needed.

## Where it breaks

**Step 3**, which equates continuity with a Lipschitz constant.

Steps 1 and 2 are correct, and importantly they are correct for **every**
matrix, Hermitian or not. That is precisely why they cannot prove a statement
that is false for non-Hermitian matrices: an argument that never uses a
hypothesis cannot establish a conclusion that needs it.

Continuity says the change tends to zero as the perturbation does. It says
nothing about the *rate*. The function $x \mapsto x^{1/n}$ is continuous at 0
and has unbounded derivative there, and that is exactly the behaviour the
Jordan block exhibits:

$$J_n(0) + \epsilon e_ne_1^{\mathsf T} \quad\text{has eigenvalues}\quad
  |\lambda| = \epsilon^{1/n}.$$

At $n = 16$ and $\epsilon = 10^{-16}$ (a perturbation at the level of double
rounding) the eigenvalues move to $|\lambda| = 0.1$. The map is continuous and
the Lipschitz constant on any neighbourhood of 0 is infinite.

## The scale of the gap

| $n$ | $\epsilon$ | $\|\Delta\lambda\|$ | ratio to $\epsilon$ |
|---|---|---|---|
| 2 | $10^{-16}$ | $10^{-8}$ | $10^{8}$ |
| 8 | $10^{-16}$ | $10^{-2}$ | $10^{14}$ |
| 16 | $10^{-16}$ | $10^{-1}$ | $10^{15}$ |

Step 4 claims a ratio of at most 1.

## What a correct proof must do

It must use the hypothesis. The Courant-Fischer proof uses Hermiticity twice:
for the min-max characterisation itself, and for $\|E\|_2 =
\max_i|\lambda_i(E)|$. A proof of Weyl's inequality that mentions neither has
gone wrong somewhere, and the cheapest way to find out is to ask which step
would fail for $J_n(0)$.

## Failure mode

`continuity-is-not-conditioning`: continuity is used where a modulus of
continuity is needed, so a result that holds for all matrices is made to carry
a conclusion that holds only for normal ones.
