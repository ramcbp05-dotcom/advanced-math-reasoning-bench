# Solution

## Part 1: $R(z)$ and A-stability

Apply the method to $f = \lambda y$:

$$y_{n+1} = y_n + \frac{h\lambda}{2}(y_n + y_{n+1})
\;\Longrightarrow\;
\Big(1 - \frac{z}{2}\Big)y_{n+1} = \Big(1 + \frac{z}{2}\Big)y_n ,$$

so

$$\boxed{\ R(z) = \frac{1 + z/2}{1 - z/2}\ }$$

### The region is exactly the left half-plane

Write $z = x + iy$. Then

$$|R(z)| \le 1
\iff \Big|1 + \tfrac z2\Big|^2 \le \Big|1 - \tfrac z2\Big|^2 .$$

Expanding both sides:

$$\Big(1+\tfrac x2\Big)^2 + \tfrac{y^2}{4}
\;\le\;
\Big(1-\tfrac x2\Big)^2 + \tfrac{y^2}{4}.$$

The $y^2/4$ and the $1 + x^2/4$ terms cancel on both sides, leaving

$$x \le -x \iff 2x \le 0 \iff \operatorname{Re}z \le 0 .$$

This is an **equivalence**, so the stability region is exactly
$\{\operatorname{Re}z \le 0\}$: both inclusions, with no slack. The trapezoidal
rule is A-stable, and it is the *boundary* case — its region is neither larger
nor smaller than the half-plane. $\blacksquare$

(Note $R$ maps the imaginary axis to the unit circle, so on
$\operatorname{Re}z = 0$ the method is exactly non-dissipative: it preserves
the amplitude of a purely oscillatory mode, which is why it is the method of
choice for Hamiltonian and wave problems.)

## Part 2: not L-stable

$$\lim_{z\to-\infty}R(z)
 = \lim_{z\to-\infty}\frac{1+z/2}{1-z/2}
 = \lim_{z\to-\infty}\frac{2/z + 1}{2/z - 1}
 = \frac{1}{-1} = -1 .$$

So $|R(z)| \to 1$, not 0: the trapezoidal rule is **not L-stable**.
$\blacksquare$

Measured:

| $z$ | $R(z)$ |
|---|---|
| $-1$ | $+0.3333333333$ |
| $-10$ | $-0.6666666667$ |
| $-10^{2}$ | $-0.9607843137$ |
| $-10^{4}$ | $-0.9996000800$ |
| $-10^{8}$ | $-0.9999999600$ |

Two things happen at once as the problem stiffens: the modulus approaches 1
(no damping) and the sign becomes negative (alternation).

## Part 3: the consequence

$\lambda = -10^{6}$, $h = 0.1$, so $z = -10^{5}$ and
$R(z) = -0.99996000\ldots$

| step $n$ | $y_n$ numerical | $y(t_n) = e^{-10^{6}\cdot 0.1n}$ exact |
|---|---|---|
| 1 | $-1.0000$ | $\approx 0$ ($e^{-10^5}$) |
| 2 | $+0.9999$ | $\approx 0$ |
| 3 | $-0.9999$ | $\approx 0$ |
| 4 | $+0.9998$ | $\approx 0$ |
| 5 | $-0.9998$ | $\approx 0$ |
| 6 | $+0.9998$ | $\approx 0$ |
| 7 | $-0.9997$ | $\approx 0$ |
| 8 | $+0.9997$ | $\approx 0$ |

The exact solution is $e^{-10^5} \approx 10^{-43429}$ — zero to any precision —
after a single step. The numerical solution **oscillates between $\pm1$** and
decays at a rate of $4\times10^{-5}$ per step: it would need $\sim10^{5}$ steps
to lose even a factor of $e$.

**Nothing is unstable.** $|R(z)| < 1$, the solution is bounded, A-stability is
not violated, and no error estimator based on growth will complain. The method
is simply reflecting the stiff transient instead of damping it, and the
reflection is of the full initial amplitude. $\blacksquare$

The failure is also *worse* for stiffer problems, which is the opposite of the
usual intuition: the stiffer the mode, the closer $R$ is to $-1$ and the longer
the spurious oscillation persists.

## Part 4: implicit Euler, and the trade

Implicit Euler has $R(z) = 1/(1-z)$, with

$$R(-10^{8}) = 10^{-8} \to 0 ,$$

so it is **L-stable**: an infinitely stiff mode is annihilated in a single
step, which is what the exact solution does.

**The price is order.** The trapezoidal rule is **second** order; implicit
Euler is **first**. On a non-stiff problem, or for the slow components of a
stiff one, the trapezoidal rule gives one more order of accuracy for the same
work per step. L-stability is bought with an order.

| method | $R(z)$ | order | A-stable | L-stable |
|---|---|---|---|---|
| explicit Euler | $1+z$ | 1 | no | no |
| implicit Euler | $1/(1-z)$ | 1 | yes | yes |
| trapezoidal | $\frac{1+z/2}{1-z/2}$ | 2 | yes | **no** |
| TR-BDF2 | — | 2 | yes | yes |

This is not an accident of these three methods. The **second Dahlquist
barrier** says no A-stable linear multistep method has order above 2, and the
trapezoidal rule attains it — so it is optimal in its class and still not
L-stable.

### What real solvers do

* **Damp the transient first.** The TR-BDF2 scheme takes a trapezoidal
  sub-step followed by a BDF2 sub-step; the composite is second order **and**
  L-stable. It is the default in several circuit and PDE codes.
* **Use an L-stable family.** BDF2-BDF5 and the stiffly accurate SDIRK/Radau
  methods are L-stable at higher order; `scipy`'s `Radau` and `BDF` are these.
* **Smooth with a short implicit-Euler step** after any discontinuity or at
  startup, which kills the $(-1)^n$ component before the trapezoidal rule
  propagates it — the Rannacher time-stepping trick, standard in option
  pricing where the payoff has a kink.

## Remarks

* $R(z) \to -1$ rather than $+1$ is why the artefact alternates in sign. A
  method with $R \to +1$ would freeze the transient instead of oscillating it,
  which is harder to notice.
* The same non-dissipativity that causes this is a *virtue* on the imaginary
  axis: $|R(iy)| = 1$ exactly, so the trapezoidal rule conserves the amplitude
  of an oscillation. A method chosen for a wave problem and reused on a stiff
  parabolic one carries this behaviour with it.
