import json, statistics, sys, time
import panel as pn
import panel_material_ui as pmui
from bokeh.document import Document

pn.config.inline = False

def build(mode, rows):
    kw = {"use_shadow_dom": False} if mode == "noshadow" else {}
    status = pmui.Typography("clicks: 0", **kw)
    items = [status]
    for i in range(rows):
        items.append(pmui.Row(
            pmui.Typography(f"Row {i}", width=80, **kw),
            pmui.TextInput(label="Name", value=f"value {i}", width=180, **kw),
            pmui.IntSlider(label="Level", value=i % 10, start=0, end=10, width=180, **kw),
            pmui.Checkbox(label="On", value=bool(i % 2), **kw),
            pmui.Select(label="Kind", options=["a", "b", "c"], value="a", width=140, **kw),
            pmui.Button(label=f"Run {i}", **kw), **kw))
    layout = pmui.Column(*items, **kw)
    return (pmui.Compiled(layout) if mode == "compiled" else layout), status

def main():
  for rows in (35, 100):
      for mode in ("classic", "compiled"):
          c, m, u, size, nmodels = [], [], [], 0, 0
          for _ in range(5):
              t0 = time.perf_counter(); layout, status = build(mode, rows); t1 = time.perf_counter()
              doc = Document(); doc.add_root(layout.get_root(doc)); t2 = time.perf_counter()
              size = len(json.dumps(doc.to_json(), default=str)); nmodels = len(doc.models)
              t3 = time.perf_counter()
              for k in range(20): status.object = f"clicks: {k}"
              t4 = time.perf_counter()
              c.append(1e3*(t1-t0)); m.append(1e3*(t2-t1)); u.append(1e3*(t4-t3)/20)
          med = statistics.median
          print(f"{mode:9s} rows={rows:3d} construct={med(c):7.1f}ms models={med(m):7.1f}ms doc={size/1024:7.0f}KB bokeh_models={nmodels:5d} one_update={med(u):6.2f}ms")

if __name__ == '__main__':
    main()
