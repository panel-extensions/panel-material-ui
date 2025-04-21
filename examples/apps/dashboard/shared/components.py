import panel as pn
import panel_material_ui as pmu
from .config import PAGES
import param

def create_menu(selected: str, pages: list[tuple] = PAGES, button_color="primary"):
    items = []
    active = -1
    for index, page in enumerate(list(pages)):
        name_, href, icon = page
        item = {"label": name_, "icon": icon, "href": href}
        items.append(item)
        if selected==name_:
            active=index
    return pmu.List(items=items, active=active, margin=(0,10), sizing_mode="stretch_width")
