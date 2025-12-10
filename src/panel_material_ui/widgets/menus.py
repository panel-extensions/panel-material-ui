from __future__ import annotations

from collections import defaultdict
from functools import partial
from typing import Callable

import param
from panel._param import Margin
from panel.io.state import state
from panel.layout import Column
from panel.layout.base import ListLike
from panel.models.reactive_html import DOMEvent
from param.parameterized import _syncing

from ..base import COLORS, ThemedTransform
from .base import MaterialWidget, TooltipTransform
from .button import _ButtonBase


class MenuBase(MaterialWidget):

    active = param.Integer(default=None, doc="""
        The index of the currently selected menu item.""")

    items = param.ClassSelector(default=[], class_=list, doc="""
        List of items to display. Each item may be a string, a tuple mapping from a label to a value,
        or an object with a few common properties and a few widget specific properties.""")

    margin = Margin(default=0)

    value = param.ClassSelector(default=None, class_=(dict, str), doc="""
        Last clicked menu item.""")

    width = param.Integer(default=None, doc="""
        The width of the menu.""")

    _item_keys = ['label', 'items']
    _descend_children = True
    _rename = {'value': None}
    _source_transforms = {"value": None, "items": None, "attached": None}

    __abstract = True

    def __init__(self, **params):
        click_handler = params.pop('on_click', None)
        super().__init__(**params)
        if self.value is None and self.active is not None:
            self._sync_active()
        elif self.value is not None and self.active is None:
            self._sync_value()
        self._on_action_callbacks = defaultdict(list)
        self._on_click_callbacks = []
        if click_handler:
            self.on_click(click_handler)

    def _process_param_change(self, params):
        params = super()._process_param_change(params)
        if 'items' in params:
            if isinstance(params['items'], list) and any(isinstance(item, tuple) for item in params['items']):
                # Legacy format from Panel
                items = []
                for item in params['items']:
                    if isinstance(item, tuple):
                        items.append({"label": item[0], "value": item[1]})
                    else:
                        items.append(item)
            else:
                items = params['items']
            params['items'] = [self._filter_item(item, self._item_keys) for item in items]
        return params

    def _process_property_change(self, props):
        props = super()._process_property_change(props)
        if 'active' in props and isinstance(props['active'], list):
            props['active'] = tuple(props['active'])
        elif 'active' in props and isinstance(props['active'], bool):
            props['active'] = 0
        return props

    @param.depends('items', watch=True)
    def _sync_items(self):
        self.param.active.bounds = (0, len(self.items)-1)

    @param.depends('active', watch=True)
    def _sync_active(self):
        with _syncing(self, ['value']):
            self.value = self._lookup_item(self.active)

    @param.depends('value', watch=True)
    def _sync_value(self):
        index = self._lookup_path(self.value)
        with _syncing(self, ['active']):
            if index is None:
                self.active = None
            else:
                self.active = index if 'items' in self._item_keys else index[0]

    def _filter_item(self, item, keys: list[str], depth: int = 0, children: bool = True):
        if isinstance(item, dict):
            item = {k: v for k, v in item.items() if k in keys and (children or k != "items")}
            if 'items' in item:
                item['items'] = [
                    self._filter_item(child, keys, depth=depth+1)
                    for child in item['items']
                ]
        return item

    def _items_equal(self, item1, item2):
        if item1 is item2:
            return True
        elif not (isinstance(item1, dict) and isinstance(item2, dict)):
            return False
        id1 = item1.get("id")
        id2 = item2.get("id")
        if id1 is not None and item2 is not None:
            return id1 == id2
        filtered1 = self._filter_item(item1, self._item_keys, children=False)
        filtered2 = self._filter_item(item2, self._item_keys, children=False)
        return filtered1 == filtered2

    def _lookup_path(self, item, items=None):
        items = self.items if items is None else items
        if not items:
            return None
        queue = [([], 0, items)]
        while queue:
            path, depth, items = queue.pop(0)
            for i, current in enumerate(items):
                current_path = path + [i]
                if self._items_equal(current, item):
                    return tuple(current_path)
                if isinstance(current, dict) and 'items' in current and self._descend_children:
                    queue.append((current_path, depth + 1, current['items']))
        return None

    def _lookup_item(self, index, items=None):
        if index is None:
            return
        indexes = index if isinstance(index, tuple) else [index]
        value = self.items if items is None else items
        for i, idx in enumerate(indexes):
            if idx >= len(value):
                return None
            value = value[idx]
            if isinstance(value, dict) and (i != len(indexes)-1) and self._descend_children:
                value = value['items']

        if isinstance(value, tuple):
            value = {'label': value[0], 'value': value[1]}
        return value

    def _process_click(self, msg, index, value):
        if not isinstance(value, dict) or value.get('selectable', True):
            with _syncing(self, ['active', 'value']):
                self.param.update(active=index, value=value)
        for fn in self._on_click_callbacks:
            try:
                state.execute(partial(fn, value))
            except Exception as e:
                print(f'List on_click handler errored: {e}')  # noqa

    def _process_action(self, msg, index, value):
        name = msg['action']
        if 'value' in msg:
            value['actions'] = [
                dict(action, value=msg['value']) if action.get('action', action.get('label')) == name else action
                for action in value['actions']
            ]
        for fn in self._on_action_callbacks.get(name, []):
            try:
                state.execute(partial(fn, value))
            except Exception as e:
                print(f'List on_action handler errored: {e}')  # noqa

    def _handle_msg(self, msg):
        index = msg.get('item')
        if isinstance(index, list):
            index = tuple(index)
        value = None if index is None else self._lookup_item(index)
        if msg['type'] == 'click':
            self._process_click(msg, index, value)
        elif msg['type'] == 'action':
            self._process_action(msg, index, value)

    def update_item(self, item, **updates):
        """
        Update an item in the menu.

        Parameters
        ----------
        item: (dict)
            The item to update.
        updates: (dict)
            The updates to apply to the item.
        """
        path= self._lookup_path(item)
        new_item = dict(item, **updates)
        *path, index = path
        root_items = items = list(self.items)
        for p in path:
            subitem = dict(items[p])
            items[p] = subitem
            subitem["items"] = items = list(subitem["items"])
        items[index] = new_item
        self.items = root_items

    def on_click(self, callback: Callable[[DOMEvent], None]):
        """
        Register a callback to be executed when a list item
        is clicked.

        Parameters
        ----------
        callback: (callable)
            The callback to run on click events.
        """
        self._on_click_callbacks.append(callback)

    def remove_on_click(self, callback: Callable[[DOMEvent], None]):
        """
        Remove a previously added click handler.

        Parameters
        ----------
        callback: (callable)
            The callback to run on edit events.
        """
        self._on_click_callbacks.remove(callback)


