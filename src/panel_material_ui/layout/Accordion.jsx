import Accordion from "@mui/material/Accordion"
import AccordionSummary from "@mui/material/AccordionSummary"
import AccordionDetails from "@mui/material/AccordionDetails"
import ExpandMoreIcon from "@mui/icons-material/ExpandMore"
import Typography from "@mui/material/Typography"
import {render_html_icon_text} from "./utils"

export function render({model}) {
  const [active, setActive] = model.useState("active")
  const [active_header_background] = model.useState("active_header_background")
  const [active_header_color] = model.useState("active_header_color")
  const [disabled] = model.useState("disabled")
  const [disable_gutters] = model.useState("disable_gutters")
  const [elevation] = model.useState("elevation")
  const [header_background] = model.useState("header_background")
  const [header_color] = model.useState("header_color")
  const [names] = model.useState("_names")
  const [toggle] = model.useState("toggle")
  const [sx] = model.useState("sx")
  const [square] = model.useState("square")
  const [title_variant] = model.useState("title_variant")
  const [variant] = model.useState("variant")
  const headers = model.render_children("_headers")
  const objects = model.render_children("objects")
  const children = new Map(objects.map((object) => [object.props.id, object]))
  const object_models = model.children("objects")
  // A child listed more than once can only be mounted in one place, so it is
  // rendered in the first expanded section it belongs to.
  const placement = new Map()
  object_models.forEach((m, index) => {
    if (!placement.has(m.id) || (active.includes(index) && !active.includes(placement.get(m.id)))) {
      placement.set(m.id, index)
    }
  })

  const handle_expand = (index) => () => {
    let newActive
    if (active.includes(index)) {
      newActive = active.filter((v) => v != index)
    } else if (toggle) {
      newActive = [index]
    } else {
      newActive = [...active]
      newActive.push(index)
    }
    setActive(newActive)
  }

  return (
    <>
      { object_models.map((obj_model, index) => {
        const obj = placement.get(obj_model.id) === index ? children.get(obj_model.id) : null
        return (
          <Accordion
            defaultExpanded={active.includes(index)}
            disabled={disabled.includes(index)}
            disableGutters={disable_gutters}
            elevation={elevation}
            expanded={active.includes(index)}
            key={`accordion-${index}`}
            slotProps={{transition: {unmountOnExit: true}}}
            square={square}
            sx={sx}
            variant={variant}
          >
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              onClick={handle_expand(index)}
              sx={{
                backgroundColor: active.includes(index) ? active_header_background || header_background : header_background,
                color: active.includes(index) ? active_header_color || header_color : header_color,
                "& .MuiAccordionSummary-content.Mui-expanded": {mt: 1, mb: 1}
              }}
            >
              {names[index] ? (
                <Typography className="title" variant={title_variant} sx={{display: "inline-flex", alignItems: "center", gap: "0.25em"}}>
                  {render_html_icon_text(names[index])}
                </Typography>
              ) : headers[index]}
            </AccordionSummary>
            <AccordionDetails sx={{pb: 1, pl: 1, pr: 1}}>{obj}</AccordionDetails>
          </Accordion>
        )
      }) }
    </>
  );
}
