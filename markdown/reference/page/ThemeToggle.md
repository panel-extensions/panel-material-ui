```python
import panel as pn
import panel_material_ui as pmui
from panel_material_ui import ThemeToggle

pn.extension()
```

The `ThemeToggle` provides a toggle to switch between light and dark themes. When added to an application the theme will be managed globally. This means that toggling will switch between the default light theme and the dark theme for all other components on the page.

## Parameters:

##### Core

* **`theme`** (`Literal["dark", "default"]`): The currently selected theme.
* **`value`** (`boolean`): Reflects the current `theme` (True if 'dark', False if 'default').

##### Display

* **`color`** (`Literal["primary", "secondary"]`): The color variant of the theme toggle.
* **`variant`** (`Literal["icon", "switch"]`): The display variant of the toggle.

---

The `ThemeToggle` can be added to an application like any other component and will globally take control over the theme:


```python
toggle = ThemeToggle()

pmui.Row(
    "# My App",
    toggle
).preview(height=100, width=200)
```

The current theme value is available via the `theme` and `value` parameters, where `theme` toggles between "dark" and "default" while the `value` reflects whether dark mode is enabled:


```python
toggle.value, toggle.theme
```

By default the application will use the `"icon"` variant but you can be toggled to use a `"switch"` variant instead:


```python
switch = ThemeToggle(variant='switch')

pmui.Row(
    "# My App",
    switch
).preview(height=100, width=320)
```
