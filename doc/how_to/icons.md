# Icons

**panel-material-ui** provides ships with the Material UI icon library. This means that you can use any of the icons defined in the [Material UI icon library](https://mui.com/material-ui/material-icons/) by default and also include them in `Markdown` and `HTML` components.

## `icon` parameter

Many components in **panel-material-ui** accept the `icon` parameter. This can be a string referring to the *snake_case* name of the icon, which you can find in the [Material icon library](https://fonts.google.com/icons?icon.set=Material+Icons).

You can choose between filled and outlined icons by adding `_outlined` to the icon name:

```{pyodide}
import panel_material_ui as pmui

pmui.Row(
  pmui.ButtonIcon(icon="lightbulb"),
  pmui.ButtonIcon(icon="lightbulb_outline")
)
```

## Icons in `Markdown` and `HTML`

You can also include icons in `Markdown` and `HTML` components by wrapping the icon name in `material-icons` or `material-icons-outlined` classes:

```{pyodide}
pmui.Column(
  'Here is a lightbulb: <span class="material-icons" style="font-size: 2em;">lightbulb</span>',
  'Here is an outlined lightbulb: <span class="material-icons-outlined" style="font-size: 2em;">lightbulb</span>'
)
```
