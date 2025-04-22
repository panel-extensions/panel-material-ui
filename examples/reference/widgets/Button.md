```python
import panel as pn
import panel_material_ui as pmu

pn.extension()
```

## Button Intro

Buttons allow users to take actions, and make choices, with a single tap.

Buttons communicate actions that users can take. They are typically placed throughout your UI, in places like

- Modal windows
- Forms
- Cards
- Toolbars

Then `panel-material-ui` button is built on top of the [Material UI `Button`](https://mui.com/material-ui/react-button/).

```python
import panel as pn
import panel_material_ui as pmu
from panel_material_ui import Button

pn.extension()
```

## Basic Button

The Button comes with three *variants*: text (default), contained, and outlined.

```python
pn.Row(
    Button(label="Text", variant="text"),
    Button(label="Contained", variant="contained"),
    Button(label="Outlined", variant="outlined"),
).servable()
```

## Text Button

[Text buttons](https://m2.material.io/components/buttons#text-button) are typically used for less-pronounced actions, including those located: in dialogs, in cards. In cards, text buttons help maintain an emphasis on card content.

```python
pn.Row(
    Button(label="Primary"),
    Button(label="Disabled", disabled=True),
    Button(label="Link", href="#text-buttons"),
).servable()
```

## Contained button

[Contained buttons](https://m2.material.io/components/buttons#contained-button) are high-emphasis, distinguished by their use of elevation and fill. They contain actions that are primary to your app.

```python
pn.Row(
    Button(label="Contained", variant="contained"),
    Button(label="Disabled", variant="contained", disabled=True),
    Button(label="Link", variant="contained", href="#contained-buttons"),
).servable()
```

You can remove the elevation with the `disable_elevation` parameter.

```python
Button(label="Disable elevation", variant="contained", disable_elevation=True).servable()
```

## Outlined Button

[Outlined buttons](https://m2.material.io/components/buttons#outlined-button) are medium-emphasis buttons. They contain actions that are important but aren't the primary action in an app.

Outlined buttons are also a lower emphasis alternative to contained buttons, or a higher emphasis alternative to text buttons.

```python
pn.Row(
    Button(label="Primary", variant="outlined"),
    Button(label="Disabled", variant="outlined", disabled=True),
    Button(label="Link", variant="outlined", href="#outlined-buttons"),
).servable()
```

**MORE TO COME. NOT FINISHED**

## Aliases

For backwards compatibility with Panel certain parameters are allowed as aliases:

- **`button_style`**: Alias for `variant`
- **`button_type`**: Alias for `color`
- **`name`**: Alias for `label`

```python
Button(name="Alias", button_style="outlined", button_type="success").servable()
```

## API

### Parameters

```python
button = Button(label="Click Me")

pn.Tabs(
    pn.pane.HTML(button.param, name="Table"),
    pn.Row(button.controls(jslink=True), button, name="Live Editor")
).servable()
```

## References

See also

- Material UI `Button` [Reference](https://mui.com/material-ui/react-button/) and [API](https://mui.com/material-ui/api/button/) documentation.
