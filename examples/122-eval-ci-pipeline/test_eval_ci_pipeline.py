"""Live CI assertion for the #122 golden-dataset evaluation workflow."""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv


sys.path.insert(0, str(Path(__file__).parent))
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

from src.workflow import create_workflow  # noqa: E402


def test_good_pipeline_passes_and_degraded_pipeline_fails():
    assert os.environ.get("OPENAI_API_KEY"), "OPENAI_API_KEY is required for this live eval test."
    results = create_workflow()
    assert results["good"]["passed"]
    assert not results["degraded"]["passed"]
