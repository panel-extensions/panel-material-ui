```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Transition` wraps a child component with a transition effect that plays when the child enters or exits. It supports multiple animation variants including fade, grow, slide, zoom, and collapse.

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`active`** (bool): Whether the child is shown (with transition). Set to False to animate the child out, True to animate it in. Default is True.
* **`object`** (Viewable): The child component to wrap with the transition.

##### Display

* **`duration`** (int or None): The duration of the transition in milliseconds. When None, the duration is automatically calculated based on the element's size.
* **`orientation`** (str): The orientation of the collapse transition - either 'vertical' (default) or 'horizontal'. Only applies when variant is 'collapse'.
* **`placement`** (str): The direction the child slides in from - options are 'down', 'left' (default), 'right', and 'up'. Only applies when variant is 'slide'.
* **`variant`** (str): The type of transition animation to apply - options are 'collapse', 'fade' (default), 'grow', 'slide', and 'zoom'.

##### Styling

- **`sx`** (dict): Component level styling API for advanced customization
- **`theme_config`** (dict): Theming API for consistent design system integration

___

### Basic Usage

Wrap any component with a transition and toggle it with `active`:


```python
toggle = pmui.Switch(value=True, label="Show")

transition = pmui.Transition(
    pmui.Button(label="Hello", variant="contained", color="primary"),
    active=toggle,
    variant="fade",
)

pmui.Column(toggle, transition)
```

### Variants

The component supports several transition types:


```python
toggle = pmui.Switch(value=True, label="Show")

transitions = []
for variant in pmui.Transition.param.variant.objects:
    t = pmui.Transition(
        pmui.Chip(label=variant, color="primary"),
        active=toggle,
        variant=variant,
    )
    transitions.append(t)

pmui.Column(toggle, pmui.Row(*transitions))
```

### Slide Direction

When using the `slide` variant, control the direction with `placement`:


```python
toggle = pmui.Switch(value=True, label="Show")

slides = []
for direction in pmui.Transition.param.placement.objects:
    t = pmui.Transition(
        pmui.Chip(label=direction, color="secondary"),
        active=toggle,
        variant="slide",
        placement=direction,
    )
    slides.append(t)

pmui.Column(toggle, pmui.Row(*slides))
```

### Collapse Orientation

The `collapse` variant supports both vertical and horizontal orientation:


```python
toggle = pmui.Switch(value=True, label="Show")

vertical = pmui.Transition(
    pmui.Chip(label="Vertical", color="success"),
    active=toggle,
    variant="collapse",
    orientation="vertical",
)
horizontal = pmui.Transition(
    pmui.Chip(label="Horizontal", color="success"),
    active=toggle,
    variant="collapse",
    orientation="horizontal",
)

pmui.Column(toggle, pmui.Row(vertical, horizontal))
```

### Custom Duration

Control the speed of the animation with `duration` (in milliseconds):


```python
toggle = pmui.Switch(value=True, label="Show")

fast = pmui.Transition(
    pmui.Chip(label="Fast (200ms)", color="info"),
    active=toggle,
    variant="zoom",
    duration=200,
)
slow = pmui.Transition(
    pmui.Chip(label="Slow (2000ms)", color="warning"),
    active=toggle,
    variant="zoom",
    duration=2000,
)

pmui.Column(toggle, pmui.Row(fast, slow))
```
