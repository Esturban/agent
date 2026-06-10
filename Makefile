.PHONY: lint check fix format

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
