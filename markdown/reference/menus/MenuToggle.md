```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `MenuToggle` component is part of the `Menu` family of components. `Menu` components provide a structured way for users to navigate or choose between a series of defined items. In the case of `MenuToggle`, these items can be individually toggled on/off with different icons for active/inactive states (e.g., filled/unfilled heart for favorites).

Each item in the `MenuToggle` list is defined by a dictionary with several supported keys:

#### Item Structure

Each item can include the following keys:

- **`label`** (str, required): The text displayed for the menu item.
- **`icon`** (str, optional): The icon when the item is not toggled.
- **`active_icon`** (str, optional): The icon when the item is toggled.
- **`toggled`** (list optional): Which indices is currently toggled (default: False).
- **`color`** (str, optional): The color of the menu item.
- **`active_color`** (str, optional): The color when toggled.
- **`tooltip`** (str, optional): Tooltip text shown when hovering over the menu item.

These dictionaries are passed to the component via the items parameter as a list. When one of the `items` is selected it will be available on the `value` parameter, and toggled items are tracked in the `toggled` parameter.

Since only the allowed keys are synced with the frontend, other information can be stored in the item dictionaries.

#### Parameters:

##### Core

* **`active`** (`int`): The last clicked item in the menu.
* **`disabled`** (boolean): Whether the button is clickable.
* **`items`** (`list`): Menu items.
* **`persistent`** (boolean): Whether the menu stays open after toggling an item (default: True).
* **`toggled`** (`list`): List of indices of currently toggled items.
* **`value`** (dict): The last selected item.

##### Display

* **`color`** (str): The color variant of the toggle, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`description`** (str | Bokeh Tooltip | pn.widgets.TooltipIcon): A description which is shown when the widget is hovered.
* **`icon`** (str): An icon to render to the left of the button label. Either an SVG or an icon name which is loaded from [Material UI Icons](https://mui.com/material-ui/material-icons).
* **`icon_size`** (str): Size of the icon as a string, e.g. 12px or 1em.
* **`label`** (str): The title of the widget.
* **`toggle_icon`** (str): Icon to display when menu is open (if different from base icon).
* **`variant`** (str): The button style, either 'solid', 'outlined', 'text'.

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

---

### Basic Usage

`MenuToggle` allows toggling individual items on/off with different icons for each state:


```python
menu_toggle = pmui.MenuToggle(items=[
    {'label': 'Favorite', 'icon': 'favorite_border', 'active_icon': 'favorite', 'toggled': False},
    {'label': 'Bookmark', 'icon': 'bookmark_border', 'active_icon': 'bookmark', 'toggled': True},
    {'label': 'Star', 'icon': 'star_border', 'active_icon': 'star', 'toggled': False},
], label='Actions', icon='more_vert')

pmui.Column(menu_toggle, height=150)
```

The items require a label but may also include `icon`, `active_icon` to show different states, and `toggled` to set the initial state.

Clicking on a particular item will toggle it and update the `toggled` parameter:


```python
print(f'Menu Open: {menu_toggle.active}')
print(f'Value: {menu_toggle.value}')
print(f'Toggled Items: {menu_toggle.toggled}')
```

Alternatively you may also register `on_click` handlers:


```python
row = pmui.Column('### Click Events')

menu_toggle.on_click(row.append)

pmui.Row(menu_toggle, row, height=150)
```

Try clicking on the `MenuToggle` items and see them toggle between their inactive and active states.

### Persistent vs Non-Persistent Mode

By default, `MenuToggle` is in persistent mode (`persistent=True`), meaning the menu stays open after toggling items. This is useful when you want to toggle multiple items:


```python
# Persistent mode (default) - menu stays open
filters_toggle = pmui.MenuToggle(
    label="Filters",
    icon="filter_list",
    persistent=True,
    items=[
        {'label': 'High Priority', 'icon': 'flag', 'color': '#ff9800', 'active_color': '#f44336', 'toggled': True},
        {'label': 'In Progress', 'icon': 'pending', 'color': '#2196f3', 'active_color': '#1976d2'},
        {'label': 'Completed', 'icon': 'check_circle_outline', 'active_icon': 'check_circle', 'color': '#757575', 'active_color': '#4caf50'},
    ]
)

