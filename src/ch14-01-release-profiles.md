## Menyesuaikan Build dengan Profil Release

Di Rust, _profil release_ adalah profil yang sudah ditentukan dan bisa disesuaikan, dengan konfigurasi berbeda yang memberi programmer lebih banyak kendali atas beragam opsi pengompilasian kode. Setiap profil dikonfigurasi secara terpisah dari profil lainnya.

Cargo punya dua profil utama: profil `dev` yang dipakai Cargo saat kamu menjalankan `cargo build`, dan profil `release` yang dipakai Cargo saat kamu menjalankan `cargo build --release`. Profil `dev` didefinisikan dengan default yang bagus untuk pengembangan, sedangkan profil `release` punya default yang bagus untuk build release.

Nama-nama profil ini mungkin sudah akrab dari keluaran build kamu:

<!-- manual-regeneration
anywhere, run:
cargo build
cargo build --release
and ensure output below is accurate
-->

```console
$ cargo build
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
$ cargo build --release
    Finished `release` profile [optimized] target(s) in 0.32s
```

`dev` dan `release` adalah profil-profil berbeda yang dipakai compiler.

Cargo punya pengaturan default untuk masing-masing profil yang berlaku saat kamu belum menambahkan secara eksplisit bagian `[profile.*]` apa pun di file _Cargo.toml_ proyekmu. Dengan menambahkan bagian `[profile.*]` untuk profil mana pun yang ingin kamu sesuaikan, kamu menimpa sebagian dari pengaturan default. Misalnya, ini nilai default untuk pengaturan `opt-level` pada profil `dev` dan `release`:

<span class="filename">Filename: Cargo.toml</span>

```toml
[profile.dev]
opt-level = 0

[profile.release]
opt-level = 3
```

Pengaturan `opt-level` mengontrol jumlah optimasi yang akan diterapkan Rust pada kode kamu, dalam rentang 0 sampai 3. Makin banyak optimasi diterapkan, makin lama waktu kompilasi, jadi kalau kamu sedang mengembangkan dan sering mengompilasi kode, kamu akan ingin lebih sedikit optimasi agar kompilasi lebih cepat meski kode yang dihasilkan berjalan lebih lambat. Karena itu, `opt-level` default untuk `dev` adalah `0`. Saat kamu siap merilis kode, sebaiknya luangkan lebih banyak waktu untuk kompilasi. Kamu hanya akan mengompilasi sekali dalam mode release, tapi menjalankan program hasil kompilasi berkali-kali, jadi mode release menukar waktu kompilasi yang lebih lama dengan kode yang berjalan lebih cepat. Itulah sebabnya `opt-level` default untuk profil `release` adalah `3`.

Kamu bisa menimpa pengaturan default dengan menambahkan nilai berbeda untuknya di _Cargo.toml_. Misalnya, kalau kita ingin memakai tingkat optimasi 1 pada profil pengembangan, kita bisa menambahkan dua baris ini ke file _Cargo.toml_ proyek kita:

<span class="filename">Filename: Cargo.toml</span>

```toml
[profile.dev]
opt-level = 1
```

Kode ini menimpa pengaturan default `0`. Sekarang saat kita menjalankan `cargo build`, Cargo akan memakai default profil `dev` plus penyesuaian kita pada `opt-level`. Karena kita menetapkan `opt-level` ke `1`, Cargo akan menerapkan lebih banyak optimasi daripada default, tapi tidak sebanyak build release.

Untuk daftar lengkap opsi konfigurasi dan default tiap profil, lihat [dokumentasi Cargo](https://doc.rust-lang.org/cargo/reference/profiles.html).
