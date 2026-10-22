#!/usr/bin/env python3
"""
Geometry passes from docs/rendered-output-qa.md, run in a real browser.

Checks (Chromium and WebKit unless --engines says otherwise):

  width sweep     every --step px from --min to --max: horizontal overflow,
                  labels that wrap to two lines, block edges off the column
  height sweep    width x height pairs: h1 and --cta inside the first viewport
  lazy media      scroll every section into view, then every visible <img>
                  must have loaded
  scroll paint    Chromium trace during a scripted scroll: elements that
                  repaint on most frames (reads as jank on iOS Safari)

Output: JSON with `checks` entries in the rendered-output-qa/v1 checkResult
shape, ready to merge into a report. Exit code 1 when any check fails.

Usage:
  uv run --with playwright python3 scripts/rendered_qa.py TARGET [options]

  TARGET  http(s) URL, a directory (served locally; --page picks the file),
          or a path to an .html file.

Examples:
  uv run --with playwright python3 scripts/rendered_qa.py dist/site
  uv run --with playwright python3 scripts/rendered_qa.py dist/site \\
      --cta ".hero .btn" --edges "main .card, main figure" --hide "#cookie"

Screenshots, axe-core and the focus-order walk are not part of this script;
run them on the breakpoint ladder as described in the document.
"""
from __future__ import annotations

import argparse
import functools
import glob
import http.server
import json
import os
import socketserver
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path

LADDER = [320, 360, 480, 640, 768, 1024, 1280, 1440, 1920]
HEIGHT_PAIRS = [(w, h) for w in (360, 390, 768, 1024, 1280, 1440) for h in (667, 720, 800)] + [(844, 390)]
DEFAULT_LABELS = "nav a, header a, button, .btn, [role=button], .tag, .badge, .chip"

JS_SWEEP = r"""
({labels, edges, edgeContainer, tolerance}) => {
  const visible = el => {
    if (!el.getClientRects().length) return false;
    const cs = getComputedStyle(el);
    return cs.visibility !== 'hidden' && cs.display !== 'none';
  };
  const name = el => {
    const t = (el.innerText || el.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ');
    const cls = typeof el.className === 'string' && el.className.trim()
      ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
    return `${el.tagName.toLowerCase()}${cls}${t ? ' "' + t.slice(0, 40) + '"' : ''}`;
  };
  const de = document.documentElement;
  const overflow = Math.max(0, de.scrollWidth - de.clientWidth);

  const wrapped = [];
  if (labels) {
    document.querySelectorAll(labels).forEach(el => {
      if (!visible(el) || !el.textContent.trim()) return;
      const r = document.createRange();
      r.selectNodeContents(el);
      const rects = [...r.getClientRects()].filter(q => q.width > 1 && q.height > 1).sort((a, b) => a.top - b.top);
      let lines = 0, bottom = -Infinity;
      for (const q of rects) {
        if (q.top >= bottom - 2) { lines++; bottom = q.bottom; } else bottom = Math.max(bottom, q.bottom);
      }
      if (lines > 1) wrapped.push(name(el));
    });
  }

  const offEdge = [];
  if (edges) {
    document.querySelectorAll(edges).forEach(el => {
      if (!visible(el)) return;
      const saved = [el.style.transform, el.style.rotate, el.style.translate, el.style.scale];
      el.style.transform = el.style.rotate = el.style.translate = el.style.scale = 'none';
      const box = el.getBoundingClientRect();
      [el.style.transform, el.style.rotate, el.style.translate, el.style.scale] = saved;
      if (box.width < 40) return;
      const own = getComputedStyle(el);
      if (own.backgroundColor === 'rgba(0, 0, 0, 0)' && !(parseFloat(own.borderRightWidth) > 0) && own.boxShadow === 'none') return;
      const host = (edgeContainer && el.parentElement && el.parentElement.closest(edgeContainer)) || el.parentElement;
      if (!host) return;
      let boxedAncestor = false;
      for (let a = el.parentElement; a && a !== host && !boxedAncestor; a = a.parentElement) {
        const as = getComputedStyle(a);
        boxedAncestor = as.backgroundColor !== 'rgba(0, 0, 0, 0)' || parseFloat(as.borderRightWidth) > 0 || as.boxShadow !== 'none';
      }
      if (boxedAncestor) return;
      let rowmate = false;
      for (let node = el; node && node !== host && !rowmate; node = node.parentElement) {
        rowmate = [...(node.parentElement ? node.parentElement.children : [])].some(s => {
          if (s === node || !s.getClientRects().length) return false;
          const b = s.getBoundingClientRect();
          return b.left >= box.right - 1 && b.top < box.bottom && b.bottom > box.top;
        });
      }
      if (rowmate) return;
      const hs = getComputedStyle(host), hb = host.getBoundingClientRect();
      const right = hb.right - parseFloat(hs.paddingRight) - parseFloat(hs.borderRightWidth);
      const cs = getComputedStyle(el);
      const m = cs.boxShadow.match(/(-?\d+(?:\.\d+)?)px\s+(-?\d+(?:\.\d+)?)px\s+0px/);
      const shadow = m ? Math.max(0, parseFloat(m[1])) : 0;
      const expected = right - shadow;
      const delta = Math.round(box.right - expected);
      if (Math.abs(delta) > tolerance) offEdge.push(`${name(el)} ${delta > 0 ? 'over' : 'short'} ${Math.abs(delta)}px (shadow ${shadow}px)`);
    });
  }
  return {overflow, wrapped, offEdge};
}
"""

