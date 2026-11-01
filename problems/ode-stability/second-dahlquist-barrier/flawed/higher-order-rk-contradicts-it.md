# Flawed solution: `higher-order-rk-contradicts-it`

## The submitted argument

> **Steps 1-2.** [Order conditions and the trapezoidal rule, both correct.]
>
> **Step 3.** The barrier claims no A-stable method exceeds order 2. But the
> 2-stage Gauss-Legendre method is A-stable with order 4, and the 3-stage one
> is A-stable with order 6. `scipy.integrate.Radau` is A-stable of order 5 and
> is used in production.
>
> **Step 4.** These are counterexamples, so the barrier as stated is false; it
> must require some additional hypothesis that is usually left unsaid.

## Where it breaks

**Step 3-4.** The hypothesis is not left unsaid: it is the first three words of
the theorem. The barrier is about **linear multistep methods**, and every
example in Step 3 is an implicit **Runge-Kutta** method.

Gauss-Legendre collocation with $s$ stages is A-stable with order $2s$, Radau
IIA with $s$ stages is L-stable with order $2s-1$, and none of them is an LMM.
They are not counterexamples; they are outside the class the theorem quantifies
over.

## The structural reason the classes differ

An LMM's stability is governed by the **root condition**: *every* root
$\zeta_i(z)$ of $\rho(\zeta) - z\sigma(\zeta)$ must satisfy $|\zeta_i| \le 1$
for every $z$ in the left half-plane. A $k$-step method has $k$ roots, and the
requirement that all of them stay in the disc (while the order conditions force
$\rho/\sigma$ to approximate $\log\zeta$) is what couples order to stability
and produces the bound 2.

An implicit Runge-Kutta method has a single rational stability function $R(z)$
with no multi-root condition. The Padé table of $e^{z}$ supplies A-stable
rational approximations at every order, and the Ehle conjecture (proved by
Wanner, Hairer and Nørsett) says exactly which Padé entries are A-stable. There
is no barrier at order 2 because there is no root condition to impose.

## The claim that *is* true across both classes

There is a genuine general result in this neighbourhood, and conflating it with
the barrier is the usual confusion: **no explicit method** (Runge-Kutta or
multistep) can be A-stable, because its stability function is a polynomial in
$z$, hence unbounded, hence its stability region is bounded. That one holds for
both classes and is proved in `explicit-euler-stability-region`.

## The check

Before invoking a theorem, read what it quantifies over. "Linear multistep" is
in the statement; Gauss-Legendre is a collocation method. The two classes
intersect only in trivial cases, and nearly every published result in stiff
integration is stated for one or the other.

## Failure mode

`theorem-applied-outside-its-class`: a result about one family of methods is
tested against members of a different family, and the mismatch is read as a
defect in the theorem.
