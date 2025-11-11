# SYSTEM
Arbeite lokal in VS Code. Erzeuge ein vollständiges, neutrales Boilerplate für ein Git-zentriertes Content-Agentenframework. Ziele:
- Hohe Qualität, Automatisierung, kein Fokus auf Geschwindigkeit.
- Inhaltstypen: web_article, youtube_script, linkedin_post.
- Redaktionsfluss in Git: Thema → Varianten (N Titel, 3 Kurz-Drafts) → Review-Agent → menschliche Auswahl → Final → PR/Merge → Publish.
- Keine großen RAG-Setups. Leichtes Snapshot/Knowledge. Optional Mini-Embeddings später.
- Quickstart: Sofort nach Bootstrap ein minimaler Vorschlag und ein fertiger LinkedIn-Preview als .md.
- Letta-Kompatibilität: Exportierbare Agent-Datei. LLM/MCP Keys werden später in Letta gesetzt.
- Keine Secrets ins Repo. Deterministische, lauffähige Skeletons.

Wenn etwas unklar ist, frage kurz, dann setze fort. Nach Erstellung testen: YAML/JSON Syntax, Ordnerstruktur, Referenzen. Git initialisieren, erster Commit. Keine fremden Abhängigkeiten installieren.

# VARIABLES  (Platzhalter beibehalten)
BRAND_PLACEHOLDER=${BRAND}
PRIMARY_MODEL=${PRIMARY_MODEL}
FACTCHECK_MODEL=${FACTCHECK_MODEL}
REVIEW_MODEL=${REVIEW_MODEL}
LOCAL_FALLBACK=${LOCAL_FALLBACK}
LOCAL_BASE_URL=${LOCAL_BASE_URL}
WEBSEARCH_MCP=${WEBSEARCH_MCP}
WP_IMPORT=${WP_IMPORT}

# OBJECTIVE
1) Erzeuge die folgende Struktur exakt:

agents/core/
  policies.md
  writing_checklist.md
  seo_checklist.md
  eval_rubrics.md
  tools.mcp.template.yaml
  llm_backends.template.yaml
  memory_schema.md
  workflows/
    linkedin.post.yaml
    youtube.script.yaml
    wordpress.landing.yaml
    wordpress.blog.yaml
  prompts/
    plan_prompt.md
    draft_prompt.md
    refine_prompt.md
    factcheck_prompt.md
    meta_prompt.md
    review_prompt.md
  eval/
    review_rubric.md
contexts/
  brand_profile.template.md
  voice_guide.template.md
  style_guide.template.md
  topic_map.template.yaml
  entity_glossary.template.yaml
  facts_knowledge.template.md
  cms_mapping.template.yaml
templates/
  planning/
    topic_init.md
    variants.md
    selection.md
    review_checklist.md
  export/
    agent_file.template.json
planning/
  cadence.template.yaml
  quickstart/
    README.md
knowledge/
  facts_knowledge.md
  research/
    web/
    youtube/
    linkedin/
sources/
  extractor.rules.yaml
  sitemap.seed.txt
  allowlist.txt
snapshots/
  pages/
  media/
cache/
  kv.json
  embeddings/
content/
  drafts/
  approved/
scripts/
  agent_run.py
  parse_checkboxes.py
  open_prs.py
  move_final.py
  derive_slug.py
  instantiate.py
.github/workflows/
  topic_init.yml
  gen_variants.yml
  auto_review.yml
  selection_to_final.yml
  weekly_research.yml
  publish.yml
  quickstart.yml
infra/
  secrets.example.env
  ci_publish.yaml
README.md
SETUP_AGENT.md
setup/
  state.json
  checklist.md

2) Fülle die Dateien mit funktionalen Skeletons.

agents/core/policies.md:
- Quellenpflicht für Zahlen und Studien.
- Keine Heilsversprechen. Keine Diagnosen. Transparente Claims.
- Keine Clickbait-Titel. LinkedIn ohne medizinische Beratung.
- Plattform-Compliance: Web mit Quellen, YouTube Skripte ohne Heilsversprechen, LinkedIn knapp und klar.

agents/core/writing_checklist.md:
- Klarer Hook, Nutzenversprechen, strukturierte Abschnitte, Beispiele, CTA, interne Links.
- Einheitlicher Ton, keine Übertreibung, aktive Sprache, konkrete Schritte.
- Frontmatter vollständig.

agents/core/seo_checklist.md:
- Title ≤ 60 Zeichen, Meta ≤ 155.
- Genau eine H1, H2/H3 decken Keywords.
- Alt-Texte, kanonische Links optional, Slug sauber.

agents/core/eval_rubrics.md:
- Fakten A–C, Lesbarkeit Flesch 50–70, Markenfit 100 %, SEO erfüllt.
- Gate: Summe ≥ 18 von 25.

agents/core/tools.mcp.template.yaml:
```yaml
tools:
  - id: web_search
    provider: ${WEBSEARCH_MCP}
    caps: ["query","topn:10"]
  - id: snapshot_lookup
    provider: local-kv
    path: "cache/kv.json"
  - id: chrome_fetch
    provider: mcp-chrome-devtools
  - id: readability_score
    provider: textstat
  - id: citation_builder
    provider: citeproc
  - id: image_prompt
    provider: imgprompt
  # optional aktivierbar:
  - id: embed_search
    provider: local-emb
    path: "cache/embeddings/"
  - id: image_generate
    provider: imggen-mcp
    caps: ["text2image","variations"]
