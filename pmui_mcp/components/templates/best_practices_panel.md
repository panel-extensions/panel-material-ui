# Panel Best Practices

## Overview

Always use an intermediate to expert level user approach using param.Parameterized classed. Not a basic level widget based approach.

## Panel Application Development

### Core Architecture Principles

**Parameter-Driven Design**

- Create applications as `param.Parameterized` or `pn.Viewable` classes
- Let Parameters drive application state, not widgets directly
- Structure code so user interactions can be tested using Parameterized classes
- Use a source `data` parameter to drive your app - structure code so app state resets when source data changes

**Widget and Display Patterns**

- Create widgets from parameters: `pn.widgets.Select.from_param(state.param.parameter_name, ...)`
- Display Parameter objects in panes: `pn.pane.HoloViews(state.param.parameter_name, ...)`
- Prefer `pn.bind` or `@param.depends` without `watch=True` for reactive updates
- Use `.on_click` for Button interactions over `watch=True` patterns
- Avoid `pn.bind` or `@pn.depends` with `watch=True`, `.watch`, or `.link` methods as they make apps harder to reason about

**other**

- prefer using `.servable()` over `.show()` for serving applications
- use `pn.state.served:` to check if the app is being served instead of `if __name__ == "__main__"

### Code Organization

**Module Structure**

- Put data extractions and transformations in `data.py` - keep clean and reusable without HoloViz dependencies
- Put plot functions in `plots.py` - keep clean and reusable without Panel code
- Separate business logic from UI concerns

**Component Selection**

- Use `panel-graphic-walker` package for Tableau-like data exploration components
- Use `panel-material-ui` components for new projects or projects already using this package
- Continue using standard Panel components in existing projects that already use them

### Testing Strategy

**Testable Architecture**

- Structure code so user interactions can be tested through Parameterized classes
- Separate UI logic from business logic to enable unit testing
- Use parameter watchers and dependencies for reactive behavior that can be tested

## Best Practices

### Reactive Programming

- Prefer declarative reactive patterns over imperative event handling
- Use `@param.depends` decorators to create reactive methods
- Leverage parameter watchers for automatic state management

### Performance Considerations

- Use `sizing_mode="stretch_width"` for responsive layouts
- Avoid unnecessary parameter watchers that could cause performance issues
- Structure data flows to minimize redundant computations

### Error Handling

- Implement graceful handling of missing or invalid data
- Provide meaningful feedback to users when operations fail
- Use safe data access patterns for robust applications

### Does and Dont's

DON'T include 'bokeh' in list of extensions. I.e. not `pn.extension('bokeh')` but just `pn.extension()`.
DON'T serve with `python path_to_this_file.py --dev --show` but with `panel serve path_to_this_file.py --dev --show`.
DO set default sizing_mode to stretch_width (pn.extension(..., sizing_mode='stretch_width')). Then set `sizing_mode='fixed'` for specific components that need it.
DO always test that the app can run and be served.
DO prefer the Panel `pn.widgets.Tabulator` component for displaying tabular data over other Panel components for displaying tabulator data.
DO prefer intermediate level, param.Parameterized approach over basic level, widget based approach
DON'T user legacy `--autoreload` flag. Instead use `--dev` flag which is faster but requires watchfiles package installed.
In a sidebar the order should be: 1) optional image/logo, 2) short app description, 3) input widgets/filters, 4) additional documentation.

## Development Process

1. Create the main app file (app.py) if it does not already exist with a basic hello world app.
2. Serve the file if it does not already exist (`panel serve app.py --port 5007 --dev --show`) to show progress to the user
3. Create the functionality to extract and transform the data. Add tests to test that it works. Update the app file to display sample data.
4. Create the functionality to plot the data. Add tests to test that it works. Update the app file to display the plots.
5. Now create the Parameterized classes with parameters and add reactivity.
6. Finally focus on the layout. Add tests to test that it works.

Make sure to add, run and fix pytests before moving to next step.

## Example Patterns

### Parameter-Driven Widget Creation
```python
# Good: Widget driven by parameter
select_widget = pn.widgets.Select.from_param(
    self.param.model_type,
    name="Model Type"
)

