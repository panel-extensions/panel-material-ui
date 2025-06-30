# Panel Material UI MCP Server

A comprehensive Model Context Protocol (MCP) server that provides intelligent access to Panel Material UI components and documentation. This composed server combines specialized sub-servers to deliver a complete development assistance experience for Panel Material UI applications.

## Purpose

The Panel Material UI MCP Server bridges the gap between developers and comprehensive Panel Material UI resources by providing:

- **Component Intelligence**: Discover, explore, and get code examples for Panel Material UI components
- **Documentation Assistance**: Access structured documentation following the Diataxis framework
- **Contextual Code Help**: Get specific component information and best practices while coding
- **Comprehensive Coverage**: Access to components, guides, tutorials, and reference materials
- **Real-time Access**: Always up-to-date information without leaving your development environment

### Key Features

- 🧩 **Component Discovery**: Find and explore Panel Material UI components with examples
- 🔍 **Smart Documentation Search**: Search across all documentation using natural language
- 📖 **Full Content Access**: Retrieve complete documentation pages and component details
- 🗂️ **Structured Browsing**: List and explore available components and documentation
- 🎯 **Precise Targeting**: Find specific components, guides, or concepts quickly
- 🔗 **Direct Links**: Get URLs to online documentation for sharing and bookmarking

## Architecture

This is a **composed MCP server** that combines two specialized sub-servers:

### Components Server (prefix: `components_`)
- Panel Material UI component information and documentation
- Component discovery and search functionality
- Example applications and code snippets

### Documentation Server (prefix: `docs_`)
- Panel Material UI documentation access following Diataxis framework
- Writing standards and style guides
- Comprehensive documentation search and retrieval

## Usage

### Prerequisites

- Python 3.8 or higher
- Panel Material UI project with components and documentation
- VS Code with GitHub Copilot extension
- FastMCP library (`pip install fastmcp`)

### Running the MCP Server

```bash
# Navigate to the project root
cd /path/to/panel-material-ui

# Run the composed server
python -m pmui_mcp.server
```

The server will start on `http://127.0.0.1:8000/mcp/` by default and automatically compose both sub-servers.

PLEASE NOTE: We are currently using http as *transport* because this is the only method that works when developing remotely with VS Code.

### Using with Copilot in VS Code

#### 1. Configure VS Code Settings

Add the MCP server configuration to your VS Code `settings.json`:

```json
{
    "mcp": {
        "servers": {
            "panel-materialui-server": {
                "type": "http",
                "url": "http://127.0.0.1:8000/mcp/",
                "headers": { "VERSION": "1.2" }
            }
        }
    }
}
```

#### 2. Use Natural Language Queries

Ask Copilot questions about Panel Material UI components and documentation:

**Component Queries:**
```
@panel-materialui-server Find Button component information
@panel-materialui-server Search for input components
@panel-materialui-server Show me layout components with examples
```

**Documentation Queries:**
```
@panel-materialui-server Search documentation about customization
@panel-materialui-server Get the theming guide
@panel-materialui-server Find all how-to guides
```

#### Run tests

```bash
pip install pytest pytest-asyncio fastmcp
python -m pytest tests_pmui_mcp
```

### Available Tools

The composed server provides tools from both sub-servers with appropriate prefixes:

#### Components Server Tools (prefix: `components_`)

- **`components_get_components()`**: List all available Panel Material UI components
- **`components_search_components(query, limit)`**: Search for components by name or functionality
- **`components_get_component(name)`**: Get detailed information about a specific component

#### Documentation Server Tools (prefix: `docs_`)

- **`docs_get_pages()`**: List all available documentation pages
- **`docs_search(query, limit)`**: Search documentation by keywords
- **`docs_get_page(name)`**: Get full content of a documentation page

### Common Use Cases

#### Finding and Using Components
```
"Search for Button components with examples"
"Show me all form input components"
"Get the TextField component documentation"
"Find components for data visualization"
```

#### Exploring Documentation
```
"Search for customization documentation"
"Find getting started guides"
"Show me all available how-to guides"
"Get the API reference documentation"
```

#### Development Workflow
```
"Find components similar to Material-UI TextField"
"Show me examples of reactive components"
"Get theming documentation and Button component info"
"Search for layout components and their usage guides"
```

### Related Projects

- [Panel](https://panel.holoviz.org/) - The high-level app and dashboarding solution for Python
- [Material-UI](https://mui.com/) - React components implementing Google's Material Design
- [FastMCP](https://github.com/jlowin/fastmcp) - A fast, modern Python framework for building MCP servers
