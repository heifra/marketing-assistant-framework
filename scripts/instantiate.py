#!/usr/bin/env python3
"""Instantiate template files by replacing ${VAR} placeholders."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

PLACEHOLDER_RE = re.compile(r"\$\{([^}]+)\}")


def parse_vars(values: list[str]) -> dict[str, str]:
    data = {}
    for item in values:
        if "=" not in item:
            continue
        key, value = item.split("=", 1)
        data[key.strip()] = value.strip()
    return data


def render(text: str, variables: dict[str, str]) -> str:
    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        return variables.get(key, match.group(0))

    return PLACEHOLDER_RE.sub(repl, text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Instantiate template")
    parser.add_argument("template", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--var", action="append", default=[], help="KEY=VALUE")
    args = parser.parse_args()

    template_text = args.template.read_text(encoding="utf-8")
    variables = parse_vars(args.var)
    rendered = render(template_text, variables)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
