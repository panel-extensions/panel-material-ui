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

from ..base import COLORS
from .base import MaterialWidget
from .button import _ButtonBase


def filter_item(item, keys):
    if isinstance(item, dict):
        item = {k: v for k, v in item.items() if k in keys}
        if 'children' in item:
            item['children'] = [filter_item(child, keys) for child in item['children']]
        return item
    return item


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

    _item_keys = ['label', 'children']
    _rename = {'value': None}
    _source_transforms = {'attached': None, "value": None, 'items': None}

    __abstract = True

    def __init__(self, **params):
        click_handler = params.pop('on_click', None)
        super().__init__(**params)
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
            params['items'] = [filter_item(item, self._item_keys) for item in items]
        return params

    @param.depends('items', watch=True, on_init=True)
    def _sync_items(self):
         self.param.active.bounds = (0, len(self.items)-1)

    @param.depends('active', watch=True, on_init=True)
    def _sync_active(self):
         self.value = self._lookup_item(self.active)

    @param.depends('value', watch=True, on_init=True)
    def _sync_value(self):
        index = self._lookup_active_by_value(self.value)
        if index is None:
            self.active = None
        else:
            self.active = index if len(index) > 1 else index[0]

    def _lookup_active_by_value(self, item):
        if not self.items:
            return None
        queue = [([], 0, self.items)]
        while queue:
            path, depth, items = queue.pop(0)

            for i, current in enumerate(items):
                current_path = path + [i]
                if current == item:
                    return tuple(current_path)
                if isinstance(current, dict):
                    if current == item:
                        return tuple(current_path)
                    if 'items' in current:
                        queue.append((current_path, depth + 1, current['items']))
        return None

    def _lookup_item(self, index):
        if index is None:
            return
        indexes = index if isinstance(index, tuple) else [index]
        value = self.items
        for i, idx in enumerate(indexes):
            value = value[idx]
            if isinstance(value, dict) and (i != len(indexes)-1):
                value = value['items']

        if isinstance(value, tuple):
            value = {'label': value[0], 'value': value[1]}
        return value

    def _handle_msg(self, msg):
        index = msg['item']
        if isinstance(index, list):
            index = tuple(index)
        value = self._lookup_item(index)
        if msg['type'] == 'click':
            if not isinstance(value, dict) or value.get('selectable', True):
                self.param.update(active=index, value=value)
            for fn in self._on_click_callbacks:
                try:
                    state.execute(partial(fn, value))
                except Exception as e:
                    print(f'List on_click handler errored: {e}')  # noqa
        elif msg['type'] == 'action':
            for fn in self._on_action_callbacks.get(msg['action'], []):
                try:
                    state.execute(partial(fn, value))
                except Exception as e:
                    print(f'List on_action handler errored: {e}')  # noqa

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


class Breadcrumbs(MenuBase):
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

    color = param.Selector(objects=COLORS, default="primary")

    max_items = param.Integer(default=None, bounds=(1, None), doc="""
        The maximum number of breadcrumb items to display.""")

    separator = param.String(default=None, doc="""
        The separator displayed between breadcrumb items.""")

    _esm_base = "Breadcrumbs.jsx"
    _item_keys = ['label', 'icon', 'avatar', 'href']


class List(MenuBase):
    """
    The `List` component is used to display a structured group of items, such as menus,
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

    :References:

    - https://panel-material-ui.holoviz.org/reference/menus/List.html
    - https://mui.com/material-ui/react-list/

    :Example:

    >>> pmui.List(items=[
    ...     {'label': 'Home', 'icon': 'home', 'secondary': 'Overview page'},
    ...     {'label': 'Gallery', 'icon': 'image', 'secondary': 'Visual overview'},
    ...     {'label': 'API', 'icon': 'code', 'secondary': 'API Reference'},
    ...     {'label': 'About', 'icon': 'info'},
    ... ], active=3)
    """

    active = param.ClassSelector(default=None, class_=(int, tuple), doc="""
        The index of the currently selected item. Can be a tuple of indices for nested items.""")

    color = param.Selector(default="primary", objects=COLORS, doc="The color of the selected list item.")

    dense = param.Boolean(default=False, doc="Whether to show the list items in a dense format.")

    highlight = param.Boolean(default=True, doc="""
        Whether to highlight the currently selected menu item.""")

    level_indent = param.Integer(default=16, doc="The number of pixels to indent the list items.")

    removable = param.Boolean(default=False, doc="Whether to allow deleting items.")

    _esm_base = "List.jsx"

    _item_keys = ['label', 'items', 'icon', 'avatar', 'color', 'secondary', 'actions', 'selectable', 'href', 'buttons']

    @param.depends('items', watch=True, on_init=True)
    def _sync_items(self):
         pass

    def _process_property_change(self, props):
        props = super()._process_property_change(props)
        if 'active' in props and isinstance(props['active'], list):
            props['active'] = tuple(props['active'])
        return props

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


class MenuButton(MenuBase, _ButtonBase):
    """
    The `MenuButton` component is a button component that allows selecting from a list of items.

    MenuButton items can be strings or objects with properties:
      - label: The label of the menu button item (required)
      - icon: The icon of the menu button item (optional)
      - color: The color of the menu button item (optional)

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

    _esm_base = "MenuButton.jsx"
    _source_transforms = {
        "attached": None,
        "button_type": None,
        "button_style": None
    }
    _item_keys = ['label', 'icon', 'color', 'items']


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
    "List",
    "MenuButton",
    "Pagination",
    "SpeedDial"
]
