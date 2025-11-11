#!/usr/bin/env python3
"""Simulate moving drafts to approved content."""
from __future__ import annotations

import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT_ROOT = ROOT / "content" / "drafts"
APPROVED_ROOT = ROOT / "content" / "approved"


def main() -> None:
    today = date.today().isoformat()
    for type_dir in sorted(DRAFT_ROOT.glob("*")):
        if not type_dir.is_dir():
            continue
        target_dir = APPROVED_ROOT / type_dir.name
        target_dir.mkdir(parents=True, exist_ok=True)
        for draft in type_dir.glob("*.md"):
            dest = target_dir / f"{today}-{draft.name}"
            shutil.copy2(draft, dest)


if __name__ == "__main__":
    main()
