_WEBSITE_VIEWS_DATA = {
    "xAxis": {"data": ["M", "T", "W", "T", "F", "S", "S"]},
    "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
    "yAxis": {},
    "series": [
        {
            "name": "Views",
            "type": "bar",
            "data": [50, 45, 30, 35, 50, 60, 75],
            "itemStyle": {"color": "green"},
        }
    ],
    "grid": {
        "top": 10,
        "bottom": 20,
    },
}

_DAILY_SALES = {
    "xAxis": {
        "type": "category",
        "data": ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"],
    },
    "yAxis": {"type": "value"},
    "series": [
        {
            "name": "Monthly Data",
            "type": "line",
            "data": [120, 132, 101, 134, 90, 230, 210, 180, 150, 200, 170, 250],
            "itemStyle": {"color": "green"},
        }
    ],
    "grid": {
        "top": 10,
        "bottom": 20,
    },
    "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
}
_COMPLETED_TASKS = {
    "xAxis": {
        "type": "category",
        "data": ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    },
    "yAxis": {"type": "value"},
    "series": [
        {
            "name": "Monthly Data",
            "type": "line",
            "data": [50, 50, 300, 210, 500, 230, 400, 230, 525],
            "itemStyle": {"color": "green"},
        }
    ],
    "grid": {
        "top": 10,
        "bottom": 20,
    },
    "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
}


def get_website_views_config():
    return _WEBSITE_VIEWS_DATA


def get_daily_sales_config():
    return _DAILY_SALES


def get_completed_tasks_config():
    return _COMPLETED_TASKS
