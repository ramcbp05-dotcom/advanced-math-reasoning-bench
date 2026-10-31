# Flawed solution: `small-error-means-stable`

## The submitted argument

> **Step 1.** The local truncation error of explicit Euler is
> $\tau = \tfrac12h^2y''(\xi) = O(h^2)$.
>
> **Step 2.** Over $n = T/h$ steps the errors accumulate, giving a global error
> of $n \cdot O(h^2) = O(h)$. The method is first-order convergent.
>
> **Step 3.** So for $h = 10^{-3}$ on $y' = -10^{6}y$ over $[0,10]$ the global
> error is $O(10^{-3})$ — small.
>
> **Step 4.** There is no stability threshold; the method simply gets more
> accurate as $h$ decreases, smoothly.

## Where it breaks

**Step 2**, at "the errors accumulate" — meaning *added*. They are not added;
each is **propagated through the remaining steps**, and propagation multiplies.

The exact recurrence is $e_{n+1} = (1+h\lambda)e_n + \tau_n$, giving

$$e_n = \sum_{k=0}^{n-1}(1+h\lambda)^{\,n-1-k}\tau_k .$$

The $n \cdot O(h^2)$ estimate in Step 2 implicitly sets every factor
$(1+h\lambda)^{j}$ to 1, which is legitimate only when $|1+h\lambda| \le 1$.

## How wrong Step 3 is

At $h = 10^{-3}$ and $\lambda = -10^{6}$, $z = h\lambda = -1000$, so

$$|R(z)| = |1 + z| = 999 .$$

Each step multiplies the error by 999. Over the $10^{4}$ steps to $t = 10$ the
amplification is $999^{10^4} \approx 10^{30000}$. The computation overflows
almost immediately; the claimed global error of $10^{-3}$ is wrong by every
order of magnitude there is.

Measured at a milder setting, $\lambda = -1$ with 200 steps:

| $h|\lambda|$ | $|y_{200}|$ | Step 2's prediction |
|---|---|---|
| $1.98$ | $1.76\times10^{-2}$ | small ✓ |
| $2.02$ | $5.25\times10^{1}$ | small ✗ |
| $3.00$ | $1.61\times10^{60}$ | small ✗ |

The transition between the first two rows is a 2 % change in $h$.

## Both statements in Step 1-2 are individually true

That is what makes this error durable. Explicit Euler **is** first-order
convergent, and the global error **is** $O(h)$ — as $h \to 0$ with $T$ fixed.
Absolute stability concerns a **fixed** $h$ with $n \to \infty$, or
equivalently a fixed $h$ and a $\lambda$ large enough that $h|\lambda| > 2$.
The two limits do not commute, and convergence theory says nothing about the
second.

## The check

Compute $z = h\lambda$ and ask whether $|1 + z| \le 1$. It is one line, it
requires only the step and the stiffest eigenvalue, and it is what every
production integrator does before accepting a step.

## Failure mode

`local-error-vs-global-stability`: per-step error is summed instead of
propagated, which silently assumes the amplification factor is at most 1.
