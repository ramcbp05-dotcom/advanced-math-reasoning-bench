# Flawed solution: `normalise-to-fix-it`

## The submitted argument

> **Steps 1-2.** [The two families computed correctly; top eigenvectors found
> to be $e_1$ and $(1,1)/\sqrt2$.]
>
> **Step 3.** These look different, but eigenvectors are only defined up to
> scale, and numerical libraries return them with arbitrary sign. The apparent
> discontinuity is this normalisation ambiguity.
>
> **Step 4.** Fixing a convention — say, making the first nonzero component
> positive and the vector unit length — removes the ambiguity. With that
> convention both families give a well-defined eigenvector that converges, and
> there is no genuine discontinuity.

## Where it breaks

**Step 3**, which misidentifies the phenomenon.

The scale and sign ambiguity is real and is a nuisance in practice: $v$ and
$-v$ span the same line and a library may return either. But that ambiguity is
a choice between **two points on the same line**, and it is removed by any
convention, exactly as Step 4 says.

What is happening here is different. The two limits are

$$e_1 = (1, 0) \qquad\text{and}\qquad \tfrac{1}{\sqrt2}(1,1),$$

which span **different lines**, at $45°$. Applying the convention in Step 4
leaves them as $(1,0)$ and $(1,1)/\sqrt2$ — still $45°$ apart. No convention
based on signs or scaling can map one line to the other, because the ambiguity
being fixed is within a line and the discrepancy is between lines.

## The measurement that distinguishes them

Compare lines rather than vectors, using $|\langle u, v\rangle|$, which is
invariant under $u \to -u$ and $v \to -v$:

| $\epsilon$ | $|\langle v_B, v_C\rangle|$ | angle |
|---|---|---|
| $10^{-2}$ | $0.7071068$ | $45.000000°$ |
| $10^{-4}$ | $0.7071068$ | $45.000000°$ |
| $10^{-6}$ | $0.7071068$ | $45.000000°$ |
| $10^{-8}$ | $0.7071068$ | $45.000000°$ |

A sign ambiguity would show up as $|\langle u,v\rangle| = 1$ with the raw inner
product flipping between $\pm 1$. A value of $1/\sqrt2$ is a genuine $45°$
separation that no convention touches.

## What Step 4's convention does achieve

It makes each *family* return a continuous eigenvector in $\epsilon$ — and both
families already did, since $e_1$ and $(1,1)/\sqrt2$ are constant in $\epsilon$.
Continuity along a path is not the issue; the issue is that the limit depends
on the path. Perturbing $I$ by $\epsilon(2vv^{\mathsf T} - I)$ gives top
eigenvector $v$ for **any** unit $v$, so the set of limit points is the entire
unit circle.

## Failure mode

`wrong-diagnosis`: a real but unrelated ambiguity is identified as the cause, so
the proposed fix is sound and addresses nothing.
