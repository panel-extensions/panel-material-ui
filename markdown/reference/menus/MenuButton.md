```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `MenuButton` component is part of the `Menu` family of components. `Menu` components provide a structured way for users to navigate or choose between a series of defined items. In the case of `MenuItem`, these items represent a series of actions to select from after opening the menu on a button click.

Each item in the `MenuButton` list is defined by a dictionary with several supported keys:

#### Item Structure

Each item can include the following keys:

- **`label`** (`str`, required): The text displayed for the menu item.
- **`icon`** (`str`, optional): An icon to display next to the label.
- **`icon_size`** (`str`, optional): The size of the icon to display next to the label, e.g. `"12px"` or `"1em"`.
- **`href`** (`str`, optional): A URL to link to. If provided, the menu item becomes a link.
- **`target`** (`str`, optional): Specifies where to open the linked document (e.g., `_blank`).
- **`tooltip`** (`str`, optional): Tooltip text shown when hovering over the menu item.

These dictionaries are passed to the component via the items parameter as a list. When one of the `items` is selected it will be available on the `value` parameter.

Since only the allowed keys are synced with the frontend, other information can be stored in the item dictionaries.

#### Parameters:

##### Core

* **`active`** (`boolean`): Whether the dialog is visible.
* **`disabled`** (boolean): Whether the button is clickable.
* **`items`** (`list`): Menu  items to select from.
* **`value`** (dict): The currently selected item.

##### Display

* **`color`** (str): A button theme; should be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`description`** (str | Bokeh Tooltip | pn.widgets.TooltipIcon): A description which is shown when the widget is hovered.
* **`icon`** (str): An icon to render to the left of the button label. Either an SVG or an icon name which is loaded from [Material UI Icons](https://mui.com/material-ui/material-icons).
* **`icon_size`** (str): Size of the icon as a string, e.g. 12px or 1em.
* **`label`** (str): The title of the widget.
* **`variant`** (str): The button style, either 'solid', 'outlined', 'text'.

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

---

### Basic Usage

`MenuButton` like all menu components allows selecting between a number of `items` defined as dictionaries in a list:


```python
menu_button = pmui.MenuButton(items=[
    {'label': 'Open', 'icon': 'description'},
    {'label': 'Save', 'icon': 'save'},
    {'label': 'Exit', 'icon': 'close'},
], label='File', icon='storage')

pmui.Column(menu_button, height=150)
```

The items require a label but may also include other information including an `icon` or `avatar` and `href` and `target` value to declare a link.

Clicking on a particular item will highlight it and set both `active` and `value` parameters:


```python
print(f'Active: {menu_button.active}')
print(f'Value: {menu_button.value}')
```

Alternatively you may also register `on_click` handlers:


```python
row = pmui.Column('# Click Events')

menu_button.on_click(row.append)

row
```

Try clicking on the `MenuButton` and see the clicked `item` appear.

### Custom Item Keys

Like all menus the `items` only sync the allowed keys. This means you can easily store other information in the items, e.g. you can use it to easily select between different views to be displayed:


```python
breadcrumbs = pmui.MenuButton(
    items=[
        {'label': '🏰 Kingdom', 'view': pmui.Typography('# 🏰 Welcome to the Kingdom')},
        {'label': '🌲 Enchanted Forest', 'view': pmui.Typography('# 🌲 You enter the Enchanted Forest...')},
        {'label': '🐉 Dragon\'s Lair', 'view': pmui.Typography('# 🐉 Beware! You approach the Dragon\'s Lair.')},
        {'label': '💎 Treasure Room', 'view': pmui .Typography('# 💎 Congratulations! You found the Treasure.')},
    ],
    label='Select a menu item',
    active=0,  # Start at the beginning of the journey
    color='warning'
)

pn.Column(
    breadcrumbs,
    pn.param.ParamRef(breadcrumbs.rx()['view']),
    height=300
)
```

In the above example we take advantage of the fact that `Widget.rx()` returns a reactive reference to the `value` parameter and then access the `view` on that item. Rendering this expression allows us to control the current view with the menu.

### Separators

The `MenuButton` also allows separating options into groups by adding a `None` in between:


```python
separated_menu = pmui.MenuButton(label="File", icon="save", items=[
    {"label": "License", "icon": "law"},
    None,
    {"label": "About", "icon": "info"}
])

pmui.Column(separated_menu, height=150)
```

### Disabled and Loading

Like any other widget the `MenuButton` can be `disabled` and / or set to `loading`:


```python
pmui.MenuButton(label="Loading", disabled=True, loading=True, color="primary")
```

### Color Options


```python
pn.GridBox(*(
    menu_button.clone(color=color)
    for color in pmui.MenuButton.param.color.objects
), ncols=2)
```

### Sizes

For larger or smaller buttons, use the `size` parameter.


```python
pmui.Column(
    pmui.Row(
        pmui.MenuButton(size="small", label="Small", align="center"), 
        pmui.MenuButton(size="medium", label="Medium", align="center"),
        pmui.MenuButton(size="large", label="Large", align="center"),
    ),
)
```

### Variants


```python
pmui.Row(*(
    menu_button.clone(variant=variant)
    for variant in pmui.MenuButton.param.variant.objects
))
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
items = [
    {"label": ":material/zoom_out_map: Open"},
    {"label": ":material/zoom_out_map: Save"},
]

pmui.MenuButton(label=":material/zoom_out_map: File", items=items, icon="storage")
```

### API Reference

#### Parameters

The `MenuButton` menu exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.MenuButton(items=[
    {'label': 'Open', 'icon': 'description'},
    {'label': 'Save', 'icon': 'save'},
    {'label': 'Exit', 'icon': 'close'},
], label='File', icon='storage').api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Button:**

- [Material UI Button Reference](https://mui.com/material-ui/react-breadcrumbs) - Complete documentation for the underlying Material UI component
- [Material UI Button API](https://mui.com/material-ui/api/breadcrumbs/) - Detailed API reference and configuration options

**Material UI Menu:**

- [Material UI Menu Reference](https://mui.com/material-ui/react-menu) - Complete documentation for the underlying Material UI component
- [Material UI Menu API](https://mui.com/material-ui/api/menu/) - Detailed API reference and configuration options
