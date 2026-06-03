"""Tests for Avatar component."""

from panel_material_ui import Avatar


class TestAvatar:

    def test_avatar_creation(self):
        avatar = Avatar(content="")
        assert avatar.content == ""
        assert avatar.size == "medium"
        assert avatar.variant == "rounded"

    def test_avatar_positional_content(self):
        avatar = Avatar("JD")
        assert avatar.content == "JD"

    def test_avatar_color(self):
        avatar = Avatar(content="AB", color="#ff0000")
        assert avatar.color == "#ff0000"
