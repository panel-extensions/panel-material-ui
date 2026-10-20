from panel_material_ui.layout import FlexBox


def test_flexbox_row_default_sizing_mode():
    assert FlexBox().sizing_mode == 'stretch_width'


def test_flexbox_column_default_sizing_mode():
    assert FlexBox(flex_direction='column').sizing_mode == 'stretch_height'


def test_flexbox_explicit_sizing_mode():
    assert FlexBox(sizing_mode='fixed', width=300).sizing_mode == 'fixed'
