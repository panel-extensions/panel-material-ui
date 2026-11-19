# Compiled parity matrix

The UI suite takes a `--compiled` flag (see `tests/conftest.py`) that wraps whatever a test passes to `serve_component` in `Compiled`. With `PMUI_COMPILED_REPORT=<path>` set, each test also writes one JSON line with what was compiled, what fell back and what the browser logged.

    pytest tests/ui --ui -n 8                # classic
    pytest tests/ui --ui -n 8 --compiled     # every served component wrapped

Run against Panel origin/main plus the three shelved shadow-free fixes, 955 tests (the ten `Compiled` tests excluded).

| Run | Passed | Failed |
| --- | --- | --- |
| Classic | 951 | 4, all flaky or already failing (two `Feed` scroll tests, `test_onload_notification`, `test_tab_menu_selection`) |
| Compiled, as the branch stood | 872 | 83 |
| Compiled, with the class name restored on the host | 924 | 31 on the full run, 27 of them consistent and specific to `Compiled` |

Of the 955 tests, 756 serve a component that is not opted in, so the root is a fallback; 122 compile fully; 77 are a compiled container with fallback children.

## Causes

| Cause | Tests | Path | Examples | Size of fix |
| --- | --- | --- | --- | --- |
| Stand-in: host lacked the kebab-cased class name (`.button`, `.select`) that Panel puts on the content element | 48 | compiled | `test_select_*` (29), `test_checkbox_*` (13), `test_text_input_variant` | Fixed in this commit, one line |
| Styling and scoping: theme state does not flow through compiled nodes | 9 | compiled | `test_python_component_change_switches_page`, `test_explicit_dark_component_switches_siblings`, `test_page_theme_config_header_color`, `test_page_header_color_primary_inverts_header_components` | Medium. `data.setv` is missing (the `ThemeToggle` crash), `dark_theme` set by one node is not synced to siblings or back to Python, a `theme_config` change on a compiled `Page` does not re-theme, and the header's inverted theme does not reach compiled children |
| Sizing: a fallback at the root is not stretched | 8 | fallback | `test_flexbox_stretches_width_by_default`, `test_badge_fills_responsive_child`, `test_float_panel_size_and_smallified` | Small. `Compiled` takes its own sizing from a compiled root only, so with a fallback root it stays `fit-content` |
| Events: Python to JS messages never arrive | 6 | compiled | `test_button_focus`, `test_select_focus`, `test_slider_focus` | Small. `_send_msg` needs routing to the owning `Compiled` as a `node_msg`, which the runtime already listens for |
| Styling: theme under a fallback root | 2 | fallback | `test_page_inline_theme_toggle_scoped`, `test_unmanaged_explicit_minimal_figure` | Small to medium. The `Compiled` root acts as an extra themed ancestor: it installs the page style and its default `theme_config` sits above the fallback's |
| Test reaches for a per-component Bokeh model | 2 | compiled | `test_render_error_is_contained_and_recovers`, `test_slider_sends_trailing_drag_value_on_unmount` | Not a rendering bug as such, but the same gap as `_models` users in general; the behaviour behind both tests (error boundary reset, flush on unmount) is untested under `Compiled` |
| Flaky under `Compiled` only | 3 | mixed | `test_float_panel_drag_and_content`, `test_tree_checkbox_selection`, `test_bokeh_toolbar_stylesheets_do_not_grow` (the last one logs the `setv` crash) | Unknown until the above are fixed |

No test failed because of sizing or layout of a compiled node, and none failed on a compiled node's own events from the browser.

## Does the fallback path work?

Yes, with two exceptions. Of the 756 tests whose root falls back, 746 pass. The ten that fail are the eight root sizing tests and the two theme tests above. Every one of the 81 component classes served as a fallback root renders and passes its behavioural tests; the failures are in `FlexBox`, `Badge`, `Clickable`, `Skeleton`, `Tooltip`, `FloatPanel` (root sizing) and a `pn.Column` and `Row` with `theme_config` (theme). Fallbacks nested under a compiled container pass 73 of 77, the four failures being theme tests.

## Components

Coverage per opted-in class in compiled form (tests passed / failed): `Page` 53/3, `Select` 38/1, `Button` 26/10, `TextInput` 19/1, `Checkbox` 16/1, `IntSlider` 16/1, `Column` 15/5, `Card` 14/0, `Switch` 2/1, `Row` 1/4, `FloatSlider` 1/1, `Paper` 1/0, `Typography` 0/0. The failures are all the shared theme and `focus()` gaps, not anything specific to a class.

