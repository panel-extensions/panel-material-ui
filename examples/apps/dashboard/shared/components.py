import panel as pn
import panel_material_ui as pmu
from .config import PAGES
import param

def create_menu(selected: str, pages: list[tuple] = PAGES, button_color="primary"):
    items = pn.Column()
    for name_, href, icon in pages:
        button_style = "contained" if selected == name_ else "text"
        button_type = button_color if selected == name_ else "default"
        button = pmu.widgets.Button(
            name=name_,
            icon=icon,
            sizing_mode="stretch_width",
            button_style=button_style,
            button_type=button_type,
            margin=(0, 10),
            href=href,
        )
        items.append(button)
    return items
