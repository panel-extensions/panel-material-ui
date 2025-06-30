"""
Simple tests for Panel Material UI MCP Server tools endpoints.

Tests the basic functionality of all MCP tools without performance testing.
"""
import pytest
from fastmcp import Client

from pmui_mcp.server import main_mcp, setup_composed_server


@pytest.mark.asyncio
async def test_server_composition():
    """Test that server composition works."""
    await setup_composed_server()

    # Check server name
    assert main_mcp.name == "Panel Material UI Suite"

    # Check instructions exist
    assert main_mcp.instructions is not None
    assert len(main_mcp.instructions) > 0


@pytest.mark.asyncio
async def test_docs_search():
    """Test the docs_search tool."""
    await setup_composed_server()

    client = Client(main_mcp)
    async with client:
        # Test basic search
        result = await client.call_tool("docs_search", {
            "query": "panel",
            "limit": 5
        })

        # Should return some result
        assert result is not None


@pytest.mark.asyncio
async def test_components_search():
    """Test the components_search_components tool."""
    await setup_composed_server()

    client = Client(main_mcp)
    async with client:
        result = await client.call_tool("components_search", {
            "query": "button",
            "limit": 3
        })

        # Should return some result
        assert result is not None


@pytest.mark.asyncio
async def test_components_get_all():
    """Test the components_get_all_components tool."""
    await setup_composed_server()

    client = Client(main_mcp)
    async with client:
        result = await client.call_tool("components_get_all", {})

        # Should return some result
        assert result is not None

@pytest.mark.asyncio
async def test_get_intermediate_hello_world_app():
    """Test the get_intermediate_hello_world_app tool."""
    await setup_composed_server()

    client = Client(main_mcp)
    async with client:
        result = await client.read_resource("app://components/intermediate/hello_world")
        assert result[0].text.startswith("import panel as pn")

@pytest.mark.asyncio
async def test_basic_tools():
    """Test basic tools that should work."""
    await setup_composed_server()

    client = Client(main_mcp)
    async with client:
        # Test docs search (should work)
        docs_result = await client.call_tool("docs_search", {
            "query": "test",
            "limit": 1
        })
        assert docs_result is not None

        # Test components search (should work)
        comp_result = await client.call_tool("components_search", {
            "query": "test",
            "limit": 1
        })
        assert comp_result is not None


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])
