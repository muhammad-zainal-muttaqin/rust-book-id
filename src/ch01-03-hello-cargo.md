## Hello, Cargo!

Cargo adalah build system dan package manager untuk Rust. Kebanyakan Rustacean memakai tool ini untuk mengelola proyek Rust mereka, karena Cargo menangani banyak tugas untukmu: meng-build kode, mengunduh library yang dibutuhkan kode kamu, dan meng-build library-library tersebut. (Library yang dibutuhkan kode kamu kita sebut _dependencies_.)

Program Rust yang paling sederhana, seperti yang baru kita tulis sejauh ini, tidak punya dependency apa pun. Kalau kita meng-build proyek "Hello, world!" dengan Cargo, kita hanya akan memakai bagian Cargo yang menangani peng-build-an kode kamu. Begitu kamu menulis program Rust yang lebih kompleks, kamu akan menambahkan dependency, dan kalau kamu memulai proyek dengan Cargo, menambahkan dependency jadi jauh lebih mudah.

Karena mayoritas besar proyek Rust memakai Cargo, sisa buku ini mengasumsikan kamu juga memakai Cargo. Cargo sudah terpasang bersama Rust jika kamu memakai installer resmi yang dibahas di bagian ["Installation"][installation]<!-- ignore -->. Jika kamu memasang Rust lewat cara lain, cek apakah Cargo sudah terpasang dengan mengetik hal berikut di terminal kamu:

```console
$ cargo --version
```

Jika kamu melihat nomor versi, berarti sudah terpasang! Jika kamu melihat error, seperti `command not found`, lihat dokumentasi metode pemasangan kamu untuk mengetahui cara memasang Cargo secara terpisah.

### Membuat Proyek dengan Cargo

Ayo kita buat proyek baru memakai Cargo dan lihat bedanya dengan proyek "Hello, world!" asli kita. Kembali ke direktori _projects_ kamu (atau di mana pun kamu menyimpan kode kamu). Lalu, di sistem operasi apa pun, jalankan ini:

```console
$ cargo new hello_cargo
$ cd hello_cargo
```

Perintah pertama membuat direktori dan proyek baru bernama _hello_cargo_. Kita menamai proyek kita _hello_cargo_, dan Cargo membuat file-file di dalamnya di direktori dengan nama yang sama.

Masuk ke direktori _hello_cargo_ dan daftarkan isinya. Kamu akan melihat Cargo sudah menghasilkan dua file dan satu direktori untuk kita: file _Cargo.toml_ dan direktori _src_ yang berisi file _main.rs_ di dalamnya.

Cargo juga sudah menginisialisasi repository Git baru beserta file _.gitignore_. File Git tidak akan dihasilkan jika kamu menjalankan `cargo new` di dalam repository Git yang sudah ada; kamu bisa menimpa perilaku ini dengan memakai `cargo new --vcs=git`.

> Catatan: Git adalah sistem kontrol versi yang umum dipakai. Kamu bisa mengubah `cargo new` agar memakai sistem kontrol versi lain atau tanpa sistem kontrol versi sama sekali dengan memakai flag `--vcs`. Jalankan `cargo new --help` untuk melihat pilihan yang tersedia.

Buka _Cargo.toml_ dengan text editor pilihan kamu. Isinya kira-kira seperti kode pada Listing 1-2.

