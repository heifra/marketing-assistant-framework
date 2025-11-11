#!/usr/bin/env python3
"""Parse checkbox selections from variant files."""
from __future__ import annotations

import argparse
from pathlib import Path


def find_checked(lines):
    titles = []
    drafts = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- [") and stripped[3:4] in {"x", "X"}:
            content = stripped.split("]", 1)[1].strip()
            if content.lower().startswith("draft"):
                drafts.append(content)
            else:
                titles.append(content)
    return titles, drafts


def review_gate_ok(review_dir: Path) -> bool:
    if not review_dir:
        return True
    for file in sorted(review_dir.glob("*.md")):
        text = file.read_text(encoding="utf-8")
        if "gate_pass: true" in text:
            return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse variant checkboxes")
    parser.add_argument("variants_dir", type=Path)
    parser.add_argument("--require-review", dest="review_dir", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=Path("planning/selected"))
    args = parser.parse_args()

    if args.review_dir and not review_gate_ok(args.review_dir):
        raise SystemExit("No passing review found; aborting selection generation.")

    args.output.mkdir(parents=True, exist_ok=True)

    for variant_file in sorted(args.variants_dir.glob("*.md")):
        lines = variant_file.read_text(encoding="utf-8").splitlines()
        titles, drafts = find_checked(lines)
        if not titles and not drafts:
            continue
        selected_title = titles[0] if titles else ""
        selected_draft = drafts[0] if drafts else ""
        target = args.output / f"selected-{variant_file.stem}.md"
        content = (
            f"source: {variant_file}\n"
            f"title: {selected_title}\n"
            f"draft: {selected_draft}\n"
        )
        target.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
