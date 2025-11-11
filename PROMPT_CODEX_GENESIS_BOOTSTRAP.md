# SYSTEM
Arbeite lokal in VS Code. Erzeuge ein vollständiges, neutrales Boilerplate für ein Git-zentriertes Content-Agenten-Framework.
Ziele:
- Qualität und Automatisierung.
- Inhaltstypen: web_article, youtube_script, linkedin_post.
- Redaktionsfluss in Git: Topic → Varianten (N Titel, 3 Kurz-Drafts) → Review-Agent → Auswahl → Final → PR/Merge → Publish.
- Leichte Snapshot/Knowledge-Schicht. Kein schweres RAG.
- Quickstart: sofort Vorschlag + LinkedIn-Preview als .md.
- Letta-Kompatibilität: exportierbares Agent-File (ohne Secrets).
- Deterministische Skeletons. Keine externen Abhängigkeiten installieren. Keine Secrets committen.
Wenn etwas unklar ist, stelle 1 kurze Rückfrage und fahre fort. Nach Erstellung: YAML/JSON prüfen, Git init, erster Commit.

# VARIABLEN (Platzhalter beibehalten)
BRAND_PLACEHOLDER=${BRAND}
PRIMARY_MODEL=${PRIMARY_MODEL}
FACTCHECK_MODEL=${FACTCHECK_MODEL}
REVIEW_MODEL=${REVIEW_MODEL}
LOCAL_FALLBACK=${LOCAL_FALLBACK}
LOCAL_BASE_URL=${LOCAL_BASE_URL}
WEBSEARCH_MCP=${WEBSEARCH_MCP}
WP_IMPORT=${WP_IMPORT}

# AUFGABE
Erzeuge exakt folgende Struktur und fülle alle Dateien mit funktionsfähigen Skeletons.

## 1) Ordnerstruktur
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

## 2) Inhalte schreiben (kompakt, vollständig)

### agents/core/policies.md
- Quellenpflicht für Zahlen/Studien. Keine Heilsversprechen. Keine Diagnosen.
- Keine Clickbait-Titel. Transparente Claims.
- Plattform-Hinweise: Web mit Quellen, YouTube ohne Heilsversprechen, LinkedIn knapp und klar.

### agents/core/writing_checklist.md
- Hook, Nutzen, klare Struktur, Beispiele, CTA, interne Links.
- Aktive Sprache, präzise Aussagen, keine Übertreibungen.
- Frontmatter vollständig (title, slug, meta, tags).

### agents/core/seo_checklist.md
- Title ≤ 60, Meta ≤ 155. Genau 1×H1. H2/H3 decken Keywords.
- Alt-Texte, interner Link mindestens 1, Slug sauber.

### agents/core/eval_rubrics.md
- Fakten A–C, Lesbarkeit Flesch 50–70, Markenfit 100 %, SEO erfüllt.
- Gate: Summe ≥ 18/25.

### agents/core/tools.mcp.template.yaml  [YAML-Beispiel]
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
  # optional:
  - id: embed_search
    provider: local-emb
    path: "cache/embeddings/"
  - id: image_generate
    provider: imggen-mcp
    caps: ["text2image","variations"]

### agents/core/llm_backends.template.yaml  [YAML-Beispiel]
default:        { model: ${PRIMARY_MODEL},   temperature: 0.3, max_tokens: 2800 }
factcheck:      { model: ${FACTCHECK_MODEL}, temperature: 0.1 }
review:         { model: ${REVIEW_MODEL},    temperature: 0.2 }
rewrite:        { model: gpt-4o-mini,        temperature: 0.2 }
local_fallback: { model: ${LOCAL_FALLBACK},  base_url: ${LOCAL_BASE_URL} }

### agents/core/memory_schema.md
Felder dokumentieren:
- voice.attributes, voice.banned_phrases
- audience.personas, audience.reading_level
- claims_policy.requires_citation=true, allowed_evidence z. B. peer_review, gov, ngo
- content_history: store=vector+kv, keys=[title, slug, date, topics, entities]
- facts_knowledge.sources: curated_markdown → contexts/facts_knowledge.template.md
Keine PII. Keine Keys.

