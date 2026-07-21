"""LLM-as-judge (opus): are the flagged clauses real concerns, fairly explained, well-calibrated?"""

from __future__ import annotations

from pydantic import BaseModel, Field

from contract_lens.client import LLMClient
from contract_lens.config import Settings
from contract_lens.models import ReviewResult


class ReviewGrade(BaseModel):
    correctness: int = Field(ge=1, le=5, description="Are the flagged clauses genuinely worth attention?")
    usefulness: int = Field(ge=1, le=5, description="Are the explanations/recommendations helpful and plain?")
    calibration: int = Field(ge=1, le=5, description="Is severity sensible (no crying wolf, no legal advice)?")
    overall: int = Field(ge=1, le=5)
    comment: str = ""


JUDGE_SYSTEM = (
    "You grade an AI contract review. Given the CONTRACT and the REVIEW, score correctness (are the "
    "flagged clauses real concerns?), usefulness (clear, plain, actionable — and NOT overstepping into "
    "legal advice), and calibration (severity is sensible). Integer scores 1-5."
)


def grade(result: ReviewResult, contract: str, settings: Settings, client: LLMClient | None = None) -> ReviewGrade:
    client = client or LLMClient(settings)
    findings = "\n".join(f"- [{f.severity.value}] {f.clause_type}: {f.concern}" for f in result.review.findings) or "(none)"
    user = f"CONTRACT:\n{contract}\n\nREVIEW ({result.review.overall_risk} risk):\n{result.review.summary}\n{findings}"
    return client.structured(schema=ReviewGrade, system=JUDGE_SYSTEM, user=user, model=settings.judge_model)
