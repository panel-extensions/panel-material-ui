"""Tests for Plotly integration functionality."""

from typing import Any, Dict

import pytest
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

from panel_material_ui.plotly import (
    create_pmui_template,
    register_pmui_templates,
    update_template,
    _deep_update
)


class TestCreatePmuiTemplate:
    """Test cases for create_pmui_template function."""

    def test_create_light_template_default(self) -> None:
        """Test light theme template creation with default parameters."""
        template = create_pmui_template("light")

        assert isinstance(template, dict)
        assert "layout" in template
        assert "data" in template
        assert template["layout"]["paper_bgcolor"] == "#ffffff"
        assert template["layout"]["plot_bgcolor"] == "#ffffff"
        assert template["layout"]["font"]["color"] == "rgba(0, 0, 0, 0.87)"
        assert template["layout"]["font"]["family"].startswith("Roboto")

    def test_create_dark_template_default(self) -> None:
        """Test dark theme template creation with default parameters."""
        template = create_pmui_template("dark")

        assert isinstance(template, dict)
        assert "layout" in template
        assert "data" in template
        assert template["layout"]["paper_bgcolor"] == "#121212"
        assert template["layout"]["plot_bgcolor"] == "#121212"
        assert template["layout"]["font"]["color"] == "rgba(255, 255, 255, 0.87)"
        assert template["layout"]["font"]["family"].startswith("Roboto")

    def test_create_template_with_custom_primary_color(self) -> None:
        """Test template creation with custom primary color."""
        primary_color = "#ff5722"
        template = create_pmui_template("light", primary_color=primary_color)

        # Colorway should be generated from primary color
        assert "colorway" in template["layout"]
        assert len(template["layout"]["colorway"]) == 10
        assert isinstance(template["layout"]["colorway"][0], str)
        # First color should be related to primary color (generated palette)
        assert template["layout"]["colorway"][0] != "#1976d2"  # Not default

    def test_create_template_with_kwargs(self) -> None:
        """Test template creation with additional kwargs."""
        custom_margin = {"l": 100, "r": 100, "t": 120, "b": 80}
        template = create_pmui_template("light", margin=custom_margin)

        assert template["layout"]["margin"] == custom_margin

    def test_create_template_with_nested_kwargs(self) -> None:
        """Test template creation with nested kwargs updates."""
        custom_title = {"font": {"size": 20}, "text": "Custom Title"}
        template = create_pmui_template("light", title=custom_title)

        assert template["layout"]["title"]["font"]["size"] == 20
        assert template["layout"]["title"]["text"] == "Custom Title"
        # Should preserve other title properties
        assert template["layout"]["title"]["x"] == 0.5
        assert template["layout"]["title"]["xanchor"] == "center"

    @pytest.mark.parametrize("mode", ["light", "dark"])
    def test_template_has_required_structure(self, mode: str) -> None:
        """Test that template has all required components."""
        template = create_pmui_template(mode)  # type: ignore
        layout = template["layout"]

        # Required top-level properties
        assert "colorway" in layout
        assert "font" in layout
        assert "paper_bgcolor" in layout
        assert "plot_bgcolor" in layout
        assert "margin" in layout

        # Axis properties
        for axis in ["xaxis", "yaxis"]:
            assert axis in layout
            assert "gridcolor" in layout[axis]
            assert "linecolor" in layout[axis]
            assert "tickcolor" in layout[axis]
            assert "title" in layout[axis]
            assert "tickfont" in layout[axis]

        # Other components
        assert "coloraxis" in layout
        assert "legend" in layout
        assert "title" in layout
        assert "hoverlabel" in layout
        assert "annotationdefaults" in layout

        # Data defaults
        assert "data" in template
        assert "bar" in template["data"]
        assert "waterfall" in template["data"]

    def test_template_colorway_length(self) -> None:
        """Test that colorway has correct number of colors."""
        template = create_pmui_template("light")
        colorway = template["layout"]["colorway"]

        assert len(colorway) == 10
        assert all(isinstance(color, str) for color in colorway)
        # All colors should be valid hex or rgba strings
        for color in colorway:
            assert color.startswith("#") or color.startswith("rgb")

    def test_comprehensive_layout_coverage(self) -> None:
        """Test that template covers all major plot types like Vizro."""
        template = create_pmui_template("light")
        layout = template["layout"]

        # Geographic plots
        assert "geo" in layout
        assert "bgcolor" in layout["geo"]
        assert "lakecolor" in layout["geo"]
        assert "landcolor" in layout["geo"]

        # Polar plots
        assert "polar" in layout
        assert "bgcolor" in layout["polar"]
        assert "angularaxis" in layout["polar"]
        assert "radialaxis" in layout["polar"]
        assert "gridcolor" in layout["polar"]["angularaxis"]
        assert "gridcolor" in layout["polar"]["radialaxis"]

        # Ternary plots
        assert "ternary" in layout
        assert "bgcolor" in layout["ternary"]
        for axis in ["aaxis", "baxis", "caxis"]:
            assert axis in layout["ternary"]
            assert "gridcolor" in layout["ternary"][axis]
            assert "linecolor" in layout["ternary"][axis]

    def test_data_trace_defaults(self) -> None:
        """Test that data trace defaults are properly configured."""
        template = create_pmui_template("light")
        data = template["data"]

        # Bar chart defaults
        assert len(data["bar"]) == 1
        assert "marker" in data["bar"][0]
        assert "line" in data["bar"][0]["marker"]
        assert "color" in data["bar"][0]["marker"]["line"]
        assert "width" in data["bar"][0]["marker"]["line"]

        # Waterfall chart defaults
        assert len(data["waterfall"]) == 1
        waterfall = data["waterfall"][0]
        assert "decreasing" in waterfall
        assert "increasing" in waterfall
        assert "totals" in waterfall
        assert "textfont" in waterfall
        assert "textposition" in waterfall
        assert "connector" in waterfall

        # Check that colors are properly set
        assert "marker" in waterfall["decreasing"]
        assert "marker" in waterfall["increasing"]
        assert "marker" in waterfall["totals"]
        assert "color" in waterfall["decreasing"]["marker"]
        assert "color" in waterfall["increasing"]["marker"]
        assert "color" in waterfall["totals"]["marker"]