class BreadcrumbsBase(MenuBase):

    color = param.Selector(objects=COLORS, default="primary", doc="The color of the breadcrumbs.")

    max_items = param.Integer(default=None, bounds=(1, None), doc="""
        The maximum number of breadcrumb items to display.""")

    separator = param.String(default=None, doc="""
        The separator displayed between breadcrumb items.""")

    __abstract = True


class Breadcrumbs(BreadcrumbsBase):
    """
    The `Breadcrumbs` component is used to show the navigation path of a user within an application.
    It improves usability by allowing users to track their location and navigate back easily.

    Breadcrumb items can be strings or objects with properties:

    - `label`: The label of the breadcrumb item (required)
    - `icon`: The icon of the breadcrumb item (optional)
    - `avatar`: The avatar of the breadcrumb item (optional)
    - `href`: Link to navigate to when clicking the breadcrumb item (optional)

    :References:

    - https://panel-material-ui.holoviz.org/reference/menus/Breadcrumbs.html
    - https://mui.com/material-ui/react-breadcrumbs/

    :Example:

    >>> pmui.Breadcrumbs(items=[
    ...     {'label': 'Documentation', 'icon': 'article'},
    ...     {'label': 'Reference Gallery', 'icon': 'category'},
    ...     {'label': 'Menus', 'icon': 'menu'},
    ...     {'label': 'Breadcrumbs', 'icon': 'grain'},
    ... ], active=3)
    """

    _esm_base = "Breadcrumbs.jsx"
    _item_keys = ['label', 'icon', 'avatar', 'href', 'target']


