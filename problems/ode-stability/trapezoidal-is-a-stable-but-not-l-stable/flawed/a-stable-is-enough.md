# Flawed solution: `a-stable-is-enough`

## The submitted argument

> **Steps 1-2.** [$R(z) = (1+z/2)/(1-z/2)$ derived and A-stability proved
> correctly.]
>
> **Step 3.** A-stability means the method is stable for every step size on any
> problem with $\operatorname{Re}\lambda \le 0$. There is therefore no step
> restriction.
>
> **Step 4.** So for a stiff problem the step can be chosen purely by accuracy
> considerations for the slow components, and the trapezoidal rule, being
> second order unlike implicit Euler, is strictly the better choice.
>
> **Step 5.** Part 3 has no counterexample: the method handles
> $\lambda = -10^{6}$, $h = 0.1$ without difficulty.

## Where it breaks

**Step 4-5**, which read A-stability as "handles stiff problems well".
A-stability is the statement $|R(z)| \le 1$ on the left half-plane, i.e. *the
numerical solution does not grow*. That is a necessary condition and not a
sufficient one.

What a stiff transient requires is that it be **damped**, matching $e^{\lambda
t} \to 0$ rapidly. That needs $|R(z)| \to 0$ as $z \to -\infty$, which is
L-stability and which the trapezoidal rule does not have:

$$\lim_{z\to-\infty}R(z) = -1 .$$

## What Step 5 would have found

$\lambda = -10^{6}$, $h = 0.1$, $z = -10^{5}$, $R(z) = -0.99996$:

| $n$ | $y_n$ | exact |
|---|---|---|
| 1 | $-1.0000$ | $\sim10^{-43429}$ |
| 2 | $+0.9999$ | $\sim10^{-86859}$ |
| 3 | $-0.9999$ | $\ldots$ |
| 8 | $+0.9997$ | $\ldots$ |

The exact solution is zero to any precision after one step; the numerical one
oscillates at amplitude 1 and decays by $4\times10^{-5}$ per step. Step 3 is
correct (nothing is unstable, $|R| < 1$, the solution is bounded) and Step 4 is
false.

## The deeper point

The failure is not caught by any stability-based error control, because the
solution is bounded and A-stability is genuinely not violated. A step-size
controller based on local error estimates *will* shrink the step, which is the
usual symptom: a code that is "A-stable so has no step restriction" ends up
taking tiny steps anyway, for a reason its author did not predict.

And the artefact **worsens with stiffness**: the stiffer the mode, the closer
$R$ is to $-1$ and the longer the oscillation persists. That is the opposite of
the behaviour Step 4 expects.

## The two properties, kept apart

| property | statement | ensures |
|---|---|---|
| A-stable | $|R(z)| \le 1$ on $\operatorname{Re}z \le 0$ | the solution does not **grow** |
| L-stable | A-stable and $R(z)\to0$ as $z\to-\infty$ | stiff transients are **damped** |

Step 4's conclusion (second order beats first order) is right on the slow
components and wrong on the transient, which is exactly why TR-BDF2 exists.

## Failure mode

`necessary-mistaken-for-sufficient`: a necessary condition for good stiff
behaviour is treated as sufficient, and the stronger property that is actually
needed is not named.
