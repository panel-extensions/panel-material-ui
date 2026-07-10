```python
import tempfile

import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `FileDownload` widget allows downloading a file on the frontend by sending the file data to the browser either on initialization (if `embed=True`) or when the button is clicked.

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html). Alternatively, learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`auto`** (boolean):  Whether to download the file with the first click (if `True`) or only after clicking a second time (if `False`, enables right-click -> Save as).
* **`callback`** (callable): A callable that returns a file or file-like object (takes precedence over `file` if set). 
* **`embed`** (boolean):  Whether to embed the data on initialization.
* **`file`** (str, Path or file-like object):  A path to a file or a file-like object.
* **`filename`** (str): The filename to save the file as.

##### Display

* **`color`** (str): The color variant of the button, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`description`** (str | Bokeh Tooltip | pn.widgets.TooltipIcon): A description which is shown when the widget is hovered.
* **`disable_elevation`** (boolean): Whether to apply elevation to the `Button` to visually separate it from the background.
* **`end_icon`** (str): An icon to render to the right of the button label. Either an SVG or an icon name which is loaded from [Material UI Icons](https://mui.com/material-ui/material-icons).
* **`icon`** (str): An icon to render to the left of the button label. Either an SVG or an icon name which is loaded from [Material UI Icons](https://mui.com/material-ui/material-icons).
* **`icon_size`** (str): Size of the icon as a string, e.g. 12px or 1em.
* **`label`** (str): A custom label for the download button (by default uses the filename)
* **`variant`** (str): The button style, either 'contained', 'outlined', 'text'.

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

##### Aliases

For compatibility with Panel certain parameters are allowed as aliases:

- **`button_style`**: Alias for `variant`
- **`button_type`**: Alias for `color`
- **`name`**: Alias for `label`

___

### Basic Usage

The `FileDownload` widget accepts a path to a file or a file-like object (with a `.read` method) if the latter is provided a `filename` must also be set. By default (`auto=True` and `embed=False`) the file is only transferred to the browser after the button is clicked (this requires a live-server or notebook kernel):


```python
# Write file
tmp = tempfile.NamedTemporaryFile(prefix='hello_', suffix='.txt', delete=False)
text = """
Hello!
""".encode('utf-8')
tmp.write(text)
tmp.seek(0)

file_download = pmui.FileDownload(file=tmp.name)

file_download
```

### Embedding data

The file data may also be embedded immediately using `embed` parameter, this allows using the widget even in a static export (such as in these docs):


```python
pmui.FileDownload(file=tmp.name, filename='hello.txt', embed=True)
```

### Request data

If `auto=False` is set the file will not be downloaded on the initial click but will change the label from "Transfer <file>" to "Download <file>" once the data has been synced. This offers an opportunity to download using the `Save as` dialog once the data has been transferred.


```python
pmui.FileDownload(
    file=tmp.name, filename='hello.txt', button_type='success', auto=False, embed=False
)
```

### In-memory files

The `FileDownload` widget may also be given a file-like object, e.g. here we save a `pandas.DataFrame` as a CSV to a `StringIO` object and pass that to the widget:


```python
from bokeh.sampledata.autompg import autompg

from io import StringIO
sio = StringIO()
autompg.to_csv(sio)
sio.seek(0)

pmui.FileDownload(file=sio, embed=True, filename='autompg.csv')
```

:::note
When providing an in-memory file object you must define a `filename`.
::

### Dynamic data

If you want to generate the file dynamically, e.g. because it depends on the parameters of some widget you can also supply a callback (which may be decorated with the widgets and/or parameters it depends on):


```python
years_options = list(autompg.yr.unique())
years = pmui.MultiChoice(
    label='Years', options=years_options, value=[years_options[0]], margin=(0, 20, 0, 0)
)
mpg = pmui.RangeSlider(
    label='Mile per Gallon', start=autompg.mpg.min(), end=autompg.mpg.max()
)

def filtered_mpg(yrs, mpg):
    df = autompg
    if years.value:
        df = autompg[autompg.yr.isin(yrs)]
    return df[(df.mpg >= mpg[0]) & (df.mpg <= mpg[1])]

def filtered_file(yr, mpg):
    df = filtered_mpg(yr, mpg)
    sio = StringIO()
    df.to_csv(sio)
    sio.seek(0)
    return sio

fd = pmui.FileDownload(
    callback=pn.bind(filtered_file, years, mpg), filename='filtered_autompg.csv'
)

pmui.Column(
    pmui.Row(years, mpg),
    fd,
    pn.pane.DataFrame(pn.bind(filtered_mpg, years, mpg), width=600),
    width=600, margin=10
)
```

### Disabled and Loading

Like any other widget the `Button` can be `disabled` and / or set to `loading`:


```python
pmui.FileDownload(label="Loading", disabled=True, loading=True)
```

### Sizes

For larger or smaller buttons, use the `size` parameter.


```python
pmui.Row(
    pmui.FileDownload(size="small", label="Small", file=tmp.name), 
    pmui.FileDownload(size="medium", label="Medium", file=tmp.name),
    pmui.FileDownload(size="large", label="Large", file=tmp.name)
)
```

### Colors and Variants

The color of the `FileDownload` button can be set by selecting one of the available `color` values and the `variant` can be `'filled'`, `'outlined'` or `'text'`:


```python
pmui.Row(
    *(pmui.Column(*(
        pmui.FileDownload(color=color, variant=variant, file=f'{color}.png', width=225)
        for color in pmui.Button.param.color.objects
    ))
    for variant in pmui.Button.param.variant.objects)
)
```

## Icons

However you can also provide an explicit `icon`, either as a named icon loaded from [Material Icons](https://fonts.google.com/icons?icon.set=Material+Icons):


```python
pmui.Row(
    pmui.FileDownload(icon='warning', color='warning', file='FileDownload.ipynb'),
    pmui.FileDownload(icon='bug_report', color='error', file='FileDownload.ipynb')
)
```

or as an explicit SVG:


```python
search_icon = """
<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="currentColor"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
"""

pmui.Row(
  pmui.FileDownload(icon=search_icon, icon_size='1em', label='Search', variant="outlined"),
  pmui.FileDownload(icon=search_icon, icon_size='2em', label='Search', variant="contained"),
)
```

You can also provide an end icon:


```python
pmui.FileDownload(variant="contained", end_icon="send_icon")
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
pmui.FileDownload(
    file=tmp.name,
    label=":material/zoom_out_map: Export",
    color="primary",
)
```

### API Reference

The `FileDownload` widget exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
file_download.api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Button:**

- [Material UI Button Reference](https://mui.com/material-ui/react-button/) - Complete documentation for the underlying Material UI component
- [Material UI Button API](https://mui.com/material-ui/api/button/) - Detailed API reference and configuration options
