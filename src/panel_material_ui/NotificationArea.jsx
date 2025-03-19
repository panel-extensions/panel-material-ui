import Alert from "@mui/material/Alert"
import Icon from "@mui/material/Icon"
import {SnackbarProvider, useSnackbar} from "notistack"
import {useTheme} from "@mui/material/styles"

function NotificationArea({model, view}) {
  const {enqueueSnackbar, closeSnackbar} = useSnackbar()
  const [notifications, setNotifications] = model.useState("notifications")
  const [position] = model.useState("position")
  const enqueuedNotifications = React.useRef(new Set())
  const deletedNotifications = React.useRef(new Set())
  const theme = useTheme()

  React.useEffect(() => {
    // Delete notifications that are not in the notifications list
    Array.from(enqueuedNotifications.current.values()).filter(key => !notifications.find(n => n._uuid === key)).forEach(key => {
      closeSnackbar(key)
    })

    // Iterate over notifications and enqueue them
    notifications.forEach((notification) => {
      if (deletedNotifications.current.has(notification._uuid)) {
        setNotifications(notifications.filter(n => n._uuid !== notification._uuid))
      } else if (!enqueuedNotifications.current.has(notification._uuid)) {

        let background, icon, type
        if (model.types.find(t => t.type === notification.notification_type)) {
          type = model.types.find(t => t.type === notification.notification_type)
          background = notification.background || type.background
          icon = notification.icon || type.icon
        } else {
          type = notification.notification_type
          background = notification.background
          icon = notification.icon
        }

        const color = background ? (theme.palette.augmentColor({
          color: {
            main: background,
          }
        })) : undefined;

        enqueuedNotifications.current.add(notification._uuid)
        const [vertical, horizontal] = position.split("-")
        enqueueSnackbar(notification.message, {
          anchorOrigin: {vertical, horizontal},
          autoHideDuration: notification.duration,
          content: (
            <Alert
              icon={icon ? <Icon>{icon}</Icon> : undefined}
              onClose={() => closeSnackbar(notification._uuid)}
              severity={notification.notification_type}
              sx={background ? (
                {
                  backgroundColor: color.main,
                  margin: "0.5em 1em",
                  color: color.contrastText
                }
              ) : {margin: "0.5em 1em"}}
            >
              {notification.message}
            </Alert>
          ),
          key: notification._uuid,
          onClose: () => {
            deletedNotifications.current.add(notification._uuid)
            setNotifications(notifications.filter(n => n._uuid !== notification._uuid))
            enqueuedNotifications.current.delete(notification._uuid)
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
  const [maxSnack] = model.useState("max_notifications")

  return (
    <SnackbarProvider maxSnack={maxSnack}>
      <NotificationArea
        model={model}
        view={view}
      />
    </SnackbarProvider>
  )
}
