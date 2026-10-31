# Bauer-Fike, and the regime where it says nothing

## Assumptions

$A \in \mathbb{C}^{n\times n}$ **diagonalisable**, $A = V\Lambda V^{-1}$ with
$\Lambda = \operatorname{diag}(\lambda_1,\dots,\lambda_n)$. $E$ arbitrary.

## Part 1

Prove the **Bauer-Fike theorem**: every eigenvalue $\mu$ of $A + E$ satisfies

$$\boxed{\ \min_{i}|\mu - \lambda_i| \;\le\; \kappa_2(V)\,\|E\|_2\ }$$

Suggested route: if $\mu \notin \operatorname{spec}(A)$ then
$\mu I - \Lambda$ is invertible; factor $\mu I - A - E$ and use that a singular
matrix has a vector in its null space.

## Part 2 (sharpness)

Show the bound is attained up to a constant: exhibit $A$, $E$ for which
$\min_i|\mu - \lambda_i|$ is of the same order as $\kappa_2(V)\|E\|_2$.

## Part 3 (degeneration)

Exhibit a family $A_t$, diagonalisable for every $t$, with
$\kappa_2(V_t) \to \infty$, such that for a **fixed** $\|E\|_2$ the Bauer-Fike
bound tends to infinity. Then answer: in that family, does the true eigenvalue
shift also grow? Decide, with evidence.

## Part 4 (no content)

What does Bauer-Fike assert for the nilpotent Jordan block $J_n$? State the
answer precisely, and explain what a numerical library's `eig` returns for `V`
in that case and why the resulting "bound" is meaningless.

## What a complete answer contains

1. A complete proof of Part 1, including the case $\mu \in \operatorname{spec}(A)$.
2. An attaining example for Part 2.
3. For Part 3, both the bound and the measured shift, so the gap is visible.
4. For Part 4, the precise statement — not "the bound is large" but what the
   theorem does and does not assert.
