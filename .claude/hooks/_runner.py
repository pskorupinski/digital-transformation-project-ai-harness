"""Shared helpers for hooks: run a command in a running docker-compose service,
falling back to the local toolchain, or skip silently if neither is available."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path(__file__).resolve().parents[2]))


def read_event() -> dict:
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError:
        return {}


def running_services() -> set[str]:
    if not shutil.which("docker"):
        return set()
    result = subprocess.run(
        ["docker", "compose", "ps", "--services", "--filter", "status=running"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return set(result.stdout.split()) if result.returncode == 0 else set()


def run(service: str, cmd: list[str], local_prefix: list[str] | None, services: set[str]):
    """Return (returncode, output) or None if no way to run the command."""
    if service in services:
        full = ["docker", "compose", "exec", "-T", service, *cmd]
        cwd = ROOT
    elif local_prefix is not None and shutil.which([*local_prefix, *cmd][0]):
        full = [*local_prefix, *cmd]
        cwd = ROOT / service  # service name == top-level folder
    else:
        return None
    result = subprocess.run(full, cwd=cwd, capture_output=True, text=True)
    return result.returncode, (result.stdout + result.stderr).strip()


def block(message: str) -> None:
    """Exit 2: Claude sees stderr and must react."""
    print(message, file=sys.stderr)
    sys.exit(2)
