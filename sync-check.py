#!/usr/bin/env python3
"""Bantu sinkronisasi dengan buku Inggris yang masih disimpan di workspace lama.

Pemakaian:
  python3 sync-check.py            # lihat sumber Inggris yang berubah / file baru
  python3 sync-check.py --apply    # salin terjemahan terbaru dari workspace lama ke folder ini
  python3 sync-check.py --refresh  # tandai sumber Inggris saat ini sebagai baseline baru

Folder workspace lama (~/Developer/rust/rust-book-id) sengaja dipertahankan
sebagai sumber Inggris + area kerja terjemahan (src-id/). Folder ini adalah
hasil rilis mandiri yang siap dibaca dan di-build.
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.expanduser("~/Developer/rust/rust-book-id")
EN_SRC = os.path.join(WORKSPACE, "src")
ID_SRC = os.path.join(WORKSPACE, "src-id")
MANIFEST = os.path.join(HERE, "source-manifest.json")
LOCAL_SRC = os.path.join(HERE, "src")


def sha(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main() -> int:
    args = set(sys.argv[1:])
    data = json.load(open(MANIFEST, encoding="utf-8"))
    old = data["files"]
    current = {os.path.basename(p): sha(p) for p in glob.glob(os.path.join(EN_SRC, "*.md"))}

    new = sorted(set(current) - set(old))
    changed = sorted(n for n in set(current) & set(old) if current[n] != old[n])
    removed = sorted(set(old) - set(current))

    print("Upstream:", data["upstream"])
    print(f"Sumber Inggris baru: {len(new)} | berubah: {len(changed)} | hilang: {len(removed)}")
    for n in new:
        print("  BARU   ", n)
    for n in changed:
        print("  UBAH   ", n)
    for n in removed:
        print("  HILANG ", n)

    # Terjemahan di folder rilis vs area kerja
    stale = []
    for p in glob.glob(os.path.join(LOCAL_SRC, "*.md")):
        n = os.path.basename(p)
        w = os.path.join(ID_SRC, n)
        if os.path.exists(w) and sha(w) != sha(p):
            stale.append(n)
    print(f"Terjemahan workspace berbeda dengan rilis: {len(stale)}")
    for n in stale[:20]:
        print("  BEDA   ", n)

    if "--apply" in args:
        os.makedirs(LOCAL_SRC, exist_ok=True)
        for n in sorted(set(os.path.basename(p) for p in glob.glob(os.path.join(ID_SRC, "*.md")))):
            w, d = os.path.join(ID_SRC, n), os.path.join(LOCAL_SRC, n)
            if not os.path.exists(d) or sha(w) != sha(d):
                shutil.copy2(w, d)
        img_src, img_dst = os.path.join(ID_SRC, "img"), os.path.join(LOCAL_SRC, "img")
        if os.path.isdir(img_src):
            shutil.copytree(img_src, img_dst, dirs_exist_ok=True)
        print("Tersalin dari workspace -> src/")
    if "--refresh" in args:
        data["files"] = current
        json.dump(data, open(MANIFEST, "w"), indent=2, ensure_ascii=False)
        print("Baseline sumber Inggris diperbarui.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
