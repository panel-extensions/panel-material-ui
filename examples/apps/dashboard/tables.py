import panel as pn
import panel_material_ui as pmu
import pandas as pd
from shared.config import BODY_STYLES, PAPER_STYLES, BODY_BACKGROUND
from shared.data import get_authors_data
from shared.page import create_page

pn.extension()


@pn.cache
def to_styled_authors_table(data):
    def render_author(row):
        return (
            f'<div style="display:flex; align-items:center; gap:10px;">'
            f'<img src="{row["image"]}" alt="img" style="width:35px; height:35px; border-radius:50%; object-fit:cover;">'
            f'<div><div style="font-weight:600;">{row["name"]}</div><div style="font-size:12px;color:gray;">{row["email"]}</div></div>'
            f"</div>"
        )

    def render_function(row):
        return f'<div><div style="font-weight:600;">{row["title"]}</div><div style="font-size:12px;color:gray;">{row["team"]}</div></div>'

    def render_status(row):
        color = "#43a047" if row["status"] == "Online" else "#747b8a"

        return f'<span style="background-color:{color}; color:white; padding:3px 8px; border-radius:5px; font-size:12px;">{row["status"]}</span>'

    def render_edit_button():
        return '<button style="color:black;border:none;padding:6px 12px;border-radius:4px;cursor:pointer;">Edit</button>'

    data["Author"] = data.apply(render_author, axis=1)
    data["Function"] = data.apply(render_function, axis=1)
    data["Status"] = data.apply(render_status, axis=1)
    data["Edit"] = render_edit_button()
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
            ]
        )
        .set_properties(
            **{"text-align": "left"},
        )
    )

    return styled_df


def get_card_with_jumbo_header(title, content):
    return pn.Column(
        pn.pane.Markdown(
            title,
            sizing_mode="stretch_width",
            styles={
                "background": "black",
                "color": "white",
                "border_radius": "5px",
                "position": "relative",
                "padding-left": "25px",
                "top": "-25px",
            },
            margin=(10, 50, 10, 50),
            height=50,
        ),
        content,
        styles=PAPER_STYLES,
        margin=10,
    )


authors_data = get_authors_data()
styled_authors_table = to_styled_authors_table(authors_data)
authors_table = pn.panel(styled_authors_table, sizing_mode="stretch_width")
authors_card = get_card_with_jumbo_header("### Authors Table", authors_table)

main = pn.Column(
    pn.Spacer(height=25),
    authors_card,
    pn.Spacer(sizing_mode="stretch_both"),
    sizing_mode="stretch_both",
)
create_page(name="Tables", main=[main]).servable(title="Tables")
