import panel as pn
import panel_material_ui as pmu
import pandas as pd
from shared.config import BODY_STYLES, CARD_STYLES, BODY_BACKGROUND

pn.extension()

data = [
    {
        "image": "https://randomuser.me/api/portraits/men/1.jpg",
        "name": "John Michael",
        "email": "john.michael@example.com",
        "title": "Manager",
        "team": "Organization",
        "status": "Online",
        "employed": "23/04/18",
    },
    {
        "image": "https://randomuser.me/api/portraits/women/2.jpg",
        "name": "Alexa Liras",
        "email": "alexa.liras@example.com",
        "title": "Programmer",
        "team": "Developer",
        "status": "Offline",
        "employed": "11/01/19",
    },
    {
        "image": "https://randomuser.me/api/portraits/men/3.jpg",
        "name": "Laurent Perrier",
        "email": "laurent.perrier@example.com",
        "title": "Executive",
        "team": "Projects",
        "status": "Online",
        "employed": "19/09/17",
    },
    {
        "image": "https://randomuser.me/api/portraits/women/4.jpg",
        "name": "Michael Levi",
        "email": "michael.levi@example.com",
        "title": "Designer",
        "team": "Creative",
        "status": "Online",
        "employed": "24/12/08",
    },
]
df = pd.DataFrame(data)

@pn.cache
def style_authors_table(df=df):
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

    df["Author"] = df.apply(render_author, axis=1)
    df["Function"] = df.apply(render_function, axis=1)
    df["Status"] = df.apply(render_status, axis=1)
    df["Edit"] = render_edit_button()
    df = df.rename(columns={"employed": "Employed"})
    df = df[
        [
            "Author",
            "Function",
            "Status",
            "Employed",
            "Edit",
        ]
    ]

    styled_df = df.style
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


styled_table = style_authors_table(df)
author_table = pn.panel(styled_table, sizing_mode="stretch_width")

authors_card = pn.Column(
    pn.pane.Markdown(
        "### Authors Table",
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
    author_table,
    styles=CARD_STYLES,
    margin=10,
)

main = pn.Column(
    pn.Spacer(height=25),
    authors_card,
    pn.Spacer(sizing_mode="stretch_both"),
    sizing_mode="stretch_both",
    # styles=BODY_STYLES,
)

pmu.template.Page(
    main=[main],
    theme_config={
        "palette": {
            "primary": {"main": BODY_BACKGROUND},
            "background": {
                "paper": BODY_BACKGROUND,
            },
        }
    },
).servable()
