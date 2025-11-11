# Review Prompt – Editorial QA
Bewerte Titel- und Draft-Varianten für ein IT/AI-SME-Piece anhand `agents/core/eval/review_rubric.md`.

## Vorgehen
1. Lies `variant_doc` (Titel + Drafts) und optionalen `review_rubric`.  
2. Für jede Variante Scores 0–5 auf Kriterien: Interesse, Mehrwert, Differenzierung, Plattformpotenzial, Markenfit.  
3. Prüfe zudem:  
   - passt Problemstellung zu SME-Realität (Budget, Teamgröße, Tool-Stack)?  
   - benanntes Outcome messbar?  
   - AI/IT-Terminologie korrekt und frei von Hype?  
4. Gib Begründungen mit Zitaten aus dem Text.

## Ausgabe
JSON in ```json Block:
```json
{
  "variants": [
    {
      "id": "title-1",
      "scores": { "interesse": 4, "mehrwert": 5, "differenzierung": 4, "plattform": 4, "markenfit": 5 },
      "strengths": [],
      "risks": [],
      "recommendation": "best|revise|reject"
    }
  ],
  "best_pick": "title-3",
  "next_steps": [
    "Ergänze konkreten KPI für Servicekosten.",
    "Vermeide Vendor-Lock wording."
  ]
}
```

Gate: Gesamtscore ≥18. Wenn keine Variante besteht, schlage alternative Perspektive + Research-Need vor.
