"""Integrity checks on the problem collection itself."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from bench import models

REPO_ROOT = Path(__file__).resolve().parent.parent
SPECS = models.discover(REPO_ROOT / "problems")
IDS = [s.problem_id for s in SPECS]


def test_collection_size():
    assert len(SPECS) >= 13, f"expected at least 13 problems, found {len(SPECS)}"


def test_every_area_is_populated():
    counts = {area: sum(s.area == area for s in SPECS) for area in models.AREAS}
    for area, count in counts.items():
        assert count >= 3, f"only {count} problems in {area}; distribution {counts}"


def test_ids_are_unique_and_kebab_case():
    assert len(set(IDS)) == len(IDS), "duplicate problem ids"
    for pid in IDS:
        assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", pid), f"{pid!r} is not kebab-case"


@pytest.mark.parametrize("spec", SPECS, ids=IDS)
def test_statement_structure(spec):
    text = spec.statement_path.read_text()
    assert text.startswith("# "), f"{spec.problem_id}: statement needs an H1"
    assert "## Assumptions" in text, f"{spec.problem_id}: no Assumptions section"
    assert "What a complete answer contains" in text, (
        f"{spec.problem_id}: no checklist of what a complete answer contains"
    )
    assert len(text.split()) >= 150, f"{spec.problem_id}: statement is too thin"


@pytest.mark.parametrize("spec", SPECS, ids=IDS)
def test_solution_contains_an_argument(spec):
    text = spec.solution_path.read_text()
    assert len(text.split()) >= 400, f"{spec.problem_id}: solution is too thin"
    assert "$$" in text, f"{spec.problem_id}: solution has no display mathematics"
    assert "blacksquare" in text or "QED" in text or "$\\blacksquare$" in text, (
        f"{spec.problem_id}: no proof is closed off; a solution must contain an "
        "argument, not only a computation"
    )


@pytest.mark.parametrize("spec", SPECS, ids=IDS)
def test_flawed_solutions_name_the_broken_step(spec):
    assert len(spec.flawed) >= 1, f"{spec.problem_id}: no flawed solution recorded"
    for flaw in spec.flawed:
        assert flaw.breaks_at.strip(), (
            f"{spec.problem_id}/{flaw.name}: problem.yaml does not say where it breaks"
        )
        text = spec.flawed_path(flaw.name).read_text()
        assert "## Where it breaks" in text, (
            f"{spec.problem_id}/{flaw.name}: no 'Where it breaks' section"
        )
        assert "## Failure mode" in text, (
            f"{spec.problem_id}/{flaw.name}: no classified failure mode"
        )
        assert "Step" in text or "step" in text, (
            f"{spec.problem_id}/{flaw.name}: the broken step is not identified"
        )


@pytest.mark.parametrize("spec", SPECS, ids=IDS)
def test_verify_script_declares_roles_and_disclaimer(spec):
    source = spec.verify_path.read_text()
    assert "from bench.verify_support import" in source, (
        f"{spec.problem_id}: verify.py does not use the shared helpers"
    )
    assert "CHECKS = [" in source, f"{spec.problem_id}: verify.py exposes no CHECKS"
    assert "report(PROBLEM" in source, f"{spec.problem_id}: verify.py does not report"
    n_checks = source.count('", "illustration"') + source.count('", "witness"') \
        + source.count('", "sympy-identity"') + source.count('", "consistency"') \
        + source.count('"illustration",') + source.count('"witness",') \
        + source.count('"sympy-identity",') + source.count('"consistency",')
    assert n_checks >= 5, (
        f"{spec.problem_id}: only {n_checks} role-tagged checks; a problem needs "
        "enough evidence that a partial answer fails some of it"
    )


@pytest.mark.parametrize("spec", SPECS, ids=IDS)
def test_existential_claims_have_a_witness(spec):
    if spec.claim_type == "universal":
        return
    source = spec.verify_path.read_text()
    assert '"witness"' in source, (
        f"{spec.problem_id}: claim_type is {spec.claim_type!r} but no check is "
        "tagged as a witness. An existential claim is settled by an exact "
        "counterexample, and that is the one kind of check that constitutes proof."
    )


@pytest.mark.parametrize("spec", SPECS, ids=IDS)
def test_statement_does_not_contain_the_proof(spec):
    text = spec.statement_path.read_text()
    assert "blacksquare" not in text, (
        f"{spec.problem_id}: the statement closes a proof; that belongs in solution.md"
    )


def test_metadata_round_trips():
    for spec in SPECS:
        data = yaml.safe_load((spec.root / "problem.yaml").read_text())
        assert data["id"] == spec.problem_id
        assert data["area"] == spec.area
        assert data["claim_type"] in models.CLAIM_TYPES
