```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `RadioBoxGroup` widget allows selecting from a list or dictionary of values using a set of checkboxes. It falls into the broad category of single-value, option-selection widgets that provide a compatible API and include the [`RadioButtonGroup`](RadioButtonGroup.ipynb), [`Select`](Select.ipynb) and [`DiscreteSlider`](DiscreteSlider.ipynb) widgets.

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html). Alternatively, learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (boolean): Whether the widget is editable
* **`options`** (list or dict): A list or dictionary of options to select from
* **`value`** (object): The current value; must be one of the option values

##### Display

* **`color`** (str): The color variant of the radio controls, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`inline`** (boolean): Whether to arrange the items vertically in a column (``False``) or horizontally in a line (``True``)
* **`label`** (str): The title of the widget

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

##### Aliases

For compatibility with Panel certain parameters are allowed as aliases:

- **`button_style`**: Alias for `variant`
- **`button_type`**: Alias for `color`
- **`name`**: Alias for `label`

___


```python
radio_group = pmui.RadioBoxGroup(label='RadioBoxGroup', options=['Biology', 'Chemistry', 'Physics'], inline=True)

radio_group
```

Like most other widgets, ``RadioBoxGroup`` has a value parameter that can be accessed or set:


```python
radio_group.value
```

### Dictionary Options

You can provide options as a dictionary where keys are the displayed labels and values are the actual option values:


```python
dict_group = pmui.RadioBoxGroup(
    label='Radiobox Group', value=['A', 'P'], options={'Apple': 'A', 'Banana': 'B', 'Pear': 'P', 'Strawberry': 'S'},
    inline=True,
)

dict_group
```

Let's observe how the `value` parameter reflects the selected dictionary values (not the labels):


```python
pn.pane.Str(dict_group.param.value)
```

### Orientation

Control the layout of checkboxes using the `inline` parameter:


```python
pmui.Column(
    pmui.RadioBoxGroup(label='Horizontal', value='Apple', options=['Apple', 'Banana', 'Pear', 'Strawberry'], inline=True),
    pmui.RadioBoxGroup(label='Vertical', value='Banana', options=['Apple', 'Banana', 'Pear', 'Strawberry'], inline=False)
)
```

## Label Placement

You may provide a `label_placement` as one of "bottom", "start", "top", "end":


```python
pmui.FlexBox(
    *(pmui.RadioBoxGroup(
        label=lp, label_placement=lp, inline=True, value='Apple', options=['Apple', 'Banana']
    ) for lp in pmui.RadioBoxGroup.param.label_placement.objects)
)
```

### Color Options

Customize the appearance of checkboxes using the `color` parameter:


```python
pmui.FlexBox(
    *(pmui.RadioBoxGroup(
        label=color, color=color, inline=True, value='Apple', options=['Apple', 'Banana']
    ) for color in pmui.RadioBoxGroup.param.color.objects)
)
```

### Disabled and Loading States

Like other widgets, `RadioBoxGroup` can be disabled and/or show a loading indicator.


```python
pmui.RadioBoxGroup(
    label='Radiobox Group', value='Pear', options=['Apple', 'Banana', 'Pear', 'Strawberry'],
    disabled=True, loading=True
)
```

### Example: Interactive Pizza Order Form

Let's create a practical example showing how `RadioBoxGroup` can be used in a real application. This pizza ordering interface demonstrates real-time updates based on user selections:


```python
import panel as pn
import panel_material_ui as pmui

pn.extension()

pizza = pmui.RadioBoxGroup(
    label="Select your Pizza:",
    options=['Pepperoni', 'Margharita', 'Fior di Late', 'Hawaii'],
    value='Pepperoni',
    inline=True,
)

def create_order_summary(topping):
    summary = f"## 🧺 Your Pizza Order\n\n"
    summary += f"Type: {topping}\n"
    
    total = 12.99 + (99 if topping == 'Hawaii' else 0)
    summary += f"\n**Total: ${total:.2f}**"
    
    return summary

order_summary = pn.bind(create_order_summary, topping=pizza)

pmui.Column(
    "## 🍕 Pizza Order Form",
    pizza,
    "---",
    order_summary,
    width=800
)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
pmui.RadioBoxGroup(
    label="Mode :material/zoom_out_map:",
    options={"Zoom :material/zoom_out_map:": "zoom", "Explore :material/explore:": "explore"},
    value="zoom",
    inline=True,
)
```

### API Reference

#### Parameters


```python
pmui.RadioBoxGroup(
    label='Radiobox Group', value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry'],
).api(jslink=True)
```

### References

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html).

Learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

See also the Material UI `Radiobox` [Reference](https://mui.com/material-ui/react-checkbox/#formgroup) for inspiration.


```python
pmui.Row(radio_group.controls(jslink=True), radio_group)
```
