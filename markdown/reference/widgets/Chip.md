```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Chip` component represents compact elements that display an input, attribute, or action. Chips allow users to enter information, make selections, filter content, or trigger actions. They support text, icons, and click events.

Chips are versatile components commonly used in:

- Tag systems and filters
- User input for categories
- Action buttons in compact spaces
- Selection indicators
- Multi-select interfaces

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`clicks`** (int): The number of times the chip has been clicked (read-only). Default is 0.
* **`disabled`** (boolean): Whether the Chip is disabled, making it opaque and disabling click events.
* **`label`** (str): The text content to display in the chip.

##### Display

* **`color`** (str): The color variant of the chip, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red) or a valid CSS color value.
* **`description`** (str): A description which is shown when the widget is hovered.
* **`icon`** (str): Name of the icon to display in the chip (appears before the label)
* **`size`** (str): Size of the chip - options include 'small' and 'medium' (default)
* **`variant`** (str): Visual style variant - either 'filled' (default) or 'outlined'

##### Styling

- **`sx`** (dict): Component level styling API for advanced customization
- **`theme_config`** (dict): Theming API for consistent design system integration

#### Constructor Arguments

* **`on_click`** (callable): A Python callback to be triggered when the chip is clicked
* **`js_on_click`** (str): JavaScript code to be triggered when the chip is clicked

#### Methods

* **`on_click`** (callable): Registers a Python callback to be executed when the chip is clicked
* **`js_on_click`** (callable): Allows defining JavaScript callbacks with `args` and `code` to be triggered when the chip is clicked

___

### Basic Usage

Create a simple `Chip` by providing a label:


```python
pmui.Chip(label="Hello")
```

The `Chip` also registers `clicks`:


```python
chip = pmui.Chip(label="Click me!")

pmui.Row(chip, pn.pane.Str(chip.param.clicks))
```

Click events can also be watched with `on_click`:


```python
clicks = pmui.Column()
click_chip = pmui.Chip(label="Click me!", on_click=clicks.append)

pmui.Row(click_chip, pn.pane.Str(click_chip.param.clicks))
```

### Icons

You may provide an `icon` either as a named icon from [Material Icon](https://fonts.google.com/icons?icon.set=Material+Icons):


```python
pmui.Row(
    pmui.Chip(label="Completed", icon="delete_icon", margin=10),
    pmui.Chip(label="Featured", icon="star_icon", margin=10),
)
```

or as an explicit SVG:


```python
search_icon = """
<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="currentColor"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
"""

pmui.Chip(label="Search", icon=search_icon, variant="outlined")
```

### Sizes

The `Chip` component supports different sizes to fit various layout requirements:


```python
pmui.Row(
    pmui.Chip(label="Small", size="small", margin=10),
    pmui.Chip(label="Medium", size="medium", margin=10),
)
```

### Variants

The `Chip` component offers different shape variants:

- **Filled**: Default style with color 
- **Outlined**: Sharp corners for a more geometric look


```python
pmui.Row(
    pmui.Chip(label="Filled", variant="filled", margin=10),
    pmui.Chip(label="Outlined", variant="outlined", margin=10),
)
```

### Colors

Customize the chip background colors for text and icon avatars to match your design system or indicate different user types:


```python
pmui.FlexBox(*(
    pmui.Chip(label=color, color=color, margin=10) for color in pmui.Chip.param.color.objects
))
```

### Loading

The `Chip` component can be displayed in loading states:


```python
pmui.Row(
    pmui.Chip(label="Disabled Chip", loading=True),
    pmui.Chip(label="Loading Chip", loading=True, color="primary"),
)
```


```python
pmui.Chip(label="Interactive Chip", icon="star", color="primary").api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using components
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Chip:**

- [Material UI Chip Reference](https://mui.com/material-ui/react-chip/) - Complete documentation for the underlying Material UI component
- [Material UI Chip API](https://mui.com/material-ui/api/chip/) - Detailed API reference and configuration options
