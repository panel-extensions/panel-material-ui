from brand import mui
import panel as pn
import panel_material_ui as pmui
import param
mui.configure()
pn.extension(sizing_mode="stretch_width")
import datetime
import pandas as pd

stop_server = pmui.Button(name='Drop the Connection', sizing_mode="stretch_width", color="error", variant="outlined")
stop_server.js_on_click(code="""
Bokeh.documents[0].event_manager.send_event({'event_name': 'connection_lost', 'publish': false})
""")

def get_quarters():
    start = datetime.datetime.now().year - 1
    dates = {}
    for year in range(start, start+10):
        dates[f"{year} Q1"]=datetime.date(year-1,12,31)
        dates[f"{year} Q2"]=datetime.date(year,3,31)
        dates[f"{year} Q3"]=datetime.date(year,6,30)
        dates[f"{year} Q4"]=datetime.date(year,9,30)
    return dates


class State(pn.viewable.Viewer):
    currency = param.Selector(default="EUR", objects=["EUR", "GBP", "USD"], label="Currency")
    time_start = param.CalendarDate()
    time_end = param.CalendarDate()

    notation_time_start = param.CalendarDate()
    notation_time_end = param.CalendarDate()

    def __init__(self, **params):
        super().__init__(**params)
        last_update = datetime.datetime.now().date() - datetime.timedelta(days=1)

        current_year = last_update.year
        end_year = datetime.date(current_year-1, 12, 31)
        self.time_start = end_year
        self.time_end = datetime.date(current_year+1, 12, 31)
        self.notation_time_start = self.time_start
        self.notation_time_end = last_update

    def __panel__(self):
        quarters = get_quarters()

        time_range_start = pmui.Select.from_param(self.param.time_start, options=quarters)
        time_range_end = pmui.Select.from_param(self.param.time_end, options=quarters)

        notation_time_start = pmui.DatePicker.from_param(self.param.notation_time_start)
        notation_time_end = pmui.DatePicker.from_param(self.param.notation_time_end)

        return pn.Column(
            self.param.currency,
            pmui.Row(time_range_start, time_range_end),
            pmui.Column(notation_time_start, notation_time_end),
        )

state = State()
example_buttons = pn.FlexBox(*[pmui.Button(name=color.capitalize(), color=color, width=120) for color in pmui.Button.param.color.objects])
github_link = pmui.Button(name="GitHub", color="primary", variant="outlined", href="https://github.com/panel-extensions/panel-material-ui", icon="open_in_new")
docs_link = pmui.Button(name="Docs", color="primary", variant="outlined", href="https://panel-material-ui.holoviz.org/", align="end", icon="open_in_new")

drawer = pmui.Drawer(pn.Spacer(height=75), stop_server, anchor="right", size=300)
open_drawer = pmui.ButtonIcon(icon="settings", sizing_mode="fixed", color="light")
open_drawer.js_on_click(args={'drawer': drawer}, code='drawer.data.open = !drawer.data.open')

page = pmui.Page(
    title="Orbitron",
    header=[pn.HSpacer(), open_drawer],
    sidebar=[pn.pane.Image("https://cdn.britannica.com/94/192794-050-3F3F3DDD/panels-electricity-order-sunlight.jpg", margin=(20,10,10,10), stylesheets=["img {border-radius: var(--mui-shape-borderRadius);}"]), pmui.Column("# Settings", state, pn.VSpacer(min_height=25), "### References", github_link, docs_link, sizing_mode="stretch_both", margin=(10,10), styles={"border": "1px solid gray"})],
    sidebar_width=425,
    main=[pmui.Container("<h2>Buttons</h2>", example_buttons, drawer)],
)

page.servable()
