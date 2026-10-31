# Flawed solution: `triangular-means-eigenvalues-suffice`

## The submitted argument

> **Step 1.** Part 1 is standard: normality gives $\sigma_i = |\lambda_i|$.
>
> **Step 2.** For Part 2, consider the candidate
> $A_t = \begin{pmatrix}1&t\\0&1\end{pmatrix}$.
>
> **Step 3.** $A_t$ is triangular, so its eigenvalues are its diagonal entries,
> both 1 — and for a triangular matrix the diagonal entries are the complete
> spectral information, since the characteristic polynomial is
> $\prod_i (x - a_{ii})$.
>
> **Step 4.** Since the spectrum is $\{1\}$ and the matrix is a bounded
> perturbation of the identity, $\kappa_2(A_t)$ stays near 1 and $A_t$ is not a
> counterexample. No counterexample exists.

## Where it breaks

**Step 3-4**, at the inference from "the diagonal is the spectrum" to "the
diagonal is what matters".

Step 3 is correct as stated: for a triangular matrix the characteristic
polynomial really is $\prod_i(x - a_{ii})$, and the eigenvalues really are
visible on the diagonal. What does not follow is that the *rest of the matrix is
irrelevant*. $A_t$ and $A_0 = I$ have identical spectra and completely different
norms:

$$\|A_t\|_2 \approx t, \qquad \|A_0\|_2 = 1 .$$

"A bounded perturbation of the identity" in Step 4 is also wrong:
$\|A_t - I\|_2 = t$, which is unbounded.

The off-diagonal entry is precisely the information the eigenvalues discard,
and for a triangular matrix it is the entire difference between the matrix and
a diagonal one.

## The measurement that settles it

$\sigma_\pm(A_t)$ satisfy $\sigma_+\sigma_- = |\det A_t| = 1$ and
$\sigma_+^2 + \sigma_-^2 = \|A_t\|_F^2 = 2 + t^2$. So
$\sigma_+ \approx t$ and $\sigma_- \approx 1/t$, giving $\kappa_2 \approx t^2$
— from two one-line identities, without computing an SVD.

At $t = 10^{6}$: $\kappa_2 = 10^{12}$ while the eigenvalue ratio is 1.

## The general lesson

Schur's theorem says every matrix is unitarily similar to a triangular one, so
"triangular" is not a special or benign structure — it is the generic case up to
the transformation that preserves $\kappa_2$. The diagonal of the Schur form
carries the eigenvalues and the strictly upper part carries the
**non-normality**, with $A$ normal exactly when that part vanishes. Reading the
diagonal and discarding the rest is discarding precisely the quantity this
problem is about.

## Failure mode

`visible-is-not-sufficient`: a quantity that is easy to read off is treated as
the quantity that determines the answer.
