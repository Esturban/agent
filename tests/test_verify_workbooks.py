import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from repair_notebooks import (
    convert_legacy_notebook,  # noqa: E402
    repair_notebook,  # noqa: E402
)
from verify_workbooks import (  # noqa: E402
    CheckResult,
    WorkbookRecord,
    _run_in_docker,
    evaluate_checks,
    load_registry,
    preflight,
    sweep_stale_workspaces,
    validate_notebook,
)


def write_notebook(path: Path, cells: list[dict]) -> None:
    path.write_text(
        json.dumps(
            {
                "nbformat": 4,
                "nbformat_minor": 5,
                "metadata": {"kernelspec": {"name": "python3"}},
                "cells": cells,
            }
        )
    )


def code_cell(cell_id: str, source: str, outputs: list[dict] | None = None) -> dict:
    return {
        "cell_type": "code",
        "id": cell_id,
        "source": source,
        "metadata": {},
        "execution_count": 1,
        "outputs": outputs or [],
    }


class VerifyWorkbooksTests(unittest.TestCase):
    def test_executor_enforces_a_global_timeout_and_writes_an_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            notebook_path = root / "slow.ipynb"
            output_path = root / "executed.ipynb"
            write_notebook(notebook_path, [code_cell("slow", "import time\ntime.sleep(10)")])
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "execute_notebook.py"),
                    "--notebook",
                    str(notebook_path),
                    "--output",
                    str(output_path),
                    "--timeout",
                    "1",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 124)
            self.assertIn("global timeout", completed.stderr)
            self.assertTrue(output_path.is_file())

    def test_registry_requires_a_unique_record_for_every_workbook(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "examples/a").mkdir(parents=True)
            write_notebook(root / "examples/a/a.ipynb", [code_cell("last", "print('ok')")])
            registry_path = root / "registry.json"
            registry_path.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "workbooks": [
                            {
                                "slug": "a",
                                "path": "examples/a/a.ipynb",
                                "profile": "local",
                                "required_env": [],
                                "checks": [{"kind": "cell_executed", "cell_id": "last"}],
                            }
                        ],
                    }
                )
            )
            registry = load_registry(registry_path, root)
            self.assertEqual([record.slug for record in registry], ["a"])

    def test_invalid_notebook_is_reported_without_execution(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "broken.ipynb"
            path.write_text("<cell>not json</cell>")
            valid, message, notebook = validate_notebook(path)
            self.assertFalse(valid)
            self.assertIn("JSON", message)
            self.assertIsNone(notebook)

    def test_legacy_cell_markup_is_converted_to_a_valid_notebook(self) -> None:
        converted = convert_legacy_notebook(
            '<cell id="intro"><cell_type>markdown</cell_type># Intro</cell id="intro">\n'
            '<cell id="answer">print("ready")</cell id="answer">'
        )
        self.assertEqual([cell["id"] for cell in converted["cells"]], ["intro", "answer"])
        self.assertEqual([cell["cell_type"] for cell in converted["cells"]], ["markdown", "code"])

    def test_repair_adds_missing_cell_ids(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "missing-id.ipynb"
            write_notebook(
                path,
                [
                    code_cell("present", "pass"),
                    {"cell_type": "markdown", "metadata": {}, "source": "text"},
                ],
            )
            self.assertTrue(repair_notebook(path, write=True))
            self.assertTrue(validate_notebook(path)[0])

    def test_preflight_blocks_missing_environment_variable(self) -> None:
        record = WorkbookRecord("demo", Path("demo.ipynb"), "live", ("DEMO_SECRET",), (), 300)
        self.assertEqual(preflight(record, {}), ["missing environment variable: DEMO_SECRET"])

    def test_checks_support_output_text_numeric_json_file_and_expected_exception(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            artifact = root / "answer.txt"
            artifact.write_text("done")
            notebook = {
                "cells": [
                    code_cell(
                        "answer",
                        "print('score=0.9')",
                        [{"output_type": "stream", "name": "stdout", "text": "score=0.9\n"}],
                    ),
                    code_cell(
                        "payload",
                        'print(\'{"label": "pass"}\')',
                        [
                            {
                                "output_type": "stream",
                                "name": "stdout",
                                "text": '{"label": "pass"}\n',
                            }
                        ],
                    ),
                    code_cell(
                        "error",
                        "raise ValueError('expected')",
                        [{"output_type": "error", "ename": "ValueError", "evalue": "expected"}],
                    ),
                ]
            }
            checks = [
                {"kind": "text_matches", "cell_id": "answer", "pattern": "score=0\\.9"},
                {
                    "kind": "number_between",
                    "cell_id": "answer",
                    "pattern": "score=(\\d+\\.\\d+)",
                    "minimum": 0.8,
                    "maximum": 1.0,
                },
                {
                    "kind": "json_field_equals",
                    "cell_id": "payload",
                    "field": "label",
                    "equals": "pass",
                },
                {"kind": "file_exists", "path": "answer.txt"},
                {"kind": "expected_exception", "cell_id": "error", "exception": "ValueError"},
            ]
            results = evaluate_checks(notebook, checks, root)
            self.assertTrue(all(result.passed for result in results), results)

    def test_cell_execution_check_uses_stable_cell_id_not_position(self) -> None:
        notebook = {"cells": [code_cell("later", "pass"), code_cell("first", "pass")]}
        results = evaluate_checks(
            notebook, [{"kind": "cell_executed", "cell_id": "first"}], Path.cwd()
        )
        self.assertEqual(results, [CheckResult("cell_executed", "first", True, "cell executed")])

    def test_docker_run_pins_the_container_user_to_the_host_uid_and_gid(self) -> None:
        """Guards against the container writing root-owned files into the bind mount."""
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory) / "repo"
            (root / "examples/a").mkdir(parents=True)
            write_notebook(root / "examples/a/a.ipynb", [code_cell("last", "print('ok')")])
            record = WorkbookRecord("a", root / "examples/a/a.ipynb", "live", (), (), 300)
            artifact_dir = Path(temporary_directory) / "artifacts"

            with patch("verify_workbooks.subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0, stderr="", stdout="")
                _run_in_docker(record, root, {}, artifact_dir, "agent-workbook-qa:latest")

            command = mock_run.call_args.args[0]
            self.assertIn("-u", command)
            self.assertEqual(command[command.index("-u") + 1], f"{os.getuid()}:{os.getgid()}")

    def test_sweep_stale_workspaces_removes_leftover_sandbox_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            base = Path(temporary_directory)
            stale = base / "workbook-qa-abc123"
            (stale / "workspace").mkdir(parents=True)
            (stale / "workspace" / "file.txt").write_text("leftover")
            removed = sweep_stale_workspaces(temp_root=base)
            self.assertEqual(removed, 1)
            self.assertFalse(stale.exists())


if __name__ == "__main__":
    unittest.main()