class TestRegisterPmuiTemplates:
    """Test cases for register_pmui_templates function."""

    def test_register_pmui_templates_default(self) -> None:
        """Test that templates are registered correctly with defaults."""
        # Store original default to restore later
        original_default = pio.templates.default

        try:
            # Register templates
            register_pmui_templates()

            # Check that templates are registered
            assert "pmui_light" in pio.templates
            assert "pmui_dark" in pio.templates

            # Check that default is set correctly
            assert pio.templates.default == "pmui_light"

        finally:
            # Restore original default
            pio.templates.default = original_default
            # Clean up registered templates
            if "pmui_light" in pio.templates:
                del pio.templates["pmui_light"]
            if "pmui_dark" in pio.templates:
                del pio.templates["pmui_dark"]

    def test_register_pmui_templates_with_primary_color(self) -> None:
        """Test registration with custom primary color for both themes."""
        original_default = pio.templates.default

        try:
            # Register with custom primary color
            register_pmui_templates(primary_color="#9c27b0")

            # Check that templates are registered
            assert "pmui_light" in pio.templates
            assert "pmui_dark" in pio.templates

            # Convert templates to dict for easier testing
            light_template = pio.templates["pmui_light"]
            dark_template = pio.templates["pmui_dark"]

            light_dict = light_template.to_plotly_json() if hasattr(light_template, 'to_plotly_json') else dict(light_template)
            dark_dict = dark_template.to_plotly_json() if hasattr(dark_template, 'to_plotly_json') else dict(dark_template)

            # Both should have colorways derived from the same primary color
            assert len(light_dict["layout"]["colorway"]) == 10
            assert len(dark_dict["layout"]["colorway"]) == 10

        finally:
            pio.templates.default = original_default
            if "pmui_light" in pio.templates:
                del pio.templates["pmui_light"]
            if "pmui_dark" in pio.templates:
                del pio.templates["pmui_dark"]

    def test_register_pmui_templates_with_different_dark_color(self) -> None:
        """Test registration with different primary colors for light and dark themes."""
        original_default = pio.templates.default

        try:
            # Register with different colors for light and dark
            register_pmui_templates(
                primary_color="#1976d2",  # Blue for light
                primary_color_dark="#ff9800"  # Orange for dark
            )

            # Check that templates are registered
            assert "pmui_light" in pio.templates
            assert "pmui_dark" in pio.templates

            # Templates should have different colorways
            light_template = pio.templates["pmui_light"]
            dark_template = pio.templates["pmui_dark"]

            light_dict = light_template.to_plotly_json() if hasattr(light_template, 'to_plotly_json') else dict(light_template)
            dark_dict = dark_template.to_plotly_json() if hasattr(dark_template, 'to_plotly_json') else dict(dark_template)

            # Colorways should be different (derived from different primary colors)
            assert light_dict["layout"]["colorway"] != dark_dict["layout"]["colorway"]

        finally:
            pio.templates.default = original_default
            if "pmui_light" in pio.templates:
                del pio.templates["pmui_light"]
            if "pmui_dark" in pio.templates:
                del pio.templates["pmui_dark"]

    def test_register_pmui_templates_with_kwargs(self) -> None:
        """Test registration with additional kwargs."""
        original_default = pio.templates.default

        try:
            # Register with custom styling
            register_pmui_templates(
                primary_color="#6200ea",
                margin={"l": 100, "r": 100, "t": 120, "b": 80},
                title={"font": {"size": 18}}
            )

            # Check that templates are registered
            assert "pmui_light" in pio.templates
            assert "pmui_dark" in pio.templates

            # Check that customizations were applied to both templates
            light_template = pio.templates["pmui_light"]
            dark_template = pio.templates["pmui_dark"]

            light_dict = light_template.to_plotly_json() if hasattr(light_template, 'to_plotly_json') else dict(light_template)
            dark_dict = dark_template.to_plotly_json() if hasattr(dark_template, 'to_plotly_json') else dict(dark_template)

            # Both templates should have the custom margin
            assert light_dict["layout"]["margin"] == {"l": 100, "r": 100, "t": 120, "b": 80}
            assert dark_dict["layout"]["margin"] == {"l": 100, "r": 100, "t": 120, "b": 80}

            # Both templates should have the custom title font size
            assert light_dict["layout"]["title"]["font"]["size"] == 18
            assert dark_dict["layout"]["title"]["font"]["size"] == 18

        finally:
            pio.templates.default = original_default
            if "pmui_light" in pio.templates:
                del pio.templates["pmui_light"]
            if "pmui_dark" in pio.templates:
                del pio.templates["pmui_dark"]

    def test_registered_templates_are_valid(self) -> None:
        """Test that registered templates have correct structure."""
        # Store original state
        original_default = pio.templates.default

        try:
            register_pmui_templates()

            # Get registered templates
            light_template = pio.templates["pmui_light"]
            dark_template = pio.templates["pmui_dark"]

            # Test light template - Plotly returns Template objects, not dicts
            assert hasattr(light_template, "layout")
            assert hasattr(light_template, "data")
            assert light_template.layout.paper_bgcolor == "#ffffff"

            # Test dark template
            assert hasattr(dark_template, "layout")
            assert hasattr(dark_template, "data")
            assert dark_template.layout.paper_bgcolor == "#121212"

            # Both should have same structure
            assert hasattr(light_template.layout, "colorway")
            assert hasattr(dark_template.layout, "colorway")
            assert len(light_template.layout.colorway) == len(dark_template.layout.colorway)

        finally:
            # Restore original state
            pio.templates.default = original_default
            # Remove added templates
            if "pmui_light" in pio.templates:
                del pio.templates["pmui_light"]
            if "pmui_dark" in pio.templates:
                del pio.templates["pmui_dark"]

    def test_register_templates_multiple_calls(self) -> None:
        """Test that multiple calls to register don't cause issues."""
        original_default = pio.templates.default

        try:
            # Call multiple times
            register_pmui_templates()
            register_pmui_templates()
            register_pmui_templates()

            # Should still work correctly
            assert "pmui_light" in pio.templates
            assert "pmui_dark" in pio.templates
            assert pio.templates.default == "pmui_light"

            # Templates should still be valid
            light_template = pio.templates["pmui_light"]
            assert light_template["layout"]["paper_bgcolor"] == "#ffffff"

        finally:
            # Restore original state
            pio.templates.default = original_default
            if "pmui_light" in pio.templates:
                del pio.templates["pmui_light"]
            if "pmui_dark" in pio.templates:
                del pio.templates["pmui_dark"]

    def test_templates_have_different_colors(self) -> None:
        """Test that light and dark templates have different color schemes."""
        original_default = pio.templates.default

        try:
            register_pmui_templates()

            light_template = pio.templates["pmui_light"]
            dark_template = pio.templates["pmui_dark"]

            # Convert to dict format for easier comparison
            light_dict = light_template.to_plotly_json() if hasattr(light_template, 'to_plotly_json') else dict(light_template)
            dark_dict = dark_template.to_plotly_json() if hasattr(dark_template, 'to_plotly_json') else dict(dark_template)

            # Background colors should be different
            assert light_dict["layout"]["paper_bgcolor"] != dark_dict["layout"]["paper_bgcolor"]
            assert light_dict["layout"]["plot_bgcolor"] != dark_dict["layout"]["plot_bgcolor"]

            # Font colors should be different
            assert light_dict["layout"]["font"]["color"] != dark_dict["layout"]["font"]["color"]

            # Grid colors should be different
            assert light_dict["layout"]["xaxis"]["gridcolor"] != dark_dict["layout"]["xaxis"]["gridcolor"]

        finally:
            # Restore original state
            pio.templates.default = original_default
            if "pmui_light" in pio.templates:
                del pio.templates["pmui_light"]
            if "pmui_dark" in pio.templates:
                del pio.templates["pmui_dark"]


