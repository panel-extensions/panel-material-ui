import pytest

pytest.importorskip('playwright')

from panel.layout import Column
from panel.tests.util import serve_component, wait_until
from panel_material_ui.layout import Stepper
from panel_material_ui.pane import Typography
from panel_material_ui.widgets import Button
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_stepper_basic(page):
    widget = Stepper(
        ("Step 1", Column("Content 1")),
        ("Step 2", Column("Content 2")),
        ("Step 3", Column("Content 3")),
    )
    serve_component(page, widget)

    steps = page.locator('.MuiStep-root')
    expect(steps).to_have_count(3)
    expect(steps.nth(0)).to_contain_text('Step 1')
    expect(steps.nth(1)).to_contain_text('Step 2')
    expect(steps.nth(2)).to_contain_text('Step 3')


def test_stepper_component_title(page):
    widget = Stepper(
        (Typography("Step A"), Column("Content A")),
        (Typography("Step B"), Column("Content B")),
    )
    serve_component(page, widget)

    steps = page.locator('.MuiStep-root')
    expect(steps).to_have_count(2)
    expect(steps.nth(0)).to_contain_text('Step A')
    expect(steps.nth(1)).to_contain_text('Step B')


def test_stepper_initial_active(page):
    widget = Stepper(
        ("Step 1", Column("Content 1")),
        ("Step 2", Column("Content 2")),
        active=1,
    )
    serve_component(page, widget)

    # Active step should have active icon
    active_icons = page.locator('.MuiStepIcon-root.Mui-active')
    expect(active_icons).to_have_count(1)

    # Content for step 2 should be visible
    expect(page.locator('body')).to_contain_text('Content 2')


def test_stepper_non_linear_click(page):
    widget = Stepper(
        ("Step 1", Column("Content 1")),
        ("Step 2", Column("Content 2")),
        ("Step 3", Column("Content 3")),
        non_linear=True,
    )
    serve_component(page, widget)

    # Click the third step button
    step_buttons = page.locator('.MuiStepButton-root')
    expect(step_buttons).to_have_count(3)
    step_buttons.nth(2).click()

    wait_until(lambda: widget.active == 2, page)
    expect(page.locator('body')).to_contain_text('Content 3')


def test_stepper_linear_no_step_buttons(page):
    """In linear mode steps should use StepLabel, not StepButton."""
    widget = Stepper(
        ("Step 1", Column("Content 1")),
        ("Step 2", Column("Content 2")),
        non_linear=False,
    )
    serve_component(page, widget)

    step_buttons = page.locator('.MuiStepButton-root')
    expect(step_buttons).to_have_count(0)


def test_stepper_vertical(page):
    widget = Stepper(
        ("Step 1", Column("Content 1")),
        ("Step 2", Column("Content 2")),
        orientation="vertical",
    )
    serve_component(page, widget)

    stepper = page.locator('.MuiStepper-vertical')
    expect(stepper).to_have_count(1)

    # Vertical mode renders StepContent for each step
    step_content = page.locator('.MuiStepContent-root')
    expect(step_content).to_have_count(2)


def test_stepper_alternative_label(page):
    widget = Stepper(
        ("Step 1", Column("Content 1")),
        ("Step 2", Column("Content 2")),
        alternative_label=True,
    )
    serve_component(page, widget)

    stepper = page.locator('.MuiStepper-alternativeLabel')
    expect(stepper).to_have_count(1)


def test_stepper_disabled(page):
    widget = Stepper(
        ("Step 1", Column("Content 1")),
        ("Step 2", Column("Content 2")),
        ("Step 3", Column("Content 3")),
        non_linear=True,
        disabled=[1],
    )
    serve_component(page, widget)

    disabled_step = page.locator('.MuiStep-root .MuiStepButton-root.Mui-disabled')
    expect(disabled_step).to_have_count(1)

    # Click disabled step button (should not change active)
    page.locator('.MuiStepButton-root').nth(1).click(force=True)
    wait_until(lambda: widget.active == 0, page)


def test_stepper_error(page):
    widget = Stepper(
        ("Step 1", Column("Content 1")),
        ("Step 2", Column("Content 2")),
        error=[1],
    )
    serve_component(page, widget)

    error_icon = page.locator('.MuiStepIcon-root.Mui-error')
    expect(error_icon).to_have_count(1)


def test_stepper_optional_label(page):
    widget = Stepper(
        ("Step 1", Column("Content 1")),
        ("Step 2", Column("Content 2")),
        optional=[1],
    )
    serve_component(page, widget)

    expect(page.locator('body')).to_contain_text('Optional')


def test_stepper_completed(page):
    widget = Stepper(
        ("Step 1", Column("Content 1")),
        ("Step 2", Column("Content 2")),
        ("Step 3", Column("Content 3")),
        active=2,
        completed=[0, 1],
    )
    serve_component(page, widget)

    completed_icons = page.locator('.MuiStepIcon-root.Mui-completed')
    expect(completed_icons).to_have_count(2)


