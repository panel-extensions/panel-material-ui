from panel_material_ui.layout import Row


def test_row_scroll_true_is_horizontal():
    row = Row(scroll=True)

    assert 'scrollable-horizontal' in row._process_param_change({'scroll': True})['css_classes']
