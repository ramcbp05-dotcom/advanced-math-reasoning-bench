# Flawed solution: `determinant-as-proxy`

## The submitted argument

> **Step 1.** By the SVD, $\|A\|_2 = \sigma_1$.
>
> **Step 2.** $A^{-1}$ exists because $A$ is nonsingular.
>
> **Step 3.** For the inverse we use $A^{-1} = \dfrac{\operatorname{adj}(A)}{\det A}$,
> so $\|A^{-1}\|_2 = \dfrac{1}{|\det A|}$.
>
> **Step 4.** Therefore $\kappa_2(A) = \dfrac{\sigma_1}{|\det A|}$, and since
> $\sigma_1$ is bounded for a matrix with bounded entries, $\kappa_2$ is large
> precisely when $|\det A|$ is small.
>
> **Step 5.** Hence statement (a) is true and statement (b) is true.

## Where it breaks

**Step 3.** The identity $A^{-1} = \operatorname{adj}(A)/\det A$ is correct.
Taking the norm of both sides gives

$$\|A^{-1}\|_2 = \frac{\|\operatorname{adj}(A)\|_2}{|\det A|},$$

and the submitted argument silently drops $\|\operatorname{adj}(A)\|_2$, i.e.
asserts that it equals 1. That is true only for $n = 1$, where the adjugate is
the $1\times 1$ matrix $(1)$.

The dropped factor is not a detail; it carries the entire result. For the
witness $A = \operatorname{diag}(10^5, 10^{-5})$ we have
$\operatorname{adj}(A) = \operatorname{diag}(10^{-5}, 10^{5})$, so
$\|\operatorname{adj}(A)\|_2 = 10^{5}$, and

$$\|A^{-1}\|_2 = \frac{10^{5}}{1} = 10^{5},$$

which is right, against the claimed $1/|\det A| = 1$. The error is a factor of
$10^5$.

## Why it is a tempting error

The $n = 1$ case is correct, and for $2\times2$ matrices with entries of order
1 the adjugate also has entries of order 1, so Step 3 is *numerically* close
for a large family of hand-written examples. The approximation degrades exactly
when the singular values spread out --- which is the regime the problem is
about.

## The structural objection

Step 4 can be rejected without computing anything. $\kappa_2(cA) = \kappa_2(A)$
for every $c \neq 0$ (Corollary 2), while
$\sigma_1(cA)/|\det(cA)| = |c|^{1-n}\sigma_1(A)/|\det A|$. The claimed formula
is not scale invariant and the quantity it claims to equal is, so for $n \ge 2$
it is wrong for every matrix at once, not merely in bad cases.

Checking a claimed identity against a symmetry the left-hand side is known to
have is cheap, and it would have caught this before any example was tried.

## Failure mode

`invalid-identity`: a correct identity is used with a factor silently set to 1.
