# Flawed solution: `residual-means-accuracy`

## The submitted argument

> **Steps 1-3.** [Part 1 proved correctly.]
>
> **Step 4.** The predicted loss for the normal equations is $u\kappa_2(A)^2$,
> which at $\kappa_2(A) = 10^8$ is $O(1)$ --- so in principle the solution is
> worthless.
>
> **Step 5.** But this is a worst-case bound. Running the computation on a
> concrete $10^8$-conditioned problem and measuring
> $\|A\hat x - b\|_2 / \|b\|_2$ gives $4\times10^{-16}$, essentially machine
> precision.
>
> **Step 6.** The residual is at the level of rounding, so the solution is
> accurate to machine precision and the bound in Step 4 is pessimistic in
> practice. The normal equations are fine.

## Where it breaks

**Step 6**, which treats a small residual as evidence of an accurate solution.
The measurement in Step 5 is real and correctly performed; the inference from
it is the error.

The relation between the two is

$$\frac{\|x - \hat x\|}{\|x\|} \le \kappa(A)\,\frac{\|r\|}{\|b\|},$$

and it is attained, so the residual bounds the error only up to a factor of
$\kappa$. Substituting the measured numbers with $\kappa_2(A^{\mathsf T}A) =
10^{16}$:

$$\frac{\|x - \hat x\|}{\|x\|} \lesssim 10^{16}\cdot 4\times10^{-16} \approx 4 .$$

The measurement in Step 5 is consistent with the solution having **no correct
digits**. It does not contradict Step 4; it is exactly what Step 4 predicts.

## Why the measurement looked reassuring

A backward-stable algorithm is *defined* by returning a solution with a small
residual --- it solves a nearby problem exactly. Observing a small residual
therefore confirms the implementation is backward stable and tells you nothing
about the forward error, which depends on the conditioning of the problem the
implementation cannot change.

For an ill-conditioned system this is not a subtlety but the normal situation:
the solution set has a long thin valley in which $\|A\hat x - b\|$ barely
changes, and $\hat x$ can wander a long way down that valley while the residual
stays at rounding level. The valley is in the direction of the smallest right
singular vector, and its aspect ratio is $\kappa$.

## The check that settles it

Construct a problem with a known exact solution and measure the **forward**
error:

```
x_exact = ones(n)
b = A @ x_exact
x_hat = solve(A.T @ A, A.T @ b)
forward = norm(x_hat - x_exact) / norm(x_exact)       <-- this is the number
residual = norm(A @ x_hat - b) / norm(b)              <-- not this one
```

`verify.py` does this at $\kappa_2(A)$ from $10^2$ to $10^{10}$ and tabulates
both. The residual stays near $10^{-16}$ throughout while the forward error
climbs as $u\kappa^2$, which is the whole content of the problem displayed in
two columns.

## Failure mode

`backward-vs-forward-error`: backward stability is measured and reported as
forward accuracy.
