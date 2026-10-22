```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `TextAreaInput` allows entering any multiline string using a text input box. Lines are joined with the newline character ``\n``. Unfortunately in the notebook, enter keys may not be intercepted correctly (see [ipywidgets](https://github.com/jupyter-widgets/ipywidgets/issues/3950)).

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html). Alternatively, learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`disabled`** (boolean, default=False): Whether the widget is editable
* **`enter_pressed`** (event): An event that triggers when `<shift>+<enter>` is pressed.
* **`value`** (str): The current value updated when pressing `<shift>+<enter>` or when the widget loses focus because the user clicks away or presses the tab key.
* **`value_input`** (str): The current value updated on every key press.

##### Display

* **`auto_grow`** (boolean, default=False): Whether the TextArea should automatically grow in height to fit the content.
* **`color`** (str): The color variant of the input, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`cols`** (int, default=2): The number of columns in the text input field. 
* **`error_state`** (boolean): Whether to display in error state.
* **`helper_text`** (str): Helper text displayed below the input field.
* **`label`** (str): The title of the widget
* **`max_length`** (int, default=5000): Max character length of the input field. Defaults to 5000
* **`max_rows`** (int, default=None): The maximum number of rows in the text input field when `auto_grow=True`. 
* **`placeholder`** (str): A placeholder string displayed when no value is entered
* **`rows`** (int, default=2): The number of rows in the text input field. 
* **`resizable`** (boolean | str, default='both'): Whether the layout is interactively resizable, and if so in which dimensions: `width`, `height`, or `both`.
* **`variant`** (`Literal["filled", "outlined", "standard"]`): The variant of the input field.

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
text_area_input = pmui.TextAreaInput(label='Text Area Input', placeholder='Enter a string here...')
text_area_input
```

``TextAreaInput.value`` returns a string type that can be read out and set like other widgets. Note that ``value`` is updated when pressing `<shift>+<enter>` or when the widget loses focus. To get the current value after every keystroke, use ``value_input`` instead:


```python
text_area_input.value
```

An auto-growing `TextAreaInput` will grow (and shrink) in height to accommodate the entered text. Setting `rows` together with `auto_grow` will set a lower bound on the number of rows and setting `max_rows` will provide an upper bound:


```python
pmui.TextAreaInput(label='Growing TextArea', auto_grow=True, max_rows=10, rows=6, value="""\
This text area will grow when newlines are added to the text:

1. Foo
2. Bar
3. Baz
""", width=500)
```

If you only want the text area to be resizable in the vertical direction, you can set the resizeable parameter to 'height':


```python
pmui.TextAreaInput(label="Vertical Adjustable TextArea", resizable="height")
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
pmui.TextAreaInput(
    label=":material/zoom_out_map: Notes",
    placeholder="Add details...",
    rows=3,
)
```

### Helper Text

The `helper_text` parameter displays additional guidance text below the input field:


```python
pmui.TextAreaInput(label='Bio', helper_text='Tell us about yourself')
```

### Controls

The `TextAreaInput` widget exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.Row(text_area_input.controls(jslink=True), text_area_input)
```
