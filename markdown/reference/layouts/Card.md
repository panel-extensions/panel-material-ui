```python
import panel as pn
import panel_material_ui as pmui
from panel_material_ui import Card

pn.extension()
```

The `Card` component creates a collapsible container with a header bar.

## Parameters

### Core

* **`collapsed`** (`boolean`): Whether the card content is collapsed. 
* **`collapsible`** (`boolean`): Whether the card can be expanded/collapsed.
* **`header`** (`Panel component`): Custom component to display in the header bar.
* **`hide_header`** (`boolean`): Whether to hide the header bar.
* **`title`** (`str`): Text to display in the header (overridden by header if set).

### Style

* **`disable_gutters`** (`boolean`): Whether to disable margins between expanded sections.
* **`elevation`** (`int`): The elevation level of the card surface.
* **`header_background`** (`str`): The background color of the header.
* **`header_color`** (`str`): The color of the header text.
* **`raised`** (`boolean`): Whether the card appears elevated above the background.
* **`square`** (`boolean`): Whether to disable rounded corners.
* **`title_variant`** (`str`): The text variant of the header title (default="h3").
* **`variant`** (`Literal["filled", "outlined"]`): Whether to show an outline instead of elevation.

---


```python
w1 = pmui.TextInput(label='Text:')
w2 = pmui.FloatSlider(label='Slider')

card = Card(w1, w2, title='Card', margin=10)
card
```

The contents of the `Card.objects` list should never be modified individually, because Panel cannot detect when items in that list have changed internally, and will thus fail to update any already-rendered views of those objects. Instead, use the provided methods for adding and removing items from the list. The only change that is safe to make directly to `Card.objects` is to replace the list of objects entirely. As a simple example of using the methods, we might add an additional widget to the card using the append method:


```python
w3 = pmui.Select(options=['A', 'B', 'C'])
card.append(w3)
```

On a live server or in a notebook the card displayed after the previous code cell (above) will dynamically expand in size to accommodate all three widgets and the title. To see the effect in a statically rendered page, we will display the column a second time:


```python
card
```

Whether the Card is collapsed or not can be controlled from Python and Javascript:


```python
print(card.collapsed)
card.collapsed = True
```

## Style

By default `Card` elements have an `elevation` (just like the `Paper` layout). The level of the elevation can be set:


```python
pmui.Row(*(
    Card(elevation=e, margin=10, title=f'Elevation={e}')
    for e in (0, 1, 2, 4, 8, 12)
))
```

Alternatively the `Card` can be `outlined`:


```python
Card(w1, w2, variant='outlined', margin=10, title='Outlined')
```

## Header

Instead of using a title, a Card may also be given an explicit header that can contain any component, e.g. in this case the Panel logo:


```python
logo = 'https://panel.holoviz.org/_static/logo_horizontal.png'

red   = pn.Spacer(styles=dict(background='red'), height=50)
green = pn.Spacer(styles=dict(background='green'), height=50)
blue  = pn.Spacer(styles=dict(background='blue'), height=50)

Card(
    red, green, blue,
    header_background='#2f2f2f',
    header_color='white',
    header=pn.panel(logo, height=40),
    width=300,
)
```

It is also possible to render a Card entirely without a header:


```python
Card(
    pn.indicators.Number(value=42, default_color='white', name='Completion', format='{value}%'),
    sx={'background': 'darkgray'},
    hide_header=True,
)
```

## Layout

In general a `Card` does not have to be given an explicit `width`, `height`, or `sizing_mode`, allowing it to adapt to the size of its contents. However in certain cases it can be useful to declare a fixed-size layout, which its responsively sized contents will then fill, making it possible to achieve equal spacing between multiple objects:


```python
red   = pn.Spacer(styles=dict(background='red'), sizing_mode='stretch_both')
green = pn.Spacer(styles=dict(background='green'), sizing_mode='stretch_both')
blue  = pn.Spacer(styles=dict(background='blue'), sizing_mode='stretch_both')

Card(red, green, blue, height=300, width=200, title='Fixed size', margin=10)
```

When no fixed size is specified the column will expand to accommodate the sizing behavior of its contents:


```python
from bokeh.plotting import figure

p1 = figure(height=250, sizing_mode='stretch_width', margin=5)
p2 = figure(height=250, sizing_mode='stretch_width', margin=5)

p1.line([1, 2, 3], [1, 2, 3])
p2.scatter([1, 2, 3], [1, 2, 3])

Card(p1, pn.layout.Divider(), p2, title="Responsive", sizing_mode='stretch_width', margin=10)
```
