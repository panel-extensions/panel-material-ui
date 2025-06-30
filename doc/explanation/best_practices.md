# Best Practices: Panel Material UI

This guide provides best practices for using Panel Material UI. Optimized for LLMs.

Please develop code, tests and documentation as an **expert Panel analytics app developer** would do when working with a **short time to market**.

## Best Practice Hello World App

Let's describe our best practices via a basic Hello World App:

```python
import panel as pn # DO import panel as pn
import panel_material_ui as pmui # DO import panel_material_ui as pmui
import param

# DO run pn.extension
# DO remember to add any imports needed by panes, e.g. pn.extension("tabulator", "plotly", ...)
# DON'T add "bokeh" as an extension. It is not needed.
pn.extension()

# DO organize functions to extract data separately as your app grows
# DO use caching to speed up the app, e.g. for expensive data loading or processing that would return the same result given same input arguments.
@pn.cache(max_items=3)
def extract(n=5):
    return "Hello World" + "⭐" * n

text = extract()
text_len = len(text)

# DO organize functions to transform data separately as your app grows. Eventually in a separate transform.py file
def transform(data: str, count: int=5)->str:
    """
    Transforms the input data by truncating it to the specified count of characters.
    """
    count = min(count, len(data))
    return data[:count]

# DO organize functions to create plots separately as your app grows. Eventually in a separate plots.py file.
# DO organize custom components and views separately as your app grows. Eventually in separate components.py or views.py file(s).

# DO use param.Parameterized, pn.viewable.Viewer or similar approach to create new components and apps with state and reactivity
class HelloWorld(pn.viewable.Viewer):
    """
    A simple Panel app that displays a "Hello World" message with a slider to control the length of the message.
    """
    # DO define parameters to hold state and drive the reactivity
    characters = param.Integer(default=text_len, bounds=(0, text_len), doc="Number of characters to display")

    def __init__(self, **params):
        super().__init__(**params)

        # DO use sizing_mode="stretch_width" for components unless "fixed" or other sizing_mode is specifically needed
        with pn.config.set(sizing_mode="stretch_width"):
            # DO create widgets using `.from_param` method
            self._characters_input = pmui.IntSlider.from_param(self.param.characters, margin=(10,20))
             # DO Collect input widgets into horizontal, columnar layout unless other layout is specifically needed
            self._inputs = pmui.Column(self._characters_input, max_width=300)
             # DO collect output components into some layout like Column, Row, FlexBox or Grid depending on use case
            self._outputs = pmui.Column(self.model)
            self._panel = pmui.Row(self._inputs, self._outputs)


    # DO use caching to speed up bound methods that are expensive to compute or load data and return the same result for a given state of the class.
    @pn.cache
    # DO prefer .depends over .bind over .rx for reactivity methods on Parameterized classes as it can be typed and documented
    # DON'T use `watch=True` or `.watch` methods to update UI. Only for updating overall app or component state.
    # DO use `watch=True` or `.watch` for triggering side effect like saving file or sending email.
    @param.depends("characters")
    def model(self):
        """
        Returns the "Hello World" message truncated to the specified number of characters.
        """
        return transform(text, self.characters)

    # DO provide a method for displaying the component in a notebook setting, i.e. without using a Template or Page element
    def __panel__(self):
        return self._panel

    # DO provide a method to create a .servable app
    @classmethod
    def create_app(cls, **params):
        """
        Create the Panel app with the interactive model and slider.
        """
        instance = cls(**params)
        # DO use the `Page` to layout the served app unless otherwise specified
        return pmui.Page(
            # DO provide a title for the app
            title="Hello World App",
            # DO provide optional image, optional app description, optional navigation menu, input widgets, optional documentation and optional links in the sidebar
            # DO provide as list of components or a list of single horizontal layout like Column as the sidebar by default is 300 px wide
            sidebar=list(instance._inputs),
            # DO provide a list of layouts and output components in the main area of the app.
            # DO use Grid or FlexBox layouts for complex dashboard layouts instead of combination Rows and Columns.
            main=list(instance._outputs),
        )

# DO provide a method to serve the app with `python`
if __name__ == "__main__":
    # DO run with `python path_to_this_file.py`
    HelloWorld.create_app().show(port=5007, autoreload=True, open=True)
# DO provide a method to serve the app with `panel serve`
elif pn.state.served:
    # DO run with `panel serve path_to_this_file.py --port 5007 --dev` add `--show` to open the app in a browser
    HelloWorld.create_app().servable() # DO mark the element(s) to serve with .servable()
```

