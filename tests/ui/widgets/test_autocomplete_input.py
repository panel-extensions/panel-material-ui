import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import AutocompleteInput
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_autocomplete_input_focus(page):
    widget = AutocompleteInput(name='Autocomplete Input test', options=["Option 1", "Option 2", "123"])
    serve_component(page, widget)
    input = page.locator('.MuiInputBase-input')
    expect(input).to_have_count(1)
    widget.focus()
    expect(input).to_be_focused()

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

def test_autocomplete_lazy_search_basic(page):
    """Test basic lazy search functionality"""
    widget = AutocompleteInput(
        label='Search',
        options=['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry'],
        lazy_search=True,
        min_characters=2
    )
    serve_component(page, widget)

    # Type in the autocomplete input
    input_field = page.locator('.MuiAutocomplete-input')
    expect(input_field).to_have_count(1)

    # Type "Ba" - should trigger lazy search
    input_field.fill("Ba")
    page.wait_for_timeout(500)  # Wait for debounce and response

    # Should show filtered results (Banana)
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(1)
    expect(page.locator(".MuiAutocomplete-option")).to_have_text("Banana")

def test_autocomplete_lazy_search_min_characters(page):
    """Test that lazy search respects min_characters"""
    widget = AutocompleteInput(
        label='Search',
        options=['Apple', 'Banana', 'Cherry'],
        lazy_search=True,
        min_characters=3
    )
    serve_component(page, widget)

    input_field = page.locator('.MuiAutocomplete-input')

    # Type "Ba" - should not trigger search (only 2 characters)
    input_field.fill("Ba")
    page.wait_for_timeout(500)

    # Should show no options (below min_characters)
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(0)

    # Type "Ban" - should trigger search (3 characters)
    input_field.fill("Ban")
    page.wait_for_timeout(500)

    # Should show filtered results
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(1)

def test_autocomplete_lazy_search_case_sensitive(page):
    """Test lazy search with case sensitivity"""

    widget = AutocompleteInput(
        label='Search',
        options=['Apple', 'Banana', 'Cherry'],
        lazy_search=True,
        case_sensitive=True,
        min_characters=2
    )
    serve_component(page, widget)

    input_field = page.locator('.MuiAutocomplete-input')

    # Type "ba" (lowercase) with case_sensitive=True
    input_field.fill("ba")
    page.wait_for_timeout(500)

    # Should not find "Banana" (case mismatch)
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(0)

    # Type "Ba" (capital B) - should find Banana
    input_field.fill("Ba")
    page.wait_for_timeout(500)
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(1)

def test_autocomplete_lazy_search_case_insensitive(page):
    """Test lazy search with case insensitive"""
    widget = AutocompleteInput(
        label='Search',
        options=['Apple', 'Banana', 'Cherry'],
        lazy_search=True,
        case_sensitive=False,
        min_characters=2
    )
    serve_component(page, widget)

    input_field = page.locator('.MuiAutocomplete-input')

    # Type "ba" (lowercase) with case_sensitive=False
    input_field.fill("ba")
    page.wait_for_timeout(500)

    # Should find "Banana" (case insensitive)
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(1)
    expect(page.locator(".MuiAutocomplete-option")).to_have_text("Banana")

def test_autocomplete_lazy_search_includes_strategy(page):
    """Test lazy search with includes search strategy"""
    widget = AutocompleteInput(
        label='Search',
        options=['Apple', 'Banana', 'Cherry', 'Pineapple'],
        lazy_search=True,
        search_strategy='includes',
        min_characters=2,
        case_sensitive=False
    )
    serve_component(page, widget)

    input_field = page.locator('.MuiAutocomplete-input')

    # Type "app" - should find both Apple and Pineapple (includes strategy)
    input_field.fill("app")
    page.wait_for_timeout(500)

    # Should show filtered results
    options = page.locator(".MuiAutocomplete-option")
    expect(options).to_have_count(2)
    expect(options.nth(0)).to_have_text("Apple")
    expect(options.nth(1)).to_have_text("Pineapple")

def test_autocomplete_lazy_search_starts_with_strategy(page):
    """Test lazy search with starts_with search strategy"""
    widget = AutocompleteInput(
        label='Search',
        options=['Apple', 'Banana', 'Cherry', 'Pineapple'],
        lazy_search=True,
        search_strategy='starts_with',
        min_characters=2,
        case_sensitive=False
    )
    serve_component(page, widget)

    input_field = page.locator('.MuiAutocomplete-input')

    # Type "app" - should only find Apple (starts_with strategy)
    input_field.fill("app")
    page.wait_for_timeout(500)

    # Should show only Apple (Pineapple doesn't start with "app")
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(1)
    expect(page.locator(".MuiAutocomplete-option")).to_have_text("Apple")

def test_autocomplete_lazy_search_vs_local(page):
    """Test that lazy_search=False uses local filtering"""
    widget = AutocompleteInput(
        label='Search',
        options=['Apple', 'Banana', 'Cherry'],
        lazy_search=False,
        min_characters=2
    )
    serve_component(page, widget)

    input_field = page.locator('.MuiAutocomplete-input')

    # Type "Ba" - should use local filtering
    input_field.fill("Ba")
    page.wait_for_timeout(100)  # Less wait needed for local filtering

    # Should show filtered results
    expect(page.locator(".MuiAutocomplete-option")).to_have_count(1)
    expect(page.locator(".MuiAutocomplete-option")).to_have_text("Banana")
