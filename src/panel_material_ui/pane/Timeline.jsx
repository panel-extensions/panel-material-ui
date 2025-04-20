import {
    Timeline as MUITimeline,
    TimelineItem,
    TimelineSeparator,
    TimelineConnector,
    TimelineContent,
    TimelineOppositeContent,
    TimelineDot,
} from '@mui/lab';
import { Icon } from "@mui/material"
import Typography from '@mui/material/Typography';

export function render({ model }) {
    const [items] = model.useState('object')
    const [position] = model.useState('position')
    const [sx] = model.useState('sx')

    return (
    <MUITimeline position={position} sx={sx}>
    {items.map((item, idx) => (
        <TimelineItem key={idx}>
        {(item.opposite !== undefined | item.opposite_title) && (
            <TimelineOppositeContent sx={{ m: 'auto 0' }} align="right" variant="body2" color="text.secondary">
                <Typography variant="h6" component="span">
                    {item.opposite_title}
                </Typography>
                <Typography>
                    {item.opposite}
                </Typography>
            </TimelineOppositeContent>
        )}
        <TimelineSeparator>
            <TimelineDot
            color={item.color || 'grey'}
            variant={item.variant || 'filled'}
            >
                {item.icon !== undefined && <Icon sx={{"margin": "2px"}}>{item.icon}</Icon>}
            </TimelineDot>
            {idx < items.length - 1 && <TimelineConnector />}
        </TimelineSeparator>
        {(item.content !== undefined | item.content_title !== undefined) && (
                <TimelineContent sx={{ m: 'auto 0' }}>
                    <Typography variant="h6" component="span">
                        {item.content_title}
                    </Typography>
                    <Typography>
                        {item.content}
                    </Typography>
                </TimelineContent>
        )}
        </TimelineItem>
    ))}
    </MUITimeline>
    )
}
