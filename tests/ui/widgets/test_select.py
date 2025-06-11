import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import Select
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


@pytest.mark.parametrize('variant', ["filled", "outlined", "standard"])
def test_select_variant(page, variant):
    widget = Select(label='Select test', variant=variant, options=["Option 1", "Option 2", "Option 3"])
    serve_component(page, widget)

    expect(page.locator(".select")).to_have_count(1)
    expect(page.locator(f".MuiSelect-{variant}")).to_have_count(1)

def test_select_disabled_options(page):
    widget = Select(name='Select test', options=["Option 1", "Option 2", "Option 3"], disabled_options=["Option 2"])
    serve_component(page, widget)

    expect(page.locator(".select")).to_have_count(1)

    page.locator(".select").click(force=True)
    expect(page.locator(".MuiMenuItem-root")).to_have_count(3)
    expect(page.locator(".MuiMenuItem-root.Mui-disabled")).to_have_text("Option 2")

def test_select_basic_functionality(page):
    widget = Select(label='Select test', options=["Option 1", "Option 2", "Option 3"])
    serve_component(page, widget)

    # Initial state
    expect(page.locator(".select")).to_have_count(1)
    expect(page.locator(".MuiSelect-select")).to_have_text("Option 1")

    # Open dropdown and select option
    page.locator(".select").click()
    expect(page.locator(".MuiMenuItem-root")).to_have_count(3)
    page.locator(".MuiMenuItem-root").nth(1).click()
    wait_until(lambda: widget.value == "Option 2", page)
    expect(page.locator(".MuiSelect-select")).to_have_text("Option 2")

def test_select_searchable(page):
    widget = Select(
        label='Select test',
        options=["Option 1", "Option 2", "Option 3", "Another Option"],
        searchable=True
    )
    serve_component(page, widget)

    # Open dropdown
    page.locator(".select").click()

    # Verify search field is present
    expect(page.locator(".MuiTextField-root")).to_have_count(1)

    # Search for an option
    page.locator(".MuiTextField-root input").fill("Another")
    expect(page.locator(".MuiMenuItem-root")).to_have_count(2)
    expect(page.locator(".MuiMenuItem-root").nth(1)).to_have_text("Another Option")

    # Select the filtered option
    page.locator(".MuiMenuItem-root").nth(1).click()
    wait_until(lambda: widget.value == "Another Option", page)

def test_select_groups(page):
    widget = Select(
        label='Select test',
        groups={
            "Group 1": ["Option 1", "Option 2"],
            "Group 2": ["Option 3", "Option 4"]
        }
    )
    serve_component(page, widget)

    # Open dropdown
    page.locator(".select").click()

    # Verify groups are displayed
    expect(page.locator(".MuiListSubheader-root")).to_have_count(2)
    expect(page.locator(".MuiListSubheader-root").nth(0)).to_have_text("Group 1")
    expect(page.locator(".MuiListSubheader-root").nth(1)).to_have_text("Group 2")

    # Select option from second group
    page.locator(".MuiMenuItem-root").nth(3).click()
    wait_until(lambda: widget.value == "Option 4", page)

@pytest.mark.parametrize('color', ["primary", "secondary", "error", "info", "success", "warning"])
def test_select_colors(page, color):
    widget = Select(label='Select test', options=["Option 1", "Option 2"], color=color)
    serve_component(page, widget)

    expect(page.locator(".select")).to_have_count(1)
    expect(page.locator(f".MuiInputBase-color{color.capitalize()}")).to_have_count(1)

@pytest.mark.parametrize('size', ["small", "large"])
def test_select_sizes(page, size):
    widget = Select(label='Select test', options=["Option 1", "Option 2"], size=size)
    serve_component(page, widget)

    expect(page.locator(".select")).to_have_count(1)
    expect(page.locator(f".MuiInputBase-size{size.capitalize()}")).to_have_count(1)

def test_select_disabled_state(page):
    widget = Select(label='Select test', options=["Option 1", "Option 2"], disabled=True)
    serve_component(page, widget)

    expect(page.locator(".select")).to_have_count(1)
    expect(page.locator(".MuiInputBase-root.Mui-disabled")).to_have_count(1)

def test_select_value_label(page):
    widget = Select(
        label='Select test',
        options=["Option 1", "Option 2"],
        value="Option 1",
        value_label="Custom Label"
    )
    serve_component(page, widget)

    expect(page.locator(".select")).to_have_count(1)
    expect(page.locator(".MuiSelect-select")).to_have_text("Custom Label")
    assert widget.value == "Option 1"

def test_select_value_updates(page):
    widget = Select(label='Select test', options=["Option 1", "Option 2"])
    serve_component(page, widget)

    # Initial state
    expect(page.locator(".MuiSelect-select")).to_have_text("Option 1")

    # Update value programmatically
    widget.value = "Option 2"
    wait_until(lambda: page.locator(".MuiSelect-select").text_content() == "Option 2", page)

    # Update to None
    widget.value = None
    wait_until(lambda: page.locator(".MuiSelect-select").text_content() == "Option 1", page)

def test_select_dict_options(page):
    widget = Select(
        label='Select test',
        options={"Option 1": 1, "Option 2": 2, "Option 3": 3}
    )
    serve_component(page, widget)

    # Open dropdown and select option
    page.locator(".select").click()
    page.locator(".MuiMenuItem-root").nth(1).click()
    wait_until(lambda: widget.value == 2, page)
    expect(page.locator(".MuiSelect-select")).to_have_text("Option 2")

def test_select_clear_selection(page):
    widget = Select(
        label='Select test',
        options=["Option 1", "Option 2"],
        value="Option 1"
    )
    serve_component(page, widget)

    # Initial state
    expect(page.locator(".MuiSelect-select")).to_have_text("Option 1")

    # Clear selection by clicking outside
    page.locator("body").click()
    page.locator(".select").click()
    page.locator(".MuiMenuItem-root").nth(0).click()
    wait_until(lambda: widget.value == "Option 1", page)

    # Try to clear by selecting empty option (should not be possible)
    page.locator(".select").click()
    expect(page.locator(".MuiMenuItem-root")).to_have_count(2)  # No empty option
