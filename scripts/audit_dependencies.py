#!/usr/bin/env python3
"""Map workbook imports to isolated dependency profiles and report manifest drift."""

from __future__ import annotations

import argparse
import ast
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from packaging.requirements import Requirement


def load_profiles(path: Path) -> dict[str, dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 1 or not isinstance(data.get("profiles"), dict):
        raise ValueError("dependency profiles must contain version 1 and a profiles object")
    return data["profiles"]


def load_requirements(path: Path) -> tuple[dict[str, str], list[str]]:
    requirements: dict[str, str] = {}
    duplicates: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        requirement = Requirement(line)
        name = requirement.name.lower().replace("_", "-")
        if name in requirements:
            duplicates.append(name)
        requirements[name] = line
    return requirements, sorted(set(duplicates))


def imported_modules(source: str) -> set[str]:
    """Return top-level modules while safely ignoring notebook shell magics."""
    python = "\n".join(
        "" if line.lstrip().startswith(("%", "!")) else line for line in source.splitlines()
    )
    try:
        tree = ast.parse(python)
    except SyntaxError:
        return set()
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module.split(".")[0])
    return modules


def source_for_notebook(path: Path) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    return "\n".join(
        "".join(cell.get("source", []))
        if isinstance(cell.get("source"), list)
        else str(cell.get("source", ""))
        for cell in notebook.get("cells", [])
        if cell.get("cell_type") == "code"
    )


def select_profile(modules: set[str], profiles: dict[str, dict[str, Any]]) -> str:
    matches = [
        name
        for name, profile in profiles.items()
        if set(profile.get("imports", [])) & modules
    ]
    if len(matches) > 1:
        raise ValueError(f"ambiguous dependency profiles {matches} for imports {sorted(modules)}")
    return matches[0] if matches else "core-openai-v1"


def audit(root: Path, profile_path: Path, requirements_path: Path) -> dict[str, Any]:
    profiles = load_profiles(profile_path)
    requirements, duplicates = load_requirements(requirements_path)
    workbooks: list[dict[str, Any]] = []
    usage: Counter[str] = Counter()
    for path in sorted((root / "examples").glob("*/*.ipynb")):
        try:
            modules = imported_modules(source_for_notebook(path))
            profile = select_profile(modules, profiles)
        except (json.JSONDecodeError, ValueError) as error:
            workbooks.append({"path": str(path.relative_to(root)), "error": str(error)})
            continue
        usage[profile] += 1
        workbooks.append(
            {
                "path": str(path.relative_to(root)),
                "profile": profile,
                "imports": sorted(modules),
            }
        )
    declared_conflicts = sorted(
        {
            tuple(sorted((name, other)))
            for name, profile in profiles.items()
            for other in profile.get("incompatible_with", [])
        }
    )
    missing_constraints = {
        name: [
            constraint
            for constraint in profile.get("constraints", [])
            if Requirement(constraint).name.lower().replace("_", "-") not in requirements
        ]
        for name, profile in profiles.items()
    }
    return {
        "version": 1,
        "manifest": str(requirements_path.relative_to(root)),
        "manifest_package_count": len(requirements),
        "duplicate_manifest_packages": duplicates,
        "profile_usage": dict(sorted(usage.items())),
        "declared_conflicts": [list(conflict) for conflict in declared_conflicts],
        "missing_profile_constraints": {
            name: missing for name, missing in missing_constraints.items() if missing
        },
        "workbooks": workbooks,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles", type=Path, default=Path("qa/dependency-profiles.json"))
    parser.add_argument("--requirements", type=Path, default=Path("requirements.txt"))
    parser.add_argument("--output", type=Path, default=Path("qa/dependency-audit.json"))
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    report = audit(root, root / arguments.profiles, root / arguments.requirements)
    arguments.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        f"audited {len(report['workbooks'])} workbooks; "
        f"profiles={report['profile_usage']}; output={arguments.output}"
    )
    return 1 if report["duplicate_manifest_packages"] or report["missing_profile_constraints"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
