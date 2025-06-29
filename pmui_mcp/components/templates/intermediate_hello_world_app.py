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
