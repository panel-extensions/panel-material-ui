# Inspiration: https://demos.creative-tim.com/material-dashboard/pages/dashboard
# docs: https://holoviz-dev.github.io/panel-material-ui/
# panel serve examples/apps/dashboard/*.py --dev
import panel_material_ui as pmu
import panel as pn
import param
import pandas as pd

from panel_material_ui import ChangeIndicator
from panel_material_ui import Icon

from shared.data import get_project_data
from shared.plots import (
    get_website_views_config,
    get_daily_sales_config,
    get_completed_tasks_config,
)
from shared.components import create_menu, Timeline
from shared.page import create_page

my_theme = {
    "palette": {
        "primary": {
            "main": "#FF5733",
            # light, dark, and contrastText can be automatically computed
        },
        "secondary": {
            "main": "#E0C2FF",
            "light": "#F5EBFF",   # optional
            "dark": "#BA99D5",    # optional
            "contrastText": "#47008F",  # optional
        }
    }
}


pn.extension("echarts")

page_title = f"""\
## Dashboard

Check the sales, value and bounce rate by country.\
"""

indicators = pn.Row(
    ChangeIndicator(
        title="Today's Money", icon="weekend", value="$53,000", change_percent=55, since="since yesterday", sizing_mode="stretch_width"
    ),
    ChangeIndicator(title="Today's Users", icon="person", value="2300", change_percent=3, since="than last month", sizing_mode="stretch_width"),
    ChangeIndicator(title="Ads Views", icon="leaderboard", value="3,462", change_percent=-2, since="since yesterday", sizing_mode="stretch_width"),
    ChangeIndicator(title="Sales", icon="weekend", value="$103,430", change_percent=5, since="since yesterday", sizing_mode="stretch_width"),
)


def last_update(message):
    schedule = Icon(value="schedule", font_size="small", sizing_mode="fixed", width=20, height=25, margin=(10,5, 10, 5))
    return pn.Row(schedule, pn.pane.HTML(message, sizing_mode="fixed", margin=(11,0)), sizing_mode="fixed")

def generate_company_html(row, image_width='40px'):
    company_name=row["Company"]
    company_image_url=row["CompanyImage"]
    html = f'''
    <div style="display: flex; align-items: center; gap: 10px;">
        <img src="{company_image_url}" alt="{company_name}" style="width: {image_width}; height: auto;">
        <h4>{company_name}</h4>
    </div>
    '''
    return html

def generate_progress_bar(row):
    completion_percent = int(round(float(row["Completion"]),0))
    color = 'green' if completion_percent >=99.999 else 'blue'
    html = f'''
    <div style=\"width: 100%;\">
        <div style=\"margin-bottom: 4px; font-size: 12px; text-align: left;\">{completion_percent}%</div>
        <div style=\"width: 100%; background-color: #e0e0e0; border-radius: 4px; overflow: hidden; height: 5px;\">
            <div style=\"width: {completion_percent}%; background-color: {color}; height: 100%;\"></div>
        </div>
    </div>
    '''
    return html

def generate_member_images(row, image_size='30px', overlap_offset='-10px'):
    members = row["Members"]
    images_html = ''
    for idx, member in enumerate(members):
        images_html += f'''
        <img src=\"{member['Image']}\" title=\"{member['Name']}\"
             style=\"
                width: {image_size};
                height: {image_size};
                border-radius: 50%;
                border: 2px solid white;
                position: relative;
                left: {idx * int(overlap_offset.replace('px', ''))}px;
                z-index: {len(members)-idx};
                transition: transform 0.2s;
             \"
             onmouseover=\"this.style.transform='scale(1.2)';this.style.zIndex='{len(members)+1}'\"
             onmouseout=\"this.style.transform='scale(1)';this.style.zIndex='{len(members)-idx}'\"
        >
        '''
    wrapper_html = f'''
    <div style=\"display: flex; align-items: center;\">
        {images_html}
    </div>
    '''
    return wrapper_html

