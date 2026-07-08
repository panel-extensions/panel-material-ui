import pytest

pytest.importorskip('playwright')

from bokeh.models.formatters import PrintfTickFormatter
from panel import config
from panel.tests.util import serve_component, wait_until
from panel_material_ui.widgets import EditableFloatSlider, EditableIntSlider, IntSlider, Rating
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


def test_slider_focus(page):
    widget = IntSlider(value=5, start=0, end=10)
    serve_component(page, widget)
    slider = page.locator('.MuiSlider-thumb > input')
    expect(slider).to_have_count(1)
    widget.focus()
    expect(slider).to_be_focused()


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


def test_slider_label_shows_value_with_colon(page):
    widget = IntSlider(value=5, start=0, end=10, label='Count')
    serve_component(page, widget)

    expect(page.locator('.MuiFormLabel-root')).to_have_text('Count: 5')


def test_slider_label_no_trailing_colon_when_value_hidden(page):
    widget = IntSlider(value=5, start=0, end=10, label='Count', show_value=False)
    serve_component(page, widget)

    expect(page.locator('.MuiFormLabel-root')).to_have_text('Count')


@pytest.mark.parametrize('size', ["small", "medium", "large"])
def test_rating(page, size):
    widget = Rating(value=3, size=size)
    serve_component(page, widget)

    rating = page.locator('.rating')
    expect(rating).to_have_count(1)

    rating_size = page.locator(f'.MuiRating-size{size.capitalize()}')
    expect(rating_size).to_have_count(1)


# --- EditableIntSlider / EditableFloatSlider throttled tests ---

@pytest.mark.parametrize('widget_cls,initial,new_val,expected', [
    (EditableIntSlider, 10, '20', 20),
    (EditableFloatSlider, 1.0, '2.5', 2.5),
])
def test_editable_slider_text_input_updates_value_throttled(page, widget_cls, initial, new_val, expected):
    with config.set(throttled=True):
        widget = widget_cls(value=initial, start=0, end=100)
        serve_component(page, widget)

        inp = page.locator("input[type='text']")
        inp.fill(new_val)
        inp.press("Enter")

        wait_until(lambda: widget.value_throttled == expected, page)
        assert widget.value == expected


@pytest.mark.parametrize('widget_cls,initial,new_val,expected', [
    (EditableIntSlider, 10, '20', 20),
    (EditableFloatSlider, 1.0, '2.5', 2.5),
])
def test_editable_slider_blur_updates_value_throttled(page, widget_cls, initial, new_val, expected):
    with config.set(throttled=True):
        widget = widget_cls(value=initial, start=0, end=100)
        serve_component(page, widget)

        inp = page.locator("input[type='text']")
        inp.fill(new_val)
        inp.blur()

        wait_until(lambda: widget.value_throttled == expected, page)
        assert widget.value == expected


@pytest.mark.parametrize('widget_cls,initial,expected', [
    (EditableIntSlider, 10, 11),
    (EditableFloatSlider, 1.0, 1.1),
])
def test_editable_slider_increment_button_updates_value_throttled(page, widget_cls, initial, expected):
    with config.set(throttled=True):
        widget = widget_cls(value=initial, start=0, end=100, step=1 if widget_cls is EditableIntSlider else 0.1)
        serve_component(page, widget)

        page.locator(".MuiIconButton-root").nth(0).click()

        wait_until(lambda: widget.value_throttled == pytest.approx(expected, abs=1e-9), page)
        assert widget.value == pytest.approx(expected, abs=1e-9)


@pytest.mark.parametrize('widget_cls,initial,expected', [
    (EditableIntSlider, 10, 9),
    (EditableFloatSlider, 1.0, 0.9),
])
def test_editable_slider_decrement_button_updates_value_throttled(page, widget_cls, initial, expected):
    with config.set(throttled=True):
        widget = widget_cls(value=initial, start=0, end=100, step=1 if widget_cls is EditableIntSlider else 0.1)
        serve_component(page, widget)

        page.locator(".MuiIconButton-root").nth(1).click()

        wait_until(lambda: widget.value_throttled == pytest.approx(expected, abs=1e-9), page)
        assert widget.value == pytest.approx(expected, abs=1e-9)
