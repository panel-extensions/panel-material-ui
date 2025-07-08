"""Tests for Avatar pane component."""

from panel_material_ui import Avatar


class TestAvatar:
    """Test cases for Avatar component."""

    def test_avatar_creation(self):
        """Test basic avatar creation."""
        avatar = Avatar(object="")
        assert avatar.object == ""
        assert avatar.size == "medium"
        assert avatar.variant == "rounded"
