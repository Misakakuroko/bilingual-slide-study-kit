#!/usr/bin/env python3
"""Repository-level wrapper for the skill's asset preparation harness."""

from __future__ import annotations

import runpy
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "course-ppt-review-html"
    / "scripts"
    / "prepare_ppt_review_assets.py"
)

runpy.run_path(str(SCRIPT), run_name="__main__")
