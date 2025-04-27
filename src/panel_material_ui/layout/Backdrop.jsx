import Backdrop from "@mui/material/Backdrop";
import {apply_flex} from "./utils"

export function render({model, view}) {
  const [open] = model.useState("open");
  const [sx] = model.useState("sx");
  const objects = model.get_child("objects");

  return (
    <Backdrop open={open} sx={{zIndex: (theme) => theme.zIndex.drawer + 1, ...sx}}>
      {objects.map((object, index) => {
        apply_flex(view.get_child_view(model.objects[index]), "column")
        return object
      })}
    </Backdrop>
  );
}
