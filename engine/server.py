# -*- coding: utf-8 -*-
"""Live dashboard server. Runs the engine loop in a background thread (it keeps searching on
its own) and serves a page that shows findings appearing in real time. Standard library only.

Run:   python server.py              (port 8822, loop ON)
       PORT=9000 python server.py
API:   GET  /api/state               loop state (current round, running probe, totals)
       GET  /api/findings?class=candidate&verdict=CONFIRMED&lens=&q=   filtered feed (newest first)
       GET  /api/summary             counts + best candidates (lowest p, class candidate)
       POST /api/stop  /api/start     pause / resume the loop
"""
import json
import os
import socket
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import nucleo as N   # noqa: E402
import loop as LP    # noqa: E402

ARM = N.Armazem()
_LOOP = {"on": True, "thread": None, "interval": 3.0}


def _read_json(path, dflt):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return dflt


def state():
    est = _read_json(ARM.f_estado, {"round": 0, "total": 0, "running": False})
    est["loop_on"] = _LOOP["on"]
    est["findings_on_disk"] = sum(1 for _ in open(ARM.f_jsonl, encoding="utf-8")) if os.path.exists(ARM.f_jsonl) else 0
    return est


def findings(q):
    items = ARM.todos()
    cls = q.get("class", [None])[0]
    ver = q.get("verdict", [None])[0]
    lens = q.get("lens", [None])[0]
    text = (q.get("q", [None])[0] or "").lower()

    def ok(a):
        if cls and a.get("class") != cls:
            return False
        if ver and a.get("verdict") != ver:
            return False
        if lens and a.get("lens") != lens:
            return False
        if text and text not in json.dumps(a, ensure_ascii=False).lower():
            return False
        return True
    sel = [a for a in items if ok(a)]
    sel.sort(key=lambda a: (a.get("round", 0), a.get("ts", "")), reverse=True)
    return {"total": len(sel), "findings": sel[:int(q.get("limit", [200])[0])]}


def summary():
    items = ARM.todos()
    by_ver, by_cls, by_lens = {}, {}, {}
    for a in items:
        by_ver[a.get("verdict")] = by_ver.get(a.get("verdict"), 0) + 1
        by_cls[a.get("class")] = by_cls.get(a.get("class"), 0) + 1
        by_lens[a.get("lens")] = by_lens.get(a.get("lens"), 0) + 1
    cand = [a for a in items if a.get("class") == "candidate" and a.get("verdict") in ("CONFIRMED", "indication")]
    cand.sort(key=lambda a: a["stat"]["p"])
    best = {}
    for a in cand:
        k = a["probe"]
        if k not in best:
            best[k] = {"title": a["title"], "p": a["stat"]["p"], "verdict": a["verdict"],
                       "lens": a["lens"], "probe": a["probe"], "variants": 0}
        best[k]["variants"] += 1
    return {"total": len(items), "by_verdict": by_ver, "by_class": by_cls, "by_lens": by_lens,
            "best_candidates": sorted(best.values(), key=lambda a: a["p"])[:12]}


def _run_loop():
    while True:
        if _LOOP["on"]:
            try:
                LP.rodar(rodadas=1, intervalo=0.0, verbose=False)
            except Exception as ex:
                sys.stderr.write(f"loop: {ex}\n")
            time.sleep(_LOOP["interval"])
        else:
            time.sleep(1.0)


ROUTES = {
    "/api/state": lambda q: state(),
    "/api/findings": lambda q: findings(q),
    "/api/summary": lambda q: summary(),
}


class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=HERE, **k)

    def _json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        u = urlparse(self.path)
        if u.path == "/api/stop":
            _LOOP["on"] = False
            return self._json({"loop_on": False})
        if u.path == "/api/start":
            _LOOP["on"] = True
            return self._json({"loop_on": True})
        self._json({"error": "unknown route"}, 404)

    def do_GET(self):
        u = urlparse(self.path)
        if u.path in ROUTES:
            try:
                self._json(ROUTES[u.path](parse_qs(u.query)))
            except Exception as ex:
                self._json({"error": str(ex)}, 500)
        elif u.path in ("/", ""):
            self.send_response(302)
            self.send_header("Location", "/panel.html")
            self.end_headers()
        else:
            super().do_GET()

    def log_message(self, *a):
        pass


def local_ips():
    ips = set()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ips.add(s.getsockname()[0])
        s.close()
    except Exception:
        pass
    return sorted(i for i in ips if not i.startswith("127."))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    port = int(os.environ.get("PORT", "8822"))
    t = threading.Thread(target=_run_loop, daemon=True)
    t.start()
    _LOOP["thread"] = t
    print("Enochian pattern engine - live dashboard, loop ON, searching in real time.")
    print(f"  this PC:    http://localhost:{port}/")
    for ip in local_ips():
        print(f"  phone:      http://{ip}:{port}/   (same Wi-Fi)")
    sys.stdout.flush()
    ThreadingHTTPServer(("0.0.0.0", port), H).serve_forever()
