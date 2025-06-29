#!/usr/bin/env python3
"""
Panel Material UI Documentation MCP Server

This MCP server provides tools and resources for the Panel Material UI documentation.
"""
from typing import Dict, Any, List
from pathlib import Path

from fastmcp import FastMCP
from .data import get_documentation_collection
from .models import DocumentationCollection, DocumentationPageSummary


# Create the Documentation FastMCP server
docs_mcp = FastMCP(
    name="Panel Material UI Documentation",
    instructions="""
    This MCP server provides tools and resources for the Panel Material UI documentation.

    The Panel Material UI documentation follows the Diataxis framework for technical documentation, which consists
    of four main categories: Tutorials, How-to Guides, Reference Guides, and Explanations.

    Available tools:

    - get_pages: Get a list of all available documentation pages
    - get_page: Get the content of a specific documentation page
    - search_pages: Search for documentation pages by name, title, or description
    """
)

# Documentation root directory
DOC_ROOT = Path(__file__).parent.parent.parent / "doc"

# Cache for all documentation data - loaded once at startup
_DOCS_COLLECTION: DocumentationCollection | None = None


def _load_docs_collection() -> DocumentationCollection:
    """
    Load all documentation data into cache at startup.
    """
    global _DOCS_COLLECTION
    if _DOCS_COLLECTION is None:
        _DOCS_COLLECTION = get_documentation_collection(DOC_ROOT)
    return _DOCS_COLLECTION


def _get_page_from_collection(name: str) -> Dict[str, Any]:
    """
    Get a page from the documentation collection by name.

    Args:
        name: The relative path to the documentation file

    Returns:
        Dictionary containing page information including content

    Raises:
        ValueError: If page is not found
    """
    collection = _load_docs_collection()
    page = collection.get_page_by_name(name)
    if page:
        return page.model_dump()

    # If not found, provide helpful error message with suggestions
    suggestions = [p.name for p in collection.pages if name.lower() in p.name.lower()]

    if suggestions:
        error_msg = f"Page '{name}' not found. Did you mean one of these?\n"
        error_msg += "\n".join(f"- {suggestion}" for suggestion in suggestions[:5])
    else:
        error_msg = f"Page '{name}' not found. Available pages:\n"
        error_msg += "\n".join(f"- {p.name}" for p in collection.pages[:10])
        if len(collection.pages) > 10:
            error_msg += f"\n... and {len(collection.pages) - 10} more"

    raise ValueError(error_msg)


@docs_mcp.tool
def get_pages() -> List[DocumentationPageSummary]:
    """
    [DOCUMENTATION] Get a list of all available documentation pages.

    Returns a list of available documentation pages with their metadata:

    - name: the relative path to the source file (unique key)
    - title: the title extracted from the page content
    - description: a short description from the first paragraph
    - url: the URL when deployed at https://panel-material-ui.holoviz.org/

    Returns:
        List of dictionaries containing page information (without content for brevity)
    """
    collection = _load_docs_collection()
    return collection.get_pages_summary()


@docs_mcp.tool
def get_page(name: str) -> str:
    """
    [DOCUMENTATION] Get the content of a specific documentation page by name.

    Args:
        name: The relative path to the documentation file (e.g., "index.md", "how_to/customize.md")

    Returns:
        The markdown content of the specified page
    """
    try:
        page = _get_page_from_collection(name)
        return page["content"]
    except ValueError:
        # Re-raise with the helpful error message from _get_page_from_collection
        raise

@docs_mcp.tool
def search_pages(query: str, limit: int = 10) -> List[DocumentationPageSummary]:
    """
    [DOCUMENTATION] Search for documentation pages by name, title, or description.

    Args:
        query: Search term to look for in page names, titles, or descriptions
        limit: Maximum number of results to return (default: 10)

    Returns:
        List of matching documentation page summaries
    """
    collection = _load_docs_collection()
    matches = collection.search_pages(query)

    # Limit results and convert to summaries
    limited_matches = matches[:limit]

    return [
        DocumentationPageSummary(**{
            "name": page.name,
            "title": page.title,
            "description": page.description,
            "url": page.url,
            "file_path": page.file_path
        })
        for page in limited_matches
    ]

if __name__ == "__main__":
    # Load documentation cache at startup
    print("Loading Panel Material UI documentation...")
    _load_docs_collection()
    print(f"Loaded {len(_DOCS_COLLECTION.pages) if _DOCS_COLLECTION else 0} documentation pages")

    # Run the server
    docs_mcp.run(transport="http")
else:
    # Load cache when imported as a module
    _load_docs_collection()
