```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `StaticText` widget displays a labeled text value that cannot be edited. It lines up with the other Material inputs, which makes it useful for read-only fields in forms and Param generated UIs.

Discover more about interactive widgets in the [Panel interactivity guides](https://panel.holoviz.org/how_to/interactivity/index.html), or learn about [callbacks and links](https://panel.holoviz.org/how_to/links/index.html) and [declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters

For customization options, see the [Panel Material UI customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (`bool`): Whether the text is rendered in the disabled color.
* **`value`** (`object`): The value to display. Strings are rendered as HTML, any other value is converted to a string and escaped.

##### Display

* **`description`** (`str`): A description shown as a tooltip next to the label.
* **`label`** (`str`): The label displayed above the value.

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

##### Aliases

For compatibility with Panel certain parameters are allowed as aliases:

- **`name`**: Alias for `label`

___

### Basic Usage

Display a value with a label:


```python
static_text = pmui.StaticText(label='Model', value='gpt-4o-mini')
static_text
```

Updating the `value` updates the displayed text:


```python
static_text.value = 'claude-sonnet'
```

### HTML and Other Values

String values may contain HTML markup, while other values are escaped before they are displayed:


```python
pmui.Column(
    pmui.StaticText(label='Status', value='<b>Running</b> since 10:15'),
    pmui.StaticText(label='Retries', value=3),
    pmui.StaticText(label='Raw markup', value=['<b>escaped</b>']),
)
```

### Read-Only Parameters

Map a parameter to `StaticText` to display it read-only in a Param generated UI:


```python
import param

class Run(param.Parameterized):

    run_id = param.String(default='a1b2c3', constant=True)

    epochs = param.Integer(default=10, bounds=(1, 100))

pmui.Paper(pn.Param(Run(), widgets={'run_id': pmui.StaticText}))
```

## API Reference

Show all parameters and their current values:


```python
pmui.StaticText(label='StaticText', value='Some text').api(jslink=True)
```

### References

**Panel Documentation:**

- [Panel StaticText Reference](https://panel.holoviz.org/reference/widgets/StaticText.html)
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html)

**Material UI:**

- [Material UI Typography Reference](https://mui.com/material-ui/react-typography/)
