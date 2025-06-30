import panel as pn # DO import panel as pn
import panel_material_ui as pmui # DO import panel_material_ui as pmui
import param

# DO run pn.extension
# DO remember to add any imports needed by panes, e.g. pn.extension("tabulator", "plotly", ...)
# DON'T add "bokeh" as an extension. It is not needed.
pn.extension()

# DO organize functions to extract data separately as your app grows
# DO use caching to speed up the app, e.g. for expensive data loading or processing
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


    # DO use caching to speed up bound methods that are expensive to compute or load data
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
