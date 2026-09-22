```python
import panel as pn
from panel_material_ui import Page, Tabs

pn.extension()
```

The `Page` component is the equivalent of a `Template` in Panel, defining the overall layout of an application.

Unlike a `Template`, the `Page` component is implemented entirely in JavaScript, allowing dynamic updates of its contents without re-rendering the entire layout.

## Parameters:
For details on other options for customizing the component see the layout and styling how-to guides.

### Core

* **`config`** (`Config`): Configuration object declaring custom CSS and JS files to load specifically for this template.
* **`favicon`** (`Path | str | dict[str, str | Path]`): Favicon to render.
* **`logo`** (`Path | str | dict[str, str | Path]`): Logo to render in the header. Can be a string, a pathlib.Path, or a dictionary with breakpoints as keys, e.g. {'sm': 'logo_mobile.png', 'md': 'logo.png'} or themes as keys, e.g. `{'dark': 'logo_dark.png', 'light': 'logo.png'}`.
* **`meta`** (`Meta`): Meta tags and other HTML head elements.
* **`template`** (`str | Path | jinja2.Template`): Overrides the default jinja2 template.
* **`title`** (`str`): Title of the application.

### Layout

* **`header`** (`Children`): Items rendered in the header.
* **`main`** (`Children`): Items rendered in the main area.
* **`sidebar`** (`Children`): Items rendered in the sidebar.
* **`contextbar`** (`Children`): Items rendered in the contextbar.

### Sidebar

* **`sidebar_open`** (`boolean`): Whether the sidebar is open or closed.
* **`sidebar_resizable`** (`boolean`): Whether the sidebar is resizable.
* **`sidebar_variant`** (`Literal["persistent", "temporary", "permanent", "auto"]`): Whether the sidebar is persistent, temporary, permanent or automatically adapts based on screen size.
* **`sidebar_width`** (`int`): Width of the sidebar.

### Contextbar

* **`contextbar_open`** (`boolean`): Whether the contextbar is open or closed.
* **`contextbar_resizable`** (`boolean`): Whether the contextbar is resizable.
* **`contextbar_variant`** (`Literal["persistent", "temporary", "permanent", "auto"]`): Whether the contextbar is persistent, temporary, permanent or automatically adapts based on screen size.
* **`contextbar_width`** (`int`): Width of the contextbar.

### Indicators

* **`busy`** (`boolean`, readonly): Linked to global busy state.
* **`busy_indicator`** (`Literal["circular", "linear"] | None`): Whether to render a linear, circular or no busy indicator.
* **`theme_toggle`** (boolean): Whether to show a theme toggle button.
___

### 📄 Basic Example: Main, Sidebar, and Contextbar

This example creates a simple `Page` layout with content defined in the `main`, `sidebar`, and `contextbar` areas.


```python
page = Page(
    main=["## I'm the main area"],
    sidebar_width=250,
    sidebar=["## I'm the sidebar"],
    contextbar=["# I'm the contextbar"],
    title="I'm a title",
)

page.preview()
```

#### 🔍 What’s Happening?

- **`main`**: The primary content area of the page, here showing a simple Markdown heading.
- **`sidebar`**: A side panel typically used for navigation or filters. Its width is set to `250` pixels.
- **`contextbar`**: An optional, secondary sidebar often used for auxiliary info or tools.
- **`title`**: Sets the page title shown in the browser tab and can be used in the layout.

## Sidebar variants

By default the `sidebar_variant` is set to `auto`, which switches from a persistent to a temporary sidebar on mobile.


```python
temp_page = page.clone(
    sidebar_variant='temporary'
)

temp_page.preview()
```

The `sidebar` now overlays the main content.

We can also make the sidebar `permanent` (disabling the sidebar toggle):


```python
temp_page = page.clone(
    sidebar_variant='permanent'
)

temp_page.preview()
```

## Contextbar variants

The `contextbar_variant` works the same way as `sidebar_variant`. By default it is set to `"temporary"`, meaning the contextbar overlays the main content when opened. Setting it to `"persistent"` keeps it visible alongside the main content:


```python
persistent_context = page.clone(
    contextbar_variant='persistent',
    contextbar_open=True
)

persistent_context.preview()
```

Both the sidebar and contextbar can be resized by dragging when `sidebar_resizable` / `contextbar_resizable` is `True` (the default). Set either to `False` to disable resizing:


```python
fixed_page = page.clone(
    sidebar_resizable=False,
    contextbar_resizable=False,
    contextbar_variant='persistent',
    contextbar_open=True
)

fixed_page.preview()
```

### 🎨 Custom Theming with `theme_config`

This example demonstrates how to apply a custom theme to the `Page` layout using the `theme_config` option.


```python
HEADER_COLOR = "#2A3E5C"
PAPER_COLOR = "#f8f8f8"

themed = page.clone(theme_config={
    'palette': {
        'primary': {
            'main': HEADER_COLOR # The header is styled by the primary palette
        },
        'background': {
          'paper': PAPER_COLOR, # The remaining areas are paper colored
        },
    }
}, theme_toggle=False)

themed.preview()
```

#### 🎯 Key Customizations

- **Primary Palette (`primary.main`)**: Sets the header color using a deep, modern blue-gray (`#2A3E5C`).
- **Background (`background.paper`)**: Applies a light neutral background (`#f8f8f8`) to content areas like the main, sidebar, and contextbar.

:::note
By setting `theme_toggle=False`, the user is not shown a button to switch between light and dark modes — keeping the design consistent.
:::

