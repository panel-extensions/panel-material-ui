# Contract audit: what PMUI components use from `model`, `view` and `el`

Scope: all 80 `.jsx`/`.js` sources under `src/panel_material_ui` on `feat/compiled-tree` (excluding `dist/` and `Compiled.jsx` as a consumer), plus the `ThemedTransform`, `LoadingTransform` and `TooltipTransform` wrappers in `base.py`. Every entry below comes from a grep hit; paths are relative to `src/panel_material_ui`. The real side was read from `panel/models/reactive_esm.ts` and `react_component.ts` in the Panel worktree. The "compiled today" column comes from reading `Compiled.jsx`. The parity run (see `parity.md`) confirmed three of the gaps directly: the missing `data.setv`, Python to JS messages, and tests that need a Bokeh model per component. The rest are predictions from reading, since the suite mostly serves one component per test and so rarely nests compiled children.

Render signatures in use: `{model, view}` (24 files), `{model, el, view}` (24), `{model}` (16), `{model, el}` (2). Five widgets destructure `data` out of props only to discard it (`ToggleIcon`, `SplitButton`, `FileInput`, `ToggleButton`, `FileDownload`), so `data` is not part of the contract in practice.

## 1. API surface

### The `model` proxy

| Member | Real side | PMUI use | Compiled today |
| --- | --- | --- | --- |
| `model.useState(name)` | React hook over `model.data` attribute, returns `[value, setter]`; throws `ReferenceError` on unknown names; event properties get special handling | 792 calls in 79 files, e.g. `widgets/Button.jsx`, `layout/Card.jsx`; also `base.py:257` (`loading`), `base.py:305` (`description`) | Yes for flat names. Unknown names return `undefined` instead of throwing. |
| `model.useState("a.b")` dotted path | Walks nested data models | `chat/ChatMessage.jsx:82-94` (7 calls on `_internal_state.*`) | No. Looks up the literal key `"_internal_state.multi_user"` in props. |
| `model.get_child(name)` | Returns React elements, one `Child` per model, re-rendered through `on_child_render` | 41 calls in 28 files, e.g. `layout/Box.jsx`, `template/Page.jsx`, `wrappers/Badge.jsx:21`; `base.py:219` (`attached`) | Yes. Flex direction of children is hard-coded per kind (`Row`, `Column`, `Page`); other containers get none, see `apply_flex` below. |
| `model.send_msg(data)` | `DataEvent` to Python `_handle_msg` | 38 calls in 20 files, e.g. `chat/ChatArea.jsx:332`, `chat/ChatMessage.jsx:343` | Yes, routed as `{type: "msg", id, data}`. |
| `model.send_event(name, event)` | Serializes the DOM event into a `DOMEvent` | 15 calls in 13 files, e.g. `widgets/Button.jsx:49`, `widgets/TextField.jsx:40`, `widgets/Avatar.jsx:41` | Partial. The event payload is dropped; only the name reaches Python. |
| `model.on/off("msg:custom", cb)` | Python `_send_msg` to JS | 36 files, e.g. `widgets/Select.jsx`, `widgets/FileInput.jsx`, `layout/Feed.jsx` | No. The runtime listens for `node_msg`, but Python never sends one: `_send_msg` on a compiled component has no model to send through. Confirmed by the six `focus()` tests in the parity run. |
| `model.on/off("lifecycle:update_layout", cb)` | Fired from the view's `update_layout` | 12 files: `layout/{Box,Card,Container,Details,Drawer,Feed,MaterialWrapper,Paper,Popup}.jsx`, `template/{Page,AppBar}.jsx`, `chat/ChatArea.jsx:266` | No. The name is registered as a property watcher that never fires. Mostly harmless because the handlers only call `apply_flex`, but any other work in them is skipped. |
| `model.on/off("remove", cb)` | Lifecycle handler on view removal | `chat/ChatArea.jsx:267` | No, never fires. |
| `model.on/off("change:data", cb)` | `change:` prefix is stripped, then a property watcher | `widgets/FileDownload.jsx:103` | No. The prefix is not stripped, so auto-download never triggers. |
| `model.on/off(prop or [props], cb)` | Property watcher | `utils.js:1513` (`theme_config`, `header_color` via `view.model_proxy`), `utils.js:1585` (`dark_theme`) | Yes on the component proxy. Not reachable through `view.model_proxy`, see below. |
| `model.esm_constants` | Bokeh model property | 12 files, e.g. `widgets/Slider.jsx:87-91`, `layout/Box.jsx:15`; `base.py:258` | Yes. |
| `model.<data prop>` direct read | `model.data[name]` | e.g. `model.description` (27), `model.min_height`, `model.height`, `model.filename`, `model.theme_config` (`template/Page.jsx:525`) | Yes for data props. Layout params (`height`, `min_height`, `width`, `sizing_mode`) live in `node.layout`, not `node.props`, so `layout/Details.jsx:69`, `layout/Container.jsx:29` and `layout/FloatPanel.jsx:131` read `undefined`. |
| `model.<child prop>` direct read | Bokeh child models with `.id`, `.class_name`, `.data`, `.sizing_mode` | `model.objects` (32), `model.header` (13), `model.main`, `model.sidebar`, `model.rail`, `model.contextbar`, `model.footer_objects`, `model.object` | Partial. Returns raw tree nodes: `.id` works, but `.sizing_mode` (`layout/Details.jsx:65`, `template/Page.jsx:524`), `.class_name` and `.data.*` (`layout/Grid.jsx:34-41`) are `undefined`. |
| `model.id` | Bokeh model id | 7 files: `widgets/Select.jsx:542-606`, `widgets/MultiSelect.jsx:61-87`, `widgets/ColorMap.jsx:35` | No. The proxy has no `id`, so label ids become `select-label-undefined` and collide across instances. `Select` is opted in today. |
| `model.class_name` | Bokeh model property | `base.py:223` (only when `is_root`) | No (`undefined`); unreachable today because `is_root` is false. |
| `model.js_events` | Bokeh model property | `NotificationArea.jsx:126` | No. |
| `model.useMount` | Hook over `lifecycle:mounted` | Not used by PMUI | n/a |