DO always create test in separate test files and DO run test via pytest:


```python
import ...

# DO put tests into separate test file(s)
# DO test the reactivity of each parameter, function, method, component or app.
# DO run pytest when the code is changed. DON'T create non-pytest scripts or files to test the code.
def test_characters_reactivity():
    """
    Always test that the reactivity works as expected.
    Put tests in a separate test file.
    """
    # Test to be added in separate test file
    hello_world = HelloWorld()
    assert hello_world.model() == text[:hello_world.characters] # DO test the default values of bound methods
    hello_world.characters = 5
    assert hello_world.model() == text[:5] # DO test the reactivity of bound methods when parameters change
    hello_world.characters = 3
    assert hello_world.model() == text[:3]
```

DO note how this test simulates the user's behaviour of loading the page, changing the `characters` input and updating the output without having to write client side tests.

## General Guidelines

- DO use the new names parameter names (e.g. `label`, `color`) instead of legacy aliases (e.g. `name`, `button_type` etc) for pmui components.
- DO use `sizing_mode` parameter over `sx` css styling parameter.
- DO use Material UI `sx` parameter for all css styling of over `styles` and `stylesheets`.
- DO use panel-material-ui components instead of panel components for projects already using panel-material-ui and for new projects

## Component Guidelines

### Page

- DO provide the title to the `Page.title` argument. DON'T provide it in the `Page.main` area.
- DO provide an optional image, description, navigation menu to the `Page.sidebar` argument. Normally DON't put them in the `header` or `main` areas.
- DO provide the input widgets as children to the `Page.sidebar` argument
- DO not add advanced or high components to the `Page.header` as it is only 100px high by default. Normally only buttons, indicators, text and navigation links go into the header.
- DON'T include `ThemeToggle` or other widgets to toggle the theme when using the `Page`. A `ThemeToggle` is already built in.

DO provide lists of children to the `Page.sidebar`, `Page.main` or `Page.header` arguments:

```python
pmui.Page(
    header=[component1, component2],  # This is correct
    sidebar=[component3, component4],  # This is correct
    main=[component5, component6],  # This is correct
)
```

DON'T provide non-lists as children to the `Page.sidebar`, `Page.main` or `Page.header` arguments:

```python
pmui.Page(
    header=component1,  # This is incorrect
    sidebar=component2,  # This is incorrect
    main=component3,  # This is incorrect
)
```

#### Linking Dashboard Theme with Page Theme

DO synchronize component themes with Page theme:

```python
    ...

    dark_theme = param.Boolean(
        doc="""True if the theme is dark""",
        allow_refs=True # To enable provide parameters and bound function references
        )

    @classmethod
    def create_app(cls, **params):
        """Create app with synchronized theming."""
        component = cls(**params)

        page = pmui.Page(
            ...,
            dark_theme=component.dark_theme,  # Pass theme to Page
        )

        # Synchronize Page theme to component theme
        component.dark_theme = page.param.dark_theme
        return page
```

### Column

- DO use `size` parameter instead of `xs`, `sm` or `md` parameters - they do not exist.

### List like layouts

For list-like layouts like `Column` and `Row` DO provide children as positional arguments:

```python
pmui.Row(child1, child2, child3) # DO
```

DON'T provide them as separate arguments:

```python
pmui.Row([child1, child2, child3,]) # DON'T
```

### Switch

- Do add `margin=(10, 20)` when displaying in the sidebar.

### Sliders

- DO add a little bit of margin left and right when displaying in the sidebar.

### Cards

- DO use the `Paper` component over the `Card` unless you need the `Card`s extra features.
- DO set `collapsible=False` unless collapsible is needed.

### Non-Existing Components

- Do use `Column` instead of `Box`. The `Box` component does not exist.

## Panel Best Practices

This section provides best practices for using Panel

### General Guidelines