### 🎨 Advanced Styling with `sx`

This example builds on the previous themed layout, applying fine-grained custom styles using the `sx` parameter (which accepts CSS-like syntax).


```python
styled = themed.clone(sx={
    "& .header": {
        "backgroundColor": "#673AB7"
    },
    "& .title": {
        "fontSize: 2.5em"
    },
    "& .main": {
        "backgroundColor": "#c3c3c3",
    },
    "&.mui-dark .main": {
        "backgroundColor": "#3f3f3f",
    },
    "& .sidebar": {
        "backgroundColor": "#e9e9e9"
    },
    "&.mui-dark .sidebar": {
        "backgroundColor": "#2a2a2a",
    },
    "& .contextbar": {
        "backgroundColor": "#525252",
        "color": "white"
    },
}, theme_toggle=True)

pn.Tabs(
    ('Theme: Default', styled.preview()),
    ('Theme: Dark', styled.clone(dark_theme=True).preview())
)
```

#### 🌗 Theme Toggle Enabled

Unlike the previous example, this version re-enables the **theme toggle**, letting users switch between light and dark modes. The `sx` rules adapt accordingly — as shown with the conditional `".mui-dark .main"` style.

### Configuring the page loader

The `Page` component renders into a `template`, which, by default, includes a loading spinner. This loading spinner can be overridden with a custom template, e.g. below we define a custom loader generated with [loading.io](https://loading.io):


```python
template = """
{% extends "base.html" %}

{% block loader_css %}
@keyframes ldio-yzaezf3dcmj-1 {
    0% { transform: rotate(0deg) }
   50% { transform: rotate(-45deg) }
  100% { transform: rotate(0deg) }
}
@keyframes ldio-yzaezf3dcmj-2 {
    0% { transform: rotate(180deg) }
   50% { transform: rotate(225deg) }
  100% { transform: rotate(180deg) }
}
.ldio-yzaezf3dcmj > div:nth-child(2) {
  transform: translate(-15px,0);
}
.ldio-yzaezf3dcmj > div:nth-child(2) div {
  position: absolute;
  top: 40px;
  left: 40px;
  width: 120px;
  height: 60px;
  border-radius: 120px 120px 0 0;
  background: #fee547;
  animation: ldio-yzaezf3dcmj-1 1s linear infinite;
  transform-origin: 60px 60px
}
.ldio-yzaezf3dcmj > div:nth-child(2) div:nth-child(2) {
  animation: ldio-yzaezf3dcmj-2 1s linear infinite
}
.ldio-yzaezf3dcmj > div:nth-child(2) div:nth-child(3) {
  transform: rotate(-90deg);
  animation: none;
}@keyframes ldio-yzaezf3dcmj-3 {
    0% { transform: translate(190px,0); opacity: 0 }
   20% { opacity: 1 }
  100% { transform: translate(70px,0); opacity: 1 }
}
.ldio-yzaezf3dcmj > div:nth-child(1) {
  display: block;
}
.ldio-yzaezf3dcmj > div:nth-child(1) div {
  position: absolute;
  top: 92px;
  left: -8px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #000000;
  animation: ldio-yzaezf3dcmj-3 1s linear infinite
}
.ldio-yzaezf3dcmj > div:nth-child(1) div:nth-child(1) { animation-delay: -0.67s }
.ldio-yzaezf3dcmj > div:nth-child(1) div:nth-child(2) { animation-delay: -0.33s }
.ldio-yzaezf3dcmj > div:nth-child(1) div:nth-child(3) { animation-delay: 0s }
.loadingio-spinner-bean-eater-2by998twmg8 {
  width: 200px;
  height: 200px;
  display: inline-block;
  overflow: hidden;
  background: #ffffff;
}
.ldio-yzaezf3dcmj {
  width: 100%;
  height: 100%;
  position: relative;
  transform: translateZ(0) scale(1);
  backface-visibility: hidden;
  transform-origin: 0 0; /* see note above */
}
.ldio-yzaezf3dcmj div { box-sizing: content-box; }

.loading {
  position: fixed;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 1050;
  height: 100%;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  font-size: 1.5rem;
  color: #ffffff;

  -webkit-animation: fadein 0.5s; /* Safari, Chrome and Opera > 12.1 */
     -moz-animation: fadein 0.5s; /* Firefox < 16 */
      -ms-animation: fadein 0.5s; /* Internet Explorer */
       -o-animation: fadein 0.5s; /* Opera < 12.1 */
          animation: fadein 0.5s;
}
{% endblock %}

{% block loader %}
<div class="loading" id="loader">
  <div class="loadingio-spinner-bean-eater-2by998twmg8">
    <div class="ldio-yzaezf3dcmj">
      <div><div></div><div></div><div></div></div><div><div></div><div></div><div></div></div>
    </div>
  </div>
</div>
{% endblock %}

{% block loader_script %}
<!--  Ordinarily this would hide the loader --!>
{% endblock %}
"""

Page(template=template).preview()
```

:::note
Above we overrode the `loader`, `loader_css` and `loader_script` block. The `loader_script` is responsible for hiding the element with `id="loader"`, ensuring that once the page is fully loaded the loading screen is hidden. Ordinarily you would only override the `loader` and `loader_css` blocks.
:::

### Controls

The `Page` exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
control_page = Page()
control_page.main = [control_page.controls(jslink=True)]
control_page.preview(height=1000)
```
