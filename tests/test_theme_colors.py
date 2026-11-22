import json
import pathlib
import shutil
import subprocess

import pytest

import panel_material_ui

NODE = shutil.which('node')
THEME_COLORS = pathlib.Path(panel_material_ui.__file__).parent / 'theme_colors.js'

pytestmark = pytest.mark.skipif(NODE is None, reason='node is required')


def run(call):
    script = (
        f"const m = await import({json.dumps(THEME_COLORS.as_uri())});"
        f"console.log(JSON.stringify(m.{call}))"
    )
    out = subprocess.run(
        [NODE, '--no-warnings', '--input-type=module', '-e', script],
        capture_output=True, text=True, check=True
    )
    return json.loads(out.stdout)


def primary_text_color(main, backgrounds=('#121212',)):
    return run(f"primary_text_color({json.dumps(main)}, {json.dumps(list(backgrounds))})")


def contrast(fg, bg):
    def luminance(color):
        rgb = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
        r, g, b = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    l1, l2 = sorted([luminance(fg), luminance(bg)], reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


@pytest.mark.parametrize('main', ['#0072B5', '#1976d2', '#6200ee', '#000080', '#2e7d32'])
def test_failing_primary_is_lightened_to_aa_contrast(main):
    assert contrast(main, '#121212') < 4.5
    text = primary_text_color(main)
    assert text != main
    assert contrast(text, '#121212') >= 4.5


def test_default_flowdash_primary_tint():
    # The tint is lightened by the 0.35 floor, past the minimum needed for 4.5:1.
    text = primary_text_color('#0072B5')
    assert text == '#59a3cf'
    assert contrast(text, '#121212') > 6.5


@pytest.mark.parametrize('main', ['#90caf9', '#58A9DE', '#ffffff'])
def test_passing_primary_is_unchanged(main):
    assert primary_text_color(main) == main


def test_contrast_against_lightest_background():
    text = primary_text_color('#0072B5', ['#121212', '#2c2c2c'])
    assert contrast(text, '#2c2c2c') >= 4.5


@pytest.mark.parametrize('main', ['var(--brand)', 'rebeccapurple'])
def test_unparseable_primary_is_unchanged(main):
    assert primary_text_color(main) == main


def test_parses_short_hex_and_rgb():
    assert primary_text_color('#00f') != '#00f'
    assert primary_text_color('rgb(0, 114, 181)') == '#59a3cf'


def test_elevated_surface_matches_mui_overlay():
    # MUI's dark Paper at elevation 8 is #121212 under an 11.9% white overlay.
    assert run("elevated_surface('#121212', 8)") == '#2e2e2e'


@pytest.mark.parametrize('main', ['#0072B5', '#6200ee', '#000080'])
def test_tint_is_readable_on_elevated_surfaces(main):
    text = primary_text_color(main, ['#121212', '#2e2e2e'])
    assert contrast(text, '#2e2e2e') >= 4.5
