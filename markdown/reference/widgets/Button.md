```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

Buttons allow users to take actions, and make choices, with a single click or tap. In addition to a `value` parameter, which will toggle from `False` to `True` while the click event is being processed, an additional `clicks` parameter is available, that can be watched to subscribe to click events.

Buttons communicate actions that users can take. They are typically placed throughout your UI, in places like

- Modal windows
- Forms
- Cards
- Toolbars

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html). Alternatively, learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`clicks`** (int): Number of clicks (can be listened to)
* **`disabled`** (boolean): Whether the button is clickable.
* **`href`** (str): An optional link to navigate to when clicking the button.
* **`target`** (str): Where to open the `href` link. Default is `_self`, i.e. in the current window or tab.
* **`value`** (boolean): Toggles from `False` to `True` while the event is being processed.

##### Display

* **`color`** (str): The color variant of the button, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`disable_elevation`** (boolean): Whether to apply elevation to the `Button` to visually separate it from the background.
* **`description`** (str | Bokeh Tooltip | pn.widgets.TooltipIcon): A description which is shown when the widget is hovered.
* **`end_icon`** (str): An icon to render to the right of the button label. Either an SVG or an icon name which is loaded from [Material UI Icons](https://mui.com/material-ui/material-icons).
* **`icon`** (str): An icon to render to the left of the button label. Either an SVG or an icon name which is loaded from [Material UI Icons](https://mui.com/material-ui/material-icons).
* **`icon_size`** (str): Size of the icon as a string, e.g. 12px or 1em.
* **`label`** (str): The title of the widget.
* **`size`** (`Literal["small", "medium", "large"]`): Controls the size of the widget.
* **`variant`** (str): The button style, either 'contained', 'outlined', or 'text'.

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

##### Aliases

For compatibility with Panel, certain parameters are allowed as aliases:

- **`button_style`**: Alias for `variant`
- **`button_type`**: Alias for `color`
- **`name`**: Alias for `label`

#### Methods

- **`on_click`**: Registers a callback to be executed when the `Button` is clicked.
- **`js_on_click`**: Allows registering a Javascript callback to be executed when the `Button` is clicked.
- **`jscallback`**: Allows registering a Javascript callback to be executed when a property changes on the `Button`.

##### Callback Arguments

- **`on_click`** (callable): A function taking an `event` argument. Executed when the `Button` is clicked.
- **`js_on_click`** (str): A string containing the Javascript code. Executed run when the `Button` is clicked.

___

### Basic Usage

The Button comes with three *variants*: text (default), contained, and outlined.


```python
pmui.Row(
    pmui.Button(label="Text", variant="text"),
    pmui.Button(label="Contained", variant="contained"),
    pmui.Button(label="Outlined", variant="outlined"),
)
```

### Text Button

[Text buttons](https://m2.material.io/components/buttons#text-button) are typically used for less-pronounced actions, including those located in dialogs, and in cards. In cards, text buttons help maintain an emphasis on card content.


```python
pmui.Row(
    pmui.Button(label="Primary"),
    pmui.Button(label="Disabled", disabled=True),
    pmui.Button(label="Link", href="#text-button"),
)
```

### Contained button

[Contained buttons](https://m2.material.io/components/buttons#contained-button) are high-emphasis, distinguished by their use of elevation and fill. They contain actions that are primary to your app.


```python
pmui.Row(
    pmui.Button(label="Contained", variant="contained"),
    pmui.Button(label="Disabled", variant="contained", disabled=True),
    pmui.Button(label="Link", variant="contained", href="#contained-buttons"),
)
```

### Outlined Button

[Outlined buttons](https://m2.material.io/components/buttons#outlined-button) are medium-emphasis buttons. They contain actions that are important but aren't the primary action in an app.

Outlined buttons are also a lower emphasis alternative to contained buttons, or a higher emphasis alternative to text buttons.


```python
pmui.Row(
    pmui.Button(label="Primary", variant="outlined"),
    pmui.Button(label="Disabled", variant="outlined", disabled=True),
    pmui.Button(label="Link", variant="outlined", href="#outlined-buttons"),
)
```

### Link Button

A `Button` can also have an `href` parameter which will cause it to navigate to the provided link on click:


```python
pmui.Button(href="https://panel.holoviz.org", label="Open Panel docs")
```

You may additionally specify where to open the link via the `target` parameter:


```python
pmui.Button(href="https://panel.holoviz.org", label="Open Panel docs in new window or tab", target="_blank")
```

### Handling Clicks

You can `bind` to the `Button` to trigger actions when the `Button` is clicked.


```python
toggle_button = pmui.Button(label="Start Spinning", variant="contained")
indicator = pmui.LoadingSpinner(value=False, size=25)

def update_indicator(event):
    indicator.value = not indicator.value
    toggle_button.label="Stop Spinning" if indicator.value else "Start Spinning"

pn.bind(update_indicator, toggle_button, watch=True)

pmui.Row(toggle_button, indicator)
```

Alternatively you can use the ``on_click`` method to trigger a function when the button is clicked:


```python
click_button = pmui.Button(label="Increment", align="center")
text = pmui.TextInput(value='Clicked 0 times', disabled=True)

def handle_click(event):
    text.value = 'Clicked {0} times'.format(click_button.clicks)

click_button.on_click(handle_click)
    
