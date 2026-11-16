import time

import pytest

pytest.importorskip('playwright')

from bokeh.models.formatters import PrintfTickFormatter
from panel import config
from panel.tests.util import serve_component, wait_until
from playwright.sync_api import expect

from panel_material_ui.layout import Column, Row
from panel_material_ui.widgets import (
    DiscreteSlider,
    EditableFloatSlider,
    EditableIntRangeSlider,
    EditableIntSlider,
    FloatSlider,
    IntSlider,
    LinearProgress,
    RangeSlider,
    Rating,
)

pytestmark = pytest.mark.ui


def test_linear_progress_max(page):
    """Absolute progress is scaled by max and responds to updates."""
    widget = LinearProgress(value=50, max=200)
    serve_component(page, widget)
    bar = page.locator('.MuiLinearProgress-bar')
    expect(bar).to_have_attribute('style', 'transform: translateX(-75%);')
    widget.value = 100
    expect(bar).to_have_attribute('style', 'transform: translateX(-50%);')
    widget.max = 100
    expect(bar).to_have_attribute('style', 'transform: translateX(0%);')


def test_discrete_slider_formatter(page):
    """Numeric option labels update without changing the selected value."""
    widget = DiscreteSlider(options=[1.234, 2.456], value=1.234, formatter='%.1f')
    serve_component(page, widget)
    expect(page.locator('.MuiFormLabel-root')).to_have_text('1.2')
    widget.formatter = '%.2f'
    expect(page.locator('.MuiFormLabel-root')).to_have_text('1.23')
    assert widget.value == 1.234


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

    expect(page.locator('.MuiSlider-vertical')).to_have_count(1)
    assert page.locator('.MuiSlider-rail').evaluate("el => el.offsetHeight") == 277


@pytest.mark.parametrize('size', ['small', 'medium'])
def test_range_slider_thumbs_stay_within_widget(page, size):
    widget = RangeSlider(value=(0, 10), start=0, end=10, size=size, width=300)
    serve_component(page, widget)

    root = page.locator('.MuiFormControl-root').bounding_box()
    thumbs = page.locator('.MuiSlider-thumb')
    expect(thumbs).to_have_count(2)
    first, last = thumbs.nth(0).bounding_box(), thumbs.nth(1).bounding_box()
    assert first['x'] == pytest.approx(root['x'], abs=1)
    assert last['x'] + last['width'] == pytest.approx(root['x'] + root['width'], abs=1)


def test_slider_bar_color(page):
    widget = IntSlider(value=5, start=0, end=10, bar_color='#ff0000')
    serve_component(page, widget)

    expect(page.locator('.MuiSlider-track')).to_have_css('background-color', 'rgb(255, 0, 0)')


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
    warnings = []
    page.on('console', lambda message: warnings.append(message.text) if message.type == 'warning' else None)
    widget = Rating(value=3, size=size)
    serve_component(page, widget)

    rating = page.locator('.rating')
    expect(rating).to_have_count(1)

    rating_size = page.locator(f'.MuiRating-size{size.capitalize()}')
    expect(rating_size).to_have_count(1)
    assert not any('fullWidth' in warning for warning in warnings)


def test_rating_description(page):
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    serve_component(page, Rating(label='Rate', description='Some help'))
    expect(page.locator('.MuiRating-root')).to_have_count(1)
    assert not errors


def _count_value_patches(page):
    frames = []
    def on_ws(ws):
        ws.on('framesent', lambda p: frames.append(p) if isinstance(p, str) and '"attr":"value"' in p else None)
    page.on('websocket', on_ws)
    return frames


@pytest.mark.parametrize('widget_cls,kwargs', [
    (FloatSlider, dict(start=0, end=1, step=0.001, value=0)),
    (RangeSlider, dict(start=0, end=1, step=0.001, value=(0, 1))),
])
def test_slider_drag_throttles_value_updates(page, widget_cls, kwargs):
    widget = widget_cls(width=600, **kwargs)
    frames = _count_value_patches(page)
    serve_component(page, widget)
    box = page.locator('.MuiSlider-thumb').first.bounding_box()
    x, y = box['x'] + box['width'] / 2, box['y'] + box['height'] / 2
    page.mouse.move(x, y)
    page.mouse.down()
    start = time.perf_counter()
    for i in range(1, 101):
        page.mouse.move(x + i * 4, y)
    elapsed = time.perf_counter() - start
    page.mouse.up()

    wait_until(lambda: widget.value_throttled == widget.value, page)
    assert widget.value != kwargs['value']
    # At most one update per 50 ms window plus leading/trailing/commit updates
    assert len(frames) <= elapsed / 0.05 + 3


