import panel as pn
import panel_material_ui as pmu
from .config import PAGES

_CHANGE_INDICATOR_CSS = """
.card {
    font-family: 'Roboto', sans-serif;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 16px;
    width: 100%;
    margin: 0xp;
    display: inline-block;
}

.card-icon {
    position: absolute;
    top: 16px;
    right: 16px;
    color: white;
    background-image: linear-gradient(195deg,#42424a,#191919);
    padding: 10px;
    margin: 3px;
    font-size: 16px;
    box-shadow: 0 4px 20px 0 rgba(0,0,0,.14),0 7px 10px -5px rgba(64,64,64,.4)!important;
    border-radius: .5rem;
}

.card-title {
    font-size: 14px;
    color: #888;
    margin-bottom: 8px;
}

.card-value {
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 8px;
    color: #344767;
}

.card-footer {
    font-size: 12px;
    color: #888;
}

.change-positive {
    color: #4caf50;
    font-weight: bold;
}

.change-negative {
    color: #f44336;
    font-weight: bold;
}
"""
_CHANGE_INDICATOR_TEMPLATE = """\
<div class="card">
    <span class='material-symbols-outlined card-icon'>{icon}</span>
    <div class="card-title">{title}</div>
    <div class="card-value">{value}</div>
    <div class="card-footer">
        <span class="{change_class}">
            {change_percent_str}
        </span>
        &nbsp;{since}
    </div>
</div>\
"""


def create_change_indicator(title, icon, value, change_percent, since):
    if change_percent > 0:
        change_class = "change-positive"
        change_percent_str = f"+{change_percent}%"
    else:
        change_class = "change-negative"
        change_percent_str = f"{change_percent}%"

    html = _CHANGE_INDICATOR_TEMPLATE.format(
        title=title,
        icon=icon,
        value=value,
        change_percent_str=change_percent_str,
        since=since,
        change_class=change_class,
    )
    # Why pn.pane.HTML not visible?
    return pn.panel(
        html,
        stylesheets=[_CHANGE_INDICATOR_CSS],
        sizing_mode="stretch_width",
    )


def create_menu(selected: str, pages: list[tuple] = PAGES):
    items = pn.Column()
    for name_, href, icon in pages:
        button_style = "contained" if selected == name_ else "text"
        button_type = "primary" if selected == name_ else "default"
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
