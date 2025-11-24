from panel_material_ui import Tree


def test_initial_expanded_from_open_flag():
    """
    Items with `open=True` should initialize as expanded.
    Items without `open` (or open=False) should not.
    """
    t = Tree(items=[
        {"label": "A", "open": True, "items": [
            {"label": "A1"},
            {"label": "A2"},
        ]},
        {"label": "B"},  # closed by default
    ])

    # A is root index 0 → expanded path (0,)
    assert t.expanded == [(0,)]


def test_expanded_simple_remap_after_items_change():
    """
    Expanded path should be remapped correctly when items reorder or shrink.
    """
    t = Tree(items=[
        {"label": "A", "open": True, "items": [
            {"label": "A1"},
            {"label": "A2"},
        ]},
        {"label": "B"},
    ])

    # Initially expanded: A → (0,)
    assert t.expanded == [(0,)]

    # Now replace items:
    # - A still exists but is now at index 1
    # - B moves to index 0
    t.items = [
        {"label": "B"},  # now index 0
        {"label": "A", "items": [
            {"label": "A1"},
            {"label": "A2"},
        ]},
    ]

    # A is now at (1,)
    assert t.expanded == [(1,)]


def test_expanded_remap_nested():
    """
    Expanded deep nested items should be remapped into the new structure,
    as long as items overlap by label structure.
    """
    t = Tree(items=[
        {"label": "root", "open": True, "items": [
            {"label": "section", "open": True, "items": [
                {"label": "leaf1"},
                {"label": "leaf2"},
            ]},
        ]},
    ])

    # expanded = [(0,), (0, 0)]
    assert t.expanded == [(0,), (0, 0)]

    # Now restructure: "section" is moved under a new folder "wrapper"
    t.items = [
        {"label": "root", "items": [
            {"label": "wrapper", "open": True, "items": [
                {"label": "section", "items": [
                    {"label": "leaf1"},
                    {"label": "leaf2"},
                ]},
            ]},
        ]},
    ]

    # New expected expanded:
    # root     → (0,)
    # wrapper  → (0, 0)
    # section  → (0, 0, 0)
    assert t.expanded == [(0,), (0, 0, 0), (0, 0)]