### The `view` object

| Member | Real side | PMUI use | Compiled today |
| --- | --- | --- | --- |
| `view.get_child_view(model)` | Child Bokeh view | 39 calls in 15 files, always as `apply_flex(view.get_child_view(...))` except `wrappers/Badge.jsx:26` | Partial. Returns the real view for fallback children and `null` for compiled ones. |
| child view `.box_sizing()`, `.parent_style.replace/append` | Bokeh layout API | `utils.js:1665-1699` (`apply_flex`), `wrappers/Badge.jsx:28` | Only for fallback children. Compiled children are sized by `hostLayout` in the runtime, which duplicates `apply_flex` and only knows `Row`, `Column` and `Page`. `Card`, `Paper`, `Details`, `Drawer`, `Container`, `Tabs`, `AppBar`, `Feed`, `ChatStep` ask for a direction that the runtime does not apply. Badge's margin reset is skipped. |
| `view.container` | The component's own content div | 9 files: overlay anchoring in `layout/{Dialog,Popup}.jsx`, `widgets/{TimePicker,DateTimePicker,DateRangePicker,SpeedDial}.jsx`, `utils.js:1081,1115`; DOM writes in `widgets/FileDownload.jsx:74`; query in `chat/ChatArea.jsx:242`; theme class in `utils.js:1447` | Partial. It is the shared root container. Overlay anchoring works. `querySelector("textarea")` finds the first textarea in the whole tree. The `mui-dark`/`mui-light` class is written to the shared container by every node, so mixed themes fight. |
| `view.el` | The component's host element | 6 files: size writes in `layout/Drawer.jsx:107-145`, `layout/Details.jsx:71`, `layout/FloatPanel.jsx:110-112`; `getBoundingClientRect` in `layout/FloatPanel.jsx:34`; ancestor walks in `menu.jsx:11`, `chat/ChatMessage.jsx:182`; `template/Page.jsx:48` | Partial. Also the shared root container, so size writes resize the whole compiled root. Ancestor walks work. `Page` works through the `compiled_root` special case. |
| `view.shadow_el` | Shadow root | `utils.js:1360,1569,1597` (theme style element), `description.jsx:22` via `view.root` | Yes (shared root). |
| `view.parent` | Parent view | `utils.js:142` (`find_on_parent`), `utils.js:1455-1470` (theme config merge), `utils.js:1576` (find the Page), `layout/Grid.jsx:18`, `layout/Popup.jsx:16`, `chat/ChatMessage.jsx:218`, `template/Page.jsx:47` | Yes for walking (`parent`, `.model.class_name`, `.model.data`). |
| `view.parent.child_views`, `view.parent.el` | Bokeh view API | `layout/Popup.jsx:16` | No. A nested stand-in has no `child_views`, so `.includes` throws. |
| `view.parent.model.type` | Bokeh model type | `chat/ChatMessage.jsx:218` | No (`undefined`, so the Feed check is always false). |
| `view.root`, `view.root.mui_cache`, `view.root.model.class_name` | Root view and its emotion cache | `description.jsx:21-23` | Partial. `root` is the `Compiled` view, never a `Page`, so descriptions under a compiled Page take the non-Page branch. |
| `view.model.data.<prop>` | Data model | `utils.js:145`, `utils.js:1456-1466`, `template/Page.jsx:323`, `layout/Feed.jsx:41`, `layout/Tabs.jsx:66`, `chat/ChatMessage.jsx:158` | Yes for props and children (children resolve to the stand-in models). |
| `view.model.data.properties` | Bokeh property map | `base.py:219` (`"attached" in ...`) | Stubbed as `{}`, so `attached` children never render. |
| `view.model.data.setv(...)` | Bokeh setter, used with `{sync: false}` | `utils.js:1536` (followers switching dark mode) | No. The stand-in data object has no `setv`, so `follow_dark_mode` throws for every non-owner node. |
| `view.model.data.change` | Bokeh signal | `utils.js:1626,1630` (error boundary reset) | Stubbed with a no-op, so a boundary that caught an error never resets. |
| `view.model.esm_constants` | Model property | `utils.js:1529` (`session_theme_owner`) | No. The stand-in model has no `esm_constants`, so a compiled `Page` is not treated as the theme owner. |
| `view.model.class_name`, `.id`, `.document` | Model properties | `utils.js:1456,1511,1577,1634`, `NotificationArea.jsx:97,166`, `utils.js:1317,1359` | Yes. |
| `view.model.sizing_mode`, `.tags`, `.dev` | Model properties | `layout/Dialog.jsx:25`, `NotificationArea.jsx:135`, `utils.js:1639` | No (`undefined`). |
| `view.model_proxy.on/off` | The view's own proxy | `utils.js:1513-1517`, `utils.js:1585-1586`, called on ancestor views | No per node. Every stand-in exposes the root `Compiled` proxy, so watching `theme_config` or `dark_theme` on an ancestor node subscribes to the wrong model and never fires. Theme changes instead rely on `theme_revision` forcing a full recompile. |
| `view.is_root` | Bokeh view property | `base.py:221,223` | Always `false`, which is right for nested nodes. |
| `view.invalidate_layout()` | Bokeh layout API | `chat/ChatMessage.jsx:223` | No, throws. |
| class name on the content element | `container.className` is the kebab-cased `class_name` (`.button`, `.select`) | 48 UI tests locate components by it; user CSS may too | Yes, added to the compiled host after the first parity run found it missing. |
| `view.compiled_root` | Compiled only | `template/Page.jsx:46` | A compiled-only member leaking into a component. |

