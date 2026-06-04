```python
import panel as pn
import panel_material_ui as pmui
from panel_material_ui import Grid, Paper

pn.extension()
```

The `Grid` component provides a responsively sized layout grid that adapts to screen size and orientation, ensuring consistency across layouts.

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`columns`** (`int | dict`): The number of columns to display in the grid, either as a fixed integer or per breakpoint ('xs', 'm', 'lg').
* **`column_spacing`** (`int`): The spacing between the columns in the grid. Overrides the `spacing` parameter.
* **`container`** (`boolean`): Declares whether the `Grid` is the outer container or an item within the grid.
* **`direction`** (`Literal["row", "column", "column-reverse", "row-reverse"]`): Direction the grid flows in.
* **`row_spacing`** (`int`): The spacing between the rows in the grid. Overrides the `spacing` parameter.
* **`size`** (`int | dict | Literal['grow']`):  The size of the grid. Overrides the `columns` parameter.
* **`spacing`** (`int | dict`): The spacing between the columns and rows in the grid.
___

In order to create a grid layout, you need a container. Use the container prop to create a grid container that wraps the grid items (the Grid is always an item).

Column widths are integer values between 1 and 12. For example, an item with size={6} occupies half of the grid container's width.


```python
item = lambda content: Paper(content, elevation=5, height=100, sizing_mode="stretch_width")

Grid(
    Grid(item('Foo'), size=8),
    Grid(item('Bar'), size=4),
    Grid(item('Baz'), size=4),
    Grid(item('Qux'), size=8),
    container=True, spacing=2, margin=10
)
```

### Breakpoints

Items may have multiple widths defined, causing the layout to change at the defined breakpoint. Width values apply to all wider breakpoints, and larger breakpoints override those given to smaller breakpoints.

For example, a component with `size={ 'xs': 12, 'sm': 6 }` occupies the entire viewport width when the viewport is less than 600 pixels wide. When the viewport grows beyond this size, the component occupies half of the total width—six columns rather than 12.


```python
Grid(
    Grid(item('Foo'), size={"md": 8, "xs": 12}),
    Grid(item('Bar'), size={"md": 4, "xs": 12}),
    Grid(item('Baz'), size={"md": 4, "xs": 12}),
    Grid(item('Qux'), size={"md": 8, "xs": 12}),
    container=True, column_spacing=2, margin=10
)
```

### Spacing

Use the spacing prop to control the space between children. The spacing value can be any positive number (including decimals) or a string. The prop is converted into a CSS property using the theme.spacing() helper.

The following demo illustrates the use of the spacing prop:


```python
spacing = pmui.RadioBoxGroup(options=[0.5, 1, 2, 4, 8], value=2, inline=True, label='Spacing')

spacing_grid = Grid(
    Grid(item('Foo'), size=2),
    Grid(item('Bar'), size=2),
    Grid(item('Baz'), size=2),
    container=True, spacing=spacing, margin=10
)

pmui.Column(spacing_grid, spacing)
```

### Auto-layout

The auto-layout feature gives equal space to all items present. When you set the width of one item, the others will automatically resize to match it.


```python
Grid(
    Grid(item('Foo'), size='grow'),
    Grid(item('Bar'), size=2),
    Grid(item('Baz'), size='grow'),
    container=True, spacing=2, margin=10
)
```
