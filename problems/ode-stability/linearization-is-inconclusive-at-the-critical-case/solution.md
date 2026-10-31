# Solution

## Part 1: the witness pair

$$\dot x = -x^3 \qquad\text{and}\qquad \dot x = +x^3 .$$

Both have the equilibrium $x_0 = 0$, and both have

$$J = \frac{d}{dx}\big(\mp x^3\big)\Big|_{x=0} = \mp 3x^2\Big|_{x=0} = 0 .$$

**The linearisation is the zero system $\dot\xi = 0$ in both cases** — the
single eigenvalue is $0$, so the critical case applies and the first method is
silent.

### Closed-form solutions

Separate variables in $\dot x = \sigma x^3$ with $\sigma = \pm1$ and
$x(0) = x_0 \ne 0$:

$$\frac{dx}{x^3} = \sigma\,dt
\;\Longrightarrow\;
-\frac{1}{2x^2} = \sigma t + C
\;\Longrightarrow\;
x(t)^2 = \frac{x_0^2}{1 - 2\sigma x_0^2 t},$$

so

$$\boxed{\ x(t) = \frac{x_0}{\sqrt{1 - 2\sigma x_0^2 t}}\ }$$

(taking the branch with $x(0) = x_0$; the sign of $x$ is preserved since $x$
cannot cross 0).

**$\sigma = -1$ (i.e. $\dot x = -x^3$):**

$$x(t) = \frac{x_0}{\sqrt{1 + 2x_0^2t}} \;\longrightarrow\; 0
\qquad\text{as } t\to\infty,$$

for every $x_0$, so $0$ is **globally asymptotically stable**.

**$\sigma = +1$ (i.e. $\dot x = +x^3$):**

$$x(t) = \frac{x_0}{\sqrt{1 - 2x_0^2t}} \;\longrightarrow\; \infty
\qquad\text{as } t \to \frac{1}{2x_0^2}^{-},$$

so $0$ is **unstable** — and in the strongest possible sense. $\blacksquare$

Identical linearisations, opposite conclusions. The third clause is therefore
not a weakness of the proof technique; **no** criterion based on $J$ alone can
decide the critical case.

## Part 2: finite-time blow-up

From the closed form, $x(t) \to \infty$ as the denominator vanishes:

$$1 - 2x_0^2t^{*} = 0 \;\Longrightarrow\;
\boxed{\ t^{*} = \frac{1}{2x_0^2}\ }$$

Measured (RK45, `rtol = 1e-10`), solving $\dot x = x^3$:

| $x_0$ | predicted $t^{*}$ | $x$ at $0.99\,t^{*}$ | $x$ at $0.9999\,t^{*}$ |
|---|---|---|---|
| $1$ | $0.5$ | $10.0$ | $100.0$ |
| $0.1$ | $50$ | $1.0$ | $10.0$ |
| $0.01$ | $5000$ | $0.1$ | $1.0$ |

Note the last column: $x(t) = x_0/\sqrt{1 - t/t^{*}}$, so at $t = 0.9999t^{*}$
the solution is only $100x_0$. **The blow-up is slow until it is not**, which
is what makes it so easy to miss numerically — see
`numerical-evidence-settles-it`.

## Part 3: algebraic, not exponential, decay

For $\dot x = -x^3$,

$$x(t) = \frac{x_0}{\sqrt{1 + 2x_0^2t}} \;\sim\; \frac{1}{\sqrt{2t}}
\qquad (t \to \infty),$$

**independently of $x_0$**. The decay is $O(t^{-1/2})$: algebraic.

Contrast a hyperbolic equilibrium, $\dot x = -ax$ with $a > 0$, where
$x(t) = x_0e^{-at}$ decays exponentially with a rate set by the eigenvalue.

Two differences worth naming:

* the asymptotic rate here does not depend on the initial condition at all
  (the $x_0$ cancels), which is a signature of the nonlinearity doing the work;
* convergence is far slower. Reaching $|x| < 10^{-3}$ from $x_0 = 1$ takes
  $t \approx 5\times10^{5}$, where $\dot x = -x$ would take $t \approx 7$.

Measured: $x(10^{6}) = 7.07\times10^{-4}$ from $x_0 = 1$, against
$1/\sqrt{2\cdot10^{6}} = 7.07\times10^{-4}$.

## Part 4: a two-dimensional critical case

$$\dot x = -y - x^3, \qquad \dot y = x - y^3 .$$

Equilibrium at the origin, with Jacobian

$$J = \begin{pmatrix}-3x^2 & -1\\ 1 & -3y^2\end{pmatrix}_{(0,0)}
  = \begin{pmatrix}0 & -1\\ 1 & 0\end{pmatrix},$$

whose eigenvalues are $\pm i$: a **centre**, real parts exactly zero. The first
method is silent — and the linear system $\dot\xi = J\xi$ has closed periodic
orbits, so a naive reading would predict neutral stability.

**The true behaviour is asymptotic stability.** Take $V(x,y) = x^2 + y^2$,
positive definite with $V(0,0)=0$. Along trajectories,

$$\dot V = 2x\dot x + 2y\dot y
   = 2x(-y - x^3) + 2y(x - y^3)
   = -2xy - 2x^4 + 2xy - 2y^4
   = -2(x^4 + y^4) ,$$

which is strictly negative for $(x,y) \ne (0,0)$. By Lyapunov's **second**
method the origin is asymptotically stable — in fact globally, since $V$ is
radially unbounded. $\blacksquare$

(The cross terms cancelling is the rotation doing no work on $V$; the quartic
terms are the whole of the dissipation.)

Measured: from $(0.5,0)$, $(1,1)$ and $(0.1,-0.3)$, the solutions reach
$\|x(60)\| \approx 0.10$ in every case — the same slow algebraic decay as Part
3, and the $x_0$-independence again. Reversing the sign of the cubic terms
gives $\dot V = +2(x^4+y^4) > 0$ and the same linearisation, with trajectories
that leave every neighbourhood.

## Remarks

* The scalar pair is the standard example, and it is worth noticing that
  $\dot x = -x^3$ and $\dot x = +x^3$ agree to **second order** at the origin.
  Any criterion using finitely many derivatives of $f$ at $x_0$ must therefore
  examine the cubic term; linearisation stops at the first.
* The right tool for the critical case is Lyapunov's second method (as in Part
  4) or centre-manifold reduction, which projects the dynamics onto the
  subspace belonging to the marginal eigenvalues and decides the question
  there.
* "Marginal" is not a small or exceptional case: it is exactly where
  bifurcations occur, so it is where the interesting behaviour lives.
