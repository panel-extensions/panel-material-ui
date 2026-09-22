```python
import panel as pn
import panel_material_ui as pmui

pn.extension()
```

The `StepperMenu` component is part of the `Menu` family of components. Like other menus it is driven by a declarative list of `items` and reports the user's position via the `active` and `value` parameters. It displays progress through a sequence of numbered steps and comes in two variants: a labelled `standard` strip and a `compact` mobile-style bar.

## Item Structure

In its simplest form each item is just a string label. For more control an item may be a dictionary with the following keys:

- **`label`** (str, required): The text displayed for the step.
- **`icon`** (str, optional): An icon name (or inline SVG) shown for pending steps.
- **`active_icon`** (str, optional): Icon shown when the step is active or completed. Falls back to the filled version of `icon` when not provided.
- **`completed`** (bool, optional): Whether the step is marked complete.
- **`error`** (bool, optional): Whether the step is in an error state.
- **`optional`** (bool, optional): Whether to show an "Optional" caption under the label.
- **`disabled`** (bool, optional): Whether the step is disabled.
- **`tooltip`** (str, optional): Tooltip text shown when hovering over the step.

When one of the `items` is selected it becomes available on the `value` parameter. Since only the allowed keys are synced to the frontend, other information can be stored in the item dictionaries.

## Parameters:

### Core

* **`active`** (`int`): The index of the currently active step.
* **`items`** (`list`): List of step items.
* **`value`** (`dict`): The currently selected item.

##### Display

* **`color`** (str): The color of the active and completed steps.
* **`variant`** (str): The stepper variant, one of `'standard'` or `'compact'`.
* **`alternative_label`** (bool): Place the label below the step icon (standard variant).
* **`connector`** (bool): Whether to display the connector line between steps (standard variant).
* **`non_linear`** (bool): Whether steps can be clicked to navigate non-linearly (standard variant).
* **`orientation`** (str): The orientation of the steps, one of `'horizontal'` or `'vertical'` (standard variant).
* **`indicator`** (str): The progress indicator in the compact variant, one of `'dots'`, `'progress'`, or `'text'`.
* **`position`** (str): Positioning of the bar in the compact variant, one of `'bottom'`, `'static'`, or `'top'`.
* **`back_text`** (str): Label for the back button (compact variant).
* **`next_text`** (str): Label for the next button (compact variant).

##### Styling

- **`sx`** (dict): Component level styling API.
- **`theme_config`** (dict): Theming API.

#### Methods

- **`next`**: Advance to the next step.
- **`back`**: Return to the previous step.
- **`reset`**: Reset to the first step.
- **`on_click`**: Register a callback executed when a step is clicked.
- **`remove_on_click`**: Remove a previously registered click callback.

---


### Basic Usage

At its simplest, pass a list of string labels. The `active` parameter (a zero-based index) controls which step is highlighted:



```python
stepper = pmui.StepperMenu(items=['Account', 'Shipping', 'Payment', 'Review'], active=1)

stepper
```

Steps before the active one are automatically marked as completed (shown with a check), the active step is highlighted, and later steps are greyed out.

The current position is reflected on both the `active` (index) and `value` (item) parameters:



```python
print(f'Active: {stepper.active}')
print(f'Value:  {stepper.value}')
```

### Navigation

The `next`, `back` and `reset` methods move between steps from Python. To react to step changes, watch the `active` parameter with `.param.watch`:



```python
stepper = pmui.StepperMenu(items=['Account', 'Shipping', 'Payment', 'Review'])

log = pmui.Column('# Step Changes')
stepper.param.watch(lambda e: log.append(f'Moved to step {e.new}'), 'active')

back = pmui.Button(label='Back')
back.on_click(lambda e: stepper.back())

forward = pmui.Button(label='Next')
forward.on_click(lambda e: stepper.next())

pmui.Column(
    stepper,
    pmui.Row(back, forward),
    log,
)
```

By default the stepper is linear and the steps are not clickable. Set `non_linear=True` to let users click a step to jump directly to it:



```python
pmui.StepperMenu(items=['Account', 'Shipping', 'Payment', 'Review'], non_linear=True)
```

### Step States

Switching from string labels to dictionaries lets each step declare its own state via the `completed`, `error`, `optional` and `disabled` keys:



```python
pmui.StepperMenu(
    items=[
        {'label': 'Account', 'completed': True},
        {'label': 'Shipping', 'completed': True},
        {'label': 'Payment', 'error': True},
        {'label': 'Review', 'optional': True},
        {'label': 'Confirm', 'disabled': True},
    ],
    active=2,
    non_linear=True,
)
```

