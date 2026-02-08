"""
Minimal reproducible example to test LinearProgress and CircularProgress hiding behavior.

This app demonstrates:
1. Theme toggle (dark/light)
2. Spinner variant selector (linear/circular/none)
3. Button to trigger 3-second busy state
"""
import time
import panel as pn
from panel_material_ui.template import Page
from panel_material_ui import Button, Select, Row, Column

pn.extension()

def trigger_busy(event):
    """Simulate a 3-second long operation"""
    time.sleep(3)

# Create controls
theme_toggle_btn = Button(
    name='Toggle Theme',
    color='primary',
    width=200
)

spinner_select = Select(
    name='Busy Indicator',
    options=['linear', 'circular', None],
    value='linear',
    width=200
)

trigger_btn = Button(
    name='Trigger 3-Second Busy State',
    on_click=trigger_busy,
    color='success',
    width=250
)

# Instructions
instructions = pn.pane.Markdown("""
# Spinner Hide Test

This app tests that the busy indicators (LinearProgress and CircularProgress) are hidden when idle.

## Instructions:

1. **Check idle state**: Look at the header - the indicator should be invisible (no bar or spinner visible)
2. **Toggle theme**: Click "Toggle Theme" to switch between dark/light themes
3. **Change variant**: Select different busy indicator types (linear/circular/none)
4. **Test busy state**: Click "Trigger 3-Second Busy State" - indicator should appear after 1 second (debounce)
5. **Verify hiding**: After the operation completes, indicator should fade out and become invisible again

## Expected Behavior:

- **Idle state**: Indicator is completely invisible (opacity: 0)
- **Busy state**: Indicator smoothly fades in and animates (opacity: 1)
- **After busy**: Indicator smoothly fades out and becomes invisible again

## Visual Test:

Both themes should show:
- Clean header when idle (no visible progress bar or spinner)
- Indicator only appears when actually busy
- Smooth fade transitions
""")

# Create the page
page = Page(
    title='Spinner Hide Test',
    busy_indicator=spinner_select,
    main=[
        Column(
            instructions,
            Row(
                theme_toggle_btn,
                spinner_select,
                trigger_btn,
                sizing_mode='stretch_width'
            ),
            pn.pane.Markdown("---"),
            pn.pane.Markdown("### Test Results:"),
            pn.pane.Markdown("""
            - When idle, check the header - you should see NO progress bar or spinner
            - Click the button above to trigger a busy state
            - The indicator should appear smoothly after 1 second
            - After 3 seconds, it should disappear smoothly
            """),
        )
    ],
    sidebar=[
        pn.pane.Markdown("## Controls"),
        pn.pane.Markdown("Use the controls in the main area to test the spinner behavior."),
    ]
)

# Wire up theme toggle
def toggle_theme(event):
    page.dark_theme = not page.dark_theme

theme_toggle_btn.on_click(toggle_theme)

# Wire up spinner variant selector
def update_spinner(event):
    page.busy_indicator = event.new

spinner_select.param.watch(update_spinner, 'value')

page.servable()
