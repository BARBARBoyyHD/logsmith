```
██╗      ██████╗  ██████╗ ███████╗███╗   ███╗██╗████████╗██╗  ██╗
██║     ██╔═══██╗██╔════╝ ██╔════╝████╗ ████║██║╚══██╔══╝██║  ██║
██║     ██║   ██║██║  ███╗███████╗██╔████╔██║██║   ██║   ███████║
██║     ██║   ██║██║   ██║╚════██║██║╚██╔╝██║██║   ██║   ██╔══██║
███████╗╚██████╔╝╚██████╔╝███████║██║ ╚═╝ ██║██║   ██║   ██║  ██║
╚══════╝ ╚═════╝  ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝

             ⚒ Forge Your Work History ⚒
```

**Logsmith** is a universal career work documentation system. It logs your achievements, blockers, learning, and todos to **Google Sheets** while simultaneously creating organized **markdown files** in `docs/projects/`.

Built for career progression — every entry captures **impact**, **skills**, and **recognition** so you're always promotion-ready.

Works with any AI coding agent (opencode, Claude Code, Cursor, etc.).

---

## Features

- **Google Sheets integration** — entries auto-appended to monthly tabs
- **Local markdown docs** — `docs/projects/{project-name}/` with `todo.md`, `progress.md`, `obstacle.md`, `learning.md`
- **AI-agent ready** — works with opencode, Claude Code, Cursor out of the box
- **Promotion-focused** — forces quantified impact + skill tagging on every entry

---

## Installation

```bash
pip install git+https://github.com/BARBARBoyyHD/logsmith.git
```

Or clone for development:

```bash
git clone https://github.com/BARBARBoyyHD/logsmith.git
cd logsmith
pip install -e .
```

### Updating

```bash
cd logsmith           # or wherever you cloned it
git pull
# pip install -e .    # only needed if dependencies changed
```

When installed with `-e` (editable), pip links directly to your repo.
A `git pull` immediately updates the CLI — no reinstall needed unless
new dependencies were added.

### Dependencies

- Python 3.10+
- Google Cloud project with [Sheets API enabled](https://console.cloud.google.com/apis/library/sheets.googleapis.com)
- A Google Sheet to log into

---

## Setup

### 1. Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. **Enable** the Google Sheets API
3. Create a **Service Account** and download its **JSON key**
4. Create a **Google Sheet**, copy its ID from the URL
5. **Share** the sheet with your service account email (Editor)

### 2. Configure

```bash
cp .env.example .env
```

Edit `.env`:

```env
SHEET_ID=your_google_sheet_id_here
SERVICE_ACCOUNT_KEY_PATH=path/to/your-service-account-key.json
```

Or just drop the JSON key in the project root — Logsmith will find it automatically.

---

## Usage

```bash
logsmith --help
```

### Log an achievement
```bash
logsmith log Achievement "Reduced deploy time from 4h to 15min" \
  --impact "Saved 120 engineering hours per month" \
  --skill "Technical Leadership" \
  --project "cicd-migration" \
  --evidence "https://github.com/org/repo/pull/42" \
  --recognition "CTO shoutout Q3"
```

### Start a new task
```bash
logsmith todo "Build analytics dashboard" --priority High --skill "Data Engineering"
```

### Log progress
```bash
logsmith progress "Shipped real-time analytics, query latency -85%" \
  --project "analytics-dashboard" \
  --impact "Saved 40h/week in manual reporting"
```

### Log a blocker
```bash
logsmith obstacle "Pending security review from compliance" \
  --project "analytics-dashboard" \
  --impact "Blocks production deployment by 1 week"
```

### View entries
```bash
logsmith list
logsmith list --project "analytics-dashboard"
```

### Categories

`Achievement` | `Blocker` | `Learning` | `Leadership` | `Milestone` | `Todo`

---

## Google Sheet Columns

| Column | Description | Example |
|---|---|---|
| `No` | Auto-numbered | 1 |
| `Date` | Auto-filled | 26 Jul 2026 |
| `Category` | Entry type | Achievement |
| `Description` | Results-driven summary | Reduced login errors by 90% |
| `Business Impact` | Quantified value | Saved 40h/week manual work |
| `Skill / Competency` | Promotion-relevant skill | Stakeholder Management |
| `Project` | Links to docs/projects/ | cicd-migration |
| `Evidence` | PR, ticket, deck URL | https://github.com/... |
| `Recognition` | Feedback, awards | Best initiative — CTO |

---

## Writing for Promotion

Write every entry as if it's going to your promotion committee:

| Instead of | Write |
|---|---|
| "Fixed login bug" | "Resolved auth failure root cause, reducing login errors by 90% and improving onboarding from 60% to 95%" |
| "Learned Kubernetes" | "Completed CKA, led migration of 3 services to K8s, reducing deploy failures by 70%" |
| "Waiting for API key" | "Pending API credentials from client IT, escalated to PM, unblocked via mock env" |

---

## AI Agent Integration

Logsmith works with any AI coding agent. Just start your message with `Logsmith:`.

### opencode

Add to `opencode.json`:

```json
{
  "skills": {
    "google-sheets-log": {
      "path": ".agents/skills/google-sheets-log"
    }
  }
}
```

### Claude Code / Cursor

Copy `AGENTS.md` or `CLAUDE.md` / `.cursorrules` into your project root.

---

## Project Structure

```
├── src/logsmith/
│   ├── __init__.py        — Package metadata
│   ├── __main__.py        — python -m logsmith support
│   ├── cli.py             — All CLI commands
│   ├── sheets.py          — Google Sheets operations
│   ├── docs.py            — Markdown file management
│   └── config.py          — Environment config loading
├── docs/projects/         — Your project logs (gitignored)
├── pyproject.toml         — Package definition
├── LICENSE                — MIT
└── README.md              — This file
```

---

```
  ╔══════════════════════════════════════════════════════╗
  ║   Forge your career, one entry at a time.     ⚒    ║
  ╚══════════════════════════════════════════════════════╝
```
