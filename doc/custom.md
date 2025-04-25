# Custom Material UI Components

The `panel-material-ui` package ships with a number of custom Material UI components that are built on top of the Material UI library. However in some cases you may need to create your own custom components.

The `MaterialUIComponent` provides a convenient entrypoint for building custom Material UI components using Panel, that will inherit the functionality of `panel-material-ui` while building on the existing JS bundle.

To understand the basics of about building custom components in Panel, see the documentation for the [ReactComponent](https://panel.holoviz.org/reference/custom_components/ReactComponent.html), which the `MaterialUIComponent` is built on top of.

## What we are making?

Let’s build something delightfully colorful: a `RainbowButton` that cycles through the colors of the rainbow when you hover or click it! You’ll get hands-on practice with:

- Subclassing `panel_material_ui.MaterialUIComponent`
- Defining `Param` properties for the Python side
- Wiring up React state and hooks in your `.jsx`

### The Python Side

First we need to define the `RainbowButton` class, which subclasses `MaterialUIComponent`.

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
```

Here we:

- Subclass `MaterialUIComponent`
- Define five parameters: `label`, `size`, `mode`, `interval`, and `colors`
- Point at our React file `RainbowButton.jsx`

### The React Side

Now we need to create the React component that will be used to render the `RainbowButton`. As with all ESM components, we need to export a `render` function that takes a `model` argument.

```jsx
import Button from "@mui/material/Button";

export function render({model}) {
  // Sync Python params into React state
  const [label]    = model.useState("name");
  const [size]     = model.useState("size");
  const [mode]     = model.useState("mode");
  const [interval] = model.useState("interval");

  // Internal state: current color index
  const [index, setIndex] = React.useState(0);

  // Function to advance the color
  const nextColor = () => (
    setIndex(i => (i + 1) % model.colors.length)
  );

  // On “click” mode, cycle once per click
  const handleClick = () => {
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

  const currentColor = model.colors[index];

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

- We pull in the Python params via `model.useState(...)`
- We maintain our own index to track which color we’re on
- Two modes:
  - `hover`: start a setInterval on enter, clear it on leave
  - `click`: advance once per click
- We style the MUI `<Button>` using the current rainbow color

## Usage

To see what we have built in action, let's quickly put it all together. We will inline ESM code in the Python side and render it:

```{pyodide}
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

    _esm_base = """
import Button from "@mui/material/Button";

export function render({model}) {
  // Sync Python params into React state
  const [label]    = model.useState("name");
  const [size]     = model.useState("size");
  const [mode]     = model.useState("mode");
  const [interval] = model.useState("interval");

  // Internal state: current color index
  const [index, setIndex] = React.useState(0);

  // Function to advance the color
  const nextColor = () => (
    setIndex(i => (i + 1) % model.colors.length)
  );

  // On “click” mode, cycle once per click
  const handleClick = () => {
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

  const currentColor = model.colors[index];

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


RainbowButton(name="Unicorn Power!", mode="hover", interval=150)
```

Give it a try, hover over the button to see it cycle through the rainbow colors!

## Summary

Hopefully this has given you a good introduction to building custom Material UI components using Panel.
