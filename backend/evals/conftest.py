"""Evals run only against the real model: `pytest evals -s` with AI_MODE=real and a key.
They are outside `testpaths`, so the normal suite and the hooks never call the model."""

import pytest

from app.config import settings
from app.integrations.ai import StructuredGenerationPort, get_generation


@pytest.fixture(scope="session")
def generation() -> StructuredGenerationPort:
    if settings.mode_for("ai") != "real" or settings.anthropic_api_key is None:
        pytest.skip("Evals need AI_MODE=real and ANTHROPIC_API_KEY (see .env.example)")
    return get_generation()
