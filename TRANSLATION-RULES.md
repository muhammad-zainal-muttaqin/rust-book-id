# Aturan Terjemahan — Bahasa Pemrograman Rust

Dokumen ini adalah satu-satunya sumber aturan untuk semua penerjemah.
Baca dokumen ini sebelum menerjemahkan, lalu patuhi tanpa pengecualian.

## Tujuan

Hasil terjemahan harus terasa seperti **buku Rust berbahasa Indonesia**, bukan
terjemahan mesin. Kalimat mengalir, aktif, dan enak dibaca. Istilah teknis tetap
presisi. Pembaca pemula harus bisa mengikuti tanpa membuka kamus.

## Sasaran pembaca dan suara

- Pembaca: pemula yang sudah bisa memprogram di bahasa lain, tetapi baru belajar Rust.
- Sapaan: **"kamu"** (bukan "Anda"). Untuk "we/our/let's" gunakan **"kita"**.
- Nada: ramah, jelas, percaya diri. Boleh sesekali santai seperti buku, tetapi
  tidak memakai bahasa gaul, singkatan chat, atau emoji.
- Hindari kalimat kaku khas terjemahan: "yang mana", "di mana" sebagai kata
  sambung, "merupakan", "adalah" yang berlebihan, dan "dilakukan oleh".
- Utamakan kalimat aktif. Pecah kalimat Inggris yang panjang menjadi 1–3
  kalimat Indonesia yang lebih pendek.
- Jangan menambah opini, contoh, atau penjelasan baru. Jangan menghilangkan
  informasi. Terjemahkan setia pada makna, bukan kata per kata.

## Yang WAJIB dipertahankan persis

Jangan mengubah satu karakter pun pada:

1. **Code block** (di antara ``` atau ~~~), termasuk komentar di dalamnya.
   Biarkan kode, komentar, dan output compiler tetap bahasa Inggris.
2. **Inline code** (di antara backtick tunggal), misalnya `String`, `let`, `&mut`.
3. **Nama API, tipe, fungsi, variabel, crate, file, path**, dan nama produk.
4. **URL dan target link**, termasuk anchor `#...`.
5. **Directive mdBook**: `{{#rustdoc_include ...}}`, `{{#include ...}}`,
   `{{#playground}}`, `{{#ignore}}`, dan sejenisnya.
6. **Atribut HTML** dan path gambar, misalnya `src="img/..."`, `class="..."`.
7. **Anchor heading eksplisit** `{#nama-anchor}` jika ada.
8. **Penanda blockquote** `>` di awal baris, indentasi list, dan pipa tabel.
9. **Struktur heading** (`#`, `##`, dst.) dan urutannya.
10. **Jumlah dan urutan paragraf, list, tabel, dan gambar.**

Yang boleh dan harus diterjemahkan: prosa, judul heading, item list, isi tabel,
blockquote, alt text gambar, dan teks link. Jangan menerjemahkan isi code block.

## Markdown

- Pertahankan baris kosong antar-blok.
- Pertahankan indentasi list dan blockquote.
- Pertahankan tabel: jumlah kolom, baris pemisah `|---|`, dan alignment.
- Untuk heading, terjemahkan teksnya. Jika ada `{#anchor}`, biarkan anchor.
- Jangan membungkus seluruh jawaban dengan code fence.
- Jangan menambahkan komentar HTML atau catatan penerjemah.

## Glosarium wajib

Gunakan pilihan berikut secara konsisten. Istilah "tetap" ditulis dalam bahasa
Inggris; miringkan saat pertama kali diperkenalkan dalam sebuah bagian.

| Inggris | Indonesia | Catatan |
|---|---|---|
| ownership | ownership | tetap; *ownership* saat pertama muncul |
| borrowing | borrowing | tetap |
| borrow checker | borrow checker | tetap |
| reference | reference | tetap |
| lifetime | lifetime | tetap |
| trait | trait | tetap |
| trait object | trait object | tetap |
| trait bound | trait bound | tetap |
| struct | struct | tetap |
| enum | enum | tetap |
| match | match | tetap (keyword) |
| pattern / pattern matching | pattern / pencocokan pola | "pattern" tetap untuk istilah |
| closure | closure | tetap |
| iterator | iterator | tetap |
| crate | crate | tetap |
| package | package | tetap |
| module | module | tetap |
| workspace | workspace | tetap |
| smart pointer | smart pointer | tetap |
| slice | slice | tetap |
| string | string | tetap |
| string slice | string slice | tetap |
| vector | vector | tetap |
| hash map | hash map | tetap |
| tuple | tuple | tetap |
| array | array | tetap |
| generic | generic | tetap |
| concurrency | concurrency | tetap; judul bab boleh "Konkurensi" |
| thread | thread | tetap |
| async / await | async / await | tetap |
| macro | macro | tetap |
| compiler | compiler | tetap |
| runtime | runtime | tetap |
| heap | heap | tetap |
| stack | stack | tetap |
| pointer | pointer | tetap |
| garbage collector | garbage collector | tetap |
| memory | memori | |
| code | kode | |
| source code | kode sumber | |
| function | fungsi | |
| variable | variabel | |
| value | nilai | |
| type | tipe | |
| data | data | |
| error | error | "kesalahan" hanya untuk kesalahan umum |
| file | file | |
| directory | direktori | |
| command | perintah | |
| command line | command line | tetap |
| argument | argumen | |
| parameter | parameter | |
| statement | statement | tetap |
| expression | ekspresi | |
| block | blok | |
| loop | loop | tetap |
| scope | scope | tetap |
| library | library | tetap |
| test | test | tetap |
| documentation | dokumentasi | |
| comment | komentar | |
| mutable | mutable | tetap |
| immutable | immutable | tetap |
| safe | aman | |
| unsafe | unsafe | tetap (nama konsep) |
| return | mengembalikan | |
| compile | mengompilasi | |
| build | build | tetap |
| run | menjalankan | |
| project | proyek | |
| package manager | package manager | tetap |
| release | release | tetap |
| debug | debug | tetap |
| API | API | tetap |

Jika istilah tidak ada di tabel: pilih yang paling wajar, lalu gunakan
konsisten sampai akhir file. Jangan membuat istilah baru jika istilah Inggrisnya
sudah lazim di komunitas Rust Indonesia.

## Contoh gaya

Buruk (kaku, harfiah):
> Ketika kamu telah menyelesaikan pembacaan dari bab ini, kamu akan memiliki
> pemahaman yang solid mengenai bagaimana ownership bekerja.

Baik (mengalir):
> Setelah membaca bab ini, kamu akan punya dasar yang kuat tentang cara kerja
> ownership.

Buruk:
> Hal ini memungkinkan kita untuk dapat melakukan pengelolaan terhadap memori.

Baik:
> Dengan begitu, kita bisa mengelola memori.

## Prosedur kerja

1. Baca file sumber sampai selesai.
2. Terjemahkan seluruh isi file, bukan sebagian.
3. Tulis hasil lengkap ke path target dengan tool `write`.
4. Jangan mengubah file sumber.
5. Balas hanya `DONE <nama-file>` setelah file target selesai ditulis.
