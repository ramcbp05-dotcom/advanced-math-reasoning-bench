# Flawed solution: `submultiplicative-bound-as-equality`

## The submitted argument

> **Step 1.** $\kappa_2(M) = \|M\|_2\|M^{-1}\|_2$ for nonsingular $M$.
>
> **Step 2.** Apply submultiplicativity to $M = A^{\mathsf T}A$:
> $$\|A^{\mathsf T}A\|_2 \le \|A^{\mathsf T}\|_2\|A\|_2,
>   \qquad \|(A^{\mathsf T}A)^{-1}\|_2 \le \|A^{-1}\|_2\|A^{-\mathsf T}\|_2 .$$
>
> **Step 3.** Multiplying and using $\|A^{\mathsf T}\|_2 = \|A\|_2$,
> $$\kappa_2(A^{\mathsf T}A) \le \kappa_2(A)^2 .$$
>
> **Step 4.** Hence $\kappa_2(A^{\mathsf T}A) = \kappa_2(A)^2$, as required.

## Where it breaks

**Step 4**, which upgrades an inequality to an equality with no further
argument. Steps 1 to 3 are all correct.

The gap is not cosmetic, and it is the half of the statement that carries the
practical content. The inequality alone leaves open that some matrices have
$\kappa_2(A^{\mathsf T}A) \ll \kappa_2(A)^2$ --- and if that were so, the normal
equations would be a perfectly good method for those matrices, and the problem
would be to characterise them. The identity says no such matrices exist: the
squaring happens for **every** full-rank $A$, with no exceptions to look for.

## What the missing half requires

The reverse inequality does not follow from the norm axioms. Submultiplicativity
is an inequality by nature, and there are matrices for which it is strict ---
e.g. $\|AB\|_2 \ll \|A\|_2\|B\|_2$ when the range of $B$ avoids the dominant
right singular subspace of $A$. The argument has to use the *specific* structure
$A^{\mathsf T}A$, which it does through the SVD:

$$A = U\Sigma V^{\mathsf T} \implies A^{\mathsf T}A = V\Sigma^2V^{\mathsf T},$$

so the eigenvalues are exactly $\sigma_i^2$, with no inequality anywhere. The
equality is then immediate.

## A smaller version of the same mistake

Submultiplicativity applied to $\kappa$ gives
$\kappa(AB) \le \kappa(A)\kappa(B)$, and this is genuinely strict in general:
for $A = \operatorname{diag}(1, \epsilon)$ and
$B = \operatorname{diag}(\epsilon, 1)$ we have
$\kappa(A) = \kappa(B) = 1/\epsilon$ while $AB = \epsilon I$ has
$\kappa(AB) = 1$. So the bound in Step 3 can be loose by a factor of
$\epsilon^{-2}$ for a general product, and it is only the symmetry of
$A^{\mathsf T}A$ that makes it tight.

Producing that example is the fastest way to see that Step 4 needs its own
argument.

## Failure mode

`inequality-reported-as-equality`: a bound is derived and the conclusion is
stated as an identity, discarding the half of the claim with the content.