class TabMenu(MenuBase):
    """
    The `TabMenu` component is used to display a group of tabs that allow users to switch
    between different views or sections of content. It provides a clean, organized way to
    navigate between related items.

    Tab items can be strings or objects with properties:

    - `label`: The label of the tab item (required)
    - `icon`: The icon of the tab item (optional)
    - `avatar`: The avatar of the tab item (optional)
    - `href`: Link to navigate to when clicking the tab item (optional)
    - `target`: Link target (e.g. `"_blank"`) (optional)

    :References:

    - https://panel-material-ui.holoviz.org/reference/menus/TabMenu.html
    - https://mui.com/material-ui/react-tabs/

    :Example:

    >>> pmui.TabMenu(items=[
    ...     {'label': 'Home', 'icon': 'home'},
    ...     {'label': 'Gallery', 'icon': 'image'},
    ...     {'label': 'Settings', 'icon': 'settings'},
    ... ], active=0)
    """

    centered = param.Boolean(default=False, doc="""
        Whether the tabs should be centered.""")

    color = param.Selector(objects=COLORS, default="primary", doc="The color of the tabs.")

    icon_position = param.Selector(objects=["start", "top", "end", "bottom"], doc="""
        The position of the icon relative to the tab label.""")

    scroll_buttons = param.Selector(default="auto", objects=["auto", "true", "false"], doc="""
        Determine behavior of scroll buttons when tabs are set to scroll.
        - "auto" will only present them when not all the items are visible.
        - "true" will always present them.
        - "false" will never present them.""")

    variant = param.Selector(default="standard", objects=["standard", "scrollable", "fullWidth"], doc="""
        The variant to use for the tabs.""")

    _esm_base = "TabMenu.jsx"
    _item_keys = ['label', 'icon', 'avatar', 'href', 'target']


class NestedMenuBase(MenuBase):

    active = param.ClassSelector(default=None, class_=(int, tuple), doc="""
        The index of the currently selected item. Can be a tuple of indices for nested items.""")

    __abstract = True

    @param.depends('items', watch=True, on_init=True)
    def _sync_items(self):
         pass

    def _process_property_change(self, props):
        props = super()._process_property_change(props)
        if 'active' in props and isinstance(props['active'], list):
            props['active'] = tuple(props['active'])
        return props


class NestedBreadcrumbs(NestedMenuBase, BreadcrumbsBase):
    """
    The `NestedBreadcrumbs` component provides breadcrumb-style navigation
    for hierarchical data. It extends standard breadcrumbs by allowing each
    non-root segment to open a sibling selector menu via a chevron, enabling
    users to navigate between branches at any level.

    Nested breadcrumbs help users visualize their position in a nested structure
    and move both upward (via breadcrumb clicks) and sideways (via sibling menus).

    Breadcrumb items are defined as objects with the following properties:

    - `label`: The label of the breadcrumb item (required)
    - `icon`: The icon of the breadcrumb item (optional)
    - `avatar`: The avatar of the breadcrumb item (optional)
    - `href`: Link to navigate to when clicking the breadcrumb item (optional)
    - `target`: Link target (e.g. `"_blank"`) (optional)
    - `items`: List of nested child items (optional)
    - `selectable`: Whether the item can be selected in sibling menus (optional, defaults to True)

    :References:

    - https://panel-material-ui.holoviz.org/reference/menus/NestedBreadcrumbs.html
    - https://mui.com/material-ui/react-breadcrumbs/

    :Example:

    >>> pmui.NestedBreadcrumbs(items=[
    ...     {
    ...         'label': 'Projects', 'icon': 'folder', 'items': [
    ...             {'label': 'A', 'icon': 'category', 'items': [
    ...                 {'label': 'A1', 'icon': 'grain'},
    ...                 {'label': 'A2', 'icon': 'grain'},
    ...             ]},
    ...             {'label': 'B', 'icon': 'category', 'items': [
    ...                 {'label': 'B1', 'icon': 'grain'},
    ...             ]},
    ...         ]
    ...     }
    ... ], active=(0,))
    """

    active = param.ClassSelector(default=None, class_=(int, tuple), doc="""
        The index of the currently selected item. Can be a tuple of indices for nested items.""")

    auto_descend = param.Boolean(default=True, doc="""
        Whether to automatically descend through the first child of each
        selected item when rendering the breadcrumb path.

        When ``True`` (default), the component will automatically extend the
        visible path by following first-child items below the current selection.

        When ``False``, the last breadcrumb segment will instead display a
        "Select…" placeholder with a chevron menu, allowing the user to pick
        a child manually.""")

    path = param.ClassSelector(default=None, class_=tuple, doc="""
        The tuple containing indices of the currently rendered path.""")

    _esm_base = "NestedBreadcrumbs.jsx"
    _item_keys = ['label', 'icon', 'avatar', 'href', 'target', 'items', 'selectable']

    def _handle_msg(self, msg):
        index = msg.get('item')
        if isinstance(index, list):
            index = tuple(index)
        path = msg.get('path')
        if isinstance(path, list):
            path = tuple(path)
        value = None if index is None else self._lookup_item(index)
        if value is not None:
            self._process_click(msg, index, value)
        if path is not None:
            with _syncing(self, ['path']):
                self.path = path

    @classmethod
    def _truncate_path(cls, path1, path2, extend=True):
        new_path = []
        for i, p in enumerate(path1 or ()):
            if i < len(path2) and path2[i] != p:
                if extend:
                    new_path.append(path2[i])
                break
            else:
                new_path.append(p)
        if extend:
            new_path.extend(path2[len(new_path):])
        return tuple(new_path)

    def _process_param_change(self, params):
        props = super()._process_param_change(params)
        if props.get("active") is not None and "path" not in props:
            active = props["active"]
            if isinstance(active, int):
                active = (active,)
            self.path = props["path"] = self._truncate_path(self.path, active)
        elif props.get("path") is not None and "active" not in props:
            self.active = props["active"] = self._truncate_path(self.active, props["path"], extend=False)
        return props

    def _process_property_change(self, props):
        props = super()._process_property_change(props)
        if 'path' in props and isinstance(props['path'], list):
            props['path'] = tuple(props['path'])
        return props


