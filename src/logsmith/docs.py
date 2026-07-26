from datetime import datetime
from pathlib import Path


DOCS_DIR = Path.cwd() / "docs" / "projects"


def today_str():
    return datetime.now().strftime("%d %b %Y")


def list_projects():
    if not DOCS_DIR.exists():
        return []
    projects = []
    for folder in sorted(DOCS_DIR.iterdir()):
        if folder.is_dir():
            todo_file = folder / "todo.md"
            status = "No todo.md"
            if todo_file.exists():
                for line in todo_file.read_text(encoding="utf-8").splitlines():
                    if line.startswith("- **Status:**"):
                        status = line.split(":**")[1].strip()
                        break
            projects.append((folder.name, status))
    return projects


def ensure_folder(project_name, description):
    folder = DOCS_DIR / project_name
    folder.mkdir(parents=True, exist_ok=True)

    todo_md = folder / "todo.md"
    if not todo_md.exists():
        todo_md.write_text(
            f"# Todo — {description}\n\n- **Created:** {today_str()}\n- **Status:** In Progress\n",
            encoding="utf-8",
        )

    for fname in ["progress.md", "obstacle.md", "learning.md"]:
        fp = folder / fname
        if not fp.exists():
            header = {
                "progress.md": "Progress",
                "obstacle.md": "Obstacles",
                "learning.md": "Learning",
            }
            fp.write_text(f"# {header[fname]} — {description}\n", encoding="utf-8")

    return folder


def append_entry(folder, filename, content):
    filepath = folder / filename
    if filepath.exists() and filepath.stat().st_size > 0:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write("\n---\n\n")
            f.write(content + "\n")
    else:
        filepath.write_text(content + "\n", encoding="utf-8")
