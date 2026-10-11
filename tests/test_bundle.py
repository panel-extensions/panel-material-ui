import pathlib
import re

import pytest
from panel.io.compile import find_module_bundles

from panel_material_ui.base import BASE_PATH, LoadingTransform, ThemedTransform, TooltipTransform

INDEX = (BASE_PATH / "index.js").read_text()

WRAPPERS = {
    ThemedTransform: "withTheme",
    LoadingTransform: "withLoading",
    TooltipTransform: "withTooltip",
}

IMPORTS = dict(
    re.findall(r'^import \{render as (\w+)\} from "\./([\w/]+)"$', INDEX, re.M) +
    re.findall(r'^const (\w+) = lazy\(\(\) => import\("\./([\w/]+)"\)\)$', INDEX, re.M)
)

ENTRIES = {
    name: (render, [w.strip() for w in wrappers.split(",")])
    for name, render, wrappers in re.findall(r'^  (\w+): component\((\w+), ([\w, ]+)\),$', INDEX, re.M)
}

COMPONENTS = [
    component for components in find_module_bundles("panel_material_ui").values()
    for component in components
]


@pytest.mark.parametrize("component", COMPONENTS, ids=lambda c: c.__name__)
def test_component_registered_in_bundle_entry(component):
    assert component.__name__ in ENTRIES, f"{component.__name__} is not registered in index.js"
    render, wrappers = ENTRIES[component.__name__]
    esm_path = component._esm_path(compiled="compiling")
    assert IMPORTS.get(render) == esm_path.relative_to(BASE_PATH).with_suffix("").as_posix()
    assert wrappers == [WRAPPERS[transform] for transform in component._esm_transforms]


def test_bundle_entry_has_no_stale_components():
    assert set(ENTRIES) == {component.__name__ for component in COMPONENTS}


def test_bundle_entry_imports_exist():
    for path in IMPORTS.values():
        assert pathlib.Path(BASE_PATH / f"{path}.jsx").is_file()


def test_inlined_bundle_does_not_load_chunks():
    from panel.config import config

    from panel_material_ui.base import INLINE_BUNDLE_PATH
    from panel_material_ui.widgets import DatePicker

    if not INLINE_BUNDLE_PATH.is_file():
        pytest.skip("Bundle has not been built")
    inline = config.inline
    config.inline = True
    try:
        esm = DatePicker._render_esm(compiled=True, server=False)
    finally:
        config.inline = inline
    assert esm == INLINE_BUNDLE_PATH.read_text(encoding="utf-8")
    assert not re.search(r'import\(\s*"\./', esm)
