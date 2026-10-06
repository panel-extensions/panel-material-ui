```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Tree` component belongs to `Menu` family of components in `panel-material-ui`. Like `MenuList` it allows renders hierarchical data, but unlike `MenuList` allows selecting more than one node. It is implemented using the MUI `RichTreeView`, optionally showing checkboxes, supporting multi-selection, buttons, actions and dropdown menus.

Each tree entry is a dictionary with a number of supported keys. Unless you explicitly supply an `id`, one is generated automatically from the node's position, meaning simple `{"label": "Node"}` entries are perfectly valid.

## Item Structure

Supported keys on each item:

- **`label`** (`str`, required): Display text for the node.
- **`items`** (`list[dict]`, optional): Nested child items.
- **`icon`** (`str`, optional): Material icon name.
- **`file_type`** (`str`, optional): Convenience helper (`"image"`, `"pdf"`, `"doc"`, `"video"`, `"folder"`, `"pinned"`, `"trash"`).
- **`secondary`** (`str`, optional): Supporting caption.
- **`color`** (`str`, optional): Palette key used when the node is selected.
- **`actions`** (`list`, optional): Inline or menu actions (same schema as `MenuList`).
- **`buttons`** (`list`, optional): Call-to-action buttons rendered next to the node label.
- **`selectable`** (`bool`, optional): Disable selection for a node when `False` (still expandable).
- **`disabled`** (`bool`, optional): Fully disables and greys out this item if `True`
- **`tooltip`** (`str`, optional): Tooltip text shown when hovering over the tree item.
 
Extra keys are preserved in Python so you can look up arbitrary metadata when handling callbacks.

## Parameters:

### Core

- **`items`** (`list[dict]`): Tree data.
- **`selected`** (`list[tuple]`): List of tuple paths of the active nodes (e.g. `(0, 1)` for the second child of the first root).
- **`expanded`** (`list[tuple]`): Paths of expanded nodes.
- **`multi_select`** (`bool`): Allow selecting multiple nodes via clicks.
- **`checkboxes`** (`bool`): Show per-node checkboxes; implies multi-select semantics.
- **`propagate_to_child` / `propagate_to_parent`** (`bool`): Mirror checkbox state downwards/upwards.

##### Display

* **`color`** (`str`): The color variant indicating the selected list item, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`item_children_indentation`** (`int`): Pixels to indent each level.
* **`level_indent`** (`int`): Number of pixels each nested level is indented by.
* **`show_children`** (`boolean`): Whether to render child items nested under `'items'`.

##### Styling

- **`sx`** (`dict`): Component level styling API.
- **`theme_config`** (`dict`): Theming API.

---


Like all `Menu`-like components `Tree` accepts a list of `items`, which each support sub-`items`:


```python
basic_tree = pmui.Tree(
    items=[
        {
            "label": "Content",
            "file_type": "folder",
            "items": [
                {"label": "Blog", "file_type": "doc"},
                {"label": "Media", "file_type": "image"},
            ],
        },
        {
            "label": "Archive",
            "file_type": "folder",
            "items": [
                {"label": "2023", "file_type": "pdf"},
                {"label": "2022", "file_type": "pdf"},
            ],
        },
    ],
    expanded=[(0,)],
)

basic_tree
```

Selecting a node updates both the `active` and `value` parameters on the Python side. `active` stores a list of the tuple indexes, while `value` returns a list of the original item dictionary:


```python
pn.Row(
    pn.Column(
        pn.pane.Markdown("**Selection path:**"),
        pn.pane.JSON(basic_tree.param.active, depth=2),
    ),
    pn.Column(
        pn.pane.Markdown("**Selected item:**"),
        pn.pane.JSON(basic_tree.param.value, depth=2)
    )
)
```

## Checkboxes & Multi-selection

Set `checkboxes=True` to render checkboxes and capture multiple selections as a list of tuple paths. You can optionally enable propagation so parent/child nodes stay in sync.


