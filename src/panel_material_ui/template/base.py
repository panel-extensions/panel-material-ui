import param
from panel.viewable import Children

from ..base import MaterialComponent


class Page(MaterialComponent):
    """
    The `Page` component is the equivalent of a `Template` in Panel.

    Unlike a `Template` the `Page` component is implemented entirely
    in Javascript, making it possible to dynamically update components.

    :Example:

    >>> Page(main=['# Content'], title='My App')
    """

    header = Children(doc="Items rendered in the header.")

    main = Children(doc="Items rendered in the main area.")

    sidebar = Children(doc="Items rendered in the sidebar.")

    sidebar_open = param.Boolean(default=True, doc="Whether the sidebar is open or closed.")

    sidebar_variant = param.Selector(default="persistent", objects=["persistent", "drawer"])

    sidebar_width = param.Integer(default=250, doc="Width of the sidebar")

    title = param.String(doc="Title of the application.")

    _esm_base = "Page.jsx"
