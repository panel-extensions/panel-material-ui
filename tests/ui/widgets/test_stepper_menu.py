import pytest

pytest.importorskip('playwright')

from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets.menus import StepperMenu
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_stepper_menu_basic(page):
    widget = StepperMenu(items=["Step 1", "Step 2", "Step 3"])
    serve_component(page, widget)

    expect(page.locator('.MuiStepper-root')).to_have_count(1)
    steps = page.locator('.MuiStep-root')
    expect(steps).to_have_count(3)
    expect(steps.nth(0)).to_contain_text('Step 1')
    expect(steps.nth(1)).to_contain_text('Step 2')
    expect(steps.nth(2)).to_contain_text('Step 3')


def test_stepper_menu_active_setting(page):
    widget = StepperMenu(items=["Step 1", "Step 2", "Step 3"], active=1)
    serve_component(page, widget)

    expect(page.locator('.MuiStepIcon-root.Mui-active')).to_have_count(1)
    assert widget.value == "Step 2"


def test_stepper_menu_non_linear_click(page):
    widget = StepperMenu(items=["Step 1", "Step 2", "Step 3"], non_linear=True)
    serve_component(page, widget)

    step_buttons = page.locator('.MuiStepButton-root')
    expect(step_buttons).to_have_count(3)
    step_buttons.nth(2).click()

    wait_until(lambda: widget.active == 2, page)
    assert widget.value == "Step 3"


def test_stepper_menu_linear_no_step_buttons(page):
    """In linear mode steps use StepLabel, not StepButton."""
    widget = StepperMenu(items=["Step 1", "Step 2"], non_linear=False)
    serve_component(page, widget)

    expect(page.locator('.MuiStepButton-root')).to_have_count(0)


def test_stepper_menu_on_click(page):
    events = []
    widget = StepperMenu(
        items=["Step 1", "Step 2", "Step 3"],
        non_linear=True,
        on_click=lambda e: events.append(e),
    )
    serve_component(page, widget)

    page.locator('.MuiStepButton-root').nth(1).click()
    wait_until(lambda: len(events) == 1, page)
    assert events[0] == "Step 2"


def test_stepper_menu_icons(page):
    widget = StepperMenu(items=[
        {"label": "Settings", "icon": "settings"},
        {"label": "Group", "icon": "group_add"},
    ])
    serve_component(page, widget)

    icons = page.locator('.material-icons')
    expect(icons).to_have_count(2)


def test_stepper_menu_error(page):
    widget = StepperMenu(items=[
        {"label": "Step 1"},
        {"label": "Step 2", "error": True},
    ])
    serve_component(page, widget)

    expect(page.locator('.MuiStepIcon-root.Mui-error')).to_have_count(1)


def test_stepper_menu_optional(page):
    widget = StepperMenu(items=[
        {"label": "Step 1"},
        {"label": "Step 2", "optional": True},
    ])
    serve_component(page, widget)

    expect(page.locator('body')).to_contain_text('Optional')


def test_stepper_menu_completed(page):
    widget = StepperMenu(items=[
        {"label": "Step 1", "completed": True},
        {"label": "Step 2", "completed": True},
        {"label": "Step 3"},
    ], active=2)
    serve_component(page, widget)

    expect(page.locator('.MuiStepIcon-root.Mui-completed')).to_have_count(2)


def test_stepper_menu_disabled(page):
    widget = StepperMenu(items=[
        {"label": "Step 1"},
        {"label": "Step 2", "disabled": True},
        {"label": "Step 3"},
    ], non_linear=True)
    serve_component(page, widget)

    expect(page.locator('.MuiStepButton-root.Mui-disabled')).to_have_count(1)


def test_stepper_menu_no_connector(page):
    widget = StepperMenu(items=["Step 1", "Step 2"], connector=False)
    serve_component(page, widget)

    expect(page.locator('.MuiStepConnector-root')).to_have_count(0)


def test_stepper_menu_alternative_label(page):
    widget = StepperMenu(items=["Step 1", "Step 2"], alternative_label=True)
    serve_component(page, widget)

    expect(page.locator('.MuiStepper-alternativeLabel')).to_have_count(1)


def test_stepper_menu_compact_basic(page):
    widget = StepperMenu(items=["Step 1", "Step 2", "Step 3"], variant="compact")
    serve_component(page, widget)

    expect(page.locator('.MuiMobileStepper-root')).to_have_count(1)
    expect(page.locator('.MuiStep-root')).to_have_count(0)


def test_stepper_menu_compact_navigation(page):
    widget = StepperMenu(items=["Step 1", "Step 2"], variant="compact")
    serve_component(page, widget)

    next_btn = page.locator('button', has_text='Next')
    back_btn = page.locator('button', has_text='Back')
    expect(next_btn).to_have_count(1)
    expect(back_btn).to_be_disabled()

    next_btn.click()
    wait_until(lambda: widget.active == 1, page)
    expect(next_btn).to_be_disabled()


def test_stepper_menu_compact_progress_indicator(page):
    widget = StepperMenu(items=["Step 1", "Step 2"], variant="compact", indicator="progress")
    serve_component(page, widget)

    expect(page.locator('.MuiMobileStepper-progress')).to_have_count(1)


def test_stepper_menu_compact_custom_button_text(page):
    widget = StepperMenu(
        items=["Step 1", "Step 2"],
        variant="compact",
        back_text="Prev",
        next_text="Forward",
    )
    serve_component(page, widget)

    expect(page.locator('button', has_text='Prev')).to_have_count(1)
    expect(page.locator('button', has_text='Forward')).to_have_count(1)