```python
checkbox_tree = pmui.Tree(
    items=[
        {
            "label": "Projects",
            "items": [
                {
                    "label": "Alpha",
                    "items": [
                        {"label": "Docs"},
                        {"label": "Reports"},
                    ],
                },
                {
                    "label": "Beta",
                    "items": [
                        {"label": "Analytics"},
                        {"label": "Dashboards"},
                    ],
                },
            ],
        }
    ],
    checkboxes=True,
    propagate_to_child=True,
    propagate_to_parent=True,
    active=[(0, 1, 1)],
    expanded=[(0,), (0, 1)],
    
)

pn.Row(
    checkbox_tree,
    pn.Column(
        "**Checked paths**",
        pn.pane.JSON(checkbox_tree.param.active)
    )
)
```

When `checkboxes=False` to select multiple independent items, press `Ctrl/⌘ + click`  and to select a range press `Shift + click`.

## Actions & Buttons

Tree nodes support the same action schema as `MenuList`, plus a `buttons` list for inline call-to-action buttons. Inline actions can toggle state, while menu actions appear inside a kebab menu.




```python
actions = [
    {"label": "Favorite", "icon": "star", "inline": True, "toggle": True, "value": False},
    {"label": "Delete", "icon": "delete"},
]

actions_log = pn.Column()

actions_tree = pmui.Tree(
    items=[
        {
            "label": "Notebooks",
            "items": [
                {
                    "label": "Explorations",
                    "secondary": "Last updated today",
                    "actions": actions,
                    "buttons": [
                        {"label": "Open", "icon": "open_in_new", "color": "primary"},
                    ],
                },
                {
                    "label": "Reports",
                    "secondary": "Last updated yesterday",
                    "actions": actions,
                    "buttons": [
                        {"label": "Share", "icon": "share", "variant": "outlined"},
                    ],
                },
            ],
        }
    ],
    active=[(0, 0)],
    expanded=[(0,)]
)

actions_tree.on_action("Favorite", lambda item: actions_log.append(f"Favorite toggled: {item['label']}, value={item['actions'][0]['value']}"))
actions_tree.on_action("Delete", lambda item: actions_log.append(f"Delete clicked: {item['label']}"))

pn.Row(actions_tree, actions_log)
```

### Item Options

Additional options can be used to `disable` specific items or toggle whether they are `selectable`. Instead of passing the `expanded` indexes it is also possible to set an item to `open` (note that these values are only used for initialization and `open` will not be updated) as items are expanded or collapsed.


```python
pmui.Tree(
    items=[
        {"label": "Project", "open": True, "items": [
            {"label": "Overview"},
            {"label": "Roadmap", "selectable": False},
            {"label": "Specs", "disabled": True, "items": [
                {"label": "Draft"},
                {"label": "Final"},
            ]}
        ]},
        {"label": "Team", "open": True, "items": [
            {"label": "Members"},
            {"label": "Archived", "disabled": True}
        ]},
    ],
    multi_select=False,   # single-select for clarity
    checkboxes=False,     # optional
)
```

### Display Options

#### `color`


```python
pn.GridBox(*(
    basic_tree.clone(color=color, label=color, active=[(0,), (0, 1)], margin=10)
    for color in pmui.MenuList.param.color.objects
), ncols=5)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
items = [
    {
        "label": ":material/zoom_out_map: Projects",
        "items": [
            {"label": ":material/zoom_out_map: Alpha"},
            {"label": ":material/zoom_out_map: Beta"},
        ],
    },
]

pmui.Tree(label=":material/zoom_out_map: Explorer", items=items, expanded=[(0,)])
```

### API Reference

Experiment with the available parameters directly in the browser:




```python
pmui.Tree(
    items=[
        {"label": "Documents", "items": [
            {"label": "Invoices"},
            {"label": "Contracts"},
        ]},
        {"label": "Media", "items": [
            {"label": "Images"},
            {"label": "Video"},
        ]},
    ],
    expanded=[(0,)],
).api(jslink=True)
```

### References

- [Panel Interactivity Guides](https://panel.holoviz.org/how_to/interactivity/) – Wiring up callbacks, linking parameters, and reacting to state changes.
- [Material UI Tree View](https://mui.com/x/react-tree-view/rich-tree-view/) – Underlying component API and styling guidance.
- [Panel Material UI Documentation](https://panel-material-ui.holoviz.org/reference/menus/Tree.html) – Latest reference entry for this widget.


