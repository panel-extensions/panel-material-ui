# Build Custom Components

The `panel-material-ui` package ships with a number of custom Material UI components that are built on top of the Material UI library. However, in some cases, you may need to create your own custom components.

The `MaterialUIComponent` provides a convenient entry point for building custom Material UI components using Panel, that will inherit the functionality of `panel-material-ui` while building on the existing JS bundle.

To understand the basics of building custom components in Panel, see the documentation for the [ReactComponent](https://panel.holoviz.org/reference/custom_components/ReactComponent.html), which the `MaterialUIComponent` is built on top of.

## What are we making?

Let’s build something delightfully colorful: a `RainbowButton` that cycles through the colors of the rainbow when you hover or click it! You’ll get hands-on practice with:

- Subclassing `panel_material_ui.MaterialUIComponent`
- Defining `Param` properties for the Python side
- Wiring up React state and hooks in your `.jsx`

### The Python Side

First, we need to define the `RainbowButton` class, which subclasses `MaterialUIComponent`.

```python
import param

from panel_material_ui import MaterialUIComponent

RAINBOW = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]

class RainbowButton(MaterialUIComponent):
    """
    A Button that cycles through rainbow colors.

    :Example:

    >>> RainbowButton(label="Go!", size="medium", mode="hover")
    """

    colors = param.List(default=RAINBOW, doc="""
        The colors to cycle through.""")

    label = param.String(default="Click me!", doc="""
        The label shown on the button.""")

    size = param.Selector(default="medium", objects=["small", "medium", "large"], doc="""
        Material-UI button size.""")

    mode = param.Selector(default="hover", objects=["hover", "click"], doc="""
        When to cycle: on hover or on click.""")

    interval = param.Integer(default=200, doc="""
        Time in ms between color changes.""")

    _esm_base = "RainbowButton.jsx"
    _importmap = {
      "imports": {
          "confetti": "https://esm.sh/canvas-confetti@1.6.0"
      }
    }
```

Here we:

- Subclass `MaterialUIComponent`
- Define five parameters: `label`, `size`, `mode`, `interval`, and `colors`
- Point at our React file `RainbowButton.jsx` with `_esm_base`, given as a path relative to the Python file
- Add an import map to load the `canvas-confetti` library

### The React Side

Now we need to create the React component that will be used to render the `RainbowButton`. As with all ESM components, we need to export a `render` function that takes a `model` argument.

Material UI components can be imported one at a time (`import Button from "@mui/material/Button"`) or several at once (`import {Stack, Typography} from "@mui/material"`), and they resolve to the copy bundled with `panel-material-ui` rather than being downloaded again. Note that the default import name has to match the name of the Material UI component, i.e. `import Button from "@mui/material/Button"` works but `import MyButton from "@mui/material/Button"` does not.

```jsx
import Button from "@mui/material/Button";
import confetti from "confetti"

export function render({model}) {
  // Sync Python params into React state
  const [label]    = model.useState("label");
  const [colors]   = model.useState("colors");
  const [size]     = model.useState("size");
  const [mode]     = model.useState("mode");
  const [interval] = model.useState("interval");

  // Internal state: current color index
  const [index, setIndex] = React.useState(0);

  // Function to advance the color
  const nextColor = () => (
    setIndex(i => (i + 1) % colors.length)
  );

  // On “click” mode, cycle once per click
  const handleClick = () => {
    confetti();
    if (mode === "click") nextColor();
  };

  // On “hover” mode, cycle continuously while hovered
  let hoverTimer = React.useRef(null);
  const handleMouseEnter = () => {
    if (mode === "hover") {
      hoverTimer.current = setInterval(nextColor, interval);
    }
  };
  const handleMouseLeave = () => {
    if (mode === "hover") {
      clearInterval(hoverTimer.current);
    }
  };

  const currentColor = colors[index % colors.length];

  return (
    <Button
      variant="contained"
      size={size}
      onClick={handleClick}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      sx={{
        backgroundColor: currentColor,
        color: "white",
        textTransform: "none"
      }}
    >
      {label}
    </Button>
  );
}
```

**What’s happening?**

- We pull in the Python params via `model.useState(...)`, which also re-renders the component whenever a parameter changes (reading `model.colors` directly would not)
- We maintain our own index to track which color we’re on
- Two modes:
  - `hover`: start a setInterval on enter, clear it on leave
  - `click`: advance once per click
- We style the MUI `<Button>` using the current rainbow color
- We use the `confetti` library to create a confetti effect when the button is clicked

## Usage

To see what we have built in action, let's quickly put it all together. We will inline ESM code in the Python side and render it:

```{pyodide}
import param
import panel as pn

from panel_material_ui import MaterialUIComponent

pn.extension()

RAINBOW = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]

class RainbowButton(MaterialUIComponent):
    """
    A Button that cycles through rainbow colors.

    :Example:

    >>> RainbowButton(label="Go!", size="medium", mode="hover")
    """

    colors = param.List(default=RAINBOW, doc="""
        The colors to cycle through.""")

    label = param.String(default="Click me!", doc="""
        The label shown on the button.""")

    size = param.Selector(default="medium", objects=["small", "medium", "large"], doc="""
        Material-UI button size.""")

    mode = param.Selector(default="hover", objects=["hover", "click"], doc="""
        When to cycle: on hover or on click.""")

    interval = param.Integer(default=200, doc="""
        Time in ms between color changes.""")

    _importmap = {
      "imports": {
          "confetti": "https://esm.sh/canvas-confetti@1.6.0"
      }
    }

    _esm = """
import Button from "@mui/material/Button";
import confetti from "confetti"

export function render({model}) {
  // Sync Python params into React state
  const [label]    = model.useState("label");
  const [colors]   = model.useState("colors");
  const [size]     = model.useState("size");
  const [mode]     = model.useState("mode");
  const [interval] = model.useState("interval");

  // Internal state: current color index
  const [index, setIndex] = React.useState(0);

  // Function to advance the color
  const nextColor = () => (
    setIndex(i => (i + 1) % colors.length)
  );

  // On “click” mode, cycle once per click
  const handleClick = () => {
    confetti();
    if (mode === "click") nextColor();
  };

  // On “hover” mode, cycle continuously while hovered
  let hoverTimer = React.useRef(null);
  const handleMouseEnter = () => {
    if (mode === "hover") {
      hoverTimer.current = setInterval(nextColor, interval);
    }
  };
  const handleMouseLeave = () => {
    if (mode === "hover") {
      clearInterval(hoverTimer.current);
    }
  };

  const currentColor = colors[index % colors.length];

  return (
    <Button
      variant="contained"
      size={size}
      onClick={handleClick}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      sx={{
        backgroundColor: currentColor,
        color: "white",
        textTransform: "none"
      }}
    >
      {label}
    </Button>
  );
}"""

RainbowButton(label="Unicorn Power!", mode="hover", interval=150)
```

Give it a try, hover over the button to see it cycle through the rainbow colors and click it to see the confetti effect!

## Icons

The Material Icons font is loaded together with the component, so the simplest way to add an icon is the `Icon` component with the icon name as its text. Set the font family explicitly with `style={{fontFamily: "Material Icons"}}` so that the icon resolves inside the component's shadow DOM; use `"Material Icons Outlined"` for the outlined variants:

```{pyodide}
import param
import panel as pn

from panel_material_ui import MaterialUIComponent

pn.extension()

class LikeButton(MaterialUIComponent):

    liked = param.Boolean(default=False)

    _esm = """
import IconButton from "@mui/material/IconButton";
import Icon from "@mui/material/Icon";

export function render({ model }) {
  const [liked, setLiked] = model.useState("liked");
  return (
    <IconButton color="primary" onClick={() => setLiked(!liked)}>
      <Icon fontSize="large" style={{fontFamily: "Material Icons"}}>
        {liked ? "favorite" : "favorite_border"}
      </Icon>
    </IconButton>
  );
}
"""

LikeButton()
```

### SVG icon imports

If you prefer the SVG icons of `@mui/icons-material`, add an explicit import for each icon to the `_importmap`, using the same version as the bundled Material UI (currently 9.0.1). Marking React as external with `?external=react` ensures the icons load as separate ESM modules while sharing the React instance of the other components. Only list `react` there: `?external=react,react/jsx-runtime` fails to load and `?external=react,@emotion/react` breaks the icon. The icons bring their own copy of the Material UI styles, which are not applied inside the component, so give them their dimensions and fill with inline styles:

```{pyodide}
import panel as pn

from panel_material_ui import MaterialUIComponent

pn.extension()

class IconComponent(MaterialUIComponent):
    """MUI IconButton with Favorite icon."""

    _importmap = {
        "imports": {
            "@mui/icons-material/Favorite": "https://esm.sh/@mui/icons-material@9.0.1/Favorite?external=react",
        }
    }

    _esm = """
import IconButton from "@mui/material/IconButton";
import FavoriteIcon from "@mui/icons-material/Favorite";

export function render({ model }) {
    return (
      <IconButton id="icon-btn" color="primary" style={{ padding: '8px' }}>
        <FavoriteIcon style={{width: 35, height: 35, fill: "currentColor"}} />
      </IconButton>
  );
}
"""

IconComponent()
```

Import map entries are global to the page, so two components that map the same icon to different URLs conflict. Keep the URL for each icon identical across your components.

## Summary

Hopefully, this has given you a good introduction to building custom Material UI components using Panel. The `MaterialUIComponent` class not only allows you to build custom components leveraging the powerful `@mui/material` library, but handles theming and styling out of the box and lets you extend it by importing additional libraries to add completely novel functionality.

## Distributing Your Extension

Once your custom component is ready to share, you can package it as a proper Python extension. See [**Publish a Panel Extension**](https://panel.holoviz.org/how_to/custom_components/publish_extension.html) in the Panel docs for an overview of packaging extensions using the Panel Extension Copier Template.

For examples of published extensions built on this pattern, browse the [**panel-extensions**](https://github.com/orgs/panel-extensions/repositories) organisation on GitHub.
