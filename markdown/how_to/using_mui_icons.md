# Use Icons

**panel-material-ui** ships with the Material UI icon library. This means that you can use any of the icons defined in the [Material UI icon library](https://mui.com/material-ui/material-icons/) by default and also include them in `Markdown` and `HTML` components.

## `icon` parameter

Many components in **panel-material-ui** accept the `icon` parameter. This can be a string referring to the *snake_case* name of the icon, which you can find in the [Material icon library](https://fonts.google.com/icons?icon.set=Material+Icons).

You can choose between filled and outlined icon variants by appending `_outlined` to the icon name:

```{pyodide}
import panel_material_ui as pmui

pmui.Row(
  pmui.ButtonIcon(icon="lightbulb"),
  pmui.ButtonIcon(icon="lightbulb_outlined"),
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

## Icons in text (`:material/...:` tokens)

You can embed icons directly in text rendered by **panel-material-ui** components using the `:material/<icon>:` token syntax:

```{pyodide}
pmui.Select(
  name="Mode",
  options=[
    "Zoom :material/zoom_out_map:",
    "Explore :material/explore:",
  ],
)
```

You can also pass per-icon options after the icon name using `@key=value` pairs, separated by commas:

```{pyodide}
pmui.Button(
  name="Warn :material/zoom_out_map@size=large,color=warning:",
)
```

Supported per-icon options are:

| Option | Description | Example |
| --- | --- | --- |
| `color` | Theme color or CSS color of the icon | `@color=warning` |
| `variant` | Icon variant: `filled`, `outlined`, `rounded` or `sharp` | `@variant=outlined` |
| `size` | Icon size, either `small`, `medium`, `large` or a CSS size | `@size=large` |
| `icon_size` | Explicit CSS font size of the icon | `@icon_size=2rem` |

Overrides apply only to the token where they appear. Unknown options are ignored, and text
which is not a valid token (e.g. `:material/not an icon:`) is left untouched.

### Where tokens are supported

Tokens are rendered wherever a **panel-material-ui** component displays text:

- Button, `Fab`, toggle, chip, pill, rating and icon labels.
- Input, select, autocomplete, checkbox, radio, switch, slider, picker and color-picker labels,
  helper text, option labels, group headers and selected values.
- Menu, menu button, split button, menu bar, list, tree, breadcrumb, stepper and speed-dial labels,
  hints and tooltips.
- `Tabs` tab names, `Card`, `Details` and `Accordion` titles, `Alert` titles, `Dialog` titles and
  `Page`/app bar titles.
- Widget `description` tooltips, the `Tooltip` wrapper, `Badge` content and notifications.

### Accessibility and string-only slots

Some slots can only hold plain strings, e.g. `aria-label`, native `title` tooltips, `alt` text,
input `placeholder` values, the floating label of an outlined input and the options of a native
`MultiSelect`. In those slots the token is stripped and the readable text is used instead, so a
label of `":material/add: Create"` produces the accessible name `Create`. If the text consists only
of tokens, the humanized icon name is used, e.g. `":material/zoom_out_map:"` becomes
`zoom out map`.

### Limitations

- Titles that are supplied as Panel components (e.g. `Card.header`) are rendered as-is; token
  parsing only applies to string titles and names.
- `Card`, `Details`, `Accordion` and `Tabs` titles continue to support HTML. HTML and tokens can be
  mixed, e.g. `":material/dashboard: <b>Overview</b>"`.
- Core Panel and Bokeh components (`pn.widgets`, `pn.Tabs`, `Markdown`, `HTML`, plots, plot tooltips
  and axis labels) have no Material Icons token renderer and display the token as literal text. Use
  the `material-icons` span syntax shown above in `Markdown` and `HTML` panes instead.
