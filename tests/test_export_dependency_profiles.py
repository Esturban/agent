from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from export_dependency_profiles import OUTPUT_DIR, load_profiles, render, validate  # noqa: E402


class DependencyProfileExportTests(unittest.TestCase):
    def test_every_registry_profile_has_a_matching_pinned_export(self) -> None:
        profiles = load_profiles()
        validate(profiles)

        for name, profile in profiles.items():
            output = OUTPUT_DIR / f"{name}.txt"
            self.assertTrue(output.exists(), output)
            self.assertEqual(output.read_text(), render(name, profile["constraints"]))


if __name__ == "__main__":
    unittest.main()
