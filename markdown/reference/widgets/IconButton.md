```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `IconButton` widget allows triggering events when the button is clicked. In addition to a value parameter, which will button from `False` to `True` while the click event is being processed an additional `clicks` parameter that can be watched to subscribe to click events.

This widget displays a default `icon` initially. Upon being clicked, an `active_icon` appears for a specified `toggle_duration`.

For instance, the `ButtonIcon` can be effectively utilized to implement a feature akin to ChatGPT's copy-to-clipboard button.

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html). Alternatively, learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`active_icon`** (`str`): The name of the icon to display when toggled from [Material Icons](https://fonts.google.com/icons?icon.set=Material+Icons) or an SVG.
* **`clicks`** (`integer`): The number of times the icon was clicked.
* **`disabled`** (`bool`): Whether the widget is editable
* **`href`** (str): An optional link to navigate to when clicking the button.
* **`icon`** (`str`): The name of the icon to display from [Material Icons](https://fonts.google.com/icons?icon.set=Material+Icons) or an SVG.
* **`target`** (str): Where to open the `href` link. Default is `_self`, i.e. in the current window or tab.
* **`toggle_duration`** (`int`): The number of milliseconds the active_icon should be shown for and how long the button should be disabled for.
* **`value`** (`bool`): Toggles from False to True while the event is being processed.

##### Display

* **`description`** (`str | Bokeh Tooltip | pn.widgets.TooltipIcon`): A description which is shown when the widget is hovered.
* **`icon_size`** (`str`): Controls the size of the icon. Usually automatically determined based on the `size` but can be used to control icon size independently.
* **`label`** (`str`): The title of the widget
* **`size`** (`Literal["small", "medium", "large"]`): Controls the size of the widget.

##### Styling

* **`sx`** (dict): Component level styling API.
* **`theme_config`** (dict): Theming API.

##### Aliases

For compatibility with Panel certain parameters are allowed as aliases:

* **`name`**: Alias for `label`

___


```python
button = pmui.IconButton(icon="favorite", size="4em", description="favorite", color="danger")
button
```

You can also replace the `description` with `name` to have it shown on the side.


```python
button = pmui.IconButton(icon="favorite", size="4em", label="favorite")
button
```

The ``clicks`` parameter will report the number of times the button has been pressed:


```python
button.clicks
```

You can `bind` to the `Button` to trigger actions when the `Button` is clicked.


```python
indicator = pmui.LoadingSpinner(value=False, size=25)

def update_indicator(event):
    if not event:
        return
    indicator.value = not indicator.value

pn.bind(update_indicator, button, watch=True)

pmui.Column(button, indicator)
```

You can also `bind` to the `clicks` parameter


```python
def handle_click(clicks):
    return f'You have clicked me {clicks} times'

pmui.Column(
    button,
    pn.bind(handle_click, button.param.clicks),
)
```

Alternatively you can use the ``on_click`` method to trigger a function when the button is clicked:


```python
text = pmui.TextInput(value='Ready')

def b(event):
    text.value = 'Clicked {0} times'.format(button.clicks)
    
button.on_click(b)
pmui.Row(button, text)
```

By default, when `value` is `True`, the `active_icon` (`heart-filled`) is the filled version of the `icon` (`heart`).

If you'd like this to be changed, manually set the `active_icon`.

The icon will automatically adapt to the specified `width`/`height` but you may also provide an explicit `size`:


```python
pmui.IconButton(icon="content_paste", active_icon="check", size="4em")
```

The `toggle_duration`, in milliseconds, will determine how long the `active_icon` should be shown for and how long the button should be `disabled` for.


```python
pmui.IconButton(icon="content_paste", active_icon="check", toggle_duration=2500, size="4em")
```

You can also use SVGs for icons.


```python
SVG = """
<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-ad-off" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 5h10a2 2 0 0 1 2 2v10m-2 2h-14a2 2 0 0 1 -2 -2v-10a2 2 0 0 1 2 -2" /><path d="M7 15v-4a2 2 0 0 1 2 -2m2 2v4" /><path d="M7 13h4" /><path d="M17 9v4" /><path d="M16.115 12.131c.33 .149 .595 .412 .747 .74" /><path d="M3 3l18 18" /></svg>
"""
ACTIVE_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-ad-filled" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M19 4h-14a3 3 0 0 0 -3 3v10a3 3 0 0 0 3 3h14a3 3 0 0 0 3 -3v-10a3 3 0 0 0 -3 -3zm-10 4a3 3 0 0 1 2.995 2.824l.005 .176v4a1 1 0 0 1 -1.993 .117l-.007 -.117v-1h-2v1a1 1 0 0 1 -1.993 .117l-.007 -.117v-4a3 3 0 0 1 3 -3zm0 2a1 1 0 0 0 -.993 .883l-.007 .117v1h2v-1a1 1 0 0 0 -1 -1zm8 -2a1 1 0 0 1 .993 .883l.007 .117v6a1 1 0 0 1 -.883 .993l-.117 .007h-1.5a2.5 2.5 0 1 1 .326 -4.979l.174 .029v-2.05a1 1 0 0 1 .883 -.993l.117 -.007zm-1.41 5.008l-.09 -.008a.5 .5 0 0 0 -.09 .992l.09 .008h.5v-.5l-.008 -.09a.5 .5 0 0 0 -.318 -.379l-.084 -.023z" stroke-width="0" fill="currentColor" /></svg>
"""

pmui.IconButton(icon=SVG, active_icon=ACTIVE_SVG, size='4em')
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
pmui.IconButton(label="Zoom :material/zoom_out_map:", icon="zoom_out_map")
```

### Controls

The `ButtonIcon` widget exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.Row(button.controls(jslink=True), button)
```
