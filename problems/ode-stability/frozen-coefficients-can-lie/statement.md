# Frozen-time eigenvalues do not determine stability

## Assumptions

Consider the linear time-varying system

$$\dot x = A(t)\,x, \qquad x \in \mathbb{R}^2 ,$$

with $A : \mathbb{R} \to \mathbb{R}^{2\times2}$ continuous and bounded.

**The constant-coefficient theorem (quoted).** If $A$ is constant and every
eigenvalue of $A$ has strictly negative real part, then the origin is globally
exponentially stable.

## Part 1 (existential)

Decide the following, and prove your answer:

> If $A(t)$ is bounded and **every eigenvalue of $A(t)$ has real part
> $\le -\alpha < 0$ for every $t$**, is the origin of $\dot x = A(t)x$
> asymptotically stable?

If the answer is no, exhibit an explicit $A(t)$ with:

* eigenvalues independent of $t$, both with strictly negative real part;
* an **exact** solution that is unbounded.

Verify the solution by substitution, not numerically.

## Part 2

For your witness, compute:

1. the eigenvalues of $A(t)$ in closed form, and confirm they do not depend on
   $t$;
2. the trace of $A(t)$, and reconcile its sign with the growth (use the
   Abel-Jacobi-Liouville formula $\det\Phi(t) =
   \det\Phi(0)\exp\int_0^t\operatorname{tr}A(s)\,ds$ for the fundamental matrix
   $\Phi$).

## Part 3

Explain the mechanism. Why can a solution grow when every instantaneous
eigenvalue decays? Identify the geometric quantity the frozen-eigenvalue
criterion ignores.

## Part 4

A tempting repair: "the criterion is valid if $A(t)$ varies **slowly enough**."
Decide whether the witness can be ruled out this way, by considering
$A_\varepsilon(t) := \varepsilon A(\varepsilon t)$.

Then state a criterion that **does** work for time-varying systems.

## What a complete answer contains

1. An explicit $A(t)$ and an exact solution, verified by substitution.
2. Both computations in Part 2, with the trace sign explained rather than waved
   at.
3. A mechanism in Part 3 naming the ignored quantity.
4. A correct treatment of Part 4: the rescaling computed, not asserted.