JS_FOLD = r"""
(cta) => {
  const vh = innerHeight, out = {};
  const h1 = document.querySelector('h1');
  if (h1) out.h1 = Math.round(h1.getBoundingClientRect().bottom - vh);
  if (cta) {
    const el = [...document.querySelectorAll(cta)].find(e => e.getClientRects().length);
    out.cta = el ? Math.round(el.getBoundingClientRect().bottom - vh) : null;
  }
  return out;
}
"""

JS_IMAGES = r"""
() => [...document.images].filter(img => img.getClientRects().length && getComputedStyle(img).visibility !== 'hidden')
  .filter(img => !(img.complete && img.naturalWidth > 0))
  .map(img => `${(img.currentSrc || img.src).split('/').pop()} (box ${Math.round(img.getBoundingClientRect().width)}x${Math.round(img.getBoundingClientRect().height)}, loading=${img.loading || 'eager'})`)
"""

JS_SCROLL_FRAMES = r"""
async (frames) => {
  const total = Math.min(document.documentElement.scrollHeight - innerHeight, innerHeight * 1.5);
  for (let i = 1; i <= frames; i++) {
    window.scrollTo(0, total * i / frames);
    await new Promise(r => requestAnimationFrame(() => r()));
  }
  return frames;
}
"""


def serve(target: str, page: str) -> tuple[str, str]:
    """Return (url, artifact_type)."""
    if target.startswith(("http://", "https://")):
        return target, "deployed_url"
    path = Path(target).resolve()
    if path.is_file():
        root, page = path.parent, path.name
    elif path.is_dir():
        root = path
    else:
        sys.exit(f"Target not found: {target}")

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    socketserver.ThreadingTCPServer.daemon_threads = True
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=str(root)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{srv.server_address[1]}/{page}", "local_url"


def launch(playwright, engine: str):
    bt = getattr(playwright, engine)
    try:
        return bt.launch()
    except Exception:
        if engine != "chromium":
            raise
        shells = sorted(glob.glob(os.path.expanduser(
            "~/Library/Caches/ms-playwright/chromium_headless_shell-*/chrome-*/chrome-headless-shell")))
        if not shells:
            raise
        return bt.launch(executable_path=shells[-1])


def ranges(widths: list[int], step: int) -> str:
    """[320, 336, 352, 900] -> '320-352, 900'."""
    if not widths:
        return ""
    out, start, prev = [], widths[0], widths[0]
    for w in widths[1:]:
        if w - prev > step:
            out.append(f"{start}-{prev}" if start != prev else f"{start}")
            start = w
        prev = w
    out.append(f"{start}-{prev}" if start != prev else f"{start}")
    return ", ".join(out)


def add_check(checks, cid, category, ok, severity, notes, viewports=None, status=None):
    item = {
        "id": cid,
        "category": category,
        "status": status or ("pass" if ok else "fail"),
        "severity": "none" if ok and not status else severity,
        "evidence": "measured",
        "notes": notes,
    }
    if viewports:
        item["viewport_ids"] = viewports
    checks.append(item)


