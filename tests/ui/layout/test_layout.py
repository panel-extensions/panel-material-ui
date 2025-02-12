import pytest

pytest.importorskip('playwright')

from panel_material_ui.layout import Card, Accordion, Tabs, Paper

from playwright.sync_api import expect
from panel.tests.util import serve_component

pytestmark = pytest.mark.ui


def test_card_default(page):
    layout = Card(1, 2, 3, title="Card 1")
    serve_component(page, layout)

    expect(page.locator('.card')).to_have_count(1)

    action = page.locator('.MuiCardHeader-action')
    content = page.locator('.MuiCardContent-root')
    expect(action).to_have_count(1)
    expect(content).to_have_count(1)

    # collapse the card
    action.click()
    expect(content).to_have_count(0)


def test_card_collapsible(page):
    layout = Card(1, 2, 3, title="Card 1", collapsible=False)
    serve_component(page, layout)
    # card not collapsible, there's no arrow icon for collapse/expand
    expect(page.locator('.MuiCardHeader-action')).to_have_count(0)


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


def test_tabs(page):
    layout = Tabs(("Tab 1", "Tab 1 objects"), ("Tab 2", "Card 2 objects"))
    serve_component(page, layout)

    expect(page.locator('.tabs')).to_have_count(1)
    expect(page.locator('.MuiTab-root')).to_have_count(2)


def test_paper(page):
    layout = Paper(name="Paper", objects=[1, 2, 3])
    serve_component(page, layout)
    expect(page.locator('.paper')).to_have_count(1)