<Listing number="1-2" file-name="Cargo.toml" caption="Isi *Cargo.toml* yang dihasilkan oleh `cargo new`">

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
```

</Listing>

File ini memakai format [_TOML_][toml]<!-- ignore --> (_Tom’s Obvious, Minimal Language_), format konfigurasi milik Cargo.

Baris pertama, `[package]`, adalah judul bagian yang menandakan bahwa statement berikutnya mengonfigurasi sebuah package. Begitu kita menambahkan lebih banyak informasi ke file ini, kita akan menambahkan bagian-bagian lainnya.

Tiga baris berikutnya mengatur informasi konfigurasi yang dibutuhkan Cargo untuk mengompilasi program kamu: nama, versi, dan edisi Rust yang dipakai. Kita akan membahas kunci `edition` di [Appendix E][appendix-e]<!-- ignore -->.

Baris terakhir, `[dependencies]`, adalah awal dari bagian untuk kamu mencantumkan semua dependency proyek kamu. Di Rust, paket-paket kode disebut _crates_. Proyek ini belum membutuhkan crate lain, tapi proyek pertama di Bab 2 akan membutuhkannya, jadi saat itu kita akan memakai bagian dependencies ini.

Sekarang buka _src/main.rs_ dan lihat isinya:

<span class="filename">Filename: src/main.rs</span>

```rust
fn main() {
    println!("Hello, world!");
}
```

Cargo sudah menghasilkan program "Hello, world!" untuk kamu, sama seperti yang kita tulis pada Listing 1-1! Sejauh ini, perbedaan antara proyek kita dan proyek hasil Cargo adalah Cargo menaruh kode di direktori _src_, sedangkan kita punya file konfigurasi _Cargo.toml_ di direktori tingkat atas.

Cargo mengharapkan file source kamu berada di dalam direktori _src_. Direktori proyek tingkat atas hanya untuk file README, informasi lisensi, file konfigurasi, dan hal-hal lain yang tidak berhubungan dengan kode kamu. Memakai Cargo membantu kamu menata proyek. Ada tempat untuk segalanya, dan segalanya ada di tempatnya.

Jika kamu memulai proyek yang tidak memakai Cargo, seperti kita lakukan pada proyek "Hello, world!", kamu bisa mengonversinya menjadi proyek yang memakai Cargo. Pindahkan kode proyek ke direktori _src_ dan buat file _Cargo.toml_ yang sesuai. Cara mudah untuk mendapatkan file _Cargo.toml_ itu adalah menjalankan `cargo init`, yang akan membuatnya secara otomatis untukmu.

### Meng-build dan Menjalankan Proyek Cargo

Sekarang mari kita lihat apa yang berbeda saat kita meng-build dan menjalankan program "Hello, world!" dengan Cargo! Dari direktori _hello_cargo_ kamu, build proyek kamu dengan mengetik perintah berikut:

```console
$ cargo build
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 2.85 secs
```

Perintah ini membuat file executable di _target/debug/hello_cargo_ (atau _target\debug\hello_cargo.exe_ di Windows), bukan di direktori kamu saat ini. Karena build bawaan adalah debug build, Cargo menaruh binary di direktori bernama _debug_. Kamu bisa menjalankan executable itu dengan perintah ini:

```console
$ ./target/debug/hello_cargo # or .\target\debug\hello_cargo.exe on Windows
Hello, world!
```

Jika semuanya berjalan lancar, `Hello, world!` akan tercetak di terminal. Menjalankan `cargo build` untuk pertama kalinya juga membuat Cargo menghasilkan file baru di tingkat atas: _Cargo.lock_. File ini mencatat versi persis dari dependency di proyek kamu. Proyek ini tidak punya dependency, jadi file itu agak kosong. Kamu tidak perlu pernah mengubah file ini secara manual; Cargo mengelola isinya untukmu.

Kita baru saja meng-build proyek dengan `cargo build` dan menjalankannya dengan `./target/debug/hello_cargo`, tapi kita juga bisa memakai `cargo run` untuk mengompilasi kode lalu menjalankan executable hasilnya, semuanya dalam satu perintah:

```console
$ cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

Memakai `cargo run` lebih praktis daripada harus mengingat untuk menjalankan `cargo build` lalu memakai path lengkap ke binary, jadi kebanyakan developer memakai `cargo run`.

Perhatikan bahwa kali ini kita tidak melihat output yang menandakan Cargo sedang mengompilasi `hello_cargo`. Cargo tahu file-file itu tidak berubah, jadi ia tidak meng-build ulang, hanya menjalankan binary-nya. Jika kamu mengubah kode sumber kamu, Cargo akan meng-build ulang proyek sebelum menjalankannya, dan kamu akan melihat output ini:

```console
$ cargo run
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.33 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

Cargo juga menyediakan perintah bernama `cargo check`. Perintah ini memeriksa kode kamu dengan cepat untuk memastikan kode itu bisa dikompilasi, tapi tidak menghasilkan executable:

```console
$ cargo check
   Checking hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.32 secs
