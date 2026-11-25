```python
import panel as pn
from panel_material_ui import (
    COLORS, BreakpointSwitcher, Column, RadioButtonGroup, Select
)

pn.extension()
```

The `BreakpointSwitcher` component allows switching between two component implementations based on the declared breakpoint or media-query. This is useful for rendering different components, e.g. two different widgets depending on the current viewport size, e.g. to achieve a more compact layout on mobile devices.

As a reminder, the default breakpoints are defined as:

- `xs`, extra-small: 0px
- `sm`, small: 600px
- `md`, medium: 900px
- `lg`, large: 1200px
- `xl`, extra-large: 1536px

## Parameters:

### Core

* **`breakpoint`** (`Literal["xs", "sm", "md", "lg", "xl"]`): The breakpoint at which to switch from rendering the `small` to the `large` component.
* **`current`** (`Any`): The currently displayed object.
* **`media_query`** (str | None): Media query to use for the breakpoint (takes precedence over breakpoint).
* **`small`** (`Any`): The component to render if the current viewport is smaller than the configured `breakpoint`.
* **`large`** (`Any`): The component to render if the current viewport is larger or equal to the configured `breakpoint`.

---

Let us create a switcher that switches between a `Select` and a `RadioButtonGroup` widget when the viewport grows larger than the `sm` breakpoint.

The `preview` method will create two separate iframes, one with a width just under the breakpoint value and one just above:


```python
switcher = BreakpointSwitcher(
    breakpoint='md',
    small=Select(options=COLORS),
    large=RadioButtonGroup(options=COLORS),
)

Column(
    switcher.preview(width=899, height=100, border='none'),
    switcher.preview(width=900, height=100, border='none')
)   
```

When switching between two widgets like this we recommend using `.jslink` to keep them synchronized:


```python
small = Select(options=COLORS)
large = RadioButtonGroup(options=COLORS)

small.jslink(large, value='value', bidirectional=True);
```

You may also define a custom `media_query` to override the default `breakpoint` based behavior:


```python
switcher = BreakpointSwitcher(
    media_query='(min-width: 800px)',
    small=small,
    large=large,
)

switcher.preview(styles={'resize': 'horizontal', 'overflow': 'hidden'}, sizing_mode='stretch_width', max_width=850, height=100)
```

Try resizing the iframe and watch the widget switch.
