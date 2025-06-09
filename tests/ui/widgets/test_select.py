import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import AutocompleteInput, Select, RadioBoxGroup, RadioButtonGroup, CheckButtonGroup
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_autocomplete_input_value_updates(page):
    widget = AutocompleteInput(name='Autocomplete Input test', options=["Option 1", "Option 2", "123"])
    serve_component(page, widget)

    expect(page.locator(".autocomplete-input")).to_have_count(1)

    page.locator("input").fill("Option 2")
    page.locator(".MuiAutocomplete-option").click()

    wait_until(lambda: widget.value == 'Option 2', page)

def test_autocomplete_dict_options(page):
    widget = AutocompleteInput(name='Autocomplete Input test', options={"Option 1": 1, "Option 2": 2, "123": 123})
    serve_component(page, widget)

    expect(page.locator(".autocomplete-input")).to_have_count(1)

    page.locator("input").fill("Option 2")
    page.locator(".MuiAutocomplete-option").click()

    wait_until(lambda: widget.value == 2, page)

def test_autocomplete_input_value_updates_unrestricted(page):
    widget = AutocompleteInput(name='Autocomplete Input test', options=["Option 1", "Option 2", "123"], restrict=False)
    serve_component(page, widget)

    expect(page.locator(".autocomplete-input")).to_have_count(1)

    page.locator("input").fill("Option 3")
    page.locator("input").press("Enter")

    wait_until(lambda: widget.value == 'Option 3', page)

@pytest.mark.parametrize('variant', ["filled", "outlined", "standard"])
def test_autocomplete_input_variant(page, variant):
    widget = AutocompleteInput(name='Autocomplete Input test', variant=variant, options=["Option 1", "Option 2", "123"])
    serve_component(page, widget)

    expect(page.locator(".autocomplete-input")).to_have_count(1)
    expect(page.locator(f"div[variant='{variant}']")).to_have_count(1)

def test_autocomplete_input_search_strategy(page):
    widget = AutocompleteInput(name='Autocomplete Input test', options=["Option 1", "Option 2", "123"])
    serve_component(page, widget)

    expect(page.locator(".autocomplete-input")).to_have_count(1)

    page.locator("input").fill("Option")
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(2)

    page.locator("input").fill("ti")
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(0)

    widget.search_strategy = "includes"
    page.locator("input").fill("tion")
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(2)

def test_autocomplete_input_case_sensitive(page):
    widget = AutocompleteInput(name='Autocomplete Input test', options=["Option 1", "Option 2", "123"])
    serve_component(page, widget)

    expect(page.locator(".autocomplete-input")).to_have_count(1)

    page.locator("input").fill("opt")
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(0)

    widget.case_sensitive = False

    page.locator("input").fill("option")
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(2)

def test_autocomplete_min_characters(page):
    widget = AutocompleteInput(name='Autocomplete Input test', options=["Option 1", "Option 2", "123"])
    serve_component(page, widget)

    expect(page.locator(".autocomplete-input")).to_have_count(1)

    page.locator("input").fill("O")
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(0)
    page.locator("input").fill("")

    widget.min_characters = 1

    page.locator("input").fill("O")
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(2)

def test_autocomplete_input_enter_completion(page):
    widget = AutocompleteInput(name='Autocomplete Input test', options=["Option 1", "Option 2", "123"])
    serve_component(page, widget)

    expect(page.locator(".autocomplete-input")).to_have_count(1)

    # Test partial match completion on enter
    page.locator("input").fill("Opt")
    page.locator("input").press("Enter")
    wait_until(lambda: widget.value == 'Option 1', page)

    # Test exact match completion on enter
    page.locator("input").fill("Option 2")
    page.locator("input").press("Enter")
    wait_until(lambda: widget.value == 'Option 2', page)

    # Test no completion when no match
    page.locator("input").fill("No Match")
    page.locator("input").press("Enter")
    wait_until(lambda: widget.value == 'Option 2', page)  # Value should not change

def test_autocomplete_input_unrestricted_enter(page):
    widget = AutocompleteInput(name='Autocomplete Input test', options=["Option 1", "Option 2", "123"], restrict=False)
    serve_component(page, widget)

    expect(page.locator(".autocomplete-input")).to_have_count(1)

    # Test entering custom value
    page.locator("input").fill("Custom Value")
    page.locator("input").press("Enter")
    wait_until(lambda: widget.value == 'Custom Value', page)

    # Test entering empty value
    page.locator("input").fill("")
    page.locator("input").press("Enter")
    wait_until(lambda: widget.value == '', page)

def test_autocomplete_input_min_characters_behavior(page):
    widget = AutocompleteInput(name='Autocomplete Input test', options=["Option 1", "Option 2", "123"], min_characters=3)
    serve_component(page, widget)

    expect(page.locator(".autocomplete-input")).to_have_count(1)

    # Test with less than min characters
    page.locator("input").fill("Op")
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(0)

    # Test with exactly min characters
    page.locator("input").fill("Opt")
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(2)

    # Test with more than min characters
    page.locator("input").fill("Opti")
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(2)

