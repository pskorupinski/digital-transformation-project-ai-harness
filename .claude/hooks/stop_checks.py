"""Stop: before Claude declares a turn done, run the test suites of the areas it changed.

Red tests → exit 2 → Claude is sent back to fix them (once; stop_hook_active prevents loops).
Only uncommitted changes count, so doc-only turns cost nothing."""

import subprocess

from _runner import ROOT, block, read_event, run, running_services

event = read_event()
if event.get("stop_hook_active"):
    raise SystemExit(0)

changed = subprocess.run(
    ["git", "status", "--porcelain", "--", "backend", "frontend"],
    cwd=ROOT,
    capture_output=True,
    text=True,
).stdout.splitlines()
areas = {line[3:].split("/")[0] for line in changed if line[3:]}
services = running_services()
failures = []

if "backend" in areas:
    outcome = run("backend", ["pytest", "-q", "-x"], ["uv", "run"], services)
    if outcome and outcome[0] != 0:
        failures.append(("backend: pytest", outcome[1]))

if "frontend" in areas:
    for label, cmd in (("typecheck", ["npm", "run", "typecheck"]), ("test", ["npm", "test"])):
        outcome = run("frontend", cmd, [], services)
        if outcome and outcome[0] != 0:
            failures.append((f"frontend: {label}", outcome[1]))

if failures:
    report = "\n\n".join(f"## {name}\n" + "\n".join(out.splitlines()[-40:]) for name, out in failures)
    block("Checks are red — fix before finishing (or explain why it is expected):\n\n" + report)
