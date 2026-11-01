# Flawed solution: `bound-is-the-answer`

## The submitted argument

> **Steps 1-3.** [Bauer-Fike proved correctly, and sharpness demonstrated in
> Part 2.]
>
> **Step 4.** For Part 3, the family $A_t$ with
> $E = \delta\operatorname{diag}(1,-1)$ has $\kappa_2(V_t) \approx 2t$, so the
> eigenvalue shift is $\kappa_2(V_t)\delta$. At $t = 10^{8}$ and
> $\delta = 10^{-10}$ that is $2\times10^{-2}$.
>
> **Step 5.** So yes, the true shift grows with $t$, reaching $2\%$ at
> $t = 10^{8}$.

## Where it breaks

**Step 4**, at "so the eigenvalue shift **is**". Bauer-Fike gives
$\min_i|\mu-\lambda_i| \le \kappa_2(V)\|E\|_2$: an upper bound, with no
accompanying lower bound.

For this particular $E$ the eigenvalues of $A_t + E$ are exactly $1 + \delta$
and $2 - \delta$, independent of $t$:

| $t$ | bound | actual shift | over-estimate |
|---|---|---|---|
| $10^{2}$ | $2.0\times10^{-8}$ | $10^{-10}$ | $\times 2.0\times10^{2}$ |
| $10^{8}$ | $2.0\times10^{-2}$ | $10^{-10}$ | $\times 2.0\times10^{8}$ |

Step 5's "2 %" is wrong by eight orders of magnitude.

## Why this is not merely conservative

A bound that over-estimates by $10^{8}$ is not a cautious answer; it carries no
information. "The eigenvalues moved by at most 2 %" is true and useless when
they moved by $10^{-10}$, and a user acting on it would discard a perfectly
accurate computation.

The structural point is that Bauer-Fike is a **worst case over all $E$ of a
given norm**. It answers "how much could a perturbation this size do?", not
"how much did *this* perturbation do?". Part 2 of the problem exhibits an $E$
that attains it, which is what makes the theorem sharp as a statement about the
worst case: and that same sharpness is why it must be loose for other $E$.

## What to do instead

Three options, in increasing order of effort:

1. **Measure.** The eigenvalues of $A + E$ are computable; if $E$ is known
   there is no need for a bound at all.
2. **Use the per-eigenvalue condition numbers** $1/|y_i^{*}x_i|$, which are
   individual rather than global and often much smaller than $\kappa_2(V)$.
3. **Compute the pseudospectrum** if the question really is about all
   perturbations of a given size, which is what Bauer-Fike approximates.

## Failure mode

`bound-reported-as-estimate`: `<=` is read as `~`, and a worst-case guarantee
is quoted as a prediction for a specific case.
