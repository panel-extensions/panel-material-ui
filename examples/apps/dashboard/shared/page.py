import panel as pn
import panel_material_ui as pmu
from shared.components import create_menu
from shared.config import CARD_STYLES, BODY_STYLES


def create_sidebar(name: str):
    documentation_link = pmu.widgets.Button(
        name="Documentation",
        variant="outlined",
        href="https://holoviz-dev.github.io/panel-material-ui/",
    )
    reference_link = pmu.widgets.Button(
        name="Reference",
        variant="contained",
        href="https://demos.creative-tim.com/material-dashboard/pages/dashboard",
        color="dark",
    )

    return pmu.Column(
        "#### <img style='margin-bottom: -10px;margin-right: 10px;margin-left:5px;' src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAM1BMVEUAcrUBd7jk6OuoxdsAcrUAbLP08vAAbbUAdLUAcrVQnMm6z99+rM86jcJ5sNElhL10qc1QLvfMAAAACnRSTlPP////////KCjO4FwxLQAAAJNJREFUKJGNktEShCAIRRXCCrX2/792aaYU3YXpTDM+nMQLGtawGIQtmE6s48S+kkRkSBEHMim6rMyYAA7u1EdSTj9kenYWRPGQsVNaWTnjxFzifGhvJbbcTp+V4yCj4gOA19rSImgkmvxAf2Ua5Vw267Ij5xTIbcUdgjc+f/DelenLXu5vTGs/EwNfuo963S23b1+vug28mwd6wAAAAABJRU5ErkJggg=='></img>Creative Panel",
        pmu.layout.Divider(sizing_mode="stretch_width", margin=(10, 5, 10, 5)),
        create_menu(name),
        pn.Spacer(sizing_mode="stretch_height"),
        documentation_link,
        reference_link,
        styles={"background": "white", "border-radius": "5px", "margin": "10px"},
        width=300,
        sizing_mode="stretch_height",
    )


def create_context():
    return pn.Column(
        "#### Material UI Configurator",
        pn.Spacer(sizing_mode="stretch_height"),
        width=300,
        margin=10,
        styles=CARD_STYLES,
        visible=True,
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
    github_star_count = pn.panel(
        """\
    <a href="https://github.com/panel-extensions/panel-material-ui">
        <img height="20" src="https://img.shields.io/github/stars/panel-extensions/panel-material-ui?style=social" alt="GitHub stars">
    </a>\
    """,
        align="center",
    )
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
    return pn.Row("© 2025, made with by **panel-material-ui** for beautiful data apps.")


def create_fab():
    fab_button = pmu.widgets.ButtonIcon(
        icon="settings", color="dark", size="2em", description="Toggle settings drawer"
    )
    return pn.Row(pn.Spacer(sizing_mode="stretch_width"), fab_button)


def create_page(name: str, main: list):
    sidebar = create_sidebar(name=name)

    context = create_context()

    def toggle_context(event):
        context.visible = not context.visible

    header = create_header(name=name, settings_callback=toggle_context)

    footer = create_footer()
    fab_row = create_fab()
    main = pn.Column(
        header,
        *main,
        pn.Spacer(sizing_mode="stretch_height"),
        footer,
        pmu.layout.Divider(sizing_mode="stretch_width", margin=5),
        fab_row,
        sizing_mode="stretch_width",
        margin=10,
    )

    return pmu.Column(
        pn.Row(sidebar, main, context),
        sizing_mode="stretch_both",
        styles=BODY_STYLES,
    )
