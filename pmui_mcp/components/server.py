"""
Panel Material UI Components MCP Server

This MCP server provides tools and resources for exploring and accessing
Panel Material UI Components.
"""
from typing import Dict, Any

from fastmcp import FastMCP
from pmui_mcp.components.data import get_components
from pmui_mcp.components.models import ComponentInfo, ParameterInfo
from pathlib import Path


# Create the FastMCP server
mcp = FastMCP(
    name="Panel Material UI",
    instructions="""
    This server provides access to [Panel Material UI](https://panel-material-ui.holoviz.org/reference/index.html) component information.

    Panel Material UI Provides a large collection of components for building interactive [Panel](https://panel.holoviz.org/) web applications
    with a Material Design look and feel.

    Available tools:

    - get_best_practices: Get the best practices for using Panel Material UI components. ALWAYS READ THIS BEFORE USING PANEL MATERIAL UI.
    - get_best_practices_panel: Get the best practices for using Panel . ALWAYS READ THIS BEFORE USING PANEL.
    - get_component_info: Get detailed information about a specific component.
    - get_component_constructor: Get the __init__ signature for a specific component
    - get_component_parameter: Get information about a specific parameter of a component
    - get_component_parameters: Get the parameters for a specific component
    - get_component_docs: Returns the reference guide for the component in Markdown format
    - get_component_docs_url: Returns the url for the component documentation
    - get_basic_hello_world_app: Get a "Hello World" Panel app using Panel Material UI components and a basic widget based coding style.
    - get_intermediate_hello_world_app: Get a "Hello World" Panel app using Panel Material UI components and an intermediate param.Parameterized based coding style. ALWAYS READ THIS BEFORE USING PANEL MATERIAL UI.
    - get_all_components: Get a summary of all available components
    - search_components: Search for components by name or description
    """
)


COMPONENTS = get_components()
TEMPLATE_DIR = Path(__file__).parent / "templates"
BEST_PRACTICES = (TEMPLATE_DIR / "best_practices.md").read_text()
BEST_PRACTICES_PANEL = (TEMPLATE_DIR / "best_practices_panel.md").read_text()
BASIC_HELLO_WORLD_APP = (TEMPLATE_DIR / "basic_hello_world_app.py").read_text()
INTERMEDIATE_HELLO_WORLD_APP = (TEMPLATE_DIR / "intermediate_hello_world_app.py").read_text()

@mcp.tool
def get_best_practices() -> str:
    """
    [GUIDELINES] Get the best practices for using Panel Material UI components.

    ALWAYS read this information before using Panel Material UI to ensure
    you are using them correctly and efficiently.

    Returns:
        Best practices guide as markdown text
    """
    return BEST_PRACTICES

@mcp.tool
def get_best_practices_panel() -> str:
    """
    [GUIDELINES] Get the best practices for using Panel.

    ALWAYS read this information before using Panel to ensure
    you are using it correctly and efficiently!

    Returns:
        Best practices guide as markdown text
    """
    return BEST_PRACTICES_PANEL


@mcp.tool
def get_all_components() -> list[dict]:
    """
    [COMPONENT DISCOVERY] List all Panel Material UI components with basic information.

    Returns a summary of all available components including their names,
    descriptions, module paths and documentation url.

    Always read this information before using Panel Material UI to ensure
    you understand which components are available.

    Returns:
        List of dictionaries containing component summary information
    """
    components_list = []

    for component in COMPONENTS:
        components_list.append({
            "name": component.name,
            "module_path": component.module_path,
            "init_signature": component.init_signature,
            "description": component.description,
            "url": component.docs_url
        })

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
def get_component_info(component_name: str) -> ComponentInfo:
    """
    [COMPONENT INFO] Get detailed information about a specific Panel Material UI component.

    Args:
        component_name: The name of the component to get details for

    Returns:
        Detailed component information including parameters, documentation, and examples
    """
    return _get_component_info(component_name)

@mcp.tool
def get_component_docs(component_name: str) -> str:
    """
    [DOCUMENTATION] Get the reference guide documentation for a specific component.

    Args:
        component_name: Name of the component to get documentation for

    Returns:
        The component's reference guide documentation in markdown format
    """
    component = _get_component_info(component_name)

    return component.docs

@mcp.tool
def get_component_docs_url(component_name: str) -> str:
    """
    [DOCUMENTATION] Get the URL to the html reference guide for a specific Panel Material UI component.

    Args:
        component_name: Name of the component to get the URL for

    Returns:
        The URL where the component documentation can be found
    """
    component = _get_component_info(component_name)

    return component.docs_url

@mcp.tool
def get_component_constructor(component_name: str) -> str:
    """
    [COMPONENT INFO] Get the __init__ signature for a specific Panel Material UI component.

    Args:
        component_name: Name of the component to get the constructor signature for

    Returns:
        The __init__ signature of the component
    """
    component = _get_component_info(component_name)

    return component.init_signature

@mcp.tool
def get_component_parameters(component_name: str) -> Dict[str, ParameterInfo]:
    """
    [COMPONENT INFO] Get the parameters for a specific Panel Material UI component.

    Args:
        component_name: Name of the component to get parameters for

    Returns:
        A dictionary of parameter names and their details
    """
    component = _get_component_info(component_name)

    return component.parameters

@mcp.tool
def get_component_parameter(component_name: str, parameter_name: str) -> ParameterInfo:
    """
    [COMPONENT INFO] Get parameter information for a specific Panel Material UI component and parameter name.

    Args:
        component_name: Name of the component to get parameters for
        parameter_name: Name of the specific parameter to get details for

    Returns:
        Parameter information including type, default value, and documentation
    """
    component = _get_component_info(component_name)

    return component.parameters[parameter_name]


@mcp.tool
def search_components(query: str, limit: int = 10) -> Dict[str, Any]:
    """
    [COMPONENT DISCOVERY] Search for Panel Material UI components by name or description.

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
        elif query_lower in component.description.lower():
            score = 40

        if score > 0:
            matches.append({
                "component": {
                    "name": component.name,
                    "description": component.description,
                    "module_path": component.module_path,
                    "url": component.docs_url
                },
                "relevance_score": score
            })

    matches.sort(key=lambda x: x["relevance_score"], reverse=True)

    return {
        "query": query,
        "total_matches": len(matches),
        "results": matches[:limit]
    }

@mcp.tool
def get_basic_hello_world_app() -> str:
    """
    [EXAMPLES] Get a basic level, interactive, "Hello World" app using Panel Material UI components and following the best practice guidelines.

    Returns:
        A string containing the code for the app
    """
    return BASIC_HELLO_WORLD_APP

@mcp.tool
def get_intermediate_hello_world_app() -> str:
    """
    [EXAMPLES] Get an intermediate level, interactive, "Hello World" app using Panel Material UI components and following the best practice guidelines.

    Returns:
        A string containing the code for the app
    """
    return INTERMEDIATE_HELLO_WORLD_APP

if __name__ == "__main__":
    # Run the server
    mcp.run(transport="http")
