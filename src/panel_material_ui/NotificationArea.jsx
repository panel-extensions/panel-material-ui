import Alert from "@mui/material/Alert";
import Icon from "@mui/material/Icon";
import {SnackbarProvider, useSnackbar} from "notistack";

function NotificationArea({model, view}) {
  const {enqueueSnackbar, closeSnackbar} = useSnackbar();
  const [notifications, setNotifications] = model.useState("notifications");
  const [position] = model.useState("position");
  const enqueuedNotifications = React.useRef(new Set());
  const deletedNotifications = React.useRef(new Set());

  React.useEffect(() => {
    notifications.forEach((notification) => {
      if (deletedNotifications.current.has(notification._uuid)) {
        setNotifications(notifications.filter(n => n._uuid !== notification._uuid))
      } else if (!enqueuedNotifications.current.has(notification._uuid)) {
        enqueuedNotifications.current.add(notification._uuid);
        const [vertical, horizontal] = position.split("-")

        const key = enqueueSnackbar(notification.message, {
          anchorOrigin: {vertical, horizontal},
          autoHideDuration: notification.duration,
          container: view.container,
          content: (
            <Alert
              icon={notification.icon ? <Icon>{notification.icon}</Icon> : undefined}
              onClose={() => closeSnackbar(key)}
              severity={notification.notification_type}
              sx={notification.background ? (
                {backgroundColor: notification.background, margin: "0.5em 1em"}
              ) : {margin: "0.5em 1em"}}
            >
              {notification.message}
            </Alert>
          ),
          key: notification._uuid,
          onClose: () => {
            deletedNotifications.current.add(notification._uuid)
            setNotifications(notifications.filter(n => n._uuid !== notification._uuid))
            enqueuedNotifications.current.delete(notification._uuid);
          },
          persist: notification.duration === 0,
          preventDuplicate: true,
          style: {
            margin: "1em",
          },
          variant: notification.notification_type,
        });
      }
    });
  }, [notifications]);
}

export function render({model, view}) {
  const [maxSnack] = model.useState("max_notifications");
  return (
    <SnackbarProvider maxSnack={maxSnack}>
      <NotificationArea
        model={model}
        view={view}
      />
    </SnackbarProvider>
  )
}
