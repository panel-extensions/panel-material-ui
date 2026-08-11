```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `MenuList` component is part of the `Menu` family of components. `Menu` components provide a structured way for users to navigate or choose between a series of defined items. In the case of `MenuList`, these items represent a series of menu options, which may also be nested in a tree.

Each item in the `MenuList` list is defined by a dictionary with several supported keys:

## Item Structure

Each item can include the following keys:

- **`label`** (`str`, required): The text displayed for the breadcrumb item.
- **`href`** (`str`, optional): A URL to link to. If provided, the breadcrumb becomes a link.
- **`icon`** (`str`, optional): An icon to display next to the label.
- **`avatar`** (`str`, optional): An avatar or image to show beside the label.
- **`secondary`** (`str`, optional): The secondary text, e.g. for describing the item.
- **`color`** (`str`, optional): The color of the list item (optional)
- **`items`** (`list[dict]`, optional): Nested items.
- **`actions`** (`list`, optional): Each menu item can have a list of actions associated with it which are accessible via a menu.
- **`selectable`** (`boolean`, optional): Whether this item can be selected.
- **`open`** (`boolean`, optional): Whether the menu item should be expanded by default (defaults to `True`).
- **`tooltip`** (`str`, optional): Tooltip text shown when hovering over the menu item.

These dictionaries are passed to the component via the items parameter as a list. When one of the `items` is selected it will be available on the `value` parameter.

Since only the allowed keys are synced with the frontend, other information can be stored in the item dictionaries.

## Parameters:

### Core

* **`active`** (`int | tuple[int, ...]`): Index of the selected item (`int` if flat, `tuple` if nested).
* **`disabled`** (`boolean`): Whether the menu is disabled.
* **`expanded`** (`list[int | tuple[int, ...]]`): Indexes of expanded nodes.
* **`items`** (`list[dict]`): Menu items to select from.
* **`value`** (`dict`): The currently selected item.

##### Display

* **`color`** (`str`): The color variant indicating the selected list item, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`dense`** (`boolean`): Whether to show the list items in a dense format, i.e. reduced margins.
* **`highlight`** (`boolean`): Whether to highlight the currently selected menu item.
* **`level_indent`** (`int`): Number of pixels each nested level is indented by.
* **`show_children`** (`boolean`): Whether to render child items nested under `'items'`.

##### Styling

- **`sx`** (`dict`): Component level styling API.
- **`theme_config`** (`dict`): Theming API.

---

Like all `Menu`-like components `MenuList` accepts a list of `items`, which each support sub-`items`:


```python
items = [
    {'label': 'Home', 'icon': 'home', 'secondary': 'Overview page'},
    {'label': 'Gallery', 'icon': 'image', 'secondary': 'Visual overview'},
    {'label': 'API', 'icon': 'code', 'secondary': 'API Reference'},
    {'label': 'About', 'icon': 'info'},
]

menu_list = pmui.MenuList(items=items, active=3)

menu_list
```

Clicking on a particular item will highlight it and set both `active` and `value` parameters:


```python
menu_list.active, menu_list.value
```

## Nested Items

Items may also contain sub-`items` making it possible to create a tree-like menu. You can also make items non-`selectable` and control the `expanded` state using the parameter. Much like `active` the `expanded` parameter represents a list of indexes to the selected items:


```python
nested_list = pmui.MenuList(
    items=[
        {
            'label': 'Home',
            'icon': 'home',
            'secondary': 'Overview page',
            'items': [
                {'label': 'Welcome', 'icon': 'handshake'},
                {'label': 'Getting Started', 'icon': 'rocket'}
            ]
        },
        {
            'label': 'Gallery',
            'icon': 'image',
            'secondary': 'Visual overview',
            'selectable': False,
            'items': [
                {'label': 'Charts', 'icon': 'stacked_line_chart'},
                {'label': 'Maps', 'icon': 'map'},
                {'label': 'Animations', 'icon': 'animation'}
            ]
        },
        {
            'label': 'API',
            'icon': 'code',
            'secondary': 'API Reference',
            'items': [
                {'label': 'Endpoints', 'icon': 'terminal'},
                {'label': 'Schemas', 'icon': 'schema'}
            ]
        },
        {
            'label': 'About',
            'icon': 'info',
            'items': [
                {'label': 'Team', 'icon': 'groups'},
                {'label': 'Contact', 'icon': 'mail'}
            ]
        },
    ],
    dense=True,
    expanded=[0, 1]
)