### agents/core/workflows/wordpress.blog.yaml  [YAML-Beispiel]
id: blog_v1
stages:
  - id: gather_context
    tools: [snapshot_lookup]
    fallback_tools: [chrome_fetch]
    outputs: [context.md]
  - id: ideation
    prompt: agents/core/prompts/plan_prompt.md
    inputs: [brief, topic_map, entity_glossary, context.md]
    outputs: [title_options, outline, key_claims]
    tools: [web_search]
    guards: [e_e_a_t_gate]
  - id: drafting
    prompt: agents/core/prompts/draft_prompt.md
    inputs: [outline, key_claims]
    outputs: [draft_v1.md]
  - id: refinement
    prompt: agents/core/prompts/refine_prompt.md
    inputs: [draft_v1.md, agents/core/seo_checklist.md, agents/core/writing_checklist.md]
    outputs: [draft_v2.md, seo_meta.json]
    tools: [readability_score]
  - id: factcheck
    prompt: agents/core/prompts/factcheck_prompt.md
    inputs: [draft_v2.md]
    outputs: [draft_v3.md, citations.md]
    tools: [web_search, citation_builder]
  - id: finalize
    prompt: agents/core/prompts/meta_prompt.md
    inputs: [draft_v3.md]
    outputs: [post.md, post.frontmatter.yaml, images.prompts.yaml]
publishing:
  target: github
  paths:
    draft: content/drafts/${BRAND_PLACEHOLDER}/blog/{slug}.md
    final: content/approved/${BRAND_PLACEHOLDER}/blog/{date}-{slug}.md

### agents/core/workflows/linkedin.post.yaml  [kurz]
id: linkedin_post_v1
stages:
  - id: plan
    prompt: agents/core/prompts/plan_prompt.md
    inputs: [brief]
    outputs: [title_options]
  - id: draft
    prompt: agents/core/prompts/draft_prompt.md
    inputs: [title_options]
    outputs: [post.md]
publishing:
  target: github
  paths:
    draft: content/drafts/${BRAND_PLACEHOLDER}/social/{slug}.md
    final: content/approved/${BRAND_PLACEHOLDER}/social/{date}-{slug}.md

### agents/core/workflows/youtube.script.yaml  [kurz]
id: youtube_script_v1
stages:
  - id: outline
    prompt: agents/core/prompts/plan_prompt.md
    inputs: [brief]
    outputs: [outline]
  - id: script
    prompt: agents/core/prompts/draft_prompt.md
    inputs: [outline]
    outputs: [script.md, beats.json]
publishing:
  target: github
  paths:
    draft: content/drafts/${BRAND_PLACEHOLDER}/youtube/{slug}.md
    final: content/approved/${BRAND_PLACEHOLDER}/youtube/{date}-{slug}.md

### agents/core/workflows/wordpress.landing.yaml  [kurz]
id: landing_v1
stages:
  - id: structure
    prompt: agents/core/prompts/plan_prompt.md
    inputs: [brief]
    outputs: [sections]
  - id: copy
    prompt: agents/core/prompts/draft_prompt.md
    inputs: [sections]
    outputs: [landing.md, hero_copy.md]

### agents/core/prompts/plan_prompt.md
Ziel: 6 Titelvarianten, Outline (H2/H3), Key-Claims mit Quellenhinweis.
Input: brief (+ optional topic_map, entity_glossary, context.md).
Output: ein JSON in Codeblock mit Feldern titles[], outline[], claims[].
Tabus: Heilsversprechen, Clickbait.

### agents/core/prompts/draft_prompt.md
Ziel: Draft mit Hook, Kontext, 2–3 Kernpunkten, Beispielen, Fazit, CTA.
Meta Description ≤155, 5 Keywords, Slug-Vorschlag.

### agents/core/prompts/refine_prompt.md
Ziel: Kürzen, Lesbarkeit, SEO-Checklist anwenden, interne Links vorschlagen.

### agents/core/prompts/factcheck_prompt.md
Ziel: falsifizierbare Claims prüfen, Quelle + Domainklasse erzwingen.

### agents/core/prompts/meta_prompt.md
Ziel: Frontmatter (title, slug, date, tags, summary) erzeugen, kompatibel zu WP Frontmatter.

### agents/core/prompts/review_prompt.md
Ziel: Titel + Kurz-Drafts bewerten nach eval/review_rubric.md. JSON mit Scores, Begründungen, Empfehlung.

### agents/core/eval/review_rubric.md
Kriterien 0–5: Interesse, Mehrwert, Differenzierung, Plattformpotenzial, Markenfit. Gate ≥18.

