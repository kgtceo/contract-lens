"""FastAPI wrapper: submit a contract / ToS → risk-ranked, grounded findings."""

from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .config import Settings
from .models import ReviewResult
from .reviewer import Reviewer

app = FastAPI(title="contract-lens", version="1.0.0")

_env_origins = [o.strip() for o in os.getenv("CL_CORS_ORIGINS", "").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_env_origins,
    allow_origin_regex=r"https://contract-lens[a-z0-9-]*\.vercel\.app|http://(localhost|127\.0\.0\.1):\d+",
    allow_methods=["*"],
    allow_headers=["*"],
)

_EXAMPLE = (
    "SUBSCRIPTION TERMS. 1. Term. This agreement renews automatically for successive 12-month "
    "periods unless you give written notice at least 90 days before the end of the current term. "
    "2. Fees. We may increase fees at any time at our sole discretion, effective immediately. "
    "3. Liability. Our total liability shall not exceed £50 in aggregate. You agree to indemnify us "
    "against all claims. 4. IP. Any feedback or content you provide becomes our exclusive property. "
    "5. Data. We may use, share and sell your usage data to third parties. 6. Changes. We may modify "
    "these terms at any time; continued use constitutes acceptance. 7. Disputes. You waive any right "
    "to a jury trial or to participate in a class action."
)


class ReviewRequest(BaseModel):
    contract: str = Field(..., min_length=40, max_length=40000)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/example")
def example() -> dict:
    return {"contract": _EXAMPLE}


@app.post("/api/review")
def review(req: ReviewRequest) -> ReviewResult:
    try:
        settings = Settings.from_env()
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    from .client import LLMClient

    return Reviewer(LLMClient(settings)).review(req.contract)
