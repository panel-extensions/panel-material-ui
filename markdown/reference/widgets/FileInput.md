```python
import io

import panel as pn
import panel_material_ui as pmui

pn.extension("tabulator", "codeeditor")
```

The `FileInput` widget empowers you to seamlessly upload one or more files from the frontend, making filename, file data, and [MIME type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types) instantly available in Python. For handling large files efficiently, we recommend using the [`FileDropper`](https://panel.holoviz.org/reference/widgets/FileDropper.html) widget instead.

#### Parameters

For comprehensive customization options, explore our [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core Parameters

* **`accept`** (str): Define accepted file types using MIME types (e.g., 'image/png') or extensions (e.g., '.png') as a comma-separated list
* **`chunk_size`** (int): Size in bytes per chunk transferred across the WebSocket (`default=10000000`, i.e. 10MB).
* **`directory`** (bool): Enable directory upload when set to `True`, allowing users to select entire folders
* **`filename`** (str/list): Access the filename(s) of uploaded file(s)
* **`max_file_size`** (str): Maximum size of a file as a string with units given in KB or MB, e.g. 5MB or 750KB.
* **`max_files`** (int): Maximum number of files that can be uploaded if `multiple=True`.
* **`max_total_file_size`** (str): Maximum size of all uploaded files, as a string with units given in KB or MB, e.g. 5MB or 750KB.
* **`mime_type`** (str/list): Retrieve the MIME type(s) of uploaded file(s)
* **`multiple`** (bool): Allow multiple file selection when enabled
* **`value`** (bytes/list): Contains file data as bytes object(s) - single object or list depending on `multiple` setting

#### Available Methods

* **`save()`**: Persist the uploaded data to a file or `BytesIO` object
* **`clear()`**: Reset all file-related parameters (`value`, `filename`, `mime_type`) to their default state
* **`object()`**: Intelligent conversion of uploaded files to appropriate Python objects (e.g., CSV → pandas DataFrame)
* **`view()`**: Automatically display uploaded content using the most suitable visualization component
___

### Getting Started with FileInput

Let's begin with a simple example to see the `FileInput` widget in action:


```python
file_input = pmui.FileInput()

file_input
```

**💡 Pro tip:** The `FileInput` widget supports intuitive **drag and drop** functionality - simply drag files directly onto the upload button!

**Accessing your uploaded content** is straightforward. The `value` parameter contains a [bytestring](https://docs.python.org/3/library/stdtypes.html#bytes-objects) with your file's contents, while the `mime_type` parameter provides the file type information in standard MIME format (e.g., `image/png`, `text/csv`).


```python
file_input.value
```

**Explore the key parameters** below - `value`, `filename`, and `mime_type` work together to give you complete information about uploaded files:


```python
pmui.FlexBox(file_input.param.value, file_input.param.filename, file_input.param.mime_type)
```

**🎯 Try it yourself!** Upload a file above and watch the parameters update in real-time.

### Saving Uploaded Files

Once you've received a file upload, the built-in `save()` method makes it easy to persist the data. You can save to either a file on disk or a [BytesIO](https://docs.python.org/3/library/io.html#binary-i-o) object for in-memory processing:


```python
# File
if file_input.value is not None:
    file_input.save('test.png')

# BytesIO object
if file_input.value is not None:
    out = io.BytesIO()
    file_input.save(out)
```

### Controlling File Types with Smart Filtering

The `accept` parameter gives you precise control over which files users can select. Using standard HTML file input patterns, you can specify:

**File Extensions:**
* `.gif, .jpg, .png, .doc` - Specific file extensions are selectable

**Media Categories:**
* `audio/*` - All audio files (MP3, WAV, etc.)
* `video/*` - All video files (MP4, AVI, etc.)
* `image/*` - All image files (PNG, JPEG, etc.)

**MIME Types:**
* Any valid [IANA Media Type](https://www.iana.org/assignments/media-types/media-types.xhtml) for precise control

**Example:** Restrict to data files only:


```python
pmui.FileInput(accept='.csv,.json')
```

### Handling Multiple Files and Directories

**Scale up your file handling** with these powerful options:
- Set `multiple=True` to allow users to select several files at once
- Use `directory=True` to enable entire folder uploads

Here's how to accept multiple PNG files:


```python
pmui.FileInput(accept='.png', multiple=True)
```

**Important:** When `multiple=True` or `directory=True` is enabled, the `value`, `filename` and `mime_type` parameters automatically become lists, making it easy to iterate through all uploaded files.

### Resetting the FileInput

Need a fresh start? The `clear()` method instantly resets all file-related parameters to their default values:


```python
# file_input.clear()
```

### Intelligent File Object Conversion

The `FileInput.object` property is your gateway to working with uploaded files as native Python objects. This smart feature automatically converts files based on their type:

**Automatic Conversions:**
- 📊 CSV files → pandas `DataFrame`
- 🗂️ JSON files → Python `dict`
- 🖼️ Images → PIL `Image` objects
- 📄 And many more!

**Try it below** - upload different file types and see the magic happen:


```python
file_input = pmui.FileInput(accept='.csv,.json,.png,.mp3,.mp4')
pmui.Column(file_input, file_input.object)
```

**Pro tip:** When you know your uploaded file will become a `DataFrame`, you can customize its display using Panel's visualization components:


```python
file_input = pmui.FileInput(accept='.csv,.xlsx')
pmui.Column(file_input, pn.widgets.Tabulator(value=file_input.object, height=200, width=500))
```

### Automatic Content Visualization

The `view()` method takes the guesswork out of displaying uploaded files by automatically choosing the best visualization component for each file type:


```python
import panel_material_ui as pmui
import panel as pn

pn.extension("tabulator", "codeeditor") # You must manually configure the possible extensions needed depending on the `accept` value.

file_input = pmui.FileInput(
    label="Upload an image",
    accept=".csv,.xlsx,.png,.jpg,.jpeg,.json,.mp3,.mp4,.pdf",
    multiple=True,
)

pmui.Column(file_input, file_input.view(height=300, width=500))
```

In addition to converting the `value` to a displayable `object` it also picks an appropriate component to display the `object` with based on the `mime_type`.

**How it works:** The method intelligently converts your uploaded `value` to a displayable `object`, then selects the most appropriate display component based on the file's `mime_type`.

**Customization Options:**

- **`object_if_no_value`**: Choose what to display when no files are uploaded (defaults to invisible layout)
- **`layout`**: Specify how multiple files are organized (defaults to `panel_material_ui.Tabs`)
- **`**kwargs`**: Pass styling options like `height`, `width`, and `sizing_mode` to the layout

**The result?** Professional-looking file previews with zero configuration!

### Real-World Example: CSV Data Explorer

Here's a practical example showing how to build a custom CSV file processor. This app demonstrates advanced file handling with custom conversion logic:


```python
import panel_material_ui as pmui
import panel as pn
import io
import pandas as pd
import io

pn.extension("tabulator")

file_input = pmui.FileInput(
    label="Upload a CSV file",
    accept=".csv",
    color="success",
    variant="outlined",
)

def csv_to_pandas(value):
    """Convert uploaded CSV file to a pandas DataFrame."""
    if value:
        return pd.read_csv(io.BytesIO(value))
    return pd.DataFrame()

df = pn.bind(csv_to_pandas, file_input)

pmui.Column(file_input, pn.widgets.Tabulator(value=df, height=300, width=800))
```

### Real-World Example: Image Viewer

Build a sleek image viewer that handles multiple formats with graceful fallbacks. This example shows how to create custom processing functions for specialized file types:


```python
import panel_material_ui as pmui
import panel as pn
from PIL import Image
import io

pn.extension()

file_input = pmui.FileInput(
    label="Upload an image",
    accept=".png, .jpg, .jpeg",
    multiple=False,
)

def image_view(value):
    """Callback function to handle image upload."""
    if value:
        image = Image.open(io.BytesIO(value))
        return pn.pane.Image(image, height=250)
    return "No Image"

file_view = pn.bind(image_view, file_input)

pmui.Column(file_input, file_view)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
icon_file_input = pmui.FileInput(label=":material/upload_file: Upload file")

icon_file_input
```

## API

### Parameters


```python
file_input.api(jslink=True)
```
