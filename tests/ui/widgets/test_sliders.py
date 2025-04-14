import pytest

pytest.importorskip('playwright')

from bokeh.models.formatters import PrintfTickFormatter
from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import IntSlider, Rating
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_int_slider(page):
    widget = IntSlider(value=5, start=0, end=10)
    serve_component(page, widget)

    slider = page.locator('.int-slider')
    expect(slider).to_have_count(1)

    slider_value = page.locator('.MuiFormLabel-root')
    expect(slider_value).to_have_text(str(widget.value))


def test_slider_value_update(page):
    widget = IntSlider(value=5, start=0, end=10)
    serve_component(page, widget)
    slider_value = page.locator('.MuiFormLabel-root')

    for i in range(widget.start, widget.end, widget.step):
        widget.value = i
        expect(slider_value).to_have_text(str(i))


@pytest.mark.parametrize('color', ['primary', 'secondary', 'error', 'info', 'success', 'warning'])
def test_slider_color(page, color):
    widget = IntSlider(value=5, start=0, end=10, color=color)
    serve_component(page, widget)

    expect(page.locator(f'.MuiSlider-color{color.capitalize()}')).to_have_count(1)


@pytest.mark.parametrize('track', ["inverted", False])
def test_slider_track(page, track):
    widget = IntSlider(value=5, start=0, end=10, track=track)
    serve_component(page, widget)
    expect(page.locator(f'.MuiSlider-track{str(track).capitalize()}')).to_have_count(1)


def test_slider_vertical_orientation(page):
    widget = IntSlider(value=5, start=0, end=10, orientation='vertical')

    serve_component(page, widget)

    expect(page.locator(f'.MuiSlider-vertical')).to_have_count(1)
    assert page.locator('.MuiSlider-rail').evaluate("el => el.offsetHeight") == 277


def test_slider_format_str(page):
    widget = IntSlider(value=1101, start=0, end=2000, format='0a')

    serve_component(page, widget)

    expect(page.locator('.MuiFormLabel-root')).to_have_text('1k')

    widget.value = 2000

    expect(page.locator('.MuiFormLabel-root')).to_have_text('2k')


def test_slider_format_model(page):
    widget = IntSlider(value=1, start=0, end=10, format=PrintfTickFormatter(format='%d m'))

    serve_component(page, widget)

    expect(page.locator('.MuiFormLabel-root')).to_have_text('1 m')

    widget.value = 7

    expect(page.locator('.MuiFormLabel-root')).to_have_text('7 m')


@pytest.mark.parametrize('size', ["small", "medium", "large"])
def test_rating(page, size):
    widget = Rating(value=3, size=size)
    serve_component(page, widget)

    rating = page.locator('.rating')
    expect(rating).to_have_count(1)

    rating_size = page.locator(f'.MuiRating-size{size.capitalize()}')
    expect(rating_size).to_have_count(1)
