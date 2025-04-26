import panel as pn
from shared.page import create_page
from panel_material_ui import Button, Alert
pn.extension(notifications=True)

with pn.config.set(sizing_mode="stretch_width"):
    alert_card = pn.Column(
        """## Alerts

Notifications on this page use the `Alert` from Material UI. Read more details [here](https://mui.com/material-ui/react-alert/).
""",
        *[Alert(title=f"A simple {severity} alert with an example link. Give it a click if you like.", severity=severity, variant="filled", closeable=True, margin=10) for severity in Alert.param.severity.objects],
        max_width=1200,
    )

    success_notification = pn.widgets.Button(name="Success")
    notifications_row = pn.Column(
        """## Notifications

Notifications on this page use the `SnackbarProvider` from notistack. Read more details [here](https://notistack.com/getting-started).""",
        pn.Row(
            Button(name="Error", color="error", sizing_mode="fixed", width=100, on_click=lambda e: pn.state.notifications.error('This is an error notification.', duration=1000)),
            Button(name="Info", color="info", sizing_mode="fixed", width=100, on_click=lambda e: pn.state.notifications.info('This is an info notification.', duration=1000)),
            Button(name="Success", color="success", sizing_mode="fixed", width=100, on_click=lambda e: pn.state.notifications.success('This is a success notification.', duration=1000)),
            Button(name="Warning", color="warning", sizing_mode="fixed", width=100, on_click=lambda e: pn.state.notifications.warning('This is a warning notification.', duration=1000)),
        )
    )

create_page("Notifications", main=[alert_card, notifications_row]).servable(title="Notifications").servable()
