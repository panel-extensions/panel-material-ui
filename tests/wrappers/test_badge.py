import pytest

from panel_material_ui.wrappers import Badge
from panel_material_ui.widgets import IconButton


class TestBadgeDefaults:

    def test_default_params(self):
        badge = Badge()
        assert badge.content == 0
        assert badge.color == "primary"
        assert badge.max == 99
        assert badge.object is None
        assert badge.offset is None
        assert badge.overlap == "rectangular"
        assert badge.placement == "top-right"
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

    def test_content_int(self):
        badge = Badge(content=42)
        assert badge.content == 42

    def test_content_string(self):
        badge = Badge(content="new")
        assert badge.content == "new"

    def test_max(self):
        badge = Badge(max=999)
        assert badge.max == 999

    def test_show_zero(self):
        badge = Badge(show_zero=True)
        assert badge.show_zero is True

    @pytest.mark.parametrize(
        "placement",
        ["top-right", "top-left", "bottom-right", "bottom-left"],
    )
    def test_placement(self, placement):
        badge = Badge(placement=placement)
        assert badge.placement == placement

    def test_object_positional(self):
        badge = Badge("Child", content=1)
        assert badge.object is not None

    def test_object_keyword(self):
        badge = Badge(object="Child", content=1)
        assert badge.object is not None


class TestBadgeOffset:

    def test_default(self):
        assert Badge().offset is None

    @pytest.mark.parametrize(
        "offset",
        [(0, 0), (2, -4), (-6, 8), (1.5, -2.5)],
        ids=["origin", "positive_x", "negative_x", "float"],
    )
    def test_set(self, offset):
        badge = Badge(offset=offset)
        assert badge.offset == offset

    @pytest.mark.parametrize("offset", [(1,), (1, 2, 3)], ids=["too_short", "too_long"])
    def test_wrong_length_raises(self, offset):
        with pytest.raises(ValueError):
            Badge(offset=offset)

    def test_non_numeric_raises(self):
        with pytest.raises((ValueError, TypeError)):
            Badge(offset=("a", "b"))


class TestBadgeMarginInheritance:

    # Margin can be a scalar, a (vertical, horizontal) pair, or a
    # (top, right, bottom, left) quad; inheritance must preserve the shape.
    @pytest.mark.parametrize(
        "margin",
        [0, 25, (5, 10), (1, 2, 3, 4)],
        ids=["zero", "scalar", "pair", "quad"],
    )
    def test_inherits_child_margin(self, margin):
        child = IconButton(icon="mail", margin=margin)
        badge = Badge(child, content=4)
        assert badge.margin == margin

    def test_inherits_child_default_margin(self):
        # With no explicit margin anywhere the Badge mirrors whatever the
        # child's (default) margin is, so wrapping is transparent to layout.
        child = IconButton(icon="mail")
        badge = Badge(child, content=4)
        assert badge.margin == child.margin

    @pytest.mark.parametrize("margin", [10, 0, (5, 10)], ids=["scalar", "zero", "pair"])
    def test_explicit_badge_margin_wins(self, margin):
        # An explicit Badge margin (including 0) must not be overwritten by
        # the child's margin.
        child = IconButton(icon="mail", margin=25)
        badge = Badge(child, content=4, margin=margin)
        assert badge.margin == margin

    @pytest.mark.parametrize(
        "new_margin",
        [40, (3, 6), (1, 2, 3, 4)],
        ids=["scalar", "pair", "quad"],
    )
    def test_inherit_updates_when_child_margin_changes(self, new_margin):
        child = IconButton(icon="mail", margin=25)
        badge = Badge(child, content=4)
        child.margin = new_margin
        assert badge.margin == new_margin

    def test_explicit_badge_margin_ignores_child_changes(self):
        child = IconButton(icon="mail", margin=25)
        badge = Badge(child, content=4, margin=10)
        child.margin = 40
        assert badge.margin == 10

    def test_inherit_follows_object_swap(self):
        badge = Badge(IconButton(icon="mail", margin=25), content=4)
        assert badge.margin == 25
        badge.object = IconButton(icon="mail", margin=7)
        assert badge.margin == 7

    def test_old_child_detached_after_swap(self):
        first = IconButton(icon="mail", margin=25)
        badge = Badge(first, content=4)
        badge.object = IconButton(icon="mail", margin=7)
        # Mutating the replaced child must no longer affect the Badge.
        first.margin = 99
        assert badge.margin == 7

    def test_non_viewable_child_does_not_error(self):
        # A plain string child has no margin param; inheritance is skipped
        # rather than raising.
        badge = Badge("Child", content=4)
        assert badge.object is not None
