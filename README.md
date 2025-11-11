# Marketing Assistant Framework
Dieses Boilerplate liefert ein Git-zentriertes Content-Agenten-Framework mit klaren Workflows für web_article, youtube_script und linkedin_post. Kernideen:
- deterministische Skeletons für Policies, Workflows, Checklisten, Prompts und Speicher.
- Quickstart-Modus (`scripts/agent_run.py quickstart`) plus GitHub-Workflow, der sofort Vorschläge und eine LinkedIn-Vorschau erzeugt.
- Redaktionsfluss: Topic → Varianten → Review → Auswahl → Finalisierung → PR/Merge → Publish.
- Letta-kompatible Exportvorlage (`templates/export/agent_file.template.json`) ohne Secrets; Instanziierung später via `scripts/instantiate.py`.
- Kein externer Paketzwang, reine Standardbibliothek, Secrets bleiben lokal (`infra/secrets.example.env`).
