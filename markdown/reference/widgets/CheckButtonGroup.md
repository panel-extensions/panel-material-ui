```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `CheckButtonGroup` widget allows users to select multiple options from a list by toggling the corresponding buttons. It falls into the broad category of multi-option selection widgets that provide a compatible API and include the [`MultiSelect`](MultiSelect.ipynb), [`CrossSelector`](CrossSelector.ipynb) and [`CheckBoxGroup`](CheckButtonGroup.ipynb) widgets that share a compatible API.

#### Parameters:

For more details on customization options, see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (bool): If True, the widget is not interactive.
* **`options`** (list or dict): The available options to choose from. Can be a list of strings or a dictionary mapping labels to values.
* **`value`** (list): The currently selected options.

##### Display

* **`color`** (str): The color variant of the buttons, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`description`** (str | Bokeh Tooltip | pn.widgets.TooltipIcon): A description which is shown when the widget is hovered.
* **`label`** (str): The title of the widget
* **`loading`** (bool): If True, displays a loading spinner over the component.
* **`orientation`** (str, default='horizontal'): Button group orientation, either 'horizontal' or 'vertical'
* **`size`**: (str, default='medium'): The size of the widget. One of "small", "medium" or "large".

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

##### Aliases

For compatibility with Panel certain parameters are allowed as aliases:

- **`button_style`**: Alias for `variant`
- **`button_type`**: Alias for `color`
- **`name`**: Alias for `label`

___

### Basic Usage

Create a `CheckButtonGroup` with a list of options. Users can select multiple items by toggling the corresponding buttons:


```python
checkbutton_group = pmui.CheckButtonGroup(label='Check Button Group', value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry'])

checkbutton_group
```

The `value` parameter returns a list of the currently selected options:


```python
checkbutton_group.value
```

### Dictionary Options

You can provide options as a dictionary where keys are the displayed labels and values are the actual option values:


```python
dict_group = pmui.CheckButtonGroup(
    label='Check Button Group', value=['A', 'P'], options={'Apple': 'A', 'Banana': 'B', 'Pear': 'P', 'Strawberry': 'S'},
)

dict_group
```

Let's observe how the `value` parameter reflects the selected dictionary values (not the labels):


```python
pn.pane.Str(dict_group.param.value)
```

### Orientation

Control the layout of buttons using the `orientation` parameter:


```python
pmui.Column(
    pmui.CheckButtonGroup(label='Horizontal Group', orientation="horizontal", value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry']),
    pmui.CheckButtonGroup(label='Vertical Group', orientation="vertical", value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry'])
)
```

### Size Options

Adjust the `CheckButtonGroup` size using the `size` parameter:


```python
pmui.FlexBox(
    *(pmui.CheckButtonGroup(label=size, size=size, value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry']) for size in pmui.CheckButtonGroup.param.size.objects)
)
```

### Disabled and Loading States

Like other widgets, the `CheckButtonGroup` can be disabled to prevent interaction and/or show a loading indicator:


```python
pmui.CheckButtonGroup(label='Disabled Group', disabled=True, loading=True, value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry'])
```

### Example: Interactive Pizza Order Form

Let's create a practical example showing how `CheckBoxGroup` can be used in a real application. This pizza ordering interface demonstrates real-time updates based on user selections:


```python
import panel as pn
import panel_material_ui as pmui

pn.extension()

toppings = pmui.CheckButtonGroup(
    label="Select your toppings:",
    options=['Pepperoni', 'Mushrooms', 'Bell Peppers', 'Onions', 'Olives', 'Extra Cheese'],
    value=['Pepperoni', 'Onions'],
    sizing_mode="stretch_width",
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
icon_checkbutton_group = pmui.CheckButtonGroup(
    label=":material/view_list: Views",
    value=["grid"],
    options={
        ":material/grid_view: Grid": "grid",
        ":material/table_rows: Table": "table",
        ":material/stacked_bar_chart: Chart": "chart",
    },
)

icon_checkbutton_group
```

### API Reference

#### Parameters


```python
pmui.CheckButtonGroup(label='Check Button Group', value=['Apple', 'Pear'], options=['Apple', 'Banana', 'Pear', 'Strawberry']).api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI ToggleButton:**

- [Material UI ToggleButton Reference](https://mui.com/material-ui/react-toggle-button/) - Complete documentation for the underlying Material UI component
- [Material UI ToggleButtonGroup API](https://mui.com/material-ui/api/toggle-button-group/) - Detailed API reference and configuration options
