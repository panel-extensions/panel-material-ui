"""
Components package for MaterialComponent metadata collection.

This package provides tools for collecting and managing metadata about
MaterialComponent subclasses in the panel_material_ui package.
"""

from .models import ParameterInfo, ComponentInfo, ComponentCollection
from .data import (
    get_components,
    save_components,
    load_components,
    get_components_dataframe,
    display_components_summary,
    collect_component_info,
    find_all_subclasses
)

__all__ = [
    'ParameterInfo',
    'ComponentInfo',
    'ComponentCollection',
    'get_components',
    'save_components',
    'load_components',
    'get_components_dataframe',
    'display_components_summary',
    'collect_component_info',
    'find_all_subclasses'
]
