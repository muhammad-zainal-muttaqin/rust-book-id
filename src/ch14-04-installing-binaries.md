<!-- Old headings. Do not remove or links may break. -->

<a id="installing-binaries-from-cratesio-with-cargo-install"></a>

## Menginstal binary dengan `cargo install`

Perintah `cargo install` memungkinkan kamu menginstal dan menggunakan binary crate secara lokal. Ini bukan untuk menggantikan package sistem; perintah ini dimaksudkan sebagai cara praktis bagi pengembang Rust untuk menginstal alat yang dibagikan orang lain di [crates.io](https://crates.io/)<!-- ignore -->. Perlu diingat bahwa kamu hanya bisa menginstal package yang memiliki binary target. _Binary target_ adalah program yang bisa dijalankan dan dibuat jika crate memiliki file _src/main.rs_ atau file lain yang ditentukan sebagai binary, berbeda dengan library target yang tidak bisa dijalankan sendiri tetapi cocok disertakan dalam program lain. Biasanya, crate memiliki informasi di file README tentang apakah sebuah crate itu library, memiliki binary target, atau keduanya.

Semua binary yang diinstal dengan `cargo install` disimpan di folder _bin_ dari root instalasi. Jika kamu menginstal Rust menggunakan _rustup.rs_ dan tidak punya konfigurasi khusus, direktori ini akan menjadi *$HOME/.cargo/bin*. Pastikan direktori ini ada di `$PATH` kamu agar bisa menjalankan program yang telah kamu instal dengan `cargo install`.

Misalnya, di Bab 12 kita menyebutkan bahwa ada implementasi Rust dari alat `grep` bernama `ripgrep` untuk mencari file. Untuk menginstal `ripgrep`, kita bisa menjalankan perintah berikut:

<!-- manual-regeneration
cargo install something you don't have, copy relevant output below
-->

```console
$ cargo install ripgrep
    Updating crates.io index
  Downloaded ripgrep v14.1.1
  Downloaded 1 crate (213.6 KB) in 0.40s
  Installing ripgrep v14.1.1
--snip--
   Compiling grep v0.3.2
    Finished `release` profile [optimized + debuginfo] target(s) in 6.73s
  Installing ~/.cargo/bin/rg
   Installed package `ripgrep v14.1.1` (executable `rg`)
```

Baris kedua dari terakhir pada output menunjukkan lokasi dan nama binary yang terinstal, yang dalam kasus `ripgrep` adalah `rg`. Selama direktori instalasi ada di `$PATH` kamu, seperti yang disebutkan sebelumnya, kamu bisa menjalankan `rg --help` dan mulai menggunakan alat pencarian file yang lebih cepat dan lebih khas Rust!
