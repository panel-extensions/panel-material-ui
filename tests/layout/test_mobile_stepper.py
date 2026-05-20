import pytest

from panel_material_ui.layout import MobileStepper


class TestMobileStepperDefaults:

    def test_default_params(self):
        stepper = MobileStepper()
        assert stepper.active == 0
        assert stepper.back_text == "Back"
        assert stepper.color == "primary"
        assert stepper.next_text == "Next"
        assert stepper.position == "static"
        assert stepper.variant == "dots"


class TestMobileStepperParams:

    @pytest.mark.parametrize(
        "variant",
        ["dots", "progress", "text"],
        ids=["dots", "progress", "text"],
    )
    def test_variant(self, variant):
        stepper = MobileStepper(variant=variant)
        assert stepper.variant == variant

    @pytest.mark.parametrize(
        "position",
        ["bottom", "static", "top"],
        ids=["bottom", "static", "top"],
    )
    def test_position(self, position):
        stepper = MobileStepper(position=position)
        assert stepper.position == position

    def test_active_bounds(self):
        stepper = MobileStepper("C1", "C2", "C3", active=2)
        assert stepper.active == 2

    def test_active_negative_raises(self):
        with pytest.raises(ValueError):
            MobileStepper(active=-1)

    def test_button_text(self):
        stepper = MobileStepper(back_text="Prev", next_text="Forward")
        assert stepper.back_text == "Prev"
        assert stepper.next_text == "Forward"


class TestMobileStepperListAPI:

    def test_append(self):
        stepper = MobileStepper("C1")
        stepper.append("C2")
        assert len(stepper.objects) == 2

    def test_pop(self):
        stepper = MobileStepper("C1", "C2")
        stepper.pop(0)
        assert len(stepper.objects) == 1

    def test_clear(self):
        stepper = MobileStepper("C1", "C2")
        stepper.clear()
        assert len(stepper.objects) == 0

    def test_empty(self):
        stepper = MobileStepper()
        assert len(stepper.objects) == 0


class TestMobileStepperNavigation:

    def test_next(self):
        stepper = MobileStepper("C1", "C2", "C3")
        stepper.next()
        assert stepper.active == 1
        stepper.next()
        assert stepper.active == 2

    def test_next_clamps_to_last(self):
        stepper = MobileStepper("C1", "C2", active=1)
        stepper.next()
        assert stepper.active == 1

    def test_back(self):
        stepper = MobileStepper("C1", "C2", active=1)
        stepper.back()
        assert stepper.active == 0

    def test_back_clamps_to_zero(self):
        stepper = MobileStepper("C1", "C2")
        stepper.back()
        assert stepper.active == 0

    def test_reset(self):
        stepper = MobileStepper("C1", "C2", active=1)
        stepper.reset()
        assert stepper.active == 0

    def test_next_on_empty(self):
        stepper = MobileStepper()
        stepper.next()
        assert stepper.active == 0

    def test_on_step_change(self):
        stepper = MobileStepper("C1", "C2")
        events = []
        stepper.on_step_change(lambda e: events.append(e.new))
        stepper.next()
        assert events == [1]

    def test_on_step_change_in_constructor(self):
        events = []
        stepper = MobileStepper(
            "C1", "C2",
            on_step_change=lambda e: events.append(e.new),
        )
        stepper.active = 1
        assert events == [1]
