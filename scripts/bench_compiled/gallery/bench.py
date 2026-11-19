"""
Loads each example app classic and compiled, takes a screenshot of both and
compares load time, memory, DOM size and payload.

    python bench.py <first_port> <runs> <out_dir>

Each app is expected on its own server, on consecutive ports in the order of
APPS, since the branding example changes defaults for its whole process.
"""
import json
import pathlib
import re
import statistics
import sys

from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

PORT, RUNS, OUT = int(sys.argv[1]), int(sys.argv[2]), pathlib.Path(sys.argv[3])
APPS = ["branding", "plotly", "holoviz", "components"]
MODES = ["classic", "compiled"]


def run(browser, app, mode, screenshot=None):
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    cdp = ctx.new_cdp_session(page)
    cdp.send("Performance.enable")
    out = {"ws_kb": 0, "errors": []}
    idle = []

    def on_console(msg):
        if msg.type == "error" and "404" not in msg.text:
            out["errors"].append(msg.text[:200])
        if (match := re.search(r"document idle at (\d+) ms", msg.text)):
            idle.append(int(match.group(1)))

    page.on("console", on_console)
    page.on("pageerror", lambda error: out["errors"].append(str(error)[:200]))
    page.on("websocket", lambda ws: ws.on(
        "framereceived", lambda payload: out.__setitem__("ws_kb", out["ws_kb"] + len(payload) / 1024)
    ))
    page.goto(f"http://localhost:{PORT + APPS.index(app)}/{app}_{mode}")

    def nodes():
        return {m["name"]: m["value"] for m in cdp.send("Performance.getMetrics")["metrics"]}

    # Settled once the number of DOM nodes has not changed for a second.
    last, changed = None, page.evaluate("performance.now()")
    while True:
        page.wait_for_timeout(100)
        now, count = page.evaluate("performance.now()"), nodes()["Nodes"]
        if count != last:
            last, changed = count, now
        if (idle and now - changed > 1000) or now > 60000:
            break
    metrics = nodes()
    out.update(
        idle_ms=idle[-1] if idle else None, settled_ms=changed,
        script_ms=1e3 * metrics["ScriptDuration"], layout_ms=1e3 * (metrics["LayoutDuration"] + metrics["RecalcStyleDuration"]),
        heap_mb=metrics["JSHeapUsedSize"] / 1e6, nodes=metrics["Nodes"],
    )
    if screenshot:
        page.wait_for_timeout(1500)
        page.screenshot(path=str(screenshot))
    ctx.close()
    return out


def difference(a, b, out):
    first, second = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    diff = ImageChops.difference(first, second).convert("L").point(lambda value: 255 if value > 24 else 0)
    diff.save(out)
    return 100 * sum(1 for value in diff.getdata() if value) / (diff.width * diff.height)


OUT.mkdir(parents=True, exist_ok=True)
results = {}
with sync_playwright() as p:
    browser = p.chromium.launch()
    for app in APPS:
        for mode in MODES:
            run(browser, app, mode, OUT / f"{app}_{mode}.png")
        for i in range(RUNS):
            for mode in MODES:
                result = run(browser, app, mode)
                results.setdefault(f"{app}|{mode}", []).append(result)
                print(app, mode, i, {k: round(v, 1) if isinstance(v, float) else v for k, v in result.items()}, flush=True)
    browser.close()

summary = {}
for key, runs in results.items():
    summary[key] = {
        name: statistics.median([r[name] for r in runs if r[name] is not None] or [float("nan")])
        for name in runs[0] if name != "errors"
    }
    summary[key]["errors"] = sorted({error for r in runs for error in r["errors"]})
for app in APPS:
    summary[f"{app}|classic"]["pixels_differing_pct"] = summary[f"{app}|compiled"]["pixels_differing_pct"] = difference(
        OUT / f"{app}_classic.png", OUT / f"{app}_compiled.png", OUT / f"{app}_diff.png"
    )
json.dump(summary, open(OUT / "results.json", "w"), indent=1)
