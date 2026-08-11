```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `LinearProgress` widget displays the status of ongoing processes, providing visual feedback to users about task completion. It supports two primary modes:

- **Determinate mode**: Shows specific progress with a known completion percentage.
- **Indeterminate mode**: Displays ongoing activity without a specific completion time

This component is essential for creating responsive user interfaces that keep users informed during data processing, file uploads, API calls, and other time-consuming operations.

For an alternative progress indicator see [`CircularProgress`](CircularProgress.ipynb).

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`active`** (boolean): Whether to animate the progress bar when in indeterminate mode
* **`max`** (int): The maximum progress value (defaults to 100)
* **`value`** (float): The current progress value; set to -1 or omit for indeterminate state
* **`value_buffer`** (int): The buffer value for buffered progress (only available with `buffer` variant)

##### Display

* **`color`** (str): The color variant of the progress bar, which must be one of 'default', 'primary' (default), 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark'
* **`variant`** (`Literal["determinate", "indeterminate", "buffer", "query"]`): The visual style variant of the progress indicator

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

___

### Basic Usage

Create a determinate progress bar by specifying both the current `value` and optional `max` value (defaults to 100). This shows users exactly how much of a task has been completed:


```python
progress = pmui.LinearProgress(label='LinearProgress', value=20, width=200)
progress
```

The progress `value` can be dynamically updated from Python:


```python
progress.value = 80
```

Let's reset it back to 20:


```python
progress.value = 20
```

For operations with unknown duration, create an indeterminate progress bar that continuously animates to indicate ongoing activity:


```python
indeterminate = pmui.LinearProgress(label='Indeterminate LinearProgress', variant="indeterminate", width=200)
indeterminate
```

### Color

The `LinearProgress` widget supports a comprehensive range of color themes to match your application's design:


```python
pn.GridBox(
    "default", pmui.LinearProgress(value=40, color="default", width=300, margin=22),
    "primary", pmui.LinearProgress(value=40, color="primary", width=300, margin=22),
    "secondary", pmui.LinearProgress(value=40, color="secondary", width=300, margin=22),
    "error", pmui.LinearProgress(value=40, color="error", width=300, margin=22),
    "info", pmui.LinearProgress(value=40, color="info", width=300, margin=22),
    "success", pmui.LinearProgress(value=40, color="success", width=300, margin=22),
    "warning", pmui.LinearProgress(value=40, color="warning", width=300, margin=22),
    "light", pmui.LinearProgress(value=40, color="light", width=300, margin=22),
    "dark", pmui.LinearProgress(value=40, color="dark", width=300, margin=22),
    "danger", pmui.LinearProgress(value=40, color="danger", width=300, margin=22),
    ncols=2,
)
```

### Variants

The `LinearProgress` widget offers several variants to suit different use cases:

- **Determinate**: Shows specific progress with a known completion percentage
- **Indeterminate**: Displays ongoing activity without a specific completion time
- **Buffer**: Shows both primary progress and a buffer value (useful for streaming content)
- **Query**: Indicates a query operation in progress


```python
pn.GridBox(
    "Determinate", pmui.LinearProgress(value=60, variant="determinate", width=300, margin=22),
    "Indeterminate", pmui.LinearProgress(variant="indeterminate", margin=22),
    "Buffer", pmui.LinearProgress(value=60, value_buffer=80, variant="buffer", width=300, margin=22),
    "Query", pmui.LinearProgress(variant="query", margin=22),
    ncols=2,
)
```

### Best Practices

**When to use each variant:**
- Use **determinate** progress when you can calculate the completion percentage (e.g., file uploads, data processing)
- Use **indeterminate** progress for operations with unknown duration (e.g., server requests, initialization)
- Use **buffer** variant for streaming scenarios where you want to show both loaded and buffered content
- Choose appropriate colors that align with your application's theme and accessibility requirements

### Example: Processing Data


```python
import panel as pn
import panel_material_ui as pmui
from panel_material_ui import LinearProgress
from time import sleep

pn.extension()

run_progress = pmui.LinearProgress(value=0, variant="determinate", visible=False, width=200)

def process_data(event):
    with run.param.update(disabled=True):
        with run_progress.param.update(visible=True, value=0):
            for i in range(1, 100):
                run_progress.value = i
                sleep(0.03)

run = pmui.Button(label="Process Data", variant="contained", on_click=process_data, icon="directions_run", width=200)

pmui.Column(run, run_progress,)
```

### Example: Fetching Data


```python
import panel as pn
import panel_material_ui as pmui
from panel_material_ui import LinearProgress
from time import sleep

pn.extension()

fetch_progress = LinearProgress(visible=False, variant="indeterminate", width=200)

def fetch_data(event):
    with fetch.param.update(disabled=True):
        with fetch_progress.param.update(visible=True):
            sleep(2.5)

fetch = pmui.Button(label="Fetch Data", variant="contained", on_click=fetch_data, icon="directions_run", width=200)

pmui.Column(fetch, fetch_progress,)
```

### API Reference

#### Parameters


```python
progress.api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Progress Documentation:**

- [Material UI Linear Progress Reference](https://mui.com/material-ui/react-progress/#linear) - Complete documentation for the underlying Material UI component
- [Material UI Linear Progress API](https://mui.com/material-ui/api/linear-progress/) - Detailed API reference and configuration options
