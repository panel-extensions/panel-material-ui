```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Fullscreen` wrapper lets any component take over the whole screen and return to its place in the page, e.g. to present a dashboard, a map or a chart.

Clicking its toggle button puts the page into the browser's full screen and lays the wrapped component over it. Leaving full screen in the browser, with Escape or the browser's own controls, brings the component back and sets `active` to `False`. Where the browser offers no full screen for pages, as on iPhone Safari, or refuses it, the component covers the browser window instead, and Escape leaves it.

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`active`** (bool): Whether the component covers the screen. Default is False.
* **`disabled`** (bool): Whether entering full screen is disabled. Default is False.
* **`object`** (Viewable): The component to show in full screen.
* **`toggle_class`** (str): A CSS class marking toggles of this wrapper anywhere on the page, e.g. a button in an app bar.

##### Browser state (read-only)

* **`native`** (bool): Whether the page is in the browser's real full screen, rather than the component covering the window.
* **`supported`** (bool): Whether the browser offers real full screen for the page.

##### Display

* **`toolbar`** (list): Components shown next to the toggle button while in full screen, e.g. a title or a status.
* **`hide_delay`** (int or None): Milliseconds without pointer or keyboard activity after which the toolbar and the pointer are hidden in full screen. None keeps them visible. Default is 2500.
* **`inert`** (bool): Whether the rest of the page is made inert in full screen, so focus, clicks and screen readers only reach the component and the dialogs, menus and notifications it opens. Default is True.
* **`label`** (str): The accessible name of the toolbar.
* **`placement`** (str): Where the toggle button and toolbar sit: 'top-left', 'top-right' (default), 'bottom-left' or 'bottom-right'.
* **`show_button`** (bool): Whether to show the toggle button. Default is True.

##### Styling

- **`sx`** (dict): Component level styling API for advanced customization
- **`theme_config`** (dict): Theming API for consistent design system integration

___

### Basic Usage

Wrap a component to add a low-emphasis toggle button in its corner. Give the wrapped component a responsive `sizing_mode` so it fills the screen:


```python
pmui.Fullscreen(
    pmui.Paper(
        pmui.Typography("Quarterly report", variant="h5"),
        pmui.Typography("Click the button in the corner to enter full screen."),
        sizing_mode="stretch_both",
    ),
    height=250,
    sizing_mode="stretch_width",
)
```

### Toolbar

Add a `toolbar` to show a title or a status beside the exit button while in full screen. They fade out, together with the pointer, after `hide_delay` milliseconds without activity and return as soon as the pointer moves, the screen is tapped or a key is pressed. Use `placement` to move them to another corner. At the top right of a `Card` they sit beside the card's own header actions, such as its collapse button, rather than over them:


```python
status = pmui.Chip(label="All systems up", color="success", size="small")

pmui.Fullscreen(
    pmui.Paper(
        pmui.Typography("Operations", variant="h5"),
        sizing_mode="stretch_both",
    ),
    toolbar=[status],
    placement="bottom-right",
    label="Operations, full screen toolbar",
    height=250,
    sizing_mode="stretch_width",
)
```


```python
pmui.Fullscreen(
    pmui.Card(
        pmui.Typography("Revenue by region"),
        title="Dashboard card",
        collapsible=True,
        sizing_mode="stretch_both",
    ),
    toolbar=[pmui.Chip(label="Live", color="success", size="small")],
    height=250,
    sizing_mode="stretch_width",
)
```

### Toggling From Elsewhere

Browsers only grant full screen in response to a user gesture, so the wrapper handles its toggles in the browser. Besides the built-in button you can:

- give any element inside the component the `pmui-fullscreen-toggle` or `pmui-fullscreen-exit` CSS class (`Fullscreen.TOGGLE_CLASS`, `Fullscreen.EXIT_CLASS`),
- mark toggles anywhere on the page, e.g. in an app bar, with a class of your choice passed as `toggle_class`,
- dispatch a `pmui:fullscreen-toggle` event on the document (`Fullscreen.TOGGLE_EVENT`), e.g. from a keyboard shortcut. It toggles the wrapper holding the focus, else the one in full screen, else the first.


```python
present = pmui.Button(label="Present", icon="slideshow", css_classes=["present-report"])

report = pmui.Fullscreen(
    pmui.Paper(
        pmui.Typography("Board meeting", variant="h5"),
        pmui.Button(label="Done", css_classes=[pmui.Fullscreen.EXIT_CLASS]),
        sizing_mode="stretch_both",
    ),
    show_button=False,
    toggle_class="present-report",
    height=250,
    sizing_mode="stretch_width",
)

pmui.Column(present, report, sizing_mode="stretch_width")
```

### Setting `active`

Setting `active` from Python also works. A request that does not follow a click closely may be refused by the browser, in which case the component covers the browser window rather than the screen. `native` and `supported` report what the browser did:


```python
wrapper = pmui.Fullscreen(
    pmui.Paper(pmui.Typography("Kiosk view", variant="h5"), sizing_mode="stretch_both"),
    height=200,
    sizing_mode="stretch_width",
)
toggle = pmui.Button(label="Toggle full screen", on_click=lambda _: wrapper.toggle())

pmui.Column(
    toggle,
    pmui.Typography(pn.bind(lambda a, n: f"active={a}, native={n}", wrapper.param.active, wrapper.param.native)),
    wrapper,
    sizing_mode="stretch_width",
)
```

### Disabled

Set `disabled=True` to prevent entering full screen, e.g. while editing. Leaving it is always possible:


```python
pmui.Fullscreen(
    pmui.Paper(pmui.Typography("Editing"), sizing_mode="stretch_both"),
    disabled=True,
    height=150,
    sizing_mode="stretch_width",
)
```

### Theming and Overlays

In full screen the component is laid over the page on the theme's background color, so it follows light and dark mode. Dialogs, menus and notifications it opens still show on top. While it covers the screen the rest of the page is made inert; give elements that must stay usable, such as a command palette rendered outside the component, the `pmui-fullscreen-keep` CSS class (`Fullscreen.KEEP_CLASS`), or turn this off with `inert=False`.

### References

**Panel Material UI:**

- [Reveal](../global/Reveal.ipynb) - Scroll to and highlight elements on the page

**Web APIs:**

- [Fullscreen API](https://developer.mozilla.org/en-US/docs/Web/API/Fullscreen_API)
- [The inert attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/inert)
