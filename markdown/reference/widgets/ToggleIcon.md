```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `ToggleIcon` widget allows users to toggle between `True` and `False` states using a sleek icon-based interface. This widget provides the same functionality as the `Checkbox`, `Switch`, and `Toggle` widgets but with a minimalist visual approach that's perfect for space-conscious designs.

Ideal for compact interfaces, toolbar buttons, and situations where you need toggle functionality without taking up much visual space, the `ToggleIcon` widget offers an elegant, icon-only alternative to traditional toggle controls.

#### Parameters

For more details on customization options, see the [customization guides](https://panel-material-ui.holoviz.org/customization/index.html).

##### Core

* **`active_icon`** (str): The icon displayed when the toggle is active. Accepts [Material icon names](https://fonts.google.com/icons) or SVG strings.
* **`disabled`** (bool): When True, the widget becomes non-interactive and appears grayed out.
* **`icon`** (str): The icon displayed when the toggle is inactive. Accepts [Material icon names](https://fonts.google.com/icons) or SVG strings.
* **`value`** (bool): The current state of the toggle (`True` for active, `False` for inactive).

##### Display

* **`icon_size`** (`str`): Controls the size of the icon. Usually automatically determined based on the `size` but can be used to control icon size independently.
* **`label`** (str): Optional text label displayed alongside the icon.
* **`size`** (`Literal["small", "medium", "large"]`): Controls the size of the widget.

##### Styling

* **`color`** (str): The color variant of the icon when active, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`sx`** (dict): Advanced styling options for fine-tuned appearance control.
* **`theme_config`** (dict): Theme-level configuration for consistent styling across your application.

##### Aliases

For seamless compatibility with Panel widgets, certain parameters accept aliases:

* **`name`**: Alternative parameter name for `label`

___

### Basic Usage

Getting started with the ToggleIcon widget is straightforward. Here's how to create a simple toggle icon that changes between two different states:


```python
toggle = pmui.ToggleIcon(icon="add_box")

