"""Traceability check (D-04): every scenario of a `built` feature has its test.

Specs are Gherkin files that are not executed; this test keeps them and the hand-written tests
from drifting apart. It checks that a test exists, not what it asserts — review does that.

    @api scenario F-01/S-02 → `def test_s02_…` in backend/tests/test_f_01_*.py
    @ui  scenario F-01/S-06 → a test titled 'F-01/S-06 …' in frontend/src/**/*.test.ts(x)
"""

import os
import re
from pathlib import Path

REPO = Path(os.environ.get("REPO_ROOT", Path(__file__).resolve().parents[2]))
FEATURES = REPO / "docs" / "02-features.md"
SPECS = REPO / "docs" / "04-specs"
BACKEND_TESTS = REPO / "backend" / "tests"
FRONTEND_SRC = REPO / "frontend" / "src"

SCENARIO = re.compile(r"^\s*Scenario(?: Outline)?:\s*(S-\d+)")


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def built_features() -> list[str]:
    """IDs of features whose Status is `built` in the feature list table."""
    if not FEATURES.exists():
        return []
    built, status_col = [], None
    for line in FEATURES.read_text(encoding="utf-8").splitlines():
        if not line.lstrip().startswith("|"):
            status_col = None
            continue
        cells = _cells(line)
        if cells and cells[0] == "ID" and "Status" in cells:
            status_col = cells.index("Status")
        elif (
            status_col is not None
            and re.fullmatch(r"F-\d+", cells[0])
            and len(cells) > status_col
            and cells[status_col] == "built"
        ):
            built.append(cells[0])
    return built


def scenarios(spec: Path) -> list[tuple[str, str]]:
    """(scenario ID, level) pairs; level is 'ui' if tagged @ui, else 'api'."""
    found, tags = [], set()
    for line in spec.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("@"):
            tags |= set(stripped.split())
            continue
        match = SCENARIO.match(line)
        if match:
            found.append((match.group(1), "ui" if "@ui" in tags else "api"))
        if stripped:
            tags = set()
    return found


def _read_all(paths) -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in paths)


def test_every_scenario_of_a_built_feature_has_a_test():
    frontend_tests = _read_all(
        p for p in FRONTEND_SRC.rglob("*.test.ts*") if "node_modules" not in p.parts
    )
    missing = []
    for feature in built_features():
        number = feature.split("-")[1]
        specs = sorted(SPECS.glob(f"{feature}-*.feature"))
        if not specs:
            missing.append(f"{feature}: no spec in docs/04-specs/")
            continue
        backend_tests = _read_all(BACKEND_TESTS.glob(f"test_f_{number}_*.py"))
        for scenario, level in scenarios(specs[0]):
            if level == "api":
                expected = f"def test_s{scenario.split('-')[1]}_"
                if expected not in backend_tests:
                    missing.append(
                        f"{feature}/{scenario} @api: no `{expected}…` in test_f_{number}_*.py"
                    )
            elif f"{feature}/{scenario}" not in frontend_tests:
                missing.append(f"{feature}/{scenario} @ui: no test titled '{feature}/{scenario} …'")
    assert not missing, "Scenarios without tests:\n" + "\n".join(missing)
