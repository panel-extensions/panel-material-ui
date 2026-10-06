```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Checkbox` widget allows users to toggle between `True` and `False` states by checking or unchecking a familiar checkbox interface. This widget provides the same functionality as the `Toggle` and `Switch` widgets but with a traditional, universally recognized visual appearance.

Perfect for forms, settings, and multi-selection scenarios, the `Checkbox` widget offers the classic interaction pattern users expect. Its unique `indeterminate` state makes it especially useful for hierarchical selections and "select all" functionality.

#### Parameters

For more details on customization options, see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (bool): When True, the widget becomes non-interactive and appears grayed out.
* **`indeterminate`** (bool): Enables a third "undefined" state, perfect for representing partial selections in hierarchical data.
* **`value`** (bool): The current state of the checkbox (`True` for checked, `False` for unchecked, `None` for indeterminate when enabled).

##### Display

* **`label`** (str): The descriptive text displayed alongside the checkbox.

##### Styling

- **`color`** (str): The color theme applied to the checkbox when checked or in indeterminate state.
- **`size`** (str): Controls the physical size of the checkbox icon.
- **`sx`** (dict): Advanced styling options for fine-tuned appearance control.
- **`theme_config`** (dict): Theme-level configuration for consistent styling across your application.

##### Aliases

For seamless compatibility with Panel widgets, certain parameters accept aliases:

- **`name`**: Alternative parameter name for `label`

___

### Basic Usage

Getting started with the Checkbox widget is straightforward. Here's how to create a simple checkbox with a descriptive label:


```python
checkbox = pmui.Checkbox(label='Checkbox')

checkbox
```

The `value` parameter automatically updates to reflect the checkbox state: `True` when checked, `False` when unchecked. You can also programmatically set this value to control the checkbox state.


```python
checkbox.value
```

### Indeterminate State

The `indeterminate` option enables a powerful third state that's perfect for hierarchical selections and "select all" scenarios. When enabled, you can set the checkbox to an undefined state by setting the `value` to `None`:


```python
pmui.Checkbox(label='Checkbox', indeterminate=True, value=None)
```

### Color Options

Customize your checkbox's appearance to match your application's design language using the `color` parameter. Each color provides different visual emphasis and semantic meaning:


```python
pmui.FlexBox(
    *(pmui.Checkbox(value=True, label=color, color=color) for color in pmui.Checkbox.param.color.objects)
)
```

### Size Options

Choose the appropriate checkbox size for your interface using the `size` parameter. Different sizes work better in different contexts:


```python
pmui.FlexBox(
    *(pmui.Checkbox(label=size, size=size) for size in pmui.Checkbox.param.size.objects)
)
```

### Disabled and Loading States

The `Checkbox` widget supports both disabled and loading states to provide clear feedback during various application states. Use these features to guide user interactions effectively:


```python
pmui.Checkbox(label="Checkbox", disabled=True, loading=True)
```

### Real-World Example: Preference Selection

Let's create a practical example that demonstrates how checkboxes work in real applications. This preference selector shows how to bind checkbox values to dynamic content updates:


```python
import panel as pn
import panel_material_ui as pmui

pn.extension()

like_rock_roll = pmui.Checkbox(label="I like rock and roll", value=True)

def create_statement(value):
    if value:
        return "👍 Rock and roll is great!"
    
    return "👎 Rock and roll is not my thing."

statement=pn.bind(create_statement, like_rock_roll)

pmui.Column(like_rock_roll, statement)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
icon_checkbox = pmui.Checkbox(label=":material/verified: Accept terms", value=True)

icon_checkbox
```

### API Reference

#### Interactive Parameter Explorer

The `Checkbox` widget offers numerous customization options that can be modified from both Python and JavaScript. Explore these parameters interactively to see their effects in real-time:


```python
pmui.Checkbox(label="Checkbox").api(jslink=True)
```

### Further Learning

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Master the art of creating interactive applications with widgets and dynamic updates
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect widget parameters to create responsive, reactive user interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build sophisticated parameter-driven applications with minimal code

**Material UI Checkbox Documentation:**

- [Material UI Checkbox Reference](https://mui.com/material-ui/react-checkbox/) - Comprehensive documentation for the underlying Material UI component
- [Material UI Checkbox API](https://mui.com/material-ui/api/checkbox/) - Complete API reference with advanced configuration options and examples
