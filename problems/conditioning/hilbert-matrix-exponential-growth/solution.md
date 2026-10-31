# Solution

## Part 1: positive definiteness

Let $c \in \mathbb{R}^n$, $c \neq 0$, and let
$p(x) = \sum_{k=1}^{n} c_k x^{k-1}$, a polynomial of degree at most $n-1$.
Then

$$c^{\mathsf T}H_nc
  = \sum_{i,j} c_ic_j\frac{1}{i+j-1}
  = \sum_{i,j} c_ic_j\int_0^1 x^{i-1}x^{j-1}\,dx
  = \int_0^1 \Big(\sum_k c_kx^{k-1}\Big)^{2}dx
  = \int_0^1 p(x)^2\,dx \;\ge\; 0 .$$

Strictness: if $\int_0^1 p^2 = 0$ then $p \equiv 0$ on $[0,1]$ (the integrand
is continuous and non-negative). A nonzero polynomial of degree $\le n-1$ has
at most $n-1$ roots, so it cannot vanish on an interval; hence $p \equiv 0$ as a
polynomial, so $c = 0$, contradicting $c \neq 0$.

Therefore $c^{\mathsf T}H_nc > 0$ for all $c \neq 0$: $H_n$ is symmetric
positive definite. $\blacksquare$

**Consequences.** All eigenvalues are strictly positive, so $H_n$ is
nonsingular for every $n$. For a symmetric positive definite matrix the
singular values *are* the eigenvalues, so by
`cond2-is-singular-value-ratio`,

$$\kappa_2(H_n) = \frac{\lambda_{\max}(H_n)}{\lambda_{\min}(H_n)} .$$

## Part 2: the determinant

Cauchy's formula gives, exactly:

| $n$ | $\det H_n$ | decimal |
|---|---|---|
| 4 | $1/6{,}048{,}000$ | $1.653\times10^{-7}$ |
| 5 | $1/266{,}716{,}800{,}000$ | $3.749\times10^{-12}$ |
| 8 | $1/365{,}356{,}847{,}125{,}734{,}485{,}878{,}112{,}256{,}000{,}000$ | $2.737\times10^{-33}$ |
| 12 | $1/3.791\times10^{77}$ | $2.638\times10^{-78}$ |

(`verify.py` reproduces these from the rational entries and checks them against
the Cauchy product formula independently.)

### Does $\det H_n \to 0$ mean $H_n$ becomes singular?

**No**, and the question is the point of including Part 2.

Every $H_n$ is positive definite, hence nonsingular, with
$\det H_n > 0$ strictly. There is no singular matrix in the sequence and no
limit being approached — the matrices have *different sizes*, so they do not
live in a common space in which a limit could be taken at all.

More importantly, even within a fixed size the inference fails, as
`cond2-is-singular-value-ratio` establishes: $10^{-5}I_2$ has determinant
$10^{-10}$ and condition number exactly 1. The determinant is the product of
the eigenvalues, and a product of $n$ numbers each less than 1 is small for
reasons that have nothing to do with conditioning. Here
$\lambda_{\max}(H_{12}) \approx 1.8$ while $\lambda_{\min} \approx 10^{-16}$, so
the determinant is small *and* the matrix is ill-conditioned, but the first
fact is not evidence for the second.

The honest statement is about the **inverse**, not the determinant: the entries
of $H_n^{-1}$ are integers that grow explosively,

| $n$ | $\max_{ij}|(H_n^{-1})_{ij}|$ |
|---|---|
| 4 | $6.48\times10^{3}$ |
| 5 | $1.79\times10^{5}$ |
| 8 | $4.25\times10^{9}$ |
| 12 | $3.66\times10^{15}$ |

and $\|H_n^{-1}\|_2$ growing like $10^{15}$ at $n = 12$ is what
ill-conditioning means.

## Part 3: the growth constant

Computing $\lambda_{\max}/\lambda_{\min}$ from the exact rational entries at 60
decimal digits (`mpmath.eigsy`, not float64 — see Part 4):

| $n$ | $\kappa_2(H_n)$ |
|---|---|
| 2 | $1.9281\times10^{1}$ |
| 4 | $1.5514\times10^{4}$ |
| 6 | $1.4951\times10^{7}$ |
| 8 | $1.5258\times10^{10}$ |
| 10 | $1.6026\times10^{13}$ |
| 12 | $1.7132\times10^{16}$ |
| 15 | $6.1166\times10^{20}$ |

A least-squares fit of $\ln\kappa_2$ against $n$ over $2 \le n \le 15$ gives

$$\textbf{slope} = 3.4629 \quad\text{against}\quad 4\ln(1+\sqrt2) = 3.5255 ,$$

