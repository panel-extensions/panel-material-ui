"""Plotly theme integration for Panel Material UI.

Provides functions to create custom Plotly templates that match
panel-material-ui's design system.

Note: Requires plotly to be installed. Install with: pip install plotly
"""

from typing import Any, Literal, Optional

from . import theme

try:
    import plotly.graph_objects as go  # type: ignore[import-untyped]
    import plotly.io as pio  # type: ignore[import-untyped]
    from plotly.graph_objects import Figure  # type: ignore[import-untyped]
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    # Create placeholder types for better error messages
    go = None
    pio = None
    Figure = Any

ThemeMode = Literal["light", "dark"]


def _check_plotly_available() -> None:
    """Check if plotly is available and raise helpful error if not.

    Raises
    ------
    ImportError
        If plotly is not installed with installation instructions.
    """
    if not PLOTLY_AVAILABLE:
        raise ImportError(
            "Plotly is required for this functionality. "
            "Install with: pip install plotly"
        )


def create_pmui_template(
    mode: ThemeMode = "light",
    primary_color: Optional[str] = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Create a Plotly template matching Panel Material UI theme.

    This function generates a complete Plotly template that matches the Panel
    Material UI design system, including colors, typography, and spacing that
    are consistent with Material Design principles.

    Parameters
    ----------
    mode : {"light", "dark"}
        Theme mode to generate. Light mode uses white backgrounds with dark
        text, while dark mode uses dark backgrounds with light text.
    primary_color : str, optional
        Primary color for the color palette. If None, uses Material UI's
        default primary blue (#1976d2).
    **kwargs : Any
        Additional template customizations passed directly to the layout
        configuration. These override default values.

    Returns
    -------
    Dict[str, Any]
        Plotly template dictionary with layout and colorway settings.
        Can be used with `plotly.io.templates` or passed directly to figures.

    Raises
    ------
    ImportError
        If plotly is not installed.
    ValueError
        If mode is not "light" or "dark".

    Examples
    --------
    Create and register a light theme template:

    >>> import plotly.io as pio
    >>> import panel_material_ui as pmui
    >>>
    >>> template = pmui.plotly.create_pmui_template("light", "#1976d2")
    >>> pio.templates["pmui_light"] = template

    Create a dark theme with custom primary color:

    >>> dark_template = pmui.plotly.create_pmui_template(
    ...     "dark",
    ...     primary_color="#bb86fc"
    ... )

    Create a template with custom margins:

    >>> custom_template = pmui.plotly.create_pmui_template(
    ...     "light",
    ...     margin={"l": 100, "r": 100, "t": 120, "b": 80}
    ... )
    """
    _check_plotly_available()

    # Validate mode
    if mode not in ("light", "dark"):
        raise ValueError(f"Mode must be 'light' or 'dark', got '{mode}'")

    if primary_color is None:
        primary_color = "#1976d2"  # Material UI default primary

    # Generate discrete color palette using existing theme function
    colorway = theme.generate_palette(primary_color, n_colors=10)

    # Material UI design tokens based on mode
    if mode == "light":
        # Light theme colors following Material Design 3.0
        paper_bgcolor = "#ffffff"
        plot_bgcolor = "#ffffff"
        font_color_primary = "rgba(0, 0, 0, 0.87)"  # text.primary
        font_color_secondary = "rgba(0, 0, 0, 0.6)"  # text.secondary
        grid_color = "rgba(0, 0, 0, 0.12)"  # divider
        axis_line_color = "rgba(0, 0, 0, 0.23)"  # outline
        zero_line_color = "rgba(0, 0, 0, 0.12)"
    else:
        # Dark theme colors following Material Design 3.0
        paper_bgcolor = "#121212"  # Material dark surface
        plot_bgcolor = "#121212"
        font_color_primary = "rgba(255, 255, 255, 0.87)"  # dark text.primary
        font_color_secondary = "rgba(255, 255, 255, 0.6)"  # dark text.secondary
        grid_color = "rgba(255, 255, 255, 0.12)"  # dark divider
        axis_line_color = "rgba(255, 255, 255, 0.23)"  # dark outline
        zero_line_color = "rgba(255, 255, 255, 0.12)"

    # Base template structure inspired by Vizro's comprehensive approach
    template = {
        "layout": {
            # Color palette for discrete data
            "colorway": colorway,

            # Typography following Material Design
            "font": {
                "color": font_color_primary,
                "family": "Roboto, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
                "size": 12,
            },

            # Background colors
            "paper_bgcolor": paper_bgcolor,
            "plot_bgcolor": plot_bgcolor,

            # Layout spacing following Material Design 8px grid
            "margin": {"l": 64, "r": 64, "t": 64, "b": 64},

            # Title styling
            "title": {
                "font": {"size": 16, "color": font_color_primary},
                "x": 0.5,
                "xanchor": "center",
                "pad": {"t": 20},
            },

            # X-axis styling
            "xaxis": {
                "gridcolor": grid_color,
                "linecolor": axis_line_color,
                "zerolinecolor": zero_line_color,
                "tickcolor": axis_line_color,
                "tickfont": {"color": font_color_secondary, "size": 11},
                "title": {
                    "font": {"size": 14, "color": font_color_primary},
                    "standoff": 20,
                },
                "showline": True,
                "linewidth": 1,
                "gridwidth": 1,
                "zerolinewidth": 1,
            },

            # Y-axis styling (matches X-axis)
            "yaxis": {
                "gridcolor": grid_color,
                "linecolor": axis_line_color,
                "zerolinecolor": zero_line_color,
                "tickcolor": axis_line_color,
                "tickfont": {"color": font_color_secondary, "size": 11},
                "title": {
                    "font": {"size": 14, "color": font_color_primary},
                    "standoff": 20,
                },
                "showline": True,
                "linewidth": 1,
                "gridwidth": 1,
                "zerolinewidth": 1,
            },

            # Color axis (for continuous color scales)
            "coloraxis": {
                "colorbar": {
                    "outlinewidth": 0,
                    "ticks": "",
                    "tickcolor": axis_line_color,
                    "tickfont": {"color": font_color_secondary},
                    "title": {"font": {"color": font_color_primary}},
                }
            },

            # Legend styling
            "legend": {
                "bgcolor": "rgba(255, 255, 255, 0)",
                "bordercolor": "rgba(0, 0, 0, 0)",
                "font": {"color": font_color_primary},
                "orientation": "v",
                "x": 1.02,
                "xanchor": "left",
            },

            # Hover label styling
            "hoverlabel": {
                "bgcolor": paper_bgcolor,
                "bordercolor": grid_color,
                "font": {"color": font_color_primary},
            },

            # Annotation styling
            "annotationdefaults": {
                "arrowcolor": font_color_primary,
                "arrowhead": 0,
                "arrowwidth": 1,
                "font": {"color": font_color_primary},
            },

            # Geographic plot styling (following Vizro's comprehensive coverage)
            "geo": {
                "bgcolor": paper_bgcolor,
                "lakecolor": paper_bgcolor,
                "landcolor": paper_bgcolor,
            },

            # Polar plot styling
            "polar": {
                "bgcolor": paper_bgcolor,
                "angularaxis": {
                    "gridcolor": grid_color,
                    "linecolor": axis_line_color,
                },
                "radialaxis": {
                    "gridcolor": grid_color,
                    "linecolor": axis_line_color,
                },
            },

            # Ternary plot styling
            "ternary": {
                "bgcolor": paper_bgcolor,
                "aaxis": {
                    "gridcolor": grid_color,
                    "linecolor": axis_line_color,
                },
                "baxis": {
                    "gridcolor": grid_color,
                    "linecolor": axis_line_color,
                },
                "caxis": {
                    "gridcolor": grid_color,
                    "linecolor": axis_line_color,
                },
            },
        },

        # Data trace defaults (following Vizro's approach)
        "data": {
            "bar": [
                {
                    "marker": {
                        "line": {"color": paper_bgcolor, "width": 0.5}
                    }
                }
            ],
            "waterfall": [
                {
                    "decreasing": {"marker": {"color": colorway[1] if len(colorway) > 1 else "#f44336"}},
                    "increasing": {"marker": {"color": colorway[0]}},
                    "totals": {"marker": {"color": "#9e9e9e"}},
                    "textfont": {"color": font_color_primary},
                    "textposition": "outside",
                    "connector": {"line": {"color": axis_line_color, "width": 1}},
                }
            ],
        },
    }

    # Apply any additional customizations using deep update
    if kwargs:
        # Type check the layout to ensure it's a dict before deep update
        layout = template.get("layout")
        if isinstance(layout, dict):
            _deep_update(layout, kwargs)

    return template


def _deep_update(base_dict: dict[str, Any], update_dict: dict[str, Any]) -> None:
    """Recursively update nested dictionary.

    Parameters
    ----------
    base_dict : Dict[str, Any]
        Dictionary to update in place
    update_dict : Dict[str, Any]
        Dictionary with updates to apply
    """
    for key, value in update_dict.items():
        if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
            _deep_update(base_dict[key], value)
        else:
            base_dict[key] = value


def register_pmui_templates(
    primary_color: Optional[str] = None,
    primary_color_dark: Optional[str] = None,
    default: str = "pmui_light",
    **kwargs: Any,
) -> None:
    """Register Panel Material UI templates with Plotly and set default.

    This function creates and registers both light and dark Panel Material UI
    templates with Plotly's template system, and sets the specified template as
    the default.

    Parameters
    ----------
    primary_color : str, optional
        Primary color for both light and dark themes. If None, uses Material UI's
        default primary blue (#1976d2).
    primary_color_dark : str, optional
        Primary color specifically for dark theme. If None, uses the same color
        as primary_color. This allows for different primary colors in light vs dark modes.
    default : str, default "pmui_light"
        Which template to set as the default. Can be any registered Plotly template name.
        After registration, "pmui_light" and "pmui_dark" will be available.
    **kwargs : Any
        Additional template customizations passed to both light and dark templates.
        These override default values for both themes.

    Raises
    ------
    ImportError
        If plotly is not installed.
    ValueError
        If the specified default template is not found after registration.

    Notes
    -----
    The templates will be available as:
    - "pmui_light" for light mode
    - "pmui_dark" for dark mode

    Examples
    --------
    Register templates with default colors:

    >>> import panel_material_ui as pmui
    >>> import plotly.express as px
    >>>
    >>> # Register templates with defaults
    >>> pmui.plotly.register_pmui_templates()
    >>>
    >>> # Use with a plot (will automatically use pmui_light)
    >>> fig = px.scatter(df, x="x", y="y")

    Register templates with dark as default:

    >>> # Set dark theme as default
    >>> pmui.plotly.register_pmui_templates(default="pmui_dark")

    Register templates with built-in Plotly template as default:

    >>> # Use a built-in Plotly template as default
    >>> pmui.plotly.register_pmui_templates(default="plotly_white")

    Register templates with custom primary color:

    >>> # Same color for both themes
    >>> pmui.plotly.register_pmui_templates(primary_color="#9c27b0")

    Register templates with different colors for light and dark:

    >>> # Purple for light, amber for dark
    >>> pmui.plotly.register_pmui_templates(
    ...     primary_color="#9c27b0",
    ...     primary_color_dark="#ff9800"
    ... )

    Register templates with custom styling:

    >>> pmui.plotly.register_pmui_templates(
    ...     primary_color="#1976d2",
    ...     margin={"l": 80, "r": 80, "t": 100, "b": 80}
    ... )
    """
    _check_plotly_available()

    # Determine colors for each theme
    light_color = primary_color
    dark_color = primary_color_dark if primary_color_dark is not None else primary_color

    # Create both light and dark templates
    light_template = create_pmui_template("light", primary_color=light_color, **kwargs)
    dark_template = create_pmui_template("dark", primary_color=dark_color, **kwargs)

    # Register with Plotly
    pio.templates["pmui_light"] = light_template
    pio.templates["pmui_dark"] = dark_template

    # Validate that the specified default template exists
    if default not in pio.templates:
        raise ValueError(
            f"Default template '{default}' not found. "
            f"Available templates: {list(pio.templates.keys())}"
        )

    # Set specified template as default
    pio.templates.default = default

def update_template(
    figure: Any,
    dark_theme: bool = False
) -> Any:
    """Update a Plotly figure's template based on theme mode.

    This function dynamically updates an existing Plotly figure to use
    the appropriate Panel Material UI template based on the theme mode.
    Useful for reactive theme switching in Panel applications.

    Parameters
    ----------
    figure : plotly.graph_objects.Figure
        The Plotly figure to update with the new template.
    dark_theme : bool, default False
        Whether to use the dark theme. If True, uses "pmui_dark" template,
        otherwise uses "pmui_light" template.

    Returns
    -------
    plotly.graph_objects.Figure
        The updated figure with the new template applied.

    Examples
    --------
    Update a figure to use dark theme:

    >>> import plotly.express as px
    >>> import panel_material_ui as pmui
    >>>
    >>> fig = px.scatter(df, x="x", y="y")
    >>> dark_fig = pmui.plotly.update_template(fig, dark_theme=True)

    Use with Panel's reactive system:

    >>> import panel as pn
    >>> toggle = pmui.ThemeToggle()
    >>> pn.pane.Plotly(pn.bind(pmui.plotly.update_template, fig, toggle))

    Notes
    -----
    This function assumes that Panel Material UI templates have been
    registered. If templates are not found, an error will be raised.
    """
    _check_plotly_available()

    template_name = "pmui_dark" if dark_theme else "pmui_light"

    # Check if the template exists before applying
    if template_name not in pio.templates:
        raise ValueError(
            f"Template '{template_name}' not found. "
            "Make sure to call pmui.plotly.register_pmui_templates() first."
        )

    figure.update_layout(template=template_name)
    return figure


# Auto-register templates for convenience when plotly is available
if PLOTLY_AVAILABLE:
    try:
        register_pmui_templates()
    except Exception:
        # Silently fail if registration fails to avoid breaking imports
        pass
