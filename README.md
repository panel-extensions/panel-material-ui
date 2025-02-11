# ✨ Welcome to panel-material-ui

[![License](https://img.shields.io/badge/License-MIT%202.0-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://img.shields.io/github/actions/workflow/status/panel-extensions/panel-material-ui/ci.yml?style=flat-square&branch=main)](https://github.com/panel-extensions/panel-material-ui/actions/workflows/ci.yml)
[![conda-forge](https://img.shields.io/conda/vn/conda-forge/panel-material-ui?logoColor=white&logo=conda-forge&style=flat-square)](https://prefix.dev/channels/conda-forge/packages/panel-material-ui)
[![pypi-version](https://img.shields.io/pypi/v/panel-material-ui.svg?logo=pypi&logoColor=white&style=flat-square)](https://pypi.org/project/panel-material-ui)
[![python-version](https://img.shields.io/pypi/pyversions/panel-material-ui?logoColor=white&logo=python&style=flat-square)](https://pypi.org/project/panel-material-ui)

An extension to bring MaterialUI components to Panel.

## Installation

Install `panel-material-ui` via `pip`:

```bash
pip install panel-material-ui
```

## Development

This project is managed by [pixi](https://pixi.sh).
You can install the package in development mode using:

```bash
git clone https://github.com/panel-extensions/panel-material-ui
cd panel-material-ui

pixi run pre-commit-install
pixi run postinstall
pixi run test
```

Note that unlike other Panel based ESM components panel-material-ui components only work in compiled mode. When working on this project we recommend you run:

```bash
pixi run compile-dev
```

or run it directly:

```bash
panel compile panel_material_ui --build-dir build --watch --file-loader woff woff2
```

This will watch JS modules for changes and rebuild the JS and CSS bundles. You can then develop using the `components.py` application:

```bash
panel serve examples/components.py --autoreload
```

which will reload whenever the bundle is automatically rebuilt.
