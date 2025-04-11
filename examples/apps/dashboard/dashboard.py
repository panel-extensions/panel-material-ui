# Inspiration: https://demos.creative-tim.com/material-dashboard/pages/dashboard
# docs: https://holoviz-dev.github.io/panel-material-ui/
# panel serve examples/apps/dashboard/*.py --index dashboard --dev
import panel_material_ui as pmu
import panel as pn
import param

CSS_RAW = """
.material-symbols-outlined {
    font-size: 12px;
}
"""

website_views_data = {"time": ["M", "T", "W", "T", "F", "S", "S"], "views": [50, 45, 30, 35, 50, 60, 75]}
website_views_data = {
    'xAxis': {
        'data': ["M", "T", "W", "T", "F", "S", "S"]
    },
    "tooltip": {
    "trigger": 'axis',
    "axisPointer": {
        "type": 'shadow'
        }
    },
    'yAxis': {},
    'series': [{
        'name': 'Views',
        'type': 'bar',
        'data': [50, 45, 30, 35, 50, 60, 75],
        'itemStyle': {
            'color': 'green'
        }
    }],
    'grid': {
        'top': 10,
        'bottom': 20,
    }
}

daily_sales = {
    'xAxis': {
        'type': 'category',
        'data': ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
    },
    'yAxis': {
        'type': 'value'
    },
    'series': [{
        'name': 'Monthly Data',
        'type': 'line',
        'data': [120, 132, 101, 134, 90, 230, 210, 180, 150, 200, 170, 250],
        'itemStyle': {
            'color': 'green'
        }
    }],
    'grid': {
        'top': 10,
        'bottom': 20,
    },
    "tooltip": {
    "trigger": 'axis',
    "axisPointer": {
        "type": 'shadow'
        }
    },
}
completed_tasks = {
    'xAxis': {
        'type': 'category',
        'data': ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    },
    'yAxis': {
        'type': 'value'
    },
    'series': [{
        'name': 'Monthly Data',
        'type': 'line',
        'data': [50, 50, 300, 210, 500, 230, 400, 230, 525],
        'itemStyle': {
            'color': 'green'
        }
    }],
    'grid': {
        'top': 10,
        'bottom': 20,
    },
    "tooltip": {
    "trigger": 'axis',
    "axisPointer": {
        "type": 'shadow'
        }
    },
}

pn.extension("echarts", design="material", css_files=["https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&icon_names=schedule,weekend"])

def create_dashboard_card(title, icon, value, change_percent, since):
    html = f"""

        <style>
            .card {{
                font-family: 'Roboto', sans-serif;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                padding: 16px;
                width: 100%;
                margin: 0xp;
                display: inline-block;
            }}

            .card-icon {{
                position: absolute;
                top: 16px;
                right: 16px;
                color: white;
                background-image: linear-gradient(195deg,#42424a,#191919);
                padding: 10px;
                margin: 3px;
                font-size: 16px;
                box-shadow: 0 4px 20px 0 rgba(0,0,0,.14),0 7px 10px -5px rgba(64,64,64,.4)!important;
                border-radius: .5rem;
            }}

            .card-title {{
                font-size: 14px;
                color: #888;
                margin-bottom: 8px;
            }}

            .card-value {{
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 8px;
                color: #344767;
            }}

            .card-footer {{
                font-size: 12px;
                color: #888;
            }}

            .change-positive {{
                color: #4caf50;
                font-weight: bold;
            }}

            .change-negative {{
                color: #f44336;
                font-weight: bold;
            }}
        </style>
        <div class="card">
            <span class='material-symbols-outlined card-icon'>{icon}</span>
            <div class="card-title">{title}</div>
            <div class="card-value">{value}</div>
            <div class="card-footer">
                <span class="{'change-positive' if change_percent >= 0 else 'change-negative'}">
                    {change_percent}%
                </span>
                &nbsp;{since}
            </div>
        </div>
    """
    return html

CARD_STYLES = {"background": "white", "border-radius": "5px", "border": "1px solid #e5e5e5", "box-shadow": "0 1px 2px 0 rgba(0,0,0,.05)"}

