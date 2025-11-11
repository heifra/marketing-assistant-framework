#!/usr/bin/env python3
"""Deterministic helper CLI for the content-agent boilerplate."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
from textwrap import dedent
from typing import List

from derive_slug import slugify

ROOT = Path(__file__).resolve().parents[1]


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def _timestamp() -> str:
    return dt.datetime.utcnow().strftime("%Y%m%d%H%M%S")


def _week_id() -> str:
    return dt.datetime.utcnow().strftime("%YW%V")


def cmd_quickstart(args: argparse.Namespace) -> None:
    proposal_path = ROOT / "planning/quickstart/proposal.md"
    draft_dir = ROOT / "content" / "drafts" / args.type
    draft_path = draft_dir / "preview.md"
    image_path = ROOT / "images" / "prompts" / "preview.yaml"

    title_suffixes = [
        "Insights", "Playbook", "Roadmap", "LinkedIn-Story"
    ]
    titles = [f"{args.topic} – {suffix}" for suffix in title_suffixes]
    short_drafts = [
        {
            "label": letter,
            "summary": f"{args.topic} für {args.audience} mit Fokus auf {args.promise.lower()} ({args.voice}).",
            "reason": f"Stützt sich auf {args.source or 'interne Beobachtungen'} und liefert schnellen Mehrwert."
        }
        for letter in ("A", "B", "C")
    ]
    proposal_lines = ["# Quickstart Proposal", "## Titelideen"]
    for idx, title in enumerate(titles, start=1):
        proposal_lines.append(f"{idx}. {title}")
    proposal_lines.append("\n## Kurz-Drafts")
    for draft in short_drafts:
        proposal_lines.append(
            f"- {draft['label']}: {draft['summary']} — Grund: {draft['reason']}"
        )
    _write(proposal_path, "\n".join(proposal_lines))

    base_sentences = [
        f"{args.topic} beschäftigt aktuell jede {args.audience}, die spürbar bessere Ergebnisse erwartet.",
        f"In diesem Beitrag zeige ich in klarer Sprache, wie {args.promise} ohne unnötige Komplexität gelingt.",
        f"Ich orientiere mich an einer Stimme, die {args.voice} wirkt und trotzdem messbar bleibt.",
        "Der Ansatz nutzt drei kurze Schritte: Beobachten, Testen und Messwerte konsequent an Stakeholder teilen.",
        "So bleiben Initiativen steuerbar, selbst wenn Budgets oder Ressourcen schwanken.",
        f"{args.topic} entfaltet erst dann seine Stärke, wenn Teams Kennzahlen als Dialog statt als Urteil lesen.",
        "Darum endet jeder Sprint mit einer Mini-Retrospektive, die Chancen und Risiken verbindet.",
        "Das macht Fortschritt sichtbar und motiviert die handelnden Personen, ihren eigenen Anteil zu beschreiben.",
        "Mein größtes Learning: Aufmerksamkeit gehört zuerst dem Problem, erst dann dem Tool.",
        f"Wenn du tiefer einsteigen willst, nutze die Quelle {args.source or 'interne Dossiers'} als Startpunkt.",
        "Lass uns testen, welche Hypothese bei dir als erstes Wirkung zeigt.",
        "Schreib mir eine kurze Nachricht, wenn du das Playbook für dein Team anpassen willst."
    ]
    words: List[str] = " ".join(base_sentences).split()
    filler = (
        "Ich halte jeden Abschnitt bewusst kompakt, damit du sofort entscheiden kannst, "
        "welcher Teil für deine Roadmap relevant ist."
    ).split()
    while len(words) < 150:
        words.extend(filler)
    if len(words) > 210:
        words = words[:210]
    split = len(words) // 2
    body = " ".join(words[:split]) + "\n\n" + " ".join(words[split:])
    frontmatter = dedent(
        f"""
        ---
        title: "Quickstart Preview – {args.topic}"
        type: {args.type}
        topic: "{args.topic}"
        audience: "{args.audience}"
        voice: "{args.voice}"
        promise: "{args.promise}"
        source: "{args.source or ''}"
        generated_at: {_timestamp()}
        ---
        """
    ).strip()
    _write(draft_path, f"{frontmatter}\n\n{body}")

    prompts = {
        "prompts": [
            {
                "label": "hero",
                "text": f"Minimalistische Illustration zu {args.topic} mit Tonalität {args.voice}"
            },
            {
                "label": "support",
                "text": f"Detailaufnahme von Teamarbeit, die {args.promise} visualisiert"
            },
            {
                "label": "data",
                "text": f"Infografik mit Key Metric für {args.audience}"
            }
        ]
    }
    _write(image_path, json.dumps(prompts, indent=2))


def cmd_topic_init(args: argparse.Namespace) -> None:
    file_id = f"{_week_id()}-{_timestamp()[-4:]}"
    path = ROOT / "planning" / "topics" / f"{file_id}.md"
    keywords = [kw.strip() for kw in (args.keywords or "").split(",") if kw.strip()]
    kw_string = ", ".join(keywords)
    content = dedent(
        f"""
        ---
        type: {args.type}
        brief: "{args.brief}"
        url: "{args.url or ''}"
        keywords: [{kw_string}]
        ---

        ## Thema
        {args.brief}
        """
    )
    _write(path, content)


def cmd_variants(_: argparse.Namespace) -> None:
    file_id = f"variants-{_timestamp()}"
    path = ROOT / "planning" / "variants" / f"{file_id}.md"
    titles = [f"Option {i}: Insight #{i}" for i in range(1, 7)]
    drafts = {
        "A": "Kurz-Story über Problem, Lösung, CTA.",
        "B": "Framework mit drei Schritten und Kennzahl.",
        "C": "Kundenbeispiel mit klarer Wirkung."
    }
    lines = ["# Varianten"]
    lines += [f"- [ ] {title}" for title in titles]
    lines.append("\n## Kurz-Drafts")
    for label, text in drafts.items():
        lines.append(f"- [ ] Draft {label}: {text}")
    _write(path, "\n".join(lines))


def cmd_review(_: argparse.Namespace) -> None:
    file_id = f"review-{_timestamp()}"
    path = ROOT / "planning" / "reviews" / f"{file_id}.md"
    scores = {
        "interesse": 4,
        "mehrwert": 4,
        "differenzierung": 3,
        "plattform": 4,
        "markenfit": 4,
    }
    total = sum(scores.values())
    content = dedent(
        f"""
        gate_pass: {str(total >= 18).lower()}
        scores:
        {json.dumps(scores, indent=2)}
        total: {total}
        recommendation: proceed
        """
    )
    _write(path, content)


def cmd_finalize(args: argparse.Namespace) -> None:
    title = args.title or "Final Draft Placeholder"
    slug = args.slug or slugify(title)
    ctype = args.type
    path = ROOT / "content" / "drafts" / ctype / f"{slug}.md"
    frontmatter = dedent(
        f"""
        ---
        title: "{title}"
        slug: "{slug}"
        type: {ctype}
        date: "{dt.date.today()}"
        tags: [draft]
        status: draft
        ---
        """
    )
    body = (
        "Dieser Skeleton-Draft markiert den Übergang vom Auswahlprozess zum finalen Text. "
        "Er enthält Platzhalter für Outline, Quellen und finale CTA."
    )
    _write(path, f"{frontmatter}\n\n{body}\n")


def cmd_research(args: argparse.Namespace) -> None:
    mode = args.mode
    timestamp = _timestamp()
    path = ROOT / "knowledge" / "research" / mode / f"research-{timestamp}.md"
    content = dedent(
        f"""
        # Research Notes ({mode})
        - Insight: Placeholder trend mit Datum {dt.date.today()}.
        - Tactic: Kurzer Hinweis, wie {mode} Content davon profitiert.
        - Source Placeholder: https://example.org/research
        """
    )
    _write(path, content)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Content agent helper")
    sub = parser.add_subparsers(dest="command", required=True)

    q = sub.add_parser("quickstart", help="Generate quickstart artifacts")
    q.add_argument("--type", required=True)
    q.add_argument("--topic", required=True)
    q.add_argument("--audience", required=True)
    q.add_argument("--voice", required=True)
    q.add_argument("--promise", required=True)
    q.add_argument("--source", default="")
    q.set_defaults(func=cmd_quickstart)

    t = sub.add_parser("topic_init", help="Create topic file from template")
    t.add_argument("--type", required=True)
    t.add_argument("--brief", required=True)
    t.add_argument("--url", default="")
    t.add_argument("--keywords", default="")
    t.set_defaults(func=cmd_topic_init)

    v = sub.add_parser("variants", help="Generate variants stub")
    v.set_defaults(func=cmd_variants)

    r = sub.add_parser("review", help="Create review stub")
    r.set_defaults(func=cmd_review)

    f = sub.add_parser("finalize", help="Create draft from selection")
    f.add_argument("--type", default="web_article")
    f.add_argument("--title", default="")
    f.add_argument("--slug", default="")
    f.set_defaults(func=cmd_finalize)

    res = sub.add_parser("research", help="Store research note")
    res.add_argument("--mode", required=True)
    res.set_defaults(func=cmd_research)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
