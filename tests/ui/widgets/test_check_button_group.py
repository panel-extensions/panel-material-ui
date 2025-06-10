import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component
from panel_material_ui.widgets import CheckButtonGroup
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


@pytest.mark.parametrize('button_type', ["primary", "secondary", "error", "info", "success", "warning"])
def test_check_button_group_color(page, button_type):
    widget = CheckButtonGroup(
        name='CheckButtonGroup test',
        value=[],
        options=["Option 1", "Option 2", "Option 3"],
        button_type=button_type
    )
    serve_component(page, widget)

    expect(page.locator(".check-button-group")).to_have_count(1)
    if button_type == "error":
        option_color = page.locator(f".Mui-{button_type}")
    else:
        option_color = page.locator(f".MuiToggleButton-{button_type}")
    expect(option_color).to_have_count(len(widget.options))

@pytest.mark.parametrize('orientation', ["horizontal", "vertical"])
def test_check_button_group_orientation(page, orientation):
    widget = CheckButtonGroup(
        name='CheckButtonGroup test',
        value=[],
        options=["Option 1", "Option 2", "Option 3"],
        orientation=orientation
    )
    serve_component(page, widget)

    expect(page.locator(".check-button-group")).to_have_count(1)
    expect(page.locator(f".MuiToggleButtonGroup-{orientation}")).to_have_count(1)

@pytest.mark.parametrize('size', ["small", "medium", "large"])
def test_check_button_group_size(page, size):
    widget = CheckButtonGroup(
        name='CheckButtonGroup test',
        value=[],
        options=["Option 1", "Option 2", "Option 3"],
        size=size
    )
    serve_component(page, widget)

    expect(page.locator(".check-button-group")).to_have_count(1)
    expect(page.locator(f".MuiToggleButton-size{size.capitalize()}")).to_have_count(len(widget.options))

def test_check_button_group_selection(page):
    widget = CheckButtonGroup(
        name='CheckButtonGroup test',
        value=[],
        options=["Option 1", "Option 2", "Option 3"],
    )
    serve_component(page, widget)

    # Test initial state
    expect(page.locator(".check-button-group")).to_have_count(1)
    expect(page.locator(".Mui-selected")).to_have_count(0)

    # Test selecting first option
    page.locator("text=Option 1").click()
    expect(page.locator(".Mui-selected")).to_have_count(1)
    expect(page.locator(".Mui-selected")).to_have_text("Option 1")

    # Test selecting second option
    page.locator("text=Option 2").click()
    expect(page.locator(".Mui-selected")).to_have_count(2)
    expect(page.locator(".Mui-selected").nth(1)).to_have_text("Option 2")

    # Test deselecting first option
    page.locator("text=Option 1").click()
    expect(page.locator(".Mui-selected")).to_have_count(1)
    expect(page.locator(".Mui-selected")).to_have_text("Option 2")

def test_check_button_group_disabled(page):
    widget = CheckButtonGroup(
        name='CheckButtonGroup test',
        value=[],
        options=["Option 1", "Option 2", "Option 3"],
        disabled=True
    )
    serve_component(page, widget)

    expect(page.locator(".MuiToggleButton-root.Mui-disabled")).to_have_count(3)

def test_check_button_group_label(page):
    widget = CheckButtonGroup(
        name='CheckButtonGroup test',
        label='Test Label',
        value=[],
        options=["Option 1", "Option 2", "Option 3"],
    )
    serve_component(page, widget)

    expect(page.locator("text=Test Label")).to_be_visible()
    expect(page.locator("label")).to_have_text("Test Label")

def test_check_button_group_width(page):
    widget = CheckButtonGroup(
        name='CheckButtonGroup test',
        value=[],
        options=["Option 1", "Option 2", "Option 3"],
        width=400
    )
    serve_component(page, widget)

    # Get the computed width of the button group
    width = page.locator(".check-button-group").evaluate("el => el.getBoundingClientRect().width")
    # Allow for some margin of error in the width calculation
    assert abs(width - 400) < 10

def test_check_button_group_initial_value(page):
    widget = CheckButtonGroup(
        name='CheckButtonGroup test',
        value=["Option 1", "Option 3"],
        options=["Option 1", "Option 2", "Option 3"],
    )
    serve_component(page, widget)

    # Verify initial selected state
    expect(page.locator(".Mui-selected")).to_have_count(2)
    expect(page.locator(".Mui-selected").nth(0)).to_have_text("Option 1")
    expect(page.locator(".Mui-selected").nth(1)).to_have_text("Option 3")