def open_page(browser, url, width, height, hide, reduce=True):
    ctx = browser.new_context(viewport={"width": width, "height": height},
                              reduced_motion="reduce" if reduce else "no-preference")
    page = ctx.new_page()
    page.goto(url, wait_until="networkidle")
    if hide:
        page.add_style_tag(content=f"{hide}{{display:none!important}}")
    page.add_style_tag(content="html{scroll-behavior:auto!important}")
    page.wait_for_timeout(150)
    return ctx, page


def run_engine(playwright, engine, url, args, checks):
    browser = launch(playwright, engine)

    # Width sweep: one page, resized in place.
    widths = sorted(set(range(args.min, args.max + 1, args.step)) | {w for w in LADDER if args.min <= w <= args.max})
    ctx, page = open_page(browser, url, widths[0], 800, args.hide)
    overflow_at, wrapped_at, edges_at = [], {}, {}
    for w in widths:
        page.set_viewport_size({"width": w, "height": 800})
        page.wait_for_timeout(40)
        r = page.evaluate(JS_SWEEP, {"labels": args.labels, "edges": args.edges, "edgeContainer": args.edge_container, "tolerance": args.edge_tolerance})
        if r["overflow"] > 1:
            overflow_at.append(w)
        for label in r["wrapped"]:
            wrapped_at.setdefault(label, []).append(w)
        for item in r["offEdge"]:
            key = item.rsplit(" over ", 1)[0].rsplit(" short ", 1)[0]
            edges_at.setdefault(key, []).append((w, item))
    ctx.close()

    add_check(checks, f"{engine}-overflow", "reflow_320", not overflow_at, "high",
              f"horizontal scroll at {ranges(overflow_at, args.step)} px" if overflow_at
              else f"no horizontal scroll, {len(widths)} widths {args.min}-{args.max}")
    if args.labels:
        notes = "; ".join(f"{k} wraps at {ranges(v, args.step)}" for k, v in wrapped_at.items())
        add_check(checks, f"{engine}-single-line", "text_overflow", not wrapped_at, "medium",
                  notes or f"all labels on one line ({args.labels})")
    if args.edges:
        notes = "; ".join(f"{v[0][1]} at {ranges([w for w, _ in v], args.step)}" for v in edges_at.values())
        add_check(checks, f"{engine}-edges", "layout_overlap", not edges_at, "medium",
                  notes or f"all blocks end on the column edge ({args.edges})")

    # Height sweep: fresh load per pair, page at the top.
    misses, landscape = [], []
    for w, h in HEIGHT_PAIRS:
        ctx, page = open_page(browser, url, w, h, args.hide)
        r = page.evaluate(JS_FOLD, args.cta)
        ctx.close()
        for key in ("h1", "cta"):
            if r.get(key) is not None and r[key] > 0:
                (landscape if w > h else misses).append(f"{key} {r[key]}px below the fold at {w}x{h}")
            if key == "cta" and args.cta and r.get("cta") is None:
                misses.append(f"cta selector matched nothing at {w}x{h}")
    add_check(checks, f"{engine}-first-viewport", "layout_overlap", not misses, "medium",
              "; ".join(misses) or f"h1{' and CTA' if args.cta else ''} inside the first viewport at {len(HEIGHT_PAIRS) - 1} portrait and desktop pairs")
    if landscape:
        add_check(checks, f"{engine}-first-viewport-landscape", "layout_overlap", False, "low",
                  "; ".join(landscape) + " (landscape phone: review, not a blocker)", status="warning")

    # Lazy media after a full scroll.
    missing = {}
    for w, h in ((390, 844), (1280, 800)):
        ctx, page = open_page(browser, url, w, h, args.hide)
        height = page.evaluate("document.documentElement.scrollHeight")
        y = 0
        while y < height:
            y += int(h * 0.8)
            page.evaluate(f"window.scrollTo(0, {y})")
            page.wait_for_timeout(120)
            height = page.evaluate("document.documentElement.scrollHeight")
        page.wait_for_timeout(800)
        for item in page.evaluate(JS_IMAGES):
            missing.setdefault(item, []).append(f"{w}x{h}")
        ctx.close()
    add_check(checks, f"{engine}-lazy-media", "cross_browser", not missing, "high",
              "; ".join(f"{k} not loaded at {', '.join(v)}" for k, v in missing.items())
              or "every visible image loaded after scrolling the page")

    # Scroll paint count (Chromium tracing only).
    if engine == "chromium":
        ctx, page = open_page(browser, url, 390, 844, args.hide, reduce=False)
        page.wait_for_timeout(300)
        cdp = ctx.new_cdp_session(page)
        root = cdp.send("DOM.getDocument", {"depth": 2})["root"]
        skip = {root["backendNodeId"]}
        for child in root.get("children", []):
            skip.add(child["backendNodeId"])
            skip.update(c["backendNodeId"] for c in child.get("children", []))
        browser.start_tracing(page=page, categories=["devtools.timeline"])
        frames = page.evaluate(JS_SCROLL_FRAMES, 60)
        page.wait_for_timeout(100)
        trace = json.loads(browser.stop_tracing())
        events = trace.get("traceEvents", trace if isinstance(trace, list) else [])
        per_node: dict[int, int] = {}
        for e in events:
            node = e.get("args", {}).get("data", {}).get("nodeId") if e.get("name") == "Paint" else None
            if node and node not in skip:
                per_node[node] = per_node.get(node, 0) + 1
        hot = []
        for node, count in sorted(per_node.items(), key=lambda kv: -kv[1]):
            if count / frames < args.paint_threshold:
                continue
            try:
                d = cdp.send("DOM.describeNode", {"backendNodeId": node})["node"]
                attrs = dict(zip(d.get("attributes", [])[0::2], d.get("attributes", [])[1::2]))
                label = d["nodeName"].lower() + "".join(f".{c}" for c in attrs.get("class", "").split()[:2])
            except Exception:
                label = f"node {node}"
            hot.append(f"{label} repaints on {count} of {frames} frames")
        ctx.close()
        add_check(checks, "chromium-scroll-paint", "performance_cwv", not hot, "medium",
                  ("; ".join(hot) if hot else f"no element repaints on {args.paint_threshold:.0%}+ of {frames} scroll frames")
                  + "; confirm smoothness on a real iOS Safari device")
    browser.close()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target")
    ap.add_argument("--page", default="index.html", help="file to open when TARGET is a directory")
    ap.add_argument("--engines", default="chromium,webkit")
    ap.add_argument("--min", type=int, default=320)
    ap.add_argument("--max", type=int, default=1920)
    ap.add_argument("--step", type=int, default=16, help="width sweep step in px (10-20 recommended)")
    ap.add_argument("--labels", default=DEFAULT_LABELS, help="elements that must stay on one line; '' to skip")
    ap.add_argument("--cta", default="", help="primary CTA selector for the first-viewport check")
    ap.add_argument("--edges", default="", help="blocks that must end on their column edge")
    ap.add_argument("--edge-container", default="", help="column selector; default is each block's parent")
    ap.add_argument("--edge-tolerance", type=float, default=2,
                    help="px a block may sit off its expected edge (raise it for tilted blocks with a reserve)")
    ap.add_argument("--hide", default="", help="selector hidden before measuring (cookie banner, chat widget)")
    ap.add_argument("--paint-threshold", type=float, default=0.5,
                    help="share of scroll frames on which one element may repaint before the check fails")
    ap.add_argument("--out", default="", help="write the JSON report here; default prints it")
    args = ap.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("Playwright is missing. Run with: uv run --with playwright python3 scripts/rendered_qa.py ...")

    url, artifact_type = serve(args.target, args.page)
    checks: list[dict] = []
    with sync_playwright() as p:
        for engine in [e.strip() for e in args.engines.split(",") if e.strip()]:
            run_engine(p, engine, url, args, checks)

    failed = [c for c in checks if c["status"] == "fail"]
    report = {
        "tool": "web-design-skill/scripts/rendered_qa.py",
        "check_vocabulary": "rendered-output-qa/v1",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "target": args.target,
        "artifact_type": artifact_type,
        "checks": checks,
        "unverified": ["scroll smoothness on a real iOS Safari device", "screenshots, axe-core, focus order"],
    }
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    for c in checks:
        print(f"[{c['status'].upper():4}] {c['id']}: {c['notes']}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
