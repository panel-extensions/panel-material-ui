from panel_material_ui.base import MaterialUIComponent


class _TestComponentESMBase(MaterialUIComponent):
    _esm_base = (
        "export function render() { return null }"
    )



class _TestComponentESM(MaterialUIComponent):
    _esm = (
        "export function render() { return null }"
    )


def test_render_esm_base_patches_utils_import():
    esm_base = _TestComponentESM._render_esm_base()
    assert (
        "const install_theme_hooks = pnmui.install_theme_hooks; "
        "const apply_global_css = pnmui.apply_global_css;"
    ) in esm_base


def test_render_esm_patches_utils_import():
    esm_base = _TestComponentESMBase._render_esm_base()
    assert (
        "const install_theme_hooks = pnmui.install_theme_hooks; "
        "const apply_global_css = pnmui.apply_global_css;"
    ) in esm_base
