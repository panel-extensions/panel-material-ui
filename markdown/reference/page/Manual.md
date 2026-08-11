```python
import math

import panel as pn
from panel_material_ui import (
    Column, Container, Drawer, Paper, ButtonIcon, ThemeToggle,
    Typography, ToggleIcon, Row, Pagination, Grid
)

pn.extension()
```

In addition to the `Page` component, Material components like `Container`, `Paper`, and others can be combined to manually define the layout of an application.
These building blocks provide more granular control over structure, spacing, and visual hierarchy when you need a fully custom page design.

In this reference guide we will discover a few ways we can use these components to generate a page-like layout.


```python
LOREM_IPSUM = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
minim veniam, quis nostrud exercitation ullamco laboris nisi ut
aliquip ex ea commodo consequat. Duis aute irure dolor in
reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.
"""

def generate_pages(text: str, chars_per_page: int, num_pages: int) -> list[str]:
    total_chars_needed = chars_per_page * num_pages
    repeats = math.ceil(total_chars_needed / len(text))
    full_text = text * repeats
    return [
        full_text[i*chars_per_page : (i+1)*chars_per_page]
        for i in range(num_pages)
    ]
```

### Building a Custom Layout with `Container` and `Paper`

When manually designing a page, two key Material components often form the foundation: `Container` and `Paper`. The `Container` sets the overall width, margins, and centering for your content, while the `Paper` provides a surface with padding, elevation, and layout flexibility inside the container.

In this example, we start by wrapping the entire layout inside a `Container`, which centers the content and constrains its width with `width_option='sm'`.
Inside the container, a `Paper` component acts as the main surface of the application — giving the content a card-like feel, adding padding (`sx={"p": "1rem"}`), and stretching to fill the available height and width.


```python
title = Typography('Lorem Ipsum', variant='h3', margin=(20, 30))
sidebar = Drawer('# Drawer', anchor='right', variant='temporary', size=300)
toggles = Row(
    ThemeToggle(),
    sidebar.create_toggle(),
    styles={'position': 'absolute', 'top': "0", 'right': "0"}
)
pages = generate_pages(LOREM_IPSUM, 1000, 99)
pagination = Pagination(count=99, align=('center', 'end'), styles={'marginTop': "auto"})

Container(
    Paper(
        title,
        toggles,
        sidebar,
        pn.rx(pages)[pagination],
        pagination,
        elevation=3,
        sizing_mode='stretch_both',
        sx={"p": "1rem"}
    ),
    margin=(10, 0),
    height=580,
    width_option='sm'
).preview(sizing_mode='stretch_width', height=600)
```

Within the `Paper`, we arrange the individual UI elements:

- A `Typography` component displays the title, styled with custom margins.
- A `Row` positions the theme toggle and sidebar toggle buttons absolutely in the top-right corner.
- A `Drawer` provides a collapsible sidebar anchored to the right side.
- The main content is a set of paginated pages, dynamically generated and linked to a `Pagination` control at the bottom.

By combining `Container` and `Paper`, you can quickly establish a clean, responsive base for your application — layering in more interactive components as needed while maintaining full control over layout and styling.

## Building a Dashboard layout with `Grid` and `Drawer`

This example builds a simple dashboard layout by combining a persistent `Drawer`, a title, a `Grid` for the main content, and floating toggle controls.

- A `Drawer` is anchored to the left side of the page, using `variant='persistent'` so it pushes the content when open instead of overlaying it. It is styled with padding to align its content below the fixed title.
- A `Typography` component displays the dashboard title, positioned with a left margin to avoid overlap with the drawer.
- The main content is arranged in a `Grid`, with two charts placed side-by-side on medium and larger screens (`md=6` each) and stacked on smaller screens (`xs=12`), followed by a full-width chart.
- Each chart is wrapped in a `Paper` component to provide padding, elevation, and a consistent card-like appearance.
- A `ThemeToggle` and a drawer toggle button are positioned absolutely in the top-right corner for easy access, without affecting the flow of the main layout.
- The overall layout is built with a `Row`, placing the `Drawer` beside the main content and the floating controls.