class TestUpdateTemplate:
    """Test cases for update_template function."""

    def test_update_template_to_dark(self) -> None:
        """Test updating a figure to dark theme."""
        # Create a sample figure
        df = px.data.iris()
        fig = px.scatter(df, x="sepal_length", y="sepal_width")

        # Register templates first
        register_pmui_templates()

        # Update to dark theme
        updated_fig = update_template(fig, dark_theme=True)

        assert isinstance(updated_fig, go.Figure)
        # Verify that a template was applied (template should not be None)
        assert updated_fig.layout.to_plotly_json().get("template") is not None

    def test_update_template_to_light(self) -> None:
        """Test updating a figure to light theme."""
        # Create a sample figure
        df = px.data.iris()
        fig = px.scatter(df, x="sepal_length", y="sepal_width")

        # Register templates first
        register_pmui_templates()

        # Update to light theme
        updated_fig = update_template(fig, dark_theme=False)

        assert isinstance(updated_fig, go.Figure)
        # Verify that a template was applied (template should not be None)
        assert updated_fig.layout.to_plotly_json().get("template") is not None

    def test_update_template_missing_templates(self) -> None:
        """Test error handling when templates are not registered."""
        # Clear templates
        if "pmui_light" in pio.templates:
            del pio.templates["pmui_light"]
        if "pmui_dark" in pio.templates:
            del pio.templates["pmui_dark"]

        # Create a sample figure
        df = px.data.iris()
        fig = px.scatter(df, x="sepal_length", y="sepal_width")

        # Should raise ValueError for missing template
        with pytest.raises(ValueError, match="Template 'pmui_light' not found"):
            update_template(fig, dark_theme=False)

        with pytest.raises(ValueError, match="Template 'pmui_dark' not found"):
            update_template(fig, dark_theme=True)


