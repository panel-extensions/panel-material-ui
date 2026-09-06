import pytest

pytest.importorskip("playwright")

from panel.tests.util import serve_component, wait_until
from playwright.sync_api import expect

from panel_material_ui.widgets import DiscretePlayer, Player

pytestmark = pytest.mark.ui


def test_player(page):
    widget = Player(label='Frame', length=10)
    serve_component(page, widget)

    expect(page.locator('.player')).to_have_count(1)
    expect(page.locator('.MuiIconButton-root')).to_have_count(9)
    expect(page.locator('.MuiToggleButton-root')).to_have_count(3)


def test_player_play_and_pause(page):
    widget = Player(length=10, interval=100)
    serve_component(page, widget)

    page.locator('.play').click()
    wait_until(lambda: widget.direction == 1, page)
    wait_until(lambda: widget.value > 2, page)

    page.locator('.pause').click()
    wait_until(lambda: widget.direction == 0, page)
    paused_at = widget.value
    page.wait_for_timeout(500)
    assert widget.value == paused_at
    assert widget.value_throttled == paused_at


def test_player_loop_policy_once_stops_at_end(page):
    widget = Player(length=4, interval=100, loop_policy='once')
    serve_component(page, widget)

    page.locator('.play').click()
    wait_until(lambda: widget.value == 3, page)
    wait_until(lambda: widget.direction == 0, page)
    page.wait_for_timeout(500)
    assert widget.value == 3


def test_player_loop_policy_loop_wraps(page):
    widget = Player(length=3, interval=100, loop_policy='loop')
    serve_component(page, widget)

    values = []
    widget.param.watch(lambda e: values.append(e.new), 'value')

    page.locator('.play').click()
    wait_until(lambda: values[-3:] == [1, 2, 0], page)
    assert widget.direction == 1


def test_player_loop_policy_reflect_reverses(page):
    widget = Player(length=3, interval=100, loop_policy='reflect')
    serve_component(page, widget)

    page.locator('.play').click()
    wait_until(lambda: widget.direction == -1, page)
    wait_until(lambda: widget.direction == 1, page)
    assert widget.value == 0


def test_player_reverse(page):
    widget = Player(length=10, value=9, interval=100)
    serve_component(page, widget)

    page.locator('.reverse').click()
    wait_until(lambda: widget.direction == -1, page)
    wait_until(lambda: widget.value < 7, page)


def test_player_frame_buttons(page):
    widget = Player(length=10, step=2)
    serve_component(page, widget)

    page.locator('.next').click()
    wait_until(lambda: widget.value == 2, page)
    page.locator('.previous').click()
    wait_until(lambda: widget.value == 0, page)
    page.locator('.last').click()
    wait_until(lambda: widget.value == 9, page)
    page.locator('.first').click()
    wait_until(lambda: widget.value == 0, page)


def test_player_step_clamps_at_bounds(page):
    widget = Player(length=10, step=4, value=8)
    serve_component(page, widget)

    page.locator('.next').click()
    wait_until(lambda: widget.value == 9, page)
    page.locator('.previous').click()
    wait_until(lambda: widget.value == 5, page)
    page.locator('.previous').click()
    wait_until(lambda: widget.value == 1, page)
    page.locator('.previous').click()
    wait_until(lambda: widget.value == 0, page)


def test_player_direction_from_python(page):
    widget = Player(length=10, interval=100)
    serve_component(page, widget)

    widget.play()
    wait_until(lambda: widget.value > 2, page)
    widget.pause()
    page.wait_for_timeout(400)
    paused_at = widget.value
    page.wait_for_timeout(400)
    assert widget.value == paused_at


def test_player_value_from_python_while_playing(page):
    widget = Player(length=50, interval=100)
    serve_component(page, widget)

    widget.play()
    wait_until(lambda: widget.value > 1, page)
    widget.value = 25
    wait_until(lambda: widget.value > 25, page)
    assert widget.direction == 1


def test_player_faster_lowers_interval(page):
    widget = Player(length=10)
    serve_component(page, widget)

    page.locator('.faster').click()
    wait_until(lambda: widget.interval == 350, page)
    page.locator('.slower').click()
    wait_until(lambda: widget.interval == 500, page)


def test_player_visible_buttons(page):
    widget = Player(length=10, visible_buttons=['play', 'pause'])
    serve_component(page, widget)

    expect(page.locator('.MuiIconButton-root')).to_have_count(2)


def test_player_show_loop_controls(page):
    widget = Player(length=10, show_loop_controls=False)
    serve_component(page, widget)

    expect(page.locator('.MuiIconButton-root')).to_have_count(9)
    expect(page.locator('.MuiToggleButtonGroup-root')).to_have_count(0)


def test_player_visible_loop_options(page):
    widget = Player(length=10, visible_loop_options=['loop', 'reflect'])
    serve_component(page, widget)

    expect(page.locator('.MuiToggleButton-root')).to_have_count(2)
    assert widget.loop_policy == 'loop'


def test_player_loop_policy_from_ui(page):
    widget = Player(length=10)
    serve_component(page, widget)

    page.locator('.MuiToggleButton-root.reflect').click()
    wait_until(lambda: widget.loop_policy == 'reflect', page)


def test_player_show_value(page):
    widget = Player(label='Frame', length=10, value=3, show_value=True)
    serve_component(page, widget)

    expect(page.locator('.MuiFormLabel-root')).to_have_text('Frame: 3')


def test_player_minimal(page):
    widget = Player(length=10, variant='minimal', show_value=True)
    serve_component(page, widget)

    # A single play/pause toggle and no loop controls.
    expect(page.locator('.MuiIconButton-root')).to_have_count(1)
    expect(page.locator('.MuiToggleButtonGroup-root')).to_have_count(0)
    expect(page.locator('.player')).to_contain_text('0 / 9')

    page.locator('.play').click()
    wait_until(lambda: widget.value > 1, page)
    page.locator('.pause').click()
    wait_until(lambda: widget.direction == 0, page)


def test_discrete_player_shows_label(page):
    widget = DiscretePlayer(label='Discrete', options={'a': 1, 'b': 2, 'c': 3}, value=3)
    serve_component(page, widget)

    expect(page.locator('.MuiFormLabel-root')).to_have_text('Discrete: c')


def test_discrete_player_advances_values(page):
    widget = DiscretePlayer(options=[2, 4, 8, 16], interval=100)
    serve_component(page, widget)

    page.locator('.play').click()
    wait_until(lambda: widget.value == 16, page)
    assert widget.value_throttled == 16


def test_discrete_player_minimal_shows_label(page):
    widget = DiscretePlayer(options={'a': 1, 'b': 2}, value=2, variant='minimal')
    serve_component(page, widget)

    expect(page.locator('.discrete-player')).to_contain_text('b')
