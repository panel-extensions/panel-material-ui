import Button from "@mui/material/Button"
import {styled} from "@mui/material/styles"
import CircularProgress from "@mui/material/CircularProgress"
import CloudUploadIcon from "@mui/icons-material/CloudUpload"
import ErrorIcon from "@mui/icons-material/Error"
import TaskAltIcon from "@mui/icons-material/TaskAlt"
import {useTheme} from "@mui/material/styles"
import {isFileAccepted, processFilesChunked} from "./utils"

const VisuallyHiddenInput = styled("input")({
  clip: "rect(0 0 0 0)",
  clipPath: "inset(50%)",
  height: 1,
  overflow: "hidden",
  position: "absolute",
  bottom: 0,
  left: 0,
  whiteSpace: "nowrap",
  width: 1,
})

export function render(props, ref) {
  const {data, el, model, view, ...other} = props
  const [accept] = model.useState("accept")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [directory] = model.useState("directory")
  const [end_icon] = model.useState("end_icon")
  const [icon] = model.useState("icon")
  const [icon_size] = model.useState("icon_size")
  const [loading] = model.useState("loading")
  const [multiple] = model.useState("multiple")
  const [label] = model.useState("label")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")

  // Store filenames locally since Panel's filename parameter has sync issues
  const [uploadedFiles, setUploadedFiles] = React.useState([])
  const [status, setStatus] = React.useState("idle")
  const [errorMessage, setErrorMessage] = React.useState("")
  const [isDragOver, setIsDragOver] = React.useState(false)
  const fileInputRef = React.useRef(null)
  const theme = useTheme()

  const N = uploadedFiles.length

  if (Object.entries(ref).length === 0 && ref.constructor === Object) {
    ref = undefined
  }

  const clearInputOnly = () => {
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  const clearFiles = () => {
    clearInputOnly()
    setUploadedFiles([])
  }

  const processFiles = async (files) => {
    try {
      setStatus("uploading")
      setErrorMessage("")

      let validFiles = files
      if (accept) {
        validFiles = Array.from(files).filter(file => isFileAccepted(file, accept))
        // Show error for invalid file type(s)
        if (!validFiles.length) {
          const invalid = Array.from(files).filter(file => !isFileAccepted(file, accept)).map(file => file.name).join(", ")
          setErrorMessage(`The file(s) ${invalid} have invalid file types. Accepted types: ${accept}`)
          setStatus("error")
          setTimeout(() => {
            setStatus("idle")
          }, 5000)
          return
        }
      }

      // Use chunked upload with frontend validation
      const count = await processFilesChunked(
        validFiles,
        model,
        model.max_file_size,
        model.max_total_file_size,
        model.chunk_size || 10 * 1024 * 1024
      )

      // Store filenames locally for persistent display
      const fileNames = Array.from(validFiles).map(file => file.name)
      setUploadedFiles(fileNames)
    } catch (error) {
      console.error("Upload error:", error)
      setErrorMessage(error.message)
      setStatus("error")
      setTimeout(() => {
        setStatus("idle")
      }, 5000)
    }
  }

  const handleDragEnter = (e) => {
    e.preventDefault()
    e.stopPropagation()

    // During dragenter/dragover, we can't reliably check file types
    // So we'll show the drag state and validate on drop
    if (e.dataTransfer.types && e.dataTransfer.types.includes("Files")) {
      setIsDragOver(true)
    }
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragOver(false)
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    e.stopPropagation()

    // Set drag effect to indicate files can be dropped
    if (e.dataTransfer.types && e.dataTransfer.types.includes("Files")) {
      e.dataTransfer.dropEffect = "copy"
    } else {
      e.dataTransfer.dropEffect = "none"
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragOver(false)

    if (disabled) { return }

    const files = e.dataTransfer.files
    if (files && files.length > 0) {
      processFiles(files)
    }
  }

  model.on("msg:custom", (msg) => {
    if (msg.status === "finished") {
      setStatus("completed")
      setTimeout(() => {
        setStatus("idle")
        clearInputOnly() // Clear only the input after successful upload to enable reupload
      }, 2000)
    } else if (msg.status === "error") {
      setErrorMessage(msg.error)
      setStatus("error")
    }
  })

  const dynamic_icon = (() => {
    switch (status) {
      case "error":
        return (
          <Tooltip title={errorMessage} arrow>
            <ErrorIcon color="error" />
          </Tooltip>
        );
      case "idle":
        return <CloudUploadIcon />;
      case "uploading":
        return <CircularProgress color={theme.palette[color].contrastText} size={15} />;
      case "completed":
        return <TaskAltIcon />;
      default:
        return null;
    }
  })();

  let title = ""
  let tooltipTitle = ""

  if (N > 0) {
    // Show filename(s) when file is uploaded
    const verb = status === "uploading" ? "Uploading" : "Uploaded"
    if (N === 1) {
      title = `${verb} ${uploadedFiles[0]}`
      tooltipTitle = uploadedFiles[0]
    } else {
      title = `${verb} ${N} files`
      tooltipTitle = uploadedFiles
    }
  } else if (label) {
    title = label
  } else {
    title = `Upload File${multiple ? "(s)" : ""}`
  }

  const buttonElement = (
    <Button
      color={color}
      component="label"
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
      loadingPosition="start"
      ref={ref}
      role={undefined}
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
      ) : dynamic_icon}
      sx={{
        ...sx,
        ...(isDragOver && {
          borderStyle: "dashed",
          transform: "scale(1.02)",
          transition: "all 0.2s ease-in-out"
        })
      }}
      tabIndex={-1}
      variant={variant}
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
      {...other}
    >
      {title}
      <VisuallyHiddenInput
        ref={(ref) => {
          fileInputRef.current = ref
          if (ref) {
            ref.webkitdirectory = directory
          }
        }}
        type="file"
        onChange={(event) => {
          processFiles(event.target.files)
        }}
        accept={accept}
        multiple={multiple}
      />
    </Button>
  );

  // Wrap in tooltip if we have filenames to show
  if (tooltipTitle && uploadedFiles && N > 0) {
    const tooltipContent = Array.isArray(tooltipTitle) ? (
      <div>
        {tooltipTitle.map((filename, index) => (
          <div key={index}>{filename}</div>
        ))}
      </div>
    ) : tooltipTitle;

    return (
      <Tooltip
        title={tooltipContent}
        arrow
        placement="top"
      >
        {buttonElement}
      </Tooltip>
    );
  }

  return buttonElement;
}
