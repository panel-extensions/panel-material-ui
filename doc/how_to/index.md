# How-To

Welcome to the **Panel Material UI** how-to guides. These guides walk you through:

- Fine-tuning **component-level** styles using `sx`, class names, and reusable components
- Applying **global theming** or **palette** overrides for consistent branding
- Leveraging **dark mode** to match user preferences or enforce a specific look
- Working with the **Material Design color system** to craft vibrant, accessible UIs

---

::::{grid} 1 2 2 3
:gutter: 1 1 1 2

:::{grid-item-card} {octicon}`tools;2.5em;sd-mr-1` How to Customize
:link: customize
:link-type: doc

Explore the fundamentals of customizing **panel-material-ui** components. Learn one-off styling with `sx`, overriding nested elements, global CSS overrides, and theme inheritance.

+++
[Learn more »](how_to_customize)
:::

:::{grid-item-card} {octicon}`list-unordered;2.5em;sd-mr-1` Palette
:link: palette
:link-type: doc

Customize the default primary, secondary, and intent-based colors. Set up advanced palette configurations including custom tokens and color schemes.

+++
[Learn more »](palette)
:::

:::{grid-item-card} {octicon}`typography;2.5em;sd-mr-1` Typography
:link: typography
:link-type: doc

Learn how to customize fonts, sizes, and text styles.

+++
[Learn more »](typography)
:::

:::{grid-item-card} {octicon}`apps;2.5em;sd-mr-1` Themed Components
:link: components
:link-type: doc

Customize components changing default props, styles, or adding new variants—by defining a `components` key within your `theme_config`..

+++
[Learn more »](components)
:::

:::{grid-item-card} {octicon}`moon;2.5em;sd-mr-1` Dark Mode
:link: dark_mode
:link-type: doc

Seamlessly toggle between light and dark palettes, or enforce one mode across your application. Perfect for low-light usage and user preference support.

+++
[Learn more »](dark_mode)
:::

:::{grid-item-card} {octicon}`paintbrush;2.5em;sd-mr-1` Color
:link: color
:link-type: doc

Dive into the Material Design color system. Create harmonious palettes, pick accessible shades, and apply them to your Panel components.

+++
[Learn more »](color)
:::

:::{grid-item-card} {octicon}`image;2.5em;sd-mr-1` Icons
:link: icons
:link-type: doc

Learn how to use icons in **panel-material-ui**.

+++
[Learn more »](icons)
:::

:::{grid-item-card} {octicon}`code;2.5em;sd-mr-1` Custom Components
:link: custom
:link-type: doc

Learn how to build custom components extending **panel-material-ui**.

+++
[Learn more »](custom)
:::

::::

## Integrations

Discover **panel-material-ui** integrates with different libraries to create beautiful, theme-aware plots, tables and more.

::::{grid} 1 2 2 3
:gutter: 1 1 1 2

:::{grid-item-card} {octicon}`project;2.5em;sd-mr-1` Bokeh, hvPlot and HoloViews
:link: bokeh_holoviews
:link-type: doc

Integrate **panel-material-ui** with **Bokeh**, **hvPlot** and **HoloViews** to create beautiful, theme-aware plots.

+++
[Learn more »](bokeh_holoviews)
:::

::::


## Where to go next?

- If you’re new to **Panel**, check out the [Getting Started](https://panel.holoviz.org/getting_started/index.html) guides to learn the basics.
- Already confident with Panel? Dive deeper into advanced theming and usage within these customization guides, or reference [Material UI’s design principles](https://mui.com/) for additional inspiration.

```{toctree}
:titlesonly:
:hidden:
:maxdepth: 2

customize
palette
typography
components
dark_mode
color
icons
bokeh_holoviews
```
