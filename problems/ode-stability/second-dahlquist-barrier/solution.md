# Solution

## Part 1: order conditions

Apply the method to $y' = f$ with a smooth exact solution and expand. The
**linear difference operator** is

$$\mathcal{L}[y](t;h) = \sum_{j=0}^{k}\Big[\alpha_j y(t+jh) - h\beta_j y'(t+jh)\Big].$$

Taylor-expanding $y(t+jh) = \sum_{i\ge0}\frac{(jh)^i}{i!}y^{(i)}(t)$ and
$y'(t+jh) = \sum_{i\ge0}\frac{(jh)^i}{i!}y^{(i+1)}(t)$ and collecting powers of
$h$:

$$\mathcal{L}[y](t;h) = C_0\,y(t) + C_1h\,y'(t) + C_2h^2y''(t) + \cdots$$

with

$$C_0 = \sum_j\alpha_j, \qquad
C_i = \frac{1}{i!}\sum_j j^{\,i}\alpha_j - \frac{1}{(i-1)!}\sum_j
j^{\,i-1}\beta_j \quad (i \ge 1).$$

The method has order $p$ iff $C_0 = \cdots = C_p = 0$ and $C_{p+1} \ne 0$,
which on clearing factorials is exactly the stated system. $\blacksquare$

$C_{p+1}$ is the **error constant**.

### The trapezoidal rule

$k = 1$, $\alpha = (-1, 1)$, $\beta = (\tfrac12, \tfrac12)$:

$$C_0 = -1 + 1 = 0,$$
$$C_1 = (0\cdot(-1) + 1\cdot 1) - (\tfrac12 + \tfrac12) = 1 - 1 = 0,$$
$$C_2 = \tfrac12(0 + 1) - (0\cdot\tfrac12 + 1\cdot\tfrac12) = \tfrac12 - \tfrac12 = 0,$$
$$C_3 = \tfrac16(0 + 1) - \tfrac12(0 + \tfrac12) = \tfrac16 - \tfrac14 = -\tfrac{1}{12}\ \ne 0 .$$

So the order is exactly **2**, with error constant $-1/12$. (All four
computations are reproduced symbolically in `verify.py`.)

## Part 2: the theorem

**Second Dahlquist barrier.** *An A-stable linear multistep method has order $p
\le 2$; among A-stable second-order methods the trapezoidal rule minimises
$|C_3|$.*

### 1. What is quantified over

**All** step numbers $k \ge 1$ and **all** real coefficient vectors
$(\alpha_0,\dots,\alpha_k)$, $(\beta_0,\dots,\beta_k)$ with $\alpha_k = 1$.
That is a countable union of uncountable sets: which is exactly why Part 3 is
asked.

### 2. No contradiction with Runge-Kutta

The theorem quantifies over **linear multistep** methods. Gauss-Legendre
collocation with $s$ stages is A-stable and has order $2s$: arbitrarily high.
It is an implicit Runge-Kutta method, not an LMM, and is simply not in the
class.

The structural difference: an LMM's stability function is the *rational*
function $\zeta \mapsto$ (roots of $\rho - z\sigma$), constrained by the
requirement that **all** roots stay in the unit disc, and that constraint is
what couples order to stability. An implicit RK method's $R(z)$ is a rational
function with no such multi-root condition, and the Padé table supplies
A-stable approximations to $e^{z}$ at every order.

### 3. No contradiction with BDF

The BDF-$k$ methods have order $k$, reaching order 6. They are **not A-stable**
for $k \ge 3$: only $A(\alpha)$-stable, with the wedge angle shrinking:

| $k$ | order | $A(\alpha)$ half-angle |
|---|---|---|
| 1 | 1 | $90°$ (A-stable) |
| 2 | 2 | $90°$ (A-stable) |
| 3 | 3 | $\approx 86.03°$ |
| 4 | 4 | $\approx 73.35°$ |
| 5 | 5 | $\approx 51.84°$ |
| 6 | 6 | $\approx 17.84°$ |
| 7 | 7 | **not zero-stable** |

BDF1 and BDF2 are A-stable and have orders 1 and 2: consistent with the barrier
and attaining it at $k = 2$. BDF3 and beyond trade A-stability for order,
exactly as the theorem requires.

### The proof

Dahlquist's proof is not reproduced here. The argument runs through the order
star of $\rho(\zeta) - z\sigma(\zeta)$ (Wanner, Hairer and Nørsett's later
treatment) or, in Dahlquist's original form, through a Riesz-Herglotz
representation of the function $\zeta \mapsto \rho(\zeta)/\sigma(\zeta)$, which
A-stability forces to map the exterior of the unit disc into the right
half-plane. The order conditions then bound how closely such a function can
approximate $\log\zeta$ near $\zeta = 1$, and the bound is 2.

**This is a citation, not a proof**, and the problem is constructed so that
distinguishing the two is part of the answer.

## Part 3: what a search establishes

The asymmetry is sharp and it is the point of this problem.

### A single hit would settle it: negatively

If a search produced coefficients $(\alpha, \beta)$ that are **provably**
A-stable and of order $\ge 3$, that single example would **refute** the
barrier. One counterexample disproves a universal claim, and the verification
of that one example is a finite, exact computation: check the order conditions
symbolically over the rationals, and check A-stability by confirming that
$\rho(\zeta) - z\sigma(\zeta)$ has all roots in $|\zeta| \le 1$ for
$\operatorname{Re}z \le 0$ (decidable by a Routh-Hurwitz / Schur-Cohn test, not
by sampling $z$).

So the search is a **valid refutation procedure**.

### The absence of hits establishes nothing of the kind

Finding nothing establishes only that nothing was found in the region searched,
at the resolution searched. Three gaps, each fatal on its own:

1. **The coefficient space is uncountable.** A grid misses all but a
   measure-zero subset, and the barrier is a statement about every real
   coefficient vector.
2. **$k$ is unbounded.** A search to $k \le 4$ says nothing about $k = 17$, and
   the theorem quantifies over all $k$.
3. **A-stability is itself a universal claim** over
   $\{\operatorname{Re}z\le0\}$. Testing it on a grid of $z$ can only fail to
   find instability; a method passing the grid test may be unstable at an
   untested $z$.

Gap 3 is worth separating out because it is the one a careful searcher still
gets wrong: even for a *single* candidate method, numerically sampling $z$ does
not establish A-stability. That needs an algebraic criterion, and such criteria
exist: which is why a hit **can** be certified while an exhaustive absence
cannot.

**Conclusion.** The search is evidence consistent with the barrier and not a
proof of it. Reporting "we searched and found nothing, therefore the barrier
holds" inverts the only direction the method supports.

## Part 4: a conjecture a search can settle

> "Every BDF method of $k$ steps is A-stable."

**This is false**, and a single witness settles it.

Take **BDF3**:

$$\tfrac{11}{6}y_{n+3} - 3y_{n+2} + \tfrac32 y_{n+1} - \tfrac13 y_n
  = h\,f(t_{n+3}, y_{n+3}).$$

Its stability region excludes a wedge about the negative real axis near
infinity: there exist $z$ with $\operatorname{Re}z < 0$ at which $\rho(\zeta) -
z\sigma(\zeta)$ has a root of modulus $> 1$.

Measured: at $z = -0.01 + 1.14i$ (in the open left half-plane, close to the
imaginary axis) the root moduli of BDF3's stability polynomial are

$$\{1.039602,\; 0.387879,\; 0.381402\},$$

with the largest exceeding 1. The method is therefore **not A-stable**, and one
such $z$ is a complete proof of that.

**Where the violation lives matters.** It is *not* on the negative real axis.
Sampling 400 points along $(-\infty, 0)$ gives a maximum root modulus of
$0.999$: BDF3 looks A-stable from there. The unstable set is the thin sliver
near the imaginary axis that the $A(\alpha)$ wedge excludes, and measuring
along rays confirms the published half-angle:

| ray half-angle | max root modulus |
|---|---|
| $80°$ | $0.998265$ |
| $84°$ | $0.998955$ |
| $86°$ | $0.999623$ |
| $86.03°$ | $0.999956$ |
| $87°$ | $\mathbf{1.010799}$ |
| $89°$ | $1.033734$ |

The root condition first fails between $86.03°$ and $87°$, matching the
published $86.03°$ to about one part in $10^{4}$.

This is also a direct demonstration of gap 3 in Part 3: a sampled A-stability
test *for a single method* can miss instability if the violating set is thin
and the samples are badly placed. A scan of 4000 points spread over the
half-plane found 96 violations; a scan of the negative real axis found none.

**Which direction is this?** The existential one. The claim "every BDF is
A-stable" is universal, its negation is existential, and an exact witness
settles an existential claim. This is precisely the half that a search *can*
do, and Part 3's conclusion is the other half.

## Remarks

* The **first** Dahlquist barrier is the companion result: a zero-stable
  $k$-step LMM has order at most $k+2$ for even $k$, $k+1$ for odd $k$, and at
  most $k$ if it is explicit.
* The practical escape from the second barrier is to leave the LMM class:
  implicit Runge-Kutta (Radau IIA, Gauss), or one-leg and general linear
  methods. `scipy.integrate.Radau` is a 5th-order A-stable (indeed L-stable)
  implicit RK method, and is not a counterexample to anything.
* The error constant claim means the trapezoidal rule is the *unique* optimal
  A-stable LMM of order 2, which is a strong statement and part of why it is so
  widely used: see `trapezoidal-is-a-stable-but-not-l-stable` for what it still
  does not give you.
