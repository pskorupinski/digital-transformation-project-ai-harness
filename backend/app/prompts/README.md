# Prompts

One file per prompt version: `<name>.v<n>.md`, loaded with `load_prompt(name, version=n)`.

| Rule | Why |
|---|---|
| Never edit a released version — add `v<n+1>` | Every stored generation records its prompt version, so it stays explainable |
| Name after the feature: `f_13_suggest_service` | Traceable to `F-13` |
| Instructions and grounding only; the input arrives as the user message | Keeps prompts reviewable and inputs minimised |
| Say what to do when unsure (e.g. "return `null` for `service_code`") | Gives the model a safe exit instead of a guess |
