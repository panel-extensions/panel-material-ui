import Button from "@mui/material/Button"
import {styled} from "@mui/material/styles";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";

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
});

async function read_file(file) {
  return new Promise<string>((resolve, reject) => {
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

async function load_files(files, accept, directory, multiple) {
  const values = []
  const filenames = []
  const mime_types = []

  for (const file of files) {
    const data_url = await read_file(file)
    const [, mime_type="",, value=""] = data_url.split(/[:;,]/, 4)

    if (directory) {
      const ext = file.name.split(".").pop()
      if ((accept.length > 0 && isString(ext)) ? accept.includes(`.${ext}`) : true) {
        filenames.push(file.webkitRelativePath)
        values.push(value)
        mime_types.push(mime_type)
      }
    } else {
      filenames.push(file.name)
      values.push(value)
      mime_types.push(mime_type)
    }
  }
  return [values, filenames, mime_types]
}

export function render({model}) {
  const [accept] = model.useState("accept")
  const [color] = model.useState("button_type")
  const [disabled] = model.useState("disabled")
  const [directory] = model.useState("directory")
  const [multiple] = model.useState("multiple")
  const [label] = model.useState("label")
  const [variant] = model.useState("button_style")

  return (
    <Button
      color={color}
      component="label"
      role={undefined}
      tabIndex={-1}
      startIcon={<CloudUploadIcon />}
      variant={variant}
    >
      Upload files
      <VisuallyHiddenInput
        type="file"
        onChange={(event) => {
          load_files(event.target.files, accept, directory, multiple).then((data) => {
            const [values, filenames, mime_types] = data
            model.send_msg({status: "initializing"})
            for (let i = 0; i < values.length; i++) {
              model.send_msg({data: values[i], mime_type: mime_types[i], filename: filenames[i], part: i, status: "in_progress"})
            }
            model.send_msg({status: "finished"})
          }).catch((e) => console.error(e))
        }}
        accept={accept}
        multiple={multiple}
      />
    </Button>
  );
}
