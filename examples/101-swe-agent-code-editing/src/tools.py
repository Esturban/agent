import os
import subprocess
import tempfile
from langchain_core.tools import tool

MAX_STEPS = 10

# The "repo": two files with deliberate bugs written to a temp dir at runtime.
# Bug 1 — find_max initialises to 0 instead of nums[0]; breaks on all-negative lists.
# Bug 2 — average subtracts 1 from the result; off-by-one arithmetic error.
BUGGY_CODE = """\
def find_max(nums):
    max_val = 0  # bug: should be nums[0]
    for n in nums:
        if n > max_val:
            max_val = n
    return max_val

def average(nums):
    return sum(nums) / len(nums) - 1  # bug: spurious -1
"""

TEST_CODE = """\
from buggy import find_max, average

def test_find_max():
    assert find_max([3, 1, 4, 1, 5, 9]) == 9
    assert find_max([-1, -2, -3]) == -1   # fails with max_val=0

def test_average():
    assert average([1, 2, 3, 4, 5]) == 3.0
    assert average([10, 20]) == 15.0       # fails due to -1

if __name__ == "__main__":
    test_find_max()
    test_average()
    print("All tests passed!")
"""


def setup_workspace() -> str:
    """Write buggy.py and test_buggy.py to a fresh temp directory."""
    d = tempfile.mkdtemp(prefix="swe_")
    open(os.path.join(d, "buggy.py"), "w").write(BUGGY_CODE)
    open(os.path.join(d, "test_buggy.py"), "w").write(TEST_CODE)
    return d


@tool
def view_file(path: str) -> str:
    """Read and return the full contents of a file."""
    try:
        return open(path).read()
    except FileNotFoundError:
        return f"Not found: {path}"


@tool
def edit_file(path: str, old_str: str, new_str: str) -> str:
    """Replace the first occurrence of old_str with new_str in a file."""
    content = open(path).read()
    if old_str not in content:
        return f"String not found in {path}"
    open(path, "w").write(content.replace(old_str, new_str, 1))
    return "Edit applied."


@tool
def run_tests(workspace: str) -> str:
    """Run test_buggy.py in workspace and return stdout + stderr."""
    r = subprocess.run(
        ["python", "test_buggy.py"], cwd=workspace,
        capture_output=True, text=True, timeout=15,
    )
    return (r.stdout + r.stderr).strip() or "(no output)"


SWE_TOOLS = [view_file, edit_file, run_tests]
