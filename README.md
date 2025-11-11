# Marketing Assistant Framework
Dieses Boilerplate liefert ein Git-zentriertes Content-Agenten-Framework mit klaren Workflows für web_article, youtube_script und linkedin_post.

## Möglichkeiten
- End-to-end Redaktionsfluss: Topic → Varianten → Review → Auswahl → Finalisierung → PR/Merge → Publish.
- Deterministische Skeletons für Policies, Workflows, Checklisten, Prompts, Memory und Knowledge – keine externen Abhängigkeiten.
- Mehrkanal-Workflows (WordPress Blog/Landing, LinkedIn, YouTube) inkl. Eval-Rubriken und Publishing-Pfade.
- Quickstart-Modus (`scripts/agent_run.py quickstart` oder `.github/workflows/quickstart.yml`), der sofort Vorschläge, Drafts und Bildprompts generiert.
- Letta-kompatibler Export (`templates/export/agent_file.template.json`) sowie Instanziierungs-Script (`scripts/instantiate.py`) für markenspezifische Ableger.
- Automatisierte Hilfsskripte (`scripts/parse_checkboxes.py`, `scripts/open_prs.py`, `scripts/move_final.py`) und CI-Workflows zur Qualitätskontrolle.

## Installation & Nutzung
```bash
git clone https://github.com/heifra/marketing-assistant-framework.git
cd marketing-assistant-framework
# optional: neues Repo initialisieren
git init && git checkout -b main
```

Die Struktur ist sofort lauffähig (nur Python-Standardbibliothek). Typische Aktionen:
- `python scripts/agent_run.py quickstart --type linkedin_post --topic "..." --audience "..." --voice "..." --promise "..."` erzeugt Quickstart-Artefakte.
- `python scripts/agent_run.py topic_init ...`, `variants`, `review`, `finalize`, `research` bilden den manuellen Redaktionsfluss.
- Templates unter `contexts/` und `agents/core/*.template.*` via `scripts/instantiate.py` mit Markenwerten befüllen, Secrets in `infra/secrets.example.env` hinterlegen (nicht committen).

GitHub Actions (.github/workflows/*.yml) können nach dem Hinterlegen der Secrets aktiviert werden, um Topic-Init, Varianten, Reviews, Quickstart, Research oder Publish-Schritte automatisiert auszulösen.