class TreeLikeBase(NestedMenuBase):
    """
    The `TreeLikeBase` component is a base class for components that are tree-like, such as `MenuList` and `Tree`.
    """

    expanded = param.List(default=[], doc="""
        List of tree paths (tuples of indices) that are currently expanded.""")

    level_indent = param.Integer(default=16, doc="""
        Indentation, in pixels, used for each nested level of the tree.""")

    show_children = param.Boolean(default=True, doc="Whether to render children.")

    __abstract = True

    def __init__(self, **params):
        super().__init__(**params)
        self.param.watch(self._update_expanded, "items")
        self.param.trigger("items")

    @property
    def _descend_children(self):
        return self.show_children

    def on_action(self, action: str, callback: Callable[[DOMEvent], None]):
        """
        Register a callback to be executed when an action is clicked.

        Parameters
        ----------
        action: (str)
            The action to register a callback for.
        callback: (callable)
            The callback to run on action events.
        """
        self._on_action_callbacks[action].append(callback)

    def toggle_action(self, item: dict, action: str, value: bool):
        """
        Toggle an action for an item.

        Parameters
        ----------
        item: (dict)
            The item to toggle the action on.
        action: (str)
            The label of the action to toggle.
        value: (bool)
            The value to set the action to.
        """
        index = self._lookup_path(item)
        if index is None:
            raise ValueError("Item {item} was not found.")
        self._send_msg({"type": "toggle_action", "index": index, "action": action, "value": value})

    def remove_on_action(self, action: str, callback: Callable[[DOMEvent], None]):
        """
        Remove a previously added action handler.

        Parameters
        ----------
        action: (str)
            The action to remove a callback for.
        callback: (callable)
            The callback to remove.
        """
        self._on_action_callbacks[action].remove(callback)

    def _update_expanded(self, event):
        """
        Remap self.expanded (paths into old items) to paths into new items
        based on stable item['id'] values.
        """
        old_items = event.old or []
        new_items = event.new or []

        expanded_items = []
        for path in self.expanded:
            item = self._lookup_item(path, old_items)
            if item is not None:
                expanded_items.append(item)

        def descend(items, path=()):
            for idx, item in enumerate(items):
                current_path = path + (idx,)
                if isinstance(item, dict):
                    if item.get("open", False):
                        expanded_items.append(item)
                    if "items" in item and self.show_children:
                        descend(item["items"], current_path)

        descend(new_items)

        expanded = []
        for item in expanded_items:
            path = self._lookup_path(item, new_items)
            if path is not None:
                expanded.append(path)
        self.expanded = expanded


