import pytest
from panel.pane import HoloViews

from panel_material_ui.widgets import DiscretePlayer, Player


def test_player_length():
    player = Player(length=10)
    assert player.start == 0
    assert player.end == 9


def test_player_length_and_bounds_raises():
    with pytest.raises(ValueError):
        Player(length=10, start=2)
    with pytest.raises(ValueError):
        Player(length=10, end=2)


def test_player_start_sets_value():
    assert Player(start=5).value == 5


def test_player_value_mirrored_to_value_throttled():
    assert Player(length=10, value=3).value_throttled == 3


def test_player_loop_policy_coerced_to_visible_options():
    player = Player(loop_policy='reflect', visible_loop_options=['once', 'loop'])
    assert player.loop_policy == 'once'


def test_player_direction_methods():
    player = Player(length=10)
    player.play()
    assert player.direction == 1
    player.pause()
    assert player.direction == 0
    player.reverse()
    assert player.direction == -1


def test_player_no_classic_stylesheet():
    assert Player()._stylesheets == []


def test_player_does_not_support_embed():
    # The classic implementation emits 'cb_obj.value' against the widget
    # model, which does not resolve on a ReactComponent.
    assert Player._supports_embed is False


def test_discrete_player_sends_index():
    player = DiscretePlayer(options={'a': 1, 'b': 2}, value=2)
    props = player._process_param_change({'options': player.options, 'value': player.value})
    assert props['options'] == ['a', 'b']
    assert props['value'] == 1


def test_discrete_player_receives_value():
    player = DiscretePlayer(options={'a': 1, 'b': 2}, value=2)
    props = player._process_property_change({'value': 1, 'value_throttled': 0})
    assert props == {'value': 2, 'value_throttled': 1}


def test_discrete_player_does_not_send_bounds():
    player = DiscretePlayer(options=[2, 4, 8])
    props = player._process_param_change({'options': player.options})
    assert 'start' not in props
    assert 'end' not in props


def test_discrete_player_sends_index_alongside_options():
    player = DiscretePlayer(options=[2, 4, 8], value=8)
    assert player._process_param_change({'options': player.options})['value'] == 2


def test_discrete_player_option_change_keeps_value_valid(document, comm):
    player = DiscretePlayer(options=[2, 4, 8], value=8)
    model = player.get_root(document, comm=comm)
    assert model.data.value == 2

    player.options = [1, 2]
    assert player.value == 1
    assert model.data.options == ['1', '2']
    assert model.data.value == 0


def test_holoviews_scrubber_is_material_player():
    assert HoloViews.default_widgets['scrubber'] is Player
