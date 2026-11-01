# Flawed solution: `tiny-perturbation-tiny-effect`

## The submitted argument

> **Steps 1-2.** [Characteristic polynomial $\lambda^n - \epsilon$ derived
> correctly, roots identified as $\epsilon^{1/n}\omega^k$.]
>
> **Step 3.** In practice $\epsilon$ is at the level of double rounding,
> $10^{-16}$. A change of that size is below any tolerance we would ever set.
>
> **Step 4.** So although the formula $\epsilon^{1/n}$ is correct in principle,
> in practice the eigenvalues of $J_n$ computed in double precision will be
> accurate to roughly $10^{-16}$ and the phenomenon is of theoretical interest
> only.

## Where it breaks

**Step 3-4**, at the unstated assumption that a small stimulus produces a small
response. The whole content of Steps 1-2 (which the submission derived
correctly) is that this is false here.

Substituting $\epsilon = 10^{-16}$ into the formula the submission itself
derived:

| $n$ | $\epsilon^{1/n}$ at $\epsilon = 10^{-16}$ |
|---|---|
| 2 | $10^{-8}$ |
| 8 | $10^{-2}$ |
| 16 | $\mathbf{10^{-1}}$ |

At $n = 16$ the eigenvalues are at radius $0.1$. The true spectrum is $\{0\}$.
The answer is wrong in the first significant figure.

This is a particularly instructive failure because nothing in Steps 1-2 is
wrong: the submission has the exact formula in hand and does not evaluate it.
Deriving a result and then reasoning about the regime from intuition rather
than from the result is a recurring pattern, and $x^{1/16}$ near zero is
exactly where intuition about "small" fails.

## What Step 4 should have concluded

The computed eigenvalues are *not* accurate to $10^{-16}$, and no algorithm can
make them so. A backward-stable eigensolver returns the exact spectrum of
$J_{16} + E$ with $\|E\| \approx u$, and that spectrum really is at radius
$0.1$. The information is not in the stored matrix: $J_{16}$ and $J_{16} +
10^{-16}e_{16}e_1^{\mathsf T}$ are different matrices with genuinely different
spectra, and double precision cannot tell them apart.

The practical consequences are real rather than theoretical:

* eigenvalues of a nearly defective matrix cannot be computed accurately, and a
  code should report the eigenvalue condition number alongside them;
* polynomial root-finding via the companion matrix inherits this exactly: a
  root of multiplicity $m$ is computed to $u^{1/m}$;
* the **pseudospectrum**, not the spectrum, is what predicts the behaviour of
  non-normal systems, and this example is its standard motivation.

## Failure mode

`assumed-linear-response`: a correct nonlinear formula is derived and then
reasoned about as though the response were proportional to the stimulus.
