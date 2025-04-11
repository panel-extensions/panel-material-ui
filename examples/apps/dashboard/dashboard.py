# Inspiration: https://demos.creative-tim.com/material-dashboard/pages/dashboard
# docs: https://holoviz-dev.github.io/panel-material-ui/
# panel serve examples/apps/dashboard/*.py --index dashboard --dev
import panel_material_ui as pmu
import panel as pn
import param

pn.extension(design="material")

CARD_STYLES = {"background": "white", "border-radius": "5px"}


show_dashboard = pmu.widgets.Button(name="Dashboard", icon="dashboard", sizing_mode="stretch_width", button_style="text", margin=(0,10), href="dashboard")
show_tables = pmu.widgets.Button(name="Tables", icon="table_view", sizing_mode="stretch_width", button_style="text", margin=(0,10), href="tables")
show_notifactions = pmu.widgets.Button(name="Notifications", icon="notifications", sizing_mode="stretch_width", button_style="text", margin=(0,10), href="notifications")

documentation_link = pmu.widgets.Button(name="Documentation", variant="outlined", href="https://holoviz-dev.github.io/panel-material-ui/")
reference_link = pmu.widgets.Button(name="Reference", variant="contained", href="https://demos.creative-tim.com/material-dashboard/pages/dashboard", color="dark")

sidebar = pmu.Column(
    "#### <img style='margin-bottom: -10px;margin-right: 10px;margin-left:5px;' src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAM1BMVEUAcrUBd7jk6OuoxdsAcrUAbLP08vAAbbUAdLUAcrVQnMm6z99+rM86jcJ5sNElhL10qc1QLvfMAAAACnRSTlPP////////KCjO4FwxLQAAAJNJREFUKJGNktEShCAIRRXCCrX2/792aaYU3YXpTDM+nMQLGtawGIQtmE6s48S+kkRkSBEHMim6rMyYAA7u1EdSTj9kenYWRPGQsVNaWTnjxFzifGhvJbbcTp+V4yCj4gOA19rSImgkmvxAf2Ua5Vw267Ij5xTIbcUdgjc+f/DelenLXu5vTGs/EwNfuo963S23b1+vug28mwd6wAAAAABJRU5ErkJggg=='></img>Creative Panel",
    pmu.layout.Divider(sizing_mode="stretch_width", margin=(10,5,10,5)),
    show_dashboard,
    show_tables,
    show_notifactions,
    pn.Spacer(sizing_mode="stretch_height"),
    documentation_link,
    reference_link,
    styles={"background": "white", "border-radius": "5px", "margin": "10px"},
    width=300,
    sizing_mode="stretch_height",
)

bread_crumbs = pmu.menus.Breadcrumbs(name='Breadcrumbs test', items=['Pages', 'Dashboard'], align="center")
search = pmu.widgets.TextInput(name="Type here...", placeholder="Search", size="small")
goto_online_pmu = pmu.widgets.Button(name="Panel Material UI", variant="outlined", color="info", href="https://panel.holoviz.org", align="center")
github_star_count = pn.pane.HTML("""\
<a href="https://github.com/panel-extensions/panel-material-ui">
    <img height="20" src="https://img.shields.io/github/stars/panel-extensions/panel-material-ui?style=social" alt="GitHub stars">
</a>\
""", align="center")
settings_button = pmu.widgets.ButtonIcon(name="Context", icon="settings", align="center")

action_row = pn.Row(bread_crumbs, pn.Spacer(sizing_mode="stretch_width"), search, goto_online_pmu, github_star_count, settings_button, sizing_mode="stretch_width")

fab_button = pmu.widgets.ButtonIcon(icon="settings", color="dark", size="2em", description="Toggle settings drawer")

footer = pn.Row("© 2025, made with by **[panel-material-ui](https://holoviz-dev.github.io/panel-material-ui/)** for beautiful data apps.")
fab_row = pn.Row(pn.Spacer(sizing_mode="stretch_width"), fab_button)
main = pn.Column(action_row, pn.Spacer(sizing_mode="stretch_height"), footer, pmu.layout.Divider(sizing_mode="stretch_width", margin=5), fab_row, sizing_mode="stretch_width", margin=10)
context = pn.Column("#### Material UI Configurator", width=300, margin=10, styles=CARD_STYLES, visible=False)

def toggle_context(event):
    context.visible=not context.visible

settings_button.on_click(toggle_context)

body = pmu.Column(
    pn.Row(sidebar,main, context),
    sizing_mode="stretch_both",
    styles={"background": "#f5f5f5", "width": "100vw"}, # Hack
).servable(title="Dashboard")



