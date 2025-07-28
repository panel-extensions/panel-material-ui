from panel_material_ui import Rating

def test_rating_initial_end():
    """Should not raise an exception when end is not set."""
    Rating(label='Max 10', end=10, value=7)
