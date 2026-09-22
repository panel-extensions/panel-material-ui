```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `DiscretePlayer` widget provides media-player like controls to step through a list or dictionary of discrete options. It is built on the [Material UI Slider](https://mui.com/material-ui/react-slider/), [IconButton](https://mui.com/material-ui/react-button/#icon-button) and [ToggleButtonGroup](https://mui.com/material-ui/react-toggle-button/) components.

The speed at which the widget plays is defined by the `interval` (in milliseconds) and it is possible to advance more than one option per update using the `step` parameter. The animation itself runs in the browser, so a `DiscretePlayer` keeps working in a static HTML export.

It falls into the broad category of single-value, option-selection widgets that provide a compatible API and include the [`DiscreteSlider`](DiscreteSlider.ipynb), [`Select`](Select.ipynb) and [`Player`](Player.ipynb) widgets.

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html). Alternatively, learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`direction`** (`int`): The current play direction: `-1` plays in reverse, `0` is paused and `1` plays forward.
* **`disabled`** (`boolean`): Whether the widget is editable.
* **`interval`** (`int`): The interval between updates in milliseconds. Default is 500, i.e. two updates per second.
* **`loop_policy`** (`Literal["once", "loop", "reflect"]`): What to do when the player reaches the last frame. `'once'` stops, `'loop'` wraps around and `'reflect'` reverses the direction.
* **`step`** (`int`): The number of frames to advance on each update or button press.
* **`options`** (`list | dict`): A list or dictionary of options to step through.
* **`value`** (`object`): The currently selected option value. Updated on every frame while playing and while the slider is dragged.
* **`value_throttled`** (`object`): The currently selected option value. Updated on every frame while playing but only once the slider handle is released.

##### Display

* **`color`** (`str`): The color of the slider and of the active transport button.
* **`label`** (`str`): The title of the widget.
* **`preview_duration`** (`int`): How long (in milliseconds) the slower/faster buttons display the resulting frame rate before reverting to their icon.
* **`scale_buttons`** (`float`): A scaling factor applied to the transport buttons.
* **`show_loop_controls`** (`boolean`): Whether the loop policy controls are shown.
* **`show_value`** (`boolean`): Whether to display the current value.
* **`size`** (`Literal["small", "medium", "large"]`): The size of the slider and the transport buttons.
* **`value_align`** (`Literal["start", "center", "end"]`): The alignment of the label and value row.
* **`variant`** (`Literal["full", "minimal"]`): Whether to render the stacked `'full'` player or the single-row `'minimal'` player.
* **`visible_buttons`** (`list[str]`): The transport buttons to display. One or more of `'slower'`, `'first'`, `'previous'`, `'reverse'`, `'pause'`, `'play'`, `'next'`, `'last'` and `'faster'`.
* **`visible_loop_options`** (`list[str]`): The loop policies to offer.

##### Styling

- **`sx`** (`dict`): Component level styling API.
- **`theme_config`** (`dict`): Theming API.

##### Aliases

For compatibility with Panel certain parameters are allowed as aliases:

- **`name`**: Alias for `label`

___

### Basic Usage

The `DiscretePlayer` steps through the `options`.


```python
player = pmui.DiscretePlayer(label='Value', options=[2, 4, 8, 16, 32, 64, 128], value=32)

player
```

Like most other widgets, `DiscretePlayer` has a `value` parameter that can be accessed or set:


```python
player.value
```

The `options` parameter also accepts a dictionary, whose keys become the labels shown next to the widget label while the `value` reflects the corresponding dictionary value:


```python
value_player = pmui.DiscretePlayer(label='Size', options={'Small': 10, 'Medium': 20, 'Large': 30})

value_player
```


```python
value_player.value
```

### Variants

The `variant` parameter controls the layout. The default `'full'` player stacks the label, the slider, the transport buttons and the loop controls, while the `'minimal'` player collapses everything into a single row consisting of a play/pause toggle, the slider and (if `show_value`) the value. Use it when the player has to fit into a toolbar or sit directly below a plot.


```python
pmui.Column(
    pmui.DiscretePlayer(label='Full', options=['A', 'B', 'C', 'D']),
    pmui.DiscretePlayer(label='Minimal', options=['A', 'B', 'C', 'D'], variant='minimal'),
)
```

### Loop Policy

The `loop_policy` determines what happens when the player reaches the last option. `'once'` stops, `'loop'` wraps back to the first option and `'reflect'` reverses the direction. The policy can also be changed from the toggle group below the buttons, which can be restricted with `visible_loop_options` or hidden entirely with `show_loop_controls=False`.


```python
pmui.Column(
    pmui.DiscretePlayer(label='Once', options=['A', 'B', 'C', 'D'], loop_policy='once'),
    pmui.DiscretePlayer(label='Loop', options=['A', 'B', 'C', 'D'], loop_policy='loop'),
    pmui.DiscretePlayer(label='Reflect', options=['A', 'B', 'C', 'D'], loop_policy='reflect'),
)
```

### Controlling Playback from Python

The `play`, `pause` and `reverse` methods (and the `direction` parameter they set) drive the player from Python:


```python
controlled = pmui.DiscretePlayer(label='Value', options=list('ABCDEFGH'), interval=300)

pmui.Column(
    controlled,
    pmui.Row(
        pmui.Button(label='Play', on_click=lambda _: controlled.play()),
        pmui.Button(label='Pause', on_click=lambda _: controlled.pause()),
        pmui.Button(label='Reverse', on_click=lambda _: controlled.reverse()),
    )
)
```

### Visible Buttons

Use `visible_buttons` to render a subset of the nine transport buttons.


```python
pmui.DiscretePlayer(label='Value', options=['A', 'B', 'C', 'D'], visible_buttons=['previous', 'play', 'pause', 'next'], show_loop_controls=False)
```

### Show Value

Unlike the `Player` the `DiscretePlayer` displays the current option label by default. Set `show_value=False` to hide it, and use `value_align` to control its placement.


```python
pmui.Column(
    pmui.DiscretePlayer(label='Hidden', options=['A', 'B', 'C', 'D'], show_value=False),
    pmui.DiscretePlayer(label='Centered', options=['A', 'B', 'C', 'D'], value_align='center'),
)
```

### Color

You can specify a `color`, which is applied to the slider and to the button matching the current `direction`.


```python
pmui.DiscretePlayer(label='Value', options=['A', 'B', 'C', 'D'], color='secondary')
```

### Sizes

Use `size` to scale the slider and the buttons and `scale_buttons` to scale the buttons on their own.


```python
pmui.Column(
    pmui.DiscretePlayer(label='Small', options=['A', 'B', 'C', 'D'], size='small'),
    pmui.DiscretePlayer(label='Medium', options=['A', 'B', 'C', 'D'], size='medium'),
    pmui.DiscretePlayer(label='Scaled buttons', options=['A', 'B', 'C', 'D'], scale_buttons=1.5),
)
```

### Disabled

The widget can be disabled with `disabled=True`, which also stops playback.


```python
pmui.DiscretePlayer(label='Value', options=['A', 'B', 'C', 'D'], disabled=True)
```

### API Reference

#### Basic Usage


```python
pmui.DiscretePlayer(label='Value', options=['A', 'B', 'C', 'D']).api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Slider:**

- [Material UI Slider Reference](https://mui.com/material-ui/react-slider/) - Complete documentation for the underlying Material UI component
- [Material UI Slider API](https://mui.com/material-ui/api/slider/) - Detailed API reference and configuration options