### Other inputs and globals

| Member | Real side | PMUI use | Compiled today |
| --- | --- | --- | --- |
| `el` prop | `view.container` | Passed to `render_description` from 23 widget files; `base.py:315` (tooltip popper container) | Yes for overlay anchoring (shared container). |
| `document.documentElement` `data-theme-managed`, global `dark_mode`, `host_theme` | Page-level theme state | `base.py:220`, `utils.js:1559-1594` | Independent of host. |
| `view.model.document.roots()`, `doc.on_change`, `doc.on_event`, `model.references()` | Bokeh document API | `utils.js:1317,1359-1415`, `NotificationArea.jsx:166-168` | Works through `model.document`, but only sees Bokeh models, which compiled nodes are not. |
| `Bokeh.index.find_one_by_id(model.id)`, `model.setv`, `model.stylesheets =` | Applied to third-party Bokeh models (plots, Tabulator, terminal) when theming | `utils.js:308,705,847-976` | Independent; applies to fallback children only. |
| `window.Bokeh.require("models/formatters")` | BokehJS module access | `widgets/Slider.jsx:235` | Independent. |
| `getRootNode()` / `ShadowRoot.host` walks | Assumes one shadow root per component | `layout/Feed.jsx:74`, `widgets/List.jsx:86`, `utils.js:1014`, `chat/ChatMessage.jsx:195`, `menu.jsx:13` | Resolve to the shared root instead of the component's own host. |