```

Mengapa kamu tidak menginginkan executable? Sering kali, `cargo check` jauh lebih cepat daripada `cargo build` karena ia melewati langkah pembuatan executable. Jika kamu terus-menerus memeriksa pekerjaan kamu selagi menulis kode, memakai `cargo check` akan mempercepat proses pemberitahuan apakah proyek kamu masih bisa dikompilasi! Karena itu, banyak Rustacean menjalankan `cargo check` secara berkala saat menulis program mereka untuk memastikan program itu bisa dikompilasi. Baru setelah itu, mereka menjalankan `cargo build` ketika sudah siap memakai executable-nya.

Ayo kita rangkum apa yang sudah kita pelajari sejauh ini tentang Cargo:

- Kita bisa membuat proyek memakai `cargo new`.
- Kita bisa meng-build proyek memakai `cargo build`.
- Kita bisa meng-build dan menjalankan proyek dalam satu langkah memakai `cargo run`.
- Kita bisa meng-build proyek tanpa menghasilkan binary untuk memeriksa error memakai `cargo check`.
- Alih-alih menyimpan hasil build di direktori yang sama dengan kode kita, Cargo menyimpannya di direktori _target/debug_.

Keuntungan tambahan memakai Cargo adalah perintahnya sama persis tidak peduli sistem operasi apa yang kamu pakai. Jadi, mulai sekarang, kita tidak lagi memberi instruksi khusus untuk Linux dan macOS versus Windows.

### Meng-build untuk Release

Ketika proyek kamu akhirnya siap dirilis, kamu bisa memakai `cargo build --release` untuk mengompilasinya dengan optimasi. Perintah ini akan membuat executable di _target/release_ alih-alih _target/debug_. Optimasi membuat kode Rust kamu berjalan lebih cepat, tapi mengaktifkannya memperpanjang waktu yang dibutuhkan program kamu untuk dikompilasi. Karena itu ada dua profile yang berbeda: satu untuk pengembangan, ketika kamu ingin meng-build ulang dengan cepat dan sering, dan satu lagi untuk meng-build program akhir yang akan kamu berikan ke pengguna, yang tidak akan di-build ulang berulang kali dan akan berjalan secepat mungkin. Jika kamu melakukan benchmark terhadap waktu jalan kode kamu, pastikan menjalankan `cargo build --release` dan mem-benchmark dengan executable di _target/release_.

<!-- Old headings. Do not remove or links may break. -->
<a id="cargo-as-convention"></a>

### Memanfaatkan Konvensi Cargo

Untuk proyek sederhana, Cargo tidak memberi banyak keunggulan dibanding hanya memakai `rustc`, tapi ia akan membuktikan nilainya begitu program kamu menjadi lebih rumit. Begitu program bertambah menjadi banyak file atau membutuhkan dependency, jauh lebih mudah membiarkan Cargo yang mengoordinasi proses build-nya.

Meskipun proyek `hello_cargo` tergolong sederhana, ia sekarang memakai banyak tooling nyata yang akan kamu pakai selama sisa karier Rust kamu. Faktanya, untuk mengerjakan proyek yang sudah ada, kamu bisa memakai perintah berikut untuk meng-clone kode memakai Git, pindah ke direktori proyek itu, lalu meng-build:

```console
$ git clone example.org/someproject
$ cd someproject
$ cargo build
```

Untuk informasi lebih lanjut tentang Cargo, lihat [dokumentasinya][cargo].

## Ringkasan

Kamu sudah memulai perjalanan Rust kamu dengan langkah yang bagus! Di bab ini, kamu sudah mempelajari cara:

- Memasang versi Rust stabil terbaru memakai `rustup`.
- Memperbarui ke versi Rust yang lebih baru.
- Membuka dokumentasi yang terpasang secara lokal.
- Menulis dan menjalankan program "Hello, world!" memakai `rustc` secara langsung.
- Membuat dan menjalankan proyek baru mengikuti konvensi Cargo.

Ini saat yang tepat untuk meng-build program yang lebih substansial agar terbiasa membaca dan menulis kode Rust. Jadi, di Bab 2, kita akan meng-build program permainan tebakan. Kalau kamu lebih suka mulai dengan mempelajari cara kerja konsep-konsep pemrograman umum di Rust, lihat Bab 3 lalu kembali ke Bab 2.

[installation]: ch01-01-installation.html#installation
[toml]: https://toml.io
[appendix-e]: appendix-05-editions.html
[cargo]: https://doc.rust-lang.org/cargo/
