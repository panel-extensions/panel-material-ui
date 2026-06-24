"""
Responsive-by-intent widget sizing.

A stretch/scale ``sizing_mode`` drops the fixed default width/height so the
widget fills its container (like a core Panel widget), while standalone widgets
keep their default size and explicitly provided sizes are respected.
"""
import pytest

from panel_material_ui.widgets import (
    EditableRangeSlider, IntSlider, RangeSlider, Select, TextInput,
)

RESPONSIVE_WIDGETS = [IntSlider, RangeSlider, Select, TextInput]


@pytest.mark.parametrize("cls", RESPONSIVE_WIDGETS)
def test_default_width_preserved(cls):
    # A standalone widget keeps its pleasant default size.
    assert cls().width == 300


@pytest.mark.parametrize("cls", RESPONSIVE_WIDGETS)
def test_stretch_width_drops_default(cls):
    # Opting into width-responsiveness drops the fixed default so it fills.
    assert cls(sizing_mode="stretch_width").width is None


def test_stretch_both_drops_width_default():
    assert IntSlider(sizing_mode="stretch_both").width is None


def test_non_responsive_sizing_mode_keeps_default():
    assert IntSlider(sizing_mode="fixed").width == 300


def test_explicit_width_respected_with_stretch():
    # An explicit width is never dropped; Panel converts it to min_width.
    w = IntSlider(width=250, sizing_mode="stretch_width")
    assert w.min_width == 250


def test_explicit_width_without_stretch():
    assert IntSlider(width=250).width == 250


def test_editable_range_slider_stretch():
    assert EditableRangeSlider(sizing_mode="stretch_width").width is None


def test_vertical_stretch_height_fills():
    # Vertical sliders swap width<->height at render, so stretch_height must
    # drop the WIDTH param (which drives the visual height).
    assert IntSlider(orientation="vertical", sizing_mode="stretch_height").width is None


def test_vertical_extent_not_regressed():
    # A vertical slider's height comes from width=300; it must be preserved for
    # the default and for the (orthogonal) stretch_width case.
    assert IntSlider(orientation="vertical").width == 300
    assert IntSlider(orientation="vertical", sizing_mode="stretch_width").width == 300
