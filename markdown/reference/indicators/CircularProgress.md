```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

`CircularProgress` indicators, commonly known as spinners, express an unspecified wait time or display the length of a process.

Progress indicators inform users about the status of ongoing processes, such as loading an app, submitting a form, or saving updates. They enhance user experience by providing visual feedback during operations that require time to complete.

- **Determinate** indicators display how long an operation will take
- **Indeterminate** indicators visualize an unspecified wait time

A progress indicator is essential for creating responsive user interfaces that keep users informed during data processing, file uploads, API calls, and other time-consuming operations. The `LoadingSpinner` component provides an elegant, Material UI-styled circular progress indicator.

For an alternative progress indicator, see [`LinearProgress`](LinearProgress.ipynb).

## Parameters

For details on other options for customizing the component, see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

### Core

* **`value`** (boolean | int): Whether the indicator is spinning (boolean) or the progress percentage (int, 0-100) for determinate variant
* **`variant`** (`Literal["determinate", "indeterminate"]`): The variant of the progress indicator

### Display

* **`bgcolor`** (`Literal['light', 'dark'] | None`): The color of the spinner background segment - 'light', 'dark', or None for no background
* **`color`** (str): The color variant of the spinning segment, which must be one of 'primary', 'secondary', 'success', 'info', 'warn', 'danger', 'light', 'dark'
* **`label`** (str): A label to display alongside the spinner
* **`size`** (int): The size of the spinner in pixels
* **`thickness`** (float): The thickness of the loading spinner stroke
* **`with_label`** (boolean): Whether to show a percentage label inside the loading spinner (when using the 'determinate' variant)

### Styling

- **`sx`** (dict): Component-level styling API for advanced customization
- **`theme_config`** (dict): Theming API for consistent design system integration

### Aliases

For compatibility with Panel, certain parameters are allowed as aliases:

- **`name`**: Alias for `label`

___

## Basic Usage

By default, the `CircularProgress` is initialized in a determinate, non-spinning state.


```python
pmui.CircularProgress()
```

You can instantiate it in an indeterminate, spinning state by setting `value=True`:


```python
pmui.CircularProgress(value=True)
```

You may add a `label`:


```python
pmui.CircularProgress(value=True, label="Progress")
```

### Size

You can customize the `size` of the CircularProgress to fit your design requirements:


```python
pmui.CircularProgress(value=True, size=100)
```

### Thickness

You can adjust the thickness of the CircularProgress stroke for visual emphasis:


```python
pmui.CircularProgress(value=True, size=50, thickness=10)
```

### Color and Background

You can customize both the `color` and `bgcolor` of the spinner to match your application's theme:


```python
pmui.CircularProgress(value=True, color="warning", bgcolor="dark")
```

Let's explore the full range of available `color` and `bgcolor` combinations:


```python
grid = pn.GridBox(*[' ']+pmui.CircularProgress.param.color.objects, nrows=4)

for bgcolor in pmui.CircularProgress.param.bgcolor.objects:
    grid.append(bgcolor or 'None')
    for color in pmui.CircularProgress.param.color.objects:
        spinner = pmui.CircularProgress(size=40, value=True, bgcolor=bgcolor, color=color)
        grid.append(spinner)

grid
```

### Determinate

When using the `determinate` variant, you can use the `CircularProgress` similarly to the `Progress` element to show specific completion percentages:


```python
pmui.CircularProgress(value=60, variant='determinate')
```

### Determinate with Label

You can also enable a percentage label inside the spinner with `with_label=True` for better user feedback:


```python
pmui.CircularProgress(value=42, variant='determinate', bgcolor='light', size=60, with_label=True)
```

### Example: Fetching Data

Here's a practical example showing how to use the `CircularProgress` to provide feedback during data fetching operations:


```python
import panel as pn
import panel_material_ui as pmui
from panel_material_ui import CircularProgress
from time import sleep

pn.extension()

fetch_progress = pmui.CircularProgress(value=True, visible=False, size=40, height=45)

def fetch_data(event):
    with fetch.param.update(disabled=True):
        with fetch_progress.param.update(visible=True):
            sleep(2.5)

fetch = pmui.Button(label="Fetch Data", variant="contained", on_click=fetch_data, icon="directions_run", width=200)

pmui.Column(fetch, fetch_progress)
```

### Example: KPI Dashboard

The `CircularProgress` with a percentage label can also be effectively used for displaying KPI (Key Performance Indicator) values in dashboards:


```python
pmui.Row(
    pmui.Paper(
        pmui.Typography("Open PRs", variant="h5"),
        pmui.CircularProgress(value=40, variant="determinate", size=60, with_label=True, align="center"),
        margin=10
    ),
    pmui.Paper(
        pmui.Typography("Closed PRs", variant="h5"),
        pmui.CircularProgress(value=60, variant="determinate", bgcolor='light', size=60, with_label=True, align="center"),
        margin=10
    )
)
```

## API Reference

Below is the complete API reference for the `CircularProgress` component:

### Parameters


```python
pmui.CircularProgress(height=40).api(jslink=True)
```

## References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets, enhancing user engagement and experience.
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces that update in real-time.
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications that automatically update when parameters change.

**Material UI Progress Documentation:**

- [Material UI Circular Progress Reference](https://mui.com/material-ui/react-progress/#circular) - Complete documentation for the underlying Material UI component, including usage examples and customization options.
- [Material UI Circular Progress API](https://mui.com/material-ui/api/circular-progress/) - Detailed API reference and configuration options for advanced customization and control.
