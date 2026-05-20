import pytest

from panel_material_ui.layout import Badge


class TestBadgeDefaults:

    def test_default_params(self):
        badge = Badge()
        assert badge.anchor_origin is None
        assert badge.badge_content == 0
        assert badge.color == "primary"
        assert badge.invisible is False
        assert badge.max == 99
        assert badge.object is None
        assert badge.overlap == "rectangular"
        assert badge.show_zero is False
        assert badge.variant == "standard"


class TestBadgeParams:

    @pytest.mark.parametrize(
        "color",
        ["primary", "secondary", "error", "success", "warning", "info"],
    )
    def test_color(self, color):
        badge = Badge(color=color)
        assert badge.color == color

    @pytest.mark.parametrize("variant", ["standard", "dot"])
    def test_variant(self, variant):
        badge = Badge(variant=variant)
        assert badge.variant == variant

    @pytest.mark.parametrize("overlap", ["rectangular", "circular"])
    def test_overlap(self, overlap):
        badge = Badge(overlap=overlap)
        assert badge.overlap == overlap

    def test_badge_content_int(self):
        badge = Badge(badge_content=42)
        assert badge.badge_content == 42

    def test_badge_content_string(self):
        badge = Badge(badge_content="new")
        assert badge.badge_content == "new"

    def test_max(self):
        badge = Badge(max=999)
        assert badge.max == 999

    def test_invisible(self):
        badge = Badge(invisible=True)
        assert badge.invisible is True

    def test_show_zero(self):
        badge = Badge(show_zero=True)
        assert badge.show_zero is True

    def test_anchor_origin(self):
        origin = {"vertical": "bottom", "horizontal": "left"}
        badge = Badge(anchor_origin=origin)
        assert badge.anchor_origin == origin

    def test_object_positional(self):
        badge = Badge("Child", badge_content=1)
        assert badge.object is not None

    def test_object_keyword(self):
        badge = Badge(object="Child", badge_content=1)
        assert badge.object is not None
