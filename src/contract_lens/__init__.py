"""contract-lens — an AI contract / terms-of-service reviewer.

Paste a contract or ToS; it flags the clauses worth attention (auto-renewal, liability, IP
assignment, data rights, unilateral changes…) with severity and a verbatim quote, grounded in the
document. Ships a planted-clause eval harness. Educational only — not legal advice."""

from .client import LLMClient
from .config import Settings
from .models import Finding, Review, ReviewResult, Severity
from .reviewer import Reviewer

__all__ = ["LLMClient", "Settings", "Finding", "Review", "ReviewResult", "Severity", "Reviewer"]
