import pytest

from panel_material_ui.wrappers import Skeleton


class TestSkeletonDefaults:

    def test_default_params(self):
        s = Skeleton()
        assert s.active is False
        assert s.animation == "pulse"
        assert s.object is None
        assert s.variant == "rounded"


class TestSkeletonParams:

    @pytest.mark.parametrize(
        "variant",
        ["text", "circular", "rectangular", "rounded"],
    )
    def test_variant(self, variant):
        s = Skeleton(variant=variant)
        assert s.variant == variant

    @pytest.mark.parametrize("animation", ["pulse", "wave", None])
    def test_animation(self, animation):
        s = Skeleton(animation=animation)
        assert s.animation == animation

    def test_active_toggle(self):
        s = Skeleton(active=False)
        assert s.active is False
        s.active = True
        assert s.active is True

    def test_object_positional(self):
        s = Skeleton("Child")
        assert s.object is not None

    def test_object_keyword(self):
        s = Skeleton(object="Child")
        assert s.object is not None
