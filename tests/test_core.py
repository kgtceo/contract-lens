"""Core offline tests — the grounding pass drops fabricated quotes."""

from __future__ import annotations

from conftest import FakeClient

from contract_lens.models import Finding, Review, Severity
from contract_lens.reviewer import Reviewer


def _review(findings):
    return Review(summary="s", overall_risk="high", findings=findings)


def test_grounded_finding_kept():
    contract = "This agreement renews automatically for successive 12-month periods."
    r = _review([Finding(clause_type="auto-renewal", severity=Severity.high,
                         concern="auto-renews", recommendation="check", quote="renews automatically")])
    result = Reviewer(FakeClient(r)).review(contract)
    assert len(result.review.findings) == 1
    assert result.clause_types == ["auto-renewal"]


def test_fabricated_quote_dropped():
    contract = "Our total liability shall not exceed £50."
    r = _review([
        Finding(clause_type="liability cap", severity=Severity.high, concern="low cap",
                recommendation="x", quote="shall not exceed £50"),
        Finding(clause_type="non-compete", severity=Severity.high, concern="invented",
                recommendation="x", quote="you may not work for a competitor for five years"),
    ])
    result = Reviewer(FakeClient(r)).review(contract)
    quotes = [f.quote for f in result.review.findings]
    assert "shall not exceed £50" in quotes
    assert "you may not work for a competitor for five years" not in quotes
    assert len(result.review.findings) == 1


def test_no_findings_ok():
    result = Reviewer(FakeClient(_review([]))).review("A short fair agreement.")
    assert result.review.findings == []
    assert result.clause_types == []
