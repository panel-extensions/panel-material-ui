```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `SplitButton` component belongs to the `Menu` family of components. Menu components provide a structured way for users to navigate or choose between a series of defined actions. The `SplitButton` supports two distinct modes:

- **`split`**: In `split` mode, the main button performs a default action, while the dropdown allows users to trigger related but independent actions.
- **`select`**: In `select` mode, users select an option from the menu, and the main button triggers the selected action.

Each item in the `SplitButton` is defined by a dictionary with a required `label` key:

#### Item Structure

Each item dictionary can include the following keys:

- **`label`** (`str`, required): The text displayed for the menu item.
- **`icon`** (`str`, optional): An icon to display next to the label.
- **`icon_size`** (`str`, optional): The size of the icon to display next to the label, e.g. `"12px"` or `"1em"`.
- **`href`** (`str`, optional): A URL to link to. If provided, the menu item becomes a link.
- **`target`** (`str`, optional): Specifies where to open the linked document (e.g., `_blank`).
- **`tooltip`** (`str`, optional): Tooltip text shown when hovering over the menu item.

These dictionaries are passed to the component via the `items` parameter as a list. When an item is selected, it is available on the `value` parameter.

Only the allowed keys are synced with the frontend, but you can store additional information in the item dictionaries for your own use.

#### Parameters

##### Core

* **`active`** (`int`): The index of the currently selected item.
* **`clicks`** (`int`): The number of times the button or a menu item has been clicked.
* **`disabled`** (`bool`): Whether the button is clickable.
* **`items`** (`list`): The menu items to select from.
* **`mode`** (`Literal["split", "select"]`): Switches the button behavior between split and select modes.
* **`value`** (`dict`): The currently selected item.

##### Display

* **`color`** (`str`): The color variant of the button, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`icon`** (`str`): An icon to display to the left of the button label. Either an SVG or an icon name from [Material UI Icons](https://mui.com/material-ui/material-icons).
* **`icon_size`** (`str`): The size of the icons, e.g., `"12px"` or `"1em"`.
* **`label`** (`str`): The title of the widget.
* **`variant`** (`str`): The button style, either `'solid'`, `'outlined'`, or `'text'`.

##### Styling

- **`sx`** (`dict`): Component-level styling API.
- **`theme_config`** (`dict`): Theming API.

#### Methods

- **`on_click`**: Registers a callback to be executed when the `SplitButton` is clicked.

---

## Basic Example


```python
pmui.SplitButton(items=[
    {'label': 'New'},
    {'label': 'Save'},
], label='Save', margin=(5, 5, 150, 5))
```

## Split Mode

In the default `split` mode, the `SplitButton` allows users to trigger actions either by clicking the main button (for a default action) or by selecting a menu item from the dropdown. This is useful when you want to offer a primary action alongside related alternatives.


```python
split_button = pmui.SplitButton(items=[
    {'label': 'New'},
    {'label': 'Save'},
], label='Save')

log = pmui.Column(min_height=100)

def handle_action(event, log=log):
    log.insert(0, f"Event: {event}, Clicks: {split_button.clicks}, Active: {split_button.active}")
    log[:]=log[:3]

split_button.on_click(handle_action)

pmui.Column(split_button, log)
```

In this mode, clicking the main button or a menu item both trigger the `on_click` event and update the `clicks` parameter.

The `on_click` handler receives the `label` when the main button is clicked, and the full item dictionary when a menu item is selected.

### Select mode

In `select` mode, only clicking the main button triggers an event. Selecting a menu item simply changes the default action for the button, but does not immediately trigger an event. This is useful when you want users to choose an action and then confirm it by clicking the button.


```python
select_button = pmui.SplitButton(items=[
    {'label': 'Create a merge commit'},
    {'label': 'Squash and merge'},
    {'label': 'Rebase and merge'},
], mode='select', width=250)

log = pmui.Column(min_height=125, max_height=300)

def handle_action(event, log=log):
    log.insert(0, f"Event: {event}, Clicks: {select_button.clicks}, Active: {select_button.active}")
    log[:] = log[:3]

select_button.on_click(handle_action)

pmui.Column(select_button, log)
```

In this mode, only clicking the main button triggers the `on_click` event and updates the `clicks` parameter.

The `on_click` handler receives the currently selected item when the button is clicked.

### Item href, target, and icon

You can add links and icons to menu items to make them more informative or interactive. For example, you can direct users to external documentation or indicate the purpose of each action visually.


```python
pmui.SplitButton(
    items=[
        {'label': 'Panel Docs', 'href': 'https://panel.holoviz.org', 'icon': 'link', 'target': '_blank'},
        {'label': 'Material UI', 'href': 'https://mui.com', 'icon': 'web', 'target': '_blank'},
    ],
    label='Links',
    icon='link',
    margin=(5, 5, 150, 5), mode="split"
)
```

### Icon and Icon Size

You can set the icon for the SplitButton and the size of all icons including the items:


```python
pmui.SplitButton(
    items=[
        {'label': 'Small', 'icon': 'add', 'icon_size': '0.8em'},
        {'label': 'Medium', 'icon': 'add', 'icon_size': '1em'},
        {'label': 'Large', 'icon': 'add', 'icon_size': '1.5em'},
    ],
    label='Star',
    icon='star',
    icon_size='2em',
    margin=(5, 5, 150, 5)
)
```

### Display Options

#### `color`


```python
pn.GridBox(*(
    split_button.clone(color=color, label=color, width=200)
    for color in pmui.SplitButton.param.color.objects
), ncols=2)
```

### `size`


```python
pn.Row(*(
    split_button.clone(size=size, label=size, width=200)
    for size in pmui.SplitButton.param.size.objects
))
```

#### `variant`


```python
pn.Row(*(
    split_button.clone(variant=variant, label=variant)
    for variant in pmui.SplitButton.param.variant.objects
))
```

### Disabled and Loading


```python
pmui.Row(
    pmui.SplitButton(label='Disabled', items=[{'label': 'A'}], disabled=True),
    pmui.SplitButton(label='Loading', items=[{'label': 'A'}], loading=True),
    height=150
)
```

### Description Tooltip

You can add a tooltip to the SplitButton using the `description` parameter:


```python
pmui.SplitButton(
    label='With Tooltip',
    items=[{'label': 'A'}, {'label': 'B'}],
    description='This SplitButton has a tooltip!',
    margin=(5, 5, 150, 5)
)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
items = [
    {"label": ":material/zoom_out_map: Export"},
    {"label": ":material/zoom_out_map: Share"},
]

pmui.SplitButton(label=":material/zoom_out_map: Actions", items=items)
```

### API Reference

#### Parameters

The `SplitButton` menu exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.SplitButton(items=[
    {'label': 'Download .parquet'},
    {'label': 'Download .xlsx'},
], label='Download .csv').api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI:**

- [Material UI Split Button Reference](https://mui.com/material-ui/react-button-group/#split-button)
