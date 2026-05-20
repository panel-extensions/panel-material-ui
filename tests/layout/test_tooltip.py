import pytest

from panel_material_ui.layout import Tooltip


class TestTooltipDefaults:

    def test_default_params(self):
        tooltip = Tooltip()
        assert tooltip.arrow is False
        assert tooltip.describe_child is False
        assert tooltip.enter_delay == 100
        assert tooltip.follow_cursor is False
        assert tooltip.leave_delay == 0
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

    def test_open_none_default(self):
        tooltip = Tooltip()
        assert tooltip.open is None


class TestTooltipListAPI:

    def test_append(self):
        tooltip = Tooltip("Child 1", title="Tip")
        tooltip.append("Child 2")
        assert len(tooltip.objects) == 2

    def test_pop(self):
        tooltip = Tooltip("Child 1", "Child 2", title="Tip")
        tooltip.pop(0)
        assert len(tooltip.objects) == 1

    def test_clear(self):
        tooltip = Tooltip("Child 1", "Child 2", title="Tip")
        tooltip.clear()
        assert len(tooltip.objects) == 0

    def test_empty(self):
        tooltip = Tooltip()
        assert len(tooltip.objects) == 0
