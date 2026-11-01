# Flawed solution: `stiffness-is-about-accuracy`

## The submitted argument

> **Steps 1-2.** [Stability region derived correctly as $|1+z| \le 1$.]
>
> **Step 3.** For the Part 2 system, the fast mode $e^{-10^6t}$ varies on a
> time scale of $10^{-6}$. To resolve it accurately the step must be small
> compared with that scale, so $h \approx 10^{-7}$ and $N \approx 10^{8}$
> steps.
>
> **Step 4.** Stiffness is therefore an accuracy requirement: a rapidly varying
> component needs a fine step to be represented.

## Where it breaks

**Step 3**, at "to resolve it accurately". The fast mode does not need
resolving, because by the time anything is being asked of the solution it has
**already decayed to nothing**:

$$e^{-10^{6}t}\Big|_{t = 10^{-4}} = e^{-100} \approx 10^{-44}.$$

Out of the interval $[0,10]$, the fast mode is non-negligible on roughly the
first $10^{-5}$: a fraction $10^{-6}$ of the integration. Its contribution to
the error over the rest is exactly zero to machine precision, so no accuracy
requirement it imposes can be binding.

The step restriction is nonetheless real, and it comes from $|1 +
h\lambda_{\text{fast}}| \le 1$, i.e. $h \le 2\times10^{-6}$. That is a
**stability** requirement: it exists to stop the dead mode from being
*amplified*, not to resolve it.

## Why the distinction matters

Step 4's diagnosis leads to the wrong remedy. If the problem were accuracy, the
answer would be a higher-order explicit method: going from order 1 to order 4
would buy a much larger step for the same error. It buys nothing here: **no
explicit Runge-Kutta method is A-stable**, because its $R(z)$ is a polynomial,
and a non-constant polynomial is unbounded, so its stability region is bounded
and a large enough $h|\lambda|$ always escapes it. RK4 on this system needs $h
\lesssim 2.78/10^{6}$ instead of $2/10^{6}$: a factor of 1.4.

The correct remedy is an **implicit** method, whose stability region is
unbounded. Implicit Euler or the trapezoidal rule integrates this system with
$h \approx 10^{-2}$, chosen purely by accuracy: $10^{3}$ steps against
$5\times10^{6}$.

| requirement | $h$ | steps to $t=10$ |
|---|---|---|
| accuracy (slow mode) | $10^{-2}$ | $10^{3}$ |
| explicit stability (fast mode) | $2\times10^{-6}$ | $5\times10^{6}$ |
| implicit Euler | $10^{-2}$ | $10^{3}$ |

## The test that separates the two causes

Integrate with a method that is A-stable and ask whether the large step is
still needed. If the answer is no, the restriction was stability. If a large
step remains inaccurate, it was accuracy. Here implicit Euler at $h = 10^{-2}$
gives a perfectly good answer, settling it.

## Failure mode

`wrong-cause-right-remedy`: the step restriction is correctly identified and
attributed to the wrong mechanism, so the proposed fix (higher order) does not
address it.
