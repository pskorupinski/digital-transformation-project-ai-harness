"""Minimal eval harness (D-05): golden cases + checks, scored against a pass-rate threshold.

Unlike tests, evals call the REAL model, so they are not binary: a few misses are expected and
the threshold is the quality bar agreed for the feature."""

import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

CASES = Path(__file__).resolve().parent / "cases"


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    passed: bool
    detail: str = ""


def load_cases(name: str) -> list[dict]:
    """evals/cases/<name>.jsonl — one JSON object per line with at least an "id"."""
    lines = (CASES / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def run_cases(cases: list[dict], check: Callable[[dict], CaseResult]) -> list[CaseResult]:
    results = []
    for case in cases:
        try:
            results.append(check(case))
        except Exception as error:  # a crash is a failed case, not an aborted eval
            results.append(CaseResult(case["id"], False, f"{type(error).__name__}: {error}"))
    return results


def assert_pass_rate(results: list[CaseResult], threshold: float) -> None:
    passed = sum(result.passed for result in results)
    rate = passed / len(results) if results else 0.0
    print(f"\n{'case':<24}{'result':<8}detail")
    for result in results:
        print(f"{result.case_id:<24}{'pass' if result.passed else 'FAIL':<8}{result.detail}")
    print(f"pass rate {passed}/{len(results)} = {rate:.0%} (threshold {threshold:.0%})")
    assert rate >= threshold, f"Pass rate {rate:.0%} below threshold {threshold:.0%}"
