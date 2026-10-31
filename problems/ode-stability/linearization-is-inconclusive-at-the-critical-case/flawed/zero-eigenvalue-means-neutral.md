# Flawed solution: `zero-eigenvalue-means-neutral`

## The submitted argument

> **Step 1.** For $\dot x = \pm x^3$ the Jacobian at $0$ is $J = 0$, with the
> single eigenvalue $\lambda = 0$.
>
> **Step 2.** An eigenvalue with negative real part means decay, positive means
> growth. Zero real part means neither: the mode is neutral.
>
> **Step 3.** So both systems are **neutrally stable** at the origin:
> trajectories neither approach nor leave, to leading order.
>
> **Step 4.** Hence no such pair as Part 1 asks for exists — systems with the
> same linearisation have the same stability type.

## Where it breaks

**Step 2-3**, which transfer a property of the linear system to the nonlinear
one. The reasoning in Step 2 is a correct description of $\dot\xi = \lambda\xi$,
and $\lambda = 0$ does give $\xi(t) \equiv \xi(0)$. What does not follow is that
the *nonlinear* system behaves that way.

This is exactly the clause of Lyapunov's first method that says **no
conclusion**. The theorem's hypothesis — every eigenvalue off the imaginary
axis — fails, and the submission proceeds as though a third conclusion were
available.

## The witness

$$\dot x = -x^3: \quad x(t) = \frac{x_0}{\sqrt{1+2x_0^2t}} \to 0
\qquad\text{(asymptotically stable)}$$

$$\dot x = +x^3: \quad x(t) = \frac{x_0}{\sqrt{1-2x_0^2t}} \to \infty
\ \text{ at } t^{*} = \frac{1}{2x_0^2}
\qquad\text{(blows up in finite time)}$$

Same equilibrium, same Jacobian, same eigenvalue, same Taylor expansion to
second order. One decays, the other escapes to infinity in finite time.
Step 3's "neither approach nor leave" is wrong for both.

## Why the intuition is appealing

For a *hyperbolic* equilibrium the intuition is sound and is a theorem
(Hartman-Grobman: the flow is locally topologically conjugate to its
linearisation). The critical case is precisely where that conjugacy fails, and
the higher-order terms become the entire story — here the cubic term, which
the linearisation discards by construction.

## The check

Ask which term in the Taylor expansion the conclusion depends on. If the answer
is "a term the linearisation discarded", the linearisation cannot supply the
conclusion. For $\pm x^3$ the two systems agree through second order, so any
criterion that decides between them must look at the third.

## Failure mode

`linearisation-outside-its-hypothesis`: the third clause of Lyapunov's first
method ("no conclusion") is read as a third conclusion ("neutral").
