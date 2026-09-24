#!/usr/bin/env python3
"""Repair legacy cell-markup workbooks and add required nbformat cell IDs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

import nbformat

LEGACY_CELL = re.compile(r'<cell id="(?P<id>[^"]+)">(?P<body>.*?)(?=<cell id="|\Z)', re.DOTALL)
LEGACY_CLOSE = re.compile(r'</cell id="[^"]+">\s*\Z')
MARKDOWN_TYPE = "<cell_type>markdown</cell_type>"


def convert_legacy_notebook(source: str) -> dict[str, Any]:
    """Convert the repository's pre-nbformat cell markup into nbformat v4 data."""
    cells = []
    for match in LEGACY_CELL.finditer(source):
        cell_id = match.group("id")
        body = LEGACY_CLOSE.sub("", match.group("body"))
        if body.startswith(MARKDOWN_TYPE):
            cells.append(
                nbformat.v4.new_markdown_cell(body.removeprefix(MARKDOWN_TYPE), id=cell_id)
            )
        else:
            cells.append(nbformat.v4.new_code_cell(body, id=cell_id))
    if not cells:
        raise ValueError("legacy markup contains no cells")
    return nbformat.v4.new_notebook(
        cells=cells, metadata={"kernelspec": {"name": "python3", "display_name": "Python 3"}}
    )


def repair_notebook(path: Path, write: bool) -> bool:
    """Return whether a repair is needed; write only when explicitly requested."""
    source = path.read_text(encoding="utf-8")
    try:
        raw_notebook = json.loads(source)
        changed = False
        for index, cell in enumerate(raw_notebook.get("cells", [])):
            cell.setdefault("metadata", {})
            if cell.get("cell_type") == "code":
                cell.setdefault("execution_count", None)
                cell.setdefault("outputs", [])
            if not cell.get("id"):
                digest = hashlib.sha1(
                    f"{path}:{index}:{cell.get('source', '')}".encode()
                ).hexdigest()[:12]
                cell["id"] = f"qa-{digest}"
                changed = True
        notebook = nbformat.from_dict(raw_notebook)
    except (nbformat.reader.NotJSONError, json.JSONDecodeError):
        notebook = convert_legacy_notebook(source)
        changed = True
    if changed and write:
        nbformat.write(notebook, path)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="apply repairs; otherwise report only")
    parser.add_argument("paths", nargs="*", type=Path)
    arguments = parser.parse_args()
    paths = arguments.paths or sorted(Path("examples").glob("*/*.ipynb"))
    changed = [path for path in paths if repair_notebook(path, arguments.write)]
    for path in changed:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
