# Inspiration: https://demos.creative-tim.com/material-dashboard/pages/dashboard
# docs: https://holoviz-dev.github.io/panel-material-ui/
# panel serve examples/apps/dashboard/*.py --index dashboard --dev
import panel_material_ui as pmu
import panel as pn

pn.extension()


show_dashboard = pmu.widgets.Button(name="Dashboard", icon="dashboard", sizing_mode="stretch_width", button_style="text", margin=(0,10), href="dashboard")
show_tables = pmu.widgets.Button(name="Tables", icon="table_view", sizing_mode="stretch_width", button_style="text", margin=(0,10), href="tables")
show_notifactions = pmu.widgets.Button(name="Notifications", icon="notifications", sizing_mode="stretch_width", button_style="text", margin=(0,10), href="notifications")

info = """\
Created with: [Panel Material UI](https://holoviz-dev.github.io/panel-material-ui/)

Inspired by: [Creative Tim Dashboard](https://demos.creative-tim.com/material-dashboard/pages/dashboard)\
"""

sidebar = pmu.Column(
    "#### <img style='margin-bottom: -10px;margin-right: 10px;margin-left:5px;' src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAcCAMAAABF0y+mAAAAM1BMVEUAcrUBd7jk6OuoxdsAcrUAbLP08vAAbbUAdLUAcrVQnMm6z99+rM86jcJ5sNElhL10qc1QLvfMAAAACnRSTlPP////////KCjO4FwxLQAAAJNJREFUKJGNktEShCAIRRXCCrX2/792aaYU3YXpTDM+nMQLGtawGIQtmE6s48S+kkRkSBEHMim6rMyYAA7u1EdSTj9kenYWRPGQsVNaWTnjxFzifGhvJbbcTp+V4yCj4gOA19rSImgkmvxAf2Ua5Vw267Ij5xTIbcUdgjc+f/DelenLXu5vTGs/EwNfuo963S23b1+vug28mwd6wAAAAABJRU5ErkJggg=='></img>Creative Panel",
    pmu.layout.Divider(sizing_mode="stretch_width", margin=(10,5,10,5)),
    show_dashboard,
    show_tables,
    show_notifactions,
    pmu.layout.Divider(sizing_mode="stretch_width", margin=(10,5,10,5)),
    info,
    styles={"background": "white", "border-radius": "5px", "margin": "10px"},
    width=300,
    sizing_mode="stretch_height",
)

bread_crumbs = pmu.menus.Breadcrumbs(name='Breadcrumbs test', items=['Pages', 'Dashboard'], align="center")
search = pmu.widgets.TextInput(name="Type here...", placeholder="Search", size="small")
goto_online_pmu = pmu.widgets.Button(name="Panel Material UI", variant="outlined", href="https://panel.holoviz.org")

action_row = pn.Row(bread_crumbs, pn.Spacer(sizing_mode="stretch_width"), search, goto_online_pmu, sizing_mode="stretch_width", )

main = pn.Column(action_row, sizing_mode="stretch_width", styles={"background": "lightgray"}, margin=10)

body = pmu.Column(
    pn.Row(sidebar,main),
    sizing_mode="stretch_both",
    styles={"background": "#f5f5f5", "width": "100vw"}, # Hack
).servable(title="Dashboard")



