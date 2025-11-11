#!/usr/bin/env python3
"""Utility to derive URL-friendly slugs."""
from __future__ import annotations

import argparse
import re


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text or "slug"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a slug from text")
    parser.add_argument("text", help="Input string")
    args = parser.parse_args()
    print(slugify(args.text))


if __name__ == "__main__":
    main()
