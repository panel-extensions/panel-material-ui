# How to customize

Customization of Panel Mui components inherits all the benefits of having a consistent design language that Mui provides. Styling can be applied using `sx` parameter, while theming is achieved through the inheritable `theme_config`. Let us walk through these two different approaches through a series of examples.

This how-to guide was adapted from the [Mui How to Customize](https://mui.com/material-ui/customization/how-to-customize/) guide.

## One-off customizations

To change the styles of one single instance of a Panel Mui component you use the `sx` parameter.

### The `sx` parameter

All Mui-for-Panel components accept an sx parameter that allows you to pass in style overrides. This approach is great for quick, local customizations, such as tweaking the padding of one button or giving a single card a different background color.

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

### Overriding nested component styles

Sometimes you need to target a nested part of a component—for instance, the “thumb” of a slider or the label of a checkbox. Mui-for-Panel components use the same Material UI class names under the hood, so you can target those nested slots by using the relevant selectors in your sx parameter.

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

:::note
Note: Even though Panel Mui components reuse Material UI’s internal class names, these names are subject to change. Make sure to keep an eye on release notes if you override nested classes.
:::

## Theming

`panel_material_ui` also supports theming via the `theme_config`. By specifying certain defaults (e.g. global colors, typography), you can apply consistent styles across components:

```{pyodide}
from panel_material_ui import Button

global_theme = {
    "palette": {
        "primary": {"main": "#d219c9"},
        "secondary": {"main": "#dc004e"},
    }
}

Button(
    label="Global Button", theme_config=global_theme, button_type="primary"
).servable()
```

### Theme inheritance

Theme inheritance is the most important piece here that allows you to apply a consistent theme at the top-level and have it flow down from there.

Here, the child Button automatically inherits the parent’s primary color setting. However, note these important points:

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

Here, the child `Button` automatically inherits the parent’s primary color setting. We generally recommend you style your top level container, be that a `Page`, a `Container` or something else (though it does have to be a Panel Mui component).

::::{caution}
There are some caveats when using theme inheritance:

1. **One-time inheritance**: When the child is first mounted, it checks its immediate parent’s theme.
2. **No automatic re-check**: If an intermediate parent (or the same parent) changes its `theme_config` after the child has already mounted, the child’s theme does not automatically update. In other words, children do not continuously observe every parent for performance reasons.
3 **Own theme overrides**: If the child itself has `theme_config`, that takes precedence, and it will not inherit from the parent.

This approach ensures good performance—otherwise, every child would have to watch for theme changes up the tree. We therefore strongly recommend that if you have specific theming needs, you set those up before initial render or when newly mounting a subcomponent. For one of styling primarily make use of one of customizations using `sx`. If you absolutely need to re-theme a sub-component **and its children** after initial render, remove it, apply the new `theme_config` and re-add it, the children will now automatically pick up the new theme.
::::
