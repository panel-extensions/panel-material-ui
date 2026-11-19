import json
import statistics
import sys

from playwright.sync_api import sync_playwright

RUNS = int(sys.argv[1]); OUT = sys.argv[2]
PAGES = {"home": "", "components": "components", "fleet_overview": "dash/503bc715136e", "performance_alerts": "dash/777663fbcaaa", "market_revenue": "dash/9a5f8b3e4141"}
MODES = {"classic": 5131, "compiled": 5132}
INIT = """
window.__m = {count: 0, last: 0, first_content: null}
const seen = new WeakSet()
const note = () => { window.__m.count++; window.__m.last = performance.now() }
const watch = (root) => new MutationObserver((records) => { for (const r of records) { note(); for (const n of r.addedNodes) hook(n) } }).observe(root, {childList: true, subtree: true, attributes: true, characterData: true})
const hook = (n) => { if (n.nodeType !== 1) return; for (const el of [n, ...n.querySelectorAll('*')]) { if (el.shadowRoot && !seen.has(el.shadowRoot)) { seen.add(el.shadowRoot); watch(el.shadowRoot); for (const c of el.shadowRoot.children) hook(c) } } }
const orig = Element.prototype.attachShadow
Element.prototype.attachShadow = function(o) { const sr = orig.call(this, o); seen.add(sr); watch(sr); return sr }
document.addEventListener('DOMContentLoaded', () => watch(document.body))
"""
COUNT = """() => { let n = 0, s = 0; const walk = (r) => { for (const el of r.querySelectorAll('*')) { n++; if (el.shadowRoot) { s++; walk(el.shadowRoot) } } }; walk(document); const d = Bokeh.documents[0]; return {elements: n, shadow_roots: s, models: d.all_models.size ?? [...d.all_models].length} }"""
def run(browser, port, path):
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}); pg = ctx.new_page()
    cdp = ctx.new_cdp_session(pg); cdp.send("Performance.enable"); cdp.send("Network.enable")
    ws = {"kb": 0}
    cdp.on("Network.webSocketFrameReceived", lambda e: ws.__setitem__("kb", ws["kb"] + len(e["response"]["payloadData"]) / 1024))
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
    pg.add_init_script(INIT)
    pg.goto(f"http://localhost:{port}/{path}")
    # settled: no mutation for 1.5 s
    pg.wait_for_function("() => window.__m && window.__m.count > 50 && performance.now() - window.__m.last > 1500", timeout=60000)
    m = pg.evaluate("window.__m")
    perf = {x["name"]: x["value"] for x in cdp.send("Performance.getMetrics")["metrics"]}
    paint = pg.evaluate("() => (performance.getEntriesByName('first-contentful-paint')[0] || {}).startTime")
    cdp.send("HeapProfiler.collectGarbage")
    perf2 = {x["name"]: x["value"] for x in cdp.send("Performance.getMetrics")["metrics"]}
    counts = pg.evaluate(COUNT)
    ctx.close()
    return dict(settled_ms=m["last"], mutations=m["count"], fcp_ms=paint, script_ms=perf["ScriptDuration"] * 1e3,
        layout_ms=perf["LayoutDuration"] * 1e3, style_ms=perf["RecalcStyleDuration"] * 1e3, task_ms=perf["TaskDuration"] * 1e3,
        heap_mb=perf2["JSHeapUsedSize"] / 1e6, dom_nodes=perf2["Nodes"], ws_kb=ws["kb"], errors=len(errs), **counts)
res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, path in PAGES.items():
        for mode, port in MODES.items(): run(b, port, path)  # warm
        runs = {mode: [] for mode in MODES}
        for i in range(RUNS):
            for mode, port in MODES.items(): runs[mode].append(run(b, port, path))
        for mode in MODES:
            res[f"{name}|{mode}"] = {k: statistics.median(r[k] for r in runs[mode]) for k in runs[mode][0]}
            print(name, mode, {k: round(v, 1) for k, v in res[f"{name}|{mode}"].items()}, flush=True)
    b.close()
json.dump(res, open(OUT, "w"), indent=1)
