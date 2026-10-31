# The condition number is not a property of the linear map

## Assumptions

$A \in \mathbb{R}^{n\times n}$ nonsingular; $D$ ranges over nonsingular
diagonal matrices. $\kappa_p(A) = \|A\|_p\|A^{-1}\|_p$.

## Part 1 (existential)

Exhibit a fixed nonsingular $A$ and a family $D_t$ such that
$\kappa_2(D_tA) \to \infty$ as $t \to \infty$. Conclude that $\kappa_2$ is not
determined by the linear map $x \mapsto Ax$ up to the obvious equivalences ---
the systems $Ax = b$ and $(DA)x = Db$ have **exactly the same solution set**.

## Part 2 (universal)

Let $A$ have rows $a_i^{\mathsf T}$ and let $D_{\mathrm{eq}}$ be the row
equilibration $(D_{\mathrm{eq}})_{ii} = 1/\|a_i\|_\infty$, so every row of
$D_{\mathrm{eq}}A$ has $\infty$-norm 1. **Van der Sluis (1969)**:

$$\kappa_\infty(D_{\mathrm{eq}}A)
  \le n \min_{D \text{ diagonal}} \kappa_\infty(DA).$$

Prove the statement for the analogous row-scaling result in the $\infty$-norm,
or give a careful proof sketch with the key inequality identified.

## Part 3

If $\kappa$ can be moved at will, what is left? Define the **Skeel
(componentwise) condition number**

$$\operatorname{cond}(A) := \big\| \,|A^{-1}|\,|A|\, \big\|_\infty ,$$

where $|\cdot|$ is entrywise. Prove that $\operatorname{cond}(DA) =
\operatorname{cond}(A)$ for every nonsingular diagonal $D$, and say what this
means for a solver.

## What a complete answer contains

1. An explicit $A$, $D_t$ and the resulting $\kappa_2$ in closed form.
2. The statement of van der Sluis with the factor $n$ in the right place, and
   an explicit note that it is a *bound*, not optimality.
3. A proof of the invariance in Part 3 --- it is three lines and it is the
   point of the problem.
