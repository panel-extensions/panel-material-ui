import Button from "@mui/material/Button"
import {styled} from "@mui/material/styles"
import CloudUploadIcon from "@mui/icons-material/CloudUpload"
import ErrorIcon from "@mui/icons-material/Error"
import CheckCircleIcon from "@mui/icons-material/CheckCircle"
import CircularProgress from '@mui/material/CircularProgress';
import {useTheme} from "@mui/material/styles"

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

async function read_file(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => {
      const {result} = reader
      if (result != null) {
        resolve(result)
      } else {
        reject(reader.error ?? new Error(`unable to read '${file.name}'`))
      }
    }
    reader.readAsDataURL(file)
  })
}

function isFileAccepted(file, accept) {
  if (!accept || accept.length === 0) {
    return true
  }
  const acceptedTypes = accept.split(',').map(type => type.trim())
  const fileName = file.name
  const fileType = file.type

  return acceptedTypes.some(acceptedType => {
    // Handle file extensions (e.g., ".jpg", ".png")
    if (acceptedType.startsWith('.')) {
      return fileName.toLowerCase().endsWith(acceptedType.toLowerCase())
    }

    // Handle MIME types (e.g., "image/*", "image/jpeg")
    if (acceptedType.includes('/')) {
      if (acceptedType.endsWith('/*')) {
        // Handle wildcard MIME types (e.g., "image/*")
        const baseType = acceptedType.slice(0, -2)
        return fileType.startsWith(baseType)
      } else {
        // Handle exact MIME types (e.g., "image/jpeg")
        return fileType === acceptedType
      }
    }
    return false
  })
}

async function load_files(files, accept, directory, multiple) {
  const values = []
  const filenames = []
  const mime_types = []

  for (const file of files) {
    // Check if file is accepted based on accept prop
    if (!isFileAccepted(file, accept)) {
      continue
    }

    const data_url = await read_file(file)
    const [, mime_type="",, value=""] = data_url.split(/[:;,]/, 4)

    if (directory) {
      filenames.push(file.webkitRelativePath)
    } else {
      filenames.push(file.name)
    }
    values.push(value)
    mime_types.push(mime_type)
  }
  return [values, filenames, mime_types]
}

export function render({model}) {
  const [accept] = model.useState("accept")
  const [color] = model.useState("color")
  const [disabled] = model.useState("disabled")
  const [directory] = model.useState("directory")
  const [loading] = model.useState("loading")
  const [multiple] = model.useState("multiple")
  const [label] = model.useState("label")
  const [variant] = model.useState("variant")
  const [sx] = model.useState("sx")

  const [status, setStatus] = React.useState("idle")
  const [n, setN] = React.useState(0)
  const [errorMessage, setErrorMessage] = React.useState("")
  const [isDragOver, setIsDragOver] = React.useState(false)
  const fileInputRef = React.useRef(null)
  const theme = useTheme()

  const clearFiles = () => {
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  const processFiles = (files) => {
    load_files(files, accept, directory, multiple).then((data) => {
      const [values, filenames, mime_types] = data
      setStatus("uploading")
      model.send_msg({status: "initializing"})
      for (let i = 0; i < values.length; i++) {
        model.send_msg({
          value: values[i],
          mime_type: mime_types[i],
          filename: filenames[i],
          part: i,
          status: "in_progress",
        })
      }
      setN(values.length)
      model.send_msg({status: "finished"})
    }).catch((e) => console.error(e))
  }

  const handleDragEnter = (e) => {
    e.preventDefault()
    e.stopPropagation()

    // During dragenter/dragover, we can't reliably check file types
    // So we'll show the drag state and validate on drop
    if (e.dataTransfer.types && e.dataTransfer.types.includes('Files')) {
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
    if (e.dataTransfer.types && e.dataTransfer.types.includes('Files')) {
      e.dataTransfer.dropEffect = 'copy'
    } else {
      e.dataTransfer.dropEffect = 'none'
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragOver(false)

    if (disabled) return

    const files = e.dataTransfer.files
    if (files && files.length > 0) {
      // Filter valid files before processing
      const validFiles = Array.from(files).filter(file => isFileAccepted(file, accept))

      if (validFiles.length > 0) {
        processFiles(validFiles)
      } else if (accept) {
        // Show error for invalid file types
        setErrorMessage(`Invalid file type. Accepted types: ${accept}`)
        setStatus("error")
        setTimeout(() => {
          setStatus("idle")
        }, 5000)
      }
    }
  }

  model.on("msg:custom", (msg) => {
    if (msg.status === "finished") {
      setStatus("completed")
      setTimeout(() => {
        setStatus("idle")
        clearFiles() // Clear the input after successful upload to enable reupload
      }, 2000)
    } else if (msg.status === "error") {
      setErrorMessage(msg.error)
      setStatus("error")
    }
  })
  const icon = (() => {
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
        return <CheckCircleIcon color="success" />;
      default:
        return null;
    }
  })();

  let title = ""
  if (status === "completed") {
    title = `Uploaded ${n} file${n === 1 ? "" : "s"}.`
  } else if (label) {
    title = label
  } else {
    title = `Upload File${  multiple ? "(s)" : ""}`
  }

  return (
    <Button
      color={color}
      component="label"
      disabled={disabled}
      fullWidth
      loading={loading}
      loadingPosition="start"
      role={undefined}
      startIcon={icon}
      sx={{
        ...sx,
        ...(isDragOver && {
          borderStyle: 'dashed',
          transform: 'scale(1.02)',
          transition: 'all 0.2s ease-in-out'
        })
      }}
      tabIndex={-1}
      variant={variant}
      onDragEnter={handleDragEnter}
      onDragLeave={handleDragLeave}
      onDragOver={handleDragOver}
      onDrop={handleDrop}
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
}