CLOCK_SVG = """<svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#1f1f1f"><path d="m614-310 51-51-149-149v-210h-72v240l170 170ZM480-96q-79.38 0-149.19-30T208.5-208.5Q156-261 126-330.96t-30-149.5Q96-560 126-630q30-70 82.5-122t122.46-82q69.96-30 149.5-30t149.55 30.24q70 30.24 121.79 82.08 51.78 51.84 81.99 121.92Q864-559.68 864-480q0 79.38-30 149.19T752-208.5Q700-156 629.87-126T480-96Zm0-384Zm.48 312q129.47 0 220.5-91.5Q792-351 792-480.48q0-129.47-91.02-220.5Q609.95-792 480.48-792 351-792 259.5-700.98 168-609.95 168-480.48 168-351 259.5-259.5T480.48-168Z"/></svg>"""

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
page_title = """\
## Dashboard

Check the sales, value and bounce rate by country.\
"""
def last_update(message):
    return pn.pane.HTML(f"<span class='material-symbols-outlined'>schedule</span> {message}", stylesheets=[CSS_RAW])

todays_money=pn.pane.HTML(create_dashboard_card("Today's Money", "weekend", "$53,000", 55, "since yesterday"), sizing_mode="stretch_width")
todays_users=pn.pane.HTML(create_dashboard_card("Today's Money", "weekend", "$53,000", 3, "since yesterday"), sizing_mode="stretch_width")
adds_views=pn.pane.HTML(create_dashboard_card("Today's Money", "weekend", "$53,000", -2, "since yesterday"), sizing_mode="stretch_width")
sales=pn.pane.HTML(create_dashboard_card("Today's Money", "weekend", "$53,000", 5, "since yesterday"), sizing_mode="stretch_width")
indicators = pn.Row(todays_money, todays_users, adds_views, sales)

web_site_views = pn.Column("#### Website Views\n\nLast Campaign Performance", pn.pane.ECharts(website_views_data, sizing_mode="stretch_width", height=250, margin=(0,5)), pn.Spacer(sizing_mode="stretch_height"), last_update("campaign sent 2 days ago"), sizing_mode="stretch_width", styles=CARD_STYLES, margin=10, height=400)
daily_sales = pn.Column("#### Daily Sales\n\n(**+15%**) increase in todays sales", pn.pane.ECharts(daily_sales, sizing_mode="stretch_width", height=250, margin=(0,5)), pn.Spacer(sizing_mode="stretch_height"), last_update("updated 4 min ago"), sizing_mode="stretch_width", styles=CARD_STYLES, margin=10, height=400)
completed_tasks = pn.Column("#### Completed Tasks\n\nLast Campaign Performance", pn.pane.ECharts(completed_tasks, sizing_mode="stretch_width", height=250, margin=(0,5)), pn.Spacer(sizing_mode="stretch_height"), last_update("just updated"), sizing_mode="stretch_width", styles=CARD_STYLES, margin=10, height=400)

plots = pn.Row(web_site_views, daily_sales, completed_tasks, sizing_mode="stretch_both")
footer = pn.Row("© 2025, made with by **[panel-material-ui](https://holoviz-dev.github.io/panel-material-ui/)** for beautiful data apps.")
fab_button = pmu.widgets.ButtonIcon(icon="settings", color="dark", size="2em", description="Toggle settings drawer")
fab_row = pn.Row(pn.Spacer(sizing_mode="stretch_width"), fab_button)
main = pn.Column(action_row, page_title, indicators, plots, pn.Spacer(sizing_mode="stretch_height"), footer, pmu.layout.Divider(sizing_mode="stretch_width", margin=5), fab_row, sizing_mode="stretch_width", margin=10)
context = pn.Column("#### Material UI Configurator", pn.Spacer(sizing_mode="stretch_height"), width=300, margin=10, styles=CARD_STYLES, visible=True)

def toggle_context(event):
    context.visible=not context.visible

settings_button.on_click(toggle_context)

body = pmu.Column(
    pn.Row(sidebar,main, context),
    sizing_mode="stretch_both",
    styles={"background": "#f5f5f5", "width": "100vw"}, # Hack
).servable(title="Dashboard")
