import Alert from "@mui/material/Alert"
import Icon from "@mui/material/Icon"
import {SnackbarProvider, useSnackbar} from "notistack"
import {useTheme} from "@mui/material/styles"

function NotificationArea({model, view}) {
  const {enqueueSnackbar, closeSnackbar} = useSnackbar()
  const [position] = model.useState("position")
  const theme = useTheme()

  const enqueueNotification = (notification) => {
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
        model.notifications = model.notifications.filter(n => n._uuid !== notification._uuid)
        model.send_msg({
          type: "destroy",
          uuid: notification._uuid,
        })
      },
      persist: notification.duration === 0,
      preventDuplicate: true,
      style: {
        margin: "1em",
      },
      variant: notification.notification_type,
    })
  }

  React.useEffect(() => {
    for (const notification of model.notifications) {
      enqueueNotification(notification)
    }
    model.on("msg:custom", (msg) => {
      if (msg.type === "destroy") {
        closeSnackbar(msg.uuid)
      } else if (msg.type === "enqueue") {
        enqueueNotification(msg.notification)
      }
    })
  }, [])
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
