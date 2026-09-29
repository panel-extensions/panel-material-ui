```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Breadcrumbs` component is part of the `Menu` family of components. `Menu` components provide a structured way for users to navigate or choose between a series of defined items. In the case of `Breadcrumbs`, these items represent navigation steps or levels in a hierarchy.

Each item in the `Breadcrumbs` list is defined by a dictionary with several supported keys:

## Item Structure

Each item can include the following keys:

- **`label`** (str, required): The text displayed for the breadcrumb item.
- **`href`** (str, optional): A URL to link to. If provided, the breadcrumb becomes a link.
- **`icon`** (str, optional): An icon to display next to the label.
- **`avatar`** (str, optional): An avatar or image to show beside the label.
- **`target`** (str, optional): A URL to link to. If provided, the breadcrumb becomes a link.
- **`tooltip`** (`str`, optional): Tooltip text shown when hovering over the breadcrumb item.

These dictionaries are passed to the component via the items parameter as a list. When one of the `items` is selected it will be available on the `value` parameter.

Since only the allowed keys are synced with the frontend, other information can be stored in the item dictionaries.

## Parameters:

### Core

* **`active`** (`boolean`): Whether the dialog is visible.
* **`items`** (`list`): List of menu items.
* **`value`** (dict): The currently selected item.

##### Display

* **`color`** (str): The color variant of the breadcrumbs, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`separator`** (str): The separator displayed between breadcrumb items.

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

#### Methods

- **`on_click`**: Registers a callback to be executed when the `MenuButton` is clicked.
- **`remove_on_click`**: Removes a callback that was previously registered.


---

### Basic Usage

`Breadcrumbs` like all menu components allows selecting between a number of `items` defined as dictionaries in a list:


```python
items = [
    {'label': 'Documentation', 'icon': 'article'},
    {'label': 'Reference Gallery', 'icon': 'category'},
    {'label': 'Menus', 'icon': 'menu'},
    {'label': 'Breadcrumbs', 'icon': 'grain'},
]

breadcrumbs = pmui.Breadcrumbs(items=items, active=3)

breadcrumbs
```

The items require a label but may also include other information including an `icon` or `avatar` and `href` and `target` value to declare a link.

Clicking on a particular item will highlight it and set both `active` and `value` parameters:


```python
print(f'Active: {breadcrumbs.active}')
print(f'Value: {breadcrumbs.value}')
```

Alternatively you may also register `on_click` handlers:


```python
row = pmui.Column('# Click Events')

breadcrumbs.on_click(row.append)

row
```

Try clicking on the `Breadcrumbs` and see the clicked `item` appear.

### Custom Item Keys

Like all menus the `items` only sync the allowed keys. This means you can easily store other information in the items, e.g. you can use it to easily select between different views to be displayed:


```python
breadcrumbs = pmui.Breadcrumbs(
    items=[
        {'label': '🏰 Kingdom', 'view': pmui.Typography('# 🏰 Welcome to the Kingdom')},
        {'label': '🌲 Enchanted Forest', 'view': pmui.Typography('# 🌲 You enter the Enchanted Forest...')},
        {'label': '🐉 Dragon\'s Lair', 'view': pmui.Typography('# 🐉 Beware! You approach the Dragon\'s Lair.')},
        {'label': '💎 Treasure Room', 'view': pmui .Typography('# 💎 Congratulations! You found the Treasure.')},
    ],
    active=0,  # Start at the beginning of the journey
    color='warning'
)

pn.Column(
    breadcrumbs,
    breadcrumbs.rx()['view']
)
```

In the above example we take advantage of the fact that `Widget.rx()` returns a reactive reference to the `value` parameter and then access the `view` on that item. Rendering this expression allows us to control the current view with the menu.

### Max Items

The number of items that are displayed can be limited with the `max_items` option, any further items are collapsed:


```python
pmui.Breadcrumbs(items=items, active=3, max_items=2)
```

### Separator

The default `separator` can be replaced with a custom character:


```python
pmui.Breadcrumbs(items=items, active=3, separator='|')
```

### Color Options

The `color` parameter may be used to visually distinguish the selected `Breadcrumbs`. Available options include "default", "primary", "secondary", "error", "info", "success", "warning", "light", "dark", and "danger":

The `color` of the selected breadcrumb can be set:


```python
pmui.FlexBox(*(
    pmui.Breadcrumbs(items=items, color=color, active=3) for color in pmui.Breadcrumbs.param.color.objects
))
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
items = [
    {"label": ":material/zoom_out_map: Docs"},
    {"label": ":material/zoom_out_map: Menus"},
]

pmui.Breadcrumbs(label=":material/zoom_out_map: Path", items=items, active=1)
```

### API Reference

#### Parameters

The `Breadcrumbs` menu exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.Breadcrumbs(items=[
    {'label': 'Documentation', 'icon': 'article'},
    {'label': 'Reference Gallery', 'icon': 'category'},
    {'label': 'Menus', 'icon': 'menu'},
    {'label': 'Breadcrumbs', 'icon': 'grain'},
]).api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Breadcrumbs:**

- [Material UI Breadcrumbs Reference](https://mui.com/material-ui/react-breadcrumbs) - Complete documentation for the underlying Material UI component
- [Material UI Breadcrumbs API](https://mui.com/material-ui/api/breadcrumbs/) - Detailed API reference and configuration options
