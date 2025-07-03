import altair as alt
import panel_material_ui as pmu
from vega_datasets import data
import panel as pn

pn.extension('vega')

def create_material_theme(primary_color="#1976d2", font_family="Roboto, Helvetica, Arial", n_colors=10, enable=True):
    """Create a custom Altair theme aligned with Material Design."""
    palette = pmu.theme.generate_palette(primary_color, n_colors=n_colors)

    # Generate color gradients for continuous scales
    light_gradient = pmu.theme.linear_gradient("#ffffff", primary_color, n=256)
    dark_theme = False
    grid_color = "rgb(255, 255, 255, 0.67)" if dark_theme else "rgba(0, 0, 0, 0.33)"

    @alt.theme.register('material', enable=enable)
    def material_theme():
        return {
            "config": {
                # View properties
                "view": {
                    "continuousWidth": 600,
                    "continuousHeight": 400,
                    "stroke": "transparent",
                    "strokeWidth": 0
                },
                "background": "transparent",

                # Font settings
                "font": font_family,

                # Mark defaults aligned with primary color
                "mark": {
                    "color": primary_color,
                    "fill": primary_color,
                    "tooltip": True
                },

                # Specific mark types
                "arc": {"fill": primary_color},
                "area": {"fill": primary_color, "fillOpacity": 0.7},
                "bar": {"fill": primary_color},
                "circle": {"fill": primary_color},
                "line": {"stroke": primary_color, "strokeWidth": 2},
                "point": {"fill": primary_color, "size": 60},
                "rect": {"fill": primary_color},
                "square": {"fill": primary_color},
                "tick": {"fill": primary_color},
                "trail": {"fill": primary_color},

                # Axis styling
                "axis": {
                    "labelFont": font_family,
                    "labelFontSize": 12,
                    "labelColor": "#666666",
                    "titleFont": font_family,
                    "titleFontSize": 14,
                    "titleColor": "#424242",
                    "titleFontWeight": 500,
                    "grid": True,
                    "gridColor": grid_color,
                    "gridOpacity": 0.5,
                    "domain": False,
                    "ticks": False,
                    "labelPadding": 8,
                    "titlePadding": 16
                },

                # Legend styling
                "legend": {
                    "labelFont": font_family,
                    "labelFontSize": 12,
                    "labelColor": "#666666",
                    "titleFont": font_family,
                    "titleFontSize": 14,
                    "titleColor": "#424242",
                    "titleFontWeight": 500,
                    "padding": 8,
                    "symbolSize": 80,
                    "symbolStrokeWidth": 0,
                    "cornerRadius": 4
                },

                # Title styling
                "title": {
                    "font": font_family,
                    "fontSize": 18,
                    "fontWeight": 500,
                    "color": "#212121",
                    "anchor": "start",
                    "align": "left",
                    "offset": 20
                },

                # Header styling (for faceted charts)
                "header": {
                    "titleFont": font_family,
                    "titleFontSize": 14,
                    "titleColor": "#424242",
                    "titleFontWeight": 500,
                    "labelFont": font_family,
                    "labelFontSize": 12,
                    "labelColor": "#666666"
                },

                # Color ranges
                "range": {
                    "category": palette,
                    "diverging": light_gradient,
                    "heatmap": light_gradient,
                    "ordinal": palette,
                    "ramp": light_gradient
                },

                # Style definitions
                "style": {
                    "guide-label": {
                        "font": font_family,
                        "fontSize": 12,
                        "fill": "#666666"
                    },
                    "guide-title": {
                        "font": font_family,
                        "fontSize": 14,
                        "fill": "#424242",
                        "fontWeight": 500
                    },
                    "group-title": {
                        "font": font_family,
                        "fontSize": 16,
                        "fill": "#212121",
                        "fontWeight": 500
                    }
                }
            }
        }

    return material_theme

# Create and apply the theme
primary_color = "#e91e63"
create_material_theme(primary_color, "Roboto, Helvetica, Arial")

df = data.cars()
toggle = pmu.ThemeToggle(styles={"margin-left": "auto"})

chart = alt.Chart(df).mark_circle(size=80).encode(
    x='Horsepower:Q',
    y='Miles_per_Gallon:Q',
    color='Origin:N',
    tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
).properties(
    width=600,
    height=400
).interactive()

pmu.Container(
    toggle,
    pn.pane.Vega(chart, sizing_mode="stretch_width"),
    theme_config={"palette": {"primary": {"main": primary_color}}},
    width_option="md"
).servable()
