# How to Customize

Customization of Panel Mui components inherits all the benefits of having a consistent design language that Mui provides. Styling can be applied using the `sx` parameter, while theming is achieved through the inheritable `theme_config`. Let us walk through these two different approaches through a series of examples.

This how-to guide was adapted from the [Mui How to Customize](https://mui.com/material-ui/customization/how-to-customize/) guide.

## One-off Customizations

To change the styles of one single instance of a Panel Mui component, you use the `sx` parameter.

### The `sx` Parameter

All Mui-for-Panel components accept an `sx` parameter that allows you to pass in style overrides. This approach is great for quick, local customizations, such as tweaking the padding of one button or giving a single card a different background color.

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

If you need to apply some styling only in either dark or light mode, you can use the `.mui-dark` or `.mui-light` class.

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


Learn more about the [`sx` parameter in the Mui docs](https://mui.com/system/getting-started/the-sx-prop/).

### Overriding Nested Component Styles

Sometimes you need to target a nested part of a component—for instance, the *thumb* of a slider or the label of a checkbox. Mui-for-Panel components use the same Material UI class names under the hood, so you can target those nested slots by using the relevant selectors in your `sx` parameter.

For example, if you want to make the thumb of a Slider square instead of round, you can do:

```{pyodide}
from panel_material_ui import FloatSlider

FloatSlider(
    sx={
        "& .MuiSlider-thumb": {
            "borderRadius": 0  # square
        }
    }
).servable()
```

Here too you can prefix the selector with `&.mui-dark` or `&.mui-light` to apply the styling only in either dark or light mode.

:::{note}
Note: Even though Panel Mui components reuse Material UI’s internal class names, these names are subject to change. Make sure to keep an eye on release notes if you override nested classes.
:::

## Theming

`panel_material_ui` also supports theming via the `theme_config`. By specifying certain defaults (e.g., global colors, typography), you can apply consistent styles across components:

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

If you want to provide distinct `theme_config` definitions for dark and light mode, you can do so by providing a dictionary with `dark` and `light` keys.

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

Theme inheritance is the most important piece here that allows you to apply a consistent theme at the top-level and have it flow down from there.

Here, the child Button automatically inherits the parent's primary color setting:

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

Here, the child `Button` automatically inherits the parent’s primary color setting. We generally recommend you style your top-level container, be that a `Page`, a `Container`, or something else (though it does have to be a Panel Mui component).
