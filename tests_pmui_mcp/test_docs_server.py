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
        result = await client.call_tool("search_pages", {
            "query": "panel",
            "limit": 3
        })
        assert result is not None

        # Test get_pages (this should work)
        result = await client.call_tool("get_pages", {})
        assert result is not None


@pytest.mark.asyncio
async def test_docs_server_search():
    """Test docs server search functionality."""
    client = Client(docs_mcp)
    async with client:
        # Test different searches
        result1 = await client.call_tool("search_pages", {
            "query": "components",
            "limit": 5
        })
        assert result1 is not None

        result2 = await client.call_tool("search_pages", {
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
    search_results = collection.search_pages("panel")
    assert isinstance(search_results, list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
