#!/usr/bin/env python3
"""Verifikasi menyeluruh buku terjemahan terhadap sumber Inggris asli.

Usage: python3 verify.py [EN_SRC_DIR] [ID_SRC_DIR] [BOOK_DIR]

Memeriksa:
- kesamaan kumpulan file dan struktur Markdown (kode, heading, link, directive, gambar, anchor)
- keberadaan semua file yang di-include dan semua gambar
- hasil build: jumlah halaman, tautan internal, anchor, gambar, sisa directive
"""
from __future__ import annotations

import glob
import html as htmlmod
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
EN = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Developer/rust/rust-book-id/src")
ID = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "src")
BOOK = sys.argv[3] if len(sys.argv) > 3 else os.path.join(HERE, "book")

FENCE = re.compile(r"(?ms)^(```+|~~~+)([^\n]*)\n(.*?)^\1\s*$")
HEAD = re.compile(r"(?m)^(#{1,6})\s+(.*)$")
LINK = re.compile(r"\]\(([^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\)")
DIRECTIVE = re.compile(r"\{\{#[^}]+\}\}")
IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
ANCHOR = re.compile(r'<a\s+id="([^"]+)"\s*></a>')
INLINE = re.compile(r"`([^`\n]+)`")

ID_MARKERS = (
    "yang", "dan", "untuk", "dengan", "kamu", "kita", "ini", "itu", "tidak",
    "akan", "bisa", "dari", "pada", "dalam", "jika", "atau", "juga", "karena",
)


def read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def fences(text: str) -> list[tuple[str, str]]:
    return [(m.group(2), m.group(3)) for m in FENCE.finditer(text)]


def no_fences(text: str) -> str:
    return FENCE.sub("", text)


def external_broken_hrefs(bookdir: str) -> set[str]:
    """Tautan ke dokumentasi Rust di luar buku (tidak ikut ter-build)."""
    found: set[str] = set()
    if not os.path.isdir(bookdir):
        return found
    for p in glob.glob(os.path.join(bookdir, "**", "*.html"), recursive=True):
        raw = read(p)
        for href in re.findall(r'href="([^"]+)"', raw):
            if href.startswith(("http:", "https:", "mailto:", "javascript:", "data:")):
                continue
            path, sep, frag = href.partition("#")
            if path.lower().endswith((".css", ".js", ".png", ".jpg", ".svg", ".ico", ".gif")):
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(p), path)) if path else p
            if not os.path.exists(target):
                found.add(href)
    return found


def problems_for(name: str, en: str, idn: str) -> tuple[list[str], list[str]]:
    hard: list[str] = []
    soft: list[str] = []

    ef, df = fences(en), fences(idn)
    if len(ef) != len(df):
        hard.append(f"jumlah code block {len(ef)} -> {len(df)}")
    else:
        bad = [i + 1 for i, (a, b) in enumerate(zip(ef, df)) if a != b]
        if bad:
            hard.append(f"isi code block berubah: {bad[:6]}")

    eh, dh = HEAD.findall(en), HEAD.findall(idn)
    if len(eh) != len(dh):
        hard.append(f"jumlah heading {len(eh)} -> {len(dh)}")
    elif [x[0] for x in eh] != [x[0] for x in dh]:
        hard.append("level heading berubah")

    el, dl = Counter(LINK.findall(en)), Counter(LINK.findall(idn))
    if el != dl:
        hard.append(f"link hilang={list((el - dl))[:4]} baru={list((dl - el))[:4]}")

    ed, dd = Counter(DIRECTIVE.findall(en)), Counter(DIRECTIVE.findall(idn))
    if ed != dd:
        hard.append(f"directive hilang={list((ed - dd))[:4]} baru={list((dd - ed))[:4]}")

    ei = Counter(re.findall(r"\]\(([^)]+)\)", ""))  # placeholder, gambar dicek terpisah
    eimg = Counter(m.group(2) for m in IMAGE.finditer(en))
    dimg = Counter(m.group(2) for m in IMAGE.finditer(idn))
    if eimg != dimg:
        hard.append(f"path gambar hilang={list((eimg - dimg))[:4]} baru={list((dimg - eimg))[:4]}")

    ea, da = Counter(ANCHOR.findall(en)), Counter(ANCHOR.findall(idn))
    # Anchor tambahan di terjemahan memang disengaja agar tautan lama tetap bekerja.
    if ea - da:
        hard.append(f"anchor eksplisit hilang={list((ea - da))[:4]}")

    ei = Counter(INLINE.findall(no_fences(en)))
    di = Counter(INLINE.findall(no_fences(idn)))
    if ei != di:
        soft.append(f"inline code hilang={list((ei - di))[:4]} baru={list((di - ei))[:4]}")

    ew, dw = len(en.split()), len(idn.split())
    if ew > 40 and not 0.55 <= dw / ew <= 1.5:
        hard.append(f"rasio kata {ew} -> {dw} ({dw / ew:.2f})")
    if dw > 80:
        low = idn.lower()
        need = 3 if dw < 150 else 6
        if sum(1 for m in ID_MARKERS if m in low) < need:
            hard.append("sedikit penanda bahasa Indonesia")
        if en.strip() == idn.strip():
            hard.append("file masih identik dengan sumber")
    return hard, soft


