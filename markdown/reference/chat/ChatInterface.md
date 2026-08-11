```python
import panel as pn
from panel_material_ui import ChatInterface

pn.extension()
```

The `ChatInterface` is a high-level layout, providing a user-friendly front-end interface for inputting different kinds of messages: text, images, PDFs, etc.

This layout provides front-end methods to:

- Input (append) messages to the chat log.
- Re-run (resend) the most recent `user` input [`ChatMessage`](ChatMessage.ipynb).
- Remove messages until the previous `user` input [`ChatMessage`](ChatMessage.ipynb).
- Clear the chat log, erasing all [`ChatMessage`](ChatMessage.ipynb) objects.

**Since `ChatInterface` inherits from [`ChatFeed`](ChatFeed.ipynb), it features all the capabilities of [`ChatFeed`](ChatFeed.ipynb); please see [ChatFeed.ipynb](ChatFeed.ipynb) for its backend capabilities.**

Check out the [panel-chat-examples](https://holoviz-topics.github.io/panel-chat-examples/) docs to see applicable examples related to [LangChain](https://python.langchain.com/docs/get_started/introduction), [OpenAI](https://openai.com/blog/chatgpt), [Mistral](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjZtP35yvSBAxU00wIHHerUDZAQFnoECBEQAQ&url=https%3A%2F%2Fdocs.mistral.ai%2F&usg=AOvVaw2qpx09O_zOzSksgjBKiJY_&opi=89978449), [Llama](https://ai.meta.com/llama/), etc. If you have an example to demo, we'd love to add it to the panel-chat-examples gallery!

<img alt="Chat Design Specification" src="https://panel.holoviz.org/assets/ChatDesignSpecification.png"></img>

#### Parameters:

##### Core

* **`widgets`** (`Widget | List[Widget]`): Widgets to use for the input. If not provided, defaults to `[TextInput]`.
* **`user`** (`str`): Name of the ChatInterface user.
* **`avatar`** (`str | bytes | BytesIO | pn.pane.Image`): The avatar to use for the user. Can be a single character text, an emoji, or anything supported by `pn.pane.Image`. If not set, uses the first character of the name.
* **`reset_on_send`** (`bool`): Whether to reset the widget's value after sending a message; has no effect for `TextInput`.
* **`auto_send_types`** (`tuple`): The widget types to automatically send when the user presses enter or clicks away from the widget. If not provided, defaults to `[TextInput]`.
* **`input_params`** (`Dict[str, Any]`): Additional parameters to pass to the `ChatAreaInput` widget, e.g. `placeholder`, `enable_upload`, `max_rows`, `rows`. Updates are applied dynamically after initialization.
* **`button_properties`** (`Dict[Dict[str, Any]]`): Allows addition of functionality or customization of buttons by supplying a mapping from the button name to a dictionary containing the `icon`, `callback`, `post_callback`, and/or `js_on_click` keys. 
  * If the button names correspond to default buttons
(send, rerun, undo, clear), the default icon can be
updated and if a `callback` key value pair is provided,
the specified callback functionality runs before the existing one.
  * For button names that don't match existing ones,
new buttons are created and must include a
`callback`, `post_callback`, and/or `js_on_click` key.
  * The provided callbacks should have a signature that accepts
two positional arguments: instance (the ChatInterface instance)
and event (the button click event).
  * The `js_on_click` key should be a str or dict. If str,
provide the JavaScript code; else if dict, it must have a
`code` key, containing the JavaScript code
to execute when the button is clicked, and optionally an `args` key,
containing dictionary of arguments to pass to the JavaScript
code.

##### Styling

* **`show_send`** (`bool`): Whether to show the send button. Default is True.
* **`show_stop`** (`bool`): Whether to show the stop button, temporarily replacing the send button during callback; has no effect if `callback` is not async.
* **`show_rerun`** (`bool`): Whether to show the rerun button. Default is True.
* **`show_undo`** (`bool`): Whether to show the undo button. Default is True.
* **`show_clear`** (`bool`): Whether to show the clear button. Default is True.
* **`show_button_name`** (`bool`): Whether to show the button name. Default is True.

#### Properties:

* **`active_widget`** (`Widget`): The currently active widget.
* **`active`** (`int`): The currently active input widget tab index; -1 if there is only one widget available which is not in a tab.

___

#### Basics


```python
ChatInterface()
```

Although `ChatInterface` can be initialized without any arguments, it becomes much more useful, and interesting, with a `callback`.


```python
def even_or_odd(contents):
    if len(contents) % 2 == 0:
        return "Even number of characters."
    return "Odd number of characters."

ChatInterface(callback=even_or_odd)
```

You may also provide a more relevant, default `user` name and `avatar`.


```python
ChatInterface(
    callback=even_or_odd,
    user="Asker",
    avatar="?",
    callback_user="Counter",
)
```

#### Buttons

Unlike the buttons in the `panel.chat.ChatInterface` the `panel_material_ui.chat.ChatInterface` folds the buttons into the so called speed-dial. You can still control which options are available using the `show_` options.

If you're not using an LLM to respond, the `Rerun` button may not be practical so it can be hidden by setting `show_rerun=False`.

The same can be done for other buttons including `show_undo`, and `show_clear`:


```python
def get_num(contents):
    if isinstance(contents, str):
        num = len(contents)
    else:
        num = contents
    return f"Got {num}."

ChatInterface(callback=get_num, show_rerun=False, show_undo=False)
```

New buttons with custom functionality can be added to the input row through `button_properties`.


```python
def show_notice(instance, event):
    instance.send("This is how you add buttons!", respond=False, user="System")

ChatInterface(
    button_properties={"help": {"callback": show_notice, "icon": "help"}}
)
```

Default buttons can also be updated with custom behaviors, before using `callback` and after using `post_callback`.


```python
def run_before(instance, event):
    instance.send(
        "This will be cleared so it won't show after clear!",
        respond=False,
        user="System",
    )


def run_after(instance, event):
    instance.send("This will show after clear!", respond=False, user="System")


ChatInterface(
    button_properties={
        "clear": {"callback": run_before, "post_callback": run_after, "icon": "help"}
    }
)
```

#### Input Params

Use `input_params` to customize the input widget. Any `ChatAreaInput` parameter can be passed, and updates are applied dynamically.


```python
ChatInterface(input_params={"placeholder": "Ask anything...", "max_rows": 5})
```

Check out the [panel-chat-examples](https://holoviz-topics.github.io/panel-chat-examples/) docs for more examples related to [LangChain](https://python.langchain.com/docs/get_started/introduction), [OpenAI](https://openai.com/blog/chatgpt), [Mistral](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjZtP35yvSBAxU00wIHHerUDZAQFnoECBEQAQ&url=https%3A%2F%2Fdocs.mistral.ai%2F&usg=AOvVaw2qpx09O_zOzSksgjBKiJY_&opi=89978449), [Llama](https://ai.meta.com/llama/), etc.


Also, since `ChatInterface` inherits from [`ChatFeed`](ChatFeed.ipynb), be sure to also read [ChatFeed.ipynb](ChatFeed.ipynb) to understand `ChatInterface`'s full potential!