# Avoid: Manual widget management
select_widget = pn.widgets.Select(
    options=['Option1', 'Option2'],
    value='Option1'
)
```

### Reactive Display Updates

```python
# Best: Depends functions and methods
@param.depends('model_results')
def create_plot(self):
    return create_performance_plot(self.model_results)

plot_pane = pn.pane.Matplotlib(
    self.create_plot
)

# Good: Bound functions and methods
def create_plot(self):
    return create_performance_plot(self.model_results)

plot_pane = pn.pane.Matplotlib(
    pn.bind(self.create_plot)
)

# Avoid: Manual updates with watchers
def update_plot(self):
    self.plot_pane.object = create_performance_plot(self.model_results)

self.param.watch(self.update_plot, 'model_results')
```

### Data-Driven Architecture

```python
class DataApp(param.Parameterized):
    data = param.DataFrame(default=pd.DataFrame())

    @param.depends('data', watch=True)
    def _reset_app_state(self):
        """Reset all app state when source data changes."""
        # Reset or update parameters but not widgets directly
        ...

    @param.depends('data')
    def _get_xyz(self):
        """Return some transformed object like a DataFrame or a Plot/ Figure."""
        # Keep this method short by using imported method from data or plots module
        ...
```

### Testing Reactivity

Below is shown reactivity can be tested in the test_characters_reactivity function.

```python
import panel as pn
import panel_material_ui as pmui
import param

pn.extension(sizing_mode="stretch_width")

text = "Hello World ⭐⭐⭐⭐⭐"
text_len = len(text)

class HelloWorld(pn.viewable.Viewer):
    """
    A simple Panel app that displays a "Hello World" message with a slider to control the length of the message.
    """
    characters = param.Integer(default=text_len, bounds=(1, text_len), doc="Number of characters to display")

    def __init__(self, **params):
        super().__init__(**params)

        with pn.config.set(sizing_mode="stretch_width"):
            self._characters_input = pmui.IntSlider.from_param(self.param.characters)
            self._inputs = pmui.Column(self._characters_input, sizing_mode="fixed", width=300)
            self._outputs = pmui.Column(self.model, sizing_mode="stretch_width")
            self._panel = pmui.Row(self._inputs, self._outputs, sizing_mode="stretch_width")


    @param.depends("characters")
    def model(self):
        """
        Returns the "Hello World" message truncated to the specified number of characters.
        """
        return text[0:self.characters]

    def __panel__(self):
        return self._panel

    @classmethod
    def create_app(cls, **params):
        """
        Create the Panel app with the interactive model and slider.
        """
        instance = cls(**params)
        return pmui.Page(
            title="Hello World App",
            main=list(instance._outputs),
            sidebar=list(instance._inputs),
        )

if __name__ == "__main__":
    # python path_to_this_file.py
    HelloWorld.create_app().show(port=5007, autoreload=True, open=True)
elif pn.state.served:
    # run with panel serve path_to_this_file.py --port 5007 --dev --show
    HelloWorld.create_app().servable()

def test_characters_reactivity():
    """
    Always test that the reactivity works as expected.
    Put tests in a separate test file.
    """
    # Test to be added in separate test file
    hello_world = HelloWorld()
    assert hello_world.model() == text[:hello_world.characters]
    hello_world.characters = 5
    assert hello_world.model() == text[:5]
    hello_world.characters = 3
    assert hello_world.model() == text[:3]
```

## hvPlot/ HoloViews

DON'T set the theme `hv.renderer('bokeh').theme = 'dark_minimal'`. Let Panel control the theme.
Prefer Bokeh over Plotly over Matplotlib backend/ renderer. So use Bokeh backed/ renderer unless explicitly asked otherwise
Never user Pie charts!

## Resources

- [Panel Intermediate Tutorials](https://panel.holoviz.org/tutorials/intermediate/index.html)
- [Panel Expert Tutorials](https://panel.holoviz.org/tutorials/expert/index.html)
- [Param Documentation](https://param.holoviz.org/)
- [Panel Material UI Components](https://panel-material-ui.holoviz.org/)
- [Panel Graphic Walker](https://panel-graphic-walker.holoviz.org/)
