"""
Pydantic models for MaterialComponent metadata collection.
"""
from __future__ import annotations

from typing import Any, Dict, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ParameterInfo(BaseModel):
    """Model for parameter attribute information."""
    model_config = ConfigDict(extra='allow')  # Allow additional fields we don't know about

    # Common attributes that most parameters have
    type: str
    default: Optional[Any] = None
    doc: Optional[str] = None
    allow_None: Optional[bool] = None
    constant: Optional[bool] = None
    readonly: Optional[bool] = None
    per_instance: Optional[bool] = None

    # Type-specific attributes (will be present only for relevant parameter types)
    objects: Optional[Any] = None  # For Selector parameters
    bounds: Optional[Any] = None   # For Number parameters
    regex: Optional[str] = None    # For String parameters


class ComponentSummary(BaseModel):
    """Model for a summary of MaterialComponent information."""

    name: str
    module_path: str
    init_signature: str
    docstring: str

class ComponentSummarySearchResult(ComponentSummary):
    """Model for a summary of MaterialComponent information."""

    relevance_score: int = Field(default=0, description="Relevance score for search results")

    @classmethod
    def from_summary(cls, component: ComponentSummary, relevance_score: int) -> ComponentSummary:
        """
        Create a ComponentSummarySearchResult from a ComponentSummary and a relevance score.

        Args:
            component (ComponentSummary): The component summary to convert.
            relevance_score (int): The relevance score for search results.

        Returns:
            ComponentSummarySearchResult: A search result summary of the component.
        """
        return cls(
            name=component.name,
            module_path=component.module_path,
            init_signature=component.init_signature,
            docstring=component.docstring,
            relevance_score=relevance_score
        )

class ComponentInfo(ComponentSummary):
    """Model for full info of MaterialComponent information."""

    parameters: Dict[str, ParameterInfo]

    def to_summary(self) -> ComponentSummary:
        """
        Convert this ComponentInfo to a ComponentSummary.

        Returns:
            ComponentSummary: A summary of the component.
        """
        return ComponentSummary(
            name=self.name,
            module_path=self.module_path,
            init_signature=self.init_signature,
            docstring=self.docstring
        )

class ComponentCollection(BaseModel):
    """Model for a collection of components with metadata."""

    components: List[ComponentInfo]
    timestamp: datetime = Field(default_factory=datetime.now)
    total_count: int = Field(default=0)

    def __init__(self, **data):
        super().__init__(**data)
        self.total_count = len(self.components)
