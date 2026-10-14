```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Alert` component displays a short, important message that attracts the user's attention without interrupting their workflow. Use it for warnings, errors, success confirmations, or informational updates. The `object` text supports Markdown formatting.

## Parameters

### Core

* **`object`** (`str`): The text content to display in the alert body (supports Markdown).
* **`title`** (`str`): An optional bold title displayed above the body text.
* **`severity`** (`Literal["error", "warning", "info", "success"]`): The severity level, which determines the icon and default color.
* **`closed`** (`boolean`): Whether the alert is currently closed (hidden).
* **`closeable`** (`boolean`): Whether to show a close button that lets users dismiss the alert.

### Style

* **`variant`** (`Literal["filled", "outlined"]`): The visual style of the alert.
* **`sx`** (`dict`): Component-level styling API for advanced customization.
* **`theme_config`** (`dict`): Theming API for consistent design system integration.

---

### Basic Usage

Create a simple alert with a title and body text:


```python
alert = pmui.Alert(title="Note", object="This is an informational alert.", severity="info")
alert
```

### Severity Levels

The `severity` parameter controls the color scheme and icon. There are four built-in levels:


```python
pmui.FlexBox(
    pmui.Alert(title="Success", object="The operation completed successfully.", severity="success", margin=5),
    pmui.Alert(title="Info", object="Here is some useful information.", severity="info", margin=5),
    pmui.Alert(title="Warning", object="Be careful with this action.", severity="warning", margin=5),
    pmui.Alert(title="Error", object="Something went wrong.", severity="error", margin=5),
)
```

### Variants

The `variant` parameter controls the visual style. The default is `"outlined"`, which shows a border. Use `"filled"` for a more prominent, solid background:


```python
pmui.FlexBox(
    pmui.Alert(
        title="Outlined", object="This is the default outlined variant.",
        severity="info", variant="outlined", margin=5
    ),
    pmui.Alert(
        title="Filled", object="This is the filled variant.",
        severity="info", variant="filled", margin=5
    ),
)
```

The filled variant works well with all severity levels:


```python
pmui.FlexBox(
    pmui.Alert(title="Success", object="Operation completed.", severity="success", variant="filled", margin=5),
    pmui.Alert(title="Info", object="Something to know.", severity="info", variant="filled", margin=5),
    pmui.Alert(title="Warning", object="Proceed with caution.", severity="warning", variant="filled", margin=5),
    pmui.Alert(title="Error", object="An error occurred.", severity="error", variant="filled", margin=5),
)
```

### Markdown Support

The `object` text is rendered as Markdown, so you can use bold, italic, links, and other formatting:


```python
pmui.Alert(
    title="Formatting Example",
    object="This alert has **bold text**, *italic text*, and a [link](https://panel.holoviz.org).",
    severity="info",
)
```

### Closeable Alerts

Set `closeable=True` to display a close button. When the user clicks it, the alert collapses with a smooth animation and the `closed` parameter becomes `True`:


```python
closeable_alert = pmui.Alert(
    title="Dismissable",
    object="Click the X to close this alert.",
    severity="warning",
    closeable=True,
)
closeable_alert
```

You can programmatically reopen a closed alert by setting `closed = False`:


```python
closeable_alert.closed = False
```

### Alert with Child Objects

Since `Alert` is a layout component, it can contain other Panel objects as children in addition to the `object` text:


```python
pmui.Alert(
    pmui.Typography("Check the **documentation** for more details."),
    title="Tip",
    severity="info",
    variant="outlined",
)
```

### Controlling Visibility

The `closed` parameter can be used to show or hide the alert dynamically. Here we wire a button to toggle the alert:


```python
toggle_button = pmui.Toggle(label="Show Alert")

toggle_alert = pmui.Alert(
    title="Toggle Me",
    object="This alert can be shown and hidden with a button.",
    severity="success",
    closed=toggle_button,
)

pmui.Column(toggle_button, toggle_alert)
```

### API Reference

#### Parameters


```python
pmui.Alert(title="API Example", object="Explore the parameters below.", severity="info").api(jslink=True)
```
