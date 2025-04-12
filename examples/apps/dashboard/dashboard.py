# Inspiration: https://demos.creative-tim.com/material-dashboard/pages/dashboard
# docs: https://holoviz-dev.github.io/panel-material-ui/
# panel serve examples/apps/dashboard/*.py --index dashboard --dev
import panel_material_ui as pmu
import panel as pn
import param
from shared.config import BODY_STYLES, CARD_STYLES
from shared.plots import (
    get_website_views_config,
    get_daily_sales_config,
    get_completed_tasks_config,
)
from shared.components import create_change_indicator, create_menu
from shared.page import create_page

CSS_RAW = """
.material-symbols-outlined {
    font-size: 12px;
}
"""


pn.extension(
    "echarts",
    design="material",
    css_files=[
        "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&icon_names=schedule,weekend,person,leaderboard"
    ],
)
page_title = f"""\
## Dashboard

"Check the sales, value and bounce rate by country".\
"""

indicators = pn.Row(
    create_change_indicator(
        "Today's Money", "weekend", "$53,000", 55, "since yesterday"
    ),
    create_change_indicator("Today's Users", "person", "2300", 3, "than last month"),
    create_change_indicator("Ads Views", "leaderboard", "3,462", -2, "since yesterday"),
    create_change_indicator("Sales", "weekend", "$103,430", 5, "since yesterday"),
)


def last_update(message):
    # Why is HTML pane hidden?
    return pn.panel(
        f"<span class='material-symbols-outlined'>schedule</span> {message}",
        stylesheets=[CSS_RAW],
    )


web_site_views = pn.Column(
    "#### Website Views\n\nLast Campaign Performance",
    pn.pane.ECharts(
        get_website_views_config(),
        sizing_mode="stretch_width",
        height=250,
        margin=(0, 5),
    ),
    pn.Spacer(sizing_mode="stretch_height"),
    last_update("campaign sent 2 days ago"),
    sizing_mode="stretch_width",
    styles=CARD_STYLES,
    margin=10,
    height=400,
)
daily_sales = pn.Column(
    "#### Daily Sales\n\n(**+15%**) increase in todays sales",
    pn.pane.ECharts(
        get_daily_sales_config(), sizing_mode="stretch_width", height=250, margin=(0, 5)
    ),
    pn.Spacer(sizing_mode="stretch_height"),
    last_update("updated 4 min ago"),
    sizing_mode="stretch_width",
    styles=CARD_STYLES,
    margin=10,
    height=400,
)
completed_tasks = pn.Column(
    "#### Completed Tasks\n\nLast Campaign Performance",
    pn.pane.ECharts(
        get_completed_tasks_config(),
        sizing_mode="stretch_width",
        height=250,
        margin=(0, 5),
    ),
    pn.Spacer(sizing_mode="stretch_height"),
    last_update("just updated"),
    sizing_mode="stretch_width",
    styles=CARD_STYLES,
    margin=10,
    height=400,
)

plots = pn.Row(web_site_views, daily_sales, completed_tasks, sizing_mode="stretch_both")

create_page(name="Dashboard", main=[page_title, indicators, plots]).servable(
    title="Dashboard"
)
