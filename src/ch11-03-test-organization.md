## Organisasi Test

Seperti yang disebutkan di awal bab ini, testing adalah disiplin yang kompleks, dan tiap orang memakai istilah serta cara pengorganisasian yang berbeda. Komunitas Rust memandang test dalam dua kategori utama: unit test dan integration test. _Unit test_ berukuran kecil dan lebih terfokus, menguji satu module secara terpisah pada satu waktu, serta bisa menguji antarmuka private. _Integration test_ sepenuhnya berada di luar library kamu dan memakai kode kamu seperti layaknya kode eksternal lainnya, hanya menggunakan antarmuka publik dan bisa jadi melibatkan beberapa module dalam satu test.

Menulis kedua jenis test itu penting untuk memastikan bagian-bagian library kamu melakukan apa yang kamu harapkan, baik secara terpisah maupun bersama-sama.

### Unit Test

Tujuan unit test adalah menguji setiap unit kode secara terpisah dari kode lainnya agar kita bisa dengan cepat menemukan bagian mana yang bekerja dan mana yang tidak sesuai harapan. Kamu akan meletakkan unit test di direktori _src_, di dalam setiap file yang berisi kode yang diuji. Kebiasaannya, kamu membuat module bernama `tests` di tiap file untuk menampung fungsi-fungsi test, lalu menandai module itu dengan `cfg(test)`.

#### Module `tests` dan `#[cfg(test)]`

Anotasi `#[cfg(test)]` pada module `tests` memberi tahu Rust untuk mengompilasi dan menjalankan kode test hanya saat kamu menjalankan `cargo test`, bukan saat menjalankan `cargo build`. Ini menghemat waktu kompilasi saat kamu hanya ingin membangun library, sekaligus menghemat ruang pada hasil kompilasi karena test tidak ikut disertakan. Kamu akan melihat bahwa karena integration test ditempatkan di direktori lain, mereka tidak memerlukan anotasi `#[cfg(test)]`. Namun, karena unit test berada di file yang sama dengan kode, kamu memakai `#[cfg(test)]` untuk menentukan bahwa test-test itu tidak boleh disertakan dalam hasil kompilasi.

Ingatlah bahwa saat kita membuat proyek baru `adder` di bagian pertama bab ini, Cargo menghasilkan kode ini untuk kita:

<span class="filename">Filename: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

Pada module `tests` yang dihasilkan otomatis itu, atribut `cfg` adalah singkatan dari _configuration_ dan memberi tahu Rust bahwa item setelahnya hanya boleh disertakan apabila ada opsi konfigurasi tertentu. Dalam kasus ini, opsi konfigurasi tersebut adalah `test`, yang disediakan Rust untuk mengompilasi dan menjalankan test. Dengan memakai atribut `cfg`, Cargo mengompilasi kode test kita hanya jika kita secara aktif menjalankan test dengan `cargo test`. Ini juga mencakup fungsi-fungsi pembantu yang mungkin ada di dalam module ini, selain fungsi-fungsi yang ditandai dengan `#[test]`.

<!-- Old headings. Do not remove or links may break. -->

<a id="testing-private-functions"></a>

#### Test Fungsi Private

Ada perdebatan di kalangan komunitas testing soal apakah fungsi private sebaiknya diuji langsung atau tidak, dan bahasa lain ada yang membuat pengujian fungsi private menjadi sulit atau bahkan mustahil. Apapun aliran testing yang kamu ikuti, aturan privasi Rust tetap mengizinkan kamu menguji fungsi private. Perhatikan kode pada Listing 11-12 dengan fungsi private `internal_adder`.

