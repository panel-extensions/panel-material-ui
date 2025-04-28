import pytest

pytest.importorskip('playwright')

from panel.layout import Column
from panel.widgets import Button
from panel.tests.util import serve_component, wait_until
from panel_material_ui.layout import Accordion
from playwright.sync_api import expect

pytestmark = pytest.mark.ui

def test_accordion_active(page):
    layout = Accordion(("Card 1", "Card 1 objects"), ("Card 2", "Card 2 objects"))
    serve_component(page, layout)

    expect(page.locator('.accordion')).to_have_count(1)
    # 2 collapsed cards
    cards = page.locator('.MuiAccordion-gutters')
    expect(cards).to_have_count(2)
    expanded_cards = page.locator('.MuiCollapse-entered')
    expect(expanded_cards).to_have_count(0)

    # expand the card, `active` is set properly
    card0 = cards.nth(0)
    card0.click()
    expect(expanded_cards).to_have_count(1)
    expanded_cards.wait_for(timeout=5000)
    assert layout.active == [0]
    # set `active`, the cards expanded accordingly
    layout.active = [0, 1]
    expect(page.locator('.MuiAccordionSummary-root.Mui-expanded')).to_have_count(2)

def test_accordion_basic(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Accordion(
        ('Section 1', content1),
        ('Section 2', content2)
    )
    serve_component(page, widget)

    # Check sections exist
    sections = page.locator('.MuiAccordion-root')
    expect(sections).to_have_count(2)

    # Check headers
    headers = page.locator('.MuiAccordionSummary-content')
    expect(headers.nth(0)).to_contain_text('Section 1')
    expect(headers.nth(1)).to_contain_text('Section 2')

def test_accordion_expansion(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Accordion(
        ('Section 1', content1),
        ('Section 2', content2)
    )
    serve_component(page, widget)

    # Initially no sections should be expanded
    hidden = page.locator('.MuiCollapse-hidden')
    expect(hidden).to_have_count(2)

    # Click to expand first section
    page.locator('.MuiAccordionSummary-root').first.click()
    expect(hidden).to_have_count(1)
    wait_until(lambda: widget.active == [0], page)

def test_accordion_toggle_mode(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Accordion(
        ('Section 1', content1),
        ('Section 2', content2),
        toggle=True
    )
    serve_component(page, widget)

    # Expand first section
    summaries = page.locator('.MuiAccordionSummary-root')
    summaries.nth(0).click()
    wait_until(lambda: widget.active == [0], page)

    # Expand second section (should collapse first in toggle mode)
    summaries.nth(1).click()
    wait_until(lambda: widget.active == [1], page)
    hidden = page.locator('.MuiCollapse-hidden')
    expect(hidden).to_have_count(1)

def test_accordion_multiple_sections(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Accordion(
        ('Section 1', content1),
        ('Section 2', content2),
        toggle=False  # Allow multiple sections to be expanded
    )
    serve_component(page, widget)

    # Expand both sections
    summaries = page.locator('.MuiAccordionSummary-root')
    summaries.nth(0).click()
    summaries.nth(1).click()

    hidden = page.locator('.MuiCollapse-hidden')
    expect(hidden).to_have_count(0)
    wait_until(lambda: sorted(widget.active) == [0, 1], page)

def test_accordion_disabled_sections(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Accordion(
        ('Section 1', content1),
        ('Section 2', content2),
        disabled=[1]  # Disable second section
    )
    serve_component(page, widget)

    # Check disabled state
    disabled = page.locator('.MuiAccordionSummary-root.Mui-disabled')
    expect(disabled).to_have_count(1)

    # Try to click disabled section (should not expand)
    page.locator('.MuiAccordionSummary-root').nth(1).click(force=True)
    hidden = page.locator('.MuiCollapse-hidden')
    expect(hidden).to_have_count(2)

def test_accordion_initial_state(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Accordion(
        ('Section 1', content1),
        ('Section 2', content2),
        active=[0]  # First section initially expanded
    )
    serve_component(page, widget)

    # Check initial expansion
    hidden = page.locator('.MuiCollapse-hidden')
    expect(hidden).to_have_count(1)
    expect(page.locator('.MuiAccordionDetails-root').nth(0)).to_contain_text('Content 1')

def test_accordion_collapse(page):
    content1 = Column("Content 1")
    widget = Accordion(
        ('Section 1', content1),
        active=[0]  # Initially expanded
    )
    serve_component(page, widget)

    # Click to collapse
    page.locator('.MuiAccordionSummary-root').click()
    hidden = page.locator('.MuiCollapse-hidden')
    expect(hidden).to_have_count(1)
    wait_until(lambda: widget.active == [], page)

def test_accordion_square_variant(page):
    content1 = Column("Content 1")
    widget = Accordion(
        ('Section 1', content1),
        square=True
    )
    serve_component(page, widget)

    # Check if square class is applied
    accordion = page.locator('.MuiAccordion-root')
    expect(accordion).to_have_css('border-radius', '0px')