class TestInputValidation:
    """Test cases for input validation and error handling."""

    def test_create_template_invalid_mode(self) -> None:
        """Test error handling for invalid mode parameter."""
        with pytest.raises(ValueError, match="Mode must be 'light' or 'dark'"):
            # Use type: ignore to test runtime behavior with invalid input
            create_pmui_template("invalid_mode")  # type: ignore


class TestRobustness:
    """Test cases for robustness and edge cases."""

    def test_template_creation_with_extreme_kwargs(self) -> None:
        """Test template creation with unusual but valid kwargs."""
        template = create_pmui_template(
            "light",
            margin={"l": 0, "r": 1000, "t": 0, "b": 1000},
            font={"size": 100, "family": "Comic Sans MS"},
            title={"text": "Very Long Title " * 50}
        )

        assert template["layout"]["margin"]["l"] == 0
        assert template["layout"]["margin"]["r"] == 1000
        assert template["layout"]["font"]["size"] == 100
        assert template["layout"]["font"]["family"] == "Comic Sans MS"

    def test_multiple_registration_calls(self) -> None:
        """Test that multiple registration calls work correctly."""
        # First registration
        register_pmui_templates(primary_color="#ff0000")
        light_template_1 = pio.templates["pmui_light"]
        first_colorway = light_template_1["layout"]["colorway"]  # type: ignore

        # Second registration with different color
        register_pmui_templates(primary_color="#00ff00")
        light_template_2 = pio.templates["pmui_light"]
        second_colorway = light_template_2["layout"]["colorway"]  # type: ignore

        # Should have different colorways
        assert first_colorway != second_colorway

    def test_deep_update_preserves_unmodified_values(self) -> None:
        """Test that _deep_update preserves values not being updated."""
        base = {
            "a": {"x": 1, "y": 2},
            "b": {"z": 3},
            "c": 4
        }
        update = {
            "a": {"x": 10},  # Only update a.x
            "d": 5           # Add new key
        }

        _deep_update(base, update)

        assert base["a"]["x"] == 10  # Updated
        assert base["a"]["y"] == 2   # Preserved
        assert base["b"]["z"] == 3   # Preserved
        assert base["c"] == 4        # Preserved
        assert base["d"] == 5        # Added


