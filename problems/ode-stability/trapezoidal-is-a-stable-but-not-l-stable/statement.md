# A-stability does not imply L-stability

## Assumptions

On the Dahlquist test equation $y' = \lambda y$, a one-step method has $y_{n+1}
= R(z)y_n$ with $z = h\lambda$.

* The method is **A-stable** if $|R(z)| \le 1$ for all $z$ with
  $\operatorname{Re}z \le 0$.
* It is **L-stable** if it is A-stable **and** $R(z) \to 0$ as $z \to -\infty$
  along the real axis.

The **trapezoidal rule** (Crank-Nicolson) is

$$y_{n+1} = y_n + \tfrac{h}{2}\big[f(t_n,y_n) + f(t_{n+1},y_{n+1})\big].$$

## Part 1

Compute $R(z)$ for the trapezoidal rule and prove it is **A-stable**, with
stability region **exactly** the closed left half-plane: not a subset of it,
and not a superset.

## Part 2

Prove the trapezoidal rule is **not L-stable** by computing
$\lim_{z\to-\infty}R(z)$.

## Part 3 (existential)

Exhibit the consequence. Integrate $y' = \lambda y$, $y(0) = 1$, with $\lambda
= -10^{6}$ and $h = 0.1$ (so $z = -10^{5}$) for eight steps. Report the
numerical solution and the exact solution, and describe the failure.

## Part 4

Contrast with implicit Euler, which is L-stable, and state the price it pays
(consider the order of accuracy of each method).

Then state what a practical stiff solver does about this.

## What a complete answer contains

1. $R(z)$ derived, and the region shown to be *exactly* the left half-plane
   (both inclusions).
2. The limit in Part 2.
3. The eight numbers in Part 3, next to the exact values.
4. The order of each method and the trade-off named.
