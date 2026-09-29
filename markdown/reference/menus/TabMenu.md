```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `TabMenu` component is part of the `Menu` family of components. `Menu` components provide a structured way for users to navigate or choose between a series of defined items. In the case of `TabMenu`, these items represent different tabs that allow users to switch between views or sections.

Each item in the `TabMenu` list is defined by a dictionary with several supported keys:

## Item Structure

Each item can include the following keys:

- **`label`** (str, required): The text displayed for the tab item.
- **`href`** (str, optional): A URL to link to. If provided, the tab becomes a link.
- **`icon`** (str, optional): An icon to display next to the label.
- **`avatar`** (str, optional): An avatar or image to show beside the label.
- **`target`** (str, optional): A URL target. If provided, the tab becomes a link with the specified target.
- **`tooltip`** (`str`, optional): Tooltip text shown when hovering over the tab item.

These dictionaries are passed to the component via the items parameter as a list. When one of the `items` is selected it will be available on the `value` parameter.

Since only the allowed keys are synced with the frontend, other information can be stored in the item dictionaries.

## Parameters:

### Core

* **`active`** (`int`): The index of the currently selected tab.
* **`items`** (`list`): List of menu items.
* **`value`** (dict): The currently selected item.

##### Display

* **`color`** (str): The color variant of the tabs, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`centered`** (bool): Whether the tabs should be centered.
* **`icon_position`** (str): Position of the tab icon relative to the label, one of `'start'`, `'end'`, `'top'`, and `'bottom'`
* **`scroll_buttons`** (str): Determine behavior of scroll buttons, one of `'auto'`, `'true'`, or `'false'`.
* **`variant`** (str): The variant of the tabs, one of `'standard'`, `'scrollable'`, or `'fullWidth'`.

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

#### Methods

- **`on_click`**: Registers a callback to be executed when a tab is clicked.
- **`remove_on_click`**: Removes a callback that was previously registered.


---


### Basic Usage

`TabMenu` like all menu components allows selecting between a number of `items` defined as dictionaries in a list:



```python
items = [
    {'label': 'Home', 'icon': 'home'},
    {'label': 'Gallery', 'icon': 'image'},
    {'label': 'Settings', 'icon': 'settings'},
    {'label': 'About', 'icon': 'info'},
]

tab_menu = pmui.TabMenu(items=items, active=0)

tab_menu
```

The items require a label but may also include other information including an `icon` or `avatar` and `href` and `target` value to declare a link.

Clicking on a particular item will highlight it and set both `active` and `value` parameters:



```python
print(f'Active: {tab_menu.active}')
print(f'Value: {tab_menu.value}')
```

Alternatively you may also register `on_click` handlers:


```python
row = pmui.Column('# Click Events')

tab_menu.on_click(row.append)

row
```

Try clicking on the `TabMenu` and see the clicked `item` appear.


### Custom Item Keys

Like all menus the `items` only sync the allowed keys. This means you can easily store other information in the items, e.g. you can use it to easily select between different views to be displayed:



```python
tab_menu = pmui.TabMenu(
    items=[
        {'label': 'Kingdom', 'icon': 'castle', 'view': pmui.Typography('# 🏰 Welcome to the Kingdom')},
        {'label': 'Enchanted Forest', 'icon': 'forest', 'view': pmui.Typography('# 🌲 You enter the Enchanted Forest...')},
        {'label': 'Dragon\'s Lair', 'icon': 'local_fire_department', 'view': pmui.Typography('# 🐉 Beware! You approach the Dragon\'s Lair.')},
        {'label': 'Treasure Room', 'icon': 'diamond', 'view': pmui.Typography('# 💎 Congratulations! You found the Treasure.')},
    ],
    active=0,  # Start at the beginning of the journey
    color='warning'
)

pn.Column(
    tab_menu,
    tab_menu.rx()['view']
)
```

In the above example we take advantage of the fact that `Widget.rx()` returns a reactive reference to the `value` parameter and then access the `view` on that item. Rendering this expression allows us to control the current view with the menu.


### Centered

The `centered` parameter can be used to center the tabs:



```python
pmui.TabMenu(items=items, active=0, centered=True)
```

### Color Options

The `color` parameter may be used to visually distinguish the selected tab. Available options include "default", "primary", "secondary", "error", "info", "success", "warning", "light", "dark", and "danger":

The `color` of the selected tab can be set:



```python
pmui.FlexBox(*(
    pmui.TabMenu(items=items, color=color, active=0, margin=10) for color in pmui.TabMenu.param.color.objects
))
```

### Icon Position

The `icon_position` allows changing where to place the icon relative to the label:


```python
pmui.FlexBox(*(
    pmui.TabMenu(items=items, icon_position=icon_position, active=0, margin=10) for icon_position in pmui.TabMenu.param.icon_position.objects
))
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
items = [
    {"label": ":material/zoom_out_map: Overview"},
    {"label": ":material/zoom_out_map: Details"},
]

pmui.TabMenu(label=":material/zoom_out_map: Sections", items=items, active=0)
```

### API Reference

#### Parameters

The `TabMenu` menu exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:



```python
pmui.TabMenu(items=[
    {'label': 'Home', 'icon': 'home'},
    {'label': 'Gallery', 'icon': 'image'},
    {'label': 'Settings', 'icon': 'settings'},
    {'label': 'About', 'icon': 'info'},
]).api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Tabs:**

- [Material UI Tabs Reference](https://mui.com/material-ui/react-tabs) - Complete documentation for the underlying Material UI component
- [Material UI Tabs API](https://mui.com/material-ui/api/tabs/) - Detailed API reference and configuration options

