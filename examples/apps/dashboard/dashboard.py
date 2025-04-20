# Inspiration: https://demos.creative-tim.com/material-dashboard/pages/dashboard
# docs: https://holoviz-dev.github.io/panel-material-ui/
# panel serve examples/apps/dashboard/*.py --index dashboard --dev
import panel_material_ui as pmu
import panel as pn
import param
from shared.config import BODY_STYLES, PAPER_STYLES, ICON_CSS
from shared.plots import (
    get_website_views_config,
    get_daily_sales_config,
    get_completed_tasks_config,
)
from shared.components import create_change_indicator, create_menu
from shared.page import create_page
import pandas as pd
from shared.data import get_project_data
from panel_material_ui.pane import Timeline

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


pn.extension(
    "echarts",
    design="material",
    # theme="dark",
    # css_files=[
    #     "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&icon_names=schedule,weekend,person,leaderboard"
    # ],
)
page_title = f"""\
## Dashboard

Check the sales, value and bounce rate by country.\
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
        stylesheets=[ICON_CSS],
    )

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
    print(color, completion_percent)
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

def to_styles_projects_table(data: pd.DataFrame):
    data["Company"]=data.apply(generate_company_html, axis=1)
    data["Completion"]=data.apply(generate_progress_bar, axis=1)
    data["Members"]=data.apply(generate_member_images, axis=1)
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
    web_site_views = pn.Column(pn.Column(
        "#### Website Views\n\nLast Campaign Performance",
        pn.pane.ECharts(
            get_website_views_config(),
            height=250,
            margin=(0, 5),
        ),
        pn.Spacer(sizing_mode="stretch_height"),
        last_update("campaign sent 2 days ago"),
    ), styles=PAPER_STYLES, height=400, margin=10, )

    daily_sales = pn.Column(
        "#### Daily Sales\n\n**+15%** increase in todays sales",
        pn.pane.ECharts(
            get_daily_sales_config(), height=250, margin=(0, 5),
        ),
        pn.Spacer(sizing_mode="stretch_height"),
        last_update("updated 4 min ago"),
        styles=PAPER_STYLES,
        margin=10,
        height=400,
    )
    completed_tasks = pn.Column(
        "#### Completed Tasks\n\nLast Campaign Performance",
        pn.pane.ECharts(
            get_completed_tasks_config(),
            height=250,
            margin=(0, 5),
        ),
        pn.Spacer(sizing_mode="stretch_height"),
        last_update("just updated"),
        styles=PAPER_STYLES,
        margin=10,
        height=400,
    )

    plots = pn.Row(web_site_views, daily_sales, completed_tasks, sizing_mode="stretch_both")
    project_table = pn.Column(
        "#### Projects\n\n**30 done** this month",
        pn.panel(to_styles_projects_table(get_project_data()), sizing_mode="stretch_width"),
        styles=PAPER_STYLES,
        margin=10,
        height=550,
    )
    timeline_config = [
        {"content_title": "$2400, Design changes", "content": "22 DEC 7:20 PM", "color": "success", "variant": "filled", "icon": "notifications", },
        {"content_title": "New order #1832412", "content": "21 DEC 11 PM", "color": "error", "variant": "filled", "icon": "code", },
        {"content_title": "Server payments for April", "content": "21 DEC 9:34 PM", "color": "primary", "variant": "filled", "icon": "shopping_cart", },
        {"content_title": "New card added for order #4395133", "content": "20 DEC 2:20 AM", "color": "warning", "variant": "filled", "icon": "credit_card", },
        {"content_title": "Unlock packages for development", "content": "18 DEC 4:54 AM", "color": "info", "variant": "filled", "icon": "key", },
        {"content_title": "New order #9583120", "content": "17 DEC", "color": "dark", "variant": "filled", "icon": "payments", },
    ]
    sx = {
        "& .MuiTimelineItem-root:before": {
          "flex": 0,
          "padding-left": 10,
        },
    }
    timeline = pn.Column(
        "#### Orders overview\n\n**24%** this month",
        Timeline(object=timeline_config, sizing_mode="stretch_width", sx=sx),
        styles=PAPER_STYLES,
        margin=10,
        height=550,
    )
    table_timeline_row = pn.Row(project_table, timeline)

create_page(name="Dashboard", main=[page_title, indicators, plots, table_timeline_row]).servable(
    title="Dashboard"
)
