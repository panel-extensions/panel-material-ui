# ❤️ Developer Guide

Welcome. We are so happy that you want to contribute.

`panel-material-ui` is automatically built, tested and released on Github Actions. The setup heavily leverages `pixi`, though we recommend using it, you can also set up your own virtual environment.

`panel-material-ui`, unlike other Panel extensions, has to be compiled and is shipped with a compiled JavaScript bundle. When making any changes you must recompile it.

## 🧳 Prerequisites

- [Git CLI](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
- Install [Pixi](https://pixi.sh/latest/#installation)

## 📙 How to

Below we describe how to install and use this project for development.

### 💻 Install for Development

To install for development you will have to clone the repository with git:

```bash
git clone https://github.com/panel-extensions/panel-material-ui.git
cd panel-material-ui
```

If you want to manage your own environment, including installations of `nodejs` and `esbuild` (e.g. using conda) set up your development environment with:

```bash
pip install -e .
```

### Developing

Whenever you make any changes to the React implementationsof the components  (i.e. the .jsx files) you have to recompile the JS bundle. To make this process easier we recommend you run:

```bash
pixi run compile-dev
```

This will continuously watch the files for changes and automatically recompile. This is equivalent to:

```bash
panel compile panel_material_ui --build-dir build --watch --file-loader woff woff2
```

In a separate terminal you can now launch a Panel server to preview the components:

```bash
pixi run serve-dev
```

This is equivalent to:

```bash
panel serve examples/components.py --dev --port 0 --show
```

### Testing

To run the test suite locally you can run linting, unit tests and UI tests with:

```bash
pixi run pre-commit-run
pixi run -e test-312 test
pixi run -e test-ui test-ui
```
