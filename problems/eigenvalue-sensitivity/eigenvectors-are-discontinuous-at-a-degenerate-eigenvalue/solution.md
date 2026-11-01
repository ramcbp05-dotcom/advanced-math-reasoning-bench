# Solution

## Part 1: why eigenvalue continuity says nothing about eigenvectors

The map $A \mapsto \operatorname{spec}(A)$ is continuous (as a map into
unordered $n$-tuples) because it factors through the characteristic polynomial.

The eigenvector map is not a map of the same kind. For a given $\lambda$, the
"eigenvector" is any nonzero element of $\ker(A - \lambda I)$: a **subspace**,
not a vector. When the eigenvalue is simple the subspace is one-dimensional and
a unit vector in it is determined up to a sign, so one can speak of *the*
eigenvector. When it is degenerate the subspace has dimension $> 1$ and there
is no canonical choice at all.

Continuity of the eigenvalues is a statement about roots of a polynomial;
nothing in it touches the dimension of a null space, which is exactly what
jumps.

## Part 2: the witness

### (1) the two perturbations have the same size

$$B(\epsilon) - A = \operatorname{diag}(\epsilon, -\epsilon), \qquad
C(\epsilon) - A = \begin{pmatrix}0 & \epsilon\\ \epsilon & 0\end{pmatrix}.$$

The first has singular values $\{\epsilon, \epsilon\}$; the second is
$\epsilon$ times a reflection, so also $\{\epsilon, \epsilon\}$. Hence

$$\|B(\epsilon) - A\|_2 = \|C(\epsilon) - A\|_2 = \epsilon$$

exactly, for every $\epsilon$. Both are symmetric, so Weyl applies to both.

### (2) the eigenvalues converge, at rate $\epsilon$

$B(\epsilon)$ is diagonal: eigenvalues $1 \pm \epsilon$.

$C(\epsilon)$ has trace 2 and determinant $1 - \epsilon^2$, so its eigenvalues
solve $\mu^2 - 2\mu + 1 - \epsilon^2 = 0$, giving $\mu = 1 \pm \epsilon$.

**The two families have identical spectra.** Both converge to $\{1,1\}$, each
eigenvalue moving by exactly $\epsilon = \|E\|_2$: attaining the Weyl bound.

### (3) the eigenvectors do not converge to each other

For $B(\epsilon)$, the larger eigenvalue $1+\epsilon$ has eigenvector $e_1 =
(1,0)$: independent of $\epsilon$.

For $C(\epsilon)$: $(C - (1+\epsilon)I)v = \begin{pmatrix}-\epsilon &
\epsilon\\ \epsilon & -\epsilon\end{pmatrix}v = 0$ gives $v_1 = v_2$, so $v =
(1,1)/\sqrt2$: also independent of $\epsilon$.

The angle between the two lines is

$$\arccos\frac{|\langle e_1, (1,1)/\sqrt2\rangle|}{1} = \arccos\frac{1}{\sqrt2}
  = 45° ,$$

for **every** $\epsilon > 0$. Measured at $\epsilon = 10^{-2}, 10^{-4},
10^{-6}, 10^{-8}$: $45.000000°$ in every case.

So as $\epsilon \to 0^{+}$ the matrices converge to the same limit $A = I$, the
eigenvalues converge to the same limit $\{1,1\}$, and the eigenvectors sit at a
fixed $45°$ apart. The eigenvector map has **no limit** at $A = I$: it depends
on the direction of approach. $\blacksquare$

Indeed every unit vector arises as a limit: perturbing $I$ by
$\epsilon(2vv^{\mathsf T} - I)$ gives top eigenvector $v$ for any unit $v$, so
the set of limit points is the whole unit circle.

### The discontinuity is not the sign ambiguity

Normalising to unit length leaves $v \mapsto -v$; comparing *lines* removes
even that. The two limits here are $45°$ apart, which is neither $0°$ nor
$180°$, so no choice of sign, phase or normalisation reconciles them. This is a
genuine failure of continuity, not a labelling artefact.

## Part 3: what is continuous

**The spectral projector**, equivalently the invariant subspace belonging to a
**separated group** of eigenvalues.

Here the group $\{1+\epsilon, 1-\epsilon\}$ is the whole spectrum, and its
spectral projector is $I$ for both families and for the limit: continuous, and
trivially so. The individual one-dimensional eigenspaces are not a separated
group as $\epsilon \to 0$, which is exactly why they misbehave.

Informally (Kato; Stewart-Sun, *Matrix Perturbation Theory*, Ch. V): if a group
of eigenvalues is separated from the rest of the spectrum by a gap $\delta$,
then the spectral projector onto the corresponding invariant subspace is
Lipschitz in the perturbation with constant $O(1/\delta)$. Eigenvalues may move
freely **within** the group without affecting it.

So the object with good perturbation theory is the invariant subspace of a
cluster, not the eigenvector of an individual eigenvalue inside it.

## Part 4: practical consequences

**What to report.** For clustered eigenvalues a code should return an
orthonormal basis of the **invariant subspace** of the cluster, not individual
eigenvectors. LAPACK's `?syevr`/`?stemr` do this, and `?trsen`/`?trsna` return
subspace condition numbers.

**The sensitivity measure for a simple eigenvalue's eigenvector** is the
reciprocal of the **gap** to the nearest other eigenvalue. The first-order
result is

$$\|\delta v_i\|_2 \;\lesssim\; \frac{\|E\|_2}{\operatorname{gap}_i},
\qquad \operatorname{gap}_i = \min_{j \neq i}|\lambda_i - \lambda_j| ,$$

for symmetric $A$ (the Davis-Kahan $\sin\theta$ theorem). Measured on
$C(\epsilon)$-type perturbations of a matrix with eigenvalue gap $g$:

| gap $g$ | $\|E\|_2$ | $\sin\theta$ measured | $\|E\|_2/g$ |
|---|---|---|---|
| $10^{-1}$ | $10^{-6}$ | $1.0\times10^{-5}$ | $1.0\times10^{-5}$ |
| $10^{-3}$ | $10^{-6}$ | $1.0\times10^{-3}$ | $1.0\times10^{-3}$ |
| $10^{-5}$ | $10^{-6}$ | $9.9\times10^{-2}$ | $1.0\times10^{-1}$ |

The gap, not the condition number of the eigenvalue, governs the eigenvector.
These are independent: a Hermitian matrix has every eigenvalue conditioned at
exactly 1 (`eigenvalue-condition-number-is-one-over-the-inner-product`) and may
still have eigenvectors of arbitrarily bad conditioning, if its eigenvalues are
close.

## Remarks

* The same phenomenon is why principal component analysis is unstable when two
  singular values are close: the individual principal directions are not
  determined, while the subspace they span is.
* Degeneracy is not required, only closeness: the discontinuity at exact
  degeneracy is the limit of an ill-conditioning that is already severe at a
  small gap, as the table above shows.
