# Flawed solution: `conditioning-is-intrinsic`

## The submitted argument

> **Step 1.** $\kappa(A)$ measures how much a relative perturbation of the data
> can be amplified in the solution. This is a statement about the problem
> $Ax = b$.
>
> **Step 2.** Multiplying row $i$ by $t$ turns $Ax = b$ into $(DA)x = Db$, which
> has the same solution set. Since the problem is unchanged, its sensitivity is
> unchanged, so $\kappa(DA) = \kappa(A)$.
>
> **Step 3.** Any apparent change in $\kappa$ under row scaling must therefore
> be a numerical artefact of how $\kappa$ is estimated.
>
> **Step 4.** Hence Part 1 has no counterexample.

## Where it breaks

**Step 2**, and the break is conceptual rather than algebraic. The two
assertions in it are both true and do not combine:

* the solution *set* is unchanged: correct;
* therefore the *sensitivity* is unchanged: false.

Sensitivity is not a property of a solution set. It is a property of a solution
set **together with a perturbation model**, and the perturbation model is
attached to the entries. The relevant model is

$$|\delta a_{ij}| \le \epsilon\,|a_{ij}| \quad\text{or}\quad
  \|\delta A\| \le \epsilon\|A\| ,$$

and the second of these is *not* preserved by row scaling: a perturbation small
relative to $\|A\|$ becomes, after scaling row 2 by $10^{8}$, a perturbation
that is large relative to row 1 and negligible relative to row 2.

So the scaled system really is a different numerical problem, even though it is
the same mathematical one. Step 3 is then false as well: the change in $\kappa$
is exact, not an estimation artefact, and `verify.py` computes it symbolically.

## The witness

$A = \begin{pmatrix}1&1\\1&1+10^{-8}\end{pmatrix}$ has $\kappa_2 =
4.0\times10^{8}$; scaling the second row by $10^{8}$ gives $\kappa_2 =
1.8\times10^{16}$. The solution of $Ax = b$ and of $(DA)x = Db$ agree exactly
in exact arithmetic. In floating point they do not, and the second is the one
that fails.

## What the submission was reaching for

There *is* a scaling-invariant sensitivity measure, and the problem asks for
it: the Skeel number $\operatorname{cond}(A) = \||A^{-1}||A|\|_\infty$, which
is provably unchanged by any diagonal row scaling. The intuition in Step 1 is
sound; it just belongs to a different quantity than the one named.

## Failure mode

`conflating-problem-with-representation`: a property of a representation is
argued to be a property of the object, by an argument that would be valid if
sensitivity depended only on the solution set.
