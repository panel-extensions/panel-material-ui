#!/usr/bin/env python
"""
Orbitron Brand Demo Application

A showcase application demonstrating the fictive Orbitron brand theme with Panel Material UI components.
This demo includes interactive plots, tables, buttons, and a custom theme.
"""
from __future__ import annotations

import datetime as dt
from typing import Dict, Tuple, Any

import hvplot.pandas  # noqa: F401
import numpy as np
import pandas as pd
import panel as pn
import param
from panel.viewable import Viewer

import panel_material_ui as pmui

from brand import mui, colors, assets

# Configure the Orbitron brand theme
mui.configure()

# Initialize Panel with necessary extensions
pn.extension("tabulator", sizing_mode="stretch_width")


def create_debug_button() -> pmui.Button:
    """
    Create a button that simulates dropping the server connection.

    Returns
    -------
    pmui.Button
        Button that triggers a connection loss event when clicked
    """
    button = pmui.Button(
        name="Drop the Connection",
        sizing_mode="stretch_width",
        color="error",
        variant="outlined",
    )
    button.js_on_click(
        code="""
    Bokeh.documents[0].event_manager.send_event({'event_name': 'connection_lost', 'publish': false})
    """
    )
    return button


def get_quarters() -> Dict[str, dt.date]:
    """
    Generate quarter dates for the last year and 9 years into the future.

    Returns
    -------
    Dict[str, dt.date]
        Dictionary mapping quarter labels to end dates
    """
    start = dt.datetime.now().year - 1
    dates = {}
    for year in range(start, start + 10):
        dates[f"{year} Q1"] = dt.date(year - 1, 12, 31)
        dates[f"{year} Q2"] = dt.date(year, 3, 31)
        dates[f"{year} Q3"] = dt.date(year, 6, 30)
        dates[f"{year} Q4"] = dt.date(year, 9, 30)
    return dates


class State(Viewer):
    """
    Application state management class for storing and tracking user preferences.

    This class manages application-level state including currency selection,
    time periods, and theme preferences. It implements Viewer to be renderable
    in Panel.

    Parameters
    ----------
    **params : dict
        Additional parameters to pass to the parent class
    """

    currency = param.Selector(
        default="EUR", objects=["EUR", "GBP", "USD"], label="Currency"
    )
    time_start = param.CalendarDate()
    time_end = param.CalendarDate()
    notation_time_start = param.CalendarDate()
    notation_time_end = param.CalendarDate()
    dark_theme = param.Boolean(default=False, label="Dark Theme", allow_refs=True)

    def __init__(self, **params):
        """Initialize the application state with sensible default values."""
        super().__init__(**params)
        last_update = dt.datetime.now().date() - dt.timedelta(days=1)

        current_year = last_update.year
        end_year = dt.date(current_year - 1, 12, 31)
        self.time_start = end_year
        self.time_end = dt.date(current_year + 1, 12, 31)
        self.notation_time_start = self.time_start
        self.notation_time_end = last_update
        self.dark_theme = pn.config.theme == "dark"

    def __panel__(self) -> pmui.Column:
        """
        Render the state as a Panel component.

        Returns
        -------
        pmui.Column
            A column containing the state UI components
        """
        quarters = get_quarters()

        time_range_start = pmui.Select.from_param(
            self.param.time_start, options=quarters
        )
        time_range_end = pmui.Select.from_param(
            self.param.time_end, options=quarters
        )
        notation_time_start = pmui.DatePicker.from_param(self.param.notation_time_start)
        notation_time_end = pmui.DatePicker.from_param(self.param.notation_time_end)

        return pmui.Column(
            self.param.currency,
            pmui.Row(time_range_start, time_range_end),
            pmui.Column(notation_time_start, notation_time_end),
        )

    def text(self) -> str:
        """
        Generate a markdown string with the current state of parameters.

        Returns
        -------
        str
            Formatted markdown string describing current selections
        """
        return f"""
        The current selections are:

        - Currency: {self.currency}
        - Time: {self.time_start} to {self.time_end}
        - Notation Time: {self.notation_time_start} to {self.notation_time_end}
        - Dark Theme: {'Enabled' if self.dark_theme else 'Disabled'}

        Learn more about [panel-material-ui](https://panel-material-ui.holoviz.org/).
        """


@pn.cache
def get_data(n_categories: int, n_rows: int = 100) -> pd.DataFrame:
    """
    Generate random data for demonstration plots.

    Parameters
    ----------
    n_categories : int
        Number of categories to generate
    n_rows : int, default=100
        Number of data rows to generate

    Returns
    -------
    pd.DataFrame
        DataFrame containing random data points with categories
    """
    x = np.random.rand(n_rows)
    y = np.random.rand(n_rows)

    categories = [f"Category {i+1}" for i in range(n_categories)]
    category = np.random.choice(categories, n_rows)

    dataframe = pd.DataFrame({"x": x, "y": y, "category": category}).sort_values(
        "category"
    )

    return dataframe


def get_categorical_plot(dark_theme: bool = False) -> hvplot.core.HoloViewsPane:
    """
    Create a categorical scatter plot with theme-appropriate colors.

    Parameters
    ----------
    dark_theme : bool, default=False
        Whether to use dark theme colors

    Returns
    -------
    hvplot.core.HoloViewsPane
        Interactive scatter plot with categorical coloring
    """
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


