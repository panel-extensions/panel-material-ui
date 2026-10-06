```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Rating` widget allows users to select a rating value, typically visualized as stars or icons. It is ideal for feedback forms, product reviews, and any scenario where a user needs to rate something on a scale.

Discover more about interactive widgets in the [Panel interactivity guides](https://panel.holoviz.org/how_to/interactivity/index.html), or learn about [callbacks and links](https://panel.holoviz.org/how_to/links/index.html) and [declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters

For customization options, see the [Panel Material UI customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (`bool`): Whether the rating is disabled. If True, the user cannot change the rating and it is set to lower opacity.
* **`end`** (`int`): The maximum rating value (number of icons).
* **`readonly`** (`bool`): Whether the rating can be edited.
* **`value`** (`float`): The current rating value.

##### Display

* **`color`** (`str`): The color variant of the icons, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`label`** (str): The title of the widget
* **`only_selected`** (`bool`): Whether to highlight only the selected value.
* **`precision`** (`float`): The precision of the rating value. Default is 1.0.
* **`size`** (`str`): Size of the rating icons (`small`, `medium`, `large`).

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

##### Aliases

For compatibility with Panel certain parameters are allowed as aliases:

- **`name`**: Alias for `label`

___

### Basic Usage

Create a simple rating widget:


```python
rating = pmui.Rating(label='Rate the product', value=3)
rating
```

You can read and set the value programmatically:


```python
rating.value
```

### Maximum Value

Set the maximum rating value using `end`:


```python
pmui.Rating(label='Max 10', end=10, value=7)
```

### Precision

Set the precision using `precision`:


```python
pmui.Rating(label='Rate the product', value=3, precision=0.5)
```

### Size

Choose between small, medium, and large icons:


```python
pmui.FlexBox(
    pmui.Rating(label='Small', size="small", value=2),
    pmui.Rating(label='Medium', size="medium", value=3),
    pmui.Rating(label='Large', size="large", value=4),
)
```

### Only Selected

Highlight only the selected value:


```python
pmui.Rating(label='Only Selected', only_selected=True, value=4)
```

### Disabled

Disable the Rating:


```python
pmui.Rating(label="Disabled", value=4, disabled=True)
```

### Readonly

Make the `Rating` readonly:


```python
pmui.Rating(label="Readonly", value=3, readonly=True)
```

### Loading

Set the `Rating` to loading:


```python
pmui.Rating(label="Readonly", value=3, loading=True)
```

### Icons

Set the `icon` and `empty_icon` to customize the ratings:


```python
pmui.Rating(
    label='Favorite', value=3, icon='favorite', empty_icon='favorite_outlined', color='danger'
)
```

### Example: User Experience Rating


```python
import panel as pn
import panel_material_ui as pmui

pn.extension()

rating = pmui.Rating(label='How was your experience?', value=0, end=5, precision=0.5)

def feedback(val):
    if val == 0:
        return "No rating selected yet."
    return f"Thank you for rating us **{val}** stars!"

pn.Column(
    "## Quick Feedback",
    rating,
    pn.bind(feedback, rating)
)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
pmui.Rating(label="Zoom :material/zoom_out_map:", value=3)
```

## API Reference

Show all parameters and their current values:


```python
pmui.Rating(label='Rating').api(jslink=True)
```

### References

**Panel Documentation:**

- [Panel Interactivity Guides](https://panel.holoviz.org/how_to/interactivity/index.html)
- [Panel Callbacks and Links](https://panel.holoviz.org/how_to/links/index.html)
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html)

**Material UI Rating:**

- [Material UI Rating Reference](https://mui.com/material-ui/react-rating/)
- [Material UI Radping API](https://mui.com/material-ui/api/rating/) - Detailed API reference and configuration options
