```python
import pathlib
import tempfile

import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `FileSelector` widget allows browsing the filesystem on the server and selecting one or more files in a directory. It renders a navigation toolbar, a breadcrumb trail and an editable path field, a list of the entries in the current directory and a collapsible summary of the current selection.

It falls into the broad category of multi-value, option-selection widgets that provide a compatible API and include the [`CrossSelector`](CrossSelector.ipynb) and [`MultiSelect`](MultiSelect.ipynb) widgets. Unlike those, its options are discovered by listing a filesystem rather than supplied up front.

Discover more on using widgets to add interactivity to your applications in the [how-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html). Alternatively, learn [how to set up callbacks and (JS-)links between parameters](https://panel.holoviz.org/how_to/links/index.html) or [how to use them as part of declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html).

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`directory`** (str): The directory currently shown.
* **`disabled`** (boolean): Whether the widget is editable
* **`file_pattern`** (str): A glob-like pattern applied to files, not directories.
* **`only_files`** (boolean): Whether only files can be selected, i.e. whether directories are selectable.
* **`refresh_period`** (int): How frequently, in milliseconds, to re-list the directory. Disabled when `None`.
* **`root_directory`** (str): The boundary the user cannot navigate above. Defaults to the directory the widget was initialized with.
* **`show_hidden`** (boolean): Whether to list hidden files and directories, i.e. those starting with a period.
* **`value`** (list): The selected paths.

The `fs` keyword argument additionally accepts an [`fsspec`](https://filesystem-spec.readthedocs.io/) filesystem, which makes the widget browse a remote filesystem such as S3 or GCS instead of the local one.

##### Display

* **`color`** (str): The color variant of the inputs, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`label`** (str): The title of the widget
* **`size`** (int): The approximate number of entries shown at once, which bounds the height of the entry list.

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

##### Aliases

For compatibility with Panel certain parameters are allowed as aliases:

- **`name`**: Alias for `label`

___

### Basic Usage

The examples below browse a small tree built in a temporary directory so they render the same wherever the docs are built:


```python
root = pathlib.Path(tempfile.mkdtemp()) / 'data'

for subdir in ('measurements', 'images'):
    (root / subdir).mkdir(parents=True)

(root / 'README.md').write_text('# Data\n')
(root / 'measurements' / 'run1.csv').write_text('a,b\n1,2\n')
(root / 'measurements' / 'run2.csv').write_text('a,b\n3,4\n')
(root / 'images' / 'plot.png').write_bytes(b'')

file_selector = pmui.FileSelector(str(root), label='Select files')

file_selector
```

Double-click a folder row, or use the chevron on the right of the row, to navigate into it. The toolbar navigates back, forward and up, and reloads the listing, while the breadcrumb trail and the path field jump straight to a directory. Checking a row adds its path to `value`:


```python
file_selector.value
```

### Confining Navigation

By default `root_directory` is pinned to the directory the widget was initialized with, so the user cannot navigate above it. Set it explicitly to open the widget on a subdirectory while still allowing navigation up to the root.

A `FileSelector` is a filesystem read primitive, and `root_directory` is the only thing standing between a browser and the read permissions of the process serving the app. Always set it when serving to untrusted users. Paths arriving from the browser are resolved and validated against the root on the server, so symlinks pointing outside the root and sibling directories sharing a name prefix with it are both rejected.


```python
pmui.FileSelector(str(root / 'measurements'), root_directory=str(root))
```

### Filtering

`file_pattern` applies a glob to files, `show_hidden` controls whether dotfiles are listed and `only_files` makes directories navigable but not selectable:


```python
pmui.FileSelector(
    str(root / 'measurements'), root_directory=str(root),
    file_pattern='*.csv', only_files=True
)
```

### Size

`size` bounds the height of the entry list, expressed as an approximate number of rows:


```python
pmui.FileSelector(str(root), size=3)
```

### Colors

The `color` parameter sets the color of the checkboxes, breadcrumb links and selection chips:


```python
pn.FlexBox(*(
    pmui.FileSelector(str(root), label=color, color=color, size=3, width=300)
    for color in pmui.FileSelector.param.color.objects
))
```

### Disabled & Loading

Like any other widget the `FileSelector` can be `disabled` and/or show a `loading` indicator:


```python
pmui.FileSelector(str(root), size=3, disabled=True, loading=True)
```

### Remote Filesystems

Passing an [`fsspec`](https://filesystem-spec.readthedocs.io/) filesystem as the `fs` argument makes the widget browse that filesystem instead of the local one. Paths keep their scheme and `root_directory` confines navigation just as it does locally:



```python
import fsspec

memory_fs = fsspec.filesystem('memory')
memory_fs.mkdirs('/datasets/measurements', exist_ok=True)

for name, content in (
    ('/datasets/README.md', b'# Data'),
    ('/datasets/measurements/run1.csv', b'a,b\n1,2'),
):
    with memory_fs.open(name, 'wb') as f:
        f.write(content)

pmui.FileSelector('memory://datasets', fs=memory_fs)
```

Any other `fsspec` backend works the same way, e.g. S3:

```python
import s3fs

pmui.FileSelector('s3://datasets.holoviz.org', fs=s3fs.S3FileSystem(anon=True))
```

### API Reference

#### Parameters

The `FileSelector` widget exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.FileSelector(str(root), label='FileSelector').api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications
- [Panel `FileSelector` reference](https://panel.holoviz.org/reference/widgets/FileSelector.html) - The classic Panel implementation this widget is API compatible with

**Material UI List:**

- [Material UI List Reference](https://mui.com/material-ui/react-list/) - Complete documentation for the underlying Material UI component
- [Material UI Breadcrumbs Reference](https://mui.com/material-ui/react-breadcrumbs/) - Documentation for the breadcrumb trail