class TestRegisterPmuiTemplates:
    """Test cases for register_pmui_templates function."""

    def test_register_pmui_templates_default(self) -> None:
        """Test that templates are registered correctly with defaults."""
        # Store original default to restore later
        original_default = pio.templates.default

        try:
            # Register templates
            register_pmui_templates()

            # Check that templates are registered
            assert "pmui_light" in pio.templates
            assert "pmui_dark" in pio.templates

            # Check that default is set correctly
            assert pio.templates.default == "pmui_light"

        finally:
            # Restore original default
            pio.templates.default = original_default
            # Clean up registered templates
            if "pmui_light" in pio.templates:
                del pio.templates["pmui_light"]
            if "pmui_dark" in pio.templates:
                del pio.templates["pmui_dark"]

    def test_register_pmui_templates_with_primary_color(self) -> None:
        """Test registration with custom primary color for both themes."""
        original_default = pio.templates.default

        try:
            # Register with custom primary color
            register_pmui_templates(primary_color="#9c27b0")

            # Check that templates are registered
            assert "pmui_light" in pio.templates
            assert "pmui_dark" in pio.templates

            # Convert templates to dict for easier testing
            light_template = pio.templates["pmui_light"]
            dark_template = pio.templates["pmui_dark"]

            light_dict = light_template.to_plotly_json() if hasattr(light_template, 'to_plotly_json') else dict(light_template)
            dark_dict = dark_template.to_plotly_json() if hasattr(dark_template, 'to_plotly_json') else dict(dark_template)

            # Both should have colorways derived from the same primary color
            assert len(light_dict["layout"]["colorway"]) == 10
            assert len(dark_dict["layout"]["colorway"]) == 10

        finally:
            pio.templates.default = original_default
            if "pmui_light" in pio.templates:
                del pio.templates["pmui_light"]
            if "pmui_dark" in pio.templates:
                del pio.templates["pmui_dark"]

    def test_register_pmui_templates_with_different_dark_color(self) -> None:
        """Test registration with different primary colors for light and dark themes."""
        original_default = pio.templates.default

        try:
            # Register with different colors for light and dark
            register_pmui_templates(
                primary_color="#1976d2",  # Blue for light
                primary_color_dark="#ff9800"  # Orange for dark
            )

            # Check that templates are registered
            assert "pmui_light" in pio.templates
            assert "pmui_dark" in pio.templates

            # Templates should have different colorways
            light_template = pio.templates["pmui_light"]
            dark_template = pio.templates["pmui_dark"]

            light_dict = light_template.to_plotly_json() if hasattr(light_template, 'to_plotly_json') else dict(light_template)
            dark_dict = dark_template.to_plotly_json() if hasattr(dark_template, 'to_plotly_json') else dict(dark_template)

            # Colorways should be different (derived from different primary colors)
            assert light_dict["layout"]["colorway"] != dark_dict["layout"]["colorway"]

        finally:
            pio.templates.default = original_default
            if "pmui_light" in pio.templates:
                del pio.templates["pmui_light"]
            if "pmui_dark" in pio.templates:
                del pio.templates["pmui_dark"]

    def test_register_pmui_templates_with_kwargs(self) -> None:
        """Test registration with additional kwargs."""
        original_default = pio.templates.default

        try:
            # Register with custom styling
            register_pmui_templates(
                primary_color="#6200ea",
                margin={"l": 100, "r": 100, "t": 120, "b": 80},
                title={"font": {"size": 18}}
            )

            # Check that templates are registered
            assert "pmui_light" in pio.templates
            assert "pmui_dark" in pio.templates

            # Check that customizations were applied to both templates
            light_template = pio.templates["pmui_light"]
            dark_template = pio.templates["pmui_dark"]

            light_dict = light_template.to_plotly_json() if hasattr(light_template, 'to_plotly_json') else dict(light_template)
            dark_dict = dark_template.to_plotly_json() if hasattr(dark_template, 'to_plotly_json') else dict(dark_template)

            # Both templates should have the custom margin
            assert light_dict["layout"]["margin"] == {"l": 100, "r": 100, "t": 120, "b": 80}
            assert dark_dict["layout"]["margin"] == {"l": 100, "r": 100, "t": 120, "b": 80}

            # Both templates should have the custom title font size
            assert light_dict["layout"]["title"]["font"]["size"] == 18
            assert dark_dict["layout"]["title"]["font"]["size"] == 18

        finally:
            pio.templates.default = original_default
            if "pmui_light" in pio.templates:
                del pio.templates["pmui_light"]
            if "pmui_dark" in pio.templates:
                del pio.templates["pmui_dark"]

    def test_registered_templates_are_valid(self) -> None:
        """Test that registered templates have correct structure."""
        # Store original state
        original_default = pio.templates.default

        try:
            register_pmui_templates()

            # Get registered templates
            light_template = pio.templates["pmui_light"]
            dark_template = pio.templates["pmui_dark"]

            # Test light template - Plotly returns Template objects, not dicts
            assert hasattr(light_template, "layout")
            assert hasattr(light_template, "data")
            assert light_template.layout.paper_bgcolor == "#ffffff"

            # Test dark template
            assert hasattr(dark_template, "layout")
            assert hasattr(dark_template, "data")
            assert dark_template.layout.paper_bgcolor == "#121212"

            # Both should have same structure
            assert hasattr(light_template.layout, "colorway")
            assert hasattr(dark_template.layout, "colorway")
            assert len(light_template.layout.colorway) == len(dark_template.layout.colorway)

        finally:
            # Restore original state
            pio.templates.default = original_default
            # Remove added templates
            if "pmui_light" in pio.templates:
                del pio.templates["pmui_light"]
            if "pmui_dark" in pio.templates:
                del pio.templates["pmui_dark"]

    def test_register_templates_multiple_calls(self) -> None:
        """Test that multiple calls to register don't cause issues."""
        original_default = pio.templates.default

        try:
            # Call multiple times
            register_pmui_templates()
            register_pmui_templates()
            register_pmui_templates()

            # Should still work correctly
            assert "pmui_light" in pio.templates
            assert "pmui_dark" in pio.templates
            assert pio.templates.default == "pmui_light"

            # Templates should still be valid
            light_template = pio.templates["pmui_light"]
            assert light_template["layout"]["paper_bgcolor"] == "#ffffff"

        finally:
            # Restore original state
            pio.templates.default = original_default
            if "pmui_light" in pio.templates:
                del pio.templates["pmui_light"]
            if "pmui_dark" in pio.templates:
                del pio.templates["pmui_dark"]

    def test_templates_have_different_colors(self) -> None:
        """Test that light and dark templates have different color schemes."""
        original_default = pio.templates.default

        try:
            register_pmui_templates()

            light_template = pio.templates["pmui_light"]
            dark_template = pio.templates["pmui_dark"]

            # Convert to dict format for easier comparison
            light_dict = light_template.to_plotly_json() if hasattr(light_template, 'to_plotly_json') else dict(light_template)
            dark_dict = dark_template.to_plotly_json() if hasattr(dark_template, 'to_plotly_json') else dict(dark_template)

            # Background colors should be different
            assert light_dict["layout"]["paper_bgcolor"] != dark_dict["layout"]["paper_bgcolor"]
            assert light_dict["layout"]["plot_bgcolor"] != dark_dict["layout"]["plot_bgcolor"]

            # Font colors should be different
            assert light_dict["layout"]["font"]["color"] != dark_dict["layout"]["font"]["color"]

            # Grid colors should be different
            assert light_dict["layout"]["xaxis"]["gridcolor"] != dark_dict["layout"]["xaxis"]["gridcolor"]

        finally:
            # Restore original state
            pio.templates.default = original_default
            if "pmui_light" in pio.templates:
                del pio.templates["pmui_light"]
            if "pmui_dark" in pio.templates:
                del pio.templates["pmui_dark"]

    def test_register_templates_with_custom_default(self) -> None:
        """Test registration with custom default template."""
        # Register with dark as default
        register_pmui_templates(default="pmui_dark")

        # Verify templates exist
        assert "pmui_light" in pio.templates
        assert "pmui_dark" in pio.templates

        # Verify dark is set as default
        assert pio.templates.default == "pmui_dark"

    def test_register_templates_invalid_default(self) -> None:
        """Test error handling for invalid default parameter."""
        with pytest.raises(ValueError, match="Default template 'invalid_template' not found"):
            register_pmui_templates(default="invalid_template")
