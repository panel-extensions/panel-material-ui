import Button from "@mui/material/Button"
import {styled} from "@mui/material/styles"
import CircularProgress from "@mui/material/CircularProgress"
import CloudUploadIcon from "@mui/icons-material/CloudUpload"
import ErrorIcon from "@mui/icons-material/Error"
import TaskAltIcon from "@mui/icons-material/TaskAlt"
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

// Size parsing function matching FileDropper
function parseSizeString(sizeStr) {
  if (!sizeStr) { return null }
  const match = sizeStr.match(/^(\d+(?:\.\d+)?)\s*(KB|MB|GB)$/i);
  if (!match) { return null }

  const value = parseFloat(match[1])
  const unit = match[2].toUpperCase()

  switch (unit) {
    case "KB": return value * 1024
    case "MB": return value * 1024 * 1024
    case "GB": return value * 1024 * 1024 * 1024
    default: return null
  }
}

// File size validation function
function validateFileSize(file, maxFileSize, maxTotalFileSize, existingFiles = []) {
  const errors = [];

  if (maxFileSize) {
    const maxFileSizeBytes = typeof maxFileSize === "string" ? parseSizeString(maxFileSize) : maxFileSize
    if (maxFileSizeBytes && file.size > maxFileSizeBytes) {
      errors.push(`File "${file.name}" (${formatBytes(file.size)}) exceeds maximum file size of ${formatBytes(maxFileSizeBytes)}`);
    }
  }

  if (maxTotalFileSize) {
    const maxTotalSizeBytes = typeof maxTotalFileSize === "string" ? parseSizeString(maxTotalFileSize) : maxTotalFileSize
    if (maxTotalSizeBytes) {
      const existingSize = existingFiles.reduce((sum, f) => sum + f.size, 0)
      const totalSize = existingSize + file.size
      if (totalSize > maxTotalSizeBytes) {
        errors.push(`Adding "${file.name}" would exceed maximum total size of ${formatBytes(maxTotalSizeBytes)}`)
      }
    }
  }

  return errors;
}

// Format bytes for display
function formatBytes(bytes) {
  if (bytes === 0) { return "0 B" }
  const k = 1024
  const sizes = ["B", "KB", "MB", "GB"]
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return `${parseFloat((bytes / k**i).toFixed(2))} ${sizes[i]}`
}

// Chunked upload function using FileDropper's protocol
async function uploadFileChunked(file, model, chunkSize = 10 * 1024 * 1024) {
  const totalChunks = Math.ceil(file.size / chunkSize);

  for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
    const start = chunkIndex * chunkSize;
    const end = Math.min(start + chunkSize, file.size)
    const chunk = file.slice(start, end)

    // Read chunk as ArrayBuffer
    const arrayBuffer = await new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onload = () => resolve(reader.result)
      reader.onerror = reject
      reader.readAsArrayBuffer(chunk)
    });

    // Send chunk using FileDropper's protocol
    model.send_msg({
      status: "upload_event",
      chunk: chunkIndex + 1, // 1-indexed
      data: arrayBuffer,
      name: file.name,
      total_chunks: totalChunks,
      type: file.type
    })
  }
}

// New chunked file processing function
async function processFilesChunked(files, model, maxFileSize, maxTotalFileSize, chunkSize = 10 * 1024 * 1024) {
  try {
    const fileArray = Array.from(files);

    // Validate file sizes on frontend
    for (const file of fileArray) {
      const sizeErrors = validateFileSize(file, model.max_file_size, model.max_total_file_size, fileArray);
      if (sizeErrors.length > 0) {
        throw new Error(sizeErrors.join("; "))
      }
    }

    model.send_msg({status: "initializing"})

    // Upload all files using chunked protocol
    for (const file of fileArray) {
      await uploadFileChunked(file, model, chunkSize)
    }

    model.send_msg({status: "finished"})
    return fileArray.length
  } catch (error) {
    model.send_msg({status: "error", error: error.message})
    throw error
  }
}

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
  const acceptedTypes = accept.split(",").map(type => type.trim())
  const fileName = file.name
  const fileType = file.type

  return acceptedTypes.some(acceptedType => {
    // Handle file extensions (e.g., ".jpg", ".png")
    if (acceptedType.startsWith(".")) {
      return fileName.toLowerCase().endsWith(acceptedType.toLowerCase())
    }

    // Handle MIME types (e.g., "image/*", "image/jpeg")
    if (acceptedType.includes("/")) {
      if (acceptedType.endsWith("/*")) {
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

export function render({model})  {
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

      setN(count)
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
      processFiles(validFiles)
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
        return <TaskAltIcon />;
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
