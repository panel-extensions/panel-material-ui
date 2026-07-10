```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `MenuBar` component provides a horizontal application menu bar, similar to those found in desktop applications (File, Edit, View, Help). It supports nested submenus, keyboard shortcut hints, icons, checkboxes, radio groups, item groups, and dividers.

## Item Structure

The top-level `items` list defines the menu triggers (buttons) in the bar. Each top-level item should have:

- **`label`** (`str`, required): The button text.
- **`icon`** (`str`, optional): Icon displayed before the label.
- **`disabled`** (`bool`, optional): Whether the entire menu is disabled.
- **`items`** (`list[dict]`, required): The dropdown items for this menu.

Each dropdown item can be:

- A **regular item**: `{'label': 'Save', 'icon': 'save', 'hint': 'Ctrl+S'}`
- A **divider**: `None` or `{'label': '---'}`
- A **submenu**: `{'label': 'Share', 'icon': 'share', 'items': [...]}`
- A **group header**: `{'label': 'Alignment', 'group': True, 'items': [...]}`
- A **checkbox item**: `{'label': 'Show Toolbar', 'checkbox': True}`
- A **radio item**: `{'label': 'Light', 'radio': 'light'}`

## Parameters

### Core

- **`active`** (`tuple[int, ...]`): Index path of the last clicked item.
- **`items`** (`list[dict]`): Top-level menus with their dropdown items.
- **`value`** (`dict`): The last clicked item.

### Display

- **`color`** (`str`): Color of the menu bar buttons. One of `'default'`, `'primary'`, `'secondary'`, `'success'`, `'info'`, `'warning'`, `'error'`.
- **`size`** (`str`): Size of the menu buttons: `'small'`, `'medium'`, or `'large'`.
- **`variant`** (`str`): Visual style of the bar container: `'elevation'` or `'outlined'`.

### Styling

- **`sx`** (`dict`): Component-level styling API.
- **`theme_config`** (`dict`): Theming API.

---

## Basic Usage

A simple menu bar with File, Edit, and Help menus:


```python
menu_bar = pmui.MenuBar(items=[
    {'label': 'File', 'items': [
        {'label': 'New', 'icon': 'note_add', 'hint': 'Ctrl+N'},
        {'label': 'Open', 'icon': 'folder_open', 'hint': 'Ctrl+O'},
        {'label': 'Save', 'icon': 'save', 'hint': 'Ctrl+S'},
        {'label': 'Save As...', 'icon': 'save_as', 'hint': 'Ctrl+Shift+S'},
        None,
        {'label': 'Exit', 'icon': 'close'},
    ]},
    {'label': 'Edit', 'items': [
        {'label': 'Undo', 'icon': 'undo', 'hint': 'Ctrl+Z'},
        {'label': 'Redo', 'icon': 'redo', 'hint': 'Ctrl+Y'},
        None,
        {'label': 'Cut', 'icon': 'content_cut', 'hint': 'Ctrl+X'},
        {'label': 'Copy', 'icon': 'content_copy', 'hint': 'Ctrl+C'},
        {'label': 'Paste', 'icon': 'content_paste', 'hint': 'Ctrl+V'},
    ]},
    {'label': 'Help', 'items': [
        {'label': 'Documentation', 'icon': 'menu_book'},
        {'label': 'About', 'icon': 'info'},
    ]},
], margin=(0, 0, 200, 0))

menu_bar
```

Clicking an item updates both `active` (the index path) and `value` (the item dict):


```python
menu_bar.active, menu_bar.value
```

## Nested Submenus

Items with an `items` key (and no `group` key) render as fly-out submenus:


```python
pmui.MenuBar(items=[
    {'label': 'File', 'items': [
        {'label': 'New', 'icon': 'note_add'},
        {'label': 'Open Recent', 'icon': 'history', 'items': [
            {'label': 'project_v2.py'},
            {'label': 'analysis.ipynb'},
            {'label': 'dashboard.py'},
        ]},
        None,
        {'label': 'Share', 'icon': 'share', 'items': [
            {'label': 'Email Link', 'icon': 'email'},
            {'label': 'Copy Link', 'icon': 'link'},
            {'label': 'Export PDF', 'icon': 'picture_as_pdf'},
        ]},
        None,
        {'label': 'Close', 'icon': 'close', 'hint': 'Ctrl+W'},
    ]},
], margin=(0, 0, 200, 0))
```

## Checkbox Items

Items with a `checkbox` key render a checkbox. The value toggles when clicked and updates the `items` in-place:


```python
view_menu = pmui.MenuBar(items=[
    {'label': 'View', 'items': [
        {'label': 'Show Toolbar', 'checkbox': True},
        {'label': 'Show Sidebar', 'checkbox': True},
        {'label': 'Show Status Bar', 'checkbox': False},
        None,
        {'label': 'Full Screen', 'icon': 'fullscreen', 'hint': 'F11'},
    ]},
], margin=(0, 0, 200, 0))

