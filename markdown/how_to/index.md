# How-To

Welcome to the **Panel Material UI** how-to guides. These guides walk you through:

- Fine-tuning **component-level** styles using `sx`, class names, and reusable components
- Applying **global theming** or **palette** overrides for consistent branding
- Leveraging **dark mode** to match user preferences or enforce a specific look
- Working with the **Material Design color system** to craft vibrant, accessible UIs

---

::::{grid} 1 2 2 3
:gutter: 1 1 1 2

:::{grid-item-card} {octicon}`tools;2.5em;sd-mr-1` Customize Themes & Styles
:link: customize_themes_and_styles
:link-type: doc

Explore the fundamentals of customizing **panel-material-ui** components. Learn one-off styling with `sx`, overriding nested elements, global CSS overrides, and theme inheritance.

+++
[Learn more »](customize_themes_and_styles)
:::

:::{grid-item-card} {octicon}`list-unordered;2.5em;sd-mr-1` Customize Color Palettes
:link: customize_palette
:link-type: doc

Customize the default primary, secondary, and intent-based colors. Set up advanced palette configurations including custom tokens and color schemes.

+++
[Learn more »](customize_palette)
:::

:::{grid-item-card} {octicon}`typography;2.5em;sd-mr-1` Customize Typography
:link: customize_typography
:link-type: doc

Learn how to customize fonts, sizes, and text styles.

+++
[Learn more »](customize_typography)
:::

:::{grid-item-card} {octicon}`apps;2.5em;sd-mr-1` Theme Components
:link: theme_components
:link-type: doc

Customize components changing default props, styles, or adding new variants—by defining a `components` key within your `theme_config`.

+++
[Learn more »](theme_components)
:::

:::{grid-item-card} {octicon}`moon;2.5em;sd-mr-1` Control Dark Mode
:link: control_dark_mode
:link-type: doc

Seamlessly toggle between light and dark palettes, or enforce one mode across your application. Perfect for low-light usage and user preference support.

+++
[Learn more »](control_dark_mode)
:::

:::{grid-item-card} {octicon}`paintbrush;2.5em;sd-mr-1` Pick Colors
:link: pick_colors
:link-type: doc

Dive into the Material Design color system. Create harmonious palettes, pick accessible shades, and apply them to your Panel components.

+++
[Learn more »](pick_colors)
:::

:::{grid-item-card} {octicon}`image;2.5em;sd-mr-1` Use Icons
:link: using_mui_icons
:link-type: doc

Learn how to use icons in **panel-material-ui**.

+++
[Learn more »](using_mui_icons)
:::

:::{grid-item-card} {octicon}`code;2.5em;sd-mr-1` Build Custom Components
:link: build_custom_components
:link-type: doc

Learn how to build custom components extending **panel-material-ui**.

+++
[Learn more »](build_custom_components)
:::

:::{grid-item-card} {octicon}`paintbrush;2.5em;sd-mr-1` Apply Branding
:link: apply_branding
:link-type: doc

Learn how to brand your **panel-material-ui** apps.

+++
[Learn more »](apply_branding)
:::

::::

## Integrations

Discover **panel-material-ui** integrates with different libraries to create beautiful, theme-aware plots, tables and more.

::::{grid} 1 2 2 3
:gutter: 1 1 1 2

:::{grid-item-card} {octicon}`project;2.5em;sd-mr-1` Theme Plotting Libraries
:link: theme_plotting_libraries
:link-type: doc

Integrate **panel-material-ui** with **Bokeh**, **hvPlot**, **HoloViews**, and **Plotly** to create beautiful, theme-aware plots.

+++
[Learn more »](theme_plotting_libraries)
:::

::::


## Where to go next?

- If you're new to **Panel**, check out the [Getting Started](https://panel.holoviz.org/getting_started/index.html) guides to learn the basics.
- Already confident with Panel? Dive deeper into advanced theming and usage within these customization guides, or reference [Material UI's design principles](https://mui.com/) for additional inspiration.

```{toctree}
:titlesonly:
:hidden:
:maxdepth: 2

customize_themes_and_styles
customize_palette
customize_typography
theme_components
control_dark_mode
pick_colors
using_mui_icons
build_custom_components
apply_branding
theme_plotting_libraries
```
