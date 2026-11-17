## Cargo Workspaces

Di Bab 12, kita membangun sebuah package yang berisi sebuah binary crate dan sebuah library crate. Seiring proyekmu berkembang, mungkin kamu mendapati library crate terus membesar dan ingin memecah package lebih lanjut menjadi beberapa library crate. Cargo menyediakan fitur bernama _workspaces_ yang bisa membantu mengelola beberapa package terkait yang dikembangkan secara bersamaan.

### Membuat Workspace

Sebuah _workspace_ adalah kumpulan package yang berbagi _Cargo.lock_ dan direktori output yang sama. Mari kita buat sebuah proyek memakai workspace—kita akan memakai kode yang sederhana agar bisa fokus pada struktur workspacenya. Ada beberapa cara menyusun workspace, jadi kita akan menunjukkan satu cara yang umum. Kita akan membuat workspace yang berisi satu binary dan dua library. Binary yang menyediakan fungsi utama akan bergantung pada kedua library itu. Satu library menyediakan fungsi `add_one` dan library lainnya fungsi `add_two`. Ketiga crate ini akan menjadi bagian dari workspace yang sama. Kita mulai dengan membuat direktori baru untuk workspace:

```console
$ mkdir add
$ cd add
```

Berikutnya, di direktori _add_, kita membuat file _Cargo.toml_ yang akan mengonfigurasi seluruh workspace. File ini tidak akan punya bagian `[package]`. Sebaliknya, file ini dimulai dengan bagian `[workspace]` yang memungkinkan kita menambahkan anggota ke dalam workspace. Kita juga memastikan memakai versi terbaru dan terbaik dari algoritma resolver Cargo di workspace dengan menetapkan nilai `resolver` menjadi `"3"`:

<span class="filename">Nama file: Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-01-workspace/add/Cargo.toml}}
```

Berikutnya, kita akan membuat binary crate `adder` dengan menjalankan `cargo new` di dalam direktori _add_:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-01-adder-crate/add
remove `members = ["adder"]` from Cargo.toml
rm -rf adder
cargo new adder
copy output below
-->

```console
$ cargo new adder
     Created binary (application) `adder` package
      Adding `adder` as member of workspace at `file:///projects/add`
```

Menjalankan `cargo new` di dalam workspace juga otomatis menambahkan package yang baru dibuat ke kunci `members` dalam definisi `[workspace]` di _Cargo.toml_ workspace, seperti ini:

```toml
{{#include ../listings/ch14-more-about-cargo/output-only-01-adder-crate/add/Cargo.toml}}
```

Pada titik ini, kita bisa build workspace dengan menjalankan `cargo build`. File-file di direktori _add_ milikmu seharusnya terlihat seperti ini:

```text
├── Cargo.lock
├── Cargo.toml
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

Workspace punya satu direktori _target_ di level teratas tempat hasil kompilasi ditempatkan; package `adder` tidak punya direktori _target_-nya sendiri. Bahkan jika kita menjalankan `cargo build` dari dalam direktori _adder_, hasil kompilasinya tetap akan berakhir di _add/target_, bukan _add/adder/target_. Cargo menyusun direktori _target_ di dalam workspace seperti ini karena crate-crate dalam workspace memang dirancang untuk saling bergantung. Jika setiap crate punya direktori _target_-nya sendiri, masing-masing crate harus mengompilasi ulang setiap crate lain di workspace untuk menaruh hasil kompilasinya di direktori _target_-nya sendiri. Dengan berbagi satu direktori _target_, para crate bisa menghindari build ulang yang tidak perlu.

### Membuat Package Kedua di dalam Workspace

Berikutnya, mari kita buat package anggota lain di workspace dan menamainya `add_one`. Hasilkan sebuah library crate baru bernama `add_one`:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-02-add-one/add
remove `"add_one"` from `members` list in Cargo.toml
rm -rf add_one
cargo new add_one --lib
copy output below
-->

```console
$ cargo new add_one --lib
     Created library `add_one` package
      Adding `add_one` as member of workspace at `file:///projects/add`
```

_Cargo.toml_ di level teratas sekarang akan menyertakan path _add_one_ dalam daftar `members`:

<span class="filename">Nama file: Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/Cargo.toml}}
```

Direktori _add_ milikmu sekarang seharusnya punya direktori dan file-file ini:

```text
├── Cargo.lock
├── Cargo.toml
├── add_one
│   ├── Cargo.toml
│   └── src
│       └── lib.rs
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

Di file _add_one/src/lib.rs_, mari kita tambahkan fungsi `add_one`:

<span class="filename">Nama file: add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/add_one/src/lib.rs}}
```

Sekarang kita bisa membuat package `adder` yang berisi binary bergantung pada package `add_one` yang berisi library kita. Pertama, kita perlu menambahkan dependensi path pada `add_one` ke _adder/Cargo.toml_.

<span class="filename">Nama file: adder/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/adder/Cargo.toml:6:7}}
```

Cargo tidak mengasumsikan bahwa crate-crate dalam workspace akan saling bergantung, jadi kita perlu menyatakan hubungan dependensinya secara eksplisit.

Berikutnya, mari kita pakai fungsi `add_one` (dari crate `add_one`) di dalam crate `adder`. Buka file _adder/src/main.rs_ dan ubah fungsi `main` agar memanggil fungsi `add_one`, seperti pada Listing 14-7.

<Listing number="14-7" file-name="adder/src/main.rs" caption="Memakai library crate `add_one` dari crate `adder`">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-07/add/adder/src/main.rs}}
```