<Listing number="11-12" file-name="src/lib.rs" caption="Testing a private function">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-12/src/lib.rs}}
```

</Listing>

Perhatikan bahwa fungsi `internal_adder` tidak ditandai sebagai `pub`. Test hanyalah kode Rust, dan module `tests` hanyalah module biasa. Seperti yang kita bahas di [“Paths for Referring to an Item in the Module Tree”][paths]<!-- ignore -->, item di dalam module anak bisa memakai item dari module induknya. Dalam test ini, kita membawa semua item milik induk module `tests` ke dalam scope dengan `use super::*`, lalu test itu bisa memanggil `internal_adder`. Kalau kamu berpendapat bahwa fungsi private tidak perlu diuji, tidak ada satupun dalam Rust yang memaksamu melakukannya.

### Integration Test

Di Rust, integration test sepenuhnya berada di luar library kamu. Mereka memakai library kamu seperti kode lainnya, yang berarti mereka hanya bisa memanggil fungsi-fungsi yang merupakan bagian dari API publik library kamu. Tujuannya adalah menguji apakah banyak bagian dari library kamu bekerja bersama dengan benar. Unit kode yang bekerja dengan benar secara mandiri bisa saja bermasalah saat digabungkan, jadi cakupan test pada kode yang sudah terintegrasi juga penting. Untuk membuat integration test, kamu pertama-tama memerlukan direktori _tests_.

#### Direktori _tests_

Kita membuat direktori _tests_ di level teratas direktori proyek, bersebelahan dengan _src_. Cargo tahu bahwa ia harus mencari file integration test di direktori ini. Setelah itu, kita bisa membuat sebanyak apapun file test yang kita mau, dan Cargo akan mengompilasi masing-masing file sebagai crate tersendiri.

Mari kita buat sebuah integration test. Dengan kode dari Listing 11-12 masih berada di file _src/lib.rs_, buatlah direktori _tests_, lalu buat file baru bernama _tests/integration_test.rs_. Struktur direktori kamu seharusnya terlihat seperti ini:

```text
adder
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    └── integration_test.rs
```

Masukkan kode dari Listing 11-13 ke dalam file _tests/integration_test.rs_.

<Listing number="11-13" file-name="tests/integration_test.rs" caption="An integration test of a function in the `adder` crate">

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-13/tests/integration_test.rs}}
```

</Listing>

Setiap file di direktori _tests_ adalah crate tersendiri, jadi kita perlu membawa library kita ke dalam scope tiap crate test. Untuk itulah kita menambahkan `use adder::add_two;` di bagian atas kode, yang tidak kita perlukan pada unit test.

Kita tidak perlu menandai kode apapun di _tests/integration_test.rs_ dengan `#[cfg(test)]`. Cargo memperlakukan direktori _tests_ secara khusus dan hanya mengompilasi file-file di direktori ini saat kita menjalankan `cargo test`. Sekarang jalankan `cargo test`:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-13/output.txt}}
```

Tiga bagian pada keluaran itu mencakup unit test, integration test, dan doc test. Perhatikan bahwa jika ada test yang gagal di sebuah bagian, bagian-bagian setelahnya tidak akan dijalankan. Misalnya, jika sebuah unit test gagal, tidak akan ada keluaran untuk integration test dan doc test, karena test-test itu hanya akan dijalankan jika semua unit test lulus.

Bagian pertama untuk unit test sama seperti yang terus kita lihat: satu baris untuk setiap unit test (satu bernama `internal` yang kita tambahkan di Listing 11-12), lalu satu baris ringkasan untuk unit test.

Bagian integration test dimulai dengan baris `Running tests/integration_test.rs`. Berikutnya, ada satu baris untuk setiap fungsi test dalam integration test itu dan satu baris ringkasan untuk hasil integration test tepat sebelum bagian `Doc-tests adder` dimulai.

Setiap file integration test punya bagiannya sendiri, jadi kalau kita menambahkan lebih banyak file di direktori _tests_, akan ada lebih banyak bagian integration test.

Kita tetap bisa menjalankan satu fungsi integration test tertentu dengan menentukan nama fungsi itu sebagai argumen untuk `cargo test`. Untuk menjalankan semua test di dalam satu file integration test tertentu, gunakan argumen `--test` dari `cargo test` yang diikuti nama file tersebut:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-05-single-integration/output.txt}}
```

Perintah ini hanya menjalankan test-test di dalam file _tests/integration_test.rs_.

#### Submodule dalam Integration Test

Saat kamu menambahkan lebih banyak integration test, kamu mungkin ingin membuat lebih banyak file di direktori _tests_ untuk membantu mengorganisasinya; misalnya, kamu bisa mengelompokkan fungsi-fungsi test berdasarkan fungsionalitas yang mereka uji. Seperti disebutkan sebelumnya, setiap file di direktori _tests_ dikompilasi sebagai crate tersendiri, yang berguna untuk membuat scope terpisah agar lebih menyerupai cara pemakai akhir memakai crate kamu. Namun, ini berarti file-file di direktori _tests_ tidak berperilaku sama seperti file-file di _src_, seperti yang kamu pelajari di Bab 7 tentang cara memisahkan kode ke dalam module dan file.