# Non-persistent mode - menu closes after selection
quick_toggle = pmui.MenuToggle(
    label="Quick Actions",
    icon="flash_on",
    persistent=False,
    items=[
        {'label': 'Enable Notifications', 'icon': 'notifications_off', 'active_icon': 'notifications_active'},
        {'label': 'Dark Mode', 'icon': 'light_mode', 'active_icon': 'dark_mode'},
    ]
)

pmui.Row(
    pmui.Column('### Persistent Mode', filters_toggle, height=200),
    pmui.Column('### Non-Persistent Mode', quick_toggle, height=200)
)
```

In persistent mode, you can toggle multiple items without the menu closing. In non-persistent mode, the menu closes after each selection.

### Colored Items

MenuToggle items can have different colors in their normal and toggled states:


```python
colored_menu = pmui.MenuToggle(
    label="Priority Levels",
    icon="flag",
    items=[
        {'label': 'Critical', 'icon': 'error_outline', 'active_icon': 'error', 'color': '#ff5252', 'active_color': '#d32f2f'},
        {'label': '---'},  # Divider
        {'label': 'High', 'icon': 'priority_high', 'color': '#ff9800', 'active_color': '#f57c00'},
        {'label': 'Medium', 'icon': 'remove', 'color': '#2196f3', 'active_color': '#1976d2'},
        {'label': 'Low', 'icon': 'arrow_downward', 'color': '#4caf50', 'active_color': '#388e3c'},
    ]
)

pmui.Column(colored_menu, height=250)
```

### Programmatic Control

You can programmatically control which items are toggled:


```python
programmatic_toggle = pmui.MenuToggle(
    label="Select Items",
    items=[
        {'label': 'Option A', 'icon': 'check_box_outline_blank', 'active_icon': 'check_box'},
        {'label': 'Option B', 'icon': 'check_box_outline_blank', 'active_icon': 'check_box'},
        {'label': 'Option C', 'icon': 'check_box_outline_blank', 'active_icon': 'check_box'},
        {'label': 'Option D', 'icon': 'check_box_outline_blank', 'active_icon': 'check_box'},
    ]
)

toggle_all = pmui.Button(
    label="Toggle All",
    on_click=lambda e: setattr(
        programmatic_toggle, 
        'toggled',
        [] if len(programmatic_toggle.toggled) == 4 else [0, 1, 2, 3]
    )
)

clear_all = pmui.Button(
    label="Clear All",
    on_click=lambda e: setattr(programmatic_toggle, 'toggled', [])
)

pmui.Column(
    programmatic_toggle,
    pmui.Row(toggle_all, clear_all),
    height=200
)
```

### Real-World Example: Bookmark System


```python
# Create a bookmark toggle menu
bookmarks = pmui.MenuToggle(
    label="Bookmarks",
    icon="bookmarks",
    toggle_icon="bookmark",
    items=[
        {'label': 'Dashboard', 'icon': 'bookmark_border', 'active_icon': 'bookmark', 'page': '# 📊 Dashboard\n\nKey metrics and analytics'},
        {'label': 'Reports', 'icon': 'bookmark_border', 'active_icon': 'bookmark', 'page': '# 📈 Reports\n\nMonthly and quarterly reports'},
        {'label': 'Settings', 'icon': 'bookmark_border', 'active_icon': 'bookmark', 'page': '# ⚙️ Settings\n\nConfigure your preferences'},
        {'label': 'Profile', 'icon': 'bookmark_border', 'active_icon': 'bookmark', 'page': '# 👤 Profile\n\nManage your account'},
    ]
)

