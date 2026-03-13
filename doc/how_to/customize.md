# Customize Themes & Styles

Customization of Panel Mui components inherits all the benefits of having a consistent design
language that Mui provides. Styling can be applied using the `sx` parameter, while theming is
achieved through the inheritable `theme_config`. Let us walk through these approaches through a
series of examples.

This how-to guide was adapted from the [Mui How to Customize](https://mui.com/material-ui/customization/how-to-customize/) guide.

## Choosing the right styling tool

Panel apps can mix classic `pn.widgets.*` components and `panel-material-ui` components. Each
type has its own styling surface:

| Tool | Applies to | What it styles |
|---|---|---|
| `styles` | Any Panel component | The outer container box (spacing, border, background) |
| `stylesheets` | Classic Panel widgets only | Internals via CSS selectors (e.g. `.noUi-handle`) |
| `sx` | `panel-material-ui` only | Internals via MUI class selectors (e.g. `& .MuiSlider-thumb`) |
| `theme_config` | `panel-material-ui` (inherited) | App-wide palette, typography, shape, component defaults |

**One rule to remember:** `styles` is *outside*, `stylesheets`/`sx` are *inside*,
`theme_config` is *everywhere*.

Start with `theme_config` for app-wide consistency, add `sx` for local exceptions on
`panel-material-ui` components, and reach for `styles`/`stylesheets` for classic Panel widgets.

---

## Styling

### `stylesheets`

When you need to reach inside a classic `pn.widgets.*` component — the slider track, handle, or
label — use `stylesheets`. You write plain CSS targeting the widget's internal class names, scoped
to `:host`.

```{pyodide}
import panel as pn

pn.extension()

slider_css = """
:host {
  --slider-size: 6px;
  --handle-width: 18px;
  --handle-height: 18px;
}

.noUi-handle {
  border-radius: 50%;
  box-shadow: none;
  border: 2px solid #0b6bcb;
  background: white;
}

.noUi-connect {
  background: #0b6bcb;
}
"""

pn.widgets.FloatSlider(
    name="Satisfaction",
    start=0, end=10, value=7,
    stylesheets=[slider_css],
)
```

### Migrating to `sx`

If you are switching a styled classic widget to its `panel-material-ui` equivalent, the styling
moves from CSS class names (noUiSlider) to MUI class names, and from kebab-case CSS to camelCase
JavaScript properties in `sx`. The visual result is identical.

```{pyodide}
import panel_material_ui as pmui

pmui.FloatSlider(
    label="Satisfaction",
    start=0, end=10, value=7,
    sx={
        "& .MuiSlider-track": {
            "height": "6px",
            "backgroundColor": "#0b6bcb",
        },
        "& .MuiSlider-rail": {
            "height": "6px",
        },
        "& .MuiSlider-thumb": {
            "width": "18px",
            "height": "18px",
            "borderRadius": "50%",
            "backgroundColor": "white",
            "border": "2px solid #0b6bcb",
            "boxShadow": "none",
        },
    },
    margin=(10, 20),
    sizing_mode="stretch_width",
)
```

The selector mapping between the two systems:

| Classic `stylesheets` target | `sx` equivalent |
|---|---|
| `.noUi-connect` | `& .MuiSlider-track` |
| `.noUi-handle` | `& .MuiSlider-thumb` |
| `--slider-size` (track height CSS var) | `& .MuiSlider-track: { "height": "6px" }` |
| `--handle-width` / `--handle-height` | `& .MuiSlider-thumb: { "width", "height" }` |

### One-off `sx`

All `panel-material-ui` components accept an `sx` parameter for quick, local customizations —
tweaking the padding of one button or giving a single card a different background color.

```{pyodide}
from panel_material_ui import Button

Button(
    label="Click Me!",
    sx={
        "color": "white",
        "backgroundColor": "black",
        "&:hover": {"backgroundColor": "gray"},
    }
).servable()
```

To apply styling only in dark or light mode, prefix selectors with `.mui-dark` or `.mui-light`:

```{pyodide}
from panel_material_ui import Button, Row, ThemeToggle

Row(
    Button(
        label="Click Me!",
        sx={
            "color": "white",
            "backgroundColor": "black",
            "&:hover": {"backgroundColor": "pink"},
            "&.mui-dark:hover": {"backgroundColor": "orange"},
        }
    ),
    ThemeToggle(),
).preview()
```

Learn more about the [`sx` parameter in the Mui docs](https://mui.com/system/getting-started/the-sx-prop/).

### Nested styles

To target a nested part of a component — the thumb of a slider, the label of a checkbox — use
MUI's internal class names as selectors in `sx`. For example, to make a slider thumb square:

```{pyodide}
from panel_material_ui import FloatSlider

FloatSlider(
    sx={"& .MuiSlider-thumb": {"borderRadius": 0}}
).servable()
```

Prefix with `&.mui-dark` or `&.mui-light` to scope overrides to a specific mode.

:::{note}
`panel-material-ui` components reuse Material UI's internal class names, which are subject to
change. Keep an eye on release notes if you override nested classes.
:::

---

## Theming

### Colors and palette

Each palette entry has up to four tokens: **main** (required), **light**, **dark**, and
**contrastText** — the latter three are auto-computed from `main` if omitted.

`panel-material-ui` provides nine built-in palette categories: `default`, `primary`, `secondary`,
`error`, `warning`, `info`, `success`, `dark`, and `light`. Override any of them via
`theme_config["palette"]`:

```{pyodide}
from panel_material_ui import Button, Row

my_theme = {
    "palette": {
        "primary": {
            "light": "#757ce8",
            "main": "#3f50b5",
            "dark": "#002884",
            "contrastText": "#fff",
        },
        "secondary": {"main": "#f44336"},
    }
}

Row(
    Button(label="Primary", theme_config=my_theme, button_type="primary"),
    Button(label="Secondary", theme_config=my_theme, button_type="secondary"),
).servable()
```

The Material Design team provides a [color tool](https://m2.material.io/inline-tools/color/) for
selecting accessible color pairs and generating palette suggestions. Community tools like
[mui-theme-creator](https://zenoo.github.io/mui-theme-creator/) let you preview components under
different palettes interactively.

According to [WCAG 2.1 Rule 1.4.3](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html),
text should have at least a 4.5:1 contrast ratio. Increase `contrastThreshold` for AA compliance,
and use `tonalOffset` to control how far `light`/`dark` tokens deviate from `main`:

```python
my_theme = {
    "palette": {
        "primary": {"main": "#3f50b5"},
        "contrastThreshold": 4.5,
        "tonalOffset": 0.25,
    }
}
```

### Dark mode

Components automatically integrate with Panel's theme configuration. Force dark mode on a single
component with `dark_theme=True`, or globally with `pn.extension(theme='dark')`.

For a managed toggle, embed `ThemeToggle` or use the `Page` component:

```{pyodide}
from panel_material_ui import Button, Row, ThemeToggle

Row(Button(label="Hello"), ThemeToggle()).preview()
```

To customise each mode's palette independently, supply `"light"` and `"dark"` keys in
`theme_config`:

```{pyodide}
from panel_material_ui import Button

theme_config = {
    "light": {"palette": {"primary": {"main": "#eb5252"}}},
    "dark":  {"palette": {"primary": {"main": "#450c0c"}}},
}

Button(label="Mode-aware", button_type="primary", theme_config=theme_config).servable()
```

### Typography

Set the font family, base font size, and per-variant styles globally via
`theme_config["typography"]`:

```{pyodide}
from panel_material_ui import Typography

my_theme = {
    "typography": {
        "fontFamily": "Georgia, serif",
        "fontSize": 14,
        "h1": {"fontWeight": 700},
        "button": {"textTransform": "none", "fontWeight": 600},
    }
}

Typography("Hello with custom typography!", theme_config=my_theme).servable()
```

Font sizes use `rem` units so they scale with the user's browser default — important for
accessibility. For responsive sizing on a single component, use `sx` with media queries:

```{pyodide}
from panel_material_ui import Typography

Typography(
    "Responsive text",
    sx={
        "fontSize": "1.2rem",
        "@media (min-width: 600px)": {"fontSize": "1.5rem"},
        "@media (min-width: 900px)": {"fontSize": "2.4rem"},
    }
).servable()
```

`panel-material-ui` exposes 13 built-in variants (`h1`–`h6`, `subtitle1`, `subtitle2`, `body1`,
`body2`, `button`, `caption`, `overline`). You can override any of them or define new ones:

```{pyodide}
from panel_material_ui import Typography

my_theme = {
    "typography": {
        "poster": {"fontSize": "4rem", "color": "red"},
        "h3": None,  # disable
    }
}

Typography("Giant poster text", theme_config=my_theme, variant="poster").servable()
```

### Component overrides

Use the `components` key in `theme_config` to change default props or globally override the CSS
of any MUI component:

```{pyodide}
from panel_material_ui import Button

custom_theme = {
    "components": {
        "MuiButton": {
            "defaultProps": {"disableRipple": True},
            "styleOverrides": {"root": {"fontSize": "1rem"}},
        }
    }
}

Button(label="No ripple, bigger text", theme_config=custom_theme).servable()
```

You can also apply conditional styles based on a component's `variant` or `color` prop:

```{pyodide}
from panel_material_ui import Card

custom_theme = {
    "components": {
        "MuiCard": {
            "styleOverrides": {
                "root": {
                    "variants": [
                        {
                            "props": {"variant": "outlined"},
                            "style": {"borderWidth": "3px"},
                        }
                    ]
                }
            }
        }
    }
}

Card(title="Thick border", variant="outlined", theme_config=custom_theme).servable()
```

:::{tip}
Component keys follow MUI's naming convention (e.g. `MuiButton`, `MuiButtonBase`, `MuiCard`).
Find the right key in the [MUI component docs](https://mui.com/material-ui/all-components/) under
each component's Customization section.
:::

### Theme inheritance

Set `theme_config` once on a top-level container and all descendant `panel-material-ui` components
inherit it automatically. We recommend setting it on a `Page`, `Container`, or similar top-level
component so that every child picks it up without repetition:

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
    },
}

Row(
    Button(label="Inherited theme", button_type="primary"),
    ThemeToggle(),
    theme_config=theme_config,
).preview()
```

---

## Bokeh and hvPlot

Bokeh, hvPlot, and HoloViews plots automatically adapt to the active theme — primary color, font
family, and dark/light mode — when placed inside a `panel-material-ui` container. Include a
`ThemeToggle` or use the `Page` component to enable this:

```{pyodide}
import panel as pn
import panel_material_ui as pmu
import pandas as pd
import hvplot.pandas

pn.extension()

df = pd.read_csv("https://datasets.holoviz.org/penguins/v1/penguins.csv")

toggle = pmu.ThemeToggle(styles={"margin-left": "auto"})

pmu.Container(
    toggle,
    df.hvplot.scatter(
        x="bill_length_mm", y="bill_depth_mm", by="species",
        height=400, responsive=True
    ),
    width_option="md"
).preview()
```

To generate a categorical palette aligned with your Material theme use `pmu.theme.generate_palette`.
For continuous data use `pmu.theme.linear_gradient`. You can also find pre-built categorical color
maps [here](https://colorcet.holoviz.org/user_guide/Categorical.html) and
[here](https://holoviews.org/user_guide/Colormaps.html#categorical-colormaps).

```{pyodide}
import pandas as pd
import hvplot.pandas
import panel_material_ui as pmu

df = pd.read_csv("https://datasets.holoviz.org/penguins/v1/penguins.csv")

primary_color = "#6200ea"
colors = pmu.theme.generate_palette(primary_color)
toggle = pmu.ThemeToggle(styles={"margin-left": "auto"})

pmu.Container(
    toggle,
    df.hvplot.scatter(
        x="bill_length_mm", y="bill_depth_mm", color="species",
        height=400, responsive=True, cmap=colors
    ),
    theme_config={"palette": {"primary": {"main": primary_color}}},
    width_option="md"
).preview()
```

```{pyodide}
import panel as pn
import panel_material_ui as pmu
import pandas as pd
import hvplot.pandas

pn.extension()

df = pd.read_csv("https://datasets.holoviz.org/penguins/v1/penguins.csv")
primary_color = "#6200ea"

cmap = pmu.theme.linear_gradient("#ffffff", primary_color, n=256)
toggle = pmu.ThemeToggle(styles={"margin-left": "auto"})

plot = df.hvplot.scatter(
    x="bill_length_mm", y="flipper_length_mm", c="body_mass_g",
    cmap=cmap, colorbar=True, height=400, responsive=True
).opts(
    backend_opts={"plot.toolbar.autohide": True},
    toolbar="above"
)

pmu.Container(
    toggle, plot,
    theme_config={"palette": {"primary": {"main": primary_color}}},
    width_option="md"
).preview()
```

## Plotly

Plotly theming is applied automatically when a figure is placed inside a `panel-material-ui`
container, and switches with dark mode:

```{pyodide}
import panel as pn
import panel_material_ui as pmui
import plotly.express as px

pn.extension("plotly")

df = px.data.iris()
toggle = pmui.ThemeToggle(styles={"margin-left": "auto"}, value=True)
plot = px.scatter(df, x="sepal_length", y="sepal_width", color="species", height=400)

pmui.Container(toggle, plot, dark_theme=True, width_option="md").preview(height=500)
```

Use `pmui.theme.generate_palette` for categorical sequences and `pmui.theme.linear_gradient` for
continuous scales, passing them via `color_discrete_sequence` and `color_continuous_scale`
respectively:

```{pyodide}
import panel as pn
import plotly.express as px
import panel_material_ui as pmui

pn.extension("plotly")

df = px.data.iris()
primary_color = "#4099da"
colors = pmui.theme.generate_palette(primary_color, n_colors=3)
toggle = pmui.ThemeToggle(styles={"margin-left": "auto"}, value=False)

plot = px.scatter(
    df, x="sepal_length", y="sepal_width", color="species",
    height=400, color_discrete_sequence=colors,
)

pmui.Container(
    toggle, plot,
    theme_config={"palette": {"primary": {"main": primary_color}}},
    width_option="md"
).preview(height=500)
```

```{pyodide}
import panel as pn
import plotly.express as px
import panel_material_ui as pmui

pn.extension("plotly")

df = px.data.iris()
primary_color = "#4099da"
colorscale = pmui.theme.linear_gradient("#ffffff", primary_color, n=256)
toggle = pmui.ThemeToggle(styles={"margin-left": "auto"}, value=False)

plot = px.scatter(
    df, x="sepal_length", y="sepal_width", color="petal_length",
    height=400, color_continuous_scale=colorscale,
)

pmui.Container(
    toggle, plot,
    theme_config={"palette": {"primary": {"main": primary_color}}},
    width_option="md"
).preview(height=500)
```

:::{note}
When using a Plotly `Figure` directly, pass a discrete color sequence via the `colorway` argument
of the `layout` property: `go.Figure(layout={"colorway": colors})`.
:::

---

## See also

- [Apply Branding](branding.md) — end-to-end example of packaging colors, typography, assets, and
  component defaults into a reusable brand module
