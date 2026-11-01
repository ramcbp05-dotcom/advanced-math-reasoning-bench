# Solution

## Part 1: the answer is no

**Witness (Markus and Yamabe, 1960).**

$$A(t) = \begin{pmatrix}
-1 + \tfrac32\cos^2 t & \;\;1 - \tfrac32\sin t\cos t \\[2pt] -1 - \tfrac32\sin
t\cos t & -1 + \tfrac32\sin^2 t \end{pmatrix}.$$

$A$ is continuous, bounded, and $2\pi$-periodic.

### The exact solution

$$\boxed{\ x(t) = e^{t/2}\begin{pmatrix}-\cos t\\ \sin t\end{pmatrix}\ }$$

**Verification by substitution.** Differentiating,

$$\dot x(t) = e^{t/2}\begin{pmatrix}
-\tfrac12\cos t + \sin t\\[2pt] \ \ \tfrac12\sin t + \cos t\end{pmatrix}.$$

Computing $A(t)x(t)$, the first component is

$$e^{t/2}\Big[\big(-1+\tfrac32\cos^2t\big)(-\cos t)
 + \big(1 - \tfrac32\sin t\cos t\big)\sin t\Big] = e^{t/2}\Big[\cos t -
   \tfrac32\cos^3 t + \sin t - \tfrac32\sin^2t\cos t\Big]$$

$$= e^{t/2}\Big[\cos t - \tfrac32\cos t\big(\cos^2t+\sin^2t\big) + \sin t\Big]
= e^{t/2}\Big[-\tfrac12\cos t + \sin t\Big],$$

which matches. The second component is the same computation with the second
row, and `verify.py` confirms both symbolically: the residual $\dot x - A(t)x$
simplifies to exactly $0$, as a function of $t$. $\blacksquare$

$\|x(t)\| = e^{t/2}$, so the solution grows without bound. The origin is
**unstable**: in fact every nonzero solution with a component along this one
grows exponentially at rate $1/2$.

Measured (RK45, `rtol = 1e-10`, from $x(0) = (1,0)$, which is $-x(0)$ of the
witness up to sign):

| $t$ | $\|x(t)\|$ | $e^{t/2}$ |
|---|---|---|
| 0 | $1.000000$ | $1.000000$ |
| 5 | $1.218249\times10^{1}$ | $1.218249\times10^{1}$ |
| 10 | $1.484132\times10^{2}$ | $1.484132\times10^{2}$ |
| 20 | $2.202647\times10^{4}$ | $2.202647\times10^{4}$ |

## Part 2

### The eigenvalues are constant and stable

$$\operatorname{tr}A(t) = \big(-1+\tfrac32\cos^2t\big) + \big(-1+\tfrac32\sin^2t\big)
 = -2 + \tfrac32 = -\tfrac12 ,$$

independent of $t$. For the determinant,

$$\det A(t) = \big(-1+\tfrac32\cos^2t\big)\big(-1+\tfrac32\sin^2t\big)
 - \big(1-\tfrac32\sin t\cos t\big)\big(-1-\tfrac32\sin t\cos t\big) .$$

Writing $c = \cos t$, $s = \sin t$ and expanding, the first product is $1 -
\tfrac32(c^2+s^2) + \tfrac94c^2s^2 = -\tfrac12 + \tfrac94c^2s^2$, and the
second is $-\big(1 - \tfrac94s^2c^2\big)$. Subtracting,

$$\det A(t) = -\tfrac12 + \tfrac94c^2s^2 + 1 - \tfrac94s^2c^2 = \tfrac12 ,$$

also independent of $t$. Hence the characteristic polynomial is $\lambda^2 +
\tfrac12\lambda + \tfrac12$ for every $t$, with roots

$$\lambda_\pm = \frac{-1 \pm i\sqrt7}{4},
\qquad \operatorname{Re}\lambda_\pm = -\tfrac14 < 0 .$$

**Every frozen-time eigenvalue has real part $-1/4$, and the solution grows
like $e^{t/2}$.** Measured at $t = 0, 0.7, 1.3, 2.9, 4.4$: the eigenvalues are
$-0.25 \pm 0.661438i$ in every case, to 15 digits.

### Reconciling the trace

$\operatorname{tr}A(t) = -\tfrac12 < 0$, so by Abel-Jacobi-Liouville

$$\det\Phi(t) = \det\Phi(0)\,e^{-t/2} \longrightarrow 0 .$$

There is no contradiction, and the two facts together are informative. The
fundamental matrix has **determinant shrinking like $e^{-t/2}$** while one of
its columns **grows like $e^{t/2}$**. Both hold simultaneously because the
other Lyapunov exponent must then be $-\tfrac12 - \tfrac12 = -1$:

$$\mu_1 + \mu_2 = \lim_{t\to\infty}\frac1t\ln\det\Phi(t)
 = \operatorname{tr}A = -\tfrac12, \qquad \mu_1 = +\tfrac12 \implies \mu_2 = -1
 .$$

So phase-space volume contracts (the system is dissipative on average) while
one direction expands. **Volume contraction does not imply stability**, and the
trace, like the eigenvalues, is a frozen-time quantity that constrains only the
*sum* of the exponents.

