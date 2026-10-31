# Eigenvalues are continuous; eigenvectors are not

## Assumptions

All matrices are real symmetric $2\times2$, so eigenvalues are real and an
orthonormal eigenbasis always exists. Eigenvectors are normalised to unit
length; the residual sign ambiguity $v \mapsto -v$ is accounted for by
comparing the **lines** $\operatorname{span}(v)$, or equivalently by using
$|\langle u, v\rangle|$.

## Part 1 (background, may be quoted)

Eigenvalues depend continuously on the entries: the characteristic polynomial's
coefficients are polynomials in the entries, and the roots of a monic
polynomial depend continuously on its coefficients. This holds for **every**
matrix, with no hypothesis.

State why this does *not* imply anything about eigenvectors.

## Part 2 (existential)

Let $A = I_2$, whose eigenvalue $1$ is degenerate with a two-dimensional
eigenspace. Consider the two families

$$B(\epsilon) = \begin{pmatrix}1+\epsilon & 0\\ 0 & 1-\epsilon\end{pmatrix},
\qquad
C(\epsilon) = \begin{pmatrix}1 & \epsilon\\ \epsilon & 1\end{pmatrix},
\qquad \epsilon > 0 .$$

Show that:

1. $\|B(\epsilon) - A\|_2 = \|C(\epsilon) - A\|_2 = \epsilon$, so the two
   perturbations have the **same size**;
2. the eigenvalues of both converge to $\{1, 1\}$ as $\epsilon \to 0^{+}$, at
   rate exactly $\epsilon$ (consistent with Weyl);
3. the eigenvector for the **larger** eigenvalue is $e_1$ for $B(\epsilon)$ and
   $(1,1)/\sqrt2$ for $C(\epsilon)$, for **every** $\epsilon > 0$ — so the two
   limits differ by $45°$ and the eigenvector has no limit as
   $\epsilon \to 0^{+}$ over all perturbations.

## Part 3

The eigenvector map is discontinuous; identify what **is** continuous at a
degenerate eigenvalue, and state the correct theorem informally.

## Part 4

Give the practical consequence: what should a numerical code report in place of
an eigenvector when eigenvalues are clustered, and what quantity measures the
sensitivity of an eigenvector of a *simple* eigenvalue?

## What a complete answer contains

1. The three computations in Part 2, exactly.
2. An explicit statement that the discontinuity survives normalisation and is
   not the sign ambiguity.
3. The correct continuous object in Part 3.
