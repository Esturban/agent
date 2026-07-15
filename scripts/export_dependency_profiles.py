#!/usr/bin/env python3
"""Export and validate pinned top-level requirements for each QA profile."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "qa" / "dependency-profiles.json"
OUTPUT_DIR = ROOT / "qa" / "profiles"


def render(name: str, constraints: list[str]) -> str:
    return "\n".join(
        [
            f"# Generated from qa/dependency-profiles.json: {name}",
            "# Top-level requirements only; resolve a full platform lock separately.",
            *sorted(constraints, key=str.lower),
            "",
            "",
        ]
    )


def load_profiles() -> dict[str, dict]:
    data = json.loads(REGISTRY.read_text())
    if data.get("version") != 1:
        raise ValueError("dependency profile registry must use version 1")
    return data["profiles"]


def validate(profiles: dict[str, dict]) -> None:
    for name, profile in profiles.items():
        constraints = profile.get("constraints", [])
        if not constraints:
            raise ValueError(f"{name} has no constraints")
        unpinned = [constraint for constraint in constraints if "==" not in constraint]
        if unpinned:
            raise ValueError(f"{name} has unpinned constraints: {', '.join(unpinned)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if exported files drift")
    args = parser.parse_args()
    profiles = load_profiles()
    validate(profiles)

    drifted: list[str] = []
    for name, profile in profiles.items():
        output = OUTPUT_DIR / f"{name}.txt"
        expected = render(name, profile["constraints"])
        actual = output.read_text() if output.exists() else ""
        if actual != expected:
            drifted.append(output.relative_to(ROOT).as_posix())
            if not args.check:
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(expected)

    if args.check and drifted:
        raise SystemExit(f"dependency profile exports drifted: {', '.join(drifted)}")
    print(f"profiles={len(profiles)}; drifted={len(drifted)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