def test_autocomplete_input_search_strategy_behavior(page):
    widget = AutocompleteInput(
        name='Autocomplete Input test',
        options=["Option 1", "Option 2", "123"],
        search_strategy="includes"
    )
    serve_component(page, widget)

    expect(page.locator(".autocomplete-input")).to_have_count(1)

    # Test includes strategy
    page.locator("input").fill("tion")
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(2)

    # Change to starts_with strategy
    widget.search_strategy = "starts_with"
    page.locator("input").fill("")
    page.locator("input").fill("tion")
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(0)

    # Test starts_with strategy
    page.locator("input").fill("Opt")
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(2)

def test_autocomplete_input_case_sensitivity_behavior(page):
    widget = AutocompleteInput(
        name='Autocomplete Input test',
        options=["Option 1", "Option 2", "123"],
        case_sensitive=True
    )
    serve_component(page, widget)

    expect(page.locator(".autocomplete-input")).to_have_count(1)

    # Test case sensitive search
    page.locator("input").fill("opt")
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(0)

    # Change to case insensitive
    widget.case_sensitive = False
    page.locator("input").fill("")
    page.locator("input").fill("opt")
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(2)

def test_autocomplete_input_value_tracking(page):
    widget = AutocompleteInput(name='Autocomplete Input test', options=["Option 1", "Option 2", "123"])
    serve_component(page, widget)

    expect(page.locator(".autocomplete-input")).to_have_count(1)

    # Test value_input tracking
    page.locator("input").fill("Test Input")
    wait_until(lambda: widget.value_input == 'Test Input', page)

    # Test value updates on selection
    page.locator("input").fill("Option 1")
    page.locator(".MuiAutocomplete-option").click()
    wait_until(lambda: widget.value == 'Option 1' and widget.value_input == 'Option 1', page)

def test_autocomplete_input_clear_behavior(page):
    widget = AutocompleteInput(name='Autocomplete Input test', options=["Option 1", "Option 2", "123"])
    serve_component(page, widget)

    expect(page.locator(".autocomplete-input")).to_have_count(1)

    # Set initial value
    page.locator("input").fill("Option 1")
    page.locator(".MuiAutocomplete-option").click()
    wait_until(lambda: widget.value == 'Option 1', page)

    # Clear input
    page.locator("input").fill("")
    page.locator("input").press("Enter")
    wait_until(lambda: widget.value is None and widget.value_input == '', page)

def test_autocomplete_input_disabled_state(page):
    widget = AutocompleteInput(name='Autocomplete Input test', options=["Option 1", "Option 2", "123"], disabled=True)
    serve_component(page, widget)

    expect(page.locator(".autocomplete-input")).to_have_count(1)
    expect(page.locator("input")).to_be_disabled()

@pytest.mark.parametrize('variant', ["filled", "outlined", "standard"])
def test_select_variant(page, variant):
    widget = Select(name='Select test', variant=variant, options=["Option 1", "Option 2", "Option 3"])
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

@pytest.mark.parametrize('color', ["primary", "secondary", "error", "info", "success", "warning"])
def test_radio_box_group_color(page, color):
    widget = RadioBoxGroup(name='RadioBoxGroup test', options=["Option 1", "Option 2", "Option 3"], color=color)
    serve_component(page, widget)

    expect(page.locator(".radio-box-group")).to_have_count(1)
    expect(page.locator(f".MuiRadio-color{color.capitalize()}")).to_have_count(len(widget.options))

@pytest.mark.parametrize('inline', [True, False])
def test_radio_box_group_orientation(page, inline):
    widget = RadioBoxGroup(name='RadioBoxGroup test', options=["Option 1", "Option 2", "Option 3"], inline=inline)
    serve_component(page, widget)

    expect(page.locator(".radio-box-group")).to_have_count(1)
    if inline:
        rbg_orient = page.locator(".MuiRadioGroup-row")
        expect(rbg_orient).to_have_count(1)

@pytest.mark.parametrize('button_type', ["primary", "secondary", "error", "info", "success", "warning"])
def test_radio_button_group_color(page, button_type):
    widget = RadioButtonGroup(
        name='RadioButtonGroup test',
        options=["Option 1", "Option 2", "Option 3"],
        button_type=button_type
    )
    serve_component(page, widget)

    expect(page.locator(".radio-button-group")).to_have_count(1)
    if button_type == "error":
        option_color = page.locator(f".Mui-{button_type}")
    else:
        option_color = page.locator(f".MuiToggleButton-{button_type}")
    expect(option_color).to_have_count(len(widget.options))

@pytest.mark.parametrize('orientation', ["horizontal", "vertical"])
def test_radio_button_group_orientation(page, orientation):
    widget = RadioButtonGroup(
        name='RadioButtonGroup test',
        options=["Option 1", "Option 2", "Option 3"],
        orientation=orientation
    )
    serve_component(page, widget)

    expect(page.locator(".radio-button-group")).to_have_count(1)
    expect(page.locator(f".MuiToggleButtonGroup-{orientation}")).to_have_count(1)

@pytest.mark.parametrize('size', ["small", "medium", "large"])
def test_radio_button_group_size(page, size):
    widget = RadioButtonGroup(
        name='RadioButtonGroup test',
        options=["Option 1", "Option 2", "Option 3"],
        size=size
    )
    serve_component(page, widget)

    expect(page.locator(".radio-button-group")).to_have_count(1)
    expect(page.locator(f".MuiToggleButton-size{size.capitalize()}")).to_have_count(len(widget.options))

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
