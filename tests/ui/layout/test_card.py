import pytest

pytest.importorskip('playwright')

from panel.layout import Column
from panel.widgets import Button
from panel.tests.util import serve_component, wait_until
from panel_material_ui.layout import Card
from playwright.sync_api import expect

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

def test_card_basic(page):
    content = Column("Card Content")
    widget = Card(
        title="Test Card",
        objects=[content]
    )
    serve_component(page, widget)

    # Check card structure
    card = page.locator('.MuiCard-root')
    expect(card).to_have_count(1)

    # Check header
    header = page.locator('.MuiCardHeader-root')
    expect(header).to_contain_text("Test Card")

    # Check content
    content = page.locator('.MuiCardContent-root')
    expect(content).to_contain_text("Card Content")

def test_card_hide_header(page):
    content = Column("Card Content")
    widget = Card(
        title="Test Card",
        objects=[content],
        hide_header=True
    )
    serve_component(page, widget)

    # Header should not exist
    header = page.locator('.MuiCardHeader-root')
    expect(header).to_have_count(0)

def test_card_collapsible(page):
    content = Column("Card Content")
    widget = Card(
        title="Test Card",
        objects=[content],
        collapsible=True
    )
    serve_component(page, widget)

    # Check expand button exists
    expand_button = page.locator('.MuiCardHeader-action button')
    expect(expand_button).to_have_count(1)

    # Initially expanded
    content = page.locator('.MuiCardContent-root')
    expect(content).to_be_visible()

    # Click to collapse
    expand_button.click()
    expect(content).not_to_be_visible()
    wait_until(lambda: widget.collapsed == True, page)

    # Click to expand
    expand_button.click()
    expect(content).to_be_visible()
    wait_until(lambda: widget.collapsed == False, page)

def test_card_custom_header(page):
    header = Button(name="Custom Header")
    content = Column("Card Content")
    widget = Card(
        header=header,
        objects=[content]
    )
    serve_component(page, widget)

    # Check custom header is rendered
    header_content = page.locator('.MuiCardHeader-content')
    expect(header_content).to_contain_text("Custom Header")

def test_card_nested_components(page):
    button = Button(name="Click Me")
    widget = Card(
        title="Test Card",
        objects=[button]
    )
    serve_component(page, widget)

    # Check if button is interactive
    page.locator('.bk-btn').click()
    wait_until(lambda: button.clicks == 1, page)

def test_card_square(page):
    content = Column("Card Content")
    widget = Card(
        title="Test Card",
        objects=[content],
        square=True
    )
    serve_component(page, widget)

    # Check if square class is applied
    card = page.locator('.MuiCard-root')
    expect(card).to_have_css('border-radius', '0px')

def test_card_elevation(page):
    content = Column("Card Content")
    widget = Card(
        title="Test Card",
        objects=[content],
        elevation=5
    )
    serve_component(page, widget)

    card = page.locator('.MuiCard-root.MuiPaper-elevation5')
    expect(card).to_have_count(1)

def test_card_header_styling(page):
    content = Column("Card Content")
    widget = Card(
        title="Test Card",
        objects=[content],
        header_background="#0000ff",
        header_color="#ffffff"
    )
    serve_component(page, widget)

    header = page.locator('.MuiCardHeader-root')
    expect(header).to_have_css('background-color', 'rgb(0, 0, 255)')
    expect(header).to_have_css('color', 'rgb(255, 255, 255)')

def test_card_multiple_objects(page):
    content1 = Column("Content 1")
    content2 = Column("Content 2")
    widget = Card(
        title="Test Card",
        objects=[content1, content2]
    )
    serve_component(page, widget)

    content = page.locator('.MuiCardContent-root')
    expect(content).to_contain_text("Content 1")
    expect(content).to_contain_text("Content 2")

def test_card_collapse_unmount(page):
    button = Button(name="Click Me")
    widget = Card(
        title="Test Card",
        objects=[button],
        collapsible=True,
        collapsed=True
    )
    serve_component(page, widget)

    # Content should not be in DOM when collapsed
    content = page.locator('.MuiCardContent-root')
    expect(content).to_have_count(0)

    # Expand and check content appears
    page.locator('.MuiCardHeader-action button').click()
    expect(content).to_have_count(1)
