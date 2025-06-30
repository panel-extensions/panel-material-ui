"""
Pydantic models for Panel Material UI Documentation metadata collection.
"""
from __future__ import annotations

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class DocumentationPageSummary(BaseModel):
    """Model for documentation page information."""
    model_config = ConfigDict(extra='forbid')

    name: str = Field(..., description="Relative path to the documentation file")
    title: str = Field(..., description="Title extracted from the page content")
    description: str = Field(..., description="Short description from the first paragraph")
    url: str = Field(..., description="URL when deployed at panel-material-ui.holoviz.org")
    file_path: str = Field(..., description="Absolute path to the source file")


class DocumentationPageInfo(DocumentationPageSummary):
    """Model for documentation page information."""

    content: str = Field(..., description="Full markdown content of the page")


class DocumentationCollection(BaseModel):
    """Model for a collection of documentation pages with metadata."""

    pages: List[DocumentationPageInfo]
    timestamp: datetime = Field(default_factory=datetime.now)
    total_count: int = Field(default=0)
    doc_root: str = Field(..., description="Path to the documentation root directory")

    def __init__(self, **data):
        super().__init__(**data)
        self.total_count = len(self.pages)

    def get_page_by_name(self, name: str) -> Optional[DocumentationPageInfo]:
        """
        Get a page by its name (relative path).

        Args:
            name: The relative path to the documentation file

        Returns:
            DocumentationPageInfo if found, None otherwise
        """
        for page in self.pages:
            if page.name == name:
                return page
        return None

    def search(self, query: str) -> List[DocumentationPageInfo]:
        """
        Search for pages containing the query in name, title, or description.

        Args:
            query: Search term

        Returns:
            List of matching pages
        """
        query_lower = query.lower()
        matches = []

        for page in self.pages:
            if (query_lower in page.name.lower() or
                query_lower in page.title.lower() or
                query_lower in page.description.lower()):
                matches.append(page)

        return matches

    def get_pages_summary(self) -> List[DocumentationPageSummary]:
        """
        Get a summary of all pages without content for efficiency.

        Returns:
            List of page summaries without content
        """
        return [
            DocumentationPageSummary(**{
                "name": page.name,
                "title": page.title,
                "description": page.description,
                "url": page.url,
                "file_path": page.file_path,
            })
            for page in self.pages
        ]
