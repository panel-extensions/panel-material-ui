from __future__ import annotations

from collections import defaultdict
from functools import partial
from typing import Callable

import param
from panel.io.state import state
from panel.models.reactive_html import DOMEvent

from ..base import COLORS
from .base import MaterialWidget


def filter_item(item, keys):
    if isinstance(item, dict):
        item = {k: v for k, v in item.items() if k in keys}
        if 'children' in item:
            item['children'] = filter_items(item['children'], keys)
        return item
    return item


def filter_items(items, keys):
    if isinstance(items, dict):
        return {k: filter_item(v, keys) for k, v in items.items()}
    elif isinstance(items, list):
        return [filter_item(item, keys) for item in items]
    elif isinstance(items, list):
        filtered_items = []
        for item in items:
            if isinstance(item, dict):
                filtered_items.append(filter_item(item, keys))
            else:
                filtered_items.append(item)
        return filtered_items
    return items


class MenuBase(MaterialWidget):

    items = param.ClassSelector(default=[], class_=(list, dict), doc="""
        List of items to display. Each item may be a string, a tuple mapping from a label to a value,
        or an object with a few common properties and a few widget specific properties.""")

    value = param.ClassSelector(default=None, class_=(dict, str), doc="""
        Last clicked menu item.""")

    width = param.Integer(default=None, doc="""
        The width of the menu.""")

    _item_keys = ['label', 'children']
    _rename = {'value': None}

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
                items = {}
                for index, item in enumerate(params['items']):
                    if isinstance(item, tuple):
                        items[item[0]] = item[1]
                    elif isinstance(item, dict):
                        items[item['label']] = item
                    elif item is None:
                        items[f'--- {index}'] = None
                    else:
                        items[item] = item
            else:
                items = params['items']
            params['items'] = filter_items(items, self._item_keys)
        return params

    def _handle_msg(self, msg):
        path = msg['item']
        keys = path if isinstance(path, list) else [path]
        value = self.items
        for key in keys:
            if isinstance(value, dict):
                value = value['subitems']
            value = value[key]
        if msg['type'] == 'click':
            self.value = value
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
      - label: The label of the breadcrumb item (required)
      - icon: The icon of the breadcrumb item (optional)
      - avatar: The avatar of the breadcrumb item (optional)
      - secondary: The secondary text of the breadcrumb item (optional)

    Reference: https://mui.com/material-ui/react-breadcrumbs/
    """

    active = param.Integer(default=None)

    color = param.Selector(objects=COLORS, default="primary")

    separator = param.String(default=None, doc="The separator displayed between breadcrumb items.")

    _esm_base = "Breadcrumbs.jsx"
    _item_keys = ['label', 'icon', 'avatar', 'color', 'secondary']



class List(MenuBase):
    """
    The `List` component is used to display a structured group of items, such as menus,
    navigation links, or settings.

    List items can be strings or objects with properties:
      - label: The label of the list item (required)
      - icon: The icon of the list item (optional)
      - avatar: The avatar of the list item (optional)
      - color: The color of the list item (optional)
      - secondary: The secondary text of the list item (optional)

    Reference: https://mui.com/material-ui/react-list/
    """

    dense = param.Boolean(default=False, doc="Whether to show the list items in a dense format.")

    removable = param.Boolean(default=False, doc="Whether to allow deleting items.")

    _esm_base = "List.jsx"

    _item_keys = ['label', 'children', 'icon', 'avatar', 'color', 'secondary', 'actions']

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


class SpeedDial(MenuBase):
    """
    The `SpeedDial` component is a menu component that allows selecting from a
    list of items.

    SpeedDial items can be strings or objects with properties:
      - label: The label of the speed dial item (required)
      - icon: The icon of the speed dial item (optional)
      - avatar: The avatar of the speed dial item (optional)
      - color: The color of the speed dial item (optional)

    Reference: https://mui.com/material-ui/react-speed-dial/
    """

    color = param.Selector(default="primary", objects=COLORS, doc="""
        The color of the menu.""")

    direction = param.Selector(default="right", objects=["right", "left", "up", "down"], doc="""
        The direction of the menu.""")

    icon = param.String(default=None, doc="""
        The icon to display when the menu is closed.""")

    open_icon = param.String(default=None, doc="""
        The icon to display when the menu is open.""")

    _esm_base = "SpeedDial.jsx"

    _item_keys = ['label', 'icon', 'avatar', 'color']


class Pagination(MaterialWidget):
    """
    The `Pagination` component allows selecting from a list of pages.

    Reference: https://mui.com/material-ui/react-pagination/
    """

    color = param.Selector(default="primary", objects=COLORS, doc="The color of the pagination.")

    count = param.Integer(default=None, doc="The total number of pages.")

    shape = param.Selector(default="circular", objects=["circular", "rounded"], doc="The shape of the pagination.")

    size = param.Selector(default="medium", objects=["small", "medium", "large"], doc="The size of the pagination.")

    sibling_count = param.Integer(default=1, doc="The number of sibling pages to show.")

    boundary_count = param.Integer(default=1, doc="The number of boundary pages to show.")

    show_first_button = param.Boolean(default=False, doc="Whether to show the first button.")

    show_last_button = param.Boolean(default=False, doc="Whether to show the last button.")

    value = param.Integer(default=None, doc="The current zero-indexed page number.")

    width = param.Integer(default=None, doc="The width of the pagination.")

    _esm_base = "Pagination.jsx"

    @param.depends('count', watch=True, on_init=True)
    def _update_count(self):
        self.param.value.bounds = (0, self.count - 1)


__all__ = [
    "Breadcrumbs",
    "List",
    "SpeedDial",
    "Pagination"
]
