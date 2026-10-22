```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Avatar` component displays profile pictures, user initials, or icons in a compact, circular or square format. Avatars are commonly used throughout user interfaces to represent users, brands, or entities in a visually consistent manner.

The component supports multiple content types including images, text initials, and icons, with automatic fallback handling when images fail to load.

#### Parameters:

For details on other options for customizing the component see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`clicks`** (int): The number of times the avatar has been clicked (read-only). Default is 0.
* **`content`** (str): The content to display - can be an image URL/path or text initials.

##### Display

* **`alt_text`** (str): Alternative text for screen readers and when images fail to load.
* **`color`** (str): Background color for text and icon avatars - supports CSS color values.
* **`size`** (str): Size of the avatar - options include 'small', 'medium' (default), and 'large'.
* **`variant`** (str): Shape variant - either 'rounded' (default) or 'square'.

##### Styling

- **`sx`** (dict): Component level styling API for advanced customization
- **`theme_config`** (dict): Theming API for consistent design system integration

#### Constructor Arguments

* **`on_click`** (callable): A Python callback to be triggered when the avatar is clicked

#### Methods

* **`on_click`** (callable): Registers a Python callback to be executed when the Avatar is clicked

___

### Basic Usage

Create a simple image avatar by providing an image URL or local path:


```python
pmui.Avatar(
    content="https://mui.com/static/images/avatar/1.jpg",
    alt_text="User Profile",
)
```

### Sizes

The `Avatar` component supports different sizes to fit various layout requirements:


```python
pmui.Row(
    pmui.Avatar(content="https://mui.com/static/images/avatar/1.jpg", size="small", margin=10),
    pmui.Avatar(content="https://mui.com/static/images/avatar/1.jpg", size="medium", margin=10),
    pmui.Avatar(content="https://mui.com/static/images/avatar/1.jpg", size="large", margin=10),
)
```

### Variants

The `Avatar` component offers different shape variants:

- **Rounded**: Default style with rounded corners for a softer appearance
- **Square**: Sharp corners for a more geometric look


```python
pmui.Row(
    pmui.Avatar(content="https://mui.com/static/images/avatar/1.jpg", variant="rounded", margin=10),
    pmui.Avatar(content="https://mui.com/static/images/avatar/1.jpg", variant="square", margin=10),
)
```

### Text Based Avatars

You can also define text based avatars


```python
pmui.Row(
    pmui.Avatar(content="P", variant="rounded", margin=10),
    pmui.Avatar(content="R", variant="square", margin=10),
)
```

### Colors

Customize avatar background colors for text and icon avatars to match your design system or indicate different user types:


```python
pmui.FlexBox(
    pmui.Avatar(content="A", color="#f44336", margin=10),
    pmui.Avatar(content="B", color="#2196f3", margin=10),
    pmui.Avatar(content="C", color="#4caf50", margin=10),
    pmui.Avatar(content="D", color="#ff9800", margin=10),
)
```

### Handling Clicks

The `Avatar` component supports click events through the `clicks` parameter and `on_click` method. This makes avatars interactive and useful for user profile actions or navigation.


```python
clickable_avatar = pmui.Avatar(content="JD", color="#2196f3", variant="square")
click_display = pmui.Typography(f"Clicks: {clickable_avatar.clicks}", variant="body2")

pn.bind(lambda event: click_display.param.update(object=f"Clicks: {clickable_avatar.clicks}"), clickable_avatar.param.clicks, watch=True)

pmui.Row(clickable_avatar, click_display)
```

You can also use the `on_click` method to register a callback function:


```python
profile_avatar = pmui.Avatar(content="https://mui.com/static/images/avatar/2.jpg", alt_text="Profile")
status_text = pmui.Typography("Click the avatar to view profile", variant="body2")

def handle_profile_click(event):
    status_text.object = f"Profile clicked! Total clicks: {profile_avatar.clicks}"

profile_avatar.on_click(handle_profile_click)

pmui.Row(profile_avatar, status_text)
```

