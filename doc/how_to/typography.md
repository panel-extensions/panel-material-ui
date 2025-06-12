# Typography

`panel_material_ui` provides a robust typography system inspired by Material UI. Fonts and sizes can be customized globally with a `theme_config`, or overridden at the component level.

## Font Family

To change the default font family across your entire app, specify it in `theme_config["typography"]["fontFamily"]`. For instance:

```{pyodide}
from panel_material_ui import Typography

my_theme = {
    "typography": {
        "fontFamily": (
            "-apple-system, "
            "BlinkMacSystemFont, "
            "\"Segoe UI\", "
            "Roboto, "
            "\"Helvetica Neue\", "
            "Arial, sans-serif, "
            "\"Apple Color Emoji\", "
            "\"Segoe UI Emoji\", "
            "\"Segoe UI Symbol\""
        )
    }
}

Typography(
    "Hello with a System Font!",
    theme_config=my_theme
).servable()
```

## Font size

Like Material UI, `panel-material-ui` uses `rem` units for font sizing. By default, browsers render `1rem = 16px`, but users may override this in their own browser settings. This approach improves accessibility, allowing your UI to scale gracefully if the user increases the default font size.

To change the base font size, set `theme_config["typography"]["fontSize"]`:

```{pyodide}
from panel_material_ui import Typography

my_theme = {
    "typography": {
        "fontSize": 12  # Default 14 in MUI
    }
}

Typography(
    "Smaller base font (12px -> 0.75rem).",
    theme_config=my_theme
).servable()
```

### Responsive font sizes

You can make your font sizes responsive by specifying breakpoints in your theme if you’d like more control, or simply adjust them via `sx` on individual components. For a single `Typography` component:

```{pyodide}
from panel_material_ui import Typography

Typography(
    "Responsive Typography",
    sx={
	"fontSize": "1.2rem",
        "@media (min-width: 600px)": {
            "fontSize": "1.5rem"
        },
        "@media (min-width: 900px)": {
            "fontSize": "2.4rem"
        }
    }
).servable()
```

If you want to systematically apply responsive font sizes across all headings or body text in your theme, you can define them in `theme_config["typography"]["h1"]`, `"h2"`, etc. using nested media queries.

### HTML font size

Some developers prefer to set the <html> font size to 10px (or 62.5%) for simpler rem arithmetic. In that case:

1. Adjust your global HTML styles (e.g., via a Panel template or CSS) to `html { font-size: 62.5%; }` which effectively makes `1rem = 10px`.

2. Let `panel-material-ui` know what the new root size is by setting `theme_config["typography"]["htmlFontSize"] = 10`.

:::{note}
Be mindful that changing the base font size can affect accessibility if a user is depending on the default 16px.
:::

## Variants

By default, panel-material-ui defines up to 13 text variants:

- `h1`, `h2`, `h3`, `h4`, `h5`, `h6`
- `subtitle1`, `subtitle2`
- `body1`, `body2`
- `button`
- `caption`
- `overline`

Each variant can be independently styled via `theme_config["typography"][<variant>]`:

```{pyodide}
from panel_material_ui import Typography

my_theme = {
    "typography": {
        "subtitle1": {"fontSize": 12},
        "body1": {"fontWeight": 500},
        "button": {"fontStyle": "italic"},
    }
}

Typography(
    "I'm a subtitle", theme_config=my_theme, variant="subtitle1"
).servable()
```

Then any `panel-material-ui` typography-based component referencing these variants will pick up your custom definitions.

### Adding & disabling variants

If you want to create entirely new variants (e.g., poster) or remove existing ones (e.g., h3), `panel-material-ui` allows you to do so by editing the typography dict:

```{pyodide}
from panel_material_ui import Typography

my_theme = {
    "typography": {
        # Custom 'poster' variant
        "poster": {
            "fontSize": "4rem",
            "color": "red"
        },
        # Disable h3
        "h3": None
    }
}

Typography(
    "I'm a subtitle", theme_config=my_theme, variant="poster"
).servable()
```

The disabled h3 variant simply reverts to default or becomes unavailable.

## Summary

- **Set global font family** in `theme_config["typography"]["fontFamily"]`.
- **Change base font size** with `theme_config["typography"]["fontSize"]` (default ~14px).
- **Use rem for accessibility**—respects user’s global font scaling.
- **Override variants individually** (h1, body2, button, etc.) in the typography section of `theme_config`.
- **Add or remove variants** for custom text styles (e.g. a giant “poster” style).
- **Use media queries** in the `theme_config` or the `sx` parameter for responsive scaling.
- **HTML root size** can be changed via CSS and `htmlFontSize` to keep rem arithmetic straightforward—but keep user accessibility in mind.

With these options, `panel-material-ui` offers a powerful and flexible typography system that stays consistent with Material Design principles while adapting neatly to Panel’s Pythonic ecosystem.
