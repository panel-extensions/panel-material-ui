import Accordion from "@mui/material/Accordion"
import AccordionSummary from "@mui/material/AccordionSummary"
import AccordionDetails from "@mui/material/AccordionDetails"
import ExpandMoreIcon from "@mui/icons-material/ExpandMore"

export function render({model}) {
  const objects = model.get_child("objects")
  const [active, setActive] = model.useState("active")
  const [names] = model.useState("_names")
  const [toggle] = model.useState("toggle")
  const [sx] = model.useState("sx")

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
  };

  return (
    <>
      { objects.map((obj, index) => {
        return (
          <Accordion
            defaultExpanded={active.includes(index)}
            expanded={active.includes(index)}
            key={`accordion-${index}`}
            sx={sx}
          >
            <AccordionSummary expandIcon={<ExpandMoreIcon />} onClick={handle_expand(index)}>{names[index]}</AccordionSummary>
            <AccordionDetails>{obj}</AccordionDetails>
          </Accordion>
        )
      }) }
    </>
  );
}
