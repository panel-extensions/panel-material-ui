"""
Simple tests for the documentation MCP server.

Tests just the docs server functionality without the composed server.
"""
import pytest
from fastmcp import Client

from pmui_mcp.docs.server import docs_mcp, _load_docs_collection


@pytest.mark.asyncio
async def test_docs_server_basic():
    """Test basic docs server functionality."""
    # Test data loading
    collection = _load_docs_collection()
    assert len(collection.pages) > 0

    # Test server with client
    client = Client(docs_mcp)
    async with client:
        # Test search (this should work)
        result = await client.call_tool("search", {
            "query": "panel",
            "limit": 3
        })
        assert result is not None

        # Test get_pages (this should work)
        result = await client.call_tool("get_pages", {})
        assert result is not None

@pytest.mark.asyncio
async def test_get_pages():
    """Test get_page server functionality."""
    client = Client(docs_mcp)
    async with client:
        result = await client.call_tool("get_pages", {})
        assert not "Download this notebook from GitHub" in result[0].text

@pytest.mark.asyncio
async def test_get_best_practices():
    """Test get_best_practices resource functionality."""
    client = Client(docs_mcp)
    async with client:
        result = await client.read_resource("docs://explanation/best_practices")
        assert result[0].text.startswith("# Best Practices")



@pytest.mark.asyncio
async def test_get_reference_page():
    """Test get_reference_page server functionality."""
    # Test server with client
    client = Client(docs_mcp)
    async with client:
        result = await client.call_tool("get_reference_page", {
            "component": "Button"
        })
        assert result[0].text.startswith("# Button\n")

        result = await client.call_tool("get_reference_page", {
            "component": "Card"
        })
        assert result[0].text.startswith("# Card\n")


@pytest.mark.asyncio
async def test_docs_server_search():
    """Test docs server search functionality."""
    client = Client(docs_mcp)
    async with client:
        # Test different searches
        result1 = await client.call_tool("search", {
            "query": "components",
            "limit": 5
        })
        assert result1 is not None

        result2 = await client.call_tool("search", {
            "query": "nonexistent_xyz",
            "limit": 5
        })
        assert result2 is not None


def test_docs_collection_loading():
    """Test that docs collection loads correctly."""
    collection = _load_docs_collection()

    # Should have pages
    assert len(collection.pages) > 0

    # Pages should have required fields
    page = collection.pages[0]
    assert hasattr(page, 'name')
    assert hasattr(page, 'title')
    assert hasattr(page, 'content')
    assert hasattr(page, 'url')

    # Test search functionality
    search_results = collection.search("panel")
    assert isinstance(search_results, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
