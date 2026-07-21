"""contract text -> structured, grounded review.

A grounding pass drops any finding whose `quote` doesn't actually appear in the document, so the
reviewer can't invent a clause that isn't there.
"""

from __future__ import annotations

from . import prompts
from .client import LLMClient
from .models import Review, ReviewResult


def _norm(s: str) -> str:
    return " ".join(s.lower().split())


class Reviewer:
    def __init__(self, client: LLMClient) -> None:
        self._client = client

    def review(self, contract: str) -> ReviewResult:
        review = self._client.structured(
            schema=Review,
            system=prompts.REVIEW_SYSTEM,
            user=prompts.review_user(contract),
        )
        review = self._ground(review, contract)
        types = sorted({f.clause_type for f in review.findings})
        return ReviewResult(review=review, clause_types=types)

    @staticmethod
    def _ground(review: Review, contract: str) -> Review:
        hay = _norm(contract)
        kept = [f for f in review.findings if f.quote.strip() and _norm(f.quote) in hay]
        return review.model_copy(update={"findings": kept})
