```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Tabs` component organizes content into separate views that can be switched between.

### Parameters:

#### Core

* **`active`** (`int`): Index of the currently active tab.
* **`closable`** (`boolean`): Whether tabs can be closed.
* **`disabled`** (`list[int]`): Integer indexes of disabled tabs.
* **`dynamic`** (`boolean`): Whether to render tab contents only when active.

### Display

* **`centered`** (`boolean`): Whether to center the tab labels.
* **`color`** (`Literal["default", "primary", "secondary"]`): The color variant of the highlight indicating the active tab, which must be one of `'default'`, `'primary'`, or `'secondary'`.
* **`tabs_location`** (`Literal["above", "below", "left", "right"]`): Position of the tab labels relative to content.
* **`wrapped`** (`boolean`): Whether labels should be wrapped.

---

### Basic Usage

The `Tabs` layout renders a list of items into a series of selectable tabs. The labels can be provided as tuples and the active tab is controlled via the `active` parameter:


```python
pmui.Tabs(
    ('Title 1', 'My content'),
    ('Title 2', 'My secondary content'),
    active=1
)
```

### Objects & Headers

A `Tabs` layout can either be instantiated as empty and be populated after the fact, or using a list of objects provided as positional arguments. If the objects are not already Panel components they will each be converted to one using the `pn.panel` conversion method. Unlike other panel `Tabs` also accepts tuples to specify the title of each tab, if no name is supplied explicitly the name of the underlying object will be used.


```python
from bokeh.plotting import figure

p1 = figure(width=300, height=300, name='Scatter')
p1.scatter([0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 2, 1, 0])

p2 = figure(width=300, height=300, name='Line')
p2.line([0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 2, 1, 0])

tabs = pmui.Tabs(('Scatter', p1), p2)
tabs
```

The ``Tabs`` objects should never be modified directly. Instead, it is recommended to modify tabs using the provided methods, except when replacing the list of ``objects`` entirely.  Using the methods ensures that the rendered views of the ``Tabs`` are rerendered in response to the change, but even more importantly it ensures the tab titles are kept in sync with the objects. As a simple example we might add an additional widget to the ``tabs`` using the append method:


```python
p3 = figure(width=300, height=300, name='Square')
p3.scatter([0, 1, 2, 3, 4, 5, 6], [0, 1, 2, 3, 2, 1, 0], marker='square', size=10)

tabs.append(p3)
```

On a live server or in a notebook the `tabs` displayed above will dynamically expand to include the new tab. To see the effect in a statically rendered page, we will display the tabs a second time:


```python
tabs
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

pmui.Tabs(
    (component_title, line),
    (html_title, square)
)
```

#### ``active``

In addition to being able to modify the ``objects`` using methods we can also get and set the currently ``active`` tab as an integer, which will update any rendered views of the object:


```python
print(tabs.active)
tabs.active = 0
```

#### ``dynamic``

When enabled the dynamic option ensures that only the active tab is actually rendered, only when switching to a new Tab are the contents loaded. This can be very helpful in a server context or notebook context when displaying a lot of tabs or when rendering the individual objects are very large or expensive to render. Note however that without a live server the contents of the non-active tab will never load:


```python
tabs = pmui.Tabs(p1, p2, p3, dynamic=True)

tabs
```

If you want the `Tabs` to be completely lazy when rendering some output you can leverage a [ParamFunction or ParamMethod](../../user_guide/Param.ipynb) to ensure that the output is not computed until you navigate to the tab:


```python
import time
import numpy as np

def plot():
    time.sleep(1) # some long running calculation
    np.random.seed(tabs.active)
    xs, ys = np.random.randn(2, 100)
    p = figure(width=300, height=300, name=f'Scatter Seed {tabs.active}')
    p.scatter(xs, ys)
    return p

p1 = pn.param.ParamFunction(plot, lazy=True, name='Seed 0')
p2 = pn.param.ParamFunction(plot, lazy=True, name='Seed 1')
p3 = pn.param.ParamFunction(plot, lazy=True, name='Seed 2')

tabs = pmui.Tabs(p1, p2, p3, dynamic=True)

tabs
```

#### ``closable``

``Tabs`` may also be initialized as ``closable``, which provides an `x` widget in the GUI that makes it possible to remove tabs and therefore remove them from the list of ``objects``:


```python
tabs = pmui.Tabs(
    ('red', pn.Spacer(styles=dict(background='red'), width=100, height=100)),
    ('blue', pn.Spacer(styles=dict(background='blue'), width=100, height=100)),
    ('green', pn.Spacer(styles=dict(background='green'), width=100, height=100)),
    closable=True
)

tabs
```

#### ``tabs_location``

Lastly, it is possible to modify the location of the tabs header relative to the content using the ``tabs_location`` parameter:


```python
pmui.Row(tabs, tabs.clone(active=1, tabs_location='right'), tabs.clone(active=2, tabs_location='below'), tabs.clone(tabs_location='left'))
```