class MenuList(TreeLikeBase):
    """
    The `MenuList` component is used to display a structured group of items, such as menus,
    navigation links, or settings.

    List items can be strings or objects with properties:
      - `label`: The label of the list item (required)
      - `secondary`: The secondary text of the list item (optional)
      - `icon`: The icon of the list item (optional)
      - `avatar`: The avatar of the list item (optional)
      - `color`: The color of the list item (optional)
      - `actions`: Actions to display on the list item (optional)
      - `items`: Nested items (optional)
      - `selectable`: Whether the list item is selectable (optional)
      - `href`: The URL to navigate to when the list item is clicked (optional)
      - `target`: The target to open the URL in (optional)

    :References:

    - https://panel-material-ui.holoviz.org/reference/menus/MenuList.html
    - https://mui.com/material-ui/react-list/

    :Example:

    >>> pmui.MenuList(items=[
    ...     {'label': 'Home', 'icon': 'home', 'secondary': 'Overview page'},
    ...     {'label': 'Gallery', 'icon': 'image', 'secondary': 'Visual overview'},
    ...     {'label': 'API', 'icon': 'code', 'secondary': 'API Reference'},
    ...     {'label': 'About', 'icon': 'info'},
    ... ], active=3)
    """

    color = param.Selector(default="primary", objects=COLORS, doc="The color of the selected list item.")

    collapsed = param.Boolean(default=False, doc="Whether to collapse the tree to show only the icons and no child items.")

    dense = param.Boolean(default=True, doc="Whether to show the list items in a dense format.")

    highlight = param.Boolean(default=True, doc="""
        Whether to highlight the currently selected menu item.""")

    removable = param.Boolean(default=False, doc="Whether to allow deleting items.")

    _esm_base = "List.jsx"

    _item_keys = [
        'label', 'items', 'icon', 'avatar', 'color', 'secondary', 'actions', 'selectable',
        'href', 'target', 'buttons'
    ]

List = MenuList


class Tree(TreeLikeBase):
    """
    The `Tree` component displays hierarchical data using a Material UI
    `RichTreeView`, with optional checkboxes and multi-selection.

    Items follow the same convention as `MenuList`:

    Each item is a dictionary with at least:

      - ``label`` (str): Display label of the node.

    The ``id`` field is optional. When omitted, a stable internal id is generated
    from the item's position, so the simplest ``{"label": "Node"}`` form works
    without any additional bookkeeping.

    Optional item fields:

      - ``items`` (list): Nested children, each with the same schema.
      - ``icon`` (str): MUI icon name (rendered via ``<Icon>``).
      - ``file_type`` (str): Helper for common icons, one of
        ``"image"``, ``"pdf"``, ``"doc"``, ``"video"``, ``"folder"``,
        ``"pinned"``, ``"trash"``.
      - ``disabled`` (bool): Whether the item is disabled.
      - ``selectable`` (bool): Whether the item is selectable.
      - ``secondary`` (str): The secondary text of the item.
      - ``actions`` (list): Actions to display on the item.
      - ``buttons`` (list): Buttons to display on the item.
      - ``color`` (str): The color of the item.

    :Example:

    >>> pmui.Tree(
    ...     items=[
    ...         {
    ...             "id": "documents",
    ...             "label": "Documents",
    ...             "file_type": "folder",
    ...             "items": [
    ...                 {
    ...                     "id": "invoice",
    ...                     "label": "Invoice Q1.pdf",
    ...                     "file_type": "pdf",
    ...                 },
    ...                 {
    ...                     "id": "notes",
    ...                     "label": "Meeting notes.docx",
    ...                     "file_type": "doc",
    ...                 },
    ...             ],
    ...         },
    ...         {
    ...             "id": "trash",
    ...             "label": "Trash",
    ...             "file_type": "trash",
    ...         },
    ...     ],
    ...     active=[(0,)],
    ... )
    """

    active = param.List(default=None, item_type=tuple, doc="""
        The index(es) of currently selected items. Provide a list of tuples of indices,
        e.g. ``[(0, 1)]`` to refer to the second child beneath the first root
        node.""")

    checkboxes = param.Boolean(default=False, doc="""
        Whether to show selection checkboxes next to each tree item.""")

    color = param.Selector(default="primary", objects=COLORS, doc="""
        Color palette key for the selected node styling.""")

    multi_select = param.Boolean(default=True, doc="""
        Whether multiple tree items can be selected at once.""")

    propagate_to_parent = param.Boolean(default=False, doc="""
        Whether checkbox selection propagates from child nodes to parent nodes.
        If True, selecting a child will also select its parent(s).""")

    propagate_to_child = param.Boolean(default=False, doc="""
        Whether checkbox selection propagates from parent nodes to child nodes.
        If True, selecting a parent node will automatically select all its child nodes.
        If False, selection is independent for each node.""")

    value = param.List(default=[], item_type=dict, doc="""
        The list of currently selected item dictionaries. This parameter is
        synchronized with the `active` parameter and reflects the items that
        are currently selected in the tree. Each item is represented as a
        dictionary containing its properties (e.g., 'id', 'label', etc.).
        """)

    _esm_base = "Tree.jsx"

    _item_keys = [
        "id",
        "label",
        "items",
        "icon",
        "file_type",
        "disabled",
        "selectable",
        "secondary",
        "actions",
        "buttons",
        "color"
    ]

    @param.depends('active', watch=True)
    def _sync_active(self):
        with _syncing(self, ['value']):
            self.value = [self._lookup_item(s) for s in self.active]

    @param.depends('value', watch=True)
    def _sync_value(self):
        index = [self._lookup_path(v) for v in self.value]
        with _syncing(self, ['active']):
            self.active = index

    def _process_property_change(self, props):
        props = super()._process_property_change(props)
        if 'active' in props:
            props['active'] = [tuple(sel) for sel in props['active']]
        if 'expanded' in props:
            props['expanded'] = [tuple(sel) for sel in props['expanded']]
        return props


