# Palette

The panel_material_ui palette system allows you to customize component colors to suit your brand. Colors are grouped into default categories (primary, secondary, error, warning, info, success) or custom categories that you define yourself.

## Color tokens

In `panel_material_ui`, each color typically has up to four tokens:

- **main**: The primary “shade” of the color
- **light**: A lighter variant of main
- **dark**: A darker variant of main
- **contrastText**: A color intended to contrast well against main (usually text)

For example, the default primary color might look like:

```python
primary = {
  'main': '#1976d2',
  'light': '#42a5f5',
  'dark': '#1565c0',
  'contrastText': '#fff',
}
```

To learn more about the theory behind these tokens, check out the [Material Design color system](https://m2.material.io/design/color/).

---

## Default colors

`panel_material_ui` provides nine default palette categories you can customize:

- default
- primary
- secondary
- error
- warning
- info
- success
- dark
- light

Each has the same four tokens (main, light, dark, contrastText). These defaults are enough for most apps, but you can add custom palette entries as needed.

## Customizing the default palette

You can override the defaults via the theme_config parameter that you pass to your panel_material_ui components:

```{pyodide}
from panel_material_ui import Button

my_theme = {
    "palette": {
        "primary": {
            "main": "#1976d2",
            "light": "#42a5f5",
            "dark": "#1565c0",
            "contrastText": "#fff",
        },
        "secondary": {
            "main": "#f44336",
        },
    }
}

Button(label="Custom Themed Button", theme_config=my_theme, button_type='primary')
```

## Summary

- **Default palette**: `default`, `primary`, `secondary`, `error`, `warning`, `info`, `success`, `light`, `dark`
- **Custom palette**: define your own named colors (e.g., ochre, violet)
- **Tokens**: `main`, `light`, `dark`, `contrastText` (and optionally more)
- **Automatic computations**: If you only specify main, panel_material_ui tries to infer `light`, `dark`, and `contrastText` using `contrastThreshold` and `tonalOffset`.
- **Accessibility**: Increase `contrastThreshold` if you need a higher text contrast ratio.
- **Dark mode: Supply a dark-themed `theme_config` or set `dark_mode=True` if your wrapper supports it.

With `panel_material_ui`, you have the full flexibility to define or override any palette color you need—at a component level using theme_config or globally across your entire application.
