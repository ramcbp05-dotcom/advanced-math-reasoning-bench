# Flawed solution: `double-precision-measurement-of-kappa`

## The submitted argument

> **Steps 1-2.** [Parts 1 and 2 answered correctly.]
>
> **Step 3.** To measure the growth constant, build $H_n$ for
> $n = 2,\dots,20$ with `numpy` and fit $\ln\kappa_2$ against $n$:
>
> ```python
> ns = range(2, 21)
> ks = [np.linalg.cond(scipy.linalg.hilbert(n), 2) for n in ns]
> slope = np.polyfit(ns, np.log(ks), 1)[0]
> ```
>
> **Step 4.** This returns a slope of about $2.3$, against the theoretical
> $3.53$. The measured growth is therefore slower than the asymptotic formula
> predicts, and the formula overestimates $\kappa_2$ for moderate $n$.

## Where it breaks

**Step 3**, at the point where `np.linalg.cond` is asked for a number larger
than double precision can represent as a ratio.

Two separate things go wrong, both in the same place:

**(i) The matrix is already perturbed.** $(H_n)_{ij} = 1/(i+j-1)$ is not
representable in binary for most $i+j$, so `scipy.linalg.hilbert(n)` is $H_n +
E$ with $\|E\|_2 \approx u\|H_n\|_2 \approx 2\times10^{-16}$. By Weyl's
inequality every eigenvalue moves by up to that amount. For $n = 20$ the true
$\lambda_{\min}$ is around $10^{-19}$: a hundred times *smaller* than the
perturbation introduced by writing the matrix down. The computed
$\lambda_{\min}$ has no significant digits.

**(ii) The ratio saturates.** Once $\lambda_{\min}$ is at the noise floor,
$\kappa_2$ is measured as roughly $\|H_n\|_2/(u\|H_n\|_2) = 1/u \approx
10^{16}$ and stops growing. The $\kappa$ values for $n = 14, \dots, 20$ are all
around $10^{16}$ to $10^{18}$ regardless of $n$, which is what pulls the fitted
slope down from $3.53$ to $2.3$.

So Step 4's conclusion is exactly backwards: the measurement did not show the
formula overestimates, it showed the measurement saturated.

## The correct measurement

Restrict the fit to the range where the computation is meaningful, $2 \le n \le
13$, and compute the eigenvalues from the **exact rational** entries at
extended precision. That gives a slope of $3.5306$ against the theoretical
$3.5255$, agreeing to 0.15 %.

The diagnostic that flags the problem without knowing the answer: plot the
residuals of the fit. A clean exponential gives residuals at the level of the
eigensolver; the saturating range gives residuals that grow monotonically and
systematically, which is a model mismatch rather than noise.

The cheaper diagnostic: **any reported condition number within a factor of ten
of $1/u$ should be read as a lower bound.** `numpy` will happily return
$2\times10^{17}$ for a matrix whose true condition number is $10^{25}$; there
is no warning, because there is nothing anomalous about the floating-point
computation: it faithfully reports the condition number of the matrix it was
given, which is not the matrix that was meant.

## Failure mode

`measurement-beyond-precision`: a quantity is measured in arithmetic that
cannot represent it, and the saturated value is treated as data.