## 2. Components using members the stand-in does not support

Grouped by missing member. JSX file, then Python classes.

- **`lifecycle:update_layout` and per-kind child flex**: `layout/Card.jsx` (Card), `layout/Paper.jsx` (Paper), `layout/Container.jsx` (Container), `layout/Details.jsx` (Details), `layout/Drawer.jsx` (Drawer), `layout/Feed.jsx` (Feed), `layout/MaterialWrapper.jsx` (MaterialWrapper and subclasses), `layout/Popup.jsx` (Popup), `layout/Tabs.jsx` (Tabs), `template/AppBar.jsx` (AppBar), `chat/ChatStep.jsx` (ChatStep), `chat/ChatArea.jsx` (ChatAreaInput). `Card` and `Paper` are opted in today, so their children get no flex rules from the runtime.
- **`view.el` as own host (size writes, bounds)**: `layout/Drawer.jsx` (Drawer), `layout/Details.jsx` (Details), `layout/FloatPanel.jsx` (FloatPanel).
- **`view.container` as own content element**: `chat/ChatArea.jsx` (ChatAreaInput, focus), every themed component with a non-inherited `dark_theme` (`utils.js:1447`).
- **Layout params through the model (`height`, `min_height`, `width`, `sizing_mode`)**: `layout/Details.jsx`, `layout/Container.jsx`, `layout/FloatPanel.jsx`, `layout/Dialog.jsx` (Dialog, via `view.model.sizing_mode`).
- **Child handles with `.sizing_mode`, `.class_name`, `.data`**: `template/Page.jsx:524` (Page, `main_stretch` is always false), `layout/Details.jsx:65`, `layout/Grid.jsx` (Grid), `chat/ChatMessage.jsx:158` (ChatMessage).
- **`model.id`**: `widgets/Select.jsx` (Select, MultiChoice), `widgets/MultiSelect.jsx` (MultiSelect), `widgets/ColorMap.jsx` (ColorMap).
- **`send_event` payload**: `widgets/Avatar.jsx`, `widgets/Chip.jsx`, `widgets/IconButton.jsx`, `widgets/TextField.jsx` (TextInput, opted in), `widgets/TextArea.jsx`, `widgets/PasswordField.jsx`, `widgets/Autocomplete.jsx`. Only matters where Python reads the event data.
- **`change:` prefix, `remove`**: `widgets/FileDownload.jsx` (FileDownload), `chat/ChatArea.jsx`.
- **Dotted `useState`**: `chat/ChatMessage.jsx` (ChatMessage).
- **`view.invalidate_layout`, `view.parent.model.type`**: `chat/ChatMessage.jsx`.
- **`view.parent.child_views`**: `layout/Popup.jsx`.
- **`view.root` being the Page with `mui_cache`**: `description.jsx`, so any widget with a `description` under a compiled Page.
- **`view.model.tags`, `model.js_events`**: `NotificationArea.jsx` (NotificationArea).
- **`attached` children (`data.properties`)**: any component with `attached` set.
- **Theme plumbing (`view.model.data.setv`, `view.model.esm_constants.session_theme_owner`, per-node `view.model_proxy`)**: all components, through `install_theme_hooks`. From reading, a dark mode switch on a theme-managed page calls `setv` on a stand-in that lacks it, for every compiled node, and a compiled `Page` is not recognised as the owner. The existing compiled tests do not toggle dark mode, so this needs a targeted test.

