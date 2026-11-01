# Solution

## Part 1: the characteristic polynomial

Expand $\det(\lambda I - J_n(\epsilon))$ along the first column. The matrix is

$$\lambda I - J_n(\epsilon) = \begin{pmatrix}
\lambda & -1 & & \\ & \lambda & \ddots & \\ & & \ddots & -1 \\ -\epsilon & & &
\lambda \end{pmatrix},$$

with nonzero entries in the first column only at positions $(1,1) = \lambda$
and $(n,1) = -\epsilon$.

**The $(1,1)$ term.** Deleting row 1 and column 1 leaves the $(n-1)\times(n-1)$
upper triangular matrix $\lambda I - J_{n-1}$, whose determinant is
$\lambda^{n-1}$. Contribution: $\lambda \cdot \lambda^{n-1} = \lambda^{n}$.

**The $(n,1)$ term.** Deleting row $n$ and column 1 leaves the
$(n-1)\times(n-1)$ matrix with $-1$ on its *main* diagonal (the superdiagonal
entries of the original, now shifted onto the diagonal) and $\lambda$ on its
subdiagonal: lower triangular with diagonal $(-1,\dots,-1)$, so its determinant
is $(-1)^{n-1}$. With the cofactor sign $(-1)^{n+1}$ and the entry $-\epsilon$,
the contribution is

$$(-1)^{n+1}\cdot(-\epsilon)\cdot(-1)^{n-1} = -\epsilon .$$

Hence

$$\boxed{\ \det\big(\lambda I - J_n(\epsilon)\big) = \lambda^{n} - \epsilon\ }$$

(verified symbolically for $n = 2,\dots,10$ in `verify.py`).

The roots are the $n$-th roots of $\epsilon$:

$$\lambda_k = \epsilon^{1/n}e^{2\pi ik/n}, \qquad k = 0,\dots,n-1,$$

each of modulus exactly $\epsilon^{1/n}$. $\blacksquare$

The eigenvalues lie on a circle of radius $\epsilon^{1/n}$, equally spaced: the
perturbation does not merely move them, it *resolves* the defective eigenvalue
into a regular $n$-gon.

## Part 2: amplification

At $\epsilon = 10^{-16}$ (double rounding level):

| $n$ | $\epsilon^{1/n}$ | amplification $\epsilon^{1/n}/\epsilon$ |
|---|---|---|
| 2 | $10^{-8}$ | $10^{8}$ |
| 4 | $10^{-4}$ | $10^{12}$ |
| 8 | $10^{-2}$ | $10^{14}$ |
| 16 | $10^{-1}$ | $10^{15}$ |

Measured values agree with $\epsilon^{1/n}$ to a ratio of **1.0000** in every
case.

**What this means.** Storing $J_{16}$ in double precision and computing its
eigenvalues returns numbers of modulus around $0.1$ scattered on a circle,
where the true spectrum is $\{0\}$. The computation is not wrong: a
backward-stable eigensolver returns the exact eigenvalues of $J_{16} + E$ with
$\|E\| \approx u$, and those really are at radius $u^{1/16} \approx 0.1$.

**There is no algorithm that does better**, because the information is not in
the stored matrix. Two matrices differing by $10^{-16}$ have genuinely
different spectra, one $\{0\}$ and one a circle of radius $0.1$. This is the
clearest case in the benchmark where the *problem*, not the method, is the
difficulty.

## Part 3: why first-order theory fails

For a **simple** eigenvalue $\lambda$ of $A$ with right eigenvector $x$ and
left eigenvector $y$ ($y^{*}A = \lambda y^{*}$), the standard first-order
result is

$$\lambda(A + tE) = \lambda + t\,\frac{y^{*}Ex}{y^{*}x} + O(t^2),$$

and $1/|y^{*}x|$ (with $x, y$ unit) is the **eigenvalue condition number**.

For $J_n$ with $n \ge 2$:

* the right eigenvector for $\lambda = 0$ is $x = e_1$ (up to scale), since
  $J_ne_1 = 0$;
* the left eigenvector is $y = e_n$, since $e_n^{\mathsf T}J_n = 0$;
* therefore $y^{*}x = e_n^{\mathsf T}e_1 = \boxed{0}$.

The condition number $1/|y^{*}x|$ is **infinite**, and the formula divides by
zero. This is not a removable singularity or a case to be handled with care:
the expansion itself does not exist.

### The correct expansion

The eigenvalue has algebraic multiplicity $n$ and geometric multiplicity 1, so
it is defective, and the perturbation expansion is a **Puiseux series** in
$t^{1/n}$ rather than a Taylor series in $t$:

$$\lambda(t) = \lambda_0 + c_1 t^{1/n} + c_2 t^{2/n} + \cdots$$

Here $\lambda_0 = 0$ and the leading term is exactly $t^{1/n}$, which Part 1
establishes with no series at all. The derivative $d\lambda/dt$ is unbounded at
$t = 0$, which is the analytic statement of "infinite condition number".

A left and right eigenvector becoming orthogonal is exactly the signature of an
approaching defective eigenvalue, and $y^{*}x \to 0$ is how a code detects the
situation before it divides by it.

## Part 4: no contradiction with Weyl

Weyl's inequality assumes $A$ and $E$ **Hermitian**. $J_n$ is as far from
Hermitian as a matrix gets: it is nilpotent, so all its eigenvalues are 0 while
$\|J_n\|_2 = 1$, giving a spectral radius of 0 against a norm of 1.

A Hermitian matrix with spectral radius 0 is the zero matrix. The two results
are statements about disjoint classes, and the gap between them (amplification
1 against amplification $10^{15}$) is a measure of how much normality buys.

## Remarks

* $\epsilon$ in the bottom-left corner is the worst case, but it is not
  special: a generic perturbation of size $\epsilon$ produces eigenvalues of
  modulus $O(\epsilon^{1/n})$ too, because the characteristic polynomial's
  constant term picks up a generic $O(\epsilon)$ contribution.
* The circle of radius $\epsilon^{1/n}$ is the boundary of the
  **$\epsilon$-pseudospectrum** of $J_n$, and this example is the standard
  motivation for pseudospectra: for a non-normal matrix the spectrum alone does
  not predict behaviour, and the set of eigenvalues reachable under small
  perturbations does.
* The same phenomenon limits root-finding by companion matrix: a polynomial
  with a root of multiplicity $m$ has that root computed to only $u^{1/m}$
  accuracy, whatever the method. See `wilkinson-polynomial-root-sensitivity`
  for the version with *simple* roots, where the mechanism is different and the
  damage is comparable.
