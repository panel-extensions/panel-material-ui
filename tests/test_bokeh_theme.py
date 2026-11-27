import json
import pathlib
import shutil
import subprocess

import pytest

import panel_material_ui

NODE = shutil.which('node')
MODULE = pathlib.Path(panel_material_ui.__file__).parent / 'bokeh_theme.js'

pytestmark = pytest.mark.skipif(NODE is None, reason='node is required')


def run(script):
    setup = """
      function model(values, explicit = []) {
        return {
          ...values,
          properties: Object.fromEntries(Object.keys(values).map(name => [name, {dirty: explicit.includes(name)}])),
          setv(updates) {
            Object.assign(this, updates)
            for (const name of Object.keys(updates)) { this.properties[name].dirty = true }
          },
        }
      }
    """
    result = subprocess.run(
        [NODE, '--no-warnings', '--input-type=module', '-e',
         f'import {{apply_plot_theme}} from {json.dumps(MODULE.as_uri())};{setup}{script}'],
        capture_output=True, text=True, check=True,
    )
    return json.loads(result.stdout)


def test_explicit_styles_are_preserved_while_defaults_are_themed():
    assert run("""
      const p = model({color: 'red', alpha: 1, font: 'helvetica'}, ['color', 'alpha'])
      apply_plot_theme(p, {color: 'black', alpha: 0, font: 'Roboto'})
      console.log(JSON.stringify([p.color, p.alpha, p.font]))
    """) == ['red', 1, 'Roboto']


def test_defaults_follow_repeated_theme_changes():
    assert run("""
      const p = model({color: 'white'})
      for (const color of ['black', 'white', 'black']) { apply_plot_theme(p, {color}) }
      console.log(JSON.stringify(p.color))
    """) == 'black'


def test_external_change_is_preserved_across_later_theme_changes():
    assert run("""
      const p = model({color: 'white'})
      apply_plot_theme(p, {color: 'black'})
      p.setv({color: 'red'})
      apply_plot_theme(p, {color: 'white'})
      apply_plot_theme(p, {color: 'black'})
      console.log(JSON.stringify(p.color))
    """) == 'red'


def test_models_have_independent_styles():
    assert run("""
      const a = model({color: 'red'}, ['color'])
      const b = model({color: 'white'})
      apply_plot_theme(a, {color: 'black'})
      apply_plot_theme(b, {color: 'black'})
      console.log(JSON.stringify([a.color, b.color]))
    """) == ['red', 'black']


def test_explicit_null_and_zero_are_preserved():
    assert run("""
      const p = model({color: null, alpha: 0}, ['color', 'alpha'])
      apply_plot_theme(p, {color: 'black', alpha: 1})
      console.log(JSON.stringify([p.color, p.alpha]))
    """) == [None, 0]


def test_custom_color_preserves_alpha_omitted_by_serialization():
    assert run("""
      const p = model({outline_line_color: '#ff0066', outline_line_alpha: 1}, ['outline_line_color'])
      for (const alpha of [0, 0.25, 0]) {
        apply_plot_theme(p, {outline_line_color: 'black', outline_line_alpha: alpha})
      }
      console.log(JSON.stringify([p.outline_line_color, p.outline_line_alpha]))
    """) == ['#ff0066', 1]


def test_default_color_and_alpha_follow_theme_switches():
    assert run("""
      const p = model({outline_line_color: 'black', outline_line_alpha: 1})
      apply_plot_theme(p, {outline_line_color: 'white', outline_line_alpha: 0.25})
      apply_plot_theme(p, {outline_line_color: 'black', outline_line_alpha: 0})
      console.log(JSON.stringify([p.outline_line_color, p.outline_line_alpha]))
    """) == ['black', 0]
