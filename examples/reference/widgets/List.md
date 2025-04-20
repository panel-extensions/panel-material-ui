# List

```python
import panel as pn
import panel_material_ui as pmu
from panel_material_ui.widgets import List

pn.extension()
```

## API

### Parameters

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

#### Core

* **`disabled`** (boolean): Whether the widget is editable
* **`items`** (list or dict): List of items to display. Each item may be a string, a tuple mapping from a label to a value,
        or an object with a few common properties and a few widget specific properties.
* **`value`** (dict, str): The current value; must be one of the option values

* **`removable`** (list): Whether to allow deleting items.

#### Styling

* **`sx`** (dict): Component level styling API.
* **`theme_config`** (dict): Theming API.
* **`dense`** (bool): Whether to show the list items in a dense format.

#### Aliases

For compatibility with Panel certain parameters are allowed as aliases:

* **`name`**: Alias for `label`

___

## Basic List

By providing a list of `items` you can define the list.

```python
menu = List(items=['Dashboard', 'Tables', 'Notifications'])
menu.servable()
```

You will notice that the capitalized, first letter of each item is used as an *Avatar*.

The selected item will be shown in the `.value` parameter

```python
pn.panel(menu.param.value).servable()
```

Try clicking an item.

**TODO: Figure out how to visually select item when clicking**

You can also set an initial selected `value`

**TODO: Get this working**.

```python
List(items=['Dashboard', 'Tables', 'Notifications'], value="Dashboard").servable()
```

## Add Header

By setting the `name` you can add a header to the `List`.

```python
menu = List(name="Pages", items=['Dashboard', 'Tables', 'Notifications'])
menu.servable()
```

## Disabled

```python
List(items=['Dashboard', 'Tables', 'Notifications'], disabled=True).servable()
```

**TODO: Get disabled working**

## Items as a List of Tuples

You can provide the `items` as list of tuples

```python
menu = List(name="Pages", items=[('1', 'Dashboard'), ('2', 'Tables'), ('3', 'Notifications')])
pn.Column(menu, menu.param.value).servable()
```

**TODO: Fix `TypeError: list indices must be integers or slices, not str` raised when clicked.**

## Items as a Dictionary

You can provide the `items` as dictionary

```python
import panel as pn
from panel.custom import ReactComponent
import param
from panel_material_ui.base import COLORS
from panel_material_ui.widgets import List

pn.extension()

menu = List(name="Pages", items={
    'No Icon or Avatar': {"label": "No Icon or Avatar"},
    'Icon': {"label": "Icon", "icon": "info"},
    'Icon w color': {"label": "Icon w color", "icon": "info", "color": "primary"},
    'Avatar': {"label": "Avatar String", "avatar": "SA"},
    'Avatar Image': {"label": "Avatar Image", "avatar": "https://cdn.jsdelivr.net/gh/alohe/avatars/png/memo_2.png"},
    'href': {"label": "Open Link Button", "icon": "east", "href": "https://panel.holoviz.org"},
    'actions': {"label": "Actions", "icon": "recommend", "actions": [{"label": "Increment", "icon": "add"}, {"label": "Decrement", "icon": "remove"}]},
    'Subitems': {"label": "Subitems", "icon": "thumb_up", "color": "success", "subitems": {"A": {"label": "A"}, "B": {"label": "B"}, "C": {"label": "C"}}},
}, width=500, removable=True)
pn.Column(menu, menu.param.value).servable()
```

- **TODO: Fix `TypeError: list indices must be integers or slices, not str` raised when clicked.**
- **TODO: Get actions working. I can see the msg sent are `{'type': 'click', 'item': ['actions']}` but its looking for 'type': 'action' not 'click'.**
- **TODO: Get subitems working. I can see they are not included in _item_keys**
- **TODO: Support avatar src url**
- **TODO: Consider whether its a better api to support a list of dicts than a dict of dicts. The keys are not used for anything.**

## Removable

```python
List(name="Pages", items=['Dashboard', 'Tables', 'Notifications'], removable=True).servable()
```

**TODO: Make removable. I don't see any way to do this.**

## Styling

### Dense

By setting the `dense` parameter you can change the appearance.

```python
List(name="Pages", items=['Dashboard', 'Tables', 'Notifications'], dense=True).servable()
```

**TODO: Make dense. I don't see any changes**

### Divider

### Custom Menu

```python
import panel as pn
from panel.custom import ReactComponent
import param
from panel_material_ui.base import COLORS
from panel_material_ui.widgets import List

pn.extension()

List(
    name="Menu",
    items={
    "Github": { "label": 'GitHub', "icon": 'code', "href": 'https://github.com/panel-extensions/panel-material-ui'},
    "Discourse": { "label": 'Discourse', "icon": 'people', "href": "https://discourse.holoviz.org/" },
    "Discord": { "label": 'Discord', "icon": 'chat'},
}, sx={
    '& .MuiListItemButton-root': {
        "border-radius": "var( --mui-shape-borderRadius )",
        "height": "40px",
    },
    '& .MuiListItemButton-root:hover': {
        'bgcolor': 'black',
        'color': 'white',
        '& .MuiListItemIcon-root': {
            'color': 'white',
        },
    }
}, width=300).servable()
```

**TODO: Figure out how to set the selected `value` initially.
