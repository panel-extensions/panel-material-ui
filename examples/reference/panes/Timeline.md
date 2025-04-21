# Timeline

```python
import panel as pn
import panel_material_ui as pmu

pn.extension()
```

The ``Timeline`` *pane* displays a list of events in chronological order. It **is** based on the Material&nbsp;UI [`Timeline`](https://mui.com/material-ui/react-timeline/) component.

Discover more about using *panes* to display objects in [how‑to construct panes](https://panel.holoviz.org/how_to/components/construct_panes.html).

## API

### Parameters

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

#### Core

* **`position`** (str): The position of the content/opposite content.
* **`object`** (list[str]): A list of dictionaries, each mapping directly onto a `TimelineItem` row. Supported keys:

    | key                | type | default | description                                                                                                       |
    |--------------------|------|---------|-------------------------------------------------------------------------------------------------------------------|
    | **content_title**  | str  | *None*  | Header of [`TimelineContent`](https://mui.com/material-ui/api/timeline-content/).                                 |
    | **content**        | str  | *None*  | Body of [`TimelineContent`](https://mui.com/material-ui/api/timeline-content/).                                   |
    | **opposite_title** | str  | *None*  | Header of [`TimelineOppositeContent`](https://mui.com/material-ui/api/timeline-opposite-content/).                |
    | **opposite**       | str  | *None*  | Body of [`TimelineOppositeContent`](https://mui.com/material-ui/api/timeline-opposite-content/).                  |
    | **color**          | str  | primary | Color prop of [`TimelineDot`](https://mui.com/material-ui/api/timeline-dot/) or [`Icon`](https://mui.com/material-ui/icons/#icon-font-icons). |
    | **variant**        | str  | filled  | Variant prop of [`TimelineDot`](https://mui.com/material-ui/api/timeline-dot/) (filled/outlined).                 |
    | **icon**           | str  | *None*  | *snake_case* name of [`Icon`](https://mui.com/material-ui/icons/#icon-font-icons).                                |
    | **disable_dot**    | bool | *None*  | If `True`, the icon is shown standalone and not inside the [`TimelineDot`](https://mui.com/material-ui/api/timeline-dot/). |

#### Styling

* **`sx`** (dict): Component‑level styling API.
* **`theme_config`** (dict): Theming API.

___

## Basic timeline

A basic timeline showing a list of events.

```python
pmu.Timeline(object=[
    {"content": "Eat"},
    {"content": "Code"},
    {"content": "Sleep"},
], width=300).servable()
```

## Left‑positioned timeline

The main content of the timeline can be positioned on the left side relative to the time axis.

```python
pmu.Timeline(object=[
    {"content": "Eat"},
    {"content": "Code"},
    {"content": "Sleep"},
], position="left", width=300).servable()
```

## Alternating timeline

The timeline can display the events on alternating sides.

```python
pmu.Timeline(object=[
    {"content": "Eat"},
    {"content": "Code"},
    {"content": "Sleep"},
], position="alternate", width=300).servable()
```

## Reverse alternating timeline

The timeline can display the events on alternating sides in reverse order.

```python
pmu.Timeline(object=[
    {"content": "Eat"},
    {"content": "Code"},
    {"content": "Sleep"},
], position="alternate-reverse", width=300).servable()
```

## Color

The `TimelineDot` can appear in different colors from the theme palette.

```python
pmu.Timeline(object=[
    {"content": "Secondary", "color": "secondary"},
    {"content": "Success", "color": "success"},
], width=300).servable()
```

## Outlined

```python
pmu.Timeline(object=[
    {"content": "Eat", "variant": "outlined"},
    {"content": "Code", "variant": "outlined", "color": "primary"},
    {"content": "Sleep", "variant": "outlined", "color": "secondary"},
    {"content": "Repeat", "variant": "outlined"},
], width=300).servable()
```

## Opposite content

The timeline can display content on opposite sides.

```python
pmu.Timeline(object=[
    {"content": "Eat", "opposite": "09:30 am"},
    {"content": "Code", "opposite": "10:00 am"},
    {"content": "Sleep", "opposite": "12:00 am"},
    {"content": "Repeat", "opposite": "09:00 pm"},
], position="alternate", width=300).servable()
```

## Customization with icons and titles

```python
pmu.Timeline(object=[
    {"content_title": "Eat", "content": "Because you need strength", "opposite": "08:30", "color": "grey",   "variant": "filled", "icon": "fastfood"},
    {"content_title": "Code", "content": "Because it's awesome!", "opposite": "09:00", "color": "primary", "variant": "filled", "icon": "laptop_mac"},
    {"content_title": "Sleep", "content": "Because you need rest", "opposite": "09:30", "color": "secondary",   "variant": "outlined", "icon": "hotel"},
    {"content_title": "Repeat", "content": "Because this is the life you love!", "opposite": "11:00", "color": "success",      "variant": "filled", "icon": "repeat"},
], position="alternate", sizing_mode="stretch_width").servable()
```

## Customization with no dot and left alignment

We can disable the dot using `disable_dot` and align the `Timeline` left using `sx` styling.

```python
config = [
    {"content_title": "$2400, Design changes", "content": "22 DEC 7:20 PM", "color": "success", "icon": "notifications", "disable_dot": True},
    {"content_title": "New order #1832412", "content": "21 DEC 11 PM", "color": "error", "icon": "code", "disable_dot": True},
    {"content_title": "Server payments for April", "content": "21 DEC 9:34 PM", "color": "primary", "icon": "shopping_cart", "disable_dot": True},
    {"content_title": "New card added for order #4395133", "content": "20 DEC 2:20 AM", "color": "warning", "icon": "credit_card", "disable_dot": True},
    {"content_title": "Unlock packages for development", "content": "18 DEC 4:54 AM", "color": "error", "icon": "key", "disable_dot": True},
    {"content_title": "New order #9583120", "content": "17 DEC", "color": "dark", "icon": "payments", "disable_dot": True},
]
sx = {
    "& .MuiTimelineItem-root:before": {
        "flex": 0,
        "padding-left": 10,
    },
}
pmu.Timeline(object=config, sx=sx, sizing_mode="stretch_width").servable()
```

## DataFrame timeline

You can convert your `DataFrame` to a timeline `object` with `.to_dict(orient="records")`.

```python
import pandas as pd

df = pd.DataFrame(config)
pmu.Timeline(
    object=df.iloc[0:2].to_dict(orient="records"),
    sx=sx, sizing_mode="stretch_width"
).servable()
```
