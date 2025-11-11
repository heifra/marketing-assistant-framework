# Meta Prompt – Publishing Package
Erzeuge finale Frontmatter + Publishing-Metadaten für ein SME-IT/AI-Stück.

## Pflichtfelder (YAML)
```
title: ""
slug: ""
date: YYYY-MM-DD
tags: [it-modernization, ai, sme, ...]
persona: ""
industry: ""
stage: awareness|consideration|decision
hero_metric: ""
cta:
  label: ""
  url: ""
summary: |
  2 Sätze, max. 320 Zeichen.
meta_description: ""
canonical_url: ""
```

## Zusätze
- `slug`: lowercase, `-`, keine Zahlenkolonnen, max. 8 Wörter.  
- `hero_metric`: Kennzahl, die Leser sofort messen kann (z. B. „<12h MTTR“).  
- `tags`: mind. 4, Mischung aus Technik (e.g. `rag-architecture`) und Business (`sme-ops`).  
- Füge `featured_image_prompt` Feld hinzu (1 Satz Visual-Idee).  
- Hänge JSON-Block mit `distribution`: channels (web, linkedin, newsletter), recommended publish day/time.
