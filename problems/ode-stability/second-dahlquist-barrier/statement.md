# The second Dahlquist barrier

## Assumptions

A **linear multistep method** (LMM) with $k$ steps is

$$\sum_{j=0}^{k}\alpha_j\,y_{n+j} \;=\; h\sum_{j=0}^{k}\beta_j\,f(t_{n+j}, y_{n+j}),
\qquad \alpha_k \neq 0 ,$$

normalised by $\alpha_k = 1$. Its **characteristic polynomials** are

$$\rho(\zeta) = \sum_{j=0}^{k}\alpha_j\zeta^{j},
\qquad \sigma(\zeta) = \sum_{j=0}^{k}\beta_j\zeta^{j}.$$

The method has **order $p$** if
$\rho(e^{h}) - h\,\sigma(e^{h}) = O(h^{p+1})$ as $h \to 0$.

It is **A-stable** if its region of absolute stability contains the closed left
half-plane, equivalently if every root of
$\rho(\zeta) - z\sigma(\zeta)$ lies in $|\zeta| \le 1$ for every $z$ with
$\operatorname{Re}z \le 0$.

## Part 1 (order conditions)

Show that the order conditions are

$$\sum_{j=0}^{k}\alpha_j = 0,
\qquad
\sum_{j=0}^{k} j^{\,i}\alpha_j \;=\; i\sum_{j=0}^{k}j^{\,i-1}\beta_j
\quad\text{for } i = 1,\dots,p .$$

Verify them for the trapezoidal rule ($k = 1$) and confirm it has order 2.

## Part 2 (the theorem, quoted)

**Second Dahlquist barrier (Dahlquist, 1963).** An A-stable linear multistep
method has order $p \le 2$. Among A-stable methods of order 2, the trapezoidal
rule has the smallest error constant.

State clearly:

1. what is quantified over ($k$, $\alpha$, $\beta$);
2. why this is **not** contradicted by A-stable Runge-Kutta methods of
   arbitrarily high order;
3. why it is not contradicted by the BDF family.

## Part 3 (what a search can and cannot do)

Suppose you search numerically over the coefficients of $k$-step methods for
$k \le 4$, testing order and A-stability on a fine grid, and find nothing of
order $> 2$ that is A-stable.

**Decide precisely what that establishes.** Address both directions:

* what would a single hit establish?
* what does the absence of hits establish?

## Part 4 (a conjecture a search can settle)

Consider instead the specific claim:

> "Every BDF method of $k$ steps is A-stable."

Decide it, and say which of Part 3's two directions your evidence belongs to.

## What a complete answer contains

1. The order conditions derived and checked for the trapezoidal rule.
2. The three points in Part 2, each in one or two sentences.
3. For Part 3, an explicit statement of the asymmetry, not a hedge.
4. For Part 4, a decision with a witness.
