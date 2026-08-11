```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Badge` generates a small badge to the top-right (by default) of its child element. Badges are commonly used to display notification counts, status indicators, or short labels overlaid on icons, avatars, or buttons.

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`content`** (int or str): The content rendered within the badge. Typically an integer count but can be a short string. Default is 0.
* **`max`** (int): Maximum count to display. Values above this show as 'max+' (e.g. '99+'). Default is 99.
* **`object`** (Viewable): The child component to wrap with the badge.
* **`show_zero`** (bool): Whether to display the badge when content is zero. Default is False.

##### Display

* **`color`** (str): The color of the badge, which must be one of `'primary'`, `'secondary'`, `'default'`, `'error'`, `'info'`, `'success'`, or `'warning'`.
* **`offset`** (tuple): The (x, y) pixel offset of the badge from its anchor point on the object. Positive x shifts the badge right, positive y down.
* **`overlap`** (str): Wrapped shape the badge should overlap - either 'rectangular' (default) or 'circular'.
* **`placement`** (str): The placement of the badge relative to the child element - options are 'top-right' (default), 'top-left', 'bottom-right', and 'bottom-left'.
* **`variant`** (str): The variant of the badge - either 'standard' (default) or 'dot' for a small dot indicator without content.

##### Styling

- **`sx`** (dict): Component level styling API for advanced customization
- **`theme_config`** (dict): Theming API for consistent design system integration

___

### Basic Usage

Apply a badge to a child component:


```python
pmui.Badge(pmui.IconButton(icon="mail"), content=4, color="primary")
```

### Color

Use the `color` parameter to apply different theme colors:


```python
pmui.Row(
    pn.Column(
    pmui.Badge(pmui.IconButton(icon="mail"), content=4, color="primary"),
    pmui.Badge(pmui.IconButton(icon="mail"), content=4, color="secondary"),
    ),
    pn.Column(pmui.Badge(pmui.IconButton(icon="mail"), content=4, color="success"),
    pmui.Badge(pmui.IconButton(icon="mail"), content=4, color="error"),
    )
).show()
```

### Maximum Value

Use the `max` parameter to cap the displayed value:


```python
pmui.Row(
    pmui.Badge(pmui.IconButton(icon="mail"), content=99, color="secondary"),
    pmui.Badge(pmui.IconButton(icon="mail"), content=100, color="secondary"),
    pmui.Badge(pmui.IconButton(icon="mail"), content=1000, max=999, color="secondary"),
)
```

### Dot Badge

The `dot` variant renders a small dot instead of a count:


```python
pmui.Badge(pmui.IconButton(icon="mail"), variant="dot", color="secondary")
```

### Show Zero

The badge auto-hides when `content` is zero. Override this with `show_zero`:


```python
pmui.Row(
    pmui.Badge(pmui.IconButton(icon="mail"), content=0, color="secondary"),
    pmui.Badge(pmui.IconButton(icon="mail"), content=0, show_zero=True, color="secondary"),
)
```

Note, `visible` hides the entire pane, so set `content=0` and `show_zero=False` to hide the badge but show the pane.


```python
pmui.Row(
    pmui.Badge(pmui.IconButton(icon="mail"), visible=False, color="secondary"),  # hidden
    pmui.Badge(pmui.IconButton(icon="mail"), content=0, show_zero=False, color="secondary")
)
```

### Badge Placement

Use the `placement` parameter to move the badge to any corner:


```python
pmui.Row(
    pmui.Badge(
        pmui.IconButton(icon="mail"), content=1, color="secondary",
        placement="top-right",
    ),
    pmui.Badge(
        pmui.IconButton(icon="mail"), content=2, color="secondary",
        placement="top-left",
    ),
    pmui.Badge(
        pmui.IconButton(icon="mail"), content=3, color="secondary",
        placement="bottom-right",
    ),
    pmui.Badge(
        pmui.IconButton(icon="mail"), content=4, color="secondary",
        placement="bottom-left",
    ),
)
```
