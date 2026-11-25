```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `AppBar` component renders a Material UI App Bar (top navigation bar). It supports a title, icon, color theming, and can contain arbitrary child components (buttons, menus, search fields, etc.) via the `objects` parameter.

The AppBar is commonly used as a top-level navigation header, either standalone or inside a `Page` component's `header` slot.

## Parameters

### Core

- **`objects`** (`list`): Components rendered inside the app bar toolbar (buttons, menus, etc.).
- **`title`** (`str`): Title text displayed in the app bar.
- **`icon`** (`str`): Icon displayed at the start of the app bar (e.g. a menu or brand icon).

### Display

- **`color`** (`str`): The color theme. One of `'default'`, `'inherit'`, `'primary'`, `'secondary'`, `'transparent'`.
- **`enable_color_on_dark`** (`bool`): If True, the `color` prop applies in dark mode too.
- **`position`** (`str`): CSS position. One of `'fixed'`, `'absolute'`, `'sticky'`, `'static'`, `'relative'`.
- **`variant`** (`str`): Toolbar density. `'dense'` for compact, `'regular'` for standard height.

### Styling

- **`sx`** (`dict`): Component-level styling API.
- **`theme_config`** (`dict`): Theming API.

---

## Basic Usage

A simple app bar with a title and icon:


```python
pmui.AppBar(title='My Application', icon='menu')
```

## With Buttons

Add action buttons to the app bar by passing them as positional arguments or via `objects`:


```python
pmui.AppBar(
    pmui.Button(label='Login', variant='outlined', color='default'),
    title='Dashboard',
    icon='dashboard',
)
```

## With MenuBar

The `AppBar` pairs naturally with `MenuBar` to create a desktop-style application header:


```python
menu = pmui.MenuBar(
    items=[
        {'label': 'File', 'items': [
            {'label': 'New', 'icon': 'note_add', 'hint': 'Ctrl+N'},
            {'label': 'Open', 'icon': 'folder_open', 'hint': 'Ctrl+O'},
            None,
            {'label': 'Save', 'icon': 'save', 'hint': 'Ctrl+S'},
            {'label': 'Exit', 'icon': 'close'},
        ]},
        {'label': 'Edit', 'items': [
            {'label': 'Undo', 'icon': 'undo', 'hint': 'Ctrl+Z'},
            {'label': 'Redo', 'icon': 'redo', 'hint': 'Ctrl+Y'},
            None,
            {'label': 'Cut', 'icon': 'content_cut'},
            {'label': 'Copy', 'icon': 'content_copy'},
            {'label': 'Paste', 'icon': 'content_paste'},
        ]},
        {'label': 'Help', 'items': [
            {'label': 'Documentation', 'icon': 'menu_book'},
            {'label': 'About', 'icon': 'info'},
        ]},
    ],
    variant='outlined',
    sx={'border': 'none', 'boxShadow': 'none', 'background': 'transparent'},
)

pmui.AppBar(menu, title='Code Editor', icon='code')
```

## Color Variants

The `color` parameter controls the app bar's background color:


```python
pn.Column(
    pmui.AppBar(title='Primary', color='primary'),
    pmui.AppBar(title='Secondary', color='secondary'),
    pmui.AppBar(title='Default', color='default'),
    pmui.AppBar(title='Transparent', color='transparent'),
)
```

## Dense vs Regular

The `variant` parameter controls the toolbar height:


```python
pn.Column(
    pmui.AppBar(title='Dense (compact)', variant='dense', icon='menu'),
    pmui.AppBar(title='Regular', variant='regular', icon='menu'),
)
```

## Multiple Components

You can place multiple components in the app bar. They are laid out horizontally with flex:


```python
pmui.AppBar(
    pmui.MenuBar(
        items=[
            {'label': 'File', 'items': [{'label': 'New'}, {'label': 'Open'}]},
            {'label': 'Edit', 'items': [{'label': 'Undo'}, {'label': 'Redo'}]},
        ],
        sx={'border': 'none', 'boxShadow': 'none', 'background': 'transparent'},
    ),
    pmui.Button(label='Sign In', variant='outlined', color='default'),
    title='My App',
    icon='apps',
)
```

## Custom Styling

Use the `sx` parameter for custom styling, or `theme_config` for full theming:


```python
pmui.AppBar(
    title='Custom Styled',
    icon='rocket',
    color='transparent',
    sx={
        'background': 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
        'color': 'white',
    },
)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Templates](https://panel.holoviz.org/how_to/templates/index.html) - Build full application layouts

**Material UI:**

- [Material UI App Bar](https://mui.com/material-ui/react-app-bar/) - Complete documentation for the underlying Material UI component
- [Material UI AppBar API](https://mui.com/material-ui/api/app-bar/) - Detailed API reference
