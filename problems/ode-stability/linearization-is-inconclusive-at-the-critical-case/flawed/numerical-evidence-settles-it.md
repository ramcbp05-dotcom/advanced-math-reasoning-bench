# Flawed solution: `numerical-evidence-settles-it`

## The submitted argument

> **Steps 1-2.** [The critical case correctly identified; the first method does
> not apply.]
>
> **Step 3.** Settle it numerically. Integrate $\dot x = x^3$ from several
> initial conditions with a high-accuracy solver (`RK45`, `rtol = 1e-10`) to
> $t = 5$:
>
> | $x_0$ | $x(5)$ |
> |---|---|
> | $0.1$ | $0.1054$ |
> | $0.01$ | $0.0100$ |
> | $0.001$ | $0.0010$ |
>
> **Step 4.** The solutions barely move, and the smaller the initial condition
> the less they move. The origin is therefore stable (marginally so), and the
> numerical evidence is conclusive.

## Where it breaks

**Step 4**, which reads a finite-horizon computation as an asymptotic
statement.

The exact solution is $x(t) = x_0/\sqrt{1 - 2x_0^2t}$, blowing up at

$$t^{*} = \frac{1}{2x_0^2}.$$

For the three initial conditions in the table:

| $x_0$ | $t^{*}$ | horizon used | fraction of $t^{*}$ reached |
|---|---|---|---|
| $0.1$ | $50$ | 5 | 10 % |
| $0.01$ | $5000$ | 5 | 0.1 % |
| $0.001$ | $500\,000$ | 5 | 0.001 % |

The computation stopped at 10 % of the blow-up time in the best case. Worse,
the *pattern* in Step 4 (smaller $x_0$ moves less) is exactly backwards as
evidence: it reflects $t^{*}$ growing like $x_0^{-2}$, so smaller initial data
pushes the blow-up further out and makes a fixed horizon less informative, not
more.

## Why a longer run would not have been enough either

$x(t) = x_0(1 - t/t^{*})^{-1/2}$, so at $t = 0.99t^{*}$ the solution is only
$10x_0$ and at $t = 0.9999t^{*}$ only $100x_0$. From $x_0 = 0.001$ that is
$0.1$: still small-looking. **The blow-up is invisible until the last fraction
of a percent of the time interval.** Any fixed horizon and any fixed "large
value" threshold can be defeated by choosing $x_0$ small enough.

An adaptive solver also does not raise an alarm: it reduces the step as the
solution steepens and returns successfully at whatever endpoint it was given.

## What numerics can and cannot do here

It **can** refute: integrating $\dot x = x^3$ from $x_0 = 1$ to $t = 0.49$
gives $x \approx 7.1$, and to $t = 0.4999$ gives $x \approx 70.7$, which is
inconsistent with "neutral" and settles the question in the negative. One
trajectory that leaves every neighbourhood disproves stability.

It **cannot** confirm: no finite set of trajectories over a finite horizon can
establish stability, because stability is a statement about all initial
conditions in a neighbourhood and all time.

This asymmetry is the one the benchmark is built around, and this problem is
its cleanest dynamical instance: a witness settles an existential claim, and
sampling cannot settle a universal one.

## Failure mode

`finite-horizon-mistaken-for-asymptotics`: a computation over $[0, T]$ is read
as a statement about $t \to \infty$, in a problem whose blow-up time exceeds
$T$ by a factor of 10 to $10^{5}$.
