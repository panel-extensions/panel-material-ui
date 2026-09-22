```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `FloatInput` widget allows selecting a floating point value using a spinbox. It behaves like a slider except that lower and upper bounds are optional and a specific value can be entered. Value can be changed using keyboard (up, down, page up, page down), mouse wheel and arrow buttons.

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html). Alternatively, learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (boolean): Whether the widget is editable
* **`end`** (float): Optional maximum allowable value
* **`start`** (float): Optional minimum allowable value
* **`step`** (float): The step added or subtracted to the current value on each click
* **`page_step_multiplier`** (int): Defines the multiplication factor applied to step when the page up and page down keys are pressed.
* **`value`** (float | None): The current value. Updates on `<enter>`, when the widget looses focus, or arrow icons or keyboard up arrow, down arrow, PgUp, or PgDown keys pressed. Can return None if all digits are deleted.
* **`value_throttled`** (float | None): Behaves identically to ``value`` for this widget, except is read only.

##### Display

* **`color`** (str): The color variant of the input, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`error_state`** (boolean): Whether to display in error state.
* **`helper_text`** (str): Helper text displayed below the input field.
* **`format`** (str): Optional format to convert the float value in string, see : http://numbrojs.com/old-format.html
* **`label`** (str): The title of the widget
* **`placeholder`** (str): A placeholder string displayed when no value is entered
* **`variant`** (`Literal["filled", "outlined", "standard"]`): The style variant to use.

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

##### Aliases

For compatibility with Panel certain parameters are allowed as aliases:

- **`name`**: Alias for `label`

___


```python
float_input = pmui.FloatInput(label='FloatInput', value=5., step=1e-1, start=0, end=1000)

float_input
```

``FloatInput.value`` returns a float value:


```python
float_input.value
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
icon_float_input = pmui.FloatInput(
    label=":material/zoom_out_map: Zoom level",
    value=1.5,
    step=0.1,
    start=0,
    end=10,
)

icon_float_input
```

### Helper Text

The `helper_text` parameter displays additional guidance text below the input field:


```python
pmui.FloatInput(label='Rate', value=0.0, step=0.1, helper_text='Value between 0 and 1')
```

### Controls

The `FloatInput` widget exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.Row(float_input.controls(jslink=True), float_input)
```
