import argparse
import re
import sys
from datetime import datetime

from logsmith import __version__, __description__
from logsmith.docs import (
    append_entry,
    ensure_folder,
    list_projects,
    today_str,
)
from logsmith.sheets import append_row, get_all_rows, get_worksheet, next_number


def cmd_log(args):
    ws = get_worksheet()
    num = next_number(ws)

    category = args.category.capitalize()
    description = args.description
    business_impact = args.impact or ""
    skill = args.skill or ""
    project = args.project or ""
    evidence = args.evidence or ""
    recognition = args.recognition or ""

    folder_name = project if project else None

    if project or category in ("Todo", "Project", "Learning"):
        folder = ensure_folder(folder_name, description)
        entry_parts = [f"### {today_str()}", f"**{category}:** {description}"]
        if business_impact:
            entry_parts.append(f"\n**Impact:** {business_impact}")
        if skill:
            entry_parts.append(f"\n**Skill:** {skill}")
        if recognition:
            entry_parts.append(f"\n**Recognition:** {recognition}")
        entry = "\n".join(entry_parts)

        if category in ("Obstacle", "Blocker"):
            append_entry(folder, "obstacle.md", entry)
        elif category in ("Learning", "Skill"):
            append_entry(folder, "learning.md", entry)
        elif category in ("Achievement", "Milestone"):
            append_entry(folder, "progress.md", entry)

    row = [
        str(num),
        today_str(),
        category,
        description,
        business_impact,
        skill,
        folder_name if (project or category in ("Todo", "Project", "Learning")) else "",
        evidence,
        recognition,
    ]
    append_row(ws, row)

    print(f"[{category}] {description}")
    if business_impact:
        print(f"  Impact: {business_impact}")
    if skill:
        print(f"  Skill: {skill}")
    if evidence:
        print(f"  Evidence: {evidence}")
    return 0


def cmd_todo(args):
    ws = get_worksheet()
    num = next_number(ws)

    description = args.description
    priority = args.priority or "Medium"
    skill = args.skill or ""
    evidence = args.evidence or ""
    project = args.project or None

    if project:
        folder_name = project
    else:
        safe = re.sub(r"[^a-zA-Z0-9\s-]", "", description)[:40]
        folder_name = safe.strip().replace(" ", "-").lower()
        date_str = datetime.now().strftime("%d%b%y")
        folder_name = f"{folder_name}-{date_str}"

    folder = ensure_folder(folder_name, description)
    folder_todo = folder / "todo.md"
    folder_todo.write_text(
        f"# Todo — {description}\n\n"
        f"- **Created:** {today_str()}\n"
        f"- **Status:** In Progress\n"
        f"- **Priority:** {priority}\n\n"
        f"## Description\n{description}\n",
        encoding="utf-8",
    )

    row = [
        str(num),
        today_str(),
        "Todo",
        description,
        "",
        skill,
        folder_name,
        evidence,
        "",
    ]
    append_row(ws, row)

    print(f"[Todo] {description}")
    if skill:
        print(f"  Skill: {skill}")
    return 0


def cmd_progress(args):
    if not args.project:
        projects = list_projects()
        if not projects:
            print("No projects found. Create a todo first.")
            return 1
        print("Available projects:")
        for name, status in projects:
            print(f"  - {name} ({status})")
        print("\nUse --project to specify one.")
        return 1
    args.category = "Achievement"
    return cmd_log(args)


def cmd_obstacle(args):
    if not args.project:
        projects = list_projects()
        if not projects:
            print("No projects found. Create a todo first.")
            return 1
        print("Available projects:")
        for name, status in projects:
            print(f"  - {name} ({status})")
        print("\nUse --project to specify one.")
        return 1
    args.category = "Obstacle"
    return cmd_log(args)


def cmd_list(args):
    ws = get_worksheet()
    all_rows = get_all_rows(ws)

    if len(all_rows) <= 1:
        print("No entries yet.")
        return 0

    headers = all_rows[0]
    rows = all_rows[1:]

    if args.project:
        try:
            proj_idx = headers.index("Project")
        except ValueError:
            proj_idx = 6
        rows = [r for r in rows if len(r) > proj_idx and r[proj_idx] == args.project]
        if not rows:
            print(f"No entries for project '{args.project}'")
            return 0

    print(f"{'#':<3} {'Date':<12} {'Category':<14} {'Description':<50} {'Impact':<35} {'Project':<20}")
    print("-" * 140)
    for r in rows:
        num = r[0] if len(r) > 0 else ""
        date = r[1] if len(r) > 1 else ""
        cat = r[2] if len(r) > 2 else ""
        desc = r[3][:48] if len(r) > 3 else ""
        impact = r[4][:33] if len(r) > 4 else ""
        proj = r[6][:18] if len(r) > 6 else ""
        print(f"{num:<3} {date:<12} {cat:<14} {desc:<50} {impact:<35} {proj:<20}")

    projects_dirs = list_projects()
    if projects_dirs:
        print(f"\n--- Projects ({len(projects_dirs)}) ---")
        for name, status in projects_dirs:
            print(f"  {name} — {status}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="logsmith",
        description=f"{__description__} v{__version__}",
    )
    sub = parser.add_subparsers(dest="command")

    p_log = sub.add_parser("log", help="Log any entry (achievement, blocker, learning, etc.)")
    p_log.add_argument(
        "category",
        choices=["Achievement", "Blocker", "Learning", "Leadership", "Milestone", "Todo", "Project"],
        help="Entry category",
    )
    p_log.add_argument("description", help="Results-driven description")
    p_log.add_argument("--impact", help="Business impact — quantifiable result")
    p_log.add_argument("--skill", help='Skill or competency (e.g. "Stakeholder Management")')
    p_log.add_argument("--project", help="Link to existing project folder")
    p_log.add_argument("--evidence", help="URL or reference")
    p_log.add_argument("--recognition", help="Feedback, award, or shoutout")

    p_todo = sub.add_parser("todo", help="Create a new project/task")
    p_todo.add_argument("description", help="Task description")
    p_todo.add_argument("--priority", choices=["Low", "Medium", "High", "Critical"], default="Medium")
    p_todo.add_argument("--skill", help="Skill demonstrated")
    p_todo.add_argument("--project", help="Project folder name (auto-generated if omitted)")
    p_todo.add_argument("--evidence", help="URL or reference")

    p_progress = sub.add_parser("progress", help="Log progress on an existing project")
    p_progress.add_argument("description", help="Results-driven progress description")
    p_progress.add_argument("--project", required=True, help="Project folder name")
    p_progress.add_argument("--impact", help="Business impact")
    p_progress.add_argument("--skill", help="Skill demonstrated")
    p_progress.add_argument("--evidence", help="URL or reference")
    p_progress.add_argument("--recognition", help="Feedback or shoutout")

    p_obstacle = sub.add_parser("obstacle", help="Log an obstacle on a project")
    p_obstacle.add_argument("description", help="Blocker description")
    p_obstacle.add_argument("--project", required=True, help="Project folder name")
    p_obstacle.add_argument("--impact", help="What this blocks")
    p_obstacle.add_argument("--skill", help="Skill demonstrated")
    p_obstacle.add_argument("--evidence", help="URL or reference")

    p_list = sub.add_parser("list", help="Show entries and projects")
    p_list.add_argument("--project", help="Filter by project folder name")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 1

    cmds = {
        "log": cmd_log,
        "todo": cmd_todo,
        "progress": cmd_progress,
        "obstacle": cmd_obstacle,
        "list": cmd_list,
    }
    return cmds[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