def to_styled_projects_table(data: pd.DataFrame):
    data["Company"] = data.apply(generate_company_html, axis=1)
    data["Completion"] = data.apply(generate_progress_bar, axis=1)
    data["Members"] = data.apply(generate_member_images, axis=1)
    data = data.drop(columns=["CompanyImage"])
    styled_df = data.style
    styled_df = (
        styled_df.hide(axis="index")
        .set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "white"),
                        ("font-weight", "bold"),
                        ("border-bottom", "1px solid black"),
                        ("text-align", "left"),
                    ],
                },
                {
                    "selector": "td",
                    "props": [
                        ("padding", "10px"),
                        ("background", "white"),
                        ("border-top", "1px solid black"),
                    ],
                },
            ]
        )
        .set_properties(
            **{"text-align": "left"},
        )
    )

    return styled_df


with pn.config.set(sizing_mode="stretch_width"):
    web_site_views = pmu.Paper(
        "#### Website Views\n\nLast Campaign Performance",
        pn.pane.ECharts(
            get_website_views_config(),
            height=250,
            margin=(0, 5),
        ),
        pn.Spacer(sizing_mode="stretch_height"),
        pmu.Divider(margin=(10, 10, -5, 10)),
        last_update("campaign sent 2 days ago"),
        height=400, margin=10
    )

    daily_sales = pmu.Paper(
        "#### Daily Sales\n\n**+15%** increase in todays sales",
        pn.pane.ECharts(
            get_daily_sales_config(),
            height=250,
            margin=(0, 5),
        ),
        pn.Spacer(sizing_mode="stretch_height"),
        pmu.Divider(margin=(10,10,-5,10)),
        last_update("updated 4 min ago"),
        margin=10,
        height=400,
    )
    completed_tasks = pmu.Paper(
        "#### Completed Tasks\n\nLast Campaign Performance",
        pn.pane.ECharts(
            get_completed_tasks_config(),
            height=250,
            margin=(0, 5),
        ),
        pn.Spacer(sizing_mode="stretch_height"),
        pmu.Divider(margin=(10,10,-5,10)),
        last_update("just updated"),
        margin=10,
        height=400,
    )

    plots = pn.Row(web_site_views, daily_sales, completed_tasks, sizing_mode="stretch_both")
    project_table = pmu.Paper(
        "#### Projects\n\n**30 done** this month",
        pn.pane.DataFrame(to_styled_projects_table(get_project_data()), sizing_mode="stretch_width"),
        margin=10,
        height=550,
    )
    timeline_config = [
        {"content_title": "$2400, Design changes", "content": "22 DEC 7:20 PM", "color": "success", "icon": "notifications", "disable_dot": True},
        {"content_title": "New order #1832412", "content": "21 DEC 11 PM", "color": "error", "icon": "code", "disable_dot": True},
        {"content_title": "Server payments for April", "content": "21 DEC 9:34 PM", "color": "primary", "icon": "shopping_cart", "disable_dot": True},
        {"content_title": "New card added for order #4395133", "content": "20 DEC 2:20 AM", "color": "warning", "icon": "credit_card", "disable_dot": True},
        {"content_title": "Unlock packages for development", "content": "18 DEC 4:54 AM", "color": "error", "icon": "key", "disable_dot": True},
        {"content_title": "New order #9583120", "content": "17 DEC", "color": "dark", "icon": "payments", "disable_dot": True},
    ]
    sx = {
        "& .MuiTimelineItem-root:before": {
          "flex": 0,
          "padding-left": 10,
        },
    }
    timeline_component = Timeline(object=timeline_config, sizing_mode="stretch_width", sx=sx)
    timeline_component = pmu.Alert("The `Timeline` component does not work yet due to [#190](https://github.com/panel-extensions/panel-material-ui/issues/190).", alert_type="error", margin=10)
    timeline = pmu.Paper(
        "#### Orders overview\n\n**24%** this month",
        timeline_component,
        margin=10,
        height=550,
    )
    table_timeline_row = pn.Row(project_table, timeline)

create_page(
    name="Dashboard",
    main=[page_title, indicators, plots, table_timeline_row]).servable(
    title="Dashboard"
)