def get_continous_plot(dark_theme: bool) -> hvplot.core.HoloViewsPane:
    """
    Create a continuous value scatter plot with theme-appropriate color map.

    Parameters
    ----------
    dark_theme : bool
        Whether to use dark theme colors

    Returns
    -------
    hvplot.core.HoloViewsPane
        Interactive scatter plot with continuous color mapping
    """
    np.random.seed(42)  # For reproducibility
    data = pd.DataFrame(
        {
            "x": np.random.rand(100),
            "y": np.random.rand(100),
            "value": np.random.rand(100) * 100,
        }
    )
    cmap = colors.get_continuous_cmap(dark_theme)
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


def create_example_buttons() -> pn.FlexBox:
    """
    Create a set of example buttons with different colors.

    Returns
    -------
    pn.FlexBox
        FlexBox containing example buttons
    """
    return pn.FlexBox(
        *(
            pmui.Button(
                name=color.capitalize(),
                color=color,
                width=120,
                on_click=lambda e, color=color: pn.state.notifications.info(
                    f"Clicked the {color.upper()} button"
                ),
            )
            for color in pmui.COLORS[:-1]
        )
    )


def create_reference_links() -> Tuple[pmui.Button, pmui.Button]:
    """
    Create GitHub and documentation reference buttons.

    Returns
    -------
    Tuple[pmui.Button, pmui.Button]
        GitHub and documentation buttons
    """
    github_link = pmui.Button(
        name="GitHub",
        color="default",
        variant="outlined",
        href="https://github.com/panel-extensions/panel-material-ui",
        target="_blank",
        icon="open_in_new",
    )
    docs_link = pmui.Button(
        name="Docs",
        color="default",
        variant="outlined",
        href="https://panel-material-ui.holoviz.org/",
        align="end",
        target="_blank",
        icon="open_in_new",
    )
    return github_link, docs_link


def create_sample_dataframe() -> pd.DataFrame:
    """
    Create a sample DataFrame with various data types for demonstration.

    Returns
    -------
    pd.DataFrame
        DataFrame with various data types
    """
    return pd.DataFrame(
        {
            "int": [1, 2, 3],
            "float": [3.14, 6.28, 9.42],
            "str": ["A", "B", "C"],
            "bool": [True, False, True],
            "date": [dt.date(2019, 1, 1), dt.date(2020, 1, 1), dt.date(2020, 1, 10)],
            "datetime": [
                dt.datetime(2019, 1, 1, 10),
                dt.datetime(2020, 1, 1, 12),
                dt.datetime(2020, 1, 10, 13),
            ],
        },
        index=[1, 2, 3],
    )


def create_tabulator_formatters() -> Dict[str, Dict[str, Any]]:
    """
    Create custom formatters for the Tabulator widget.

    Returns
    -------
    Dict[str, Dict[str, Any]]
        Dictionary of formatters indexed by column name
    """
    return {
        "float": {
            "type": "progress",
            "max": 10,
            "color": [
                colors.LIGHT_THEME.success,
                colors.LIGHT_THEME.warning,
                colors.LIGHT_THEME.error,
            ],
        },
        "bool": {
            "type": "tickCross",
            "tickElement": f'<span class="material-icons-outlined" style="color: {colors.LIGHT_THEME.error}">check</span>',
            "crossElement": f'<span class="material-icons-outlined" style="color: {colors.LIGHT_THEME.success}">clear</span>',
        },
    }


def main():
    """
    Main application entry point.

    Configures and creates the application interface and serves it.
    """
    # Initialize application state
    state = State()

    # Create UI components
    stop_server = create_debug_button()
    example_buttons = create_example_buttons()
    github_link, docs_link = create_reference_links()

    # Create drawer with settings
    drawer = pmui.Drawer(pn.Spacer(height=75), stop_server, anchor="right", size=300)
    open_drawer = drawer.create_toggle(
        icon="settings", sizing_mode="fixed", color="light", styles={"margin-left": "auto"}
    )

    # Create plots with theme binding
    categorical_plot = pn.bind(get_categorical_plot, dark_theme=state.param.dark_theme)
    continuous_plot = pn.bind(get_continous_plot, dark_theme=state.param.dark_theme)

    # Create data table
    df = create_sample_dataframe()
    tabulator_formatters = create_tabulator_formatters()
    df_widget = pn.widgets.Tabulator(
        df,
        buttons={"Print": '<span class="material-icons-outlined">print</span>'},
        sizing_mode="stretch_width",
        height=300,
        formatters=tabulator_formatters,
        show_index=False,
        disabled=True,
    )

    # Create main page
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
        main=[
            pmui.Container(
                "## Text",
                state.text,
                "## Buttons",
                example_buttons,
                "## Plots",
                categorical_plot,
                continuous_plot,
                drawer,
                "## Table",
                df_widget,
            )
        ],
    )

    # Sync the state's dark theme with the page's dark theme
    state.dark_theme = page.param.dark_theme

    # Make the page available to serve
    page.servable()


if pn.state.served:
    main()