toggle
```

By default, when `value` is `True`, the `active_icon` is displayed. If no `active_icon` is specified, Material Icons will automatically use the filled version of the icon when available.

The `value` parameter automatically updates to reflect the toggle state: `True` when active, `False` when inactive. You can also programmatically set this value to control the toggle state:


```python
toggle.value
```

You can also add a text label alongside the icon using the `label` parameter for better accessibility and context:


```python
pmui.ToggleIcon(icon="favorite", active_icon="check", label="Favorite")
```

### Using Material Icons

The `ToggleIcon` widget uses [Google's Material Icons](https://fonts.google.com/icons), which provide a consistent, beautiful set of icons following Material Design principles. Icon names use underscores instead of dashes (e.g., `favorite_border`, `thumb_up`, `check_circle`).

Popular icon pairs for toggles include:
- `favorite_border` / `favorite` (for favorites/likes)
- `bookmark_border` / `bookmark` (for bookmarks)
- `visibility_off` / `visibility` (for show/hide)
- `thumb_down` / `thumb_up` (for reactions)

___


```python
pmui.FlexBox(
    pmui.ToggleIcon(icon="favorite_border", active_icon="favorite", label="Favorite"),
    pmui.ToggleIcon(icon="bookmark_border", active_icon="bookmark", label="Bookmark"),
    pmui.ToggleIcon(icon="visibility_off", active_icon="visibility", label="Show/Hide"),
    pmui.ToggleIcon(icon="thumb_down", active_icon="thumb_up", label="Like/Dislike")
)
```

### Icon Customization

The ToggleIcon widget offers intelligent icon selection. When only an `icon` is provided, Material Icons automatically selects the corresponding filled version for the active state:


```python
pmui.ToggleIcon(icon="thumb_down")
```

You can customize this behavior by explicitly setting both icons to create meaningful visual transitions:


```python
pmui.ToggleIcon(icon="thumb_down", active_icon="thumb_up")
```

The icon will automatically adapt to the specified `width`/`height` but you may also provide an explicit `size`:

### Size Options

Choose the appropriate icon size for your interface using the `size` parameter. The icon automatically adapts to your layout, or you can specify explicit sizing:


```python
pmui.ToggleIcon(icon="thumb_down", active_icon="thumb_up", size='small')
```

You may also independently control the `icon_size`:


```python
pmui.ToggleIcon(icon="thumb_down", active_icon="thumb_up", icon_size='30px')
```

### Color Options

Customize your toggle icon's appearance to match your application's design language using the `color` parameter. Each color provides different visual emphasis and semantic meaning:


```python
pmui.ToggleIcon(icon="favorite_border", active_icon="favorite", color="primary", value=True)
```

Here's a showcase of all available color options:


```python
pmui.FlexBox(
    *(pmui.ToggleIcon(icon="favorite_border", active_icon="favorite", label=color, color=color, value=True) 
      for color in pmui.ToggleIcon.param.color.objects)
)
```

### Custom SVG Icons

For complete design control, you can use custom SVG icons instead of the built-in Material icons. This is perfect for brand-specific iconography:


```python
SVG = """
<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-ad-off" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M9 5h10a2 2 0 0 1 2 2v10m-2 2h-14a2 2 0 0 1 -2 -2v-10a2 2 0 0 1 2 -2" /><path d="M7 15v-4a2 2 0 0 1 2 -2m2 2v4" /><path d="M7 13h4" /><path d="M17 9v4" /><path d="M16.115 12.131c.33 .149 .595 .412 .747 .74" /><path d="M3 3l18 18" /></svg>
"""
ACTIVE_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-ad-filled" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M19 4h-14a3 3 0 0 0 -3 3v10a3 3 0 0 0 3 3h14a3 3 0 0 0 3 -3v-10a3 3 0 0 0 -3 -3zm-10 4a3 3 0 0 1 2.995 2.824l.005 .176v4a1 1 0 0 1 -1.993 .117l-.007 -.117v-1h-2v1a1 1 0 0 1 -1.993 .117l-.007 -.117v-4a3 3 0 0 1 3 -3zm0 2a1 1 0 0 0 -.993 .883l-.007 .117v1h2v-1a1 1 0 0 0 -1 -1zm8 -2a1 1 0 0 1 .993 .883l.007 .117v6a1 1 0 0 1 -.883 .993l-.117 .007h-1.5a2.5 2.5 0 1 1 .326 -4.979l.174 .029v-2.05a1 1 0 0 1 .883 -.993l.117 -.007zm-1.41 5.008l-.09 -.008a.5 .5 0 0 0 -.09 .992l.09 .008h.5v-.5l-.008 -.09a.5 .5 0 0 0 -.318 -.379l-.084 -.023z" stroke-width="0" fill="currentColor" /></svg>
"""

pmui.ToggleIcon(icon=SVG, active_icon=ACTIVE_SVG)
```

### Disabled and Loading States

The `ToggleIcon` widget supports both disabled and loading states to provide clear feedback during various application states. Use these features to guide user interactions effectively:


```python
pmui.ToggleIcon(icon="thumb_down", active_icon="thumb_up", disabled=True, loading=True)
```

### Real-World Example: Favorite Toggle

Let's create a practical example that demonstrates how toggle icons work in real applications. This favorite toggle shows how to bind toggle values to dynamic content updates:


```python
import panel as pn
import panel_material_ui as pmui

pn.extension()

favorite_toggle = pmui.ToggleIcon(
    icon="favorite", 
    active_icon="check",
    label="Favorite",
    value=False
)

def create_favorite_status(value):
    if value:
        return "👍 Added to favorites!"
    
    return "❤️ Click the heart to add to favorites"

favorite_status = pn.bind(create_favorite_status, favorite_toggle)

pmui.Column(favorite_toggle, favorite_status)
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
pmui.ToggleIcon(icon="zoom_in", active_icon="zoom_out_map", label=":material/zoom_out_map: Zoom mode")
```

### API Reference

#### Interactive Parameter Explorer

The `ToggleIcon` widget offers numerous customization options that can be modified from both Python and JavaScript. Explore these parameters interactively to see their effects in real-time:


```python
pmui.ToggleIcon(icon="favorite_border", active_icon="favorite", label="ToggleIcon").api(jslink=True)
```

### Further Learning

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Master the art of creating interactive applications with widgets and dynamic updates
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect widget parameters to create responsive, reactive user interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build sophisticated parameter-driven applications with minimal code

**Material Icons:**

- [Material Icons Library](https://fonts.google.com/icons) - Browse the complete collection of beautiful, customizable icons used by the `ToggleIcon` widget
