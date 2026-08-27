# Schema — .reversa/state.json

This file persists the complete analysis state between sessions. Reversa reads and writes to this file.

## Complete structure

```json
{
  "version": "1.0.0",
  "project": "nome-do-projeto",
  "user_name": "Nome do Usuário",
  "chat_language": "pt-br",
  "doc_language": "Português",
  "answer_mode": "chat",
  "doc_level": null,
  "output_folder": "_reversa_sdd",
  "phase": "reconhecimento",
  "completed": ["reconhecimento"],
  "pending": ["escavacao", "interpretacao", "geracao", "revisao"],
  "engines": ["claude-code"],
  "agents": ["reversa", "reversa-scout", "reversa-archaeologist"],
  "checkpoints": {
    "scout": {
      "completed_at": "2026-04-26T10:00:00Z",
      "files": [
        "_reversa_sdd/inventory.md",
        "_reversa_sdd/dependencies.md",
        ".reversa/context/surface.json"
      ]
    },
    "archaeologist": {
      "completed_at": "2026-04-26T11:00:00Z",
      "modules_analyzed": ["auth", "orders", "payments"],
      "files": [
        "_reversa_sdd/code-analysis.md",
        "_reversa_sdd/data-dictionary.md",
        ".reversa/context/modules.json"
      ]
    }
  },
  "created_files": [
    "CLAUDE.md",
    ".agents/skills/reversa/SKILL.md",
    ".reversa/state.json",
    ".reversa/plan.md"
  ]
}
```

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Installed Reversa version |
| `project` | string | Legacy project name |
| `user_name` | string | User name (for interactions) |
| `chat_language` | string | Interaction language (e.g., pt-br, en-us) |
| `doc_language` | string | Language of generated specs (e.g., Português, English) |
| `answer_mode` | string | How the user responds to gaps: `chat` or `file` |
| `doc_level` | string \| null | Volume of generated documentation: `essencial`, `completo`, or `detalhado`. Starts as `null` — must be filled via user choice after the Scout. |
| `output_folder` | string | Specs output folder (default: `_reversa_sdd`) |
| `phase` | string \| null | Current phase. `null` = not started |
| `completed` | string[] | Completed phases |
| `pending` | string[] | Pending phases |
| `checkpoints` | object | Completion record for each agent |
| `engines` | string[] | Configured engines (e.g., `["claude-code", "codex"]`) |
| `agents` | string[] | Installed agents |
| `created_files` | string[] | All files created by Reversa (for safe uninstall) |

## Valid phases

`reconhecimento` → `escavacao` → `interpretacao` → `geracao` → `revisao`

## Writing rule

Never remove existing fields. Only add or update.

## Where NOT to write

The specs organization decision (granularity, custom folders, Scout's original suggestion, choice timestamp) does **not** go in `state.json`. It is persisted in `.reversa/config.toml`, section `[specs]`, per `references/step-03-specs-organization.md`. `state.json` is runtime state; `config.toml` is a long-term decision.
