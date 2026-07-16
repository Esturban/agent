#!/usr/bin/env python3
"""Execute teaching workbooks in disposable environments and report evidence.

The runner intentionally keeps notebook sources immutable. It writes all execution
outputs and reports to an ignored artifact directory.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    from dotenv import dotenv_values
except ImportError:  # pragma: no cover - dependency is pinned for the project
    dotenv_values = None


DEFAULT_TIMEOUT_SECONDS = 300
TERMINAL_STATUSES = {"PASS", "FAIL", "BLOCKED", "INVALID", "TIMEOUT"}


@dataclass(frozen=True)
class WorkbookRecord:
    slug: str
    path: Path
    profile: str
    required_env: tuple[str, ...]
    checks: tuple[dict[str, Any], ...]
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS


@dataclass(frozen=True)
class CheckResult:
    kind: str
    target: str
    passed: bool
    detail: str


@dataclass
class WorkbookResult:
    slug: str
    path: str
    profile: str
    status: str
    duration_seconds: float
    detail: str
    checks: list[CheckResult]
    failed_cell_id: str | None = None
    script_check: str = "not found"


def validate_notebook(path: Path) -> tuple[bool, str, dict[str, Any] | None]:
    """Return notebook data only when it is valid nbformat-style JSON."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return False, f"invalid JSON: {error.msg}", None
    except OSError as error:
        return False, f"cannot read notebook: {error}", None

    if not isinstance(data, dict) or not isinstance(data.get("cells"), list):
        return False, "invalid notebook schema: missing cells list", None
    if data.get("nbformat") != 4:
        return False, "invalid notebook schema: expected nbformat 4", None

    cell_ids = [cell.get("id") for cell in data["cells"] if isinstance(cell, dict)]
    if not all(isinstance(cell_id, str) and cell_id for cell_id in cell_ids):
        return False, "invalid notebook schema: every cell requires an id", None
    if len(cell_ids) != len(set(cell_ids)):
        return False, "invalid notebook schema: duplicate cell id", None
    return True, "valid", data