view_menu
```

After toggling checkboxes, the updated state is reflected on `items`:


```python
view_menu.items[0]['items'][:3]
```

## Radio Items

Items with a `radio` key render as mutually exclusive radio options. All radio items at the same nesting level form a group. Set `_radio_selected: True` on the initially selected item:


```python
pmui.MenuBar(items=[
    {'label': 'Theme', 'items': [
        {'label': 'Light', 'radio': 'light', '_radio_selected': True},
        {'label': 'Dark', 'radio': 'dark'},
        {'label': 'System', 'radio': 'system'},
    ]},
], margin=(0, 0, 200, 0))
```

## Groups

Items with `group: True` render their sub-items as a labeled section (with a subheader), rather than as a nested submenu. This is useful for organizing related options visually:


```python
pmui.MenuBar(items=[
    {'label': 'Format', 'items': [
        {'label': 'Text', 'group': True, 'icon': 'text_fields', 'items': [
            {'label': 'Bold', 'icon': 'format_bold', 'hint': 'Ctrl+B'},
            {'label': 'Italic', 'icon': 'format_italic', 'hint': 'Ctrl+I'},
            {'label': 'Underline', 'icon': 'format_underlined', 'hint': 'Ctrl+U'},
        ]},
        {'label': 'Paragraph', 'group': True, 'icon': 'format_align_left', 'items': [
            {'label': 'Align Left', 'icon': 'format_align_left'},
            {'label': 'Align Center', 'icon': 'format_align_center'},
            {'label': 'Align Right', 'icon': 'format_align_right'},
        ]},
    ]},
], margin=(0, 0, 200, 0))
```

## Callbacks

Use `on_click` to register a callback that fires whenever a menu item is clicked:


```python
callback_bar = pmui.MenuBar(items=[
    {'label': 'Actions', 'items': [
        {'label': 'Run', 'icon': 'play_arrow', 'hint': 'F5'},
        {'label': 'Debug', 'icon': 'bug_report', 'hint': 'F9'},
        {'label': 'Stop', 'icon': 'stop', 'hint': 'Shift+F5'},
    ]},
], margin=(0, 0, 200, 0))

log = pn.Column()

callback_bar.on_click(lambda item: log.append(f"Clicked: {item['label']}"))

pmui.Row(callback_bar, log)
```

## Icons on Top-Level Menus

Top-level menu triggers can also display icons:


```python
pmui.MenuBar(items=[
    {'label': 'File', 'icon': 'description', 'items': [
        {'label': 'New', 'icon': 'note_add'},
        {'label': 'Open', 'icon': 'folder_open'},
    ]},
    {'label': 'Edit', 'icon': 'edit', 'items': [
        {'label': 'Undo', 'icon': 'undo'},
        {'label': 'Redo', 'icon': 'redo'},
    ]},
    {'label': 'View', 'icon': 'visibility', 'items': [
        {'label': 'Zoom In', 'icon': 'zoom_in'},
        {'label': 'Zoom Out', 'icon': 'zoom_out'},
    ]},
], margin=(0, 0, 200, 0))
```

## Disabled Menus

Individual top-level menus or specific items can be disabled:


```python
pmui.MenuBar(items=[
    {'label': 'File', 'items': [
        {'label': 'New', 'icon': 'note_add'},
        {'label': 'Save', 'icon': 'save', 'disabled': True},
    ]},
    {'label': 'Edit', 'disabled': True, 'items': [
        {'label': 'Undo'},
    ]},
    {'label': 'Help', 'items': [
        {'label': 'About', 'icon': 'info'},
    ]},
], margin=(0, 0, 200, 0))
```

## Color and Size

The `color` parameter controls the button color, and `size` adjusts the button size:


```python
sample_items = [
    {'label': 'File', 'items': [{'label': 'New'}, {'label': 'Open'}]},
    {'label': 'Edit', 'items': [{'label': 'Undo'}, {'label': 'Redo'}]},
]

