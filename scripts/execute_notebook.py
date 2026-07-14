#!/usr/bin/env python3
"""Container entrypoint that writes an executed notebook without touching its source."""

from __future__ import annotations

import argparse
import signal
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient


class WorkbookTimeout(TimeoutError):
    """Raised when the complete workbook exceeds its wall-clock smoke limit."""


def _raise_timeout(signum: int, frame: object) -> None:
    del signum, frame
    raise WorkbookTimeout("workbook exceeded its global timeout")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--notebook", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=int, required=True)
    parser.add_argument(
        "--progress", action="store_true", help="print the current cell id as it runs"
    )
    parser.add_argument("--progress-file", type=Path, help="append current cell IDs to this file")
    arguments = parser.parse_args()
    notebook = nbformat.read(arguments.notebook, as_version=4)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    callbacks = {}
    if arguments.progress or arguments.progress_file:

        def record_progress(cell: object, cell_index: int) -> None:
            cell_id = getattr(cell, "get", lambda *_: "<missing>")("id", "<missing>")
            message = f"cell {cell_index}: {cell_id}"
            if arguments.progress:
                print(message, flush=True)
            if arguments.progress_file:
                arguments.progress_file.parent.mkdir(parents=True, exist_ok=True)
                with arguments.progress_file.open("a", encoding="utf-8") as progress_file:
                    progress_file.write(message + "\n")

        callbacks["on_cell_start"] = record_progress
    previous_handler = signal.signal(signal.SIGALRM, _raise_timeout)
    signal.setitimer(signal.ITIMER_REAL, arguments.timeout)
    try:
        NotebookClient(
            notebook,
            timeout=arguments.timeout,
            kernel_name="python3",
            shutdown_kernel="immediate",
            resources={"metadata": {"path": str(arguments.notebook.parent)}},
            **callbacks,
        ).execute()
    except WorkbookTimeout as error:
        print(str(error), file=sys.stderr)
        return 124
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)
        nbformat.write(notebook, arguments.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
