import Button from "@mui/material/Button"
import CircularProgress from "@mui/material/CircularProgress"
import FileDownloadIcon from "@mui/icons-material/FileDownload"
import {useTheme} from "@mui/material/styles"

function dataURItoBlob(dataURI) {
  const byteString = atob(dataURI.split(",")[1])
  const mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0]
  const ab = new ArrayBuffer(byteString.length)
  const ia = new Uint8Array(ab)
  for (let i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i)
  }
  const bb = new Blob([ab], {type: mimeString})
  return bb
}

export function render(props, ref) {
  const {data, el, model, view, ...other} = props
  const [auto] = model.useState("auto")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [disableElevation] = model.useState("disable_elevation")
  const [embed] = model.useState("embed")
  const [end_icon] = model.useState("end_icon")
  const [filename] = model.useState("filename")
  const [file_data] = model.useState("data")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [label] = model.useState("label")
  const [loading] = model.useState("loading")
  const [size] = model.useState("size")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")
  const [_syncing] = model.useState("_syncing")

  const theme = useTheme()

  if (Object.entries(ref).length === 0 && ref.constructor === Object) {
    ref = undefined
  }

  const downloadFile = () => {
    const link = document.createElement("a")
    link.download = model.filename
    const blob = dataURItoBlob(model.data)
    link.href = URL.createObjectURL(blob)
    view.container.appendChild(link)
    link.click()
    setTimeout(() => {
      URL.revokeObjectURL(link.href)
      view.container.removeChild(link)
    }, 100)
  }

  const handleClick = () => {
    if (embed || (file_data != null && !auto)) {
      downloadFile()
    } else {
      model.send_event("click", {})
    }
  }

  React.useEffect(() => {
    model.on("change:data", () => {
      if (model.data != null && auto) {
        downloadFile()
      }
    })
  }, [])

  return (
    <Button
      color={color}
      disabled={disabled}
      endIcon={end_icon && (
        end_icon.trim().startsWith("<") ?
          <span style={{
            maskImage: `url("data:image/svg+xml;base64,${btoa(end_icon)}")`,
            backgroundColor: "currentColor",
            maskRepeat: "no-repeat",
            maskSize: "contain",
            width: icon_size,
            height: icon_size,
            display: "inline-block"}}
          /> :
          <Icon style={{fontSize: icon_size}}>{end_icon}</Icon>
      )}
      fullWidth
      loading={loading}
      ref={ref}
      startIcon={icon ? (
        icon.trim().startsWith("<") ?
          <span style={{
            maskImage: `url("data:image/svg+xml;base64,${btoa(icon)}")`,
            backgroundColor: "currentColor",
            maskRepeat: "no-repeat",
            maskSize: "contain",
            width: icon_size,
            height: icon_size,
            display: "inline-block"}}
          /> :
          <Icon style={{fontSize: icon_size}}>{icon}</Icon>
      ): auto || model.data != null ? <FileDownloadIcon style={{fontSize: icon_size}} />
        : _syncing ? <CircularProgress size={icon_size} sx={{color: "var(--variant-containedColor)"}} />
          : ""}
      onClick={handleClick}
      onContextMenu={(e) => e.stopPropagation()}
      size={size}
      sx={{
        cursor: _syncing ? "not-allowed" : "pointer",
        ...sx
      }}
      variant={variant}
      {...other}
    >
      {label}
    </Button>
  )
}
