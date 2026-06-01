import pytest

from panel_material_ui.widgets import StepperMenu


class TestStepperMenuDefaults:

    def test_default_params(self):
        menu = StepperMenu()
        assert menu.active == 0
        assert menu.items == []
        assert menu.variant == "standard"
        assert menu.indicator == "dots"
        assert menu.position == "static"
        assert menu.back_text == "Back"
        assert menu.next_text == "Next"
        assert menu.color == "primary"
        assert menu.alternative_label is False
        assert menu.connector is True
        assert menu.non_linear is False


class TestStepperMenuParams:

    @pytest.mark.parametrize("variant", ["standard", "compact"])
    def test_variant(self, variant):
        assert StepperMenu(variant=variant).variant == variant

    @pytest.mark.parametrize("indicator", ["dots", "progress", "text"])
    def test_indicator(self, indicator):
        assert StepperMenu(indicator=indicator).indicator == indicator

    @pytest.mark.parametrize("position", ["bottom", "static", "top"])
    def test_position(self, position):
        assert StepperMenu(position=position).position == position

    def test_button_text(self):
        menu = StepperMenu(back_text="Prev", next_text="Forward")
        assert menu.back_text == "Prev"
        assert menu.next_text == "Forward"

    def test_active_negative_raises(self):
        with pytest.raises(ValueError):
            StepperMenu(active=-1)


class TestStepperMenuItems:

    def test_string_items(self):
        menu = StepperMenu(items=["A", "B", "C"])
        assert len(menu.items) == 3

    def test_state_keys_preserved(self):
        menu = StepperMenu(items=[
            {"label": "A", "completed": True},
            {"label": "B", "error": True, "optional": True},
            {"label": "C", "disabled": True},
        ])
        assert menu.items[0]["completed"] is True
        assert menu.items[1]["error"] is True
        assert menu.items[1]["optional"] is True
        assert menu.items[2]["disabled"] is True

    def test_extra_keys_retained(self):
        # Only allowed keys are synced to the frontend, but arbitrary keys
        # may still be stored on the Python-side items.
        menu = StepperMenu(items=[{"label": "A", "view": "anything"}])
        assert menu.items[0]["view"] == "anything"

    def test_active_syncs_value(self):
        menu = StepperMenu(items=[{"label": "A"}, {"label": "B"}], active=1)
        assert menu.value == {"label": "B"}

    def test_value_syncs_active(self):
        menu = StepperMenu(items=[{"label": "A"}, {"label": "B"}, {"label": "C"}])
        menu.value = {"label": "C"}
        assert menu.active == 2

    def test_string_item_value(self):
        menu = StepperMenu(items=["A", "B", "C"], active=2)
        assert menu.value == "C"


class TestStepperMenuNavigation:

    def test_next(self):
        menu = StepperMenu(items=["A", "B", "C"])
        menu.next()
        assert menu.active == 1
        menu.next()
        assert menu.active == 2

    def test_next_clamps_to_last(self):
        menu = StepperMenu(items=["A", "B"], active=1)
        menu.next()
        assert menu.active == 1

    def test_back(self):
        menu = StepperMenu(items=["A", "B"], active=1)
        menu.back()
        assert menu.active == 0

    def test_back_clamps_to_zero(self):
        menu = StepperMenu(items=["A", "B"])
        menu.back()
        assert menu.active == 0

    def test_reset(self):
        menu = StepperMenu(items=["A", "B", "C"], active=2)
        menu.reset()
        assert menu.active == 0

    def test_next_on_empty(self):
        menu = StepperMenu()
        menu.next()
        assert menu.active == 0

    def test_on_step_change(self):
        menu = StepperMenu(items=["A", "B"])
        events = []
        menu.on_step_change(lambda e: events.append(e.new))
        menu.next()
        assert events == [1]

    def test_on_step_change_in_constructor(self):
        events = []
        menu = StepperMenu(
            items=["A", "B"],
            on_step_change=lambda e: events.append(e.new),
        )
        menu.active = 1
        assert events == [1]
