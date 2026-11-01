# Flawed solution: `equilibration-is-optimal`

## The submitted argument

> **Steps 1-3.** [Part 1 answered correctly with an explicit witness.]
>
> **Step 4.** Van der Sluis's theorem states
> $\kappa_\infty(D_{\mathrm{eq}}A) \le n\min_D \kappa_\infty(DA)$.
>
> **Step 5.** Therefore row equilibration achieves the minimum condition number
> over all diagonal scalings, and the right thing for a solver to do is always
> to equilibrate.

## Where it breaks

**Step 5.** The theorem bounds equilibration *within a factor of $n$* of the
optimum. It does not say equilibration attains the optimum, and in general it
does not.

A factor of $n$ is not nothing: at $n = 1000$ it is three digits. What the
theorem buys is the guarantee that equilibration cannot be *arbitrarily* worse
than the best scaling: which is the useful statement, because the alternative
to a guarantee is an unbounded loss.

## A concrete gap

Take $A = \operatorname{diag}(1,
\epsilon)\begin{pmatrix}1&1\\1&-1\end{pmatrix}$. Row equilibration divides row
2 by $\epsilon$, recovering the orthogonal factor and giving $\kappa_\infty =
2$: here equilibration is essentially optimal. Now take a matrix whose rows are
not merely scaled copies of a well-conditioned system, and the optimum is
attained by a different $D$: the minimisation $\min_D \kappa_\infty(DA)$ is a
genuine convex program in $\log D$ (it is a min-max of linear functions of
$\log d_i$) and its solution is not given by any closed-form rule on the row
norms.

## The second, quieter error in Step 5

"The right thing for a solver to do is always to equilibrate" is also false,
for a reason unrelated to optimality. Equilibration changes the *perturbation
model*: it makes the backward error small relative to the scaled rows, which is
what the user wants only if the original row scaling carried no information. If
row 2 is measured in different physical units with genuinely smaller absolute
uncertainty, equilibrating discards that and the scaled backward error no
longer corresponds to anything the user cares about.

This is why LAPACK's expert drivers *return* the scaling factors rather than
applying them silently.

## Failure mode

`bound-read-as-optimality`: a theorem of the form "within a factor of $n$ of
the best" is restated as "the best".
