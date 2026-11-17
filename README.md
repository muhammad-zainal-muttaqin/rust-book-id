# Bahasa Pemrograman Rust — Terjemahan Indonesia

Terjemahan lengkap buku *The Rust Programming Language* (rust-lang/book,
commit `2771df1`, 2026-10-28) dalam bahasa Indonesia.

## Membaca

Buka `book/index.html` di browser. Seluruh bab, lampiran, prakata, dan title
page sudah diterjemahkan (112 file Markdown, 137 halaman HTML).

## Build ulang

```bash
mdbook build
```

Preprocessor `mdbook-trpl` disertakan di `packages/`. Kode Rust tidak perlu
diubah; seluruh directive `{{#include}}` dan gambar sudah lengkap.

## Verifikasi

```bash
python3 verify.py
```

Membandingkan `src/` dengan sumber Inggris asli di workspace lama, memeriksa
kode, heading, link, directive, gambar, include, anchor, serta hasil build.

## Sinkronisasi dengan buku Inggris

Folder workspace lama `~/Developer/rust/rust-book-id/` sengaja dipertahankan
(sebagai sumber Inggris dan area kerja terjemahan). Folder ini adalah salinan
mandiri, bukan pemindahan.

```bash
python3 sync-check.py            # cek sumber Inggris yang berubah / baru
python3 sync-check.py --apply    # tarik terjemahan terbaru dari workspace lama
python3 sync-check.py --refresh  # tandai baseline baru setelah sumber diperbarui
```

Aturan gaya dan glosarium ada di `TRANSLATION-RULES.md`.
