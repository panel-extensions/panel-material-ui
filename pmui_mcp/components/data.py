#!/usr/bin/env python3
"""
Data collection module for MaterialComponent metadata.

This module provides functionality to collect metadata about all child classes
of MaterialComponent in the panel_material_ui package, including their documentation,
parameter schema, and reference documentation paths/URLs.
"""
from __future__ import annotations

from typing import List
import json
from datetime import datetime
from pathlib import Path
import pandas as pd

import panel_material_ui as pmui
from panel_material_ui.base import MaterialComponent

from .models import ComponentInfo, ParameterInfo


def find_all_subclasses(cls: type) -> set[type]:
    """
    Recursively find all subclasses of a given class.

    Parameters
    ----------
    cls : type
        The base class to find subclasses for.

    Returns
    -------
    set[type]
        Set of all subclasses found recursively.
    """
    subclasses = set()
    for subclass in cls.__subclasses__():
        subclasses.add(subclass)
        subclasses.update(find_all_subclasses(subclass))
    return subclasses


def collect_component_info(cls: type) -> ComponentInfo:
    """
    Collect information about a MaterialComponent subclass.

    Parameters
    ----------
    cls : type
        The class to collect information for.

    Returns
    -------
    ComponentInfo
        Pydantic model containing component information
    """
    # Determine the reference guide notebook path
    module_parts = cls.__module__.split('.')
    class_name = cls.__name__

    # Extract docstring
    docstring = cls.__doc__ if cls.__doc__ else ""

    # Extract description (first sentence from docstring)
    description = ""
    if docstring:
        # Clean the docstring and get first sentence
        cleaned_docstring = docstring.strip()
        if cleaned_docstring:
            # Find first sentence ending with period, exclamation, or question mark
            import re
            sentences = re.split(r'[.!?]', cleaned_docstring)
            if sentences:
                description = sentences[0].strip()
                # Remove leading/trailing whitespace and normalize spaces
                description = ' '.join(description.split())

    # Extract parameters information
    parameters = {}
    if hasattr(cls, 'param'):
        for param_name in cls.param:
            # Skip private parameters
            if param_name.startswith('_'):
                continue

            param_obj = cls.param[param_name]
            param_data = {}

            # Get common parameter attributes (skip private ones)
            for attr in ['default', 'doc', 'allow_None', 'constant', 'readonly', 'per_instance']:
                if hasattr(param_obj, attr):
                    value = getattr(param_obj, attr)
                    # Handle non-JSON serializable values
                    try:
                        json.dumps(value)
                        param_data[attr] = value
                    except (TypeError, ValueError):
                        param_data[attr] = "NON_JSON_SERIALIZABLE_VALUE"

            # Get type-specific attributes
            param_type = type(param_obj).__name__
            param_data['type'] = param_type

            # For Selector parameters, get options
            if hasattr(param_obj, 'objects'):
                try:
                    json.dumps(param_obj.objects)
                    param_data['objects'] = param_obj.objects
                except (TypeError, ValueError):
                    param_data['objects'] = "NON_JSON_SERIALIZABLE_VALUE"

            # For Number parameters, get bounds
            if hasattr(param_obj, 'bounds'):
                try:
                    json.dumps(param_obj.bounds)
                    param_data['bounds'] = param_obj.bounds
                except (TypeError, ValueError):
                    param_data['bounds'] = "NON_JSON_SERIALIZABLE_VALUE"

            # For String parameters, get regex
            if hasattr(param_obj, 'regex'):
                try:
                    json.dumps(param_obj.regex)
                    param_data['regex'] = param_obj.regex
                except (TypeError, ValueError):
                    param_data['regex'] = "NON_JSON_SERIALIZABLE_VALUE"

            # Create ParameterInfo model
            parameters[param_name] = ParameterInfo(**param_data)

    # Get __init__ method signature
    init_signature = ""
    if hasattr(cls, '__init__'):
        try:
            import inspect
            sig = inspect.signature(cls.__init__)
            init_signature = str(sig)
        except Exception as e:
            init_signature = f"Error getting signature: {e}"

    # Read reference guide content
    # Create and return ComponentInfo model
    return ComponentInfo(
        name=cls.__name__,
        module_path=f"{cls.__module__}.{cls.__name__}",
        docstring=docstring,
        description=description,
        parameters=parameters,
        init_signature=init_signature
    )


