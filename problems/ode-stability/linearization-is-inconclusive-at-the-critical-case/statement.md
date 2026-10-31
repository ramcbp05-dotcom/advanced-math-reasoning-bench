# Linearisation decides nothing when the linear part is marginal

## Assumptions

Consider the autonomous system $\dot x = f(x)$, $f \in C^1$, with an
equilibrium $f(x_0) = 0$, and let $J = Df(x_0)$.

**Lyapunov's first method (quoted).**

* If every eigenvalue of $J$ has **strictly negative** real part, $x_0$ is
  locally asymptotically stable.
* If some eigenvalue has **strictly positive** real part, $x_0$ is unstable.
* If some eigenvalue has real part **exactly zero** and none has positive real
  part, the method gives **no conclusion**.

The first two cases are the *hyperbolic* case; the third is the **critical
case**.

## Part 1 (existential)

Show the third clause cannot be improved: exhibit two scalar systems with the
**same** equilibrium and the **same** linearisation, one of which is
asymptotically stable and the other unstable.

Solve both in closed form.

## Part 2

For the unstable member of your pair, show the solution blows up in **finite
time** and compute the blow-up time $t^{*}$ as a function of $x(0)$.

## Part 3

For the stable member, show the decay is **not exponential**: find the exact
rate and contrast it with what a hyperbolic equilibrium would give.

## Part 4

Give a two-dimensional example in which the linearisation is a centre
(eigenvalues $\pm i$) and the true behaviour is asymptotic stability, so the
critical case is not an artefact of one dimension.

## What a complete answer contains

1. Closed-form solutions of both scalar equations, by separation of variables.
2. The blow-up time with its derivation.
3. The algebraic decay rate, stated as a power of $t$.
4. For Part 4, the system, its Jacobian, and an argument that settles the true
   behaviour (a Lyapunov function suffices).