### Icons

Add an `icon` to a step (any [Material Icon](https://fonts.google.com/icons) name) to replace the default numbered circle. The active and completed steps show the icon filled and in the active color, while pending steps show it outlined and greyed — so the current step stays clear:



```python
pmui.StepperMenu(
    items=[
        {'label': 'Account', 'icon': 'person'},
        {'label': 'Shipping', 'icon': 'local_shipping'},
        {'label': 'Payment', 'icon': 'payment'},
        {'label': 'Review', 'icon': 'check_circle'},
    ],
    active=1,
    non_linear=True,

)
```

Provide an `active_icon` to use a different icon once a step becomes active or completed. If omitted, the filled version of `icon` is used automatically:



```python
pmui.StepperMenu(
    items=[
        {'label': 'Cart', 'icon': 'shopping_cart', 'active_icon': 'shopping_cart_checkout'},
        {'label': 'Address', 'icon': 'home', 'active_icon': 'where_to_vote'},
        {'label': 'Done', 'icon': 'task_alt'},
    ],
    active=1,
    non_linear=True,
)
```

### Driving a View

Because only the allowed keys are synced to the frontend, you can store arbitrary data on each item (such as a `view`) and use a reactive reference to the `value` to render the content for the active step:



```python
stepper = pmui.StepperMenu(
    items=[
        {'label': 'Welcome', 'icon': 'waving_hand', 'view': pmui.Typography('# Welcome 👋')},
        {'label': 'Configure', 'icon': 'settings', 'view': pmui.Typography('# Configure your settings ⚙️')},
        {'label': 'Finish', 'icon': 'flag', 'view': pmui.Typography('# All done! 🎉')},
    ],
    active=0,
    non_linear=True,
)

pmui.Column(
    stepper,
    stepper.rx()['view'],
)
```

### Vertical Orientation

Set `orientation='vertical'` to stack the steps from top to bottom, which suits narrow layouts such as a sidebar. It applies to the `standard` variant; icons, connectors and step states behave just as they do horizontally:



```python
pmui.StepperMenu(
    items=[
        {'label': 'Account', 'icon': 'person'},
        {'label': 'Shipping', 'icon': 'local_shipping'},
        {'label': 'Payment', 'icon': 'payment'},
        {'label': 'Review', 'icon': 'check_circle'},
    ],
    orientation='vertical',
    active=1,
    non_linear=True,
)
```

### Compact Variant

Set `variant='compact'` for a minimal, mobile-style bar with back/next buttons. Step labels are not shown in this mode; the number of steps is derived from the number of `items`. Choose the indicator style with `indicator` (`'dots'`, `'progress'`, or `'text'`):



```python
items = ['Account', 'Shipping', 'Payment', 'Review']

pmui.Column(
    pmui.StepperMenu(items=items, variant='compact', indicator='dots'),
    pmui.StepperMenu(items=items, variant='compact', indicator='progress'),
    pmui.StepperMenu(items=items, variant='compact', indicator='text'),
)
```

The button labels can be customized with `back_text` and `next_text`:



```python
pmui.StepperMenu(items=items, variant='compact', indicator='progress', back_text='Prev', next_text='Forward')
```

### Color Options

The `color` parameter sets the color of the active and completed steps:



```python
pmui.Column(*(
    pmui.StepperMenu(items=['Account', 'Shipping', 'Payment', 'Review'], color=color, active=1, margin=10)
    for color in pmui.StepperMenu.param.color.objects
))
```

### API Reference

#### Parameters

The `StepperMenu` menu exposes a number of options which can be changed from both Python and Javascript. Try out the effect of these parameters interactively:



```python
pmui.StepperMenu(items=['Account', 'Shipping', 'Payment', 'Review']).api(jslink=True)
```

### References

**Panel Documentation:**

- [How-to guides on interactivity](https://panel.holoviz.org/how_to/interactivity/index.html) - Learn how to add interactivity to your applications using widgets
- [Setting up callbacks and links](https://panel.holoviz.org/how_to/links/index.html) - Connect parameters between components and create reactive interfaces
- [Declarative UIs with Param](https://panel.holoviz.org/how_to/param/index.html) - Build parameter-driven applications

**Material UI Stepper:**

- [Material UI Stepper Reference](https://mui.com/material-ui/react-stepper/) - Complete documentation for the underlying Material UI component
- [Material UI Stepper API](https://mui.com/material-ui/api/stepper/) - Detailed API reference and configuration options

