#!/usr/bin/env python3
"""Repository-level wrapper for the skill's review page build/audit harness."""

from __future__ import annotations

import runpy
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "course-ppt-review-html"
    / "scripts"
    / "build_review_page.py"
)

runpy.run_path(str(SCRIPT), run_name="__main__")
