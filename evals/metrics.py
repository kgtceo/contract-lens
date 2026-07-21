"""Deterministic eval metrics for contract-lens."""

from __future__ import annotations

from contract_lens.models import ReviewResult

_MATERIAL = {"high", "medium"}


def material_count(result: ReviewResult) -> int:
    return sum(1 for f in result.review.findings if f.severity.value in _MATERIAL)


def high_count(result: ReviewResult) -> int:
    return sum(1 for f in result.review.findings if f.severity.value == "high")


def findings_are_grounded(result: ReviewResult, contract: str) -> bool:
    """Every quote actually appears in the contract (no fabricated clauses)."""
    hay = " ".join(contract.lower().split())
    for f in result.review.findings:
        if " ".join(f.quote.lower().split()) not in hay:
            return False
    return True


def catches_enough(result: ReviewResult, planted: list[str], threshold: float = 0.6) -> bool:
    """On a loaded contract, it should surface a solid share of the planted issues (recall proxy:
    at least `threshold` × count material findings)."""
    return material_count(result) >= max(1, int(len(planted) * threshold))