- DO prefer an [intermediate](https://panel.holoviz.org/tutorials/intermediate/index.html) to [expert](https://panel.holoviz.org/tutorials/expert/index.html) level user approach using param.Parameterized classed. Not a [basic](https://panel.holoviz.org/tutorials/basic/index.html) level widget based approach.

### Core Architecture Principles

**Parameter-Driven Design**

- DO prefer declarative reactive patterns over imperative event handling
- DO create applications as `param.Parameterized` or `pn.Viewable` classes
- DO let Parameters drive application state, not widgets directly
- DO structure your code using Parameterized classes, so that user interactions can be tested be testing on the Python server side.

**UI Update Patterns**

- Create widgets from parameters: `pn.widgets.Select.from_param(state.param.parameter_name, ...)`
- Display Parameter values in components: `pn.pane.HoloViews(state.param.parameter_name, ...)`
- DO Update UI components via parameters our reference .bind and .depends functions and methods, i.e.
  - `pn.pane.HoloViews(state.param.parameter_name, ...)` is OK
  - `pn.pane.Markdown(bound_function)` is OK
- DON'T update UI components as side effects with `.watch` functions or with `watch=True`, i.e.
  - `holoviews_panel.object = some_plot` is NOT OK
  - `markdown_pane.object = some_object` is NOT OK
- DO feel free to update component or app parameter state via `.watch` or `watch=True` functions and methods.
- DO feel free to trigger non-UI, side-effects like external computations or sending emails via `.watch` or `watch=True` functions and methods.
- DON't use `.link` its hard to reason about.
- DO create the overall layout and content structure once, but update the content dynamically. This eliminates flickering and provides a smooth, professional user experience.

**Module Structure**

- Put data extractions in `extract.py`, data transformations in `transformations.py` - keep both clean and reusable without HoloViz dependencies
- Put plot functions in `plots.py` - keep it clean and reusable without Panel code
- Put custom components in `components.py` and custom views in `views.py`
- Separate business logic from UI concerns

**Component Selection**

- DO use [`panel-graphic-walker`](https://github.com/panel-extensions/panel-graphic-walker) package for Tableau-like data exploration components
- DO use [`panel-material-ui`](https://panel-material-ui.holoviz.org/) components for new projects or projects already using this package
- DO prefer the Panel `pn.widgets.Tabulator` component for displaying tabular data over other Panel components for displaying tabulator data.

**Other**

- DO always include `pn.extension` in your main app file.
- DO include extensions like Tabulator and Plotly in pn.extension if used by the application, e.g. `pn.extension("tabulator", "plotly").
    - DON'T include 'bokeh' in list of extensions, i.e. `pn.extension("bokeh")` is not valid.
- DO use `if pn.state.served:` to check if the app is being `panel serve` served
- DO use `if __name__ == "__main__:` to check if the app being being `python` served
- DO prefer to serve with `panel serve path_to_this_file.py --dev --show` instead of `python path_to_this_file.py`.
    DON'T use legacy `--autoreload` flag. Instead use `--dev` flag which reloads faster but requires `watchfiles` package installed.
- DO keep start a panel development server with hot reload using `panel serve ...`. DO keep it running alive during development - it will automatically reload as you update the code.
    - DON'T `kill` or `pkill` the panel server while developing and testing.
- DO use sizing_mode='stretch_width' for all components unless you specifically want another `sizing_mode` like `fixed` or `stretch_both`.
- DO always test that the app can run and be served.

In a sidebar the order should be: 1) optional image/logo, 2) short app description, 3) input widgets/filters, 4) additional documentation.
Don't recreate components when it can be avoided. Instead bind them to bound/ depends function and methods.

## Development Process

**Start with the data. End with layout and styling**

1. Create the main app file (app.py) if it does not already exist with a basic hello world app.
2. Serve the file if it does not already exist (`panel serve app.py --port 5007 --dev --show`) to show progress to the user.
  - DON'T kill the app - it will automatically reload when the code is updated.
3. Create the functionality to extract and transform the data.
  - Update the app file to display sample data.
  - Add and run tests to test that everything works.
4. Create the functionality to plot the data.
  - Update the app file to display the plots.
  - Add and run tests to test that everything works.
5. Now create the Parameterized classes with parameters, widgets, output and layout components.
  - Provide reference .bind and .depends functions and methods as arguments.
  - Update the app file to display inputs and outputs.
  - Add and run tests to test that everything works.
6. Finally focus on the layout and styles.
  - Add and run tests to test that everything works.

Make sure to run pytests and fix issues before moving to next step.

### Testing Strategy