Perbedaan perilaku file-file di direktori _tests_ ini paling terasa saat kamu memiliki sekumpulan fungsi pembantu yang dipakai di beberapa file integration test, lalu kamu mencoba mengikuti langkah-langkah di bagian [“Separating Modules into Different Files”][separating-modules-into-files]<!-- ignore --> Bab 7 untuk mengekstraknya menjadi module bersama. Misalnya, jika kita membuat _tests/common.rs_ dan meletakkan fungsi bernama `setup` di dalamnya, kita bisa menambahkan kode ke `setup` yang ingin kita panggil dari beberapa fungsi test di beberapa file test:

<span class="filename">Filename: tests/common.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/tests/common.rs}}
```

Saat kita menjalankan test lagi, kita akan melihat bagian baru pada keluaran test untuk file _common.rs_, meskipun file ini tidak berisi fungsi test apapun dan kita juga tidak memanggil fungsi `setup` dari mana pun:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/output.txt}}
```

Munculnya `common` di hasil test dengan tampilan `running 0 tests` bukanlah yang kita inginkan. Kita hanya ingin berbagi kode dengan file-file integration test lainnya. Untuk menghindari `common` muncul di keluaran test, alih-alih membuat _tests/common.rs_, kita akan membuat _tests/common/mod.rs_. Sekarang direktori proyek terlihat seperti ini:

```text
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    ├── common
    │   └── mod.rs
    └── integration_test.rs
```

Ini adalah konvensi penamaan lama yang juga masih dipahami Rust dan kita singgung di [“Alternate File Paths”][alt-paths]<!-- ignore --> Bab 7. Menamai file dengan cara ini memberi tahu Rust agar tidak memperlakukan module `common` sebagai file integration test. Saat kita memindahkan kode fungsi `setup` ke _tests/common/mod.rs_ dan menghapus file _tests/common.rs_, bagian itu di keluaran test tidak akan muncul lagi. File-file di dalam subdirectory direktori _tests_ tidak dikompilasi sebagai crate terpisah atau punya bagian tersendiri di keluaran test.

Setelah kita membuat _tests/common/mod.rs_, kita bisa memakainya dari file integration test manapun sebagai sebuah module. Berikut contoh memanggil fungsi `setup` dari test `it_adds_two` di _tests/integration_test.rs_:

<span class="filename">Filename: tests/integration_test.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-13-fix-shared-test-code-problem/tests/integration_test.rs}}
```

Perhatikan bahwa deklarasi `mod common;` sama dengan deklarasi module yang kita tunjukkan di Listing 7-21. Lalu, di dalam fungsi test, kita bisa memanggil fungsi `common::setup()`.

#### Integration Test untuk Crate Biner

Jika proyek kita adalah crate biner yang hanya berisi file _src/main.rs_ dan tidak punya file _src/lib.rs_, kita tidak bisa membuat integration test di direktori _tests_ lalu membawa fungsi-fungsi yang didefinisikan di file _src/main.rs_ ke dalam scope dengan pernyataan `use`. Hanya crate library yang mengekspos fungsi yang bisa dipakai crate lain; crate biner memang ditujukan untuk dijalankan sendiri.

Ini adalah salah satu alasan mengapa proyek Rust yang menyediakan biner punya file _src/main.rs_ yang sederhana yang memanggil logika yang berada di file _src/lib.rs_. Dengan struktur seperti itu, integration test _bisa_ menguji crate library dengan `use` agar fungsionalitas penting tersedia. Jika fungsionalitas penting itu bekerja, sedikit kode di file _src/main.rs_ juga akan bekerja, dan sedikit kode itu tidak perlu diuji.

## Ringkasan

Fitur testing Rust menyediakan cara untuk menentukan bagaimana kode seharusnya bekerja guna memastikan kode itu terus bekerja sesuai harapan, bahkan saat kamu melakukan perubahan. Unit test menguji bagian-bagian berbeda dari sebuah library secara terpisah dan bisa menguji detail implementasi private. Integration test memeriksa apakah banyak bagian dari library bekerja bersama dengan benar, dan mereka memakai API publik library untuk menguji kode dengan cara yang sama seperti kode eksternal akan memakainya. Meskipun sistem tipe dan aturan ownership Rust membantu mencegah beberapa jenis bug, test tetap penting untuk mengurangi bug logika yang berkaitan dengan perilaku yang diharapkan dari kode kamu.

Mari kita gabungkan pengetahuan yang kamu pelajari di bab ini dan bab-bab sebelumnya untuk mengerjakan sebuah proyek!

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
[separating-modules-into-files]: ch07-05-separating-modules-into-different-files.html
[alt-paths]: ch07-05-separating-modules-into-different-files.html#alternate-file-paths
