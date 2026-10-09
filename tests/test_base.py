import pytest
from panel.config import config
from panel.theme.base import Design

from panel_material_ui.base import MaterialUIComponent
from panel_material_ui.theme import MaterialDesign
from panel_material_ui.widgets import Button


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


def test_render_esm_wraps_with_bundle_transforms():
    esm_base = _TestComponentESM._render_esm_base()
    assert esm_base.count('import pnmui from "panel-material-ui"') == 1
    assert 'const {withLoading} = pnmui;' in esm_base
    assert 'const {withTheme} = pnmui;' in esm_base
    assert 'from "./transforms"' not in esm_base
    assert 'const Themed_TestComponentESM = withTheme(Loading_TestComponentESM)' in esm_base
    assert esm_base.rstrip().endswith('export default { render: Themed_TestComponentESM }')


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


class _ExternalButton(Button):
    """A subclass defined outside panel_material_ui, which the bundle does not export."""


def test_external_subclass_renders_with_compiled_ancestor(document):
    button = _ExternalButton(label='External')
    assert button._get_properties(document)['class_name'] == 'Button'


def test_interactive_subclass_resolves_bundle(document):
    # Classes defined in IPython have no module file to resolve the bundle from.
    cls = type('InteractiveButton', (Button,), {'__module__': 'interactive_session'})
    props = cls(label='Interactive')._get_properties(document)
    assert props['bundle'] is not None
    assert props['class_name'] == 'Button'


def test_material_ui_component_keeps_its_class_name(document):
    props = _TestComponentESM()._get_properties(document)
    assert props['bundle'] is None
    assert props['class_name'] == '_TestComponentESM'
