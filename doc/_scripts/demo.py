import datetime as dt

import pandas as pd
import hvplot.pandas
import panel as pn
import panel_material_ui as pmui

pn.extension(inline=False)

df = pd.read_csv('https://datasets.holoviz.org/penguins/v1/penguins.csv')

WIDTH = 260
NO_PAD = {'& > p': {'margin-block': "0 !important"}}

pmui.widgets.base.MaterialWidget.width = WIDTH

menu_items = [
    {"label": "Home", "icon": "home"},
    {"label": "Catalog", "icon": "category"},
    {"label": "Checkout", "icon": "shopping_cart"},
]

color = pmui.RadioButtonGroup(options=pmui.COLORS[:-3], value='primary')
color_select = pmui.Select(options=pmui.COLORS[:-3], value='primary', color=color, width=200)
color.jslink(color, value='color')
color.jslink(color_select, value='value', bidirectional=True)

switch = pmui.BreakpointSwitcher(
    breakpoint='md',
    small=color_select,
    large=color
)

title = pmui.BreakpointSwitcher(
    breakpoint='md',
    small=pmui.Column(
        pmui.Typography('pmui', variant='h4', sx=NO_PAD, margin=0),
        pmui.Typography('Components', variant='h6', sx=dict(NO_PAD, color='gray'), margin=0),
        width=145, margin=(0, 5)
    ),
    large=pmui.Column(
        pmui.Typography('panel-material-ui', variant='h4', sx=NO_PAD, margin=0),
        pmui.Typography('Components', variant='h5', margin=0, sx=dict(NO_PAD, color='gray')),
        width=None, margin=(0, 5)
    ), width=None
)

drawer = pmui.Drawer('## Drawer')

pmui.Paper(
    pmui.Row(
        title,
        switch,
        pmui.ThemeToggle(styles={'margin-left': 'auto'}),
        sizing_mode='stretch_width'
    ),
    pmui.Tabs(
        ('Widgets', pn.FlexBox(
            pmui.Column(
                pmui.Typography('Sliders', variant='h6'),
                pmui.FloatSlider(label='FloatSlider', value=42.314, color=color),
                pmui.DateSlider(label='DateSlider', color=color, start=dt.datetime(2025, 4, 1), end=dt.datetime(2025, 4, 30), value=dt.datetime(2025, 4, 14)),
                pmui.EditableFloatSlider(label='EditableSlider', color=color, value=42.31, width=WIDTH),
                pmui.RangeSlider(label='RangeSlider', color=color, value=(13, 42))
            ),
            pmui.Column(
                pmui.Typography('Select', variant='h6'),
                pmui.Select(label='Select', options=pmui.COLORS, color=color, value='primary', width=WIDTH),
                pmui.MultiChoice(label='MultiChoice', options=pmui.COLORS, color=color, value=['primary']),
                pmui.MultiSelect(label='MultiSelect', color=color, options=pmui.COLORS, value=['primary'])
            ),
            pmui.Column(
                pmui.Typography('Text', variant='h6'),
                pmui.TextInput(label='TextInput', color=color, value='My Text'),
                pmui.PasswordInput(label='PasswordInput', color=color, value='mysupersecretpassword'),
                pmui.TextAreaInput(label='TextArea', color=color, value='1. Default\n2. Primary\n3. Secondary', rows=4)
            ),
            pmui.Column(
                pmui.Typography('Date & Time', variant='h6'),
                pmui.DatePicker(label='DatePicker', color=color, width=WIDTH),
                pmui.DatetimePicker(label='DatetimePicker', color=color, width=WIDTH),
                pmui.TimePicker(label='TimePicker', color=color)
            ),
            pmui.Column(
                pmui.Typography('Buttons', variant='h6'),
                pmui.Row(
                    pmui.Button(label='Button', color=color, icon='home'),
                    pmui.Button(label='Button', color=color, icon='home', variant='outlined')
                ),
                pmui.Row(
                    pmui.Fab(label='Fab', color=color, icon='home', variant='circular'),
                    pmui.Fab(label='Fab', color=color, icon='home', variant='extended')
                ),
                pmui.Row(
                    pmui.FileInput(label='FileInput', color=color),
                    pmui.FileInput(label='FileInput', color=color, variant='outlined')
                )
            ),
            pmui.Column(
                pmui.Typography('Menus', variant='h6'),
                pmui.Breadcrumbs(active=1, color=color, items=menu_items),
                pmui.List(active=1, color=color, items=menu_items),
                pmui.SpeedDial(active=1, color=color, items=menu_items),
                margin=10
            )
        )),
        ('Plots', pmui.Column(
            df.hvplot.scatter(
                x="bill_length_mm", y="bill_depth_mm", by="species",
                height=400, responsive=True, max_width=800
            ),
        )),
        ('Layouts', pn.FlexBox(
            pmui.Accordion(
                ('Accordion 1', 'Content'),
                ('Accordion 2', 'Content'),
                width=WIDTH, margin=(0, 10), active=[2]
            ),
            pmui.Card(
                'Card Content',
                title='Card',
                width=WIDTH, margin=(0, 10)
            ),
            pmui.Card(
                'Card Content',
                title='Card',
                width=WIDTH, margin=(0, 10)
            ),
            pmui.Column(
                pmui.Typography('Drawer', variant='h6'),
                pmui.RadioButtonGroup.from_param(drawer.param.anchor),
                pmui.Toggle.from_param(drawer.param.open),
                drawer,
                width=WIDTH, margin=(0, 10)
            ),
            pmui.Column(
                pmui.Typography('Paper', variant='h6'),
                pmui.Row(
                    pmui.Paper(width=50, height=50, margin=10, elevation=1),
                    pmui.Paper(width=50, height=50, margin=10, elevation=3),
                    pmui.Paper(width=50, height=50, margin=10, elevation=10),
                )
            ),
            margin=10
        )),
        color=color, sizing_mode='stretch_both',
    ),
    sizing_mode="stretch_both",
    styles={'overflow': 'hidden'}
).save(
    'doc/_static/demo.html',
    resources='cdn'
)