def test_range_slider_drag_does_not_echo_value_start_end(page):
    widget = RangeSlider(width=600, start=0, end=1, step=0.001, value=(0, 1))
    received = []
    page.on('websocket', lambda ws: ws.on(
        'framereceived', lambda p: received.append(p) if isinstance(p, str) and 'value_start' in p else None
    ))
    serve_component(page, widget)
    box = page.locator('.MuiSlider-thumb').first.bounding_box()
    x, y = box['x'] + box['width'] / 2, box['y'] + box['height'] / 2
    page.mouse.move(x, y)
    page.mouse.down()
    for i in range(1, 21):
        page.mouse.move(x + i * 10, y)
    page.mouse.up()
    wait_until(lambda: widget.value_start > 0, page)
    assert widget.value_start == widget.value[0]
    assert not received


def test_editable_int_slider_keyboard_respects_fixed_start(page):
    widget = EditableIntSlider(value=1, start=0, end=10, fixed_start=0, fixed_end=10)
    serve_component(page, widget)
    page.locator('.MuiInputBase-input').first.click()
    for _ in range(3):
        page.keyboard.press('ArrowDown')
    wait_until(lambda: widget.value == 0, page)
    for _ in range(15):
        page.keyboard.press('ArrowUp')
    wait_until(lambda: widget.value == 10, page)
    assert widget.start == 0
    assert widget.end == 10


def test_editable_float_slider_keyboard_extends_end(page):
    widget = EditableFloatSlider(value=0.5, start=0, end=1, step=0.5)
    serve_component(page, widget)
    page.locator('.MuiInputBase-input').first.click()
    for _ in range(4):
        page.keyboard.press('ArrowUp')
    wait_until(lambda: widget.value == 2.5, page)
    wait_until(lambda: widget.end == 2.5, page)


def test_editable_int_range_slider_keyboard_respects_fixed_bounds(page):
    widget = EditableIntRangeSlider(value=(1, 9), start=0, end=10, fixed_start=0, fixed_end=10)
    serve_component(page, widget)
    page.locator('.MuiInputBase-input').first.click()
    for _ in range(3):
        page.keyboard.press('ArrowDown')
    wait_until(lambda: widget.value == (0, 9), page)
    page.locator('.MuiInputBase-input').nth(1).click()
    for _ in range(5):
        page.keyboard.press('ArrowUp')
    wait_until(lambda: widget.value == (0, 10), page)


@pytest.mark.parametrize('text', ['', 'abc'])
def test_editable_int_slider_invalid_input_reverts(page, text):
    widget = EditableIntSlider(value=5, start=0, end=10)
    serve_component(page, widget)
    inp = page.locator('.MuiInputBase-input').first
    inp.click()
    inp.fill('7')
    page.keyboard.press('Enter')
    wait_until(lambda: widget.value == 7, page)
    # Input keeps DOM focus after Enter, edit again without re-focusing
    inp.fill(text)
    page.keyboard.press('Enter')
    expect(inp).to_have_value('7')
    assert widget.value == 7


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


@pytest.mark.parametrize('text,expected', [('1e-3', 0.001), ('2.5E-1', 0.25)])
def test_editable_float_slider_accepts_exponent_input(page, text, expected):
    widget = EditableFloatSlider(value=0.5, start=0, end=1, step=0.001)
    serve_component(page, widget)
    inp = page.locator('.MuiInputBase-input').first
    inp.click()
    inp.fill(text)
    page.keyboard.press('Enter')
    wait_until(lambda: widget.value == expected, page)


def test_slider_sends_trailing_drag_value_on_unmount(page):
    slider = FloatSlider(start=0, end=100, value=0, step=1)
    col = Column(slider, width=400)
    # A second view keeps the model in the document once col drops its view
    layout = Row(col, Column(slider, width=400))
    serve_component(page, layout)

    roots = page.locator('.MuiSlider-root')
    expect(roots).to_have_count(2)
    # Let the Row settle its layout before measuring the drag target
    page.wait_for_timeout(300)
    box = roots.first.bounding_box()
    y = box['y'] + box['height'] / 2
    page.mouse.move(box['x'] + box['width'] * 0.3, y)
    page.mouse.down()
    page.mouse.move(box['x'] + box['width'] * 0.4, y, steps=3)
    wait_until(lambda: slider.value >= 30, page)

    # The last move lands inside the 50 ms throttle window and the view is
    # unmounted before the trailing update fires.
    col_id = col._models[list(col._models)[0]][0].ref['id']
    page.mouse.move(box['x'] + box['width'] * 0.6, y)
    page.mouse.move(box['x'] + box['width'] * 0.8, y)
    page.evaluate("(id) => { Bokeh.documents[0].get_model_by_id(id).data.objects = [] }", col_id)
    page.mouse.up()
    wait_until(lambda: slider.value >= 75, page)
