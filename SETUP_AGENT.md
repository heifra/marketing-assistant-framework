# Setup Agent
1. Nutze den separaten Setup-Prompt, um Markenvariablen auszufüllen und Dateien aus `contexts/*.template.*` zu instanziieren.
2. Führe `python scripts/instantiate.py <template> <output> --var BRAND=<Name>` usw. aus, erstelle danach `templates/export/agent_file.template.json` als `<brand>.agent.json` im `templates/export`-Ordner.
3. Hinterlege LLM- und MCP-Bindings in `agents/core/llm_backends.template.yaml` und `agents/core/tools.mcp.template.yaml`, ohne Secrets zu committen.
4. Prüfe Policies, Knowledge und Setup-Checklist (`setup/checklist.md`), bevor Assets nach Letta importiert werden.
