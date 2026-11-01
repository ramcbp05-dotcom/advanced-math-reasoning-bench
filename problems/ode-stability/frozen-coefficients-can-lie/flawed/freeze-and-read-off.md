# Flawed solution: `freeze-and-read-off`

## The submitted argument

> **Step 1.** Compute the eigenvalues of $A(t)$. The trace is $-1/2$ and the
> determinant is $1/2$, both independent of $t$, so the characteristic
> polynomial is $\lambda^2 + \tfrac12\lambda + \tfrac12$ and
> $\lambda_\pm = (-1 \pm i\sqrt7)/4$.
>
> **Step 2.** $\operatorname{Re}\lambda_\pm = -1/4 < 0$ for every $t$: in fact
> uniformly, with $\alpha = 1/4$.
>
> **Step 3.** A linear system whose matrix has all eigenvalues in the open left
> half-plane is exponentially stable, with decay rate given by the spectral
> abscissa.
>
> **Step 4.** So every solution decays like $e^{-t/4}$, and the answer to
> Part 1 is yes.

## Where it breaks

**Step 3**, which states a theorem about **constant** $A$ and applies it to a
time-varying one. Steps 1 and 2 are entirely correct: the eigenvalue
computation is right, and the uniformity in Step 2 is real.

The constant-coefficient proof decomposes the initial condition in the
eigenbasis and propagates each component at its own rate. That requires the
eigenbasis to be **the same at every time**. Here it rotates at unit angular
velocity, and the rotation rate is precisely the quantity freezing $t$
discards.

## The witness

$$x(t) = e^{t/2}\begin{pmatrix}-\cos t\\ \sin t\end{pmatrix}$$

solves $\dot x = A(t)x$ exactly: verified by substitution, with the residual
simplifying symbolically to zero. So $\|x(t)\| = e^{t/2}$:

| $t$ | predicted by Step 4 ($e^{-t/4}$) | actual ($e^{t/2}$) |
|---|---|---|
| 5 | $0.287$ | $12.18$ |
| 10 | $0.082$ | $148.4$ |
| 20 | $0.0067$ | $22\,026$ |

Step 4 predicts decay by a factor of 150 where the true solution grows by a
factor of 22 000: wrong in direction, not only in magnitude.

## Why the eigenvalues are not "wrong"

They are exactly right for the question they answer: for each fixed $t_0$, the
*constant* system $\dot x = A(t_0)x$ really is stable with decay rate $1/4$.
The error is that this is a different system from the one posed.

Changing basis to the rotating frame $x = Q(t)y$ gives $\dot y = (B -
Q^{-1}\dot Q)y$ with $B - Q^{-1}\dot Q$ constant and eigenvalues $+\tfrac12,
-1$: the true Lyapunov exponents. The term $Q^{-1}\dot Q$ is what Step 3 sets
to zero.

## The check

Ask what the theorem's proof uses. If it decomposes in a fixed eigenbasis and
the eigenbasis is not fixed, the proof does not transfer. For a one-line
numerical check, integrate from one initial condition and compare the growth
with $e^{-\alpha t}$: a single trajectory refutes a universal stability claim.

## Failure mode

`constant-coefficient-theory-outside-its-hypothesis`: a theorem whose proof
requires a fixed eigenbasis is applied where the eigenbasis rotates.
