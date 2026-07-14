# Workbook QA contracts

`workbooks.json` is a versioned registry generator: it materializes one record
for every `examples/*/*.ipynb` file, including its path, required environment,
runtime profile, five-minute timeout, and final code-cell execution checkpoint.

Add lesson-specific checks in an explicit `workbooks` list when a workbook has a
stable expected value. Available checks are `text_matches`, `number_between`,
`json_field_equals`, `file_exists`, and `expected_exception`; all cell checks
target notebook cell IDs rather than positions.

`dependency-profiles.json` records framework environments that cannot safely
share a resolver. Run `python scripts/audit_dependencies.py` to refresh the
import-to-profile report before adding or changing a dependency.
