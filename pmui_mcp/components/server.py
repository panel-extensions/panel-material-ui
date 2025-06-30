"""
Panel Material UI Components MCP Server

This MCP server provides tools and resources for exploring and accessing
Panel Material UI Components.
"""
from typing import Dict

from fastmcp import FastMCP
from pmui_mcp.components.data import get_components
from pmui_mcp.components.models import ComponentInfo, ComponentSummary, ParameterInfo, ComponentSummarySearchResult
from pathlib import Path


# Create the FastMCP server
mcp = FastMCP(
    name="Panel Material UI",
    instructions="""
    This server provides access to [Panel Material UI](https://panel-material-ui.holoviz.org/reference/index.html) resources and tools.

    The panel-material-ui python package provides a large collection of components for building
    interactive [Panel](https://panel.holoviz.org/) web applications with a Material Design look and feel.

    Use this server to access:
    - Panel Material UI components: Explore and use various components for building interactive applications.
    - Example applications: Get example code to kickstart your Panel projects.
    """
)


COMPONENTS = get_components()
TEMPLATE_DIR = Path(__file__).parent / "templates"
BASIC_HELLO_WORLD_APP = (TEMPLATE_DIR / "basic_hello_world_app.py").read_text()
INTERMEDIATE_HELLO_WORLD_APP = (TEMPLATE_DIR / "intermediate_hello_world_app.py").read_text()

@mcp.tool
def get_all() -> list[ComponentSummary]:
    """
    Lists all components with summary information.

    Read this information to get an overview of available components.

    Returns:
        List of dictionaries containing component summary information
    """
    components_list = []

    for component in COMPONENTS:
        components_list.append(component.to_summary())

    return components_list

def _get_component_info(component_name: str)->ComponentInfo:
    component = None
    for comp in COMPONENTS:
        if comp.name.lower() == component_name.lower():
            component = comp
            break

    if not component:
        # Try partial matching
        matches = [comp for comp in COMPONENTS if component_name.lower() in comp.name.lower()]
        if matches:
            msg = str({
                "error": f"Component '{component_name}' not found",
                "suggestions": [comp.name for comp in matches[:5]],
                "message": "Did you mean one of these components?"
            })
            raise RuntimeError(msg)
        else:
            msg = str({
                "error": f"Component '{component_name}' not found",
                "available_components": [comp.name for comp in COMPONENTS[:10]],
                "message": "Here are some available components"
            })
            raise RuntimeError(msg)

    return component

@mcp.tool
def get(component_name: str) -> ComponentInfo:
    """
    Returns information about a specific Panel Material UI component.

    Use this tool to get detailed information about the component, including its parameters and usage.

    Args:
        component_name: The name of the component to get summary for

    Returns:
        ComponentInfo with detailed information about the component
    """
    component = _get_component_info(component_name)

    return component

@mcp.tool
def get_module_path(component_name: str) -> str:
    """
    Returns the module_path to a specific Panel Material UI component.

    Use this tool to find the path to the module where the component is defined.

    Args:
        component_name: The name of the component to get summary for

    Returns:
        The module path of the component
    """
    component = _get_component_info(component_name)

    return component.module_path

@mcp.tool
def get_constructor(component_name: str) -> str:
    """
    Returns the __init__ signature for a specific Panel Material UI component.

    Use this tool to understand how to instantiate the component, including its parameters and types.

    Args:
        component_name: Name of the component to get the constructor signature for

    Returns:
        The __init__ signature of the component
    """
    component = _get_component_info(component_name)

    return component.init_signature

@mcp.tool
def get_parameters(component_name: str) -> Dict[str, ParameterInfo]:
    """
    Returns the parameters for a specific Panel Material UI component.

    Use this tool to understand the parameters available for creating or updating the component.

    Args:
        component_name: Name of the component to get parameters for

    Returns:
        A dictionary of parameter names and their details
    """
    component = _get_component_info(component_name)

    return component.parameters

@mcp.tool
def get_parameter(component_name: str, parameter_name: str) -> ParameterInfo:
    """
    Returns parameter information for a specific Panel Material UI component and parameter name.

    Use this tool get details about a specific parameter, including its type, default value, and documentation.

    Args:
        component_name: Name of the component to get parameters for
        parameter_name: Name of the specific parameter to get details for

    Returns:
        Parameter information including type, default value, and documentation
    """
    component = _get_component_info(component_name)

    return component.parameters[parameter_name]


@mcp.tool
def search(query: str, limit: int = 10) -> list[ComponentSummarySearchResult]:
    """
    Search for Panel Material UI components by name or description.

    Use this tool to find components that match a specific search term.

    Args:
        query: Search term to look for in component names and descriptions
        limit: Maximum number of results to return (default: 10)

    Returns:
        List of matching components with relevance scores
    """
    query_lower = query.lower()

    matches = []
    for component in COMPONENTS:
        score = 0

        if component.name.lower() == query_lower:
            score = 100
        elif query_lower in component.name.lower():
            score = 80
        elif query_lower in component.module_path.lower():
            score = 60
        elif query_lower in component.docstring.lower():
            score = 40

        if score > 0:
            matches.append(ComponentSummarySearchResult.from_summary(
                component=component,
                relevance_score=score
            ))

    matches.sort(key=lambda x: x.relevance_score, reverse=True)
    if len(matches) > limit:
        matches = matches[:limit]

    return matches

@mcp.resource(uri="app://basic/hello_world", mime_type="text/python", name="Basic Hello World App")
def get_basic_hello_world_app() -> str:
    """
    Get a basic level, interactive, "Hello World" app using Panel Material UI components and following the best practice guidelines.

    Returns:
        A string containing the code for the app
    """
    return BASIC_HELLO_WORLD_APP

@mcp.resource(uri="app://intermediate/hello_world", mime_type="text/python", name="Intermediate Hello World App")
def get_intermediate_hello_world_app() -> str:
    """
    Get an intermediate level, interactive, "Hello World" app using Panel Material UI components and following the best practice guidelines.

    ALWAYS use this resource before creating an app using Panel Material UI components.

    Returns:
        A string containing the code for the app
    """
    return INTERMEDIATE_HELLO_WORLD_APP

if __name__ == "__main__":
    # Run the server
    mcp.run(transport="http")