## 3. Proposed interface

The audit shows the real contract is small, and that most of the drift comes from components reaching past it into Bokeh view internals (`view.el.style`, `parent_style`, `box_sizing`, `child_views`, `model.data.setv`, `model_proxy` on ancestors). The proposal is to name the contract, route those reaches through it, and have both hosts implement it.

```ts
interface ComponentModel {
  readonly id: string
  readonly kind: string                       // class_name
  readonly constants: Record<string, unknown> // esm_constants
  useState<T>(path: string): [T, (next: T | ((prev: T) => T)) => void]  // dotted paths allowed, throws on unknown
  get<T>(name: string): T                     // non-reactive read, replaces model.<prop>
  set(values: Record<string, unknown>, opts?: {sync?: boolean}): void   // replaces data.setv
  children(name: string): ChildHandle[]       // replaces model.objects etc.
  render_children(name: string, opts?: {direction?: "row" | "column"}): React.ReactNode[]
  send_msg(data: unknown): void
  send_event(name: string, event?: Event | object): void
  on(event: "msg" | "layout" | "remove" | `change:${string}`, cb: (...args: any[]) => void): () => void
}

interface ChildHandle {
  readonly id: string
  readonly kind: string
  readonly layout: {sizing_mode?: string, width?: number, height?: number, /* policies, margin, align */}
  get<T>(name: string): T
}

interface ComponentHost {
  readonly model: ComponentModel
  readonly parent: ComponentHost | null       // for theme and context walks
  readonly is_root: boolean
  readonly dev: boolean
  readonly host_el: HTMLElement               // this component's own box; safe to style and measure
  readonly content_el: HTMLElement            // this component's own content element; safe to query
  readonly overlay_root: HTMLElement          // where popovers, dialogs and theme styles mount
  readonly style_root: ShadowRoot | Document  // where scoped <style> elements go
  readonly emotion_cache: unknown | null
  readonly layout: ChildHandle["layout"]      // own layout params
  readonly document: unknown                  // Bokeh document, for doc-level events only
  invalidate_layout(): void
  set_host_style(styles: Partial<CSSStyleDeclaration>): void
}
```

`render` would receive `{model, host}`; `view` and `el` stay as aliases during migration.

What goes in is exactly what the tables above show components needing. `render_children` takes the flex direction as an argument, which removes the `apply_flex(view.get_child_view(...))` calls in 15 files, the `lifecycle:update_layout` handlers that exist only to re-run them, and the kind table inside `Compiled.jsx`. The real host implements it with `box_sizing` and `parent_style`; the compiled host with its layout rules. `on` returns an unsubscribe function and uses one naming scheme, which closes the `change:` and lifecycle gaps.

What stays private to Panel: `get_child_view`, `child_views`, `parent_style`, `box_sizing`, `model_proxy`, `shadow_el`, `container`, `style_cache`, `react_root`, `patch_container`, the Bokeh `data` model with its `properties`, `attributes`, `setv` and `change` signal. PMUI code that themes third-party Bokeh models (`apply_bokeh_theme`) keeps using Bokeh directly, since it operates on other models through `host.document`, not on the component.

Migration of the current reaches:

