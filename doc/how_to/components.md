# Themed Components

You can customize `panel-material-ui` components—changing default props, styles, or adding new variants—by defining a `components` key within your `theme_config`. This approach is ideal for ensuring a consistent look and feel across your entire application. If your customizations are extensive, however, consider creating new component classes for maintainability.

---

## Theme default props

Every `panel-material-ui` component has its own default props. You can override these defaults by specifying `defaultProps` under the component’s key in your `theme_config["components"]` dictionary. For example, to disable the ripple effect in a `Button` everywhere:

```{pyodide}
from panel_material_ui import Button

custom_theme = {
    "components": {
        "MuiButton": {
            "defaultProps": {
                "disableRipple": True
            }
        }
    }
}

Button(label="No Ripple!", theme_config=custom_theme).servable()
```

:::{tip}
The exact key for each component may vary. For instance, if you want to override `MuiButtonBase` specifically, you’d use "MuiButtonBase". If you need to target the higher-level Button or Card, find the appropriate name in Mui documentation.
:::

## Theme style overrides

Use `styleOverrides` to globally change a component’s CSS. Each component’s “slots” are mapped to nested dictionary keys. The `root` slot usually targets the component’s outermost element.

```{pyodide}
custom_theme = {
    "components": {
        "MuiButton": {
            "styleOverrides": {
                "root": {
                    "fontSize": "1rem"
                }
            }
        }
    }
}

Button(label="Styled Button", theme_config=custom_theme).servable()
```

Multiple nesting levels are possible. For instance, `styleOverrides["root"][".my-class"] = {...}` if you need deeper overrides.

## Variants

Some components have props like `variant` or `color` that change their appearance. You can use the variants array in `styleOverrides["root"]` to apply conditional styling based on these props.

### Overriding styles for an existing variant

For example, to increase the border thickness on a Card when variant="outlined":

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
                            "style": {
                                "borderWidth": "3px"
                            }
                        }
                    ]
                }
            }
        }
    }
}
Card(
    title="Thick Outlined Card", variant="outlined", theme_config=custom_theme
).servable()
```

## Theme variables

You can also adjust “global” theme variables like typography or spacing to affect how all components render. For example:


```{pyodide}
from panel_material_ui import Button

custom_theme = {
    "typography": {
        "button": {
            "fontSize": "1rem"
        }
    }
}

Button(
    label="Big Button Text", theme_config=custom_theme
).servable()
```

These theme-level variables can be combined with components overrides for a comprehensive theming approach.

## Summary

1. **Global Defaults**: Set `defaultProps` to override default parameter values for any `panel_material_ui` component.
2. **Style Overrides**: Use styleOverrides["root"] (and other slots) to globally change CSS.
3. **Variants**: Dynamically style components based on existing or custom props—great for “outlined,” “dashed,” or any new variant.
4. **Theme Variables**: Adjust base typography, spacing, and more for broad changes across all components.

With these tools, you can tailor `panel_material_ui` to fit your brand and user experience—whether you need slight tweaks or entirely new variants for your UI.
