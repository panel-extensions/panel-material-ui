```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Accordion` component creates expandable/collapsible sections. The labels for each section may be defined explicitly as part of a tuple, and otherwise default to the name parameter of the card’s contents. Like Column and Row, Tabs has a list-like API that allows interactively updating and modifying the cards using methods append, extend, clear, insert, pop, remove and `__setitem__` (to replace the contents).

## Parameters:

### Core

* **`active`** (`list[int]`): List of indexes of currently expanded sections.
* **`disabled`** (`list[int]`): List of indexes of disabled sections.
* **`toggle`** (`boolean`): If True, only one section can be expanded at a time.

### Style

* **`active_header_background`** (`str`): The text color of the header when the Card is expanded.
* **`active_header_color`** (`str`): The background color of the header when the Card is expanded.
* **`disable_gutters`** (`boolean`): Whether to disable margins between expanded sections.
* **`elevation`** (`int`): The elevation level of the card surface.
* **`header_background`** (`str`): The background color of the header.
* **`header_color`** (`str`): The color of the header text.
* **`raised`** (`boolean`): Whether the card appears elevated above the background.
* **`square`** (`boolean`): Whether to disable rounded corners.
* **`title_variant`** (`str`): The text variant of the header title (default="h3").
* **`variant`** (`Literal["filled", "outlined"]`): Whether to show an outline instead of elevation.

---

### Basic Usage

The `Accordion` renders a list of items into a stack of collapsible cards. The labels can be provided as tuples and whether a card is expanded is controlled via the `active parameter:


```python
pmui.Accordion(
    ('Title 1', 'My content'),
    ('Title 2', 'My secondary content'),
    active=[1]
)
```

### Objects & Headers

An Accordion layout can either be instantiated as empty and populated after the fact, or by using a list of objects provided on instantiation as positional arguments.

If the objects are not already Panel components they will each be converted to one using the pn.panel conversion method. 

Unlike other panel types, Accordion also accepts tuples to specify the title of each tab; if no name is supplied explicitly the name of the underlying object will be used:


```python
from bokeh.plotting import figure

p1 = figure(width=300, height=300, name='Scatter', margin=5)
p1.scatter([0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 2, 1, 0])

p2 = figure(width=300, height=300, name='Line', margin=5)
p2.line([0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 2, 1, 0])

accordion = pmui.Accordion(('Scatter', p1), p2, margin=10)
accordion
```

The contents of the Accordion.objects list should never be modified individually, because Panel cannot detect when items in that list have changed internally, and will thus fail to update any already-rendered views of those objects (and their card titles!). Instead, use the provided methods for adding and removing items from the list. The only change that is safe to make directly to Accordion.objects is to replace the list of objects entirely. As a simple example of using the methods, we might add an additional widget to the Accordion using the append method:


```python
p3 = figure(width=300, height=300, name='Square', margin=5)
p3.scatter([0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 2, 1, 0], marker='square', size=10)

accordion.append(('Square', p3))
```

On a live server or in a notebook the accordion displayed above will dynamically expand to include the new card. To see the effect in a statically rendered page, we will display the accordion a second time:


```python
accordion
```

#### HTML & Component Titles

The titles of each card may also contain HTML or render Panel components:


```python
component_title = pmui.Row(
    pmui.IconButton(icon='show_chart', size='small', margin=(10, 0)),
    '#### Line'
)

line = figure(width=300, height=300, name='Line')
line.line([0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 2, 1, 0])

html_title = """
<p style="display: inline-flex; align-items: center;">
  <span class="material-icons" style="font-size: 1.2em; padding-right: 1em;">square</span>
  <span>Square</span>
</p>"""

square = figure(width=300, height=300, name='Square')
square.scatter([0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 2, 1, 0], marker='square', size=10)

pmui.Accordion(
    (component_title, line),
    (html_title, square)
).show()
```

### `active`

In addition to being able to modify the objects using methods we can also get and set the currently active cards as a list of integers, which will update any rendered views of the object:


```python
pmui.Accordion(p1, p2, p3, active=[0, 2], margin=10)
```

### `disabled`

The `disabled` parameter also contains indexes but instead controls which section can't be expanded.


```python
pmui.Accordion(
    'Foo', 'Bar', 'Baz', disabled=[2]
)
```

### `toggle`

When toggle is enabled only one card can be active at the same time, i.e., expanding one card will collapse the other active cards (much like a Tabs layout).


```python
accordion.clone(toggle=True, active=[0])
```
