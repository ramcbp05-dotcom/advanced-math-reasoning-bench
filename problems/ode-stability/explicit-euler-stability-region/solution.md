# Solution

## Part 1: the region

Applying $y_{n+1} = y_n + hf(t_n,y_n)$ to $f = \lambda y$:

$$y_{n+1} = y_n + h\lambda y_n = (1 + h\lambda)y_n ,$$

so $R(z) = 1 + z$ with $z = h\lambda$, and by induction $y_n = (1+z)^ny_0$.
Hence

$$|y_n| \to 0 \iff |1 + z| < 1 ,$$

and the closed region of absolute stability is $|1+z| \le 1$: the **disc of
radius 1 centred at $-1$**. $\blacksquare$

For real $\lambda < 0$, write $z = h\lambda$ with $h > 0$, so $z$ is real and
negative:

$$|1 + h\lambda| \le 1
\iff -1 \le 1 + h\lambda \le 1 \iff -2 \le h\lambda \le 0 \iff h \le
\frac{2}{|\lambda|}.$$

Measured, integrating $y' = \lambda y$ for 200 steps:

| $h|\lambda|$ | $|y_{200}|$ |
|---|---|
| $1.00$ | $0$ (underflow) |
| $1.98$ | $1.76\times10^{-2}$ |
| $2.02$ | $5.25\times10^{1}$ |
| $3.00$ | $1.61\times10^{60}$ |

The table is **identical** for $\lambda = -1, -10, -100$ with $h$ scaled
accordingly, confirming that only the product $h\lambda$ matters.

The transition at $h|\lambda| = 2$ is a **sharp threshold**, not a degradation:
at 1.98 the solution decays, at 2.02 it grows.

## Part 2: the step restriction

The system decouples, so each component obeys the scalar analysis.

**Accuracy.** After a short transient the fast mode $y_1 = e^{-10^6t}$ is
numerically zero ($e^{-10^6 \cdot 10^{-5}} = e^{-10} \approx 5\times10^{-5}$,
and utterly negligible by $t = 10^{-4}$). What remains to be resolved is $y_2 =
e^{-t}$, which needs perhaps $h \approx 10^{-2}$ for a few digits:

$$N_{\text{accuracy}} \approx \frac{10}{10^{-2}} = 10^{3}\ \text{steps}.$$

**Stability.** The step must satisfy $h \le 2/\lambda_{\text{fast}} =
2\times10^{-6}$: governed by the mode that has **already vanished**:

$$N_{\text{stability}} \approx \frac{10}{2\times10^{-6}} = 5\times10^{6}\
\text{steps}.$$

A factor of **5000** more steps, all of them to keep a component that is
identically zero to machine precision from being amplified.

**This is the definition of stiffness**: the stability requirement is set by a
time scale much faster than the one being resolved.

## Part 3: local error has no threshold; the amplification factor does

The local truncation error is

$$\tau_n = \tfrac12h^2y''(\xi_n) ,$$

$O(h^2)$ for every $h$ with no threshold anywhere. Both statements in the
problem are true, and they are about different quantities.

**The global error obeys a recurrence.** Writing $e_n = y_n - y(t_n)$,

$$e_{n+1} = (1 + h\lambda)\,e_n + \tau_n ,$$

so

$$e_n = \sum_{k=0}^{n-1}(1+h\lambda)^{\,n-1-k}\,\tau_k .$$

The local errors are not merely added; each is **multiplied by a power of $R(z)
= 1 + h\lambda$** on its way to the end.

* If $|1+h\lambda| \le 1$ the powers are bounded, the sum is controlled, and
  the familiar $O(h)$ global error holds.
* If $|1+h\lambda| > 1$ the powers grow geometrically. Over $n$ steps the
  earliest error is amplified by $|1+h\lambda|^{n-1}$, and at $h|\lambda| = 3$
  with $n = 200$ that factor is $2^{199} \approx 10^{60}$: which is exactly the
  $1.61\times10^{60}$ in the table.

So:

* **no threshold**: the local truncation error, $\tfrac12h^2y''$;
* **sharp threshold at $|R(z)| = 1$**: the amplification factor applied to
  accumulated error.

A consistent method ($\tau_n \to 0$) converges as $h \to 0$ for **fixed** $t$:
that is the Lax/Dahlquist equivalence theorem, and it is an asymptotic
statement. Absolute stability is a statement about a **fixed** $h$ and $n \to
\infty$, and the two limits do not commute.

## Part 4: implicit Euler

$$y_{n+1} = y_n + h\lambda y_{n+1} \implies
  y_{n+1} = \frac{1}{1 - h\lambda}y_n, \qquad R(z) = \frac{1}{1-z}.$$

$|R(z)| \le 1 \iff |1 - z| \ge 1$: the **exterior** of the disc of radius 1
centred at $+1$. This contains the entire left half-plane, so implicit Euler is
**A-stable**: stable for every $h > 0$ whenever $\operatorname{Re}\lambda < 0$.

For the Part 2 system, $h$ is then chosen purely for accuracy: $10^{3}$ steps
rather than $5\times10^{6}$.

It also has $R(z) \to 0$ as $z \to -\infty$ ($|R(-10^{8})| = 10^{-8}$), so
infinitely stiff modes are annihilated in one step. That property is
**L-stability**, and it is *not* implied by A-stability: see
`trapezoidal-is-a-stable-but-not-l-stable`.

**The cost.** Each step requires solving $y_{n+1} - h f(t_{n+1},y_{n+1}) =
y_n$, a nonlinear system in general, typically by Newton with a Jacobian
factorisation: an $O(m^3)$ linear solve per step against $O(m)$ for the
explicit method. The trade is worth it exactly when the stiffness ratio exceeds
the per-step cost ratio, which on the Part 2 system it does by a factor of
5000.

## Remarks

* The stability region of explicit Euler is bounded, so **no** explicit
  one-step method with a bounded region can be A-stable. That is not a
  limitation of Euler: a Runge-Kutta method of $s$ stages has $R(z)$ a
  polynomial of degree $\le s$, and a non-constant polynomial is unbounded, so
  no explicit Runge-Kutta method is A-stable at all.
* For $\lambda$ complex with $\operatorname{Re}\lambda < 0$ but
  $|\operatorname{Im}\lambda|$ large (an oscillatory problem), the disc
  condition is far more restrictive than $h \le 2/|\operatorname{Re}\lambda|$:
  the region touches the imaginary axis only at the origin.
