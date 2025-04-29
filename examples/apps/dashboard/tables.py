import panel as pn
import panel_material_ui as pmu
import pandas as pd

from shared.data import get_authors_data, get_project_data_2
from shared.page import create_page
from shared.components import create_card_with_jumbo_header
from shared import tables as table_func

pn.extension()


@pn.cache
def to_styled_authors_table(data):
    data["Author"] = data.apply(table_func.render_author, axis=1)
    data["Function"] = data.apply(table_func.render_function, axis=1)
    data["Status"] = data.apply(table_func.render_status, axis=1)
    data["Edit"] = table_func.render_edit_button()
    data = data.rename(columns={"employed": "Employed"})
    data = data[
        [
            "Author",
            "Function",
            "Status",
            "Employed",
            "Edit",
        ]
    ]

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
                {
                    "selector": ".col0, .col1, .col2, .col3, .col4",
                    "props": [
                        ("width", "20%"),
                    ],
                },
            ]
        )
        .set_properties(
            **{"text-align": "left"},
        )
    )

    return styled_df



@pn.cache
def to_styled_projects_2_table(data: pd.DataFrame):

    data["Company"] = data.apply(table_func.generate_company_html, axis=1)
    data["Completion"] = data.apply(table_func.generate_progress_bar, axis=1)
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
                {
                    "selector": ".col0, .col1, .col2, .col3",
                    "props": [
                        ("width", "20%"),
                    ],
                },
            ]
        )
        .set_properties(
            **{"text-align": "left"},
        )
    )

    return styled_df


authors_data = get_authors_data()
styled_authors_table = to_styled_authors_table(authors_data)
authors_table = pn.panel(styled_authors_table, sizing_mode="stretch_width")
authors_card = create_card_with_jumbo_header("### Authors Table", authors_table)

projects_data_2 = get_project_data_2()
styled_projects_2_table = to_styled_projects_2_table(projects_data_2)
projects_2_table = pn.panel(styled_projects_2_table, sizing_mode="stretch_width")
projects_2_card = create_card_with_jumbo_header("### Project Table", projects_2_table)

main = pn.Column(
    pn.Spacer(height=25),
    authors_card,
    projects_2_card,
    pn.Spacer(sizing_mode="stretch_both"),
    sizing_mode="stretch_both",
)
create_page(name="Tables", main=[main]).servable(title="Tables")
