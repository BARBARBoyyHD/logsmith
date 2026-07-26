# Logsmith — Claude Code Instructions

You are logging career documentation entries using **Logsmith**.

## How it works
- Every entry goes to **Google Sheets** + markdown files in `docs/projects/`
- All entries must be **results-driven, promotion-ready language**

## Trigger
Messages starting with `Logsmith:` trigger the logging workflow.

## Categories
`Achievement` | `Blocker` | `Learning` | `Leadership` | `Milestone` | `Todo`

## Commands
```
logsmith log <Category> "<description>" --impact "..." --skill "..." --project "..." --evidence "..." --recognition "..."
logsmith todo "<description>" --priority High --skill "..."
logsmith progress "<description>" --project "Folder-Name" --impact "..." --skill "..."
logsmith obstacle "<description>" --project "Folder-Name" --impact "what it blocks"
logsmith list
logsmith list --project "Folder-Name"
```

## Writing Rules
- Quantify everything: %, hours, revenue
- Tag every entry with a skill/competency
- Never read or expose .env or JSON key files
- Always confirm with user before running the command