### JavaScript Callbacks

For client-side interactions, you can use the `js_on_click` method to register JavaScript callbacks:


```python
javascript_code = """
alert('Avatar clicked! This is a client-side JavaScript callback.');
"""

js_avatar = pmui.Avatar(content="JS", color="#ff5722", variant="square")
js_avatar.js_on_click(code=javascript_code)

pmui.Column(
    pmui.Typography("Click the avatar below to trigger a JavaScript alert:", variant="body2"),
    js_avatar,
)
```

### Fallback Handling

Avatars automatically handle fallbacks when images fail to load. The component will attempt to display alternative content based on the `alt_text` parameter:


```python
pmui.Avatar(
    content="https://broken-image-url.jpg",
    alt_text="John Doe",
)
```

### Loading


```python
pmui.Avatar(
    content="https://mui.com/static/images/avatar/1.jpg",
    loading=True,
)
```

### Example: Interactive Avatar Grid

Here's a practical example showing clickable avatars in a user selection interface:


```python
users = [
    {"name": "Alice", "initials": "AL", "color": "#e91e63"},
    {"name": "Bob", "initials": "BO", "color": "#2196f3"},
    {"name": "Charlie", "initials": "CH", "color": "#4caf50"},
    {"name": "Diana", "initials": "DI", "color": "#ff9800"},
]

selected_user = pmui.Typography("Select a user by clicking their avatar", variant="h6")

def create_user_avatar(user):
    avatar = pmui.Avatar(content=user["initials"], color=user["color"], size="large", margin=5)

    def handle_user_click(event):
        selected_user.object = f"Selected: {user['name']} (clicked {avatar.clicks} times)"

    avatar.on_click(handle_user_click)
    return avatar

avatar_grid = pmui.Row(*[create_user_avatar(user) for user in users])

pmui.Column(
    pmui.Typography("User Selection", variant="h5"),
    avatar_grid,
    selected_user,
    width=600,
)
```

### Example: User Profile Card

Here's a practical example showing how to use avatars in a user profile context with reactive updates:


```python
import param

class UserProfile(param.Parameterized):
    user_name = param.String(default="John Doe")
    profile_image = param.String(default="https://mui.com/static/images/avatar/1.jpg")
    avatar_size = param.Selector(objects=["small", "medium", "large"], default="medium")
    avatar_variant = param.Selector(objects=["rounded", "square"], default="rounded")

    def create_profile_card(self):
        avatar = pmui.Avatar(
            content=self.param.profile_image,
            alt_text=self.param.user_name,
            size=self.param.avatar_size,
            variant=self.param.avatar_variant,
        )

        name_text = pmui.Typography(
            object=self.param.user_name,
            variant="h6",
        )

        return pmui.Card(
            pmui.Row(
                avatar,
                pmui.Column(
                    name_text,
                    pmui.Typography(object="Software Developer", variant="body2"),
                    margin=(0, 20),
                ),
                margin=20,
            ),
            width=300, collapsible=False,
        )

profile = UserProfile()

controls = pn.Param(
    profile,
    parameters=['user_name', 'avatar_size', 'avatar_variant'],
    widgets={
        'user_name': pmui.widgets.TextInput,
        'avatar_size': pmui.widgets.RadioButtonGroup,
        'avatar_variant': pmui.widgets.RadioButtonGroup,
    },
    width=300,
)

pn.Row(profile.create_profile_card(), controls)
```

### API Reference


```python
pmui.Avatar(content="https://mui.com/static/images/avatar/1.jpg").api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using components
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Avatar:**

- [Material UI Avatar Reference](https://mui.com/material-ui/react-avatar/) - Complete documentation for the underlying Material UI component
- [Material UI Avatar API](https://mui.com/material-ui/api/avatar/) - Detailed API reference and configuration options
