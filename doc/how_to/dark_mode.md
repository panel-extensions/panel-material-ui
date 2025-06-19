# Dark Mode

The `panel-material-ui` components automatically integrate with Panel’s dark mode configuration and allow you to force dark mode by setting `dark_theme=True` at the component level or in your Panel extension.

## Dark mode only (no system preference)

If you want your application to always use dark mode, you can use `dark_mode=True` on each component:

```{pyodide}
from panel_material_ui import Button

Button(
    label="Dark Button", dark_theme=True
).servable()
```

or set it globally:

```python
pn.extension(theme='dark')
```

## Managed theme

By default each component will control its own theme, however if you want to manage dark mode globally you have two options:

1. Use the `Page` component, which will automatically include a theme toggle and manage the theme for you.

```{pyodide}
from panel_material_ui import Page, Button

Page(
    dark_theme=True,
    main=[
        Button(
            label="Dark Button"
        )
    ],
    title="Dark Mode Demo",
).preview()
```

2. Embed the `ThemeToggle` component, which will ensure the theme is managed globally and let you switch between light and dark mode.

```{pyodide}
from panel_material_ui import Button, Row, ThemeToggle

Row(Button(name="Hello"), ThemeToggle()).preview()
```

## Overriding dark palette

When `dark_mode=True`, your components automatically swap to a dark palette. To customize that palette further—for instance, to change the primary color—you can use `theme_config`, just like you would for other color overrides:

```{pyodide}
from panel_material_ui import Button

dark_theme_config = {
    "dark": {
        "palette": {
            "primary": {
                "main": "#450c0c"
            }
        }
    },
    "light": {
        "palette": {
            "primary": {
                "main": "#eb5252"
            }
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