def main() -> int:
    en_files = sorted(os.path.basename(p) for p in glob.glob(os.path.join(EN, "*.md")))
    id_files = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ID, "*.md")))
    print(f"FILE: EN={len(en_files)} ID={len(id_files)}")
    if en_files != id_files:
        print("  SELISIH:", set(en_files) ^ set(id_files))
        return 1

    hard_all, soft_all = [], []
    missing_includes, missing_images = [], []
    for name in en_files:
        en, idn = read(os.path.join(EN, name)), read(os.path.join(ID, name))
        h, s = problems_for(name, en, idn)
        if h:
            hard_all.append((name, h))
        if s:
            soft_all.append((name, s))
        for m in DIRECTIVE.finditer(idn):
            d = m.group(0)
            mm = re.search(r"\{\{#(?:rustdoc_)?include\s+([^\s}:]+)", d)
            if mm:
                target = os.path.normpath(os.path.join(ID, mm.group(1)))
                if not os.path.exists(target):
                    missing_includes.append((name, d))
        for m in IMAGE.finditer(idn):
            target = os.path.normpath(os.path.join(ID, m.group(2)))
            if not os.path.exists(target):
                missing_images.append((name, m.group(2)))

    print(f"STRUKTUR: {len(en_files) - len(hard_all)}/{len(en_files)} lolos")
    for n, p in hard_all:
        print("  GAGAL", n, "; ".join(p))
    print(f"INCLUDE: {len(missing_includes)} referensi listings hilang")
    for x in missing_includes[:10]:
        print("  ", x)
    print(f"GAMBAR SUMBER: {len(missing_images)} gambar hilang")
    for x in missing_images[:10]:
        print("  ", x)
    print(f"INLINE CODE (peringatan, bukan kerusakan): {len(soft_all)} file")
    for n, p in soft_all:
        print("  ", n, "; ".join(p))

    # --- hasil build ---
    pages = glob.glob(os.path.join(BOOK, "**", "*.html"), recursive=True)
    expected = [os.path.join(BOOK, f[:-3] + ".html") for f in en_files if f != "SUMMARY.md"]
    missing_pages = [p for p in expected if not os.path.exists(p)]
    print(f"BUILD: {len(pages)} halaman, {len(missing_pages)} halaman MD tidak ter-build")
    for p in missing_pages[:10]:
        print("  ", os.path.basename(p))

    ids_cache: dict[str, set[str]] = {}
    broken_anchor, broken_file, broken_img, leftover = [], [], [], []
    for p in pages:
        raw = read(p)
        if "{{#" in raw:
            leftover.append(os.path.relpath(p, BOOK))
        if "<img" in raw:
            for src in re.findall(r'<img[^>]+src="([^"]+)"', raw):
                if src.startswith(("http:", "https:", "data:")):
                    continue
                target = os.path.normpath(os.path.join(os.path.dirname(p), src))
                if not os.path.exists(target):
                    broken_img.append((os.path.relpath(p, BOOK), src))
        for href in re.findall(r'href="([^"]+)"', raw):
            if href.startswith(("http:", "https:", "mailto:", "javascript:", "data:")):
                continue
            path, sep, frag = href.partition("#")
            if path.lower().endswith((".css", ".js", ".png", ".jpg", ".svg", ".ico", ".gif")):
                continue
            site_url = ""
            cfg = os.path.join(HERE, "book.toml")
            if os.path.exists(cfg):
                m = re.search(r'^site-url\s*=\s*"([^"]+)"', read(cfg), re.M)
                if m:
                    site_url = m.group(1).rstrip("/")
            if site_url and path.startswith(site_url):
                # Tautan root-relative untuk GitHub Pages, valid saat di-deploy.
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(p), path)) if path else p
            if not os.path.exists(target):
                broken_file.append((os.path.relpath(p, BOOK), href))
            elif sep and frag:
                if target not in ids_cache:
                    t = read(target)
                    ids_cache[target] = set(re.findall(r'\bid="([^"]+)"', t)) | set(
                        re.findall(r'\bname="([^"]+)"', t)
                    )
                if frag not in ids_cache[target]:
                    broken_anchor.append((os.path.relpath(p, BOOK), href))
    baseline = external_broken_hrefs(os.path.join(os.path.dirname(EN), "book"))
    new_broken = {href for _, href in broken_file} - baseline
    print(f"BUILD LINK: file hilang={len(broken_file)} (sama dengan baseline Inggris={len(baseline)}, "
          f"baru={len(new_broken)}) anchor hilang={len(broken_anchor)}")
    for href in sorted(new_broken)[:10]:
        print("   BARU:", href)
    print(f"BUILD GAMBAR: {len(broken_img)} gagal dimuat")
    print(f"BUILD DIRECTIVE: {len(leftover)} halaman masih mengandung {{{{#")
    for label, arr in (("FILE", broken_file), ("ANCHOR", broken_anchor), ("IMG", broken_img), ("DIRECTIVE", leftover)):
        for x in arr[:8]:
            print("  ", label, x)

    idx = read(os.path.join(BOOK, "index.html"))
    title = re.search(r"<title>([^<]+)</title>", idx)
    lang = re.search(r'<html lang="([^"]+)"', idx)
    print("META:", htmlmod.unescape(title.group(1)) if title else "?", "lang=", lang.group(1) if lang else "?")

    ok = not (hard_all or missing_includes or missing_images or missing_pages
              or new_broken or broken_anchor or broken_img or leftover)
    print("HASIL:", "LULOS" if ok else "ADA MASALAH")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
