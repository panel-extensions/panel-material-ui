```python
import panel as pn
import panel_material_ui as pmui
from panel_material_ui import Paper

pn.extension()
```

The `Paper` component provides a surface to display content with optional elevation effects.

## Parameters:
For details on other options for customizing the component see the layout and styling how-to guides.

### Core

* **`direction`** (`Literal["row", "column", "column-reverse", "row-reverse"]`): Direction the grid flows in.

### Display

* **`elevation`** (`int`): The elevation level of the card surface.
* **`raised`** (`boolean`): Whether the card appears elevated above the background.
* **`square`** (`boolean`): Whether to disable rounded corners.
* **`variant`** (`Literal["filled", "outlined"]`): Whether to show an outline instead of elevation.

---


```python
size_opts = dict(width=200, height=200, margin=20)

pmui.Row(
    Paper(elevation=0, **size_opts),
    Paper(**size_opts),
    Paper(elevation=3, **size_opts),
    styles={'background-color': '#f0f0f0'}
)
```

### Elevation

Use the elevation prop to establish hierarchy through the use of shadows. The Paper component's default elevation level is 1. The prop accepts values from 0 to 24. The higher the number, the further away the Paper appears to be from its background.

In dark mode, increasing the elevation also makes the background color lighter. This is done by applying a semi-transparent gradient with the background-image CSS property.


```python
size_opts = dict(width=100, height=100, margin=10)

pn.GridBox(
    *(Paper(f'elevation={e}', elevation=e, **size_opts) for e in (0, 1, 2, 3, 4, 8, 16, 24)),
    ncols=4, margin=20
)
```

### Variants

Set the variant prop to "outlined" for a flat, outlined Paper with no shadows:


```python
pmui.Row(
    Paper(variant='outlined', **size_opts),
    Paper(variant='elevation', **size_opts),
    margin=20, styles={'background-color': '#f0f0f0'}
)
```
