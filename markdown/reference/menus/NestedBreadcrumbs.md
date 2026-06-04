```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `NestedBreadcrumbs` component is part of the `Menu` family. `Menu` components provide a structured way for users to navigate or choose between a defined set of items. Unlike `Breadcrumbs`, `NestedBreadcrumbs` represents a **tree**: for each level, a small chevron opens a menu to switch between **siblings at that depth**. Clicking a segment navigates to that depth.

Each item in the `NestedBreadcrumbs` list is defined by a dictionary with several supported keys:

## Item Structure

Each item can include the following keys:

* **`label`** (`str`, required): The text displayed for the segment.
* **`href`** (`str`, optional): URL to link to (used on non-terminal segments).
* **`target`** (`str`, optional): Link target (e.g. `"_blank"`).
* **`icon`** (`str`, optional): Material icon name to render next to the label.
* **`avatar`** (`str`, optional): A short avatar/text badge to show beside the label.
* **`items`** (`list[dict]`, optional): Nested children for the next depth.
* **`selectable`** (`bool`, optional): Whether this item can be selected in the sibling menu (defaults to `True`).
* **`tooltip`** (`str`, optional): Tooltip text shown when hovering over the menu item.

Items are passed via the `items` parameter as a list containing a single **root** item. When a depth is selected, the explicit selection path is stored in `active` (see below).

## Parameters

### Core

* **`active`** (`tuple[int, ...]`): The explicit selection path from the root (e.g. `(0, 2, 1)`).
  The UI may **auto-descend** for rendering (first-child tails), but only the explicit part is stored here.
* **`auto_descend`** (`bool`, default `True`): Controls whether the UI auto-descends via first children when rendering.
  * `True`: The UI appends a first-child tail to `active` to compute `path` (for display).
  * `False`: No auto-descent; if the last explicit node has children, the last breadcrumb renders as an unselected **“Select…”** segment with a chevron menu.
* **`disabled`** (`bool`): Whether the breadcrumb control is disabled.
* **`items`** (`list[dict]`): A list with **one** root item; children live in each item’s `items`.
* **`path`** (`tuple[int, ...]`): The currently visible path.
  The UI may **auto-descend** for rendering (first-child tails), but only the explicit part is stored here.

### Display

* **`color`** (`str`): Color variant for the **active** segment; one of your theme’s supported colors (e.g. `'primary'`, `'success'`, …).
* **`separator`** (`str`, optional): Custom separator between segments. Defaults to the MUI NavigateNext icon.
* **`max_items`** (`int`, optional): Maximum number of segments to display (older segments are collapsed per MUI behavior).

### Styling

* **`sx`** (`dict`): Component-level styling API.
* **`theme_config`** (`dict`): Theming API.

---

### Basic Usage

`NestedBreadcrumbs` like all menu components allows selecting between a number of `items` defined as dictionaries in a list. The 


```python
breadcrumb_items = [
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
        'items': [
            {'label': 'Charts', 'icon': 'stacked_line_chart'},
            {'label': 'Maps', 'icon': 'map', 'items': [
                {'label': 'World', 'icon': 'public'},    
            ]},
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
        'selectable': False,
        'items': [
            {'label': 'Team', 'icon': 'groups'},
            {'label': 'Contact', 'icon': 'mail'}
        ]
    },
]

breadcrumb_menu = pmui.NestedBreadcrumbs(
    items=breadcrumb_items
)

pmui.Column(breadcrumb_menu, height=120)
```

The `active` and `path` parameters represent the paths to the selected and rendered items expressed as tuples of indexes:


```python
pmui.NestedBreadcrumbs(
    items=breadcrumb_items, active=(1, 1), path=(1, 1, 0)
)
```

By default, the component will automatically descend the tree (`auto_descend=True`), extending the visible breadcrumb path by following the first child at each level below the current selection.

This behavior ensures that users always see a fully expanded path to a leaf item, even when only a higher-level node is explicitly selected. When `auto_descend=False`, the component instead stops at the last explicitly selected item and renders a “Select…” placeholder segment with a chevron menu, prompting the user to choose the next level manually.


```python
descend_menu = pmui.NestedBreadcrumbs(
    items=breadcrumb_items, auto_descend=False, active=(1, 1)
)

pmui.Column(descend_menu, height=120)
```

### Display Options

#### `color`


```python
pn.GridBox(*(
    breadcrumb_menu.clone(color=color, label=color, active=0)
    for color in pmui.NestedBreadcrumbs.param.color.objects
), ncols=2)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
items = [
    {"label": ":material/zoom_out_map: Home"},
    {"label": ":material/zoom_out_map: Reports"},
]

pmui.NestedBreadcrumbs(
    label=":material/zoom_out_map: Navigation",
    items=items,
    active=(0,),
)
```

### API Reference

#### Parameters

The `NestedBreadcrumbs` exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.NestedBreadcrumbs(items=breadcrumb_items).api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Breadcrumbs:**

- [Material UI Breadcrumbs Reference](https://mui.com/material-ui/react-breadcrumbs) - Complete documentation for the underlying Material UI component
- [Material UI Breadcrumbs API](https://mui.com/material-ui/api/breadcrumbs/) - Detailed API reference and configuration options
