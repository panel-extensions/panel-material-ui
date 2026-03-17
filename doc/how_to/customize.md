# Customize Themes & Styles

Customization of Panel Mui components inherits all the benefits of having a consistent design language that Mui provides. Styling can be applied using the `sx` parameter, while theming is achieved through the inheritable `theme_config`. Let us walk through these two different approaches through a series of examples.

This how-to guide was adapted from the [Mui How to Customize](https://mui.com/material-ui/customization/how-to-customize/) guide.

## Styling Layers Overview

Panel provides multiple tools for styling, each suited to different needs:

| Tool | Purpose | Scope |
|---|--|---|
| `sx` | Style component internals (one-off tweaks, experiments) | Local to one instance |
| `theme_config` | Define app-wide palette, typography, and defaults | Global (flows to all children) |
| `styles` | Style the outer container box (spacing, borders, backgrounds) | Local to one instance |
| `stylesheets` | Style widget internals via CSS selectors | Local to one instance |

**Quick mental model:** Start with `sx` for local customizations, use `theme_config` for consistency, use `styles` for container wrapping, and `stylesheets` only for classic Panel internals.

---

## One-off Customizations with `sx`

To change the styles of a single `panel-material-ui` component instance, use the `sx` parameter. This is ideal for quick, local customizations like tweaking padding, changing colors, or adding hover effects.

### The `sx` Parameter

All `panel-material-ui` components accept an `sx` parameter that allows you to pass in style overrides.

```{pyodide}
from panel_material_ui import Button

Button(
    label="Click Me!",
    sx={
        "color": "white",
        "backgroundColor": "black",
        "&:hover": {
            "backgroundColor": "gray",
        }
    }
).servable()
```

#### Dark and Light Mode Selectors

If you need to apply styling only in dark or light mode, use the `.mui-dark` or `.mui-light` class:

```{pyodide}
from panel_material_ui import Button, Row, ThemeToggle

Row(
    Button(
        label="Click Me!",
        sx={
            "color": "white",
            "backgroundColor": "black",
            "&:hover": {
                "backgroundColor": "pink",
            },
            "&.mui-dark:hover": {
                "backgroundColor": "orange",
            }
        }
    ),
    ThemeToggle(),
).preview()
```

#### Targeting Nested Component Parts

Sometimes you need to style a nested part of a component—for instance, the thumb of a slider or the label of a checkbox. Use the `&` selector to target nested Material UI class names:

```{pyodide}
from panel_material_ui import FloatSlider

FloatSlider(
    sx={
        "& .MuiSlider-thumb": {
            "borderRadius": 0  # square instead of round
        }
    }
).servable()
```

You can also combine nested selectors with dark/light mode:

```{pyodide}
from panel_material_ui import FloatSlider, ThemeToggle, Row

Row(
    FloatSlider(
        sx={
            "& .MuiSlider-thumb": {
                "borderRadius": 0,
                "backgroundColor": "white",
            },
            "&.mui-dark .MuiSlider-thumb": {
                "backgroundColor": "black",
            }
        }
    ),
    ThemeToggle(),
).preview()
```

:::{note}
Note: Even though Panel Mui components reuse Material UI’s internal class names, these names are subject to change. Make sure to k
eep an eye on release notes if you override nested classes.
:::

Learn more about the [`sx` parameter in the Mui docs](https://mui.com/system/getting-started/the-sx-prop/).

---

## Global Theming with `theme_config`

For app-wide consistency, use `theme_config` to define defaults (colors, typography, shape) that flow down to all child components. This is the most maintainable approach for larger apps.

### Basic Theme Configuration

Define a theme at the parent level and all children inherit it:

```{pyodide}
from panel_material_ui import Button

theme_config = {
    "palette": {
        "primary": {"main": "#d219c9"},
        "secondary": {"main": "#dc004e"},
    }
}

Button(
    label="Themed Button", theme_config=theme_config, button_type="primary"
).servable()
```

### Mode-Specific Themes

Provide distinct theme configs for dark and light modes using `"light"` and `"dark"` keys:

```{pyodide}
from panel_material_ui import Button, Row, ThemeToggle

theme_config = {
    "light": {
        "palette": {
            "primary": {"main": "#d219c9"},
            "secondary": {"main": "#dc004e"},
        }
    },
    "dark": {
        "palette": {
            "primary": {"main": "#dc004e"},
            "secondary": {"main": "#d219c9"},
        }
    }
}

Row(
    Button(
        label="Global Button", theme_config=theme_config, button_type="primary"
    ),
    ThemeToggle(),
).preview()
```

### Theme Inheritance

The most powerful feature is that child components automatically inherit the parent's theme. This allows you to style your entire app from one top-level configuration:

```{pyodide}
from panel_material_ui import Card, Button

Card(
    Button(label="Child Button", button_type="primary"),  # Inherits parent's theme
    title="Parent Card",
    theme_config={
        "palette": {
            "primary": {"main": "#d219c9"},
        }
    }
).servable()
```

Here, the child `Button` automatically inherits the parent's primary color. We recommend styling your top-level container (e.g., `Page`, `Container`, or `Row`) so the theme cascades throughout your app.

### Comparison: `sx` vs `theme_config`

Both approaches can achieve the same visual result, but serve different purposes:

**Using `sx` (local):**
```{pyodide}
from panel_material_ui import Button

Button(
    label="Local Style",
    sx={"backgroundColor": "#d219c9", "color": "white"}
).servable()
```

**Using `theme_config` (global):**
```{pyodide}
from panel_material_ui import Button, Row

theme = {
    "palette": {
        "primary": {"main": "#d219c9"},
    }
}

Row(
    Button(label="Global Style", button_type="primary"),
    theme_config=theme,
).servable()
```

**When to choose:**
- Use `sx` for one-off exceptions or quick experiments
- Use `theme_config` when you want consistency across many components or the entire app
- Combine both: set global defaults with `theme_config`, then use `sx` for local overrides

---

## Container Styling with `styles`

The `styles` parameter styles the **outer container** of any Panel component—perfect for spacing, borders, backgrounds, and shadows around the component itself (not its internals).

```{pyodide}
from panel_material_ui import Button, Row

container_style = {
    "background": "#f8fafc",
    "border": "1px solid #dce3eb",
    "border-radius": "10px",
    "padding": "12px",
    "box-shadow": "0 2px 8px rgba(0,0,0,0.08)",
}

Row(
    Button(label="Button in styled container", button_type="primary", styles=container_style),
).preview()
```

### Difference Between `sx` and `styles`

- **`sx`**: Styles the **component internals** (text, background inside the Button, Slider handle, etc.)
- **`styles`**: Styles the **outer container box** (wraps around the component)

Example showing the difference:

```{pyodide}
from panel_material_ui import Button, Row

# styles: changes the wrapper box around the button
container_style = {
    "background": "#e3f2fd",
    "border": "2px solid #1976d2",
    "border-radius": "8px",
    "padding": "16px",
}

# sx: changes the button itself
button_sx = {
    "backgroundColor": "#ff6b6b",
    "color": "white",
    "&:hover": {"backgroundColor": "#ff5252"}
}

Row(
    Button(
        label="Styled Button",
        sx=button_sx,
        styles=container_style
    ),
).preview()
```

---

## Putting It All Together

A real app typically combines multiple approaches:

```{pyodide}
import panel as pn
import panel_material_ui as pmui

pn.extension()

# Global theme applied at the top level
app_theme = {
    "light": {
        "palette": {
            "primary": {"main": "#6a1b9a"},
            "secondary": {"main": "#1565c0"},
        },
        "shape": {"borderRadius": 12},
    },
    "dark": {
        "palette": {
            "primary": {"main": "#9575cd"},
            "secondary": {"main": "#64b5f6"},
        },
        "shape": {"borderRadius": 12},
    },
}

# Local container styling
card_container = {
    "padding": "8px",
    "background": "rgba(0,0,0,0.02)",
}

# Local component styling
button_sx = {
    "fontWeight": 700,
    "&:hover": {"transform": "scale(1.02)"}
}

pmui.Row(
    pmui.Card(
        pmui.Button(
            label="Submit",
            button_type="primary",
            sx=button_sx,  # Local exception
        ),
        title="Form",
        styles=card_container,  # Container styling
    ),
    pmui.ThemeToggle(),
    theme_config=app_theme,  # Global theme
).preview(height=300)
```
