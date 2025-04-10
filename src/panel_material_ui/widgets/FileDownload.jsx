import Button from "@mui/material/Button"
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

export function render({model, view}) {
  const [auto] = model.useState("auto")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [embed] = model.useState("embed")
  const [filename] = model.useState("filename")
  const [file_data] = model.useState("data")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [label] = model.useState("label")
  const [sx] = model.useState("sx")
  const [variant] = model.useState("variant")

  const linkRef = React.useRef(null)
  const theme = useTheme()

  const downloadFile = () => {
    const link = document.createElement("a")
    link.download = filename
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
    if (embed || (file_data != null && auto)) {
      downloadFile()
    } else {
      model.send_event("click", {})
    }
  }

  React.useEffect(() => {
    model.on("change:data", () => {
      if (model.data != null && auto) {
        downloadFile()
      } else if (linkRef.current) {
        const blob = dataURItoBlob(model.data)
        linkRef.current.href = URL.createObjectURL(blob)
      }
    })
  }, [])

  return (
    <Button
      color={color}
      disabled={disabled}
      fullWidth
      startIcon={icon ? (
        icon.trim().startsWith("<") ?
          <img src={`data:image/svg+xml;base64,${btoa(icon)}`} width={icon_size} height={icon_size} style={{paddingRight: "0.5em"}} /> :
          <Icon style={{fontSize: icon_size}}>{icon}</Icon>
      ): <FileDownloadIcon style={{fontSize: icon_size}}/>}
      onClick={handleClick}
      sx={sx}
      variant={variant}
    >
      {auto ? label : <a ref={linkRef} href={file_data} download={filename} style={{color: theme.palette[color].contrastText}}>{label}</a>}
    </Button>
  )
}
