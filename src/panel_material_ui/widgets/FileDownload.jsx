import Button from "@mui/material/Button"
import FileDownloadIcon from "@mui/icons-material/FileDownload"
import SvgIcon from "@mui/material/SvgIcon"
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
  const [button_style] = model.useState("button_style")
  const [button_type] = model.useState("button_type")
  const [disabled] = model.useState("disabled")
  const [embed] = model.useState("embed")
  const [filename] = model.useState("filename")
  const [file_data] = model.useState("data")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [label] = model.useState("label")
  const [sx] = model.useState("sx")

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
      color={button_type}
      disabled={disabled}
      startIcon={icon ? (
        icon.startsWith("<") ? <SvgIcon>{icon}</SvgIcon> : <Icon style={{fontSize: icon_size}}>{icon}</Icon>
      ) : <FileDownloadIcon style={{fontSize: icon_size}}/>}
      onClick={handleClick}
      sx={sx}
      variant={button_style}
    >
      {auto ? label : <a ref={linkRef} href={file_data} download={filename} style={{color: theme.palette[button_type].contrastText}}>{label}</a>}
    </Button>
  )
}
