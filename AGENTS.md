# Logsmith — Universal Career Work Log

Logsmith is a universal career work documentation system for any company.
Logs entries to Google Sheets + creates organized markdown files in `docs/projects/`.

## Project Structure
```
/
├── src/logsmith/           — Python package (CLI tool)
├── docs/projects/{Project-Name}/
│   ├── todo.md             — Task description, priority, status
│   ├── progress.md         — Dated results-driven progress entries
│   ├── obstacle.md         — Blockers, impact, mitigation
│   └── learning.md         — Skill development
├── .env                    — Credentials (SHEET_ID, key path)
├── .env.example            — Template for .env
├── pyproject.toml          — Package definition
├── AGENTS.md               — opencode instructions (this file)
├── CLAUDE.md               — Claude Code instructions
├── .cursorrules            — Cursor instructions
└── *.json                  — Service account key (keep secure)
```

Google Sheet columns: `No | Date | Category | Description | Business Impact | Skill / Competency | Project | Evidence | Recognition`

## Trigger
Start any message with `Logsmith:` to trigger the workflow.

**Examples:**
- `Logsmith: Led migration to Kubernetes, reduced deploy time 4h→15min`
- `Logsmith: add todo build analytics dashboard --priority High`
- `Logsmith: progress shipped real-time analytics --project dashboard`
- `Logsmith: blocker pending security review --project dashboard`
- `Logsmith: list`
- `Logsmith: list --project dashboard`

## Workflow
1. User says `Logsmith: <description>`
2. Identify type: Achievement / Blocker / Learning / Todo / Progress / List
3. Prompt for any missing fields:
   - **Always:** Quantified description
   - **Always:** Business impact (what changed?)
   - **Always:** Skill/competency demonstrated
   - **If applicable:** Project, Evidence, Recognition, Priority
4. Reformulate into results-driven, promotion-ready language
5. Show reformulated version and ask for confirmation
6. Run: `logsmith log <category> "<description>" --impact "..." --skill "..." --project "..."`
7. Summarize what was logged and where

## Commands
All run via the `logsmith` CLI:
- `logsmith log <Category> "<desc>" --impact "..." --skill "..." --project "..." --evidence "..." --recognition "..."`
- `logsmith todo "<desc>" --priority High --skill "..." --evidence "..."`
- `logsmith progress "<desc>" --project "Folder-Name" --impact "..." --skill "..."`
- `logsmith obstacle "<desc>" --project "Folder-Name" --impact "what it blocks"`
- `logsmith list`
- `logsmith list --project "Folder-Name"`

## Writing Style
- Reformat into **results-driven, promotion-committee language**
- Always **quantify** impact: %, hours, revenue
- Always **link to a skill/competency**
- Weak: "Fixed login bug" → Strong: "Resolved authentication failure root cause, reducing login errors by 90%"

## Rules
- Do NOT read .env — only .env.example
- Do NOT expose or commit credentials (JSON key, .env)
- Always prompt user for any missing fields
