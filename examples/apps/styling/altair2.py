import panel as pn
import panel_material_ui as pmu
import altair as alt
from vega_datasets import data
from typing import Optional

pn.extension("vega")

df = data.cars()
toggle = pmu.ThemeToggle(styles={"margin-left": "auto"})

chart = alt.Chart(df).mark_circle(size=60).encode(
    x='Horsepower:Q',
    y='Miles_per_Gallon:Q',
    color='Origin:N',
    tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
).properties(
    width=600,
    height=400
)

def configure(
    chart: alt.Chart,
    primary: str = "#1976d2",
    primary_dark: str | None = None,
    dark_theme: bool = True,
) -> alt.Chart:
    """
    Configure Altair chart with Material UI theme colors.

    Parameters
    ----------
    chart : alt.Chart
        The Altair chart to configure
    primary : str, default "#1976d2"
        Primary color for chart elements
    primary_dark : str, default "#115293"
        Darker variant of primary color for accents
    dark_theme : bool, default True
        Whether to use dark theme styling

    Returns
    -------
    alt.Chart
        Configured chart with Material UI theming
    """
    font = "Roboto, Helvetica, Arial, sans-serif"
    font_color = "rgb(255, 255, 255)" if dark_theme else "rgba(0, 0, 0, 0.87)"
    primary = primary_dark if (primary_dark and dark_theme) else primary
    colors = pmu.theme.generate_palette(primary, n_colors=5)
    return chart.configure(
        font=font,
        background="transparent"
    ).configure_view(
        stroke="transparent"
    ).configure_mark(
        color=primary,
        filled=True,
        tooltip=True,
    ).configure_axis(
        labelColor=font_color,
        titleColor=font_color,
        tickColor=font_color,
        gridColor=font_color,
        gridOpacity=0.33,
        domainColor=font_color,
    ).configure_legend(
        labelColor=font_color,
        titleColor=font_color,
    ).configure_title(
        color=font_color
    ).configure_range(
        # category=colors  # Use generated palette for categorical colors
    ).interactive()

# Define theme colors
# orsted blue
primary_color = "#788A12"
primary_dark_color = "#E38DE6"

pmu.Container(
    toggle,
    pn.pane.Vega(
        pn.bind(
            configure,
            chart,
            primary=primary_color,
            primary_dark=primary_dark_color,
            dark_theme=toggle.param.dark_theme,
        ),
        sizing_mode="stretch_width"
    ),
    """Lorum ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.""",
    theme_config={
        "palette": {
            "primary": {
                "main": primary_color,
                "dark": primary_dark_color
            }
        }
    },
    width_option="md"
).servable()
