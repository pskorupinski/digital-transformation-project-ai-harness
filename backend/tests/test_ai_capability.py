"""Harness self-tests for the AI capability (D-05): fake adapter, real adapter request/response
handling (HTTP mocked — no network, no key), and per-capability mode selection."""

import json

import anthropic
import httpx2
import pytest
from pydantic import BaseModel

from app.config import Settings
from app.integrations.ai import (
    AnthropicStructuredGenerationAdapter,
    FakeStructuredGenerationAdapter,
    GenerationError,
    load_prompt,
)

PROMPT = load_prompt("harness_selftest", version=1)


class Label(BaseModel):
    label: str


def anthropic_client(reply_text: str, stop_reason: str = "end_turn", status: int = 200):
    requests = []

    def handler(request: httpx2.Request) -> httpx2.Response:
        requests.append(json.loads(request.content))
        if status != 200:
            return httpx2.Response(
                status, json={"type": "error", "error": {"type": "api_error", "message": "boom"}}
            )
        return httpx2.Response(
            200,
            json={
                "id": "msg_test",
                "type": "message",
                "role": "assistant",
                "model": "claude-sonnet-5-5",
                "content": [{"type": "text", "text": reply_text}],
                "stop_reason": stop_reason,
                "stop_sequence": None,
                "usage": {"input_tokens": 12, "output_tokens": 5},
            },
        )

    client = anthropic.Anthropic(
        api_key="test",
        http_client=httpx2.Client(transport=httpx2.MockTransport(handler)),
        max_retries=0,
    )
    return client, requests


def test_fake_returns_registered_output_and_records_input():
    fake = FakeStructuredGenerationAdapter()
    fake.register(Label, Label(label="spam"))
    generation = fake.generate(prompt=PROMPT, input="buy now", schema=Label)
    assert generation.output == Label(label="spam")
    assert generation.prompt_version == "harness_selftest.v1"
    assert fake.calls == [("harness_selftest.v1", "buy now")]


def test_fake_without_registration_or_with_error_raises():
    fake = FakeStructuredGenerationAdapter()
    with pytest.raises(GenerationError, match="No fake response"):
        fake.generate(prompt=PROMPT, input="x", schema=Label)
    fake.register(Label, GenerationError("model down"))
    with pytest.raises(GenerationError, match="model down"):
        fake.generate(prompt=PROMPT, input="x", schema=Label)


def test_real_adapter_sends_prompt_and_schema_and_returns_metadata():
    client, requests = anthropic_client('{"label": "ham"}')
    adapter = AnthropicStructuredGenerationAdapter(client, "claude-sonnet-5-5", 256)
    generation = adapter.generate(prompt=PROMPT, input="hello", schema=Label)
    assert generation.output == Label(label="ham")
    assert (generation.model, generation.input_tokens, generation.output_tokens) == (
        "claude-sonnet-5-5",
        12,
        5,
    )
    sent = requests[0]
    assert sent["system"] == PROMPT.text
    assert sent["messages"] == [{"role": "user", "content": "hello"}]
    assert sent["output_config"]["format"]["type"] == "json_schema"


@pytest.mark.parametrize(
    ("reply", "stop_reason", "status"),
    [
        ('{"label": "ham"}', "refusal", 200),
        ('{"label": "h', "max_tokens", 200),
        ('{"wrong": 1}', "end_turn", 200),
        ("", "end_turn", 500),
    ],
    ids=["refusal", "truncated", "invalid-schema", "api-error"],
)
def test_real_adapter_turns_unusable_output_into_generation_error(reply, stop_reason, status):
    client, _ = anthropic_client(reply, stop_reason, status)
    adapter = AnthropicStructuredGenerationAdapter(client, "claude-sonnet-5-5", 256)
    with pytest.raises(GenerationError):
        adapter.generate(prompt=PROMPT, input="hello", schema=Label)


def test_capability_mode_override_beats_default():
    assert Settings(integrations_mode="fake", ai_mode="real").mode_for("ai") == "real"
    assert Settings(integrations_mode="fake").mode_for("ai") == "fake"
    assert Settings(integrations_mode="real").mode_for("payment") == "real"
