```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Container` component centers content horizontally with responsive padding. 

#### Parameters:

##### Core

* **`disable_gutters`** (`boolean`): If True, removes the default padding on the left and right.
* **`fixed`** (`boolean`): Sets max-width to match min-width of current breakpoint for fixed-width layouts.
* **`width_option`** (`Literal["xs", "sm", "md", "lg", "xl", False]`): Maximum width breakpoint for the container.

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

---

### Basic Uage

A `Container` has two modes, fluid (the default), where the width is bounded by the `width_option`, which corresponds to a breakpoint:


```python
sx = {'boxShadow':'var(--mui-shadows-12)', 'backgroundColor': '#afafaf'}

title = pmui.Typography('Container', height=100, variant='h4')
content = pmui.Typography('This container centers it contents', height=100)

pmui.Container(title, content, sx=sx, width_option='sm')
```

### Fixed

If you want to design for a fixed set of sizes instead of trying to accommodate a fully fluid viewport, you can set the `fixed` parameter. The Container will adapt it's max-width to the min-width of the current breakpoint:


```python
pmui.Container(title, sx=sx, width_option=False, fixed=True)
```

### Gutters

By default the `Container` will have gutters around the contents, you can disable this with `disable_gutters=True`:


```python
pmui.Container(title, sx=sx, width_option='xs', disable_gutters=True)
```

### API Reference

#### Parameters


```python
container = pmui.Container(title, sx=sx, width_option='sm')

pmui.Row(container.controls(jslink=True), container)
```

### References

**Material UI Container:**

- [Material UI Container Reference](https://mui.com/material-ui/react-container/) - Complete documentation for the underlying Material UI component
- [Material UI Container API](https://mui.com/material-ui/api/container/) - Detailed API reference and configuration options
