import Alert from "@mui/material/Alert"
import Icon from "@mui/material/Icon"
import {SnackbarProvider, useSnackbar} from "notistack"
import {useTheme} from "@mui/material/styles"

function standardize_color(str) {
  const ctx = document.createElement("canvas").getContext("2d")
  ctx.fillStyle = str
  return ctx.fillStyle
}

function NotificationArea({model, view}) {
  const {enqueueSnackbar, closeSnackbar} = useSnackbar()
  const [position] = model.useState("position")
  const theme = useTheme()

  const enqueueNotification = (notification, uuid = null) => {
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

    const color = background ? (
      theme.palette.augmentColor({
        color: {
          main: (background.startsWith("#") || background.includes("(")) ? background : standardize_color(background),
        }
      })) : undefined;

    const [vertical, horizontal] = position.split("-")
    enqueueSnackbar(notification.message, {
      anchorOrigin: {vertical, horizontal},
      autoHideDuration: notification.duration,
      content: (
        <Alert
          icon={icon ? <Icon>{icon}</Icon> : undefined}
          onClose={() => notification._uuid && closeSnackbar(notification._uuid)}
          severity={notification.notification_type}
          id={uuid ?? notification._uuid}
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
      key: uuid ?? notification._uuid,
      onEnter: notification.onEnter,
      onClose: () => {
        if (notification._uuid == null) {
          return
        }
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

  const timeout_ref = React.useRef(null)
  const clear_timeout = () => {
    if (timeout_ref.current != null) {
      clearTimeout(timeout_ref.current)
      timeout_ref.current = null
    }
  }

  const register_reconnect = () => {
    const reconnect_id = `reconnect-notification-${view.model.id}`
    if (window.session_reconnect) {
      const config = {
        message: "Connection with server was re-established.",
        duration: 5000,
        notification_type: "success"
      }
      enqueueNotification(config)
      window.session_reconnect = false
    }
    view.model.document.on_event("client_reconnected", (_, _event) => {
      clear_timeout()
      closeSnackbar(reconnect_id)
      window.session_reconnect = true
    })
    const update_reconnect = (msg, event) => {
      const reconnect_msg = document.getElementById(reconnect_id)?.children[1]
      reconnect_msg.innerHTML = `<div>${msg} <span class="reconnect-button"><b>Click here</b></span> to attempt manual re-connect.<div>`
      const reconnectSpan = reconnect_msg.querySelector(".reconnect-button")
      if (reconnectSpan) {
        reconnectSpan.addEventListener("click", () => { clear_timeout(); event.reconnect() })
      }
    }
    view.model.document.on_event("connection_lost", (_, event) => {
      clear_timeout()
      const {timeout} = event
      const msg = model.js_events.connection_lost.message
      const reconnect_msg = document.getElementById(reconnect_id)?.children[1]
      if (timeout != null || reconnect_msg == null) {
        let current_timeout = timeout
        const config = {
          message: msg,
          duration: 0,
          notification_type: model.data.js_events.connection_lost.type
        }
        if (timeout == null && view.model.tags[0] === "prompt") {
          config.onEnter = () => update_reconnect(msg, event)
        }
        if (reconnect_msg == null) {
          enqueueNotification(config, reconnect_id)
        }
        const set_timeout = () => {
          const reconnect_msg = document.getElementById(reconnect_id)?.children[1]
          if (reconnect_msg == null) {
            return
          }
          const timeout = Math.max(0, Math.round(current_timeout / 1000))
          let message = msg
          if (timeout == 0) {
            message = `${msg} Reconnecting now.`
            clear_timeout()
          } else {
            message = `${msg} Attempting to reconnect in ${timeout} seconds…`
          }
          reconnect_msg.textContent = message
        }
        if (timeout != null) {
          set_timeout()
          timeout_ref.current = setInterval(() => { current_timeout -= 1000; set_timeout() }, 1000)
        }
      }
      if (timeout == null && reconnect_msg) {
        update_reconnect(msg, event)
      }
    })
  }

  React.useEffect(() => {
    register_reconnect(view.model)
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
