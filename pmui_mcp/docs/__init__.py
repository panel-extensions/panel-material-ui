"""
Documentation package for Panel Material UI MCP server.

This package provides tools for collecting and managing metadata about
Panel Material UI documentation pages.
"""

from .models import DocumentationPageInfo, DocumentationCollection
from .data import (
    extract_title_and_description,
    collect_documentation_pages,
    get_documentation_collection,
    save_documentation_collection,
    load_documentation_collection,
    display_documentation_summary,
    get_page_suggestions
)

__all__ = [
    'DocumentationPageInfo',
    'DocumentationCollection',
    'extract_title_and_description',
    'collect_documentation_pages',
    'get_documentation_collection',
    'save_documentation_collection',
    'load_documentation_collection',
    'display_documentation_summary',
    'get_page_suggestions'
]
