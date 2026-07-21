"""Typed contracts for contract-lens.

The reviewer reads a contract / terms-of-service and returns risk-ranked clause findings, each
grounded in a verbatim quote from the document so it can't invent a clause. Educational only —
this is not legal advice.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class Severity(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


class Finding(BaseModel):
    clause_type: str = Field(
        description="Short label, e.g. 'auto-renewal', 'liability cap', 'IP assignment', "
        "'data/privacy', 'termination', 'unilateral changes', 'arbitration/class-action waiver'.",
    )
    severity: Severity
    concern: str = Field(description="Why this clause is worth attention, in plain English.")
    recommendation: str = Field(description="What to check, negotiate, or push back on.")
    quote: str = Field(description="A short verbatim span from the document that this relates to.")


class Review(BaseModel):
    """A contract review. A fair, balanced contract should get few findings."""

    summary: str = Field(description="2–3 sentences: what this document is and its main risk areas.")
    overall_risk: str = Field(description="'low' | 'medium' | 'high' — how one-sided/risky it reads.")
    findings: list[Finding] = Field(default_factory=list)


class ReviewResult(BaseModel):
    review: Review
    clause_types: list[str] = Field(default_factory=list)
    disclaimer: str = (
        "Educational tool, not legal advice. It highlights clauses to look at; it does not "
        "interpret them for your situation. Consult a qualified lawyer for anything that matters."
    )
