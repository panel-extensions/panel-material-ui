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
    This is a MCP server that provides comprehensive tools for building dashboard, data apps and tools using Python,
    [Panel](https://panel.holoviz.org), and [Panel Material UI](https://panel-material-ui.holoviz.org/) components following best practices.

    Use this server to access:

    - Panel Material UI documentation: Explore and study the documentation for building applications with Panel Material UI.
        - Best practices: Learn how to develop your Panel applications using Panel Material UI components effectively.

    ALWAYS read and learn from the best practice documentation resource before using Panel Material UI
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
