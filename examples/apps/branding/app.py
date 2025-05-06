import datetime

import hvplot.pandas  # noqa: F401
import numpy as np
import pandas as pd
import panel_material_ui as pmui
import panel as pn
import param
from panel.viewable import Viewer

from brand import mui, colors, assets

mui.configure()

pn.extension(sizing_mode="stretch_width")

stop_server = pmui.Button(
    name="Drop the Connection",
    sizing_mode="stretch_width",
    color="error",
    variant="outlined",
)
stop_server.js_on_click(
    code="""
Bokeh.documents[0].event_manager.send_event({'event_name': 'connection_lost', 'publish': false})
"""
)


def get_quarters():
    start = datetime.datetime.now().year - 1
    dates = {}
    for year in range(start, start + 10):
        dates[f"{year} Q1"] = datetime.date(year - 1, 12, 31)
        dates[f"{year} Q2"] = datetime.date(year, 3, 31)
        dates[f"{year} Q3"] = datetime.date(year, 6, 30)
        dates[f"{year} Q4"] = datetime.date(year, 9, 30)
    return dates


class State(Viewer):
    currency = param.Selector(
        default="EUR", objects=["EUR", "GBP", "USD"], label="Currency"
    )
    time_start = param.CalendarDate()
    time_end = param.CalendarDate()

    notation_time_start = param.CalendarDate()
    notation_time_end = param.CalendarDate()

    dark_theme = param.Boolean(default=False, label="Dark Theme", allow_refs=True)

    def __init__(self, **params):
        super().__init__(**params)
        last_update = datetime.datetime.now().date() - datetime.timedelta(days=1)

        current_year = last_update.year
        end_year = datetime.date(current_year - 1, 12, 31)
        self.time_start = end_year
        self.time_end = datetime.date(current_year + 1, 12, 31)
        self.notation_time_start = self.time_start
        self.notation_time_end = last_update
        self.dark_theme = pn.config.theme == "dark"

    def __panel__(self):
        quarters = get_quarters()

        time_range_start = pmui.Select.from_param(
            self.param.time_start, options=quarters
        )
        time_range_end = pmui.Select.from_param(self.param.time_end, options=quarters)
        notation_time_start = pmui.DatePicker.from_param(self.param.notation_time_start)
        notation_time_end = pmui.DatePicker.from_param(self.param.notation_time_end)

        return pmui.Column(
            self.param.currency,
            pmui.Row(time_range_start, time_range_end),
            pmui.Column(notation_time_start, notation_time_end),
        )


state = State()

example_buttons = pn.FlexBox(
    *(
        pmui.Button(name=color.capitalize(), color=color, width=120)
        for color in pmui.COLORS[:-1]
    )
)
github_link = pmui.Button(
    name="GitHub",
    color="default",
    variant="outlined",
    href="https://github.com/panel-extensions/panel-material-ui",
    icon="open_in_new",
)
docs_link = pmui.Button(
    name="Docs",
    color="default",
    variant="outlined",
    href="https://panel-material-ui.holoviz.org/",
    align="end",
    icon="open_in_new",
)

drawer = pmui.Drawer(pn.Spacer(height=75), stop_server, anchor="right", size=300)
open_drawer = drawer.create_toggle(icon="settings", sizing_mode="fixed", color="light", styles={"margin-left": "auto"})

cards = pmui.Row(
    pmui.Paper(
        pn.pane.Image(
            "https://cdn.britannica.com/94/192794-050-3F3F3DDD/panels-electricity-order-sunlight.jpg",
            margin=0,
            sizing_mode="stretch_both",
        ),
        "# Reports\n\nDownload our annual report and see all our reports and presentations",
        width=300,
        sizing_mode="fixed",
        margin=10,
    ),
    pmui.Paper(
        pn.pane.Image(
            "https://cdn.britannica.com/94/192794-050-3F3F3DDD/panels-electricity-order-sunlight.jpg",
            margin=0,
            sizing_mode="stretch_both",
        ),
        "# Reports\n\nDownload our annual report and see all our reports and presentations",
        width=300,
        sizing_mode="fixed",
        margin=10,
    ),
    sizing_mode="fixed",
    align="center",
    margin=25,
)


@pn.cache
def get_data(n_categories: int, n_rows=100):
    x = np.random.rand(n_rows)
    y = np.random.rand(n_rows)

    categories = [f"Category {i+1}" for i in range(n_categories)]
    category = np.random.choice(categories, n_rows)

    dataframe = pd.DataFrame({"x": x, "y": y, "category": category}).sort_values(
        "category"
    )

    return dataframe


def get_categorical_plot(dark_theme: bool=False):
    df = get_data(n_categories=3, n_rows=30)
    cmap = colors.get_categorical_palette(n_colors=3, dark_theme=dark_theme)
    return df.hvplot.scatter(
        x="x",
        y="y",
        size=75,
        color="category",
        cmap=cmap,
        height=350,
        responsive=True,
        title="Categorical Plot",
        tools=["fullscreen"],
        legend="top_right",
    ).opts(backend_opts={"plot.toolbar.autohide": True}, toolbar="above")


def get_continous_plot(dark_theme):
    np.random.seed(42)
    data = pd.DataFrame(
        {
            "x": np.random.rand(100),
            "y": np.random.rand(100),
            "value": np.random.rand(100) * 100,
        }
    )
    cmap = colors.get_continous_cmap(dark_theme)
    return data.hvplot.scatter(
        x="x",
        y="y",
        c="value",
        size=75,
        cmap=cmap,
        colorbar=True,
        height=350,
        responsive=True,
        title="Continuous Plot",
        tools=["fullscreen"],
    ).opts(backend_opts={"plot.toolbar.autohide": True}, toolbar="above")

categorical_plot = pn.bind(get_categorical_plot, dark_theme=state.param.dark_theme)
continous_plot = pn.bind(get_continous_plot, dark_theme=state.param.dark_theme)

page = pmui.Page(
    header=[open_drawer],
    sidebar=[
        pn.pane.Image(
            assets.VISION_PATH,
            margin=(20, 10, 10, 10),
            sizing_mode="scale_width",
        ),
        pmui.Column(
            "# Settings",
            state,
            pn.VSpacer(min_height=25),
            "### References",
            github_link,
            docs_link,
            sizing_mode="stretch_both",
            margin=(10, 10),
        ),
    ],
    sidebar_width=425,
    main=[pmui.Container("## Buttons", example_buttons, "## Plots", categorical_plot, continous_plot, drawer)],
)

state.dark_theme = page.param.dark_theme

page.servable()
