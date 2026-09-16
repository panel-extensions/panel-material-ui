import pytest
from panel.config import config
from panel.theme.base import Design

from panel_material_ui.base import MaterialUIComponent
from panel_material_ui.theme import MaterialDesign


class _TestComponentESMBase(MaterialUIComponent):
    _esm_base = (
        "export function render() { return null }"
    )



class _TestComponentESM(MaterialUIComponent):
    _esm = (
        "export function render() { return null }"
    )


class _OtherMaterialDesign(MaterialDesign):
    """A Material-family design distinct from the base MaterialDesign, e.g.
    panel.ui's own MaterialUIDesign subclass."""


class _UnrelatedDesign(Design):
    """A design unrelated to the Material family, e.g. a classic design
    like panel.theme.Native or panel.theme.Default."""


@pytest.fixture
def reset_config_design():
    original = config.design
    try:
        yield
    finally:
        config.design = original


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


def test_design_defaults_to_material_design_when_config_design_unset(reset_config_design):
    config.design = None
    component = _TestComponentESM()
    assert component.design is MaterialDesign


def test_design_respects_config_design_material_subclass(reset_config_design):
    # e.g. panel.ui setting config.design = panel.ui.theme.MaterialUIDesign
    # should be honored instead of the hardcoded base MaterialDesign.
    config.design = _OtherMaterialDesign
    component = _TestComponentESM()
    assert component.design is _OtherMaterialDesign


def test_design_ignores_unrelated_config_design(reset_config_design):
    # An unrelated classic design (e.g. panel.theme.Native) must never be
    # forced onto a panel-material-ui component; it should fall back to the
    # hardcoded base MaterialDesign exactly as before this behavior existed.
    config.design = _UnrelatedDesign
    component = _TestComponentESM()
    assert component.design is MaterialDesign


def test_design_explicit_kwarg_always_wins(reset_config_design):
    config.design = _OtherMaterialDesign
    component = _TestComponentESM(design=MaterialDesign)
    assert component.design is MaterialDesign