**Compiled-safe today**, apart from those shared gaps: `Button`, `Checkbox`, `Switch`, `TextInput`, `IntSlider`, `FloatSlider`, `Select`, `Column`, `Row`, `Card`, `Paper`, `Page`. Caveats the suite cannot see: `Typography`, `Paper`, `Row` and `FloatSlider` have almost no compiled coverage; `Select` renders `select-label-undefined` ids because the stand-in has no `model.id`; `Card` and `Paper` ask for child flex through `get_child_view`, which returns nothing for compiled children (tests mostly give them fallback children).

**Fixable**, meaning the contract audit found only supported members or small stand-in additions (`model.id`, event payloads, `get_child_view` for one child). Classified from the audit, not yet tried:
- Buttons and toggles: `Fab`, `IconButton`, `Toggle`, `ToggleIcon`, `SplitButton`, the button groups.
- Inputs: `IntInput`, `FloatInput`, `PasswordInput`, `TextAreaInput`, `AutocompleteInput`, `FileInput`, `CheckBoxGroup`, `RadioBoxGroup`, `Rating`, `ColorPicker`, the date and time pickers.
- Sliders and selects: range, editable and discrete sliders, `MultiSelect`, `MultiChoice`, `ColorMap`.
- Menus and indicators: `MenuList`, `MenuButton`, `MenuToggle`, `MenuBar`, `Breadcrumbs`, `Pagination`, `SpeedDial`, `StepperMenu`, `TabMenu`, `Tree`, `Chip`, `Avatar`, progress indicators.
- Wrappers and simple containers: `Badge`, `Tooltip`, `Clickable`, `Skeleton`, `Container`, `Tabs`, `Accordion`, `AppBar`, `Backdrop`, `FlexBox`.

**Hard**, because they treat `view.el` or `view.container` as their own element, depend on Bokeh layout calls, or need a Bokeh model:
- `Drawer`, `Details`, `FloatPanel`, `Dialog`, `Popup` (own host sizing and overlays).
- `Feed`, `ChatFeed`, `ChatInterface`, `ChatMessage`, `ChatStep`, `ChatAreaInput` (shadow-root walks, dotted state, `invalidate_layout`).
- `Grid`, `NotificationArea`, `FileDownload`, `Player`, `ThemeToggle`, a nested `Page`.
- Any instance with `loading`, `description`, `attached`, `theme_config`, scroll options or a `jslink`, which fall back per instance today.

## After the component interface

Run on plain Panel origin/main, without the shelved shadow-free fixes, which `Compiled` does not need: the earlier run repeats there within flake noise (917 to 924 of 955 across runs, every difference passing on rerun).

| Run | Before | After |
| --- | --- | --- |
| Classic, 955 tests | 951 passed | 952 passed; with the 36 new tests 988 of 991 |
| `--compiled`, 955 tests | 924 passed, 27 consistent failures specific to `Compiled` | 933 to 935 passed, 6 consistent failures specific to `Compiled`, three of them in how the test looks |

The three classic failures are the two known ones and `test_float_panel_drag_and_content`, which fails at the same rate on origin/main when run under load (8 and 11 of 24 repeats there, 7 and 14 here).

Closed since the first matrix: root fallback sizing (6 of 8), `focus()` and other messages from Python (6), all nine theme tests on compiled nodes, and both theme tests under a fallback root.

What still fails consistently with `--compiled`:

| Test | Cause |
| --- | --- |
| `test_float_panel_size_and_smallified`, `test_float_panel_resizes_from_right_bottom_anchor` | A `FloatPanel` as fallback root does not grow when resized. It collapses its own box to 0px, and the `Compiled` box around it now copies its sizing. Not diagnosed further |
| `test_invalid_theme_config_falls_back_and_recovers` | A `theme_config` changed after render on a child that falls back: the theme is rebuilt with the new color, but the CSS variables the button reads are not. An initial `theme_config` works |
| `test_unmanaged_root_does_not_style_host_document` | The behaviour is right (styles go into the fallback root's shadow root), the test only looks one shadow root deep |
| `test_render_error_is_contained_and_recovers`, `test_slider_sends_trailing_drag_value_on_unmount` | The tests reach for a per-component Bokeh model through `_models` |

Also found on the way: patches made inside one Bokeh `hold` were collapsed into the last one, which forced a full resync. A patch now carries the earlier ones of the same hold.