class MenuButton(MenuBase, _ButtonBase):
    """
    The `MenuButton` component is a button component that allows selecting from a list of items.

    MenuButton items can be strings or objects with properties:
      - `label`: The label of the menu button item (required)
      - `icon`: The icon of the menu button item (optional)
      - `color`: The color of the menu button item (optional)
      - `href`: The URL to navigate to when the menu button item is clicked (optional)
      - `target`: The target to open the URL in (optional)

    :References:

    - https://panel-material-ui.holoviz.org/reference/menus/MenuButton.html
    - https://mui.com/material-ui/react-menu-button/

    :Example:

    >>> pmui.MenuButton(items=[
    ...     {'label': 'Open', 'icon': 'description'},
    ...     {'label': 'Save', 'icon': 'save'},
    ...     {'label': 'Exit', 'icon': 'close'},
    ... ], label='File', icon='storage')
    """

    margin = Margin(default=5)

    disable_elevation = param.Boolean(default=False, doc="Removes the menu's box-shadow for a flat appearance.")

    size = param.Selector(default="medium", objects=["small", "medium", "large"], doc="The size of the menu button.")

    _esm_base = "MenuButton.jsx"
    _esm_transforms = [TooltipTransform, ThemedTransform]
    _source_transforms = {
        "attached": None,
        "button_type": None,
        "button_style": None
    }
    _item_keys = ['label', 'icon', 'color', 'href', 'target', 'icon_size']


