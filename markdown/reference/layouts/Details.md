```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Details` component creates a collapsible container with three expansion states: collapsed, expanded (with scrollable area), and fully expanded. This makes it useful for providing a preview for longer outputs, while still providing an option to expand and view the full content if needed.

## Parameters

### Core

* **`collapsed`** (`boolean`): Whether the details content is collapsed (default=True).
* **`fully_expanded`** (`boolean`): Whether the details are fully expanded with no scrollable area (default=False). Only applies when collapsed is False.
* **`header`** (`Panel component`): Custom component to display in the header bar.
* **`hide_header`** (`boolean`): Whether to hide the header bar.
* **`title`** (`str`): Text to display in the header (overridden by header if set).
* **`scrollable_height`** (`str`): Maximum height of the scrollable area when expanded but not fully expanded (default="200px").

### Style

* **`elevation`** (`int`): The elevation level of the details surface.
* **`header_background`** (`str`): The background color of the header.
* **`header_color`** (`str`): The color of the header text.
* **`header_css_classes`** (`list`): List of CSS classes to apply to the header component.
* **`outlined`** (`boolean`): Whether the details is outlined (default=True).
* **`raised`** (`boolean`): Whether the details appears elevated above the background.
* **`square`** (`boolean`): Whether to disable rounded corners.
* **`title_css_classes`** (`list`): List of CSS classes to apply to the title component.
* **`variant`** (`Literal["elevation", "outlined"]`): Whether to show an outline instead of elevation.

---

The `Details` component accepts arbitrary Panel components like other layouts. It is `collapsed` by default:


```python
code = """
```python
import panel as pn
import panel_material_ui as pmui

pn.extension()

long_content = pn.Column(*[
    pn.pane.Str(f"Item {i}") for i in range(20)
], margin=5)

pmui.Details(
    long_content,
    title='Details'
)
```
"""

code = pn.pane.Markdown(code, margin=0, stylesheets=['.codehilite { margin: 0}'])

details = pmui.Details(code, title='Details', margin=10, collapsed=False)
details
```

The contents of the `Details.objects` list should never be modified individually, because Panel cannot detect when items in that list have changed internally, and will thus fail to update any already-rendered views of those objects. Instead, use the provided methods for adding and removing items from the list. The only change that is safe to make directly to `Details.objects` is to replace the list of objects entirely. As a simple example of using the methods, we might add an additional widget to the details using the append method:



```python
w3 = pmui.Select(options=['A', 'B', 'C'])
details.append(w3)
```

On a live server or in a notebook the details displayed after the previous code cell (above) will dynamically expand in size to accommodate all three widgets and the title. To see the effect in a statically rendered page, we will display the details a second time:



```python
details
```

Whether the Details is collapsed or not can be controlled from Python and Javascript:



```python
print(details.collapsed)
details.collapsed = False
```

## Three Expansion States

The `Details` component has three distinct expansion states:

1. **Collapsed**: Content is hidden (default state)
2. **Expanded (scrollable)**: Content is visible with a scrollable area limited by `max_height`
3. **Fully Expanded**: Content takes up all available space without scrolling

When expanded but not fully expanded, a button appears at the bottom to toggle to fully expanded state:



```python
# Create content that exceeds scrollable_height to demonstrate scrolling
long_content = pmui.Column(*[pn.pane.Str(f"Item {i}") for i in range(20)], margin=5)

details_states = pmui.Details(
    long_content,
    title='Expandable Details',
    collapsed=False,
    fully_expanded=False,
    scrollable_height=250,
    margin=10
)
details_states
```

The `fully_expanded` state can also be controlled programmatically:



```python
details_states.fully_expanded = True
```

## Header

Instead of using a title, a Details may also be given an explicit header that can contain any component, e.g. in this case the Panel logo:



```python
logo = 'https://panel.holoviz.org/_static/logo_horizontal.png'

red   = pn.Spacer(styles=dict(background='red'), height=100, sizing_mode='stretch_width')
green = pn.Spacer(styles=dict(background='green'), height=100, sizing_mode='stretch_width')
blue  = pn.Spacer(styles=dict(background='blue'), height=100, sizing_mode='stretch_width')

pmui.Details(
    red, green, blue,
    header_background='#2f2f2f',
    header_color='white',
    header=pn.panel(logo, height=40),
    width=300,
    collapsed=False
)
```

## Style

By default `Details` elements are `outlined`. The `scrollable_height` parameter controls the scrollable area height when expanded:


```python
content = pn.Column(*[pn.pane.Str(f"Content item {i}") for i in range(10)], margin=5)

pmui.Row(*(
    pmui.Details(
        content,
        title=f'Max height={h}',
        scrollable_height=h,
        collapsed=False,
        margin=10
    )
    for h in range(100, 300, 50)
))
```

Header styling can be customized with `header_background` and `header_color`:



```python
w1 = pmui.TextInput(label='Text:')
w2 = pmui.FloatSlider(label='Slider')

pmui.Details(
    w1, w2,
    title='Styled Header',
    header_background='#1976d2',
    header_color='white',
    collapsed=False,
    margin=10
)
```

## Layout

In general a `Details` does not have to be given an explicit `width`, `height`, or `sizing_mode`, allowing it to adapt to the size of its contents. However in certain cases it can be useful to declare a fixed-size layout, which its responsively sized contents will then fill, making it possible to achieve equal spacing between multiple objects:


```python
red   = pn.Spacer(styles=dict(background='red'), sizing_mode='stretch_both')
green = pn.Spacer(styles=dict(background='green'), sizing_mode='stretch_both')
blue  = pn.Spacer(styles=dict(background='blue'), sizing_mode='stretch_both')

pmui.Details(red, green, blue, scrollable_height=100, height=300, width=200, title='Fixed size', margin=10)
```

When no fixed size is specified the column will expand to accommodate the sizing behavior of its contents:


```python
from bokeh.plotting import figure

p1 = figure(height=250, sizing_mode='stretch_width', margin=5)
p2 = figure(height=250, sizing_mode='stretch_width', margin=5)

p1.line([1, 2, 3], [1, 2, 3])
p2.scatter([1, 2, 3], [1, 2, 3])

pmui.Details(p1, pn.layout.Divider(), p2, title="Responsive", sizing_mode='stretch_width', margin=10)
```
