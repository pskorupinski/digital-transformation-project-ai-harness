# Evals

Tests prove the code **around** the model behaves (fake adapter, deterministic). Evals measure
the **model's output quality** on golden cases (real adapter, scored). See D-05.

| Part | Where |
|---|---|
| Golden cases | `evals/cases/f_nn_<slug>.jsonl` — one JSON object per line: `id`, the input, the expectation |
| Checks + threshold | `evals/test_eval_f_nn_<slug>.py` — one check per case, `assert_pass_rate(results, 0.8)` |
| Run | `docker compose exec backend pytest evals -s` (needs `AI_MODE=real` + `ANTHROPIC_API_KEY`) |

Good checks are cheap and objective: output is in the allowed set, grounded in the provided
data, empty when the input gives no basis, no personal data echoed back. Start with 5–10 cases
covering the typical input, the ambiguous one and the "should decline" one.

```python
from evals.harness import CaseResult, assert_pass_rate, load_cases, run_cases
from app.integrations.ai import load_prompt


def test_eval_f_13_suggest_service(generation):
    prompt = load_prompt("f_13_suggest_service", version=1)

    def check(case):
        out = generation.generate(prompt=prompt, input=case["input"], schema=Suggestion).output
        return CaseResult(
            case["id"], out.service_code == case["expected"], f"got {out.service_code}"
        )

    assert_pass_rate(run_cases(load_cases("f_13_suggest_service"), check), threshold=0.8)
```
