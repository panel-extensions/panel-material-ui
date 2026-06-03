import pytest

from panel_material_ui.wrappers import Animation


class TestAnimationDefaults:

    def test_default_params(self):
        anim = Animation()
        assert anim.active is True
        assert anim.duration is None
        assert anim.object is None
        assert anim.orientation == "vertical"
        assert anim.placement == "left"
        assert anim.variant == "fade"


class TestAnimationParams:

    @pytest.mark.parametrize(
        "variant",
        ["collapse", "fade", "grow", "slide", "zoom"],
    )
    def test_variant(self, variant):
        anim = Animation(variant=variant)
        assert anim.variant == variant

    def test_active_toggle(self):
        anim = Animation(active=False)
        assert anim.active is False
        anim.active = True
        assert anim.active is True

    def test_duration(self):
        anim = Animation(duration=500)
        assert anim.duration == 500

    def test_duration_negative_raises(self):
        with pytest.raises(ValueError):
            Animation(duration=-1)

    @pytest.mark.parametrize("placement", ["down", "left", "right", "up"])
    def test_placement(self, placement):
        anim = Animation(variant="slide", placement=placement)
        assert anim.placement == placement

    @pytest.mark.parametrize("orientation", ["vertical", "horizontal"])
    def test_orientation(self, orientation):
        anim = Animation(variant="collapse", orientation=orientation)
        assert anim.orientation == orientation

    def test_object_positional(self):
        anim = Animation("Child", variant="fade")
        assert anim.object is not None

    def test_object_keyword(self):
        anim = Animation(object="Child", variant="grow")
        assert anim.object is not None