**Testable Architecture**

- DO structure your code so user interactions can be tested through Parameterized classes
- DO separate UI logic from business logic to enable unit testing
- DO separate models, data extraction, data transformation, plots generation, custom components and views, styles etc. to enable unit testing as your app grows

### Example Patterns

#### Parameter-Driven Widget Creation
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

#### Reactive Display Updates

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

#### Data-Driven Architecture

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

#### Convert widget date values to Timestamp for comparison

When comparing to data values to Pandas series:

```python
start_date, end_date = self.date_range
# DO convert date objects to pandas Timestamp for proper comparison
start_date = pd.Timestamp(start_date)
end_date = pd.Timestamp(end_date)
filtered = filtered[
    (filtered['date'] >= start_date) &
    (filtered['date'] <= end_date)
]
```

#### Don't recreate static components

Don't recreate static, nested components

```python
import panel as pn
import panel_material_ui as pmui
import param

pn.extension()

class HelloWorld(pn.viewable.Viewer):
    characters = param.Integer(default=10, bounds=(1, 100), doc="Number of characters to display")

    @param.depends("characters")
    def _get_kpi_card(self):
        # Dont recreate static-nested components every time
        # Will make the web site flickr as it recreates from scratch
        return pmui.Paper(
            pmui.Column(
                pmui.Typography(
                    "📊 Key Performance Metrics",
                    variant="h6",
                    sx={
                        "color": "text.primary",
                        "fontWeight": 700,
                        "mb": 3,
                        "display": "flex",
                        "alignItems": "center",
                        "gap": 1
                    }
                ),
                pmui.Row(
                    f"The kpi is {self.characters}",
                )
            ),
    )

    def __panel__(self):
        return pmui.Paper(
            pmui.Column(
                self.param.characters,
                self._get_kpi_card,
            ),
            sx={"padding": "20px", "borderRadius": "8px"},
            sizing_mode="stretch_width"
        )

if pn.state.served:
    HelloWorld().servable()
```

Instead create static layouts and components with reactive/ bound/ reference values

```python
import panel as pn
import panel_material_ui as pmui
import param

pn.extension()

class HelloWorld(pn.viewable.Viewer):
    characters = param.Integer(default=10, bounds=(1, 100), doc="Number of characters to display")

    def _get_kpi_card(self):
        # Create a static layout once
        return pmui.Paper(
            pmui.Column(
                pmui.Typography(
                    "📊 Key Performance Metrics",
                    variant="h6",
                    sx={
                        "color": "text.primary",
                        "fontWeight": 700,
                        "mb": 3,
                        "display": "flex",
                        "alignItems": "center",
                        "gap": 1
                    }
                ),
                pmui.Row(
                    # Use a reactive/ bound/ reference value for dynamic content
                    self.kpi_value
                )
            ),
        )

    @param.depends("characters")
    def kpi_value(self):
        return f"The kpi is {self.characters}"

    def __panel__(self):
        return pmui.Paper(
            pmui.Column(
                self.param.characters,
                self._get_kpi_card(),
            ),
            sx={"padding": "20px", "borderRadius": "8px"},
            sizing_mode="stretch_width"
        )

if pn.state.served:
    HelloWorld().servable()
```

## hvPlot/ HoloViews

### General Guidelines

- DO let Panel control the renderer theme.
  - DON'T set the theme `hv.renderer('bokeh').theme = 'dark_minimal'`.
- Prefer Bokeh over Plotly over Matplotlib renderer.
  - Bokeh works great for interactive and advanced scientific visualisations
  - Plotly works great for interactive and simpler business visualizations
  - Matplotlib works great for static plots in static reports
- DO user bar charts over pie Charts. Pie charts are not supported.

### Formatting Axes

- DO use NumeralTickFormatter using 'a' formatter for axis:

| Input | Format String | Output |
| - |  - | - |
| 1230974 | '0.0a' | 1.2m |
| 1460 | '0 a' | 1 k |
| -104000 | '0a' | -104k |

## Plotly

DO make the *plot* methods depend on a `theme` or `dark_theme` parameter:

```python
    @param.depends("data", "dark_theme")
    def create_plot(self) -> go.Figure:
        fig = ...
        template = "plotly_dark" if dark_theme else "plotly_white"
        fig.update_layout(template=template,)
        return fig
```