which is **1.77 % low**. That gap is not noise, and it is not a failure of the
theorem — it is the $\sqrt n$ in the denominator of the asymptotic law. Taking
logs,

$$\ln\kappa_2(H_n) = 4\ln(1+\sqrt2)\,n \;-\; \tfrac12\ln n \;+\; \text{const}
  \;+\; o(1),$$

so a *linear* fit absorbs the $-\tfrac12\ln n$ term into its slope and must come
out low. Fitting $\ln\kappa_2 + \tfrac12\ln n$ instead:

$$\textbf{slope} = 3.5334, \qquad \textbf{0.22 % from } 4\ln(1+\sqrt2).$$

A sharper form of the same evidence is the successive ratios
$\ln(\kappa_{n+1}/\kappa_n)$, which should climb to $4\ln(1+\sqrt2)$ from below
at rate $1/(2n)$:

| $n \to n+1$ | $\ln(\kappa_{n+1}/\kappa_n)$ |
|---|---|
| $4 \to 5$ | $3.4250$ |
| $8 \to 9$ | $3.4757$ |
| $11 \to 12$ | $3.4890$ |
| $14 \to 15$ | $3.4966$ |

Monotone increasing, and short of the limit by $0.029$ at $n = 14$, against a
predicted $1/(2\cdot14) = 0.036$. Each additional row costs a factor of about
$e^{3.5} \approx 33$, so roughly **1.5 decimal digits per row**.

### What the measurement establishes

It establishes that for $2 \le n \le 15$ the computed condition numbers follow
the predicted law closely, that the residual discrepancy has the *shape* the
law's correction term predicts, and that the successive ratios are converging
upward towards the predicted limit rather than to something else.

It does **not** prove the asymptotic law. Fourteen points cannot establish
behaviour as $n \to \infty$; any law agreeing on this range and departing later
is equally consistent with the data. The asymptotic result is Szegő's, proved by
a different route entirely (Hankel-determinant asymptotics and the connection to
Chebyshev approximation on $[0,1]$), and the role of the measurement is to check
that the implementation and the theorem are discussing the same object.

This is the clearest instance in the benchmark of the distinction it is built
around. Note also that the *first* version of this measurement reported
agreement to 0.15 % — a better-looking number obtained from eigenvalues that had
silently saturated at $n = 12, 13$. The worse-looking 1.77 % is the correct one,
and the structure of the discrepancy is what turns it into real evidence. An
agreement that is too good is worth as much suspicion as one that is too bad.

## Part 4: precision limits

Solving $H_nx = b$ in double precision gives a relative error of roughly
$u\,\kappa_2(H_n)$ with $u \approx 1.1\times10^{-16}$:

| $n$ | $u\,\kappa_2$ | correct digits |
|---|---|---|
| 6 | $1.7\times10^{-9}$ | ~9 |
| 8 | $1.7\times10^{-6}$ | ~6 |
| 10 | $1.8\times10^{-3}$ | ~3 |
| 12 | $1.9$ | 0 |

So **$n = 12$** is where the last digit goes, and $n = 11$ already leaves well
under one.

### Why measuring $\kappa_2(H_{20})$ in double precision is meaningless

To compute $\kappa_2 = \lambda_{\max}/\lambda_{\min}$ one must resolve
$\lambda_{\min}$. Representing $H_{20}$ in double precision already perturbs its
entries by a relative $u$, and by Weyl's inequality that moves every eigenvalue
by up to $u\|H_{20}\|_2 \approx 2\times10^{-16}$. The true $\lambda_{\min}$ is
around $10^{-19}$ — smaller than the uncertainty introduced by writing the
matrix down.

The computed $\lambda_{\min}$ is therefore noise, and the reported $\kappa_2$
saturates around $1/u \approx 10^{16}$ regardless of $n$. **Any reported
condition number within a factor of ten of $1/u$ is a property of the
arithmetic, not of the matrix**, and should be read as "at least $10^{16}$".

The fit in Part 3 stops at $n = 13$ for exactly this reason, and even $n = 13$
is computed from 30-digit arithmetic rather than from float64.

## Remarks

* $H_n^{-1}$ has an exact integer closed form involving binomial coefficients,
  which is how the table in Part 2 is computed without any floating point.
* The Hilbert matrix is the standard worked example of ill-conditioning
  precisely because every quantity in it is known in closed form, so numerical
  claims about it can be checked against exact arithmetic rather than against
  another computation.
* The same phenomenon is why polynomial fitting in the monomial basis is a bad
  idea: the normal-equations matrix for degree-$d$ fitting on $[0,1]$ *is* a
  Hilbert-like Gram matrix, and by
  `normal-equations-square-the-condition` the damage is squared.
