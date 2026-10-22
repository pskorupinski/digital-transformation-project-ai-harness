"""PostToolUse (Edit|Write): lint + format the edited file. Fast by design (ruff/oxlint).

Exit 2 feeds unfixable lint errors back to Claude; anything else passes silently."""

from pathlib import Path

from _runner import ROOT, block, read_event, run, running_services

event = read_event()
file_path = (event.get("tool_input") or {}).get("file_path")
if not file_path:
    raise SystemExit(0)

path = Path(file_path)
try:
    rel = path.resolve().relative_to(ROOT.resolve())
except ValueError:
    raise SystemExit(0) from None

parts = rel.parts
if len(parts) < 2 or parts[0] not in ("backend", "frontend"):
    raise SystemExit(0)
inner = str(Path(*parts[1:]))
services = running_services()

if parts[0] == "backend" and rel.suffix == ".py":
    run("backend", ["ruff", "format", inner], ["uv", "run"], services)
    outcome = run("backend", ["ruff", "check", "--fix", inner], ["uv", "run"], services)
    if outcome and outcome[0] != 0:
        block(f"ruff found issues in {rel} that need a manual fix:\n{outcome[1]}")

elif parts[0] == "frontend" and rel.suffix in (".ts", ".tsx"):
    outcome = run("frontend", ["npx", "oxlint", inner], [], services)
    if outcome and outcome[0] != 0:
        block(f"oxlint found issues in {rel}:\n{outcome[1]}")
