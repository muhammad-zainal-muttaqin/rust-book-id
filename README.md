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

## SEO / metadata

`book.toml` sudah berisi judul, deskripsi, dan `lang = "id"`. Template
`theme/head.hbs` menambahkan tag Open Graph dan Twitter Card untuk pratinjau
saat tautan dibagikan.

Setelah URL publik diketahui, hasilkan `robots.txt` dan `sitemap.xml`:

```bash
python3 generate-seo.py https://USERNAME.github.io/rust-book-id/
mdbook build
```

## Lisensi dan atribusi

Terjemahan ini merupakan karya turunan dari *The Rust Programming Language*
oleh Steve Klabnik, Carol Nichols, Chris Krycho, dan komunitas Rust, yang
dirilis di bawah lisensi ganda **MIT** atau **Apache-2.0**. Lisensi asli
disertakan sebagai `LICENSE-MIT` dan `LICENSE-APACHE`. Terjemahan ini
dididistribusikan dengan ketentuan lisensi yang sama, dengan tetap menjaga
atribusi kepada penulis dan proyek aslinya.
