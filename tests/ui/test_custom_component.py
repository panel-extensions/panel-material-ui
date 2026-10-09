import pytest

pytest.importorskip("playwright")

import param
from playwright.sync_api import expect

from panel.tests.util import serve_component
from panel_material_ui.base import CDN_BASE, DIST_PATH, MaterialUIComponent

pytestmark = pytest.mark.ui


class CustomButton(MaterialUIComponent):

    label = param.String(default="Custom")

    _esm = """
    import Button from "@mui/material/Button"

    export function render({model}) {
      const [label] = model.useState("label")
      return <Button variant="contained">{label}</Button>
    }
    """


@pytest.fixture
def local_bundle(page):
    # MaterialUIComponent imports the bundle and shims from the CDN, which
    # only has released versions, so serve the locally built files instead.
    def fulfill(route):
        name = route.request.url.split("?")[0].rsplit("/", 1)[-1]
        route.fulfill(path=DIST_PATH / name, content_type="text/javascript")
    page.route(f"{CDN_BASE}/*.js*", fulfill)


def test_material_ui_component_renders_with_transforms(page, local_bundle):
    widget = CustomButton(loading=True)
    serve_component(page, widget)

    expect(page.locator(".MuiButton-root")).to_have_text("Custom")
    expect(page.locator(".MuiCircularProgress-root")).to_have_count(1)

    widget.loading = False
    expect(page.locator(".MuiCircularProgress-root")).to_have_count(0)
