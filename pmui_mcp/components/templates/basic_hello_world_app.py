import panel as pn
import panel_material_ui as pmui

pn.extension(sizing_mode="stretch_width")

text = "Hello World ⭐⭐⭐⭐⭐"
text_len = len(text)

def model(n=text_len):
    return text[0:n]

def create_app():
    slider = pmui.IntSlider(value=5, start=1, end=text_len)

    interactive_model = pn.bind(model, n=slider)

    page = pmui.Page(
        title="Hello World App",
        main=[interactive_model],
        sidebar=[slider],
    )
    return page

if __name__ == "__main__":
    # python path_to_this_file.py
    create_app().show(port=5007, autoreload=True, open=True)
elif pn.state.served:
    # run with panel serve path_to_this_file.py --port 5007 --dev --show
    create_app().servable()
