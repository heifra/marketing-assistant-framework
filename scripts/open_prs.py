#!/usr/bin/env python3
"""Create placeholder PR readme files for draft directories."""
from __future__ import annotations

import argparse
from pathlib import Path


def read_checklist(path: Path) -> str:
    if path and path.exists():
        return path.read_text(encoding="utf-8").strip()
    fallback = Path("templates/planning/review_checklist.md")
    if fallback.exists():
        return fallback.read_text(encoding="utf-8").strip()
    return "- [ ] Review Checklist pending"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate PR README placeholders")
    parser.add_argument("draft_root", type=Path)
    parser.add_argument("checklist", type=Path)
    args = parser.parse_args()

    checklist_text = read_checklist(args.checklist)
    for subdir in sorted(args.draft_root.iterdir()):
        if not subdir.is_dir():
            continue
        readme = subdir / "PR_README.md"
        content = (
            f"# PR Placeholder for {subdir.name}\n\n"
            "Bitte referenziere das passende Draft-Dokument und hake die Prüfpunkte ab.\n\n"
            f"{checklist_text}\n"
        )
        readme.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
