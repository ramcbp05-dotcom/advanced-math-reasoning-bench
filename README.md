# Advanced Mathematics Reasoning and Verification Benchmark

Fifteen carefully verified problems in three focused areas (**matrix
conditioning**, **eigenvalue sensitivity** and **differential-equation
stability**) each with explicit assumptions, a full proof, counterexamples
where they sharpen the result, and a SymPy/NumPy verification script that is
kept deliberately separate from the proof.

Every problem also ships **two flawed solutions**, each naming the exact step
where the reasoning breaks and classifying the failure.

```
15 problems · 30 recorded flawed solutions · 131 verification checks
5 conditioning / 5 eigenvalue-sensitivity / 5 ode-stability
```

## Quick start

```bash
pip install -r requirements.txt
```

```bash
python -m bench.cli list
```

```bash
python -m bench.cli verify
```

Read a problem the way a solver would see it: the statement only:

```bash
python -m bench.cli show jordan-block-perturbation-is-epsilon-to-the-one-over-n
```

Add `--solution` for the proof and `--flawed` for the recorded wrong turns.

## The central discipline: verification is not proof

`solution.md` carries the **argument**. `verify.py` carries **evidence at
instances**. The harness keeps them apart and tags every check with a role:

| role | what it establishes |
|---|---|
| `illustration` | sampled evidence; the proof is in `solution.md` |
| `witness` | an **exact** counterexample: this *does* settle an existential claim |
| `sympy-identity` | a symbolic identity, for the symbols quantified |
| `consistency` | arithmetic internal to the repository |

The asymmetry is the point. A universal claim ("for every matrix A…") cannot be
established by finitely many instances; a sampled check can only fail to
contradict it. An existential claim ("there is an A for which…") *is* settled
by one exact witness. Every `verify.py` prints that disclaimer before its
results, and `tests/test_problem_integrity.py` requires every non-universal
problem to carry a `witness`-tagged check.

Full treatment, including three traps this repository actually fell into, in
[docs/verification-vs-proof.md](docs/verification-vs-proof.md).

## The problems

### Matrix conditioning

| problem | claim | what it settles |
|---|---|---|
| [`cond2-is-singular-value-ratio`](problems/conditioning/cond2-is-singular-value-ratio) | mixed | κ₂ = σ₁/σₙ, and two exact witnesses killing the determinant folklore in both directions |
| [`normal-equations-square-the-condition`](problems/conditioning/normal-equations-square-the-condition) | universal | κ(AᵀA) = κ(A)² exactly: and why a small residual is not an accurate solution |
| [`row-scaling-changes-the-condition-number`](problems/conditioning/row-scaling-changes-the-condition-number) | mixed | κ is a property of the matrix as written, not of the map; the Skeel number is what survives |
| [`hilbert-matrix-exponential-growth`](problems/conditioning/hilbert-matrix-exponential-growth) | universal | exact Cauchy determinants, and a growth constant measured honestly at 60 digits |
| [`eigenvalues-do-not-determine-the-condition-number`](problems/conditioning/eigenvalues-do-not-determine-the-condition-number) | mixed | both eigenvalues exactly 1, κ₂ ≈ t² |

### Eigenvalue sensitivity

| problem | claim | what it settles |
|---|---|---|
| [`hermitian-eigenvalues-are-perfectly-conditioned`](problems/eigenvalue-sensitivity/hermitian-eigenvalues-are-perfectly-conditioned) | universal | Weyl via Courant: Fischer, attained: and absolute, not relative |
| [`jordan-block-perturbation-is-epsilon-to-the-one-over-n`](problems/eigenvalue-sensitivity/jordan-block-perturbation-is-epsilon-to-the-one-over-n) | universal | char. poly λⁿ − ε exactly; at n = 16 a 10⁻¹⁶ perturbation moves eigenvalues to 0.1 |
| [`bauer-fike-and-when-it-says-nothing`](problems/eigenvalue-sensitivity/bauer-fike-and-when-it-says-nothing) | mixed | sharp to a factor of 2 for one E, vacuous by 10⁸ for another, and **no content at all** for a defective matrix |
| [`eigenvalue-condition-number-is-one-over-the-inner-product`](problems/eigenvalue-sensitivity/eigenvalue-condition-number-is-one-over-the-inner-product) | universal | one matrix with κ(λ) = 1 and κ(λ) = 10⁸ side by side |
| [`eigenvectors-are-discontinuous-at-a-degenerate-eigenvalue`](problems/eigenvalue-sensitivity/eigenvectors-are-discontinuous-at-a-degenerate-eigenvalue) | existential | two perturbations of identical norm, identical spectra, eigenvectors 45° apart for every ε |

