```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Pill` widget allows selecting a single value from a list or dictionary of `options` rendered as clickable pills. It is built on top of the [Material UI Chip](https://mui.com/material-ui/react-chip/) component.

The `Pill` widget falls into the broad category of single-value, option-selection widgets that provide a compatible API and include the [`Select`](Select.ipynb), [`AutocompleteInput`](AutocompleteInput.ipynb) and [`RadioButtonGroup`](RadioButtonGroup.ipynb) widgets.

Discover more about using widgets to add interactivity to your applications in the [Make your component interactive](https://panel.holoviz.org/how_to/interactivity/index.html) guide. For linking or callbacks, see the [Links](https://panel.holoviz.org/how_to/links/index.html) and [Param](https://panel.holoviz.org/how_to/param/index.html) guides.

#### Parameters

For details on other options for customizing the component, see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (boolean): Whether the widget is editable.
* **`disabled_options`** (list): Optional list of `options` that are disabled.
* **`options`** (list or dict): A list or dictionary of options to select from.
* **`value`** (object): The current value; must be one of the option values.

##### Display

* **`color`** (str): The color of the selected pill.
* **`label`** (str): The title of the widget.
* **`size`** (str): One of small, medium (default), or large.
* **`variant`** (str): One of filled or outlined (default).

##### Styling

- **`sx`** (dict): Component-level styling API.
- **`theme_config`** (dict): Theming API.

##### Aliases

For compatibility with Panel, certain parameters are allowed as aliases:

- **`name`**: Alias for `label`.

___

### Basic Usage

The `Pill` widget allows selecting a single option:


```python
pill = pmui.Pill(label='Study', options=['Biology', 'Chemistry', 'Physics'], width=200)

pill.show()
```

The `options` parameter also accepts a dictionary where keys are labels:


```python
pmui.Pill(label='Age', options={'Ten': 10, 'Twenty': 20, 'Thirty': 30})
```

### Sizes

Use the `size` parameter to control the chip size:


```python
pmui.FlexBox(
    *(pmui.Pill(label=size, size=size, options=['One', 'Two', 'Three'], value='Two')
      for size in pmui.Pill.param.size.objects)
)
```

### Variants

Choose from `filled` or `outlined` variants:


```python
pmui.FlexBox(
    *(pmui.Pill(label=variant, variant=variant, options=['One', 'Two', 'Three'], value='Two')
      for variant in pmui.Pill.param.variant.objects)
)
```

### Colors

Color is applied to the selected pill:


```python
pmui.FlexBox(
    *(pmui.Pill(label=color, color=color, options=['One', 'Two'], value='Two')
      for color in pmui.Pill.param.color.objects)
)
```

### Disabled and Disabled Options

Disable the whole widget or individual options:


```python
pmui.Column(
    pmui.Pill(label='Disabled', options=['One', 'Two', 'Three'], value='Two', disabled=True),
    pmui.Pill(label='Disabled option', options=['One', 'Two', 'Three'], value='Two', disabled_options=['Two']),
)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
pmui.Pill(
    label="Mode :material/zoom_out_map:",
    options={
        "Zoom :material/zoom_out_map:": "zoom",
        "Explore :material/explore:": "explore",
    },
    value="zoom",
)

```

### Controls

The `Pill` widget exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.Row(pill.controls(jslink=True), pill)
```
