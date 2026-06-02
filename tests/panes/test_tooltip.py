import pytest

from panel_material_ui.pane import Tooltip


class TestTooltipDefaults:

    def test_default_params(self):
        tooltip = Tooltip()
        assert tooltip.arrow is False
        assert tooltip.describe_child is False
        assert tooltip.enter_delay == 100
        assert tooltip.follow_cursor is False
        assert tooltip.leave_delay == 0
        assert tooltip.object is None
        assert tooltip.open is None
        assert tooltip.placement == "bottom"
        assert tooltip.title == ""


class TestTooltipParams:

    @pytest.mark.parametrize(
        "placement",
        [
            "bottom-end", "bottom-start", "bottom",
            "left-end", "left-start", "left",
            "right-end", "right-start", "right",
            "top-end", "top-start", "top",
        ],
    )
    def test_placement(self, placement):
        tooltip = Tooltip(placement=placement)
        assert tooltip.placement == placement

    def test_title(self):
        tooltip = Tooltip(title="Help text")
        assert tooltip.title == "Help text"

    def test_arrow(self):
        tooltip = Tooltip(arrow=True)
        assert tooltip.arrow is True

    def test_follow_cursor(self):
        tooltip = Tooltip(follow_cursor=True)
        assert tooltip.follow_cursor is True

    def test_describe_child(self):
        tooltip = Tooltip(describe_child=True)
        assert tooltip.describe_child is True

    def test_enter_delay(self):
        tooltip = Tooltip(enter_delay=500)
        assert tooltip.enter_delay == 500

    def test_enter_delay_negative_raises(self):
        with pytest.raises(ValueError):
            Tooltip(enter_delay=-1)

    def test_leave_delay(self):
        tooltip = Tooltip(leave_delay=200)
        assert tooltip.leave_delay == 200

    def test_leave_delay_negative_raises(self):
        with pytest.raises(ValueError):
            Tooltip(leave_delay=-1)

    def test_open_controlled(self):
        tooltip = Tooltip(open=True)
        assert tooltip.open is True

    def test_object_positional(self):
        tooltip = Tooltip("Child", title="Tip")
        assert tooltip.object is not None

    def test_object_keyword(self):
        tooltip = Tooltip(object="Child", title="Tip")
        assert tooltip.object is not None
