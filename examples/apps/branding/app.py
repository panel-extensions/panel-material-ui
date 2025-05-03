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
        dates[f"{year} - Q1"]=datetime.date(year-1,12,31)
        dates[f"{year} - Q2"]=datetime.date(year,3,31)
        dates[f"{year} - Q3"]=datetime.date(year,6,30)
        dates[f"{year} - Q4"]=datetime.date(year,9,30)
    return dates


class State(pn.viewable.Viewer):
    currency = param.Selector(default="EUR", objects=["EUR", "GBP", "USD"], label="Currency")
    time_range = param.CalendarDateRange()
    notationtime_range = param.CalendarDateRange()

    def __panel__(self):
        quarters = get_quarters()
        time_range_start = pmui.Select(name='Time Start', options=quarters)
        time_range_end = pmui.Select(name='Time End', options=quarters)

        return pn.Column(
            self.param.currency,
            pn.Row(time_range_start, time_range_end),
            self.param.notationtime_range,
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
    sidebar=["# Settings", state, pn.VSpacer(), github_link, docs_link],
    sidebar_width=350,
    main=[pmui.Container("<h2>Buttons</h2>", example_buttons, drawer)],
)

page.servable()