- `view.el.style.*` in Drawer, Details, FloatPanel becomes `host.set_host_style`; `view.el.getBoundingClientRect()` becomes `host.host_el`.
- `view.container` for overlays becomes `host.overlay_root`; for queries and the theme class becomes `host.content_el`.
- `view.shadow_el.insertBefore(style, view.container)` becomes an insert into `host.style_root`.
- `view.root.mui_cache` in `description.jsx` becomes `host.emotion_cache` plus `host.overlay_root`, which removes the Page special case.
- `view.model.data.setv` and `view.model_proxy.on` on ancestors become `host.model.set` and `host.parent.model.on`.
- `model.objects[i].sizing_mode`, `model.class_name` and `model.data.*` on children become `model.children(name)[i].layout` and `.get`.
- `model.height`, `view.model.sizing_mode` become `host.layout`.
- `view.parent?.child_views.includes(view)` in Popup becomes a `host.parent` check plus `host.parent.host_el`.
- `view.compiled_root` in `Page.jsx` goes away once `is_fullscreen` uses `host.is_root` and `host.host_el`.

Where it lives: the interface and the real implementation belong in Panel, next to `react_model_proxy` in `react_component.ts`, because Panel owns the view lifecycle and other ReactComponent libraries would benefit. Until that lands, PMUI can carry an adapter in `utils.js` (`make_host(view, model)`) that builds a `ComponentHost` from a real `ReactComponentView`, and `Compiled.jsx` builds the same shape from its store. Components then import nothing host-specific.

Conformance: one Playwright suite, parametrized over the two hosts, built from small probe components (not PMUI widgets) that each exercise one member: state round trip in both directions, dotted state, unknown-name error, child render and reorder with a direction, child handle layout, message in each direction, event payload, each `on` event and its unsubscribe, host element identity (`host_el` contains the rendered output and nothing of a sibling), host style writes not leaking to siblings, overlay root placement, parent walk, `set` with `sync: false`. The parity matrix flag from step 1 is the second line of defence: it runs real components through both hosts, while the probe suite pins the contract itself. A lint rule or grep check in CI that fails on `view.` access outside the adapter keeps new code from bypassing the interface.

## 4. Notes on later gaps

- **jslink / jscallback**: PMUI calls `jslink` in `base.py:514`, `base.py:747,754` (`controls`, default `jslink=True`), `layout/base.py:1353` (a toggle linked to `open`) and `widgets/base.py:79`; `widgets/icon.py:184` defines `jscallback`. All of these target a Bokeh model per widget, which compiled nodes do not have. Each needs either a fallback or a client-side link op in the tree.
- **Bokeh JS callbacks referencing widget models**: `widgets/player.py:66-69` already opts out of embed because callbacks address `cb_obj.value` on the widget model while the value lives in the nested data model. Compiled nodes are one step further: there is no model to reference at all.
- **`_models` / `get_root` users**: `layout/base.py:42-43,430,472-489,833-844,1113` look up child models by ref, `base.py:393-405` walks `state._views` to find owners and roots, `base.py:556` and `template/base.py:258` gate on `not self._models`, and `template/base.py:344` overrides `get_root`. A compiled child has an empty `_models`, so anything gated on it sees the component as unrendered.
- **Static save / embed**: `base.py:780` and `template/base.py:400` override `save`. The compiled tree is plain JSON in one model, so it should serialize, but `pn.io.embed` state caching works by recording model property changes per widget and has nothing to record here.
- **Notebook comms**: `base.py:393-405` and `_get_model` (`base.py:639-662`) switch bundle loading on `comm`. The patch channel uses a synced param plus `msg:custom`, which should carry over comms, but the `rev` gap and resync path is the part to test, since comm messages can arrive before the view listens.
- **Incremental layout**: sizing is computed in two places, `hostLayout` in `Compiled.jsx` and `apply_flex` in `utils.js`, with the parent's direction known only for `Row`, `Column` and `Page`. Moving the direction into `render_children` (section 3) gives every container a single path, which is also what would let a layout param change become a per-node patch instead of a full recompile.
- **Shadow-root assumptions**: `getRootNode().host` walks in `layout/Feed.jsx:74`, `widgets/List.jsx:86`, `chat/ChatMessage.jsx:195` and `menu.jsx:13` assume one shadow root per component and will resolve to the shared root.
