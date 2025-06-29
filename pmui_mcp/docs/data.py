#!/usr/bin/env python3
"""
Data collection module for Panel Material UI Documentation metadata.

This module provides functionality to collect metadata about all documentation
pages in the Panel Material UI project, including their content, titles,
descriptions, and URLs.
"""
from __future__ import annotations

from typing import List, Dict, Any
import json
import re
from datetime import datetime
from pathlib import Path

from .models import DocumentationPageInfo, DocumentationCollection


def extract_title_and_description(content: str) -> tuple[str, str]:
    """
    Extract title and description from markdown content.

    Args:
        content: Markdown content

    Returns:
        Tuple of (title, description)
    """
    lines = content.strip().split('\n')
    title = ""
    description = ""

    # Find the first H1 heading
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break

    # Extract first paragraph after title
    content_lines = []
    found_title = False
    skip_empty_lines = True

    for line in lines:
        # Mark when we've found the title
        if line.startswith('# ') and title:
            found_title = True
            skip_empty_lines = True
            continue

        if found_title:
            line = line.strip()

            # Skip empty lines until we find content
            if skip_empty_lines and not line:
                continue
            elif line:
                skip_empty_lines = False

            # Stop if we hit another heading
            if line.startswith('#'):
                break

            # Skip directive blocks and code blocks
            if line.startswith(':::') or line.startswith('```') or line.startswith('::') or line.startswith('..'):
                continue

            # Collect content lines
            if line:
                content_lines.append(line)
                # Stop when we have enough content
                if len(' '.join(content_lines)) > 150:
                    break

    if content_lines:
        description = ' '.join(content_lines)
        # Clean up description - remove markdown syntax
        description = re.sub(r'\*\*(.*?)\*\*', r'\1', description)  # Bold
        description = re.sub(r'\*(.*?)\*', r'\1', description)      # Italic
        description = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', description)  # Links

        # Truncate if too long
        if len(description) > 200:
            description = description[:197] + "..."

    return title or "Untitled", description or "No description available"


def collect_documentation_pages(doc_root: Path) -> List[DocumentationPageInfo]:
    """
    Recursively find all markdown files in the documentation directory and collect their metadata.

    Args:
        doc_root: Path to the documentation root directory

    Returns:
        List of DocumentationPageInfo objects
    """
    pages = []

    if not doc_root.exists():
        return pages

    # Walk through all markdown files
    for md_file in doc_root.rglob("*.md"):
        try:
            # Skip files that shouldn't be included
            if any(skip in str(md_file) for skip in ['_build', '__pycache__', '.pytest_cache']):
                continue

            # Read file content
            content = md_file.read_text(encoding='utf-8')

            # Extract title and description
            title, description = extract_title_and_description(content)

            # Create relative path from doc root
            relative_path = md_file.relative_to(doc_root)

            # Generate URL
            url_path = str(relative_path).replace('.md', '.html')
            url = f"https://panel-material-ui.holoviz.org/{url_path}"

            # Create DocumentationPageInfo object
            page_info = DocumentationPageInfo(
                name=str(relative_path),
                title=title,
                description=description,
                url=url,
                file_path=str(md_file),
                content=content
            )

            pages.append(page_info)

        except Exception as e:
            # Skip files that can't be read
            continue

    # Sort by name for consistent ordering
    pages.sort(key=lambda x: x.name)
    return pages


def get_documentation_collection(doc_root: Path) -> DocumentationCollection:
    """
    Get all documentation pages as a DocumentationCollection.

    Args:
        doc_root: Path to the documentation root directory

    Returns:
        DocumentationCollection containing all pages
    """
    pages = collect_documentation_pages(doc_root)

    return DocumentationCollection(
        pages=pages,
        doc_root=str(doc_root)
    )


def save_documentation_collection(
    collection: DocumentationCollection,
    filename: str | None = None
) -> str:
    """
    Save documentation collection to JSON file.

    Args:
        collection: DocumentationCollection to save
        filename: Custom filename. If None, generates timestamped filename.

    Returns:
        Path to saved file
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    if filename is None:
        filename = f'documentation_pages_{timestamp}.json'

    filepath = Path(filename)

    # Convert Pydantic model to dict for JSON serialization
    json_data = collection.model_dump()

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    print(f"Documentation collection saved to: {filepath}")
    return str(filepath)


def load_documentation_collection(filepath: str) -> DocumentationCollection:
    """
    Load documentation collection from JSON file.

    Args:
        filepath: Path to saved documentation collection file

    Returns:
        Loaded DocumentationCollection
    """
    file_path = Path(filepath)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # Convert JSON data back to Pydantic model
    return DocumentationCollection(**json_data)


def display_documentation_summary(collection: DocumentationCollection) -> None:
    """
    Display a summary of the documentation collection.

    Args:
        collection: DocumentationCollection to summarize
    """
    print("Panel Material UI Documentation Analysis")
    print("=" * 50)

    print(f"Total documentation pages: {collection.total_count}")
    print(f"Documentation root: {collection.doc_root}")
    print(f"Collection timestamp: {collection.timestamp}")
    print()

    # Analyze page distribution by category
    categories = {}
    for page in collection.pages:
        path_parts = page.name.split('/')
        category = path_parts[0] if len(path_parts) > 1 else 'root'
        categories[category] = categories.get(category, 0) + 1

    print("Pages by category:")
    print("-" * 20)
    for category, count in sorted(categories.items()):
        print(f"{category}: {count} pages")

    print()
    print("Sample pages:")
    print("-" * 15)

    # Show sample pages from each category
    shown_categories = set()
    for page in collection.pages[:10]:
        category = page.name.split('/')[0] if '/' in page.name else 'root'
        if category not in shown_categories:
            print(f"  {category}: {page.name} - {page.title}")
            shown_categories.add(category)

    print()
    print("Note: Full page content and metadata available programmatically")
    print("Example: collection.get_page_by_name('index.md')")


def get_page_suggestions(collection: DocumentationCollection, name: str) -> List[str]:
    """
    Get suggestions for similar page names when a page is not found.

    Args:
        collection: DocumentationCollection to search
        name: The name that was not found

    Returns:
        List of suggested page names
    """
    suggestions = []
    name_lower = name.lower()

    for page in collection.pages:
        if name_lower in page.name.lower():
            suggestions.append(page.name)

    return suggestions[:5]  # Return top 5 suggestions