### contexts/*.template.*
- brand_profile.template.md: ${BRAND}, Ziel, Audience, Voice-Attribute.
- voice_guide.template.md: Do/Don’t-Beispiele, Satzrhythmus, Tonalität.
- style_guide.template.md: Terminologie, Formatierungen, Verbotsliste.
- topic_map.template.yaml: Themencluster mit Priorität.
- entity_glossary.template.yaml: Begriffe, Synonyme, verbotene Phrasen.
- facts_knowledge.template.md: kuratierte Fakten mit Platzhalter-Quellen.
- cms_mapping.template.yaml: WP_IMPORT Platzhalter, Feldmapping.

### templates/planning/*.md
- topic_init.md: Frontmatter {type, brief, url, keywords}; Abschnitt „Thema“.
- variants.md: 6 Checkbox-Titel, 3 Kurz-Drafts A/B/C (Checkboxen).
- selection.md: gewählter Titel, gewählter Draft, Hinweisfelder.
- review_checklist.md: Fakten, Voice, SEO, Compliance, interne Links.

### templates/export/agent_file.template.json  [JSON-Skeleton]
{
  "agent_name": "${BRAND_PLACEHOLDER}-content-agent",
  "workflows_dir": "agents/core/workflows",
  "prompts_dir": "agents/core/prompts",
  "eval_dir": "agents/core/eval",
  "contexts_dir": "agents/brand",
  "llm_config": "agents/core/llm_backends.yaml",
  "tools_config": "agents/core/tools.mcp.yaml",
  "memory_doc": "agents/core/memory_schema.md",
  "policies": "agents/core/policies.md",
  "checklists": ["agents/core/writing_checklist.md","agents/core/seo_checklist.md","agents/core/eval_rubrics.md"]
}

### planning/cadence.template.yaml  [YAML-Beispiel]
frequency: weekly
day_of_week: Mon
variants:
  titles_per_topic: 6
  short_drafts_per_topic: 3
content_plan:
  web_article: 2
  youtube_script: 1
  linkedin_post: 1

### planning/quickstart/README.md
Erläutere Quickstart-Inputs (type, topic, audience, voice, promise, source) und Outputs:
- planning/quickstart/proposal.md
- content/drafts/<type>/preview.md
- images/prompts/preview.yaml

### knowledge/facts_knowledge.md
Neutraler Start mit 3 Beispielpunkten und Platzhalter-Quellen.

### sources/*
- extractor.rules.yaml: include-/exclude-Beispiele, main_selector, title_selector, slug_from.
- sitemap.seed.txt: leer mit Kommentar.
- allowlist.txt: Domains je nach Projekt ergänzen.

### cache/kv.json
{}

### scripts/agent_run.py  (deterministische Skeleton-CLI, keine Netzaufrufe)
- Subcommands: quickstart | topic_init | variants | review | finalize | research
- quickstart: nimmt type, topic, audience, voice, promise, source; schreibt:
  - planning/quickstart/proposal.md (4 Titel, 3 Kurz-Drafts mit kurzen Begründungen)
  - content/drafts/<type>/preview.md (LinkedIn-Post 140–220 Wörter mit Frontmatter)
  - images/prompts/preview.yaml (2–4 Bildprompt-Kandidaten)
- topic_init: erstellt planning/topics/<WEEK>-<ID>.md aus Template-Platzhaltern.
- variants: erzeugt planning/variants/<ID>.md mit 6 Titeln + 3 Kurz-Drafts (Dummytexte).
- review: schreibt planning/reviews/<ID>.md mit fiktiven Scores (Schema aus review_rubric.md).
- finalize: erstellt content/drafts/<type>/<slug>.md mit Frontmatter.
- research: legt knowledge/research/<mode>/<stamp>.md mit Platzhalter-Insights an.

### scripts/parse_checkboxes.py
Liest Checkboxen aus variants.md, prüft vorhandenes Review-File mit gate_pass:true, erzeugt planning/selected/<ID>.md.

