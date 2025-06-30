"""
Pydantic models for Panel Material UI Documentation metadata collection.
"""
from __future__ import annotations

import re
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

        Uses improved algorithm that handles multi-word queries and provides
        relevance-based scoring for better results.

        Args:
            query: Search term (can be multiple words)

        Returns:
            List of matching pages ordered by relevance
        """
        if not query.strip():
            return []

        query_lower = query.lower().strip()
        query_words = re.findall(r'\b\w+\b', query_lower)

        if not query_words:
            return []

        scored_matches = []

        for page in self.pages:
            name_lower = page.name.lower()
            title_lower = page.title.lower()
            desc_lower = page.description.lower()

            # Calculate relevance score
            score = 0

            # Exact phrase match (highest score)
            if query_lower in title_lower:
                score += 100
            if query_lower in name_lower:
                score += 90
            if query_lower in desc_lower:
                score += 80

            # Individual word matches
            title_words = set(re.findall(r'\b\w+\b', title_lower))
            name_words = set(re.findall(r'\b\w+\b', name_lower))
            desc_words = set(re.findall(r'\b\w+\b', desc_lower))

            for word in query_words:
                # Word matches in title (high relevance)
                if word in title_words:
                    score += 50
                # Word matches in name (medium-high relevance)
                if word in name_words:
                    score += 40
                # Word matches in description (medium relevance)
                if word in desc_words:
                    score += 30

                # Partial word matches (lower relevance)
                if any(word in title_word for title_word in title_words):
                    score += 20
                if any(word in name_word for name_word in name_words):
                    score += 15
                if any(word in desc_word for desc_word in desc_words):
                    score += 10

            # Bonus for matching multiple words
            matched_words = len([w for w in query_words if w in title_words or w in name_words or w in desc_words])
            if matched_words > 1:
                score += matched_words * 25

            # Bonus for word order preservation in title/name
            if len(query_words) > 1:
                title_text = title_lower
                name_text = name_lower
                for i in range(len(query_words) - 1):
                    word1_pos_title = title_text.find(query_words[i])
                    word2_pos_title = title_text.find(query_words[i + 1])
                    if word1_pos_title != -1 and word2_pos_title != -1 and word1_pos_title < word2_pos_title:
                        score += 35

                    word1_pos_name = name_text.find(query_words[i])
                    word2_pos_name = name_text.find(query_words[i + 1])
                    if word1_pos_name != -1 and word2_pos_name != -1 and word1_pos_name < word2_pos_name:
                        score += 30

            if score > 0:
                scored_matches.append((score, page))

        # Sort by score (descending) and return pages
        scored_matches.sort(key=lambda x: x[0], reverse=True)
        return [page for _, page in scored_matches]

    def get_pages_summary(self) -> List[DocumentationPageSummary]:
        """
        Get a summary of all pages without content for efficiency.

        Returns:
            List of page summaries without content
        """
        return [
            DocumentationPageSummary(
                name = page.name,
                title = page.title,
                description = page.description,
                url = page.url,
                file_path = page.file_path,
            )
            for page in self.pages
        ]
