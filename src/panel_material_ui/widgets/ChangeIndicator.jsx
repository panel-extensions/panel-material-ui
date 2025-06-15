import {Card, CardContent, Typography, Box, Icon, Divider} from "@mui/material";

/**
 * A reusable change indicator card displaying a metric, its change, and an icon.
 *
 * Props:
 * - title: Label for the metric
 * - icon: Name of the Material Icon to display
 * - value: Current value of the metric
 * - changePercent: Percentage change (positive or negative)
 * - since: Text describing the period, e.g. "Since last week"
 */
const ChangeIndicator = ({title, icon, value, changePercent, since}) => {
  const isPositive = changePercent > 0;
  const changeColor = isPositive ? "success.main" : "error.main";
  const changeSymbol = isPositive ? "+" : "";

  return (
    <Card
      sx={{
        position: "relative",
        borderRadius: 2,
        boxShadow: 2,
        padding: 2,
        width: "100%",
        overflow: "visible",
      }}
    >
      <Box
        sx={{
          position: "absolute",
          top: 16,
          right: 16,
          bgcolor: "grey.800",
          color: "common.white",
          borderRadius: 1,
          padding: 1,
          boxShadow: 3,
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Icon fontSize="small">{icon}</Icon>
      </Box>

      <CardContent sx={{"&:last-child": {padding: "0px"}}}>
        <Typography variant="subtitle2" color="text.secondary" gutterBottom>
          {title}
        </Typography>

        <Typography variant="h4" component="div" gutterBottom sx={{color: "text.primary", fontWeight: "bold"}}>
          {value}
        </Typography>
        <Divider sx={{"margin-bottom": "10px"}}/>
        <Typography variant="caption" color="text.secondary">
          <Box component="span" sx={{color: changeColor, fontWeight: "bold"}}>
            {`${changeSymbol}${changePercent}%`}
          </Box>
          &nbsp;{since}
        </Typography>
      </CardContent>
    </Card>
  );
};

export function render({model}) {
  const [title]=model.useState("title")
  const [icon]=model.useState("icon")
  const [value]=model.useState("value")
  const [change_percent]=model.useState("change_percent")
  const [since]=model.useState("since")
  return <ChangeIndicator title={title} icon={icon} value={value} changePercent={change_percent} since={since} />
}
