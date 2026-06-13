#!/usr/bin/env python3
"""
Serve the EventLens monitoring dashboard.

The dashboard reads ../data/*.json, so the HTTP root must be the repository
root (not the dashboard/ folder). This server roots there and opens the page.

    python3 dashboard/serve.py            # serve + open browser
    python3 dashboard/serve.py --port 9000 --no-open

Read-only: it only serves existing files. Stop with Ctrl-C.
"""

import argparse
import functools
import http.server
import os
import webbrowser

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser(description="Serve the EventLens dashboard (read-only).")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--no-open", action="store_true", help="do not open a browser")
    args = ap.parse_args()

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=REPO_ROOT)
    url = f"http://{args.host}:{args.port}/dashboard/"
    with http.server.ThreadingHTTPServer((args.host, args.port), handler) as httpd:
        print(f"EventLens dashboard → {url}")
        print(f"Serving repo root {REPO_ROOT}  (Ctrl-C to stop)")
        if not args.no_open:
            webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped.")


if __name__ == "__main__":
    main()
