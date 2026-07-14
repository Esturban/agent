import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_dependencies import imported_modules, select_profile  # noqa: E402


class DependencyAuditTests(unittest.TestCase):
    def test_import_parser_ignores_notebook_magics(self) -> None:
        modules = imported_modules("%pip install dspy\nimport dspy\nfrom crewai import Agent\n")
        self.assertEqual(modules, {"dspy", "crewai"})

    def test_profile_selection_rejects_incompatible_imports(self) -> None:
        profiles = {
            "core-openai-v1": {"imports": []},
            "crewai-1": {"imports": ["crewai"]},
            "dspy-2": {"imports": ["dspy"]},
        }
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            select_profile({"crewai", "dspy"}, profiles)

    def test_profile_selection_uses_core_when_no_special_framework_is_imported(self) -> None:
        profiles = {"core-openai-v1": {"imports": []}, "dspy-2": {"imports": ["dspy"]}}
        self.assertEqual(select_profile({"langchain"}, profiles), "core-openai-v1")


if __name__ == "__main__":
    unittest.main()
