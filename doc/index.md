# Panel Material UI

Welcome to Panel Material UI – a library that brings the sleek design and comprehensive component set of [Material UI](https://mui.com/material-ui/) into the world of Panel.

:::{raw} html
<iframe id="demo-iframe" src="_static/demo.html" width="100%" height="800px" style="border: none;"></iframe>
<script>
  const iframe = document.getElementById("demo-iframe")
  const theme = document.documentElement.dataset.theme
  iframe.src = `_static/demo.html?theme=${theme}`
</script>
:::

## Why Panel Material UI?

- **Consistent Look & Feel**
  Panel Material UI leverages Material UI’s design principles to give your Panel dashboards and applications a modern, cohesive style.

- **Easy Theming & Styling**
  Take control of your UI using Material UI’s theming concepts. Customize colors, typography, spacing, and more with minimal configuration. Quickly modify styling for one-off situations using the sx parameter or create global overrides via theme_config.

- **Seamless Dark Mode**
  Effortlessly toggle between light and dark palettes. Whether you want a permanently dark dashboard, a user-driven switch, or to match the system preference, Panel Material UI has you covered.

- **Familiar Panel API**
All components provide a similar API to native Panel widgets, ensuring a smooth developer experience. Pass parameters, bind widgets to reactive functions, and lay them out using Panel’s layout system.

- **Rich Component Set**
Access a growing collection of Material UI–inspired components (Buttons, Sliders, Cards, Dialogs, and more), all adapted to work with Panel. Spend less time building UI from scratch and more time showcasing your data.

- **Powerful Theming Inheritance**
  Define a theme at a parent level and let it automatically apply to child components without extra configuration, reducing repetitive code while maintaining consistent branding.

## Disclaimer

Panel Material UI is a relatively new project, having been first released in May 2025. As with any young project, there may be some growing pains as we continue to develop and improve the library.

We are actively using this library in production environments, which means you can expect regular updates and improvements. Our team is committed to addressing any issues that arise promptly, ensuring a stable and reliable experience for all users.

We appreciate your understanding and support as we work to make Panel Material UI the best it can be!

## Getting Started

Install Panel Material UI

:::::{tab-set}

::::{tab-item} pip
:sync: pip

```bash
pip install panel_material_ui
```

::::

::::{tab-item} conda
:sync: conda

```bash
conda install -c conda-forge panel_material_ui
```

::::

:::::

Then [discover the components](components/index) and [customization options](customization/index) available in Panel Material UI or build your own [custom components](custom).

```{toctree}
:titlesonly:
:hidden:
:maxdepth: 2
:caption: FOR USERS

reference/index
customization/index
custom
```
