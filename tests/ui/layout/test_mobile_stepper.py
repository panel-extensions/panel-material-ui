import pytest

pytest.importorskip('playwright')

from panel.layout import Column
from panel.tests.util import serve_component, wait_until
from panel_material_ui.layout import MobileStepper
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_mobile_stepper_dots(page):
    widget = MobileStepper(
        Column("Content 1"),
        Column("Content 2"),
        Column("Content 3"),
        variant="dots",
    )
    serve_component(page, widget)

    dots = page.locator('.MuiMobileStepper-dot')
    expect(dots).to_have_count(3)

    active_dot = page.locator('.MuiMobileStepper-dotActive')
    expect(active_dot).to_have_count(1)


def test_mobile_stepper_progress(page):
    widget = MobileStepper(
        Column("Content 1"),
        Column("Content 2"),
        variant="progress",
    )
    serve_component(page, widget)

    progress = page.locator('.MuiLinearProgress-root')
    expect(progress).to_have_count(1)


def test_mobile_stepper_text(page):
    widget = MobileStepper(
        Column("Content 1"),
        Column("Content 2"),
        Column("Content 3"),
        variant="text",
        active=1,
    )
    serve_component(page, widget)

    stepper = page.locator('.MuiMobileStepper-root')
    expect(stepper).to_contain_text('2 / 3')


def test_mobile_stepper_next(page):
    widget = MobileStepper(
        Column("Content 1"),
        Column("Content 2"),
    )
    serve_component(page, widget)

    expect(page.locator('body')).to_contain_text('Content 1')

    page.locator('button', has_text='Next').click()
    wait_until(lambda: widget.active == 1, page)
    expect(page.locator('body')).to_contain_text('Content 2')


def test_mobile_stepper_back(page):
    widget = MobileStepper(
        Column("Content 1"),
        Column("Content 2"),
        active=1,
    )
    serve_component(page, widget)

    expect(page.locator('body')).to_contain_text('Content 2')

    page.locator('button', has_text='Back').click()
    wait_until(lambda: widget.active == 0, page)
    expect(page.locator('body')).to_contain_text('Content 1')


def test_mobile_stepper_next_disabled_at_end(page):
    widget = MobileStepper(
        Column("Content 1"),
        Column("Content 2"),
        active=1,
    )
    serve_component(page, widget)

    next_button = page.locator('button', has_text='Next')
    expect(next_button).to_be_disabled()


def test_mobile_stepper_back_disabled_at_start(page):
    widget = MobileStepper(
        Column("Content 1"),
        Column("Content 2"),
    )
    serve_component(page, widget)

    back_button = page.locator('button', has_text='Back')
    expect(back_button).to_be_disabled()


def test_mobile_stepper_custom_button_text(page):
    widget = MobileStepper(
        Column("Content 1"),
        Column("Content 2"),
        back_text="Prev",
        next_text="Forward",
    )
    serve_component(page, widget)

    expect(page.locator('button', has_text='Prev')).to_have_count(1)
    expect(page.locator('button', has_text='Forward')).to_have_count(1)


def test_mobile_stepper_empty(page):
    widget = MobileStepper()
    serve_component(page, widget)

    stepper = page.locator('.MuiMobileStepper-root')
    expect(stepper).to_have_count(1)
