from importlib.resources import files

import panel_material_ui


def test_package_declares_inline_typing():
    assert files(panel_material_ui).joinpath("py.typed").is_file()