### ODE stability

| problem | claim | what it settles |
|---|---|---|
| [`linearization-is-inconclusive-at-the-critical-case`](problems/ode-stability/linearization-is-inconclusive-at-the-critical-case) | mixed | x′ = ±x³: same linearisation, one asymptotically stable, one blowing up at t* = 1/(2x₀²) |
| [`explicit-euler-stability-region`](problems/ode-stability/explicit-euler-stability-region) | universal | the disc \|1+z\| ≤ 1, and why local error has no threshold while the amplification factor does |
| [`trapezoidal-is-a-stable-but-not-l-stable`](problems/ode-stability/trapezoidal-is-a-stable-but-not-l-stable) | mixed | R(z) → −1, so a stiff transient oscillates at amplitude 1 forever while A-stability is never violated |
| [`frozen-coefficients-can-lie`](problems/ode-stability/frozen-coefficients-can-lie) | existential | eigenvalues of A(t) constant at Re = −1/4 for every t, exact solution growing like e^(t/2) |
| [`second-dahlquist-barrier`](problems/ode-stability/second-dahlquist-barrier) | universal | the barrier is cited, not proved: and a search is shown to be a refutation procedure, not a proof procedure |

## Where reasoning breaks

The 26 flawed solutions are not straw men. Several reach the **right numerical
answer** by an argument that does not support it: the case a reviewer waves
through. Recurring failure modes:

* `missing-hypothesis`: a theorem about normal matrices applied to general ones
* `inequality-reported-as-equality`: the half of the claim with the content
  dropped
* `bound-reported-as-estimate`: `≤` read as `≈`, over-estimating by 10⁸
* `continuity-is-not-conditioning`: a qualitative property used where a modulus
  is needed
* `finite-horizon-mistaken-for-asymptotics`: integrating to t = 5 on a problem
  that blows up at t = 50
* `measurement-beyond-precision`: a quantity measured in arithmetic that cannot
  represent it
* `expansion-invalid-at-a-defective-eigenvalue`: first-order theory applied
  where it divides by exactly zero

## Honest notes on the measurements

**The Hilbert growth constant.** The first draft reported 0.15 % agreement with
`4 ln(1+√2)`. Those eigenvalues had silently saturated at `n = 12, 13`. The
correct figure from 60-digit arithmetic is **1.77 %** for a plain linear fit:
and **0.22 %** once the `√n` term in the asymptotic law is accounted for, with
the successive ratios climbing monotonically (3.4250 → 3.4966) towards the
limit. The worse-looking number is the real one, and the *structure* of the
discrepancy is what turns it into evidence.

**`simplify(e) == 0` is not a zero test**, and two SymPy expressions that print
identically need not be equal (`charpoly` returns a `Dummy`). Both bit this
repository; `bench.verify_support.symbolically_zero()` exists because of it.

## Layout

```
bench/
  models.py          problem.yaml schema
  verify_support.py  Check roles, the disclaimer, symbolically_zero()
  runner.py          runs every verify.py and collects outcomes
  cli.py             list / show / verify
problems/<area>/<id>/   statement, solution, flawed/, verify.py
tests/                  integrity checks on the collection itself
docs/                   problem format, verification vs proof
```

```bash
python -m pytest tests/ -q       # 94 integrity checks
python -m bench.cli verify       # 15/15 problems, 131/131 checks
```

## Status

All fifteen problems are complete and verifying, five in each area. The
collection is designed to grow to twenty.

The `second-dahlquist-barrier` problem is deliberately the one where the proof
is **cited rather than given**: the barrier quantifies over all step numbers
and an uncountable coefficient space, so no computation in this repository
establishes it. What the verification script does establish is the other half:
an exact witness showing BDF3 is not A-stable, found near the imaginary axis
where a scan of the negative real axis misses it entirely. That contrast is the
repository's thesis in one file.

## License

MIT: see [LICENSE](LICENSE).
