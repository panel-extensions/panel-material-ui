import panel as pn
import panel_material_ui as pmu
from .config import PAGES
import param
import copy

def create_menu(selected: str, pages: list[tuple] = PAGES, button_color="primary"):
    active = -1
    for index, page in enumerate(pages):
        if selected==page["label"]:
            active=index

    def get_pages(button_color):
        pages2 = copy.deepcopy(pages)
        for item in pages2:
            item["color"]=button_color
        return pages2
    return pmu.List(items=pn.bind(get_pages, button_color), active=active, margin=(0,10), sizing_mode="stretch_width")
