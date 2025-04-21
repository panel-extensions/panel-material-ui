import panel as pn
import panel_material_ui as pmu
from shared.components import create_menu
from shared.config import PAPER_STYLES, BODY_STYLES, PageSettings


def create_sidebar(name: str, button_color, settings: PageSettings):
    documentation_link = pmu.widgets.Button(
        name="Documentation",
        variant="outlined",
        href="https://holoviz-dev.github.io/panel-material-ui/",
        sizing_mode="stretch_width",
    )
    reference_link = pmu.widgets.Button(
        name="Reference",
        variant="contained",
        href="https://demos.creative-tim.com/material-dashboard/pages/dashboard",
        color="dark",
        sizing_mode="stretch_width",
    )

    return pmu.Column(
        "#### <img style='margin-bottom: -10px;margin-right: 10px;margin-left:5px;' src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAM1BMVEUAcrUBd7jk6OuoxdsAcrUAbLP08vAAbbUAdLUAcrVQnMm6z99+rM86jcJ5sNElhL10qc1QLvfMAAAACnRSTlPP////////KCjO4FwxLQAAAJNJREFUKJGNktEShCAIRRXCCrX2/792aaYU3YXpTDM+nMQLGtawGIQtmE6s48S+kkRkSBEHMim6rMyYAA7u1EdSTj9kenYWRPGQsVNaWTnjxFzifGhvJbbcTp+V4yCj4gOA19rSImgkmvxAf2Ua5Vw267Ij5xTIbcUdgjc+f/DelenLXu5vTGs/EwNfuo963S23b1+vug28mwd6wAAAAABJRU5ErkJggg=='></img>Panel Material UI",
        pmu.layout.Divider(sizing_mode="stretch_width", margin=(10, 5, 10, 5)),
        create_menu(name, button_color=button_color),
        pn.Spacer(sizing_mode="stretch_height"),
        documentation_link,
        reference_link,
        styles=settings.sidebar_styles,
        width=300,
        sizing_mode="stretch_height",
    )


def create_github_star_count():
    return pn.panel(
        """\
    <a href="https://github.com/panel-extensions/panel-material-ui">
        <img height="20" src="https://img.shields.io/github/stars/panel-extensions/panel-material-ui?style=social" alt="GitHub stars">
    </a>\
    """,
        align="center",
    )

def create_context(settings: PageSettings):
    buttons = [pmu.widgets.Button(name=name, variant="outlined", color="dark") for name in settings.param.sidebar_background_color.objects]
    def update_buttons(buttons=buttons):
        for but in buttons:
            but.variant = "contained" if but.name==settings.sidebar_background_color else "outlined"
    update_buttons()

    def click(event, buttons=buttons):
        button = event.obj
        settings.sidebar_background_color=button.name
        update_buttons()
    [button.on_click(click) for button in buttons]


    return pmu.Drawer(
        pn.Column(
            "## Material UI Configurator",
            pmu.widgets.RadioBoxGroup.from_param(settings.param.sidebar_button_color),
            """### Sidenav Type

Choose between different sidenav types.""",
            pn.Row(*buttons, align="center"),
            pmu.layout.Divider(sizing_mode="stretch_width", margin=5, min_width=500),
            pmu.Switch.from_param(settings.param.dark_theme, name="Light/ Dark", disabled=True),
            pmu.layout.Divider(sizing_mode="stretch_width", margin=5),
            pmu.widgets.Button(name="Free Download", href="https://github.com/panel-extensions/panel-material-ui", color="primary", variant="contained", sizing_mode="stretch_width"),
            pmu.widgets.Button(name="Documentation", href="https://holoviz-dev.github.io/panel-material-ui/", variant="outlined", sizing_mode="stretch_width"),
            create_github_star_count(),
            pn.pane.Markdown("## Thank you for sharing!", align="center"),
            pn.Row(
                pmu.widgets.Button(name="Tweet", href="https://twitter.com/intent/tweet?text=Check%20Panel%20Material%20UI%20Dashboard%20made%20by%20%40HoloViz%20%23webdesign%20%23dashboard%20%23dataviz&url=https%3A%2F%2Fholoviz-dev.github.io%2Fpanel-material-ui%2F", color="dark", variant="contained"),
                pmu.widgets.Button(name="Share", href="https://www.facebook.com/sharer/sharer.php?u=https://holoviz-dev.github.io/panel-material-ui", color="dark", variant="contained"),
                align="center"
            ),
            sizing_mode="fixed", width=400,
        ),
        anchor="right",
    )



def create_header(name: str, settings_callback):
    bread_crumbs = pmu.menus.Breadcrumbs(
        name="Breadcrumbs test", items=["Pages", name], align="center"
    )
    search = pmu.widgets.TextInput(
        name="Type here...", placeholder="Search", size="small"
    )
    goto_online_pmu = pmu.widgets.Button(
        name="Panel Material UI",
        variant="outlined",
        color="info",
        href="https://panel.holoviz.org",
        align="center",
    )
    github_star_count = create_github_star_count()
    settings_button = pmu.widgets.ButtonIcon(
        name="Context", icon="settings", align="center", on_click=settings_callback
    )

    return pn.Row(
        bread_crumbs,
        pn.Spacer(sizing_mode="stretch_width"),
        search,
        goto_online_pmu,
        github_star_count,
        settings_button,
        sizing_mode="stretch_width",
    )


def create_footer():
    return pn.Row(
        "© 2025, made with by **panel-material-ui** for beautiful data apps.",
        pn.Spacer(sizing_mode="stretch_width"),
        pmu.widgets.Button(
            name="Panel Material UI",
            variant="text",
            href="https://panel-extensions.github.io/panel-material-ui/",
        ),
        pmu.widgets.Button(
            name="About Us",
            variant="text",
            href="https://panel.holoviz.org",
        ),
        pmu.widgets.Button(
            name="Blog",
            variant="text",
            href="https://blog.holoviz.org/",
        ),
        pmu.widgets.Button(
            name="License",
            variant="text",
            href="https://panel-extensions.github.io/panel-material-ui/LICENSE.md",
        )
    )


def create_fab(settings_callback):
    sx ={
        "position": 'fixed',
        "bottom": 16,
        "right": 16,
    }
    fab_button = pmu.Fab(color='light', label='Click me', icon="settings", size="large", description="Toggle settings drawer", on_click=settings_callback, sx=sx)
    return fab_button


def create_page(name: str, main: list):
    settings = PageSettings()

    sidebar = create_sidebar(name=name, button_color=settings.param.sidebar_button_color, settings=settings)

    context = create_context(settings=settings)

    def toggle_drawer(event):
        context.open = not context.open

    header = create_header(name=name, settings_callback=toggle_drawer)

    footer = create_footer()
    fab_row = create_fab(settings_callback=toggle_drawer)
    main = pn.Column(
        header,
        *main,
        pn.Spacer(sizing_mode="stretch_height"),
        footer,
        pmu.layout.Divider(sizing_mode="stretch_width", margin=5),
        pn.Spacer(height=50, sizing_mode="stretch_width"),
        fab_row,
        sizing_mode="stretch_width",
        margin=10,
    )

    return pmu.Column(
        pn.Row(sidebar, main, context),
        sizing_mode="stretch_both",
        styles=BODY_STYLES,
    )
