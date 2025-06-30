#!/usr/bin/env python3
"""
Panel Material UI Documentation MCP Server

This MCP server provides tools and resources for the Panel Material UI documentation.
"""
from typing import List
from pathlib import Path

from fastmcp import FastMCP
from .data import get_documentation_collection
from .models import DocumentationCollection, DocumentationPageSummary, DocumentationPageInfo


# Create the Documentation FastMCP server
docs_mcp = FastMCP(
    name="Panel Material UI Documentation",
    instructions="""
    This MCP server provides tools and resources for the Panel Material UI documentation.

    Use this server to access:
    - Documentation pages: Explore and use various documentation pages for building interactive applications.
    - Reference documentation: Get detailed reference information about specific Panel Material UI components.

    ALWAYS read and learn from the best practice documentation resource before using Panel Material UI
    """
)

_DOC_ROOT = Path(__file__).parent.parent.parent / "doc"
_DOCS_COLLECTION: DocumentationCollection | None = None

def _load_docs_collection() -> DocumentationCollection:
    """
    Load all documentation data into cache at startup.

    Args:
        doc_root: The root directory where documentation files are located
    """
    global _DOCS_COLLECTION
    if _DOCS_COLLECTION is None:
        _DOCS_COLLECTION = get_documentation_collection(_DOC_ROOT)
    return _DOCS_COLLECTION


def _get_page_from_collection(name: str) -> DocumentationPageInfo:
    """
    Get a page from the documentation collection by name.

    Args:<
        name: The relative path to the documentation file

    Returns:
        DocumentationPageInfo containing page information including content

    Raises:
        ValueError: If page is not found
    """
    collection = _load_docs_collection()
    page = collection.get_page_by_name(name)
    if page:
        return page

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

def _get_reference_page_from_collection(name: str) -> DocumentationPageInfo:
    """
    Get a reference page from the documentation collection by name.

    Args:
        name: The name of the component. For example, "Button", "Card", etc.

    Returns:
        DocumentationPageInfo containing page information including content

    Raises:
        ValueError: If page is not found
    """
    collection = _load_docs_collection()
    for page in collection.pages:
        filename = Path(page.name).name
        if filename == name + ".md":
            return page

    error_msg = f"Reference page for component '{name}' not found."
    raise ValueError(error_msg)


@docs_mcp.tool
def get_pages() -> List[DocumentationPageSummary]:
    """
    Returns a list of available documentation pages with their metadata:

    - name: the relative path to the source file. Use this value when requesting the page content.
    - title: the title extracted from the page content
    - description: a short description from the first paragraph
    - url: the URL when deployed at https://panel-material-ui.holoviz.org/

    Use this tool to understand which documentation pages are available.

    Returns:
        List of dictionaries containing page information (without content for brevity)
    """
    collection = _load_docs_collection()
    return collection.get_pages_summary()


@docs_mcp.tool
def get_page(name: str) -> str:
    """
    Returns the content of a specific documentation page by name.

    Use this tool to understand how to use a specific topic or feature of Panel Material UI.

    Args:
        name: The relative path to the documentation file (e.g., "index.md", "how_to/customize.md")

    Returns:
        The markdown content of the specified page
    """
    try:
        page = _get_page_from_collection(name)
        return page.content
    except ValueError:
        # Re-raise with the helpful error message from _get_page_from_collection
        raise

@docs_mcp.tool
def get_reference_page(component: str) -> str:
    """
    Returns the reference documentation for a specific component by name.

    Use this tool to:

    - get detailed information about the API and usage of a specific component.
    - understand how to use a specific component in your application.

    Args:
        component: The name of the component to get reference documentation for. Example "Button", "Card" or similar.

    Returns:
        The markdown content of the reference page for the specified component
    """
    try:
        return _get_reference_page_from_collection(component).content
    except ValueError as e:
        raise ValueError(f"Reference page for component '{component}' not found. {str(e)}")

@docs_mcp.resource(uri="docs://explanation/best_practices")
def get_best_practices_page() -> str:
    """
    Returns the best practices documentation page.

    ALWAYS read and learn from the best practice and example app resources before using Panel Material UI.

    Use this resource to get detailed guidance about using Panel Material UI effectively.

    Returns:
        The markdown content of the best practices page
    """
    return _get_page_from_collection("explanation/best_practices.md").content


@docs_mcp.tool
def search(query: str, limit: int = 10) -> List[DocumentationPageSummary]:
    """
    Search for documentation pages by name, title, or description.

    Use this tool to find documentation pages that can help you understand a topic, feature or component.

    Args:
        query: Search term to look for in page names, titles, or descriptions
        limit: Maximum number of results to return (default: 10)

    Returns:
        List of matching documentation page summaries
    """
    collection = _load_docs_collection()
    matches = collection.search(query)

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