## Part 3: the mechanism

For a constant $A$, the eigenvectors are fixed, and decomposing the initial
condition in that basis gives decay at the eigenvalue rates. That decomposition
is what the constant-coefficient theorem rests on.

Here the eigenvectors **rotate**, and the right change of variables is a
*clockwise* rotation. Put $x = Q(t)y$ with

$$Q(t) = \begin{pmatrix}\cos t & \sin t\\ -\sin t & \cos t\end{pmatrix}
\qquad(\text{rotation by } -t).$$

Then $\dot x = \dot Q y + Q\dot y = A Q y$ gives

$$\dot y = \big(Q^{-1}AQ - Q^{-1}\dot Q\big)\,y ,$$

and the bracket evaluates to a **constant diagonal** matrix:

$$Q^{-1}AQ - Q^{-1}\dot Q = \begin{pmatrix}\tfrac12 & 0\\ 0 & -1\end{pmatrix}.$$

So in the rotating frame the system decouples completely, with growth rate
$+\tfrac12$ in one coordinate and decay rate $-1$ in the other. Those are the
**Lyapunov exponents**, and they sum to $-\tfrac12 = \operatorname{tr}A$ as
Abel requires. An entirely independent computation (the Floquet multipliers of
the $2\pi$-periodic system) gives $\ln|\rho_i|/2\pi = (+\tfrac12, -1)$ to ten
decimal places.

The direction of the rotation is part of the result: taking $Q =
\operatorname{rot}(+t)$ instead leaves a matrix that is not even constant.

**The ignored quantity is $\dot Q$: the rate at which the eigenvectors turn.**
Freezing $t$ sets $\dot Q = 0$ by construction, which is exactly the term that
changes the answer. The instantaneous eigenvalues are correct for the frozen
problem and the frozen problem is not the one being solved.

The intuition: a solution decaying along the slow eigendirection is
continuously rotated *out* of it and into a direction where it has further to
fall, and the geometry can be arranged so that it gains more from the rotation
than it loses to the decay.

## Part 4: slow variation does not save it

Set $A_\varepsilon(t) := \varepsilon A(\varepsilon t)$ for $\varepsilon > 0$.
Then $A_\varepsilon$ varies on the time scale $1/\varepsilon$, as slowly as one
likes.

If $x$ solves $\dot x = A(t)x$, put $x_\varepsilon(t) := x(\varepsilon t)$.
Then

$$\dot x_\varepsilon(t) = \varepsilon\,\dot x(\varepsilon t)
 = \varepsilon A(\varepsilon t)\,x(\varepsilon t) =
 A_\varepsilon(t)\,x_\varepsilon(t),$$

so $x_\varepsilon$ solves the slowed system, and

$$\|x_\varepsilon(t)\| = e^{\varepsilon t/2} .$$

Still unbounded: growing at rate $\varepsilon/2$ instead of $1/2$. Meanwhile
the eigenvalues of $A_\varepsilon(t)$ are $\varepsilon\lambda_\pm$, with real
part $-\varepsilon/4 < 0$: still stable, still constant in $t$.

**The repair fails.** Slowing the variation slows the growth by exactly the
same factor and changes nothing qualitative. Measured at $\varepsilon = 0.1$:
$\|x(200)\| = 2.2\times10^{4} = e^{10}$, matching $e^{\varepsilon t/2}$.

(There *is* a correct slow-variation theorem: for $\dot x = A(\delta t)x$ with
$\delta \to 0$ and a **uniform** spectral gap, stability does follow for
$\delta$ small enough. The difference is that $\delta$ there is independent of
the time horizon, whereas the rescaling above moves the horizon with it.)

### What does work

* **Lyapunov exponents** $\mu_i = \lim_{t\to\infty}\tfrac1t\ln\|x_i(t)\|$: here
  $+\tfrac12$ and $-1$. These decide the question by definition, and are what
  the frozen eigenvalues fail to approximate.
* **Floquet theory** when $A$ is $T$-periodic, as it is here: compute the
  monodromy matrix $\Phi(T)$ and read its eigenvalues (the Floquet
  multipliers). Instability corresponds to $|\rho| > 1$; here $\rho_1 = e^{\pi}
  \approx 23.14$ and $\rho_2 = e^{-2\pi} \approx 0.00187$, with $\rho_1\rho_2 =
  e^{-\pi} = \det\Phi(2\pi)$ as Abel requires.
* **A time-varying Lyapunov function** $V(t,x) = x^{\mathsf T}P(t)x$ with $P$
  solving a differential Lyapunov equation: the general sufficient condition,
  and the one that reduces to the eigenvalue criterion when $A$ is constant.

## Remarks

* The converse direction fails too: a system can have frozen eigenvalues with
  *positive* real part everywhere and still be asymptotically stable.
* The periodicity here is a convenience (it makes Floquet available), not the
  cause. Aperiodic examples with the same behaviour exist.
* This is the time-varying analogue of
  `eigenvalues-do-not-determine-the-condition-number`: in both cases the
  eigenvalues are correct and the eigen*vectors* carry the information that
  decides the question.