This structure keeps the layout responsive, clean, and modular, while giving the user control over both theme and sidebar visibility.


```python
title = Typography("My Dashboard", variant="h4", margin=(0, 0, 0, 50))

drawer = Drawer(
    Typography("I'm in a Drawer!", variant="h6"),
    variant="persistent",
    anchor="left",
    styles={"height": "100%"},
    sx={"paddingTop": "50px"}
)

theme_toggle = ThemeToggle(styles={"position": "fixed", "right": "0", "zIndex": "10001"})

render_content = lambda text: Paper(Typography(text, variant='h6'), elevation=2, sx={"p": "1rem"}, sizing_mode="stretch_both")

grid = Grid(
    Grid(
        render_content("Chart 1"),
        size={"md": 6, "xs": 12}
    ),
    Grid(
        render_content("Chart 2"),
        size={"md": 6, "xs": 12}
    ),
    Grid(
        render_content("Chart 3"),
        size={"md": 12, "xs": 12}
    ),
    container=True,
    column_spacing=2,
    row_spacing=2,
    sizing_mode='stretch_both',
    margin=(0, 20, 20, 20)
)

main = Column(title, grid)

toggle = drawer.create_toggle(styles={"position": "fixed", "zIndex": "10001"})

Row(
    drawer,
    main,
    theme_toggle,
    toggle,
    sizing_mode="stretch_width"
).preview(sizing_mode='stretch_width')
```

## Building an App Layout with `AppBar`

The `AppBar` component provides a ready-made top navigation bar that can contain a title, icon, and arbitrary child components like buttons and menus. Combined with other layout components it serves as the header of a full application.

In this example we combine an `AppBar` with a `MenuBar` for navigation, a `Drawer` for a sidebar, and paginated content in the main area.


```python
from panel_material_ui import AppBar, MenuBar, Button

menu = MenuBar(
    items=[
        {'label': 'File', 'items': [
            {'label': 'New', 'icon': 'note_add', 'hint': 'Ctrl+N'},
            {'label': 'Open', 'icon': 'folder_open', 'hint': 'Ctrl+O'},
            None,
            {'label': 'Save', 'icon': 'save', 'hint': 'Ctrl+S'},
        ]},
        {'label': 'Edit', 'items': [
            {'label': 'Undo', 'icon': 'undo'},
            {'label': 'Redo', 'icon': 'redo'},
        ]},
        {'label': 'View', 'items': [
            {'label': 'Zoom In', 'icon': 'zoom_in'},
            {'label': 'Zoom Out', 'icon': 'zoom_out'},
        ]},
    ],
    sx={'border': 'none', 'boxShadow': 'none', 'background': 'transparent', 'color': 'white'},
    margin=(15, 0, 0, 0)
)

drawer = Drawer(
    Typography("Sidebar", variant="h6"),
    Typography("Navigation and tools go here."),
    variant="persistent",
    anchor="left",
    size=250,
    sx={"paddingTop": "60px", "zIndex": 1}
)

appbar = AppBar(
    menu,
    ThemeToggle(styles={"margin-left": "auto"}),
    drawer_toggle=drawer.create_toggle(sx={".MuiIcon-root": {"color": "white"}}),
    title='My Application',
    icon='nature',
    sizing_mode="stretch_width",
    styles={"z-index": "999"}
)

pages = generate_pages(LOREM_IPSUM, 800, 10)
pagination = Pagination(count=10, align=('center', 'end'), styles={'marginTop': 'auto'})

main = Container(
    Paper(
        pn.rx(pages)[pagination],
        pagination,
        elevation=1,
        sx={"p": "1.5rem", "m": "1em 0"},
        sizing_mode='stretch_both',
    )
)

Column(
    appbar,
    Row(drawer, main, sizing_mode='stretch_both'),
    sizing_mode='stretch_width',
    height=500,
).preview(sizing_mode='stretch_width', height=520)
```

The `AppBar` handles the top-level header concerns (title, icon, color theming) while the child components inside it provide the interactive elements. This pattern scales well: you can add search fields, avatar menus, notification badges, or any other widget as children of the AppBar.

These are just a few ways in which components can be combined to create a custom application layout.
