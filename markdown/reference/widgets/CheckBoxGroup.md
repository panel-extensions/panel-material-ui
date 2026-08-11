```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `CheckBoxGroup` widget allows users to select multiple options from a list by checking the corresponding checkboxes. This widget is part of the multi-option selection family, which includes [`MultiSelect`](MultiSelect.ipynb), [`CrossSelector`](CrossSelector.ipynb), and [`CheckButtonGroup`](CheckButtonGroup.ipynb) widgets that share a compatible API.

#### Parameters

For more details on customization options, see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (bool): If True, the widget is not interactive.
* **`options`** (list or dict): The available options to choose from. Can be a list of strings or a dictionary mapping labels to values.
* **`value`** (list): The currently selected options.

##### Display

* **`inline`** (bool): Whether to lay out the options in a row (`inline=True`) or column (the default).
* **`label`** (str): The title displayed above the checkbox group.
* **`label_placement`** (`Literal["bottom", "start", "top", "end"]`): Placement of the option labels.
* **`loading`** (bool): If True, displays a loading spinner over the component.

##### Styling

- **`color`** (str): The color theme for the checkboxes.
- **`sx`** (dict): Component-level styling options.
- **`theme_config`** (dict): Theming configuration.

##### Aliases

For compatibility with Panel, some parameters have aliases:

- **`name`**: Alias for `label`

___

### Basic Usage

Create a checkbox group with a list of options. Users can select multiple items by checking the corresponding boxes:


```python
checkbox_group = pmui.CheckBoxGroup(
    label='Checkbox Group', value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry'], inline=True
)

checkbox_group
```

The `value` parameter returns a list of the currently selected options:


```python
checkbox_group.value
```

### Dictionary Options

You can provide options as a dictionary where keys are the displayed labels and values are the actual option values:


```python
dict_group = pmui.CheckBoxGroup(
    label='Checkbox Group', value=['A', 'P'], options={'Apple': 'A', 'Banana': 'B', 'Pear': 'P', 'Strawberry': 'S'},
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
    pmui.CheckBoxGroup(label='Horizontal', value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry'], inline=True),
    pmui.CheckBoxGroup(label='Vertical', value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry'], inline=False)
)
```

## Label Placement

You may provide a `label_placement` as one of "bottom", "start", "top", "end":


```python
pmui.FlexBox(
    *(pmui.CheckBoxGroup(label=lp, label_placement=lp, inline=True, value=['Apple'], options=['Apple', 'Banana']) for lp in pmui.CheckBoxGroup.param.label_placement.objects)
)
```

### Color Options

Customize the appearance of checkboxes using the `color` parameter:


```python
pmui.FlexBox(
    *(pmui.CheckBoxGroup(label=color, color=color, inline=True, value=['Apple'], options=['Apple', 'Banana']) for color in pmui.CheckBoxGroup.param.color.objects)
)
```

### Disabled and Loading

Like other widgets, the `CheckBoxGroup` can be disabled and/or show a loading indicator.


```python
pmui.CheckBoxGroup(
    label='Checkbox Group', value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry'],
    disabled=True, loading=True
)
```

### Example: Interactive Pizza Order Form

Let's create a practical example showing how `CheckBoxGroup` can be used in a real application. This pizza ordering interface demonstrates real-time updates based on user selections:


```python
import panel as pn
import panel_material_ui as pmui

pn.extension()

toppings = pmui.CheckBoxGroup(
    label="Select your toppings:",
    options=['Pepperoni', 'Mushrooms', 'Bell Peppers', 'Onions', 'Olives', 'Extra Cheese'],
    value=['Pepperoni', 'Onions'],
    inline=True,
)

def create_order_summary(toppings):
    summary = f"## 🧺 Your Pizza Order\n\n"
    summary += f"• Toppings: {', '.join(toppings) if toppings else 'None'}\n"
    
    base_price = 12.99
    topping_price = len(toppings) * 1.50
    total = base_price + topping_price
    summary += f"\n**Total: ${total:.2f}**"
    
    return summary

order_summary = pn.bind(create_order_summary, toppings=toppings)

pmui.Column(
    "## 🍕 Pizza Order Form",
    toppings,
    "---",
    order_summary,
    width=800
)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
icon_options = {
    ":material/zoom_out_map: Full screen": "fullscreen",
    ":material/zoom_in: Zoom in": "zoom_in",
    ":material/zoom_out: Zoom out": "zoom_out",
}

pmui.CheckBoxGroup(
    label=":material/zoom_out_map: View",
    options=icon_options,
    value=["fullscreen", "zoom_in"],
    inline=True,
)
```

### API Reference

#### Parameters


```python
pmui.CheckBoxGroup(
    label='Checkbox Group', value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry'],
).api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI CheckBox:**

- [Material UI CheckBox Reference](https://mui.com/material-ui/react-checkbox/#formgroup) - Complete documentation for the underlying Material UI component
