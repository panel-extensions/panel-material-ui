import time

import panel as pn
import panel_material_ui as pmui

pn.extension()

args = pn.state.session_args
mode = args.get("mode", [b"classic"])[0].decode()
rows = int(args.get("rows", [b"35"])[0])
kw = {"use_shadow_dom": False} if mode == "noshadow" else {}

t0 = time.perf_counter()
status = pmui.Typography("clicks: 0", css_classes=["status"], **kw)
count = {"n": 0}

def bump(event):
    count["n"] += 1
    status.object = f"clicks: {count['n']}"

items = [status]
for i in range(rows):
    button = pmui.Button(label=f"Run {i}", css_classes=[f"btn-{i}"], **kw)
    button.on_click(bump)
    items.append(pmui.Row(
        pmui.Typography(f"Row {i}", width=80, **kw),
        pmui.TextInput(label="Name", value=f"value {i}", width=180, **kw),
        pmui.IntSlider(label="Level", value=i % 10, start=0, end=10, width=180, **kw),
        pmui.Checkbox(label="On", value=bool(i % 2), **kw),
        pmui.Select(label="Kind", options=["a", "b", "c"], value="a", width=140, **kw),
        button,
        **kw,
    ))
layout = pmui.Column(*items, **kw)
if mode == "compiled":
    layout = pmui.Compiled(layout)
print(f"BENCH construct mode={mode} rows={rows} {1e3 * (time.perf_counter() - t0):.1f}ms", flush=True)
layout.servable()
