```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `Pagination` component provides a convenient way to navigate between a number of consecutive pages.

## Parameters:

### Core

* **`count`** (`int`): The total number of pages
* **`disabled`** (`boolean`): Whether the menu is disabled.
* **`value`** (`dict`): The currently selected page.

##### Display

* **`boundary_count`** (`int`): The number of boundary pages to show
* **`color`** (`str`): The color variant of the paginator, which must be one of `'default'` (white), `'primary'` (blue), `'success'` (green), `'info'` (yellow), `'light'` (light), or `'danger'` (red).
* **`shape`** (`Literal["circular", "rounded"]`): The direction the menu opens in.
* **`sibling_count`** (`int`): The number of sibling pages to show
* **`show_first_button`** (`boolean`): Whether to show button to navigate to first page.
* **`show_last_button`** (`boolean`): Whether to show button to navigate to last page.
* **`size`** (`Literal["small", "medium", "large"]`): The size of the pagination menu.

##### Styling

- **`sx`** (`dict`): Component level styling API.
- **`theme_config`** (`dict`): Theming API.

---

The `Pagination` component allows selecting between a `count` of Pages.


```python
pagination = pmui.Pagination(count=100)

pagination
```

While the display uses 1-baseed indexing, clicking on a particular page will set the 0-indexed `value`:


```python
pagination.value
```

If you have a list of objects that you want to `paginate` you can create a pagination with the `Pagination.paginate` method, providing the list of objects, a `page_size` and optionally the `layout` for the paginated view:


```python
pmui.Pagination.paginate([f'Item: {i}' for i in range(1, 101)], page_size=5)
```

### Display

#### `color`


```python
pn.GridBox(*(
    pagination.clone(color=color)
    for color in pmui.Pagination.param.color.objects
), ncols=2)
```

#### `shape`


```python
pmui.Row(*(
    pagination.clone(shape=shape)
    for shape in pmui.Pagination.param.shape.objects
))
```

#### `show_first_button`/`show_last_button`


```python
pmui.Pagination(count=100, show_first_button=True, show_last_button=True)
```

#### `size`


```python
pmui.Column(*(
    pagination.clone(size=size)
    for size in pmui.Pagination.param.size.objects
))
```

#### `variant`


```python
pmui.Row(*(
    pagination.clone(variant=variant)
    for variant in pmui.Pagination.param.variant.objects
))
```

### Icon Labels

Material icon tokens like `:material/zoom_out_map:` render as icons in labels and option labels.


```python
items = [
    {"label": ":material/zoom_out_map: Page 1"},
    {"label": ":material/zoom_out_map: Page 2"},
    {"label": ":material/zoom_out_map: Page 3"},
]

pmui.Pagination(count=len(items), label=":material/zoom_out_map: Pages")
```

### API Reference

#### Parameters

The `Pagination` exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:


```python
pmui.Pagination().api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Pagination:**

- [Material UI Button Reference](https://mui.com/material-ui/react-pagination) - Complete documentation for the underlying Material UI component
- [Material UI Button API](https://mui.com/material-ui/api/pagination/) - Detailed API reference and configuration options
