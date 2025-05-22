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

def create_card_with_jumbo_header(title: str, content: str):
    return pmu.Paper(
        pn.pane.Markdown(
            title,
            sizing_mode="stretch_width",
            styles={
                "background": "black",
                "color": "white",
                "border-radius": "5px",
                "position": "relative",
                "padding-left": "10px",
            },
            margin=10,
        ),
        content,
        margin=10,
    )

class Timeline(pmu.MaterialUIComponent):
    """Material‑UI **Timeline** component for Panel.

    References:

    - https://mui.com/material-ui/react-timeline/

    Example:

    >>> config = [
    ...     {"content_title": "Eat", "content": "Because you need strength", "opposite": "08:30", "color": "grey",   "variant": "filled", "icon": "fastfood"},
    ...     {"content_title": "Code", "content": "Because it's awesome!", "opposite": "09:00", "color": "primary", "variant": "filled", "icon": "laptop_mac"},
    ...     {"content_title": "Sleep", "content": "Because you need rest", "opposite": "09:30", "color": "secondary",   "variant": "outlined", "icon": "hotel"},
    ...     {"content_title": "Repeat", "content": "Because this is the life you love!", "opposite": "11:00", "color": "success",      "variant": "filled", "icon": "repeat"},
    ... ]
    >>> Timeline(object=config, width=600)
    """  # noqa: E501
    object = param.List(default=[], doc="""
    A list of dictionaries, each mapping directly onto a `TimelineItem` row.
    Supported keys:

    | key               | type | default | description                                                                                                       |
    |-------------------|------|---------|-------------------------------------------------------------------------------------------------------------------|
    | **content_title** | str  | *None*  | Header of `TimelineContent`.                                                                                      |
    | **content**       | str  | *None*  | Body of `TimelineContent`.                                                                                        |
    | **opposite_title**| str  | *None*  | Header of `TimelineOppositeContent`.                                                                              |
    | **opposite**      | str  | *None*  | Body of `TimelineOppositeContent`.                                                                                |
    | **color**         | str  | primary | Color prop of `TimelineDot`.                                                                                      |
    | **variant**       | str  | filled  | Variant prop of `TimelineDot` (filled/ outlined).                                                                 |
    | **icon**          | str  | *None*  | Lowercase name of `Icon`.                                                                                         |
    | **disable_dot**   | bool | *None*  | If `True`, the `Icon` is shown standalone and not inside the `TimelineDot`.                                       |
    """)

    position = param.Selector(default="right", objects=[
      'alternate-reverse',
      'alternate',
      'left',
      'right',
    ], doc="""The position of the content/ opposite content.""")

    _esm_base = "Timeline.jsx"
