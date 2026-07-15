.PHONY: lint check fix format verify-workbooks build-workbook-image check-dependency-profiles

# Lint — report errors without changing files
lint:
	ruff check examples/

# Check formatting — report diff without changing files (used in CI)
check:
	ruff check examples/
	ruff format --check examples/

# Fix — apply all auto-fixable lint issues and reformat
fix:
	ruff check --fix examples/
	ruff format examples/

# Alias
format: fix

build-workbook-image:
	docker build -f Dockerfile.workbook-qa -t agent-workbook-qa:latest .

verify-workbooks:
	.venv/bin/python scripts/verify_workbooks.py --all

check-dependency-profiles:
	python3 scripts/export_dependency_profiles.py --check
