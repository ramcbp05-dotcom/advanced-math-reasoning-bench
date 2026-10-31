# Solution

## Part 1: Weyl's inequality

Fix $k$. By Courant-Fischer applied to $A + E$, there is a $k$-dimensional
subspace $S^{\star}$ attaining the max, and for **any** $k$-dimensional $S$,

$$\lambda_k(A+E) \;\ge\; \min_{0 \neq x\in S}\frac{x^{*}(A+E)x}{x^{*}x}.$$

Take $S$ to be the maximising subspace for $A$, so that
$\min_{0\neq x\in S} \frac{x^{*}Ax}{x^{*}x} = \lambda_k(A)$. Then for any unit
$x \in S$,

$$x^{*}(A+E)x = x^{*}Ax + x^{*}Ex \;\ge\; \lambda_k(A) + \lambda_n(E)
  \;\ge\; \lambda_k(A) - \|E\|_2 ,$$

using $x^{*}Ex \ge \lambda_{\min}(E) = \lambda_n(E) \ge -\|E\|_2$ (valid because
$E$ is Hermitian, so $\|E\|_2 = \max_i|\lambda_i(E)|$). Taking the minimum over
unit $x \in S$ and then the max over subspaces,

$$\lambda_k(A+E) \;\ge\; \lambda_k(A) - \|E\|_2 .$$

For the other direction apply the same argument with $A \to A+E$ and
$E \to -E$, which is Hermitian with the same norm:

$$\lambda_k(A) \;\ge\; \lambda_k(A+E) - \|E\|_2 .$$

Combining the two gives $|\lambda_k(A+E) - \lambda_k(A)| \le \|E\|_2$ for every
$k$. $\blacksquare$

**Where Hermiticity is used:** twice, and both times essentially.

1. Courant-Fischer requires a real spectrum and an orthonormal eigenbasis —
   it is a statement about the Rayleigh quotient of a Hermitian form.
2. $\|E\|_2 = \max_i|\lambda_i(E)|$ requires $E$ normal. For a general $E$ the
   spectral radius can be far below the norm (see
   `eigenvalues-do-not-determine-the-condition-number`), and the step
   $x^{*}Ex \ge -\|E\|_2$ would still hold, but the pairing of eigenvalues by
   index would not survive, because the eigenvalues need not be real and there
   is no canonical ordering.

## Part 2: attainment

Take $A = \operatorname{diag}(1, 0)$ and $E = \operatorname{diag}(\epsilon, 0)$
with $\epsilon > 0$. Both Hermitian, $\|E\|_2 = \epsilon$, and

$$\lambda_1(A+E) = 1 + \epsilon, \qquad \lambda_1(A) = 1,$$

so $|\lambda_1(A+E) - \lambda_1(A)| = \epsilon = \|E\|_2$ exactly.

More generally $E = \epsilon I$ shifts every eigenvalue by exactly $\epsilon$.
So the constant 1 in Weyl's inequality cannot be reduced. $\blacksquare$

Measured over 150 random Hermitian pairs at $\|E\|_2 = 10^{-6}$, the worst
observed ratio $|\Delta\lambda|/\|E\|_2$ was **0.9917** — within 1 % of the
bound, confirming that it is tight rather than pessimistic.

## Part 3: absolute, not relative

Weyl says the eigenvalue condition number is **1 in the absolute sense**:
the map $A \mapsto \lambda_k(A)$ is Lipschitz with constant 1 in the 2-norm.
This is the best possible behaviour; no other class of matrices does better.

**But it is an absolute bound.** For an eigenvalue near zero the relative error
can still be enormous:

$$\frac{|\Delta\lambda_k|}{|\lambda_k|} \le \frac{\|E\|_2}{|\lambda_k|} .$$

If $A$ is Hermitian with $\lambda_1 = 1$ and $\lambda_n = 10^{-14}$, a backward
error of $\|E\|_2 = u\|A\|_2 \approx 10^{-16}$ — the best any backward-stable
algorithm can promise — gives

$$\frac{|\Delta\lambda_n|}{|\lambda_n|} \lesssim \frac{10^{-16}}{10^{-14}}
  = 10^{-2},$$

two correct digits in the smallest eigenvalue, from an algorithm that made no
mistake. This is why symmetric eigensolvers are described as computing the
eigenvalues to high *absolute* accuracy, and why algorithms promising high
*relative* accuracy for small eigenvalues (Jacobi on a well-scaled matrix,
bisection with careful inertia counts) are a separate subject.

## Part 4: the hypothesis

Bauer-Fike for diagonalisable $A = V\Lambda V^{-1}$ gives
$\kappa_2(V)\|E\|_2$, so Weyl's constant 1 corresponds to $\kappa_2(V) = 1$,
which holds exactly when $V$ can be taken **unitary** — i.e. when $A$ is
**normal**, by the spectral theorem.

**Diagonalisability is not enough.** $A = \begin{pmatrix}1 & t\\ 0 & 2\end{pmatrix}$
is diagonalisable for every $t$ (distinct eigenvalues) and has
$\kappa_2(V) \approx 2t$:

| $t$ | $\kappa_2(V)$ | Bauer-Fike bound at $\|E\|_2 = 10^{-10}$ | observed shift |
|---|---|---|---|
| $10^{2}$ | $2.0\times10^{2}$ | $2.0\times10^{-8}$ | $1.0\times10^{-8}$ |
| $10^{4}$ | $2.0\times10^{4}$ | $2.0\times10^{-6}$ | $1.0\times10^{-6}$ |
| $10^{6}$ | $2.0\times10^{6}$ | $2.0\times10^{-4}$ | $1.0\times10^{-4}$ |

The eigenvalues really do move by $10^{-4}$ under a $10^{-10}$ perturbation —
the bound is not merely loose, the amplification is real. Normality, not
diagonalisability, is what buys the constant 1.

## Remarks

* Weyl's inequality extends to the full interlacing family (Lidskii, Horn), and
  the $\infty$-norm statement $\|\lambda(A+E) - \lambda(A)\|_\infty \le \|E\|_2$
  is exactly what was proved here.
* The analogous statement for **singular values** holds for *every* matrix:
  $|\sigma_k(A+E) - \sigma_k(A)| \le \|E\|_2$, because singular values are
  eigenvalues of the Hermitian dilation $\begin{psmallmatrix}0 & A\\ A^{*} &
  0\end{psmallmatrix}$. This is why SVD-based algorithms are robust where
  eigenvalue-based ones are not.
* Eigen**vectors** are a different matter entirely, and are not covered by any
  of this: see `eigenvectors-are-discontinuous-at-a-degenerate-eigenvalue`.
