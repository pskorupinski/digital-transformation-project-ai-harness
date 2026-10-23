"""Capability: structured generation with an LLM (D-05).

Services depend on StructuredGenerationPort, never on a vendor SDK. The model returns a
validated Pydantic object or raises GenerationError — invalid output never reaches a service.

    generation = get_generation().generate(
        prompt=load_prompt("f_13_suggest_service", version=1),
        input=prepared_input,          # minimised: only what the prompt needs (no PII)
        schema=ServiceSuggestion,      # Pydantic model the output must satisfy
    )
    generation.output                  # ServiceSuggestion
    generation.model, generation.prompt_version, generation.input_tokens, ...   # for the audit

Modes (settings.mode_for("ai")):
- fake: FakeStructuredGenerationAdapter — deterministic, free; tests and offline runs
- real: AnthropicStructuredGenerationAdapter — Claude API structured outputs (messages.parse)
"""

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Protocol

import anthropic
from pydantic import BaseModel

from app.config import settings

PROMPTS = Path(__file__).resolve().parent.parent / "prompts"


class GenerationError(Exception):
    """Model unavailable, refused, truncated or returned invalid output.

    Callers must handle it explicitly — typically a fallback the human can complete."""


@dataclass(frozen=True)
class Prompt:
    name: str
    version: int
    text: str

    @property
    def id(self) -> str:
        return f"{self.name}.v{self.version}"


def load_prompt(name: str, version: int) -> Prompt:
    """Prompts are versioned files: app/prompts/<name>.v<version>.md. Never edit a released
    version in place — add v<n+1>, so every stored generation stays explainable."""
    path = PROMPTS / f"{name}.v{version}.md"
    return Prompt(name=name, version=version, text=path.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class Generation[T: BaseModel]:
    output: T
    model: str
    prompt_version: str
    input_tokens: int
    output_tokens: int


class StructuredGenerationPort(Protocol):
    def generate[T: BaseModel](
        self, *, prompt: Prompt, input: str, schema: type[T]
    ) -> Generation[T]: ...


class FakeStructuredGenerationAdapter:
    """Returns the canned output registered for a schema (or raises a registered error)."""

    def __init__(self) -> None:
        self._responses: dict[type[BaseModel], BaseModel | Exception] = {}
        self.calls: list[tuple[str, str]] = []  # (prompt id, input) — lets tests assert inputs

    def register[T: BaseModel](self, schema: type[T], response: T | Exception) -> None:
        self._responses[schema] = response

    def generate[T: BaseModel](
        self, *, prompt: Prompt, input: str, schema: type[T]
    ) -> Generation[T]:
        self.calls.append((prompt.id, input))
        response = self._responses.get(schema)
        if response is None:
            raise GenerationError(f"No fake response registered for {schema.__name__}")
        if isinstance(response, Exception):
            raise response
        return Generation(
            output=schema.model_validate(response.model_dump()),
            model="fake",
            prompt_version=prompt.id,
            input_tokens=0,
            output_tokens=0,
        )


class AnthropicStructuredGenerationAdapter:
    def __init__(self, client: anthropic.Anthropic, model: str, max_tokens: int) -> None:
        self._client = client
        self._model = model
        self._max_tokens = max_tokens

    def generate[T: BaseModel](
        self, *, prompt: Prompt, input: str, schema: type[T]
    ) -> Generation[T]:
        try:
            response = self._client.messages.parse(
                model=self._model,
                max_tokens=self._max_tokens,
                system=prompt.text,
                messages=[{"role": "user", "content": input}],
                output_format=schema,
            )
        except anthropic.APIError as error:
            raise GenerationError(f"Model call failed: {error}") from error
        except ValueError as error:  # the SDK raises on output that fails schema validation
            raise GenerationError(f"Model output failed validation: {error}") from error
        if response.stop_reason in ("refusal", "max_tokens") or response.parsed_output is None:
            raise GenerationError(f"No usable output (stop_reason={response.stop_reason})")
        return Generation(
            output=response.parsed_output,
            model=response.model,
            prompt_version=prompt.id,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )


@lru_cache
def _fake() -> FakeStructuredGenerationAdapter:
    return FakeStructuredGenerationAdapter()


def get_generation() -> StructuredGenerationPort:
    """FastAPI dependency / factory. Tests override it with their own fake."""
    if settings.mode_for("ai") == "fake":
        return _fake()
    if settings.anthropic_api_key is None:
        raise GenerationError("AI_MODE=real needs ANTHROPIC_API_KEY in .env")
    client = anthropic.Anthropic(api_key=settings.anthropic_api_key.get_secret_value())
    return AnthropicStructuredGenerationAdapter(client, settings.ai_model, settings.ai_max_tokens)