### scripts/open_prs.py
Schreibt PR-README in content/drafts/* als Platzhalter (kein API-Call).

### scripts/move_final.py
Simuliert Verschieben von drafts → approved.

### scripts/derive_slug.py
Erzeugt URL-Slug aus Titel (lowercase, minus, nur a-z0-9-).

### scripts/instantiate.py
Ersetzt Variablen aus contexts-Templates in reale Dateien (spätere Instanzen).

### .github/workflows/topic_init.yml  [YAML-Beispiel]
name: topic_init
on:
  workflow_dispatch:
    inputs:
      type: { description: "web_article|youtube_script|linkedin_post", required: true }
      brief: { description: "Kurzbriefing", required: true }
      url: { description: "Optionale Quelle", required: false }
      keywords: { description: "Komma-getrennt", required: false }
jobs:
  init:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          mkdir -p planning/topics
          python scripts/agent_run.py topic_init --type "${{ github.event.inputs.type }}" \
            --brief "${{ github.event.inputs.brief }}" --url "${{ github.event.inputs.url }}" \
            --keywords "${{ github.event.inputs.keywords }}"

### .github/workflows/gen_variants.yml  [kurz]
name: gen_variants
on:
  push:
    paths: ["planning/topics/*.md"]
jobs:
  variants:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python scripts/agent_run.py variants

### .github/workflows/auto_review.yml  [kurz]
name: auto_review
on:
  push:
    paths: ["planning/variants/*.md"]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python scripts/agent_run.py review

### .github/workflows/selection_to_final.yml  [kurz]
name: selection_to_final
on:
  push:
    paths: ["planning/variants/*.md","planning/selected/*.md"]
jobs:
  finalize:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          python scripts/parse_checkboxes.py planning/variants --require-review planning/reviews
          python scripts/agent_run.py finalize
          python scripts/open_prs.py content/drafts planning/templates/review_checklist.md

### .github/workflows/weekly_research.yml  [kurz]
name: weekly_research
on:
  schedule: [{ cron: "0 6 * * 1" }]
jobs:
  research:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          python scripts/agent_run.py research --mode web_article
          python scripts/agent_run.py research --mode youtube_script
          python scripts/agent_run.py research --mode linkedin_post

### .github/workflows/publish.yml  [kurz]
name: publish
on:
  pull_request:
    types: [closed]
jobs:
  move_on_merge:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          python scripts/move_final.py
          git config user.name bot && git config user.email bot@local
          git add content/approved || true
          git commit -m "publish: finalize" || true
          git push || true

### .github/workflows/quickstart.yml  [YAML-Beispiel]
name: quickstart
on:
  workflow_dispatch:
    inputs:
      type:     { description: "linkedin_post|web_article|youtube_script", required: true }
      topic:    { description: "Thema 1 Satz", required: true }
      audience: { description: "Zielperson(a)", required: true }
      voice:    { description: "3 Adjektive", required: true }
      promise:  { description: "Kernversprechen", required: true }
      source:   { description: "Optionale URL", required: false }
jobs:
  gen_quickstart:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          python scripts/agent_run.py quickstart \
            --type "${{ github.event.inputs.type }}" \
            --topic "${{ github.event.inputs.topic }}" \
            --audience "${{ github.event.inputs.audience }}" \
            --voice "${{ github.event.inputs.voice }}" \
            --promise "${{ github.event.inputs.promise }}" \
            --source "${{ github.event.inputs.source }}"

### infra/secrets.example.env
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
SERPER_API_KEY=
OLLAMA_BASE_URL=${LOCAL_BASE_URL}

### infra/ci_publish.yaml
# optionaler Lint-Stub; bei fehlenden Tools still überspringen

### README.md
Kurzbeschreibung Boilerplate, Quickstart, Redaktionsfluss, Letta-Export, keine Secrets, Instanziierung später.

### SETUP_AGENT.md
Kurzanleitung für spätere Instanzen; verweist auf separaten Setup-Prompt, der Platzhalter füllt und export/<brand>.agent.json erzeugt.

### setup/state.json
{"brand":"${BRAND}","steps":{"brand_style":false,"policies":false,"knowledge":false,"llm_binding":false,"mcp_check":false,"letta_import":false},"last_run":null}

### setup/checklist.md
- [ ] Brand/Style definiert
- [ ] Policies ergänzt
- [ ] Knowledge initialisiert
- [ ] LLM/MCP Platzhalter gesetzt
- [ ] Letta Agent File erzeugt
- [ ] Import in Letta bestätigt

## 3) Quickstart sofort berücksichtigen
- scripts/agent_run.py enthält Subcommand `quickstart` wie oben.
- .github/workflows/quickstart.yml vorhanden.
- planning/quickstart/README.md erklärt Nutzung.

## 4) Git initialisieren und erster Commit
git init
git checkout -b main
git add .
git commit -m "chore: genesis boilerplate with quickstart"
# Remote und Push später manuell setzen.

## 5) Abschluss
Gib nach Erstellung einen kurzen Report mit Dateianzahl, wichtigsten Pfaden und „Nächste Schritte“ aus.
