"""Offline test doubles — no API key, no network."""

from __future__ import annotations

import pytest

from contract_lens.config import Settings
from contract_lens.models import Review


class FakeClient:
    """Returns a scripted Review so the reviewer's grounding pass runs offline."""

    def __init__(self, review: Review) -> None:
        self._review = review
        self.calls = 0

    def structured(self, *, schema, system, user, model=None):
        self.calls += 1
        return self._review


@pytest.fixture
def settings() -> Settings:
    return Settings(anthropic_api_key="test-key")