def test_stepper_no_connector(page):
    widget = Stepper(
        ("Step 1", Column("Content 1")),
        ("Step 2", Column("Content 2")),
        connector=False,
    )
    serve_component(page, widget)

    connectors = page.locator('.MuiStepConnector-root')
    expect(connectors).to_have_count(0)


def test_stepper_dynamic_update(page):
    content1 = Column("Content 1")
    widget = Stepper(("Step 1", content1))
    serve_component(page, widget)

    expect(page.locator('.MuiStep-root')).to_have_count(1)

    # Add another step
    content2 = Column("Content 2")
    widget.append(("Step 2", content2))
    expect(page.locator('.MuiStep-root')).to_have_count(2)


def test_stepper_nested_component(page):
    button = Button(label="Click Me")
    widget = Stepper(("Step 1", button))
    serve_component(page, widget)

    page.locator('.MuiButton-root').click()
    wait_until(lambda: button.clicks == 1, page)


def test_stepper_icons(page):
    widget = Stepper(
        ("Settings", Column("Content 1")),
        ("Group", Column("Content 2")),
        ("Video", Column("Content 3")),
        icons=["settings", "group_add", "videocam"],
    )
    serve_component(page, widget)

    # Icons replace the default numbered circles
    icons = page.locator('.material-icons')
    expect(icons).to_have_count(3)


def test_stepper_show_buttons(page):
    widget = Stepper(
        ("Step 1", Column("Content 1")),
        ("Step 2", Column("Content 2")),
        show_buttons=True,
    )
    serve_component(page, widget)

    expect(page.locator('body')).to_contain_text('Content 1')

    next_btn = page.locator('button', has_text='Next')
    back_btn = page.locator('button', has_text='Back')
    expect(next_btn).to_have_count(1)
    expect(back_btn).to_be_disabled()

    next_btn.click()
    wait_until(lambda: widget.active == 1, page)
    expect(page.locator('body')).to_contain_text('Content 2')
    expect(next_btn).to_be_disabled()


def test_stepper_show_buttons_custom_text(page):
    widget = Stepper(
        ("Step 1", Column("Content 1")),
        ("Step 2", Column("Content 2")),
        show_buttons=True,
        back_text="Prev",
        next_text="Forward",
    )
    serve_component(page, widget)

    expect(page.locator('button', has_text='Prev')).to_have_count(1)
    expect(page.locator('button', has_text='Forward')).to_have_count(1)


def test_stepper_empty(page):
    widget = Stepper()
    serve_component(page, widget)

    steps = page.locator('.MuiStep-root')
    expect(steps).to_have_count(0)


def test_stepper_compact_basic(page):
    widget = Stepper(
        Column("Content 1"),
        Column("Content 2"),
        Column("Content 3"),
        variant="compact",
    )
    serve_component(page, widget)

    # Compact variant renders a MobileStepper bar, not labelled steps
    expect(page.locator('.MuiMobileStepper-root')).to_have_count(1)
    expect(page.locator('.MuiStep-root')).to_have_count(0)
    # Active step's content is visible
    expect(page.locator('body')).to_contain_text('Content 1')


def test_stepper_compact_navigation(page):
    widget = Stepper(
        Column("Content 1"),
        Column("Content 2"),
        variant="compact",
    )
    serve_component(page, widget)

    next_btn = page.locator('button', has_text='Next')
    back_btn = page.locator('button', has_text='Back')
    expect(next_btn).to_have_count(1)
    expect(back_btn).to_be_disabled()

    next_btn.click()
    wait_until(lambda: widget.active == 1, page)
    expect(page.locator('body')).to_contain_text('Content 2')
    expect(next_btn).to_be_disabled()


def test_stepper_compact_progress_indicator(page):
    widget = Stepper(
        Column("Content 1"),
        Column("Content 2"),
        variant="compact",
        indicator="progress",
    )
    serve_component(page, widget)

    expect(page.locator('.MuiMobileStepper-progress')).to_have_count(1)


def test_stepper_compact_custom_button_text(page):
    widget = Stepper(
        Column("Content 1"),
        Column("Content 2"),
        variant="compact",
        back_text="Prev",
        next_text="Forward",
    )
    serve_component(page, widget)

    expect(page.locator('button', has_text='Prev')).to_have_count(1)
    expect(page.locator('button', has_text='Forward')).to_have_count(1)


def test_stepper_compact_nested_component(page):
    button = Button(label="Click Me")
    widget = Stepper(button, Column("Content 2"), variant="compact")
    serve_component(page, widget)

    page.locator('.MuiButton-root', has_text="Click Me").click()
    wait_until(lambda: button.clicks == 1, page)