</Listing>

Mari build workspace dengan menjalankan `cargo build` di direktori _add_ level teratas!

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.22s
```

Untuk menjalankan binary crate dari direktori _add_, kita bisa menentukan package mana di workspace yang ingin dijalankan dengan memakai argumen `-p` dan nama package bersama `cargo run`:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo run -p adder
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo run -p adder
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running `target/debug/adder`
Hello, world! 10 plus one is 11!
```

Ini menjalankan kode di _adder/src/main.rs_, yang bergantung pada crate `add_one`.

<!-- Old headings. Do not remove or links may break. -->

<a id="depending-on-an-external-package-in-a-workspace"></a>

### Bergantung pada Package Eksternal

Perhatikan bahwa workspace hanya punya satu file _Cargo.lock_ di level teratas, bukan sebuah _Cargo.lock_ di direktori masing-masing crate. Ini memastikan semua crate memakai versi yang sama dari semua dependensi. Jika kita menambahkan package `rand` ke file _adder/Cargo.toml_ dan _add_one/Cargo.toml_, Cargo akan menyelesaikan keduanya menjadi satu versi `rand` dan mencatatnya di _Cargo.lock_ yang satu itu. Dengan membuat semua crate di workspace memakai dependensi yang sama, para crate akan selalu kompatibel satu sama lain. Mari tambahkan crate `rand` ke bagian `[dependencies]` di file _add_one/Cargo.toml_ agar kita bisa memakai crate `rand` di dalam crate `add_one`:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
-->

<span class="filename">Nama file: add_one/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add/add_one/Cargo.toml:6:7}}
```

Sekarang kita bisa menambahkan `use rand;` ke file _add_one/src/lib.rs_, dan build seluruh workspace dengan menjalankan `cargo build` di direktori _add_ akan mengambil dan mengompilasi crate `rand`. Kita akan mendapat satu warning karena kita tidak merujuk ke `rand` yang sudah kita bawa ke scope:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
    Updating crates.io index
  Downloaded rand v0.10.1
   --snip--
   Compiling rand v0.10.1
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
warning: unused import: `rand`
 --> add_one/src/lib.rs:1:5
  |
1 | use rand;
  |     ^^^^
  |
  = note: `#[warn(unused_imports)]` (part of `#[warn(unused)]`) on by default

