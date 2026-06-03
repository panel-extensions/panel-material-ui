"""
Build markdown versions of docs and generate llms.txt with per-category index pages.

Run as part of the docs build pipeline:
    python scripts/build_llms_txt.py
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOC_DIR = ROOT / "doc"
REFERENCE_DIR = ROOT / "examples" / "reference"
BUILTDOCS_DIR = ROOT / "builtdocs"
OUTPUT_DIR = BUILTDOCS_DIR / "markdown"
MARKDOWN_BASE_URL = "/markdown"

SECTION_DESCRIPTIONS = {
    "how_to": "How-to guides for theming, styling, and customizing Panel Material UI apps",
    "tutorials": "Tutorials for getting started with Panel Material UI components",
}

REFERENCE_DESCRIPTIONS = {
    "widgets": "Interactive input widgets (Button, Select, Slider, TextInput, DatePicker, etc.)",
    "menus": "Navigation and menu components (Breadcrumbs, MenuButton, Pagination, SpeedDial, TabMenu, Tree, etc.)",
    "layouts": "Layout containers (Accordion, Card, Dialog, Drawer, Grid, Tabs, etc.)",
    "panes": "Display panes (Typography, etc.)",
    "wrappers": "Wrapper components (Badge, Skeleton, Tooltip, Transition, etc.)",
    "page": "Page-level components (Page template, BreakpointSwitcher, ThemeToggle, etc.)",
    "chat": "Chat components (ChatFeed, ChatInterface, ChatMessage, ChatStep, etc.)",
    "indicators": "Progress and status indicators (CircularProgress, LinearProgress, LoadingSpinner, etc.)",
    "global": "Global components (Notifications, etc.)",
}


def copy_markdown_docs():
    """Copy all .md files from doc/ into the markdown output directory."""
    for md_file in DOC_DIR.rglob("*.md"):
        rel = md_file.relative_to(DOC_DIR)
        dest = OUTPUT_DIR / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(md_file, dest)
    print(f"Copied markdown docs to {OUTPUT_DIR}")


def convert_reference_notebooks():
    """Convert reference notebooks to markdown using nbconvert."""
    for notebook in sorted(REFERENCE_DIR.rglob("*.ipynb")):
        if ".ipynb_checkpoints" in str(notebook):
            continue
        rel = notebook.relative_to(REFERENCE_DIR)
        output_dir = OUTPUT_DIR / "reference" / rel.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            [
                sys.executable, "-m", "jupyter", "nbconvert",
                "--to", "markdown",
                "--output-dir", str(output_dir),
                str(notebook),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"  Warning: failed to convert {notebook}: {result.stderr.strip()}")
        else:
            print(f"  Converted {rel}")


def generate_index_pages():
    """Generate a markdown index page for each reference category."""
    index_dir = OUTPUT_DIR / "reference"
    index_dir.mkdir(parents=True, exist_ok=True)

    for category, description in REFERENCE_DESCRIPTIONS.items():
        category_dir = index_dir / category
        if not category_dir.exists():
            continue

        md_files = sorted(category_dir.glob("*.md"))
        if not md_files:
            continue

        title = category.replace("_", " ").title()
        lines = [
            f"# {title}",
            "",
            f"> {description}",
            "",
        ]
        for md_file in md_files:
            if md_file.name == "index.md":
                continue
            name = md_file.stem
            url = f"{MARKDOWN_BASE_URL}/reference/{category}/{md_file.name}"
            lines.append(f"- [{name}]({url})")

        index_file = category_dir / "index.md"
        index_file.write_text("\n".join(lines) + "\n")
        print(f"  Generated index: reference/{category}/index.md")


def generate_llms_txt():
    """Generate llms.txt with links to per-category index pages."""
    lines = [
        "# Panel Material UI",
        "",
        "Panel Material UI is a Material Design extension for HoloViz Panel, providing "
        "Material UI themed components for building interactive Python web applications. "
        "It offers widgets, layouts, menus, indicators, chat components, and page templates "
        "styled with Google's Material Design.",
        "",
        f"All documentation is available as markdown files under the {MARKDOWN_BASE_URL}/ path.",
        "",
    ]

    # Documentation sections
    lines.append("## Documentation")
    lines.append("")
    for section, description in SECTION_DESCRIPTIONS.items():
        section_dir = OUTPUT_DIR / section
        if not section_dir.exists():
            continue
        md_files = sorted(
            f for f in section_dir.rglob("*.md")
            if f.name != "index.md"
        )
        if not md_files:
            continue
        lines.append(f"### {section}")
        lines.append(f"> {description}")
        lines.append("")
        for md_file in md_files:
            rel = md_file.relative_to(OUTPUT_DIR)
            name = md_file.stem.replace("_", " ").title()
            lines.append(f"- [{name}]({MARKDOWN_BASE_URL}/{rel})")
        lines.append("")

    # Component reference with links to index pages
    lines.append("## Component Reference")
    lines.append("")
    lines.append(
        "Detailed reference documentation for every Panel Material UI component, "
        "organized by category."
    )
    lines.append("")
    for category, description in REFERENCE_DESCRIPTIONS.items():
        category_dir = OUTPUT_DIR / "reference" / category
        if not category_dir.exists():
            continue
        md_files = [f for f in category_dir.glob("*.md") if f.name != "index.md"]
        if not md_files:
            continue
        title = category.replace("_", " ").title()
        index_url = f"{MARKDOWN_BASE_URL}/reference/{category}/index.md"
        lines.append(f"- [{title}]({index_url}): {description}")

    lines.append("")

    llms_txt = BUILTDOCS_DIR / "llms.txt"
    llms_txt.write_text("\n".join(lines))
    print(f"Generated {llms_txt}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Copying markdown docs...")
    copy_markdown_docs()
    print("Converting reference notebooks...")
    convert_reference_notebooks()
    print("Generating category index pages...")
    generate_index_pages()
    print("Generating llms.txt...")
    generate_llms_txt()
    print("Done!")


if __name__ == "__main__":
    main()
