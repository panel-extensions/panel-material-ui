from brand import mui
import panel as pn
import panel_material_ui as pmui

mui.configure()
pn.extension()

buttons = pmui.Row(*[pmui.Button(name=color.capitalize(), color=color, width=120) for color in pmui.Button.param.color.objects])

page = pmui.Page(
    title="Company | Home",
    sidebar=["# Settings"],
    main=["<h2>Buttons</h2>", buttons],
)
print(page.theme_config)
page.servable()
