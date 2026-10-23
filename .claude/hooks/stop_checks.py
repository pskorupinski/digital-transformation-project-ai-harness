"""Stop: before Claude declares a turn done, run the checks for what it changed.

Red checks → exit 2 → Claude is sent back to fix them (once; stop_hook_active prevents loops).
Only uncommitted changes count.

| Changed                                   | Runs                                        |
|-------------------------------------------|---------------------------------------------|
| backend/                                  | full backend suite (includes traceability)  |
| frontend/                                 | typecheck + frontend tests                  |
| docs/02-features.md or docs/04-specs/     | traceability test only (no database needed) |
| any other doc (brief, architecture, ...)  | nothing                                     |
"""

import subprocess

from _runner import ROOT, block, read_event, run, running_services

TRACEABILITY_DOCS = ("docs/02-features.md", "docs/04-specs/")

event = read_event()
if event.get("stop_hook_active"):
    raise SystemExit(0)

changed = [
    line[3:].split(" -> ")[-1]
    for line in subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all", "--", "backend", "frontend", "docs"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    if line[3:]
]
backend = any(path.startswith("backend/") for path in changed)
frontend = any(path.startswith("frontend/") for path in changed)
traceability = any(path.startswith(TRACEABILITY_DOCS) for path in changed)

if not (backend or frontend or traceability):
    raise SystemExit(0)

services = running_services()
failures = []

if backend:
    outcome = run("backend", ["pytest", "-q", "-x"], ["uv", "run"], services)
    if outcome and outcome[0] != 0:
        failures.append(("backend: pytest", outcome[1]))
elif traceability:
    outcome = run("backend", ["pytest", "-q", "tests/test_traceability.py"], ["uv", "run"], services)
    if outcome and outcome[0] != 0:
        failures.append(("traceability (D-04)", outcome[1]))

if frontend:
    for label, cmd in (("typecheck", ["npm", "run", "typecheck"]), ("test", ["npm", "test"])):
        outcome = run("frontend", cmd, [], services)
        if outcome and outcome[0] != 0:
            failures.append((f"frontend: {label}", outcome[1]))

if failures:
    report = "\n\n".join(f"## {name}\n" + "\n".join(out.splitlines()[-40:]) for name, out in failures)
    block("Checks are red — fix before finishing (or explain why it is expected):\n\n" + report)
