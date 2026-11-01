# Solution

## Part 1: the normal case

By the spectral theorem $A = U\Lambda U^{*}$ with $U$ unitary and $\Lambda =
\operatorname{diag}(\lambda_i)$. Then

$$A^{*}A = U\Lambda^{*}U^{*}U\Lambda U^{*} = U|\Lambda|^2U^{*},$$

**using $U^{*}U = I$**: this is the only place normality enters, and it is the
whole of the argument. So the eigenvalues of $A^{*}A$ are $|\lambda_i|^2$, the
singular values of $A$ are $\sigma_i = |\lambda_i|$, and by
`cond2-is-singular-value-ratio`,

$$\kappa_2(A) = \frac{\sigma_1}{\sigma_n} = \frac{|\lambda_1|}{|\lambda_n|}.
\qquad\blacksquare$$

For a general diagonalisation $A = V\Lambda V^{-1}$ the same computation gives
$A^{*}A = V^{-*}\Lambda^{*}V^{*}V\Lambda V^{-1}$, and $V^{*}V$ does **not**
cancel. Everything in Part 3 is an account of what that leftover factor does.

## Part 2: the witness

$$A_t = \begin{pmatrix} 1 & t \\ 0 & 1\end{pmatrix}, \qquad t > 0 .$$

$A_t$ is upper triangular, so its spectrum is its diagonal: $\lambda = 1$ with
algebraic multiplicity 2. Hence $|\lambda_{\max}|/|\lambda_{\min}| = 1$ for
**every** $t$.

### Singular values in closed form

$$A_t^{\mathsf T}A_t = \begin{pmatrix} 1 & t \\ t & 1 + t^2\end{pmatrix},
\qquad \operatorname{tr} = 2 + t^2, \quad \det = 1 .$$

The eigenvalues solve $\mu^2 - (2+t^2)\mu + 1 = 0$, so

$$\mu_\pm = \frac{2 + t^2 \pm t\sqrt{t^2+4}}{2},
\qquad \sigma_\pm = \sqrt{\mu_\pm}, \qquad \mu_+\mu_- = 1 .$$

Since $\sigma_+\sigma_- = \sqrt{\det(A_t^{\mathsf T}A_t)} = 1$ (which is just
$|\det A_t| = 1$),

$$\kappa_2(A_t) = \frac{\sigma_+}{\sigma_-} = \sigma_+^2 = \mu_+
  = \frac{2 + t^2 + t\sqrt{t^2+4}}{2} \;\sim\; t^2 \quad (t \to \infty).$$

Checked exactly:

| $t$ | $\sigma_-$ | $\sigma_+$ | $\kappa_2$ | $t^2$ |
|---|---|---|---|---|
| $10^{2}$ | $9.9990\times10^{-3}$ | $1.0001\times10^{2}$ | $1.0002\times10^{4}$ | $10^{4}$ |
| $10^{4}$ | $9.99999\times10^{-5}$ | $1.0000\times10^{4}$ | $1.0000\times10^{8}$ | $10^{8}$ |
| $10^{6}$ | $10^{-6}$ | $10^{6}$ | $1.0000\times10^{12}$ | $10^{12}$ |

So the eigenvalue ratio is pinned at 1 while $\kappa_2$ runs to infinity
quadratically. $\blacksquare$

**Why this is not a pathology.** $A_t$ is a shear. It is perfectly invertible,
its determinant is 1, and it has no small or clustered eigenvalues. What it has
is a highly non-orthogonal eigenstructure: both eigenvectors are multiples of
$e_1$ (the matrix is defective for $t \neq 0$), so there is no eigenvector
basis at all, let alone an orthogonal one. The eigenvalues are simply not
carrying the information.

## Part 3: the sandwich

Let $A = V\Lambda V^{-1}$ be diagonalisable.

### Lower bound

For any eigenpair $Ax = \lambda x$ with $\|x\|_2 = 1$, $\|A\|_2 \ge \|Ax\|_2 =
|\lambda|$, so $\|A\|_2 \ge |\lambda_1|$. The same applied to $A^{-1}$, whose
eigenvalues are $\lambda_i^{-1}$, gives $\|A^{-1}\|_2 \ge 1/|\lambda_n|$.
Multiplying,

$$\kappa_2(A) \ge \frac{|\lambda_1|}{|\lambda_n|}.$$

(This half needs no diagonalisability: only that $\lambda_1, \lambda_n$ are
eigenvalues. It is the *spectral radius* bound $\rho(A) \le \|A\|$.)

### Upper bound

Submultiplicativity on $A = V\Lambda V^{-1}$:

$$\|A\|_2 \le \|V\|_2\|\Lambda\|_2\|V^{-1}\|_2 = \kappa_2(V)\,|\lambda_1| ,$$

and on $A^{-1} = V\Lambda^{-1}V^{-1}$,

$$\|A^{-1}\|_2 \le \kappa_2(V)\,\frac{1}{|\lambda_n|} .$$

Multiplying,

$$\kappa_2(A) \le \kappa_2(V)^2\,\frac{|\lambda_1|}{|\lambda_n|}. \qquad\blacksquare$$

### The normal case

$A$ normal means $V$ may be taken unitary, so $\kappa_2(V) = 1$ and the
sandwich collapses to the equality of Part 1. **The missing quantity is exactly
$\kappa_2(V)$: the conditioning of the eigenvector basis.**

For the witness $A_t$ there is no eigenvector basis at all, so the sandwich
says nothing; the natural statement for the defective case is the Jordan-form
bound, and the sharp one is through the SVD, which always exists.

## Remarks

* The same quantity $\kappa_2(V)$ governs **eigenvalue** sensitivity through
  the Bauer-Fike theorem, and the same degeneration appears there. That is not
  a coincidence: non-orthogonality of the eigenvectors is the single defect
  behind both, and it is the subject of `bauer-fike-and-when-it-says-nothing`
  in the eigenvalue-sensitivity area.
* A matrix with well-separated eigenvalues can still have $\kappa_2(V)$
  enormous: separation of eigenvalues and orthogonality of eigenvectors are
  independent properties.
* For *real symmetric* and *Hermitian* matrices the whole difficulty vanishes:
  they are normal, $\kappa_2 = |\lambda_1|/|\lambda_n|$, and the eigenvalues
  are perfectly conditioned (see
  `hermitian-eigenvalues-are-perfectly-conditioned`). Most of the trouble in
  numerical linear algebra is a consequence of non-normality.