nested_list
```

### Actions

`MenuList` items may also have a list of actions associated with it, which will be rendered into a menu:


```python
actions = [
    {'label': 'Favorite', 'icon': 'star', 'inline': True},
    {'label': 'Edit', 'icon': 'edit'},
    {'label': 'Delete', 'icon': 'delete'}
]

list_with_actions = pmui.MenuList(
    items=[
        {
            'label': 'Notebook 1',
            'icon': 'book',
            'secondary': 'Last edited: Today',
            'actions': actions
        },
        {
            'label': 'Notebook 2',
            'icon': 'book',
            'secondary': 'Last edited: Yesterday',
            'actions': actions
        },
        {
            'label': 'Notebook 3',
            'icon': 'book',
            'secondary': 'Last edited: Last week',
            'actions': actions
        },
    ]
)

actions = pn.Column()

list_with_actions.on_action('Favorite', lambda item: actions.append(f"Favorited {item['label']}"))
list_with_actions.on_action('Edit', lambda item: actions.append(f"Edited {item['label']}"))
list_with_actions.on_action('Delete', lambda item: actions.append(f"Deleted {item['label']}"))

pmui.Row(list_with_actions, actions)
```

### Toggle Actions

Inline `MenuList` actions may also be defined as toggles, switching between `True` and `False` states. This can be enabled by setting `toggle=True`. In this mode a few additional configuration options become available for the action:

- `active_icon`: The icon rendered when the toggle value is True.
- `active_color`: The color of the `active_icon` when the toggle value is True.
- `value`: The current value of the toggle (True or False).

For example here we render a toggle to favorite various notebooks:


```python
actions = [
    {'label': 'Favorite', 'icon': 'star_outline', 'active_icon': 'star', 'color': 'warning', 'inline': True, 'toggle': True, 'value': False},
]
list_with_toggle_action = pmui.MenuList(
    items=[
        {
            'label': 'Notebook 1',
            'icon': 'book',
            'actions': actions
        },
        {
            'label': 'Notebook 2',
            'icon': 'book',
            'actions': actions
        },
        {
            'label': 'Notebook 3',
            'icon': 'book',
            'actions': actions
        },
    ]
)

toggle_actions = pn.Column()

list_with_toggle_action.on_action('Favorite', lambda item: toggle_actions.append(f'{item["label"]}: {item["actions"][0]["value"]}'))

pn.Row(list_with_toggle_action, toggle_actions)
```

The `True`/`False` state of the toggle will be updated on the "value" key of the actions:


```python
list_with_toggle_action.items
```

### Display Options

#### `collapsed`

The `collapsed` parameter allows toggling between a view showing just the icons to the expanded view:


```python
collapsed = pmui.Switch(label='Collapsed', value=True)

pmui.Column(collapsed, pmui.MenuList(items=items, active=2, collapsed=collapsed))
```

#### `color`

`MenuList` supports different `color`s to indicate which item is selected:


```python
pn.GridBox(*(
    menu_list.clone(color=color, label=color, active=0, highlight=True)
    for color in pmui.MenuList.param.color.objects
), ncols=5)
```

#### `highlight`

Highlighting can be disabled entirely by setting `highlight=False`:


```python
pmui.MenuList(items=items, highlight=False, active=2)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
items = [
    {"label": ":material/zoom_out_map: Overview"},
    {"label": ":material/zoom_out_map: Details"},
]

pmui.MenuList(label=":material/zoom_out_map: Sections", items=items, active=0)
```

### API Reference

#### Parameters

The `MenuList` exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.MenuList(items=[
    {'label': 'Open', 'icon': 'description'},
    {'label': 'Save', 'icon': 'save'},
    {'label': 'Exit', 'icon': 'close'},
], label='File').api(jslink=True)
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
