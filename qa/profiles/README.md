# Dependency profiles

Each `.txt` file is the pinned top-level dependency set for one workbook runtime profile. Install exactly one profile into an isolated environment; do not merge profiles into the root environment.

```bash
python -m pip install -r qa/profiles/core-openai-v1.txt
python3 scripts/export_dependency_profiles.py --check
```

The registry in `qa/dependency-profiles.json` is authoritative. These files intentionally pin first-party/top-level requirements only; generate a platform-specific full transitive lock when provisioning a production or CI image.