class SplitButton(MenuBase, _ButtonBase):
    """
    The `SplitButton` component combines a button with a dropdown menu, allowing users to quickly access a primary action and related alternatives.

    This component supports two modes:

    - **`split`**: The main button performs a default action, while the dropdown lets users trigger related but independent actions.
    - **`select`**: Users select an option from the dropdown, and the main button triggers the selected action when clicked.

    Each menu item can be a string or a dictionary with the following keys:
      - **`label`** (`str`, required): The text displayed for the menu item.
      - **`icon`** (`str`, optional): An icon to display next to the label.
      - **`href`** (`str`, optional): A URL to open when the menu item is clicked.
      - **`target`** (`str`, optional): Where to open the linked URL (e.g., `_blank`).

    The `SplitButton` is ideal for workflows where a primary action is most common, but users may occasionally need to choose an alternative.

    :References:

    - https://panel-material-ui.holoviz.org/reference/menus/SplitButton.html
    - https://mui.com/material-ui/react-button-group/#split-button

    :Example:

    >>> pmui.SplitButton(items=[
    ...     {'label': 'Open'},
    ...     {'label': 'Save'},
    ... ], label='Save')
    """

    mode = param.Selector(default='split', objects=['split', 'select'], doc="""
        Allows toggling button behavior between split mode (button click and menu click actions raise events) and
        select mode (only button click raise events).""")

    margin = Margin(default=5)

    _esm_base = "SplitButton.jsx"
    _esm_transforms = [TooltipTransform, ThemedTransform]
    _source_transforms = {
        "attached": None,
        "button_type": None,
        "button_style": None
    }
    _item_keys = ['label', 'icon', 'href', 'target', 'icon_size']

    @param.depends('mode', watch=True, on_init=True)
    def _switch_mode(self):
        if self.mode == 'select' and self.value is None:
            with _syncing(self, ['active', 'value']):
                self.param.update(active=0, value=self.items[0])

    def _process_click(self, msg, index, value):
        if self.mode == 'select' and 'item' in msg:
            with _syncing(self, ['active', 'value']):
                self.param.update(active=index, value=value)
            return
        updates = {'clicks': self.clicks+1}
        if value is None:
            value = self.value if self.mode == 'select' else self.label
        elif not isinstance(value, dict) or value.get('selectable', True):
            updates.update(active=index, value=value)
        with _syncing(self, list(updates)):
            self.param.update(updates)
        for fn in self._on_click_callbacks:
            try:
                state.execute(partial(fn, value))
            except Exception as e:
                print(f'List on_click handler errored: {e}')  # noqa


class MenuToggle(MenuBase, _ButtonBase):
    """
    The `MenuToggle` component is a menu button where individual items can be toggled on/off.

    Unlike MenuButton, MenuToggle allows each menu item to have a toggle state with
    different icons for active/inactive states (e.g., filled/unfilled heart for favorites).

    MenuToggle items can be strings or objects with properties:
      - `label`: The label of the menu toggle item (required)
      - `icon`: The icon when item is not toggled (optional)
      - `active_icon`: The icon when item is toggled (optional)
      - `toggled`: Whether the item is currently toggled (optional, default: false)
      - `color`: The color of the menu toggle item (optional)
      - `active_color`: The color when toggled (optional)

    :References:

    - https://panel-material-ui.holoviz.org/reference/menus/MenuToggle.html
    - https://mui.com/material-ui/react-toggle-button/

    :Example:

    >>> pmui.MenuToggle(items=[
    ...     {'label': 'Favorite', 'icon': 'favorite_border', 'active_icon': 'favorite', 'toggled': False},
    ...     {'label': 'Bookmark', 'icon': 'bookmark_border', 'active_icon': 'bookmark', 'toggled': True},
    ...     {'label': 'Star', 'icon': 'star_border', 'active_icon': 'star', 'toggled': False},
    ... ], label='Actions', icon='more_vert')
    """

    toggle_icon = param.String(default=None, doc="""
        Icon to display when menu is open (if different from base icon).""")

    toggled = param.List(default=[], doc="""
        List of indices of currently toggled items.""")

    margin = Margin(default=5)

    persistent = param.Boolean(default=True, doc="""
        Whether the menu stays open after toggling an item.""")

    size = param.Selector(default="medium", objects=["small", "medium", "large"], doc="The size of the menu toggle.")

    _esm_base = "MenuToggle.jsx"
    _esm_transforms = [TooltipTransform, ThemedTransform]
    _source_transforms = {
        "attached": None,
        "button_type": None,
        "button_style": None,
    }
    _item_keys = ['label', 'icon', 'active_icon', 'toggled', 'color', 'active_color', 'icon_size']
    _rename = {'value': None}

    @param.depends('items', watch=True, on_init=True)
    def _sync_toggled(self):
        if self.items:
            self.toggled = [
                i for i, item in enumerate(self.items)
                if isinstance(item, dict) and item.get('toggled', False)
            ]
        else:
            self.toggled = []

    def _handle_msg(self, msg):
        if msg['type'] != 'toggle_item':
            return
        index = msg['item']
        if index in self.toggled:
            self.toggled = [i for i in self.toggled if i != index]
        else:
            self.toggled = self.toggled + [index]
        # Update the item's toggled state
        if isinstance(self.items[index], dict):
            self.items[index]['toggled'] = index in self.toggled
        # Update value to the clicked item
        value = self._lookup_item(index)
        if value.get('selectable', True):
            self.value = value
        for fn in self._on_click_callbacks:
            state.execute(partial(fn, value))


