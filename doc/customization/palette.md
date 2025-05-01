# Palette

The `panel-material-ui` palette system allows you to customize component colors to suit your brand. Colors are grouped into default categories (primary, secondary, error, warning, info, success) or custom categories that you define yourself.

## Color tokens

In `panel-material-ui`, each color typically has up to four tokens:

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

`panel-material-ui` provides nine default palette categories you can customize:

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

You can override the defaults via the `theme_config` parameter that you pass to your panel-material-ui components:

```{pyodide}
from panel_material_ui import Button

my_theme = {
    "palette": {
        "primary": {
            "main": "#ff69b4", # Changed to pink
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

### Providing colors directly

You don’t need to use a predefined palette. For each palette entry (e.g., primary), you can specify `main` (required), and optionally `light`, `dark`, and `contrastText`:

```{pyodide}
my_theme = {
    "palette": {
        "primary": {
            "main": "#ff69b4", # Changed to pink
            # light, dark, and contrastText can be automatically computed
        },
        "secondary": {
            "main": "#E0C2FF",
            "light": "#F5EBFF",   # optional
            "dark": "#BA99D5",    # optional
            "contrastText": "#47008F",  # optional
        }
    }
}
Button(label="Custom Themed Button", theme_config=my_theme, button_type='primary')
```

### Contrast threshold


When `panel_material_ui` automatically picks contrastText for a color (if you don’t specify it), it uses a `contrastThreshold` value. By default, it’s 3 (a 3:1 contrast), but you can increase it for improved accessibility:

```python
my_theme = {
    "palette": {
        "primary": {
            "main": "#3f50b5",
        },
        "contrastThreshold": 4.5  # Increase for higher contrast
    }
}
```

This helps ensure a better color contrast ratio for text displayed over the `primary.main` color.

### Tonal offset

Similarly, panel_material_ui calculates the `light` and `dark` tokens by shifting the luminance of `main`. The `tonalOffset` defaults to 0.2, but you can override it at the top level of your palette:

```python
my_theme = {
    "palette": {
        "tonalOffset": 0.25,
        "primary": {
            "main": "#FF5733",
        },
    }
}
```

This means `light` becomes lighter and `dark` becomes darker relative to `main`.

### Accessibility

For color contrast, the recommendation is a minimum ratio of 4.5:1 for body text (per [WCAG 2.1 Rule 1.4.3](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)). If you’re relying on `panel_material_ui` to auto-compute `contrastText`, be sure to increase `contrastThreshold` to 4.5:

```python
my_theme = {
    "palette": {
        "contrastThreshold": 4.5,
        "primary": {"main": "#3f50b5"},
    }
}
```

However, you should still verify that the chosen foreground and background colors yield the contrast you want, especially if you’re targeting stricter guidelines.

## Dark mode

For more guidance on setting up dark mode, including toggling, see our [Dark mode guide](./dark_mode). Typically, in `panel_material_ui`, you either set `dark_mode=True` on individual components or at the `Page` level.

## Summary

- **Default palette**: `default`, `primary`, `secondary`, `error`, `warning`, `info`, `success`, `light`, `dark`
- **Custom palette**: define your own named colors (e.g., ochre, violet)
- **Tokens**: `main`, `light`, `dark`, `contrastText` (and optionally more)
- **Automatic computations**: If you only specify main, panel-material-ui tries to infer `light`, `dark`, and `contrastText` using `contrastThreshold` and `tonalOffset`.
- **Accessibility**: Increase `contrastThreshold` if you need a higher text contrast ratio.
- **Dark mode: Supply a dark-themed `theme_config` or set `dark_mode=True` if your wrapper supports it.

With `panel-material-ui`, you have the full flexibility to define or override any palette color you need—at a component level using theme_config or globally across your entire application.
