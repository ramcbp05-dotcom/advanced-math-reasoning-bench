# Problem format

```
problems/<area>/<problem-id>/
├── problem.yaml        metadata -> bench.models.ProblemSpec
├── statement.md        assumptions and the claim, in LaTeX
├── solution.md         the proof, with counterexamples where they sharpen it
├── flawed/*.md         plausible wrong solutions, each naming the broken step
└── verify.py           numerical / symbolic evidence -- NOT the proof
```

## `problem.yaml`

```yaml
id: cond2-is-singular-value-ratio      # must equal the directory name
area: conditioning                     # must equal the parent directory
title: ...
difficulty: undergraduate | graduate | research-adjacent
claim_type: universal | existential | mixed
proof_method: analytic | sympy-assisted | analytic-with-witness
summary: >
  One paragraph naming what is proved and what is witnessed.
tags: [svd, condition-number]
flawed:
  - name: determinant-as-proxy
    summary: One line on what the flawed answer does.
    breaks_at: >
      The exact step, and why it fails there.
    failure_mode: invalid-identity
```

At least one flawed solution is required; the loader refuses a problem without
one, because a problem with no recorded wrong turn does not say where reasoning
actually breaks.

## `statement.md`

Opens with an H1, states the assumptions explicitly (including which are load
bearing), separates the parts, and ends with a **What a complete answer
contains** checklist. A universal part and an existential part are labelled as
such.

## `solution.md`

The proof, with each step's hypothesis visible. Where a counterexample sharpens
the result it is given exactly — a matrix and its singular values in closed
form, not floating-point output. Measured tables are included with the numbers
that were actually produced.

## `verify.py`

Imports `bench.verify_support` and exposes `CHECKS`, a list of zero-argument
functions returning `Check`. Each check carries a `role`
(`illustration`, `witness`, `sympy-identity`, `consistency`) and a `detail`
string with the measured numbers. See
[verification-vs-proof.md](verification-vs-proof.md) for why the roles exist
and for the three traps that motivated `symbolically_zero()`.

Standard bootstrap, so the script runs directly as well as through the harness:

```python
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
```

## Running

```bash
python -m bench.cli list
python -m bench.cli show <problem-id> --solution --flawed
python -m bench.cli verify
python -m bench.cli verify -a conditioning --report results/verification.json
```
