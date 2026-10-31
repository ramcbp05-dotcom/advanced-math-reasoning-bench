# Flawed solution: `diagonalisable-is-enough`

## The submitted argument

> **Steps 1-3.** [Weyl proved correctly from Courant-Fischer.]
>
> **Step 4.** The essential ingredient is that $A$ has a complete eigenbasis:
> that is what lets each eigenvalue be isolated by a Rayleigh quotient. Any
> diagonalisable $A = V\Lambda V^{-1}$ has one.
>
> **Step 5.** Bauer-Fike confirms this, giving
> $\operatorname{dist}(\mu, \operatorname{spec}A) \le \kappa_2(V)\|E\|_2$ for
> diagonalisable $A$. Since $V$ is a basis of eigenvectors it can be normalised
> to have unit columns, so $\kappa_2(V)$ is $O(1)$.
>
> **Step 6.** Hence the Weyl bound holds for every diagonalisable matrix, and
> Hermiticity is a convenience rather than a necessity.

## Where it breaks

**Step 5**, at "normalised to have unit columns, so $\kappa_2(V)$ is $O(1)$."

Normalising the columns of $V$ makes $\|V\|_2 \le \sqrt n$. It does **nothing**
to $\|V^{-1}\|_2$, which is governed by how close the columns are to being
linearly dependent — i.e. by the *angles* between eigenvectors, not their
lengths. Two unit vectors at an angle $\theta$ give a matrix with
$\kappa_2 \approx 2/\theta$ as $\theta \to 0$, with no bound at all.

The hypothesis that makes $\kappa_2(V) = 1$ is that $V$ can be chosen
**unitary**, i.e. the eigenvectors are *orthogonal*. By the spectral theorem
that is exactly normality.

Step 4's intuition is also subtly wrong: Courant-Fischer does not merely need a
complete eigenbasis, it needs an *orthonormal* one, since it characterises
eigenvalues by a variational principle over orthogonal complements.

## The witness

$A_t = \begin{pmatrix}1 & t\\ 0 & 2\end{pmatrix}$ is diagonalisable for every
$t$ — its eigenvalues 1 and 2 are distinct, so a complete eigenbasis exists,
and the eigenvectors can be normalised to unit length as Step 5 proposes. Their
angle closes like $1/t$, and

| $t$ | $\kappa_2(V)$ | shift under $\|E\|_2 = 10^{-10}$ |
|---|---|---|
| $10^{2}$ | $2.0\times10^{2}$ | $1.0\times10^{-8}$ |
| $10^{4}$ | $2.0\times10^{4}$ | $1.0\times10^{-6}$ |
| $10^{6}$ | $2.0\times10^{6}$ | $1.0\times10^{-4}$ |

A shift of $10^{-4}$ from a perturbation of $10^{-10}$ is an amplification of
$10^{6}$, against the claimed 1. Step 6 is false by six orders of magnitude at
$t = 10^{6}$, and by any amount one likes at larger $t$.

## The distinction to keep

* **Diagonalisable** — a complete eigenbasis exists. Says nothing about
  conditioning.
* **Normal** — an *orthonormal* eigenbasis exists. Gives $\kappa_2(V) = 1$ and
  with it Weyl, Bauer-Fike with constant 1, and
  $\kappa_2(A) = |\lambda_1|/|\lambda_n|$.

Almost every "nice" property in numerical linear algebra follows from
normality, and almost none follows from diagonalisability.

## Failure mode

`wrong-hypothesis`: the correct hypothesis (normality) is weakened to a nearby
one (diagonalisability) that does not support the conclusion.