def get_components() -> List[ComponentInfo]:
    """
    Get all MaterialComponent subclasses as a list of ComponentInfo models.

    Returns
    -------
    List[ComponentInfo]
        List of component information models
    """
    all_subclasses = find_all_subclasses(MaterialComponent)

    # Filter to only those in panel_material_ui package and exclude private classes
    pmui_subclasses = [
        cls for cls in all_subclasses
        if cls.__module__.startswith('panel_material_ui') and not cls.__name__.startswith('_')
    ]

    # Collect component information
    component_data = [collect_component_info(cls) for cls in pmui_subclasses]

    # Sort by module_path for consistent ordering
    component_data.sort(key=lambda x: x.module_path)
    return component_data


def save_components(data: List[ComponentInfo], filename: str | None = None) -> str:
    """
    Save component data to JSON file.

    Parameters
    ----------
    data : List[ComponentInfo]
        Component data from get_components()
    filename : str, optional
        Custom filename. If None, generates timestamped filename.

    Returns
    -------
    str
        Path to saved file
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    if filename is None:
        filename = f'material_components_{timestamp}.json'

    filepath = Path(filename)

    # Convert Pydantic models to dict for JSON serialization
    json_data = [component.model_dump() for component in data]

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    print(f"Component data saved to: {filepath}")
    return str(filepath)


def load_components(filepath: str) -> List[ComponentInfo]:
    """
    Load component data from JSON file.

    Parameters
    ----------
    filepath : str
        Path to saved component data file

    Returns
    -------
    List[ComponentInfo]
        Loaded component data as Pydantic models
    """
    file_path = Path(filepath)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # Convert JSON data back to Pydantic models
    return [ComponentInfo(**item) for item in json_data]


def get_components_dataframe() -> pd.DataFrame:
    """
    Get MaterialComponent subclasses as a pandas DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame containing component information
    """
    component_data = get_components()
    df_data = [component.model_dump() for component in component_data]
    return pd.DataFrame(df_data)


def display_components_summary() -> List[ComponentInfo]:
    """
    Collect all MaterialComponent subclasses and display as DataFrame.

    Finds all MaterialComponent subclasses, excludes private classes (starting with '_'),
    and displays the results in a structured DataFrame format.

    Returns
    -------
    List[ComponentInfo]
        List of component information models
    """
    print("MaterialComponent Subclasses Analysis")
    print("=" * 50)

    # Get all subclasses
    component_data = get_components()

    # Convert to dict format for pandas DataFrame
    df_data = [component.model_dump() for component in component_data]
    df = pd.DataFrame(df_data)

    # Display summary statistics
    print(f"Total MaterialComponent subclasses found: {len(component_data)}")
    print(f"Modules covered: {df['module_path'].str.split('.').str[1].nunique()}")
    print()

    # Display DataFrame
    print("Component Details:")
    print("-" * 30)

    # Configure pandas display options for better output
    with pd.option_context(
        'display.max_rows', None,
        'display.max_columns', None,
        'display.width', None,
        'display.max_colwidth', 60
    ):
        # Display main columns including description
        display_df = df[['name', 'description', 'docs_url']].copy()
        print(display_df.to_string(index=False))

    print()
    print("Note: Full data (docstring, parameters, paths, docs) available programmatically via get_components()")
    print("Example: data = get_components(); save_components(data, 'my_components.json')")

    print()
    print("Module Distribution:")
    print("-" * 20)

    # Show distribution by module
    module_counts = df['module_path'].str.split('.').str[1].value_counts()
    for module, count in module_counts.items():
        print(f"{module}: {count} classes")

    return component_data
