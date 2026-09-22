```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

Floating Action Buttons or `Fab`s for short allow users to take actions, and make choices, with a single click or tap. In contrast to the `Button` the `Fab` is designed performs the primary, or most common, action on a screen.

In addition to a `value` parameter, which will toggle from `False` to `True` while the click event is being processed, an additional `clicks` parameter is available, that can be watched to subscribe to click events.

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
* **`disabled`** (boolean): Whether the widget is editable.
* **`href`** (str): The link to navigate to when clicking the button.
* **`value`** (boolean): Toggles from `False` to `True` while the event is being processed.

##### Display

* **`color`** (str): The color variant of the button, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`description`** (str | Bokeh Tooltip | pn.widgets.TooltipIcon): A description which is shown when the widget is hovered.
* **`icon`** (str): An icon to render to the left of the button label. Either an SVG or an icon name which is loaded from [Material UI Icons](https://mui.com/material-ui/material-icons).
* **`icon_size`** (str): Size of the icon as a string, e.g. 12px or 1em.
* **`label`** (str): The title of the widget.
* **`variant`** (str): The button style, either 'circular' or 'extended'.

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

##### Aliases

For compatibility with Panel certain parameters are allowed as aliases:

- **`button_style`**: Alias for `variant`
- **`button_type`**: Alias for `color`
- **`name`**: Alias for `label`

#### Methods

- **`on_click`**: Registers a callback to be executed when the `Fab` is clicked.
- **`js_on_click`**: Allows registering a Javascript callback to be executed when the `Fab` is clicked.
- **`jscallback`**: Allows registering a Javascript callback to be executed when a property changes on the `Fab`.

##### Callback Arguments

- **`on_click`** (callable): A function taking an `event` argument. Executed when the `Fab` is clicked.
- **`js_on_click`** (str): A string containing the Javascript code. Executed run when the `Fab` is clicked.

___

### Basic Usage

The `Fab` button is designed as way to invoke the most common action in the app:


```python
fab = pmui.Fab(color='primary', label='Click me')

fab
```

The `clicks` parameter will report the number of times the button has been pressed:


```python
fab.clicks
```

While the `value` parameter toggles to `True` while the click event is processed:


```python
fab.value
```

### Link Button

A `Fab` can also have an `href` parameter which will cause it to navigate to the provided link on click:


```python
pmui.Fab(href="https://panel.holoviz.org", label="Open Panel docs")
```

You may additionally specify where to open the link via the `target` parameter:


```python
pmui.Fab(href="https://panel.holoviz.org", label="Open Panel docs in new window or tab", target="_blank")
```

### Handling Clicks

You can `bind` to the `Fab` to trigger actions when the `Fab` is clicked.


```python
toggle_button = pmui.Fab(label="Start Spinning")
indicator = pmui.LoadingSpinner(value=False, size=25)

def update_indicator(event):
    indicator.value = not indicator.value
    toggle_button.label="Stop Spinning" if indicator.value else "Start Spinning"

pn.bind(update_indicator, toggle_button, watch=True)

pmui.Row(toggle_button, indicator)
```

Alternatively you can use the ``on_click`` method to trigger a function when the button is clicked:


```python
click_button = pmui.Fab(label="Increment", align="center")
text = pmui.TextInput(value='Clicked 0 times', disabled=True)

def handle_click(event):
    text.value = 'Clicked {0} times'.format(click_button.clicks)

click_button.on_click(handle_click)
    
pmui.Row(click_button, text)
```

### Disabled and Loading

Like any other widget the `Button` can be `disabled` and / or set to `loading`:


```python
pmui.Fab(label="Loading", disabled=True, loading=True, color="primary")
```

### Positioning

A floating action button generally should use 'fixed', 'absolute' or 'sticky' positioning. To achieve this you can set the `styles` attribute:


```python
position = {
    "position": "absolute",
    "bottom": "0",
}

pmui.Column(
    pmui.Fab(color='default', styles=dict(position='absolute')),
    pmui.Fab(color='primary', styles=dict(position='absolute', right="0")),
    pmui.Fab(color='secondary', styles=dict(position="absolute", bottom="0")),
    pmui.Fab(color='error', styles=dict(position="absolute", bottom="0", right="0")),
    height=200, sizing_mode='stretch_width'
).show()
```

To position it on a scrollable container use `'sticky'`:


```python
sticky_fab = pmui.Fab(color='primary', styles={'position': 'sticky', 'left': '100%', 'bottom': '12px'})

pn.Column(
    *range(100),
    sticky_fab,
    scroll='y',
    width=200,
    height=300
)
```

and to absolutely position it on the page use `'fixed'`.

### Color and Variant

The color of the button can be set by selecting one of the available `color` values and the `variant` can be `'circular'` or `'extended'`:


```python
pmui.Row(
    *(pmui.Column(*(pmui.Fab(label=f'{color=}, {variant=}', color=color, variant=variant)
                  for color in pmui.Fab.param.color.objects))
    for variant in pmui.Fab.param.variant.objects)
)
```

### Icons

By default the circular variant will pnly display an `icon`, which can be defined as an icon loaded from [Material Icons](https://fonts.google.com/icons?icon.set=Material+Icons):


```python
pmui.Row(
    pmui.Fab(icon='warning', color='warning', label='WARNING'),
    pmui.Fab(icon='bug_report', color='error', label='ERROR')
)
```

or as an explicit SVG:


```python
cash_icon = """
<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-cash" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="white" fill="none" stroke-linecap="round" stroke-linejoin="round">
  <path stroke="none" d="M0 0h24v24H0z" fill="none"/>
  <path d="M7 9m0 2a2 2 0 0 1 2 -2h10a2 2 0 0 1 2 2v6a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2z" />
  <path d="M14 14m-2 0a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" />
  <path d="M17 9v-2a2 2 0 0 0 -2 -2h-10a2 2 0 0 0 -2 2v6a2 2 0 0 0 2 2h2" />
</svg>
"""

pmui.Fab(icon=cash_icon, color='success', label='Checkout', icon_size='2em', variant='extended')
```

You can also provide an end icon:


```python
pmui.Fab(label="Send", end_icon="send_icon")
```

### Example: Random Quotes


```python
import panel as pn
import panel_material_ui as pmui
import time
import random

pn.extension()

submit = pmui.Fab(label="Update Quote", variant="extended", color="primary", size="small", icon="refresh",)

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

pmui.Fab(label="Show Quote", color="primary", size="small", icon="refresh", js_on_click=javascript_code)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
icon_fab = pmui.Fab(label=":material/add: Create", color="primary")

icon_fab
```

### API Reference

#### Parameters


```python
pmui.Fab(label="Click Me").api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Fab:**

- [Material UI Fab Reference](https://mui.com/material-ui/react-fab/) - Complete documentation for the underlying Material UI component
- [Material UI Fab API](https://mui.com/material-ui/api/fab/) - Detailed API reference and configuration options
