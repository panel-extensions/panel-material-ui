# ❤️ Developer Guide

Welcome. We are so happy that you want to contribute.

`panel-material-ui` is automatically built, tested and released on Github Actions. The setup heavily leverages `pixi`, though we recommend using it, you can also set up your own virtual environment.

`panel-material-ui`, unlike other Panel extensions, has to be compiled and is shipped with a compiled JavaScript bundle. When making any changes you must recompile it.

## 🧳 Prerequisites

- [Git CLI](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
- Install [Pixi](https://pixi.sh/latest/#installation)

## 📙 How to

Below we describe how to install and use this project for development.

### 💻 Clone the repository

To install for development you will have to clone the repository with git:

```bash
git clone https://github.com/panel-extensions/panel-material-ui.git
cd panel-material-ui
```

### Install Pixi

Install pixi as described on the [Pixi web site](https://pixi.sh/latest/).

To see all available commands run:

```bash
pixi task list
```

### Developing

To install the dependencies run:

```bash
pixi install
```

In order for changes to the React code (i.e. the .jsx files) to take effect you need to recompile the JS bundle. To make this process easier we recommend you run:

```bash
pixi run compile-dev
```

**This will continuously watch the files for changes and automatically recompile**.

In a separate terminal you can now launch a Panel server to preview the components:

```bash
pixi run serve-dev
```

### Testing

To run the test suite locally you can run linting, unit tests and UI tests with:

```bash
pixi run pre-commit-run
pixi run -e test-312 test
pixi run -e test-ui test-ui
```
