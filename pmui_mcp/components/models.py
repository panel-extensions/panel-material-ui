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
    description: str
    docstring: str
    docs_url: str
    docs_notebook_path: str
    docs_markdown_path: str
    parameters: Dict[str, ParameterInfo]

class ComponentInfo(ComponentSummary):
    """Model for MaterialComponent information."""

    docs: str


class ComponentCollection(BaseModel):
    """Model for a collection of components with metadata."""

    components: List[ComponentInfo]
    timestamp: datetime = Field(default_factory=datetime.now)
    total_count: int = Field(default=0)

    def __init__(self, **data):
        super().__init__(**data)
        self.total_count = len(self.components)