pmui.Row(click_button, text)
```

### Disabled and Loading

Like any other widget the `Button` can be `disabled` and / or set to `loading`:


```python
pmui.Button(label="Loading", disabled=True, loading=True, color="primary")
```

### Color

The color of the button can be set by selecting one of the available `color` values.


```python
pmui.Row(
    pmui.Button(color="secondary", label="Secondary"),
    pmui.Button(color="success", variant="contained", label="Success"),
    pmui.Button(color="error", variant="outlined", label="Error"),
)
```

### Sizes

For larger or smaller buttons, use the `size` parameter.


```python
pmui.Column(
    pmui.Row(
        pmui.Button(size="small", label="Small", align="center"), 
        pmui.Button(size="medium", label="Medium", align="center"),
        pmui.Button(size="large", label="Large", align="center"),
    ),
    pmui.Row(
        pmui.Button(size="small", label="Small", variant="outlined", align="center"), 
        pmui.Button(size="medium", label="Medium", variant="outlined", align="center"),
        pmui.Button(size="large", label="Large", variant="outlined", align="center"),
    ),
    pmui.Row(
        pmui.Button(size="small", label="Small", variant="contained", align="center"), 
        pmui.Button(size="medium", label="Medium", variant="contained", align="center"),
        pmui.Button(size="large", label="Large", variant="contained", align="center"),
    )
)
```

Please note that, contrast to Material UI you have to `align` a pmui button `center` if you so wish.

### Buttons with Icons and Label

Sometimes you might want to have icons for certain buttons to enhance the UX of the application, as we recognize logo's more easily than plain text. For example, if you have a delete button you can label it with a dustbin icon.

You may provide an icon either as a named icon from [Material Icon](https://fonts.google.com/icons?icon.set=Material+Icons)


```python
pmui.Row(
    pmui.Button(label="Delete", variant="outlined", icon="delete_icon"),
    pmui.Button(label="Send", variant="contained", icon="send_icon"),
)
```

or as an explicit SVG:


```python
search_icon = """
<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="currentColor"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
"""

pmui.Row(
  pmui.Button(icon=search_icon, icon_size='1em', label='Search', variant="outlined"),
  pmui.Button(icon=search_icon, icon_size='2em', label='Search', variant="contained"),
)
```

You can also provide an end icon:


```python
pmui.Button(label="Send", variant="contained", end_icon="send_icon")
```

Alternatively you may use *html codes* and *emojis* in your `label`.


```python
pmui.Row(
    pmui.Button(label='\u25c0', variant="outlined", width=50),
    pmui.Button(label='\u25b6', variant="outlined", width=50),
    pmui.Button(label='🔍', variant="outlined", width=100),
    pmui.Button(label="💾 Save", variant="outlined", width=100),
    pmui.Button(label="Copy ✂️", variant="outlined", width=100),
)
```

### Icon Button

See [`ButtonIcon`](IconButton.ipynb)

### Aliases

For backwards compatibility with Panel, certain parameters are allowed as aliases:

- **`button_style`**: Alias for `variant`
- **`button_type`**: Alias for `color`
- **`name`**: Alias for `label`


```python
pmui.Button(name="Alias", button_style="outlined", button_type="success")
```

### Example: Random Quotes


```python
import panel as pn
import panel_material_ui as pmui
import time
import random

pn.extension()

submit = pmui.Button(label="Update Quote", variant="contained", color="primary", size="small", icon="refresh",)

motivational_quotes = [
    "🚀 The best time to plant a tree was 20 years ago. The second best time is now!",
    "💪 Success is not final, failure is not fatal: it is the courage to continue that counts.",
    "🌟 The only way to do great work is to love what you do.",
    "⚡ Innovation distinguishes between a leader and a follower.",
    "🎯 The future belongs to those who believe in the beauty of their dreams.",
    "🔥 Don't watch the clock; do what it does. Keep going!",
    "✨ Your limitation—it's only your imagination.",
]

def pick_quote(value):
    yield "Loading Quote..."
    time.sleep(0.5)
    yield random.choice(motivational_quotes)

quote = pn.bind(pick_quote, submit)

pmui.Column(quote, submit)
```

### Example: Random Quotes (Javascript)

When you click the button an alert will open and display a quote:


```python
import panel as pn
import panel_material_ui as pmui

pn.extension()

javascript_code = """
const quotes = [
    "🚀 The best time to plant a tree was 20 years ago. The second best time is now!",
    "💪 Success is not final, failure is not fatal: it is the courage to continue that counts.",
    "🌟 The only way to do great work is to love what you do.",
    "⚡ Innovation distinguishes between a leader and a follower.",
    "🎯 The future belongs to those who believe in the beauty of their dreams.",
    "🔥 Don't watch the clock; do what it does. Keep going!",
    "✨ Your limitation—it's only your imagination."
];
const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
alert(randomQuote);
"""

pmui.Button(label="Show Quote", variant="contained", color="primary", size="small", icon="refresh", js_on_click=javascript_code)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
pmui.Button(
    label=":material/zoom_out_map: Expand",
    variant="contained",
    color="primary",
)
```

### API Reference

#### Parameters


```python
pmui.Button(label="Click Me").api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Button:**

- [Material UI Button Reference](https://mui.com/material-ui/react-button/) - Complete documentation for the underlying Material UI component
- [Material UI Button API](https://mui.com/material-ui/api/button/) - Detailed API reference and configuration options
