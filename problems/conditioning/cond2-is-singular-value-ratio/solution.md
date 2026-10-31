# Solution

## Part 1

### Step 1: the operator norm is the largest singular value

Let $A = U\Sigma V^{*}$ be a singular value decomposition, with $U, V$ unitary
and $\Sigma = \operatorname{diag}(\sigma_1,\dots,\sigma_n)$.

Unitary matrices preserve the Euclidean norm, so for any $x$,

$$\|Ax\|_2 = \|U\Sigma V^{*}x\|_2 = \|\Sigma V^{*}x\|_2 ,
\qquad \|x\|_2 = \|V^{*}x\|_2 .$$

Writing $y = V^{*}x$, which ranges over all of $\mathbb{C}^n$ as $x$ does,

$$\|A\|_2
  = \max_{y \neq 0} \frac{\|\Sigma y\|_2}{\|y\|_2}
  = \max_{y \neq 0} \frac{\left(\sum_i \sigma_i^2 |y_i|^2\right)^{1/2}}
                         {\left(\sum_i |y_i|^2\right)^{1/2}} .$$

The quotient is a weighted average of the $\sigma_i^2$, so it is at most
$\sigma_1^2$, with equality at $y = e_1$. Hence $\|A\|_2 = \sigma_1$.

### Step 2: the inverse

From $A = U\Sigma V^{*}$ and nonsingularity, $A^{-1} = V\Sigma^{-1}U^{*}$, which
is a singular value decomposition of $A^{-1}$ once the diagonal entries
$\sigma_n^{-1} \ge \cdots \ge \sigma_1^{-1}$ are put in decreasing order (which
only permutes the columns of $V$ and $U$). Applying Step 1 to $A^{-1}$,

$$\|A^{-1}\|_2 = \frac{1}{\sigma_n}.$$

### Step 3: combine

$$\kappa_2(A) = \|A\|_2\|A^{-1}\|_2 = \frac{\sigma_1}{\sigma_n}. \qquad\blacksquare$$

### Corollary 1: $\kappa_2 \ge 1$, with the equality case

$\sigma_1 \ge \sigma_n > 0$ gives $\kappa_2(A) \ge 1$ immediately.

Equality holds iff $\sigma_1 = \sigma_n$, i.e. all singular values are equal to
some $\sigma > 0$. Then $\Sigma = \sigma I$ and

$$A = U(\sigma I)V^{*} = \sigma\,(UV^{*}),$$

a scalar multiple of the unitary matrix $UV^{*}$. Conversely if $A = cQ$ with
$Q$ unitary then $A^{*}A = |c|^2 I$, so every singular value is $|c|$ and
$\kappa_2 = 1$. The two directions give the "if and only if". $\blacksquare$

### Corollary 2: scale invariance

The singular values of $cA$ are $|c|\sigma_i$, so

$$\kappa_2(cA) = \frac{|c|\sigma_1}{|c|\sigma_n} = \kappa_2(A).$$

This corollary is the heart of Part 2, and it is worth stating before the
counterexamples: **$\kappa_2$ is invariant under scaling and $\det$ is not**,
since $\det(cA) = c^n \det A$. No scale-invariant quantity can be a function of
a scale-dependent one alone, so no formula of the form $\kappa_2 = f(\det A)$
can exist for $n \ge 1$ with $c$ free. Both parts of Part 2 are corollaries of
this observation; the explicit witnesses below merely make it concrete.

## Part 2

### (a) is false

Take

$$A = \begin{pmatrix} 10^{5} & 0 \\ 0 & 10^{-5}\end{pmatrix}.$$

$A$ is diagonal with positive entries, so its singular values are exactly
$\sigma_1 = 10^{5}$ and $\sigma_2 = 10^{-5}$. Then

$$\det A = 1, \qquad \kappa_2(A) = \frac{10^{5}}{10^{-5}} = 10^{10}.$$

The determinant is as far from zero as one could wish and the matrix loses ten
digits. $\blacksquare$

### (b) is false

Take

$$B = 10^{-5} I_2 = \begin{pmatrix} 10^{-5} & 0 \\ 0 & 10^{-5}\end{pmatrix}.$$

Both singular values are $10^{-5}$, so

$$\det B = 10^{-10}, \qquad \kappa_2(B) = 1 .$$

$B$ is a scalar multiple of the identity: perfectly conditioned, by Corollary 1.
$\blacksquare$

### Why the determinant cannot do this job

Both witnesses are instances of the scaling argument above, and the mechanism is
worth naming. The determinant is the **product** of the singular values,

$$|\det A| = \prod_{i=1}^{n}\sigma_i ,$$

while $\kappa_2$ is a **ratio of the extremes**. A product is blind to how the
factors are distributed: $10^{5}\cdot 10^{-5}$ and $1 \cdot 1$ are the same
number and describe utterly different matrices. Conversely a ratio is blind to
overall scale.

The two quantities measure different things, and the confusion is helped along
by the $2\times 2$ case over the integers, where a small determinant often does
accompany near-dependence of the rows. That correlation is an artefact of
holding the row norms fixed; it is not a theorem.

The sharp statement in the neighbourhood of this folklore is a different one:
$\sigma_n = \min\{\|A - B\|_2 : B \text{ singular}\}$, so $1/\kappa_2(A)$ is the
*relative* distance to singularity. It is $\sigma_n$ relative to $\sigma_1$ that
matters, never $\det$.

## Remarks

* The identity fails for other norms. For the Frobenius norm,
  $\|A\|_F = \big(\sum_i \sigma_i^2\big)^{1/2}$, so $\|A\|_F = \sigma_1$ only
  when $\operatorname{rank}(A) = 1$. The quantity $\|A\|_F\|A^{-1}\|_F$ is a
  legitimate condition number for some purposes, but it is not $\sigma_1/\sigma_n$
  and can exceed it by a factor of up to $n$.
* For a Hermitian positive definite $A$ the singular values are the eigenvalues,
  so $\kappa_2(A) = \lambda_{\max}/\lambda_{\min}$. For a general matrix the
  eigenvalues say nothing about $\kappa_2$ --- a nilpotent Jordan block has all
  eigenvalues zero and is perfectly ordinary in norm.