# Display bookmarked items
bookmarked_display = pn.pane.Markdown("### Bookmarked Pages")

def update_bookmarks(event=None):
    bookmarked_items = [bookmarks.items[i] for i in bookmarks.toggled]
    if bookmarked_items:
        content = "### Bookmarked Pages\n\n"
        for item in bookmarked_items:
            content += f"- **{item['label']}**\n"
    else:
        content = "### Bookmarked Pages\n\n*No pages bookmarked yet*"
    bookmarked_display.object = content

bookmarks.param.watch(update_bookmarks, 'toggled')
update_bookmarks()

pmui.Column(
    bookmarks,
    bookmarked_display,
    height=300
)
```

### Color Options


```python
pn.GridBox(*(
    menu_toggle.clone(color=color, label=color.title())
    for color in pmui.MenuToggle.param.color.objects
), ncols=3)
```

### Variants


```python
pn.Row(*(
    menu_toggle.clone(variant=variant, label=variant.title())
    for variant in pmui.MenuToggle.param.variant.objects
))
```

### Use Cases


```python
# Different use cases for MenuToggle
use_cases = pmui.Tabs(
    ('Favorites', pmui.MenuToggle(
        label="Favorite Items",
        icon="grade",
        items=[
            {'label': 'Product A', 'icon': 'star_border', 'active_icon': 'star'},
            {'label': 'Product B', 'icon': 'star_border', 'active_icon': 'star', 'toggled': True},
            {'label': 'Product C', 'icon': 'star_border', 'active_icon': 'star'},
        ]
    )),
    ('Feature Flags', pmui.MenuToggle(
        label="Features",
        icon="tune",
        items=[
            {'label': 'Beta Features', 'icon': 'toggle_off', 'active_icon': 'toggle_on', 'toggled': True},
            {'label': 'Analytics', 'icon': 'toggle_off', 'active_icon': 'toggle_on'},
            {'label': 'Debug Mode', 'icon': 'toggle_off', 'active_icon': 'toggle_on'},
        ]
    )),
    ('Multi-Select', pmui.MenuToggle(
        label="Select Tags",
        icon="label",
        items=[
            {'label': 'Important', 'icon': 'label_outline', 'active_icon': 'label', 'color': '#f44336'},
            {'label': 'Work', 'icon': 'label_outline', 'active_icon': 'label', 'color': '#2196f3'},
            {'label': 'Personal', 'icon': 'label_outline', 'active_icon': 'label', 'color': '#4caf50'},
            {'label': 'Urgent', 'icon': 'label_outline', 'active_icon': 'label', 'color': '#ff9800'},
        ]
    )),
)

use_cases
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
items = [
    {"label": ":material/zoom_out_map: Favorite", "toggled": True},
    {"label": ":material/zoom_out_map: Follow"},
]

pmui.MenuToggle(label=":material/zoom_out_map: Toggles", items=items, icon="more_vert")
```

### API Reference

#### Parameters

The `MenuToggle` menu exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.MenuToggle(items=[
    {'label': 'Favorite', 'icon': 'favorite_border', 'active_icon': 'favorite'},
    {'label': 'Bookmark', 'icon': 'bookmark_border', 'active_icon': 'bookmark'},
    {'label': 'Star', 'icon': 'star_border', 'active_icon': 'star'},
], label='Actions', icon='more_vert').api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Toggle Button:**

- [Material UI Toggle Button Reference](https://mui.com/material-ui/react-toggle-button) - Complete documentation for the underlying Material UI component
- [Material UI Toggle Button API](https://mui.com/material-ui/api/toggle-button/) - Detailed API reference and configuration options

**Material UI Menu:**

- [Material UI Menu Reference](https://mui.com/material-ui/react-menu) - Complete documentation for the underlying Material UI component
- [Material UI Menu API](https://mui.com/material-ui/api/menu/) - Detailed API reference and configuration options
