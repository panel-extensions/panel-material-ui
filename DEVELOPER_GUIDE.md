# ❤️ Developer Guide

Welcome. We are so happy that you want to contribute.

## 🧳 Prerequisites

- [Git CLI](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
- Install [Pixi](https://pixi.sh/latest/#installation)

## 📙 How to

Below we describe how to install and use this project for development.

### 💻 Install for Development

To install for development you will have to clone the repository with git:

```bash
git clone https://github.com/panel-extensions/panel-graphic-walker.git
cd panel-graphic-walker
```

Now you can either install `nodejs` and `esbuild` manually and then run:

```bash
pip install -e .
```

Alternatively we recommend developing with pixi. To get started run the following command to install into the default environment:

```bash
pixi run install
```

### Developing

Note that unlike other Panel based ESM components panel-material-ui components only work in compiled mode. This means that whenever you make any changes to the React implementation you have to recompile the JS bundle. To make this process easier we recommend you run:

```bash
pixi run compile-dev
```

This will continuously watch the files for changes and automatically recompile. And is equivalent to:

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
