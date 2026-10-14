```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Typography` component is used to display text with different styles and weights following Material UI's typography system. It provides consistent text styling across your application with predefined variants for headers, body text, and other text elements.

Typography is fundamental to good user interface design as it establishes hierarchy, improves readability, and creates visual consistency. The component supports:

- Semantic HTML heading tags (h1-h6)
- Body text variants with different weights
- Specialized text styles like captions and overlines
- Custom colors and styling options
- Markdown rendering capabilities

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`object`** (str): The text content to display - supports plain text and markdown

##### Display

* **`color`** (str): The color variant of the text, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red) or a valid CSS color value.
* **`variant`** (str): Typography variant that defines the text styling (h1, h2, body1, etc.)

##### Styling

- **`sx`** (dict): Component level styling API for advanced customization
- **`theme_config`** (dict): Theming API for consistent design system integration

___

### Basic Usage

Create typography with different text variants:


```python
simple_text = pmui.Typography("Hello World", variant="h4")
simple_text
```

Typography supports markdown rendering:


```python
markdown_text = pmui.Typography("This is **bold** and *italic* text with [links](https://panel.holoviz.org)")
markdown_text
```

### Variants

Typography supports various predefined variants that follow Material UI's type system:


```python
pmui.Column(
    pmui.Typography("h1 Heading", variant="h1"),
    pmui.Typography("h2 Heading", variant="h2"),
    pmui.Typography("h3 Heading", variant="h3"),
    pmui.Typography("h4 Heading", variant="h4"),
    pmui.Typography("h5 Heading", variant="h5"),
    pmui.Typography("h6 Heading", variant="h6"),
)
```

### Body Text Variants

Different body text styles for various content needs:


```python
pmui.Column(
    pmui.Typography("Body 1 - Regular body text for most content", variant="body1"),
    pmui.Typography("Body 2 - Smaller body text for secondary content", variant="body2"),
    pmui.Typography("Subtitle 1 - Larger subtitle text", variant="subtitle1"),
    pmui.Typography("Subtitle 2 - Smaller subtitle text", variant="subtitle2"),
)
```

### Specialized Text Styles

Typography variants for specific use cases:


```python
pmui.Column(
    pmui.Typography("Caption text - Small descriptive text", variant="caption"),
    pmui.Typography("OVERLINE TEXT - All caps labels", variant="overline"),
    pmui.Typography("Button text", variant="button"),
)
```

### Colors

Customize text colors using Material UI theme colors or CSS values:


```python
pmui.Column(
    pmui.Typography("Primary color text", color="primary", variant="h6"),
    pmui.Typography("Secondary color text", color="secondary", variant="h6"),
    pmui.Typography("Error color text", color="error", variant="h6"),
    pmui.Typography("Custom color text", color="#9c27b0", variant="h6"),
)
```

### Markdown Support

Typography automatically renders markdown content:


```python
markdown_content = """
# Markdown Example

This is **bold text** and *italic text*.

- List item 1
- List item 2
- List item 3

> This is a blockquote

[Link to Panel](https://panel.holoviz.org)
"""

pmui.Typography(markdown_content)
```

### Icon Support

The `Typography` element can display material icons:


```python
pmui.Column(
    pmui.Typography('''<p>Here is an inline lightbulb <span class="material-icons" style="font-size: 1em">lightbulb</span>.
                    And here is a larger, standalone one:</p>'''),
    pmui.Typography('<span class="material-icons" style="font-size: 4em;">lightbulb</span>'),
)
```

### Loading

The `Typography` component can be displayed in a loading state:


```python
pmui.Column(
    pmui.Typography("Loading text", loading=True, variant="body1"),
)
```

### Example: Article Layout

Typography components work well together to create structured content:


```python
pmui.Column(
    pmui.Typography("The Future of Data Visualization", variant="h3", color="primary"),
    pmui.Typography("Published on July 8, 2025", variant="caption", color="text.secondary"),
    pmui.Typography("""
    Data visualization is rapidly evolving with new technologies and methodologies. 
    **Interactive dashboards** are becoming more sophisticated, allowing users to 
    explore data in real-time.
    """, variant="body1"),
    pmui.Typography("Key Technologies", variant="h5"),
    pmui.Typography("""
    - **[Panel](https://panel.holoviz.org/)**: For creating interactive web applications
    - **Bokeh**: For interactive visualizations
    - **HoloViz**: For the complete visualization ecosystem
    """, variant="body2"),
    width=800
)
```

### API Reference

#### Parameters


```python
pmui.Typography("Interactive Typography API", variant="h5").api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using components
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Typography:**

- [Material UI Typography Reference](https://mui.com/material-ui/react-typography/) - Complete documentation for the underlying Material UI component
- [Material UI Typography API](https://mui.com/material-ui/api/typography/) - Detailed API reference and configuration options
