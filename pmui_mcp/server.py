#!/usr/bin/env python3
"""
Panel Material UI MCP Server - Composed

This is the main MCP server that composes multiple sub-servers:
- Components server: Panel Material UI component information
- Docs server: Documentation creation guidelines

This demonstrates FastMCP server composition using the import_server method.
"""
import asyncio
from fastmcp import FastMCP

# Import the sub-servers using relative imports
from .components.server import mcp as components_mcp
from .docs.server import docs_mcp


# Create the main composed server
main_mcp = FastMCP(
    name="Panel Material UI Suite",
    instructions="""
    This is a MCP server that provides comprehensive tools for building
    Panel applications with Material UI components and following best practices.

    Use this server to access:
    - Panel Material UI components: Explore and use various components for building interactive applications.
    - Documentation: Get guidelines on how to create documentation for your Panel applications.
    - Best practices: Learn how to structure your Panel applications effectively.
    - Example applications: Get example code to kickstart your Panel projects.
    """
)


async def setup_composed_server():
    """
    Set up the composed server by importing all sub-servers with prefixes.

    This uses static composition (import_server) which copies components
    from sub-servers into the main server with appropriate prefixes.
    """
    # Import components server with 'components' prefix
    await main_mcp.import_server(components_mcp, prefix="components")

    # Import docs server with 'docs' prefix
    await main_mcp.import_server(docs_mcp, prefix="docs")

@main_mcp.prompt(
    "learn",
    description="Learn the basics of the Panel Material UI MCP server",
)
def learn():
    """
    Returns a string explaining how to explore the Panel Material UI MCP Server.

    Use this prompt to learn about Panel Material UI and its MCP server before using it.
    """
    return """
    Welcome to the Panel Material UI MCP Server!

    Please:

    - read the component best practices for both Panel and Panel Material UI
    - read the example applications for Panel Material UI to understand how to use the components effectively
    - explore the available documentation and component tools, resources and prompts
    """

def main():
    """
    Main function to set up and run the composed server.
    """
    # Set up the server composition and run
    async def setup_and_run():
        await setup_composed_server()
        await main_mcp.run_async(transport="http")

    # Run everything in a single event loop
    asyncio.run(setup_and_run())


if __name__ == "__main__":
    # Run the composed server
    main()
