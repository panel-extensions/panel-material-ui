```python
import asyncio
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `ChatAreaInput` inherits from `TextAreaInput`, allowing entering any multiline string using a text input
box, with the ability to click the "Enter" key or optionally the "Ctrl-Enter" key to submit the message.

Whether "Enter" or "Ctrl-Enter" sends the message depends on whether the `enter_sends` parameter is set to True (the default) or False.

Unlike TextAreaInput, the `ChatAreaInput` defaults to auto_grow=True and
max_rows=10, and the `value` is not synced to the server until the message is actually sent, so watch `value_input` if you need to access what's currently
available in the text input box.

Lines are joined with the newline character `\n`.

The primary purpose of `ChatAreaInput` is its use with [`ChatInterface`](ChatInterface.ipynb) for a high-level, *easy to use*, *ChatGPT like* interface.

<img alt="Chat Design Specification" src="https://panel.holoviz.org/assets/ChatDesignSpecification.png"></img>

#### Parameters:

For layout and styling-related parameters see the [Control the size](../../tutorials/basic/size.md), [Align Content](../../tutorials/basic/align.md) and [Style](../../tutorials/basic/style.md) tutorials.

##### Core

* **`accept`** (str): A comma separated string of file extensions (with dots) or MIME types
  that should be accepted for upload. Examples: '.csv,.json,.txt' or
  'text/csv,application/json'.
* **`actions`** (dict): A dictionary of actions that can be invoked via the speed dial to the
  left of input area. The actions should be defined as a dictionary indexed
  by the name of the action mapping to values that themselves are dictionaries
  containing an icon. Users can define callbacks by registering callbacks using
  the on_action method.
* **`disabled_enter`** (bool): If True, disables sending the message by pressing the `enter_sends` key.
* **`enable_upload`** (bool): If True, enables uploading of files.
* **`enter_sends`** (bool): If True, pressing the Enter key sends the message, if False it is sent by pressing the Ctrl-Enter. Defaults to True.
* **`value`** (str): The value when the "Enter" or "Ctrl-Enter" key is pressed. Only to be used with `watch` or `bind` because the `value` resets to `""` after the message is sent; use `value_input` instead to access what's currently available in the text input box.
* **`value_input`** (str): The current value updated on every key press.
* **`value_uploaded`** (dict): Dictionary containing raw file data keyed by filename after user sends uploads. Each entry contains mime_type, value (bytes), and size
* **`pending_uploads`** (list): List of filenames that have been selected for upload but not yet transferred to the server.
* **`enter_pressed`** (bool): Event when the Enter/Ctrl+Enter key has been pressed.
* **`on_submit`** (callable): Callback to invoke when the send button or enter is pressed; should accept an event and instance as args. If unspecified, the default behavior is to send a Column containing the input text and views. This only affects the user-facing input, and does not affect the `send` method.

##### Display

* **`auto_grow`** (boolean, default=True): Whether the TextArea should automatically grow in height to fit the content.
* **`cols`** (int, default=2): The number of columns in the text input field.
* **`disabled`** (boolean, default=False): Whether the widget is editable
* **`max_length`** (int, default=50000): Max character length of the input field. Defaults to 50000
* **`max_rows`** (int, default=10): The maximum number of rows in the text input field when `auto_grow=True`.
* **`name`** (str): The title of the widget
* **`placeholder`** (str): A placeholder string displayed when no value is entered
* **`rows`** (int, default=2): The number of rows in the text input field.
* **`resizable`** (boolean | str, default='both'): Whether the layout is interactively resizable, and if so in which dimensions: `width`, `height`, or `both`.
* **`views`** (list): A list of views of the uploaded files.

##### Methods

* **`sync()`**: Programmatically syncs uploaded files to the server without requiring the user to press Enter or click submit.
___

#### Basics

To submit a message, press the "Enter" key if **`enter_sends`** is True (the default), else press "Ctrl-Enter".


```python
pmui.ChatAreaInput(placeholder="Type something, and press Enter to clear!")
```

The `ChatAreaInput` is useful alongside `pn.bind` or `param.depends`.


```python
def output(value):
    return f"Submitted: {value}"

chat_area_input = pmui.ChatAreaInput(placeholder="Type something, and press Enter to submit!")
output_markdown = pn.bind(output, chat_area_input.param.value)
pmui.Row(chat_area_input, output_markdown)
```

To see what's currently typed in, use `value_input` instead because `value` will only be set during submission and be `""` otherwise.


```python
chat_area_input = pmui.ChatAreaInput(enter_sends=False,   # To submit a message, press Ctrl-Enter
                                        placeholder="Type something, do not submit it, and run the next cell",)
output_markdown = pn.bind(output, chat_area_input.param.value)

pmui.Row(chat_area_input, output_markdown)
```


```python
print(f'{chat_area_input.value_input=}, {chat_area_input.value=}')
```

#### Programmatic File Sync

The `sync()` method allows you to programmatically sync uploaded files to the server without requiring the user to press Enter or click the submit button. This is useful when you want to process file uploads separately from text input, or when building custom workflows.

##### Checking Uploaded Files

Using the `pending_uploads` parameter, you can check which files have been selected for upload but not yet synced to the server. This allows you to provide feedback to users about their selected files before they are processed.


```python
def check_pending_uploads(count):
    return f"Uploaded {count} file(s)!"

chat_area = pmui.ChatAreaInput(placeholder="Upload a file, then click Sync")
result = pn.bind(check_pending_uploads, chat_area.param.pending_uploads)
pmui.Row(chat_area, result)
```

##### Accessing File Contents

The `value_uploaded` dictionary contains the raw file data for each uploaded file. Each entry is keyed by filename and contains:

- `mime_type`: The MIME type of the file (e.g., 'text/plain', 'image/png')
- `value`: The file contents as bytes
- `size`: The file size in bytes

Here's an example showing how to read the contents of uploaded text files:


```python
async def on_sync_click(event):
    print("Initiating file sync...")
    chat_area.sync()

def on_sync_complete(value_uploaded):
    result = ""
    for filename, data in value_uploaded.items():
        result += (
            f"File: {filename}"
            f"  MIME type: {data['mime_type']}"
            f"  Size: {data['size']} bytes\n"
        )
    return result

chat_area = pmui.ChatAreaInput(placeholder="Upload a file, then click Sync")
result = pn.bind(on_sync_complete, chat_area.param.value_uploaded)

sync_button = pmui.Button(label="Sync", on_click=on_sync_click)

pmui.Row(chat_area, sync_button, result)
```
