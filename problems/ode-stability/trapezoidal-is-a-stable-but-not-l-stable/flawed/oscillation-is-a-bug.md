# Flawed solution: `oscillation-is-a-bug`

## The submitted argument

> **Steps 1-3.** [$R(z)$, A-stability and the $z \to -\infty$ limit all
> correct.]
>
> **Step 4.** Running the Part 3 integration produces
> $-1.0000, +0.9999, -0.9999, +0.9998, \ldots$ — a sign flip at every step.
>
> **Step 5.** A sign flip at every step is the classic signature of an index
> error in the implementation: the stiff term is being applied with the wrong
> sign, or $y_n$ and $y_{n+1}$ have been swapped in the update.
>
> **Step 6.** After fixing the implementation the oscillation will disappear,
> so Part 3 asks for something that does not occur.

## Where it breaks

**Step 5**, a plausible diagnosis of a correct computation.

The output is exactly what $R(z)^n$ predicts. With $z = -10^{5}$,

$$R(z) = \frac{1 + z/2}{1 - z/2} = \frac{1 - 50000}{1 + 50000} = -0.99996000\ldots$$

and $y_n = R(z)^n$, which alternates in sign with modulus
$0.99996^n$. The computed values match to every digit printed.

There is nothing to fix. The method is second-order accurate, A-stable and
correctly implemented, and this is its defined behaviour on this input.

## The check that distinguishes the two explanations

A sign error in the update would change $R(z)$, so compare the computed ratio
with the formula:

```
ratio = y[1] / y[0]
assert abs(ratio - (1 + z/2)/(1 - z/2)) < 1e-12
```

It matches. A swapped-index bug would also fail on a *non-stiff* problem, and
the same code at $z = -1$ gives $R = +1/3$ and a clean monotone decay — correct
and non-alternating. A bug does not switch itself off when the parameter
changes.

## Why the misdiagnosis is costly

It sends the investigation into the implementation, where there is nothing to
find, and it leaves the real cause — the choice of method — unexamined. The fix
is not in the code but in the scheme: use an L-stable method, or damp the
transient with a few implicit-Euler steps before switching to the trapezoidal
rule (Rannacher smoothing).

Alternation is a genuine signature of a sign error **and** of $R(z) < 0$, and
the second is far more common in stiff integration. The discriminator is
cheap: compute $R(z)$ and compare.

## Failure mode

`correct-output-misread-as-a-bug`: a numerically correct result with an
unexpected shape is attributed to an implementation fault, and the property of
the method that produces it is not checked.
