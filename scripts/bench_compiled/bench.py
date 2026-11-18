import json, re, statistics, sys
from playwright.sync_api import sync_playwright

PORT = sys.argv[1]
ROWS = [int(r) for r in sys.argv[2].split(",")]
RUNS = int(sys.argv[3])
MODES = ["classic", "noshadow", "compiled"]

CLICK = """([btn, status, want]) => new Promise(res => {
  const t = performance.now()
  const check = () => {
    if (!status.isConnected) { return res(-1) }
    if ((status.shadowRoot ?? status).textContent.includes(want)) { return res(performance.now() - t) }
    if (performance.now() - t > 15000) { return res(-2) }
    setTimeout(check, 1)
  }
  btn.click(); check()
})"""

def patch(route):
    r = route.fetch(); body = r.text()
    route.fulfill(response=r, body=body.replace("setup_style_cache(){", "setup_style_cache(){if(!this.use_shadow_dom)return;"))

def run(browser, mode, rows):
    ctx = browser.new_context(viewport={"width": 1200, "height": 800})
    pg = ctx.new_page()
    cdp = ctx.new_cdp_session(pg); cdp.send("Performance.enable")
    out = {"ws_in": 0, "errors": 0}
    idle = []
    def on_console(m):
        if m.type == "error" and "404" not in m.text: out["errors"] += 1
        if (mt := re.search(r"document idle at (\d+) ms", m.text)): idle.append(int(mt.group(1)))
    pg.on("console", on_console)
    def on_ws(ws):
        ws.on("framereceived", lambda p: out.__setitem__("ws_in", out["ws_in"] + len(p)))
    pg.on("websocket", on_ws)
    pg.route("**/panel.min.js*", patch)
    pg.goto(f"http://localhost:{PORT}/app?mode={mode}&rows={rows}")
    btn = pg.locator(f".btn-{rows-1} button"); btn.wait_for(timeout=120000)
    out["ready_ms"] = pg.evaluate("performance.now()")
    pg.wait_for_timeout(1500)
    m = {x["name"]: x["value"] for x in cdp.send("Performance.getMetrics")["metrics"]}
    out.update(idle_ms=idle[-1] if idle else None, script_ms=1e3*m["ScriptDuration"], layout_ms=1e3*m["LayoutDuration"],
               style_ms=1e3*m["RecalcStyleDuration"], task_ms=1e3*m["TaskDuration"], heap_mb=m["JSHeapUsedSize"]/1e6,
               nodes=m["Nodes"], load_ws_kb=out["ws_in"]/1024)
    status = pg.locator(".status").first
    bh, sh = btn.element_handle(), status.element_handle()
    before = out["ws_in"]; clicks = []
    for i in range(1, 16):
        clicks.append(pg.evaluate(CLICK, [bh, sh, f"clicks: {i}"]))
        pg.wait_for_timeout(60)
    good = [c for c in clicks[3:] if c >= 0]
    out["click_ms"] = statistics.median(good) if good else None
    out["click_fail"] = len([c for c in clicks if c < 0])
    out["click_ws_kb"] = (out["ws_in"] - before) / 1024 / 15
    del out["ws_in"]
    ctx.close()
    return out

res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    run(b, "classic", 5)
    for rows in ROWS:
        for i in range(RUNS):
            for mode in MODES:
                r = run(b, mode, rows)
                res.setdefault((mode, rows), []).append(r)
                print(mode, rows, i, {k: (round(v, 1) if isinstance(v, float) else v) for k, v in r.items()}, flush=True)
    b.close()
summary = {f"{m}|{r}": {k: statistics.median([x[k] for x in v if x[k] is not None] or [float("nan")]) for k in v[0]} for (m, r), v in res.items()}
json.dump(summary, open(f"results_{'_'.join(map(str, ROWS))}.json", "w"), indent=1)
