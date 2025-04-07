# Dark Mode

Your Mui-for-Panel components automatically integrate with Panel’s dark mode. Simply set `dark_mode=True` at the component level or in your Panel extension to force dark mode.

## Dark mode only (no system preference)

If you want your application to always use dark mode, you can use `dark_mode=True` on each component:

```{pyodide}
from panel_material_ui import Button

Button(
    label="Dark Button", dark_mode=True)
).servable()
```

or set it globally:

```python
pn.extension(theme='dark')
```

## Overriding dark palette

When `dark_mode=True`, your components automatically swap to a dark palette. To customize that palette further—for instance, to change the primary color—you can use `theme_config`, just like you would for other color overrides:

```{pyodide}
from panel_material_ui import Button

dark_theme_config = {
    "palette": {
        "mode": "dark",
        "primary": {
            "main": "#ff5252"
        }
    }
}

Button(
    label="Custom Dark",
    dark_theme=True,
    button_type="primary",
    theme_config=dark_theme_config
).servable()
```

## Toggling

When using the `Page` component a theme toggle is automatically included.
