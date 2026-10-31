# Flawed solution: `frobenius-substitution`

## The submitted argument

> **Step 1.** Compute $\|A\|$ and $\|A^{-1}\|$ and multiply.
>
> **Step 2.** The matrix norm is $\|A\| = \sqrt{\sum_{ij}|a_{ij}|^2}$, and by
> the SVD this equals $\sigma_1$.
>
> **Step 3.** Likewise $\|A^{-1}\| = 1/\sigma_n$, so
> $\kappa(A) = \sigma_1/\sigma_n$, proving Part 1.
>
> **Step 4.** For Part 2, $A = \operatorname{diag}(10^5, 10^{-5})$ gives
> $\|A\|_F = \sqrt{10^{10} + 10^{-10}} \approx 10^5$ and
> $\|A^{-1}\|_F \approx 10^5$, so $\kappa \approx 10^{10}$ and (a) is false.

## Where it breaks

**Step 2.** The quantity defined there is the **Frobenius** norm, and the SVD
gives

$$\|A\|_F = \Big(\sum_{i=1}^{n}\sigma_i^2\Big)^{1/2},$$

not $\sigma_1$. The two coincide exactly when all singular values beyond the
first vanish, i.e. when $\operatorname{rank}(A) \le 1$.

The error is bounded, which is why it survives: for all $A$,

$$\sigma_1 \le \|A\|_F \le \sqrt{n}\,\sigma_1 ,$$

so in the Frobenius norm the computed condition number satisfies

$$\frac{\sigma_1}{\sigma_n} \le \|A\|_F\|A^{-1}\|_F \le n\,\frac{\sigma_1}{\sigma_n}.$$

For $n = 2$ that is a factor of at most 2 --- which is why the *conclusion* of
Step 4 is nonetheless correct.

## Why this one is worse than being wrong

Step 4 reaches the right answer. $\kappa_F \approx 10^{10}$ and
$\kappa_2 = 10^{10}$ agree to the precision quoted, because the witness has
$\sigma_2/\sigma_1 = 10^{-10}$ and the extra terms are negligible. A reviewer
checking the final number against a reference implementation sees agreement.

What is wrong is **Step 3**, which claims to have *proved* the boxed identity
and has not: it has proved an inequality within a factor of $n$. The submission
is a correct answer resting on a false lemma, and the lemma is the part that
would be reused.

## The check that catches it

Evaluate both quantities on a matrix with several comparable singular values,
where the factor of $n$ is visible. For $A = I_3$:

$$\|A\|_F\|A^{-1}\|_F = \sqrt3 \cdot \sqrt3 = 3,
\qquad \frac{\sigma_1}{\sigma_3} = 1 .$$

The identity claimed in Step 3 would make these equal. The identity matrix is
the first thing to try against any claimed norm identity, and it costs nothing.

## Failure mode

`wrong-norm`: a statement true for one norm is asserted for another, and the
final numerical answer happens not to depend on the difference.
