import pytest

from panel.layout import Column

from panel_material_ui.layout import Stepper


class TestStepperConstruction:

    def test_tuple_construction(self):
        stepper = Stepper(
            ("Step 1", "Content 1"),
            ("Step 2", "Content 2"),
        )
        assert len(stepper.objects) == 2
        assert stepper._names == ["Step 1", "Step 2"]

    def test_named_object_construction(self):
        c1 = Column(name="First")
        c2 = Column(name="Second")
        stepper = Stepper(c1, c2)
        assert len(stepper.objects) == 2
        assert stepper._names == ["First", "Second"]

    def test_empty(self):
        stepper = Stepper()
        assert len(stepper.objects) == 0
        assert stepper._names == []

    def test_single_step(self):
        stepper = Stepper(("Only Step", "Content"))
        assert len(stepper.objects) == 1
        assert stepper._names == ["Only Step"]


class TestStepperDefaults:

    def test_default_params(self):
        stepper = Stepper()
        assert stepper.active == 0
        assert stepper.alternative_label is False
        assert stepper.color == "primary"
        assert stepper.completed == []
        assert stepper.connector is True
        assert stepper.disabled == []
        assert stepper.dynamic is False
        assert stepper.error == []
        assert stepper.non_linear is False
        assert stepper.optional == []
        assert stepper.orientation == "horizontal"


class TestStepperParams:

    @pytest.mark.parametrize("orientation", ["horizontal", "vertical"])
    def test_orientation(self, orientation):
        stepper = Stepper(orientation=orientation)
        assert stepper.orientation == orientation

    @pytest.mark.parametrize(
        ("color",),
        [("primary",), ("secondary",), ("error",), ("success",)],
        ids=["primary", "secondary", "error", "success"],
    )
    def test_color(self, color):
        stepper = Stepper(color=color)
        assert stepper.color == color

    def test_active_bounds(self):
        stepper = Stepper(
            ("Step 1", "C1"),
            ("Step 2", "C2"),
            active=1,
        )
        assert stepper.active == 1

    def test_active_zero_lower_bound(self):
        with pytest.raises(ValueError):
            Stepper(active=-1)

    def test_list_params_accept_ints(self):
        stepper = Stepper(
            ("S1", "C1"), ("S2", "C2"), ("S3", "C3"),
            completed=[0],
            disabled=[1],
            error=[2],
            optional=[1, 2],
        )
        assert stepper.completed == [0]
        assert stepper.disabled == [1]
        assert stepper.error == [2]
        assert stepper.optional == [1, 2]


class TestStepperListAPI:

    def test_append(self):
        stepper = Stepper(("Step 1", "Content 1"))
        stepper.append(("Step 2", "Content 2"))
        assert len(stepper.objects) == 2
        assert stepper._names == ["Step 1", "Step 2"]

    def test_insert(self):
        stepper = Stepper(("Step 1", "C1"), ("Step 3", "C3"))
        stepper.insert(1, ("Step 2", "C2"))
        assert len(stepper.objects) == 3
        assert stepper._names == ["Step 1", "Step 2", "Step 3"]

    def test_pop(self):
        stepper = Stepper(("Step 1", "C1"), ("Step 2", "C2"))
        popped = stepper.pop(0)
        assert len(stepper.objects) == 1
        assert stepper._names == ["Step 2"]

    def test_setitem(self):
        stepper = Stepper(("Step 1", "C1"), ("Step 2", "C2"))
        stepper[0] = ("New Step 1", "New C1")
        assert stepper._names[0] == "New Step 1"

    def test_clear(self):
        stepper = Stepper(("Step 1", "C1"), ("Step 2", "C2"))
        stepper.clear()
        assert len(stepper.objects) == 0
        assert stepper._names == []


class TestStepperActiveTriggering:

    def test_active_triggers_objects(self):
        stepper = Stepper(("Step 1", "C1"), ("Step 2", "C2"))
        events = []
        stepper.param.watch(lambda e: events.append(e), "objects")
        stepper.active = 1
        assert len(events) == 1