def load_registry(path: Path, root: Path) -> list[WorkbookRecord]:
    """Load a registry and reject duplicate or untracked workbook paths."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 1:
        raise ValueError("registry must contain version 1")
    raw_records = data.get("workbooks")
    if raw_records is None and data.get("discover") is True:
        raw_records = _discover_workbooks(root, data)
    if not isinstance(raw_records, list):
        raise ValueError("registry must contain a workbooks list or discover=true")

    records: list[WorkbookRecord] = []
    seen_slugs: set[str] = set()
    seen_paths: set[Path] = set()
    for raw in raw_records:
        slug = raw.get("slug")
        relative_path = raw.get("path")
        if not isinstance(slug, str) or not isinstance(relative_path, str):
            raise ValueError("every registry record needs string slug and path")
        resolved_path = (root / relative_path).resolve()
        if root.resolve() not in resolved_path.parents:
            raise ValueError(f"workbook path escapes repository: {relative_path}")
        if slug in seen_slugs or resolved_path in seen_paths:
            raise ValueError(f"duplicate workbook registry entry: {slug}")
        checks = raw.get("checks", [])
        if not isinstance(checks, list):
            raise ValueError(f"checks for {slug} must be a list")
        records.append(
            WorkbookRecord(
                slug=slug,
                path=resolved_path,
                profile=str(raw.get("profile", "live")),
                required_env=tuple(raw.get("required_env", [])),
                checks=tuple(checks),
                timeout_seconds=int(raw.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS)),
            )
        )
        seen_slugs.add(slug)
        seen_paths.add(resolved_path)

    discovered = {item.resolve() for item in (root / "examples").glob("*/*.ipynb")}
    if seen_paths != discovered:
        missing = sorted(str(item.relative_to(root)) for item in discovered - seen_paths)
        extra = sorted(str(item.relative_to(root)) for item in seen_paths - discovered)
        raise ValueError(f"registry does not match examples (missing={missing}, extra={extra})")
    return records


def _discover_workbooks(root: Path, registry: dict[str, Any]) -> list[dict[str, Any]]:
    """Materialize one deterministic record per workbook from versioned defaults."""
    environment_names = tuple(registry.get("environment_names", []))
    timeout_seconds = int(registry.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
    paths = sorted((root / "examples").glob("*/*.ipynb"))
    duplicate_slugs = {
        path.parent.name
        for path in paths
        if sum(item.parent.name == path.parent.name for item in paths) > 1
    }
    records: list[dict[str, Any]] = []
    for path in paths:
        source = path.read_text(encoding="utf-8")
        slug = (
            path.parent.name
            if path.parent.name not in duplicate_slugs
            else f"{path.parent.name}--{path.stem}"
        )
        profile = _profile_for(path, source)
        required_env = [
            name
            for name in environment_names
            if re.search(rf"(?<![A-Z0-9_]){re.escape(name)}(?![A-Z0-9_])", source)
        ]
        checks: list[dict[str, Any]] = []
        valid, _, notebook = validate_notebook(path)
        if valid and notebook:
            code_cells = [cell for cell in notebook["cells"] if cell.get("cell_type") == "code"]
            if code_cells:
                checks.append({"kind": "cell_executed", "cell_id": code_cells[-1]["id"]})
        records.append(
            {
                "slug": slug,
                "path": str(path.relative_to(root)),
                "profile": profile,
                "required_env": required_env,
                "timeout_seconds": timeout_seconds,
                "checks": checks,
            }
        )
    return records


def _profile_for(path: Path, source: str) -> str:
    text = f"{path.as_posix()} {source}".lower()
    if any(
        term in text
        for term in ("finetuning", "alignment", "model-merging", "qlora", "lora-architecture")
    ):
        return "training"
    if any(term in text for term in ("redis", "qdrant", "searx", "deerflow", "langfuse", "zep")):
        return "service"
    if any(term in text for term in ("playwright", "browser", "computer-use")):
        return "browser"
    return "live"


def preflight(record: WorkbookRecord, environment: dict[str, str]) -> list[str]:
    """Return safe, human-readable prerequisite failures without secret values."""
    return [
        f"missing environment variable: {variable}"
        for variable in record.required_env
        if not environment.get(variable)
    ]


def _cell_by_id(notebook: dict[str, Any], cell_id: str) -> dict[str, Any] | None:
    return next((cell for cell in notebook["cells"] if cell.get("id") == cell_id), None)


def _cell_text(cell: dict[str, Any]) -> str:
    text: list[str] = []
    for output in cell.get("outputs", []):
        if output.get("output_type") == "stream":
            raw_text = output.get("text", "")
            text.append(raw_text if isinstance(raw_text, str) else "".join(raw_text))
        elif output.get("output_type") in {"execute_result", "display_data"}:
            value = output.get("data", {}).get("text/plain", "")
            text.append(value if isinstance(value, str) else "".join(value))
    return "\n".join(text)


def evaluate_checks(
    notebook: dict[str, Any],
    checks: tuple[dict[str, Any], ...] | list[dict[str, Any]],
    workspace: Path,
) -> list[CheckResult]:
    """Evaluate deterministic notebook-output contracts."""
    results: list[CheckResult] = []
    for check in checks:
        kind = str(check.get("kind", ""))
        cell_id = str(check.get("cell_id", ""))
        cell = _cell_by_id(notebook, cell_id) if cell_id else None
        target = cell_id or str(check.get("path", ""))
        if kind == "file_exists":
            target_path = workspace / str(check["path"])
            results.append(
                CheckResult(
                    kind,
                    str(check["path"]),
                    target_path.is_file(),
                    "file exists" if target_path.is_file() else "file missing",
                )
            )
            continue
        if cell is None:
            results.append(CheckResult(kind, target, False, "cell id not found"))
            continue
        if kind == "cell_executed":
            passed = cell.get("execution_count") is not None
            results.append(
                CheckResult(
                    kind, cell_id, passed, "cell executed" if passed else "cell was not executed"
                )
            )
        elif kind == "expected_exception":
            exception = str(check["exception"])
            errors = [
                output.get("ename")
                for output in cell.get("outputs", [])
                if output.get("output_type") == "error"
            ]
            results.append(
                CheckResult(
                    kind, cell_id, exception in errors, f"expected {exception}, got {errors}"
                )
            )
        elif kind == "text_matches":
            passed = bool(re.search(str(check["pattern"]), _cell_text(cell), re.MULTILINE))
            results.append(
                CheckResult(
                    kind, cell_id, passed, "text matched" if passed else "text did not match"
                )
            )
        elif kind == "number_between":
            match = re.search(str(check["pattern"]), _cell_text(cell), re.MULTILINE)
            value = float(match.group(1)) if match else None
            passed = value is not None and float(check["minimum"]) <= value <= float(
                check["maximum"]
            )
            results.append(CheckResult(kind, cell_id, passed, f"value={value}"))
        elif kind == "json_field_equals":
            try:
                payload = json.loads(_cell_text(cell).strip())
                passed = payload.get(check["field"]) == check["equals"]
            except (json.JSONDecodeError, AttributeError):
                passed = False
            results.append(
                CheckResult(
                    kind,
                    cell_id,
                    passed,
                    "JSON field matched" if passed else "JSON field did not match",
                )
            )
        else:
            results.append(CheckResult(kind, target, False, "unsupported check kind"))
    return results


def _environment_from_dotenv(root: Path) -> dict[str, str]:
    values = {key: value for key, value in os.environ.items() if isinstance(value, str)}
    dotenv_path = root / ".env"
    if dotenv_values and dotenv_path.is_file():
        values.update(
            {key: value for key, value in dotenv_values(dotenv_path).items() if value is not None}
        )
    return values


def _copy_repository(root: Path, destination: Path) -> Path:
    ignored_names = shutil.ignore_patterns(
        ".git", ".venv", ".venv-*", ".qa-runs", "__pycache__", ".pytest_cache"
    )
    copied_root = destination / "workspace"
    shutil.copytree(root, copied_root, ignore=ignored_names)
    return copied_root


def _warn_if_workspace_survived(temporary_directory: str) -> None:
    """Surface a leaked sandbox loudly instead of letting cleanup fail silently."""
    remaining = Path(temporary_directory)
    if remaining.exists():
        print(
            f"WARNING: could not fully remove temporary workbook workspace: {remaining}\n"
            "It may contain files with different ownership (e.g. written by a Docker "
            f"container). Remove it manually once safe, e.g.: rm -rf {remaining}",
            file=sys.stderr,
        )


def stale_workspaces(temp_root: Path | None = None) -> list[Path]:
    """Return workbook-qa-* sandbox directories left behind by prior interrupted runs."""
    base = temp_root or Path(tempfile.gettempdir())
    return sorted(path for path in base.glob("workbook-qa-*") if path.is_dir())


def sweep_stale_workspaces(temp_root: Path | None = None) -> int:
    """Remove stale workbook-qa-* sandbox directories, warning about any that resist removal."""
    stale = stale_workspaces(temp_root)
    if not stale:
        print("no stale workbook-qa-* directories found")
        return 0
    removed = 0
    for path in stale:
        shutil.rmtree(path, ignore_errors=True)
        if path.exists():
            print(f"WARNING: could not remove {path} (check ownership/permissions)", file=sys.stderr)
        else:
            print(f"removed {path}")
            removed += 1
    return removed


def _run_in_docker(
    record: WorkbookRecord, root: Path, environment: dict[str, str], artifact_dir: Path, image: str
) -> tuple[bool, str, Path | None]:
    with tempfile.TemporaryDirectory(
        prefix="workbook-qa-", ignore_cleanup_errors=True
    ) as temporary_directory:
        copied_root = _copy_repository(root, Path(temporary_directory))
        relative_notebook = record.path.relative_to(root)
        output_relative = Path(".qa-executed") / f"{record.slug}.ipynb"
        command = [
            "docker",
            "run",
            "--rm",
            "-u",
            f"{os.getuid()}:{os.getgid()}",
            "-v",
            f"{copied_root}:/workspace",
            "-w",
            "/workspace",
        ]
        for variable in record.required_env:
            command.extend(["-e", variable])
        command.extend(
            [
                image,
                "python",
                "scripts/execute_notebook.py",
                "--notebook",
                str(relative_notebook),
                "--output",
                str(output_relative),
                "--timeout",
                str(record.timeout_seconds),
            ]
        )
        completed = subprocess.run(
            command,
            cwd=root,
            env={
                **os.environ,
                **{key: environment[key] for key in record.required_env if key in environment},
            },
            text=True,
            capture_output=True,
            timeout=record.timeout_seconds + 30,
            check=False,
        )
        source_output = copied_root / output_relative
        if source_output.is_file():
            artifact_dir.mkdir(parents=True, exist_ok=True)
            target = artifact_dir / f"{record.slug}.ipynb"
            shutil.copy2(source_output, target)
            result = (completed.returncode == 0, completed.stderr[-4000:], target)
        else:
            result = (
                completed.returncode == 0,
                completed.stderr[-4000:] or completed.stdout[-4000:],
                None,
            )
    _warn_if_workspace_survived(temporary_directory)
    return result


def _run_locally(
    record: WorkbookRecord,
    root: Path,
    environment: dict[str, str],
    artifact_dir: Path,
) -> tuple[bool, str, Path | None]:
    """Run in a disposable repository copy using the active project interpreter."""
    with tempfile.TemporaryDirectory(
        prefix="workbook-qa-", ignore_cleanup_errors=True
    ) as temporary_directory:
        copied_root = _copy_repository(root, Path(temporary_directory))
        relative_notebook = record.path.relative_to(root)
        output_relative = Path(".qa-executed") / f"{record.slug}.ipynb"
        completed = subprocess.run(
            [
                sys.executable,
                "scripts/execute_notebook.py",
                "--notebook",
                str(relative_notebook),
                "--output",
                str(output_relative),
                "--timeout",
                str(record.timeout_seconds),
            ],
            cwd=copied_root,
            env={**os.environ, **{key: environment[key] for key in record.required_env}},
            text=True,
            capture_output=True,
            timeout=record.timeout_seconds + 30,
            check=False,
        )
        source_output = copied_root / output_relative
        if source_output.is_file():
            artifact_dir.mkdir(parents=True, exist_ok=True)
            target = artifact_dir / f"{record.slug}.ipynb"
            shutil.copy2(source_output, target)
            result = (completed.returncode == 0, completed.stderr[-4000:], target)
        else:
            result = (
                completed.returncode == 0,
                completed.stderr[-4000:] or completed.stdout[-4000:],
                None,
            )
    _warn_if_workspace_survived(temporary_directory)
    return result


def _validate_companion_script(record: WorkbookRecord) -> str:
    """Statically compile a matching entry point without importing application code."""
    script_path = record.path.parent / "main.py"
    if not script_path.is_file():
        return "not found"
    try:
        compile(script_path.read_text(encoding="utf-8"), str(script_path), "exec")
    except SyntaxError as error:
        return f"syntax error: line {error.lineno}: {error.msg}"
    return "syntax valid"


def verify_record(
    record: WorkbookRecord,
    root: Path,
    environment: dict[str, str],
    artifact_dir: Path,
    image: str,
    engine: str,
) -> WorkbookResult:
    started = time.monotonic()
    script_check = _validate_companion_script(record)
    valid, detail, notebook = validate_notebook(record.path)
    if not valid:
        return WorkbookResult(
            record.slug,
            str(record.path.relative_to(root)),
            record.profile,
            "INVALID",
            0,
            detail,
            [],
            script_check=script_check,
        )
    prerequisites = preflight(record, environment)
    if prerequisites:
        return WorkbookResult(
            record.slug,
            str(record.path.relative_to(root)),
            record.profile,
            "BLOCKED",
            0,
            "; ".join(prerequisites),
            [],
            script_check=script_check,
        )
    try:
        if engine == "docker":
            succeeded, output, executed_path = _run_in_docker(
                record, root, environment, artifact_dir, image
            )
        else:
            succeeded, output, executed_path = _run_locally(record, root, environment, artifact_dir)
    except subprocess.TimeoutExpired:
        return WorkbookResult(
            record.slug,
            str(record.path.relative_to(root)),
            record.profile,
            "TIMEOUT",
            record.timeout_seconds,
            "container timed out",
            [],
            script_check=script_check,
        )
    if not succeeded or executed_path is None:
        status = "TIMEOUT" if "global timeout" in output else "FAIL"
        return WorkbookResult(
            record.slug,
            str(record.path.relative_to(root)),
            record.profile,
            status,
            time.monotonic() - started,
            output or "execution failed",
            [],
            script_check=script_check,
        )
    _, _, executed_notebook = validate_notebook(executed_path)
    assert executed_notebook is not None
    checks = evaluate_checks(executed_notebook, record.checks, executed_path.parent)
    status = "PASS" if all(result.passed for result in checks) else "FAIL"
    detail = "verified" if status == "PASS" else "one or more lesson checks failed"
    return WorkbookResult(
        record.slug,
        str(record.path.relative_to(root)),
        record.profile,
        status,
        time.monotonic() - started,
        detail,
        checks,
        script_check=script_check,
    )


def write_reports(results: list[WorkbookResult], report_dir: Path) -> tuple[Path, Path]:
    report_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    json_path = report_dir / f"workbooks-{timestamp}.json"
    markdown_path = report_dir / f"workbooks-{timestamp}.md"
    json_path.write_text(
        json.dumps([asdict(result) for result in results], indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    counts = {
        status: sum(result.status == status for result in results)
        for status in sorted(TERMINAL_STATUSES)
    }
    lines = [
        "# Workbook verification report",
        "",
        f"Generated: {timestamp}",
        "",
        "| Status | Count |",
        "| --- | ---: |",
    ]
    lines.extend(f"| {status} | {count} |" for status, count in counts.items())
    lines.extend(
        [
            "",
            "| Workbook | Status | Entry script | Duration | Evidence |",
            "| --- | --- | --- | ---: | --- |",
        ]
    )
    lines.extend(
        f"| {result.slug} | {result.status} | {result.script_check} | {result.duration_seconds:.1f}s | {result.detail.replace('|', '/')} |"
        for result in results
    )
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, markdown_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="verify every registered workbook")
    parser.add_argument("--only", action="append", default=[], help="verify one slug (repeatable)")
    parser.add_argument(
        "--profile", action="append", default=[], help="restrict to a runtime profile"
    )
    parser.add_argument("--registry", type=Path, default=Path("qa/workbooks.json"))
    parser.add_argument("--image", default="agent-workbook-qa:latest")
    parser.add_argument("--engine", choices=("docker", "local"), default="docker")
    parser.add_argument("--artifacts", type=Path, default=Path(".qa-runs"))
    parser.add_argument(
        "--resume", type=Path, help="rerun only non-passing records from a JSON report"
    )
    parser.add_argument(
        "--gc",
        action="store_true",
        help="remove stale workbook-qa-* sandbox directories from prior interrupted runs and exit",
    )
    arguments = parser.parse_args()
    if arguments.gc:
        sweep_stale_workspaces()
        return 0
    if not arguments.all and not arguments.only and not arguments.resume:
        parser.error("choose --all, at least one --only slug, or --resume")

    root = Path(__file__).resolve().parents[1]
    records = load_registry(root / arguments.registry, root)
    if arguments.resume:
        previous_results = json.loads(arguments.resume.read_text(encoding="utf-8"))
        unfinished = {item["slug"] for item in previous_results if item["status"] != "PASS"}
        records = [record for record in records if record.slug in unfinished]
    selected = [record for record in records if not arguments.only or record.slug in arguments.only]
    if arguments.profile:
        selected = [record for record in selected if record.profile in arguments.profile]
    environment = _environment_from_dotenv(root)
    run_dir = root / arguments.artifacts / datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    results = [
        verify_record(
            record, root, environment, run_dir / "executed", arguments.image, arguments.engine
        )
        for record in selected
    ]
    json_path, markdown_path = write_reports(results, run_dir)
    print(f"report: {json_path}")
    print(f"report: {markdown_path}")
    return 0 if results and all(result.status == "PASS" for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
