# Flawed solution: `slowly-varying-so-it-is-fine`

## The submitted argument

> **Steps 1-3.** [The witness found, the exact solution verified, and the
> answer to Part 1 correctly given as no.]
>
> **Step 4.** The failure is caused by $A(t)$ varying on the same time scale as
> the dynamics: the eigenvectors rotate at unit angular velocity and the decay
> rate is $1/4$, so the two compete.
>
> **Step 5.** The criterion is therefore valid in the **slowly varying** case.
> Replacing $A(t)$ by $A_\varepsilon(t) = \varepsilon A(\varepsilon t)$ makes
> the variation arbitrarily slow, and for $\varepsilon$ small enough the system
> becomes stable, as the frozen eigenvalues predict.

## Where it breaks

**Step 5.** Step 4's diagnosis is right, and the proposed repair does not
follow from it, because the rescaling slows the *dynamics* by exactly the same
factor as the *variation*.

If $x$ solves $\dot x = A(t)x$ then $x_\varepsilon(t) := x(\varepsilon t)$
satisfies

$$\dot x_\varepsilon(t) = \varepsilon\,\dot x(\varepsilon t)
 = \varepsilon A(\varepsilon t)x(\varepsilon t) =
 A_\varepsilon(t)\,x_\varepsilon(t),$$

so the slowed system has the exact solution $\|x_\varepsilon(t)\| =
e^{\varepsilon t/2}$: **still unbounded**, for every $\varepsilon > 0$.

Meanwhile the eigenvalues of $A_\varepsilon(t)$ are $\varepsilon\lambda_\pm$,
with real part $-\varepsilon/4$: still strictly negative and still constant in
$t$. The counterexample survives the repair intact; only the clock has changed.

Measured at $\varepsilon = 0.1$: $\|x(200)\| = 2.2\times10^{4} = e^{10} =
e^{\varepsilon t/2}$.

The ratio that Step 4 identifies as the cause (rotation rate against decay
rate) is $1 : \tfrac14$ before the rescaling and $\varepsilon :
\tfrac{\varepsilon}4$ after. It is **scale invariant**, which is why rescaling
cannot change the outcome.

## The correct slow-variation theorem

There is one, and the difference is where the small parameter sits. For

$$\dot x = A(\delta t)\,x$$

(the matrix slowed, the dynamics **not**) with a uniform spectral gap
$\operatorname{Re}\lambda_i(A(\tau)) \le -\alpha$ for all $\tau$, the origin is
exponentially stable for all $\delta$ below a threshold depending on $\alpha$
and on bounds for $A$ and $A'$.

Step 5's rescaling is $\varepsilon A(\varepsilon t)$, which slows both. The
factor of $\varepsilon$ in front is what makes it a change of clock rather than
a slowing of the coefficients relative to the dynamics.

## Failure mode

`rescaling-does-not-remove-the-phenomenon`: a repair is proposed as a limit,
and the limit rescales the quantity it was meant to control along with
everything else.
