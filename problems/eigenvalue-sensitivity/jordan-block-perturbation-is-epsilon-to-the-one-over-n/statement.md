# A Jordan block's eigenvalues move like the $n$-th root of the perturbation

## Assumptions

Let $J_n$ be the $n\times n$ nilpotent Jordan block,

$$J_n = \begin{pmatrix}
0 & 1 & & \\
 & 0 & \ddots & \\
 & & \ddots & 1 \\
 & & & 0
\end{pmatrix},$$

so $\operatorname{spec}(J_n) = \{0\}$ with algebraic multiplicity $n$ and
geometric multiplicity 1 (the only eigenvectors are multiples of $e_1$).

For $\epsilon > 0$ define the perturbation in the bottom-left corner,

$$J_n(\epsilon) = J_n + \epsilon\, e_ne_1^{\mathsf T}.$$

Note $\|\epsilon\,e_ne_1^{\mathsf T}\|_2 = \epsilon$.

## Part 1

Compute the characteristic polynomial of $J_n(\epsilon)$ exactly and deduce

$$\boxed{\ \operatorname{spec}\big(J_n(\epsilon)\big)
   = \big\{\,\epsilon^{1/n}\,\omega^{k} \;:\; k = 0,\dots,n-1 \,\big\},
   \qquad \omega = e^{2\pi i/n}\ }$$

so every eigenvalue has modulus exactly $\epsilon^{1/n}$.

## Part 2

Tabulate the amplification $\epsilon^{1/n}/\epsilon$ for
$n \in \{2, 8, 16\}$ at $\epsilon = 10^{-16}$, and state what this means for
computing the eigenvalues of a defective matrix in double precision.

## Part 3

Explain why **first-order perturbation theory does not apply**. Specifically:

* state the standard first-order formula
  $\delta\lambda \approx \dfrac{y^{*}Ex}{y^{*}x}$ with $x, y$ the right and
  left eigenvectors;
* compute $y^{*}x$ for $J_n$ and say what goes wrong;
* identify the correct form of the expansion.

## Part 4

Reconcile this with `hermitian-eigenvalues-are-perfectly-conditioned`: why is
there no contradiction with Weyl's inequality?

## What a complete answer contains

1. The characteristic polynomial derived, not asserted.
2. The amplification table.
3. For Part 3, the explicit value of $y^{*}x$ and the Puiseux form of the
   expansion.
4. A one-sentence resolution of Part 4.