warning: `add_one` (lib) generated 1 warning (run `cargo fix --lib -p add_one` to apply 1 suggestion)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.95s
```

_Cargo.lock_ di level teratas sekarang berisi informasi tentang dependensi `add_one` pada `rand`. Namun, meskipun `rand` dipakai di suatu tempat di workspace, kita tidak bisa memakainya di crate lain dalam workspace kecuali kita menambahkan `rand` ke file _Cargo.toml_ mereka juga. Misalnya, jika kita menambahkan `use rand;` ke file _adder/src/main.rs_ untuk package `adder`, kita akan mendapat error:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-03-use-rand/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
  --snip--
   Compiling adder v0.1.0 (file:///projects/add/adder)
error[E0432]: unresolved import `rand`
 --> adder/src/main.rs:2:5
  |
2 | use rand;
  |     ^^^^ no external crate `rand`
```

Untuk memperbaikinya, edit file _Cargo.toml_ untuk package `adder` dan nyatakan bahwa `rand` juga merupakan dependensinya. Build package `adder` akan menambahkan `rand` ke daftar dependensi untuk `adder` di _Cargo.lock_, tetapi tidak ada salinan tambahan `rand` yang akan diunduh. Cargo akan memastikan setiap crate di setiap package dalam workspace yang memakai package `rand` memakai versi yang sama selama mereka menentukan versi `rand` yang kompatibel, sehingga menghemat ruang dan memastikan crate-crate di workspace kompatibel satu sama lain.

Jika crate-crate di workspace menentukan versi yang tidak kompatibel dari dependensi yang sama, Cargo akan menyelesaikan masing-masing, tetapi tetap berusaha menyelesaikan sesedikit mungkin versi.

### Menambahkan Test ke dalam Workspace

Sebagai penyempurnaan lain, mari kita tambahkan test untuk fungsi `add_one::add_one` di dalam crate `add_one`:

<span class="filename">Nama file: add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add/add_one/src/lib.rs}}
```

Sekarang jalankan `cargo test` di direktori _add_ level teratas. Menjalankan `cargo test` di workspace yang disusun seperti ini akan menjalankan test untuk semua crate di workspace:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test
copy output below; the output updating script doesn't handle subdirectories in
paths properly
-->

```console
$ cargo test
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.20s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (target/debug/deps/adder-3a47283c568d2b6a)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

Bagian pertama dari output menunjukkan bahwa test `it_works` di crate `add_one` lulus. Bagian berikutnya menunjukkan bahwa tidak ada test yang ditemukan di crate `adder`, lalu bagian terakhir menunjukkan bahwa tidak ada documentation test yang ditemukan di crate `add_one`.

Kita juga bisa menjalankan test untuk satu crate tertentu di workspace dari direktori level teratas dengan memakai flag `-p` dan menentukan nama crate yang ingin kita test:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test -p add_one
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo test -p add_one
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

Output ini menunjukkan `cargo test` hanya menjalankan test untuk crate `add_one` dan tidak menjalankan test crate `adder`.

Jika kamu mempublikasikan crate-crate di workspace ke [crates.io](https://crates.io/)<!-- ignore -->, setiap crate di workspace perlu dipublikasikan secara terpisah. Seperti `cargo test`, kita bisa mempublikasikan satu crate tertentu di workspace dengan memakai flag `-p` dan menentukan nama crate yang ingin kita publikasikan.

Untuk latihan tambahan, tambahkan crate `add_two` ke workspace ini dengan cara yang mirip dengan crate `add_one`!

Seiring proyekmu bertumbuh, pertimbangkan untuk memakai workspace: ini memungkinkan kamu bekerja dengan komponen-komponen yang lebih kecil dan lebih mudah dipahami daripada satu gumpalan kode besar. Selain itu, menyimpan crate-crate dalam workspace bisa membuat koordinasi antarcrate lebih mudah jika mereka sering diubah bersamaan.
