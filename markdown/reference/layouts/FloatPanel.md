```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `FloatPanel` layout displays content in a movable Material UI `Paper` surface. By default it floats within its parent; set `contained=False` to anchor it to the browser viewport. Drag the title bar or empty surface to move it without moving widgets inside.

## Parameters

### Position and content

* **`contained`** (`bool`): Position the panel within its parent (`True`, the default) or the viewport (`False`).
* **`position`** (`str`): Initial anchor, default `"right-top"`. Options: `"center"`, `"left-top"`, `"center-top"`, `"right-top"`, `"right-center"`, `"right-bottom"`, `"center-bottom"`, `"left-bottom"`, and `"left-center"`.
* **`offsetx`**, **`offsety`** (`int`): Pixel offsets from the selected anchor, default 0. Change the anchor or offsets to reset a panel after it has been dragged.
* **`status`** (`str`): `"normalized"` (default), `"maximized"`, `"minimized"`, `"smallified"`, `"smallifiedmax"`, or `"closed"`. The title-bar buttons update this parameter.
* **`controls`** (`list[str]`): Title-bar actions to show, selected from `"minimize"`, `"maximize"`, and `"close"`. All three are shown by default; use `[]` to hide them all.
* **`objects`** (`list`): Panel or Material UI components displayed inside the surface. Like other list-like layouts, `FloatPanel` accepts positional children and supports `append`, `extend`, and `clear`.

### Appearance

* **`elevation`** (`int`): Shadow depth of the surface when `variant="elevation"`; defaults to 1.
* **`variant`** (`"elevation"` or `"outlined"`): Use a shadow or an outline; defaults to `"elevation"`.
* **`square`** (`bool`): Remove the rounded corners; defaults to `False`.
* **`sx`** (`dict`): Material UI style overrides applied to the Paper surface.

See the [styling guide](https://panel-material-ui.holoviz.org/how_to/customize_themes_and_styles.html) for more ways to customize Material UI components.

### Floating controls

Pass widgets as positional children or through `objects`. Drag the title bar or padding around these controls; the rating and button remain interactive. This example floats over the page content.


```python
controls = pmui.FloatPanel(
    pmui.Rating(value=3, size="small"),
    pmui.Button(label="Submit", on_click=lambda event: print("Submitted")),
    name="Feedback", contained=False, position="left-top", offsetx=24, offsety=80,
    elevation=4,
)

pmui.Page(title="Floating controls", main=["# Try dragging the panel", controls]).preview()
```

### Positioning

`position` selects one of nine anchors relative to the parent (`contained=True`) or the viewport (`contained=False`). `offsetx` and `offsety` add spacing from that anchor. A viewport panel stays put as the page scrolls. A contained panel needs space from its parent layout, for example a `Column` with an explicit height.

Focus the surface with Tab and use the arrow keys to move it in 10-pixel steps. Dragging changes its browser position; it does not change the named `position` anchor in Python. Assign a new anchor or offset to reposition it programmatically.


```python
positioned = pmui.FloatPanel("Move me within the box", name="Contained panel",
                             position="center", sx={"p": 2})

pmui.Column(positioned, width=450, height=280, sx={"border": "1px dashed"})
```

### Elevation and variants

Like `Paper`, the default `elevation` variant uses a shadow to separate the surface from the page. A higher `elevation` makes the shadow stronger. Use `variant="outlined"` for a flat surface with a border instead. `square=True` removes the rounded corners. These options follow the active Material UI theme, including dark mode. Drag the bottom-right 16-pixel corner to resize a normalized panel. Resizing stays within the parent or viewport and does not change Python's `width` and `height` parameters.


```python
shadow = pmui.FloatPanel("Elevated surface", name="Shadow", elevation=8,
                         position="left-center", offsetx=20)
outline = pmui.FloatPanel(
    "Outlined, square surface", name="Outline", variant="outlined", square=True,
    position="right-center", offsetx=20,
)

pmui.Column(shadow, outline, width=560, height=300, sx={"border": "1px dashed"})
```

### Window controls

The title bar shows the panel's `name` and buttons to minimize, maximize, restore, and close it. These controls update `status` in Python; set `status="normalized"` to reopen a closed panel. A minimized panel retains its title bar so it can be restored. Set `controls=["minimize", "maximize"]` to omit the close button, or `controls=[]` to omit all actions.


```python
window = pmui.FloatPanel("Try the window controls", name="Window states",
                         contained=False, position="center", controls=["minimize", "maximize"])

pmui.Page(title="Window controls", main=[window]).preview()
```

### Updating the contents

`FloatPanel` uses the same list-like API as other Material UI layouts. Add a component with `append`, replace `objects`, or call `clear` to remove them. In a live server app, calling `actions.append(...)` again updates the displayed panel without recreating it.


```python
actions = pmui.FloatPanel(pmui.Button(label="First action"), name="Actions",
                          position="center")
actions.append(pmui.Button(label="Second action"))

pmui.Column(actions, width=450, height=280, sx={"border": "1px dashed"})
```
