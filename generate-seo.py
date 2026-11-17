#!/usr/bin/env python3
"""Buat robots.txt dan sitemap.xml setelah URL publik diketahui.

Pemakaian:
  python3 generate-seo.py https://USERNAME.github.io/rust-book-id/
  mdbook build

Base URL harus diakhiri "/" dan tanpa "index.html".
"""
from __future__ import annotations

import glob
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(HERE, "book")
SRC = os.path.join(HERE, "src")


def main() -> int:
    if len(sys.argv) != 2 or not sys.argv[1].startswith("https://"):
        print(__doc__)
        return 1
    base = sys.argv[1].rstrip("/") + "/"

    pages = []
    for p in glob.glob(os.path.join(BOOK, "**", "*.html"), recursive=True):
        rel = os.path.relpath(p, BOOK).replace(os.sep, "/")
        if rel in {"404.html", "print.html"} or rel.startswith("searchindex"):
            continue
        if rel.endswith("/index.html"):
            rel = rel[: -len("index.html")]
        elif rel == "index.html":
            rel = ""
        pages.append(rel)
    pages = sorted(set(pages))
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for rel in pages:
        lines.append("  <url>")
        lines.append(f"    <loc>{base}{rel}</loc>")
        lines.append(f"    <lastmod>{now}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    with open(os.path.join(SRC, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    with open(os.path.join(SRC, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write("User-agent: *\nAllow: /\n\n")
        fh.write(f"Sitemap: {base}sitemap.xml\n")

    print(f"{len(pages)} URL ditulis ke src/sitemap.xml dan src/robots.txt")
    print("Jalankan: mdbook build")
    return 0


if __name__ == "__main__":
    sys.exit(main())
