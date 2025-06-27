# Copilot Instructions

This file provides custom instructions for GitHub Copilot based on our Best Practice Coding Guidelines.
Write code as a very experienced lead developer proficient in Python, Javascript  and React would do.
Enable users to use the code in notebooks and python scripts with minimal effort, while ensuring it is maintainable, secure, and high-quality.

## Core Coding Standards

Always add comprehensive docstrings using Numpy style format.
Use type hints for all function parameters and return values.
Follow PEP 8 style guidelines strictly.
Write concise, single-responsibility functions.
Use pathlib for file path operations instead of os.path.
Prefer f-strings for string formatting.
Add meaningful variable names that describe the data they contain.
Implement proper error handling with specific exception types.

## Preferred Technologies

Use Python as the primary programming language.
Use pixi for virtual environment management and package installation.
Use Pytest for all testing with Coverage.py for coverage reports.
Use Mypy for static type checking.
Use Ruff for code formatting, linting, and import sorting.
Use Typer for building command-line interfaces.
Use DuckDB for fast, portable database operations.
Use Pandas or Polars for DataFrame operations.
Use HoloViz Param to build reactive Python classes/ components.
Use React and Panel ReactComponent for front end side of components.
Use Sphinx for documentation generation.
Store project metadata in pyproject.toml files.

## Testing Requirements

Write unit tests for all public functions and methods.
Minimize use of mocks - prefer integration tests with real data.
Avoid docstring tests in favor of dedicated test files.
Achieve minimum 80% code coverage.
Use descriptive test names that explain what is being tested.
Use playwright for end-to-end testing of components and web applications.

## Documentation

We follow the Diataxis framework for technical documentation, which consists of four main categories: Tutorials, How-to Guides, Reference Guides, and Explanations.
All documentation is in the 'docs' folder except reference guides
Overall the tone of the documentation should be **modern**, **engaging** and **professional**. The goal is to help users, so the documentation should be clear, concise, and easy to follow.
Only add comments when necessary to explain complex logic. Avoid comments that restate the obvious.

### Docstrings

We add docstrings to all classes, param Parameters, methods, and functions.
The docstrings should be clear, concise, and follow the numpy style guide.
The docstrings of components should contain links to their reference guide as well as a short usage example like Button example.

```Python
class Button(_ButtonBase, _ClickButton):
    """
    The `Button` widget allows triggering events when the button is
    clicked.

    The Button provides a `value` parameter, which will toggle from
    `False` to `True` while the click event is being processed

    It also provides an additional `clicks` parameter, that can be
    watched to subscribe to click events.

    :References:

    - https://panel-material-ui.holoviz.org/reference/widgets/Button.html
    - https://panel.holoviz.org/reference/widgets/Button.html
    - https://mui.com/material-ui/react-button/

    :Example:

    >>> Button(label='Click me', icon='caret-right', button_type='primary')
    """
```

### Reference Guides

In the examples/reference subfolder, you will find reference guides for each component provided by the Panel Material UI extension.
During the build process the reference guide notebooks will be converted to markdown files in the 'docs/reference' folder.

Use the [`Button`](examples/reference/widgets/Button.ipynb), [`Checkbox`](examples/reference/widgets/CheckBox.ipynb) and [`CheckBoxGroup`](examples/reference/widgets/CheckBoxGrop.ipynb) reference guides as a **reference reference guides**:

When creating a new reference guide, follow these guidelines:

- Reuse MUI explanations and examples as much as possible
- Systematically document usage of each parameter and method. Preferably individually.
- Make sure to include the sections
  - "Parameters"
  - "Basic Usage"
  - "Disabled and Loading"
  -  "Aliases" (If more than `name` parameter is an alias)
  - "Example: Some simple app with pn.bind. Others if important for usage."
  - "API Reference"
  - "References"
- Use `label` over `name`. Similarly for other aliases.
- Use `pmui` shorthand, i.e. `import panel_material_ui as pmui`.
- use `pmui` components over `pn` components, i.e. `pmui.Column` over `pn.Column`

When asked to improve or finalize a reference guide, follow these guidelines:

"Please improve the reference notebook by fixing spelling errors and improving the language to help users of Panel Material UI use the component. Make it engaging but keep a professional tone."

## Security and Quality

Run Bandit security analysis on all code.
Use PyUpgrade to maintain modern Python syntax.
Implement proper logging using Python's logging module.
Handle secrets through environment variables or secure vaults.
Validate all external inputs and API responses.

## Git Workflow

Follow GitHub flow with feature branches.
Keep pull requests under 400 lines of changes.
Name branches using enhancement/xyz or fix/xyz format.
Install pre-commit before committing code.
Ensure all tests pass before merging.

## Project Context

This project is created by HoloViz team.
We are a group of domain specialists, data scientists and others passionate about data visualization.
We focus on Python data visualization use cases in .py and .ipynb files.
Read the README.md file in the root of the project for specific context.
