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
* **`end`** (int): Optional maximum allowable value
* **`start`** (int): Optional minimum allowable value
* **`step`** (int): The step added or subtracted to the current value on each click
* **`page_step_multiplier`** (int): Defines the multiplication factor applied to step when the page up and page down keys are pressed.
* **`value`** (float | None): The current value. Updates on `<enter>`, when the widget looses focus, or arrow icons or keyboard up arrow, down arrow, PgUp, or PgDown keys pressed. Can return None if all digits are deleted.
* **`value_throttled`** (float | None): Behaves identically to ``value`` for this widget, except is read only.

##### Display

* **`error_state`** (boolean): Whether to display in error state.
* **`format`** (str): Optional format to convert the float value in string, see : http://numbrojs.com/old-format.html
* **`helper_text`** (str): Helper text displayed below the input field.
* **`label`** (str): The title of the widget
* **`placeholder`** (str): A placeholder string displayed when no value is entered

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

##### Aliases

For compatibility with Panel certain parameters are allowed as aliases:

- **`name`**: Alias for `label`

___


```python
int_input = pmui.IntInput(label='IntInput', value=5, step=2, start=0, end=1000)

int_input
```

``IntInput.value`` returns an integer value:


```python
int_input.value
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
pmui.IntInput(label="Zoom :material/zoom_out_map:", value=3)
```

### Helper Text

The `helper_text` parameter displays additional guidance text below the input field:


```python
pmui.IntInput(label='Count', value=0, helper_text='Enter a positive integer')
```

### Controls

The `IntInput` widget exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.Row(int_input.controls(jslink=True), int_input)
```