pmui.Row(
    pmui.MenuBar(items=sample_items, color='primary'),
    pmui.MenuBar(items=sample_items, color='secondary'),
    pmui.MenuBar(items=sample_items, color='success'),
    margin=(0, 0, 200, 0)
)
```

## Variant

The `variant` parameter controls the container style, either `'elevation'` (with a shadow) or `'outlined'` (with a border):


```python
pn.Row(
    pmui.MenuBar(items=sample_items, variant='elevation'),
    pmui.MenuBar(items=sample_items, variant='outlined'),
)
```

## Complete Example

A comprehensive menu bar combining multiple features:


```python
pmui.MenuBar(items=[
    {'label': 'File', 'items': [
        {'label': 'New', 'icon': 'note_add', 'hint': 'Ctrl+N'},
        {'label': 'Open', 'icon': 'folder_open', 'hint': 'Ctrl+O'},
        {'label': 'Open Recent', 'icon': 'history', 'items': [
            {'label': 'project.py'},
            {'label': 'analysis.ipynb'},
            {'label': 'dashboard.py'},
        ]},
        None,
        {'label': 'Save', 'icon': 'save', 'hint': 'Ctrl+S'},
        {'label': 'Save As...', 'icon': 'save_as'},
        None,
        {'label': 'Exit', 'icon': 'close'},
    ]},
    {'label': 'Edit', 'items': [
        {'label': 'Undo', 'icon': 'undo', 'hint': 'Ctrl+Z'},
        {'label': 'Redo', 'icon': 'redo', 'hint': 'Ctrl+Y'},
        None,
        {'label': 'Cut', 'icon': 'content_cut', 'hint': 'Ctrl+X'},
        {'label': 'Copy', 'icon': 'content_copy', 'hint': 'Ctrl+C'},
        {'label': 'Paste', 'icon': 'content_paste', 'hint': 'Ctrl+V'},
        None,
        {'label': 'Find', 'icon': 'search', 'hint': 'Ctrl+F'},
        {'label': 'Replace', 'icon': 'find_replace', 'hint': 'Ctrl+H'},
    ]},
    {'label': 'View', 'items': [
        {'label': 'Show Toolbar', 'checkbox': True},
        {'label': 'Show Sidebar', 'checkbox': True},
        {'label': 'Show Minimap', 'checkbox': False},
        None,
        {'label': 'Theme', 'group': True, 'icon': 'palette', 'items': [
            {'label': 'Light', 'radio': 'light', '_radio_selected': True},
            {'label': 'Dark', 'radio': 'dark'},
            {'label': 'System', 'radio': 'system'},
        ]},
        {'label': 'Zoom In', 'icon': 'zoom_in', 'hint': 'Ctrl++'},
        {'label': 'Zoom Out', 'icon': 'zoom_out', 'hint': 'Ctrl+-'},
    ]},
    {'label': 'Help', 'items': [
        {'label': 'Documentation', 'icon': 'menu_book'},
        {'label': 'Release Notes', 'icon': 'new_releases'},
        None,
        {'label': 'Report Issue', 'icon': 'bug_report'},
        None,
        {'label': 'About', 'icon': 'info'},
    ]},
], margin=(0, 0, 300, 0))
```

### API Reference

#### Parameters

The `MenuBar` exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.MenuBar(items=[
    {'label': 'File', 'items': [
        {'label': 'New', 'icon': 'note_add'},
        {'label': 'Open', 'icon': 'folder_open'},
        {'label': 'Save', 'icon': 'save'},
    ]},
    {'label': 'Edit', 'items': [
        {'label': 'Undo', 'icon': 'undo'},
        {'label': 'Redo', 'icon': 'redo'},
    ]},
]).api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI:**

- [Material UI MenuBar](https://mui.com/material-ui/react-menubar/) - Complete documentation for the underlying Material UI component
- [Material UI Menu](https://mui.com/material-ui/react-menu/) - Menu component reference
- [Material UI Menu API](https://mui.com/material-ui/api/menu/) - Detailed API reference
