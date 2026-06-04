```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Skeleton` wraps a child component and displays an animated placeholder in its place while loading. When `active` is True the child is shown; when False the skeleton placeholder is rendered.

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`active`** (bool): Whether to show the child content. When False the skeleton placeholder is rendered; when True the child is displayed normally. Default is False.
* **`object`** (Viewable): The child component to wrap with the skeleton.

##### Display

* **`animation`** (str or None): The animation effect for the skeleton - options are 'pulse' (default), 'wave', or None (disabled).
* **`variant`** (str): Shape variant of the skeleton placeholder - options are 'text', 'circular', 'rectangular', or 'rounded' (default).

##### Styling

- **`sx`** (dict): Component level styling API for advanced customization
- **`theme_config`** (dict): Theming API for consistent design system integration

___

### Basic Usage

Wrap a component and toggle `active` to reveal it once loaded:


```python
toggle = pmui.Switch(value=False, label="Loaded")

skeleton = pmui.Skeleton(
    pmui.Button(label="Click me", variant="contained", color="primary"),
    active=toggle,
    variant="rounded",
)

pmui.Column(toggle, skeleton)
```

### Variants

The skeleton supports different shape variants to match the content it's replacing:


```python
toggle = pmui.Switch(value=False, label="Loaded")

pmui.Column(
    toggle,
    pmui.Column(
        pmui.Skeleton(
            pmui.Chip(label="Text", color="primary"),
            active=toggle,
            variant="text",
        ),
        pmui.Skeleton(
            pmui.Chip(label="Rounded", color="primary"),
            active=toggle,
            variant="rounded",
        ),
        pmui.Skeleton(
            pmui.Chip(label="Rectangular", color="primary"),
            active=toggle,
            variant="rectangular",
        ),
    ),
)
```

### Animation

Choose between pulse (default), wave, or no animation:


```python
toggle = pmui.Switch(value=False, label="Loaded")

pmui.Column(
    toggle,
    pmui.Skeleton(
        pmui.Button(label="Pulse", variant="contained"),
        active=toggle,
        animation="pulse",
        variant="rounded",
    ),
    pmui.Skeleton(
        pmui.Button(label="Wave", variant="contained"),
        active=toggle,
        animation="wave",
        variant="rounded",
    ),
    pmui.Skeleton(
        pmui.Button(label="None", variant="contained"),
        active=toggle,
        animation=None,
        variant="rounded",
    ),
)
```

### Revealing Content

Set `active=True` to reveal the wrapped child:


```python
toggle = pmui.Switch(value=False, label="Loaded")

pmui.Column(
    toggle,
    pmui.Row(
        pmui.Skeleton(
            pmui.Chip(label="Loading", color="warning"),
            active=toggle,
            variant="rounded",
        ),
    ),
)
```


```python

```