class Pagination(MaterialWidget):
    """
    The `Pagination` component allows selecting from a list of pages.

    :References:

    - https://panel-material-ui.holoviz.org/reference/menus/Pagination.html
    - https://mui.com/material-ui/react-pagination/

    :Example:

    >>> pmui.Pagination(count=100)
    """

    boundary_count = param.Integer(default=1, bounds=(0, None), doc="The number of boundary pages to show.")

    color = param.Selector(default="primary", objects=COLORS, doc="The color of the pagination.")

    count = param.Integer(default=1, bounds=(0, None), doc="The total number of pages.")

    shape = param.Selector(default="circular", objects=["circular", "rounded"], doc="The shape of the pagination.")

    size = param.Selector(default="medium", objects=["small", "medium", "large"], doc="The size of the pagination.")

    sibling_count = param.Integer(default=1, bounds=(0, None), doc="The number of sibling pages to show.")

    show_first_button = param.Boolean(default=False, doc="Whether to show the first button.")

    show_last_button = param.Boolean(default=False, doc="Whether to show the last button.")

    value = param.Integer(default=None, doc="The current zero-indexed page number.")

    variant = param.Selector(default="text", objects=["outlined", "text"], doc="The variant of the pagination.")

    width = param.Integer(default=None, doc="The width of the pagination.")

    _esm_base = "Pagination.jsx"

    @param.depends('count', watch=True, on_init=True)
    def _update_count(self):
        self.param.value.bounds = (0, self.count - 1 if self.count else 0)
        if self.count != 0 and self.value is None:
            self.value = 0

    @classmethod
    def paginate(cls, objects: list, layout: type[ListLike] = Column, page_size: int = 10, **params):
        """
        Paginate the items based on the current page and page size.

        Parameters
        ----------
        objects: list
            The list of objects to paginate.
        layout: type[LayoutBase]
            The layout to use for the paginated items.
        page_size: int
            The number of items to display per page.
        params: dict
            Additional parameters to pass to the layout.

        Returns
        -------
        layout
            The layout with the paginated items.
        """
        pagination = Pagination(count=len(objects)//page_size)
        val_rx = pagination.rx()
        objects_rx = param.rx(objects)[val_rx * page_size:(val_rx + 1) * page_size]
        return Column(
            layout(objects=objects_rx, **params),
            pagination
        )


class SpeedDial(MenuBase):
    """
    The `SpeedDial` component is a menu component that allows selecting from a
    list of items.

    SpeedDial items can be strings or objects with properties:

    - `label`: The label of the speed dial item (required)
    - `icon`: The icon of the speed dial item (optional)
    - `avatar`: The avatar of the speed dial item (optional)
    - `color`: The color of the speed dial item (optional)

    :References:

    - https://panel-material-ui.holoviz.org/reference/menus/SpeedDial.html
    - https://mui.com/material-ui/react-speed-dial/

    :Example:

    >>> pmui.SpeedDial(items=[
    ...     {'label': 'Camera', 'icon': 'camera'},
    ...     {'label': 'Photos', 'icon': 'photo'},
    ...     {'label': 'Documents', 'icon': 'article'},
    ... ], active=2, margin=(50, 20))
    """

    color = param.Selector(default="primary", objects=COLORS, doc="""
        The color of the menu.""")

    direction = param.Selector(default="right", objects=["right", "left", "up", "down"], doc="""
        The direction of the menu.""")

    icon = param.String(default=None, doc="""
        The icon to display when the menu is closed.""")

    open_icon = param.String(default=None, doc="""
        The icon to display when the menu is open.""")

    persistent_tooltips = param.Boolean(default=False, doc="""
        Whether to show persistent tooltips next to the menu items.""")

    _esm_base = "SpeedDial.jsx"

    _item_keys = ['label', 'icon', 'avatar', 'color']



__all__ = [
    "Breadcrumbs",
    "MenuButton",
    "MenuList",
    "MenuToggle",
    "NestedBreadcrumbs",
    "Pagination",
    "SpeedDial",
    "SplitButton",
    "TabMenu",
    "Tree"
]
