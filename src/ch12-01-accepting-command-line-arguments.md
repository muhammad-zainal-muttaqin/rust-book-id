## Menerima Argumen Command Line

Mari kita buat proyek baru dengan, seperti biasa, `cargo new`. Kita akan menyebut proyek kita `minigrep` agar berbeda dari tool `grep` yang mungkin sudah ada di sistem kamu:

```console
$ cargo new minigrep
     Created binary (application) `minigrep` project
$ cd minigrep
```

Tugas pertama adalah membuat `minigrep` menerima dua argumen command line: path file dan string yang dicari. Dengan kata lain, kita ingin bisa menjalankan program kita dengan `cargo run`, dua tanda hubung untuk menandakan bahwa argumen setelahnya ditujukan untuk program kita, bukan untuk `cargo`, sebuah string yang dicari, dan path ke file tempat mencari, seperti ini:

```console
$ cargo run -- searchstring example-filename.txt
```

Saat ini, program yang dihasilkan oleh `cargo new` belum bisa memproses argumen yang kita berikan. Beberapa library yang sudah ada di [crates.io](https://crates.io/) bisa membantu menulis program yang menerima argumen command line, tetapi karena kamu baru belajar konsep ini, mari kita terapkan kemampuan ini sendiri.

### Membaca Nilai Argumen

Agar `minigrep` bisa membaca nilai argumen command line yang kita berikan kepadanya, kita membutuhkan fungsi `std::env::args` yang disediakan oleh library standar Rust. Fungsi ini mengembalikan iterator berisi argumen command line yang diberikan kepada `minigrep`. Kita akan membahas iterator secara lengkap di [Chapter 13][ch13]<!-- ignore -->. Untuk sekarang, kamu hanya perlu tahu dua hal tentang iterator: iterator menghasilkan serangkaian nilai, dan kita bisa memanggil method `collect` pada iterator untuk mengubahnya menjadi sebuah koleksi, seperti vector, yang berisi semua elemen yang dihasilkan iterator tersebut.

Kode di Listing 12-1 memungkinkan program `minigrep` kamu membaca argumen command line apa pun yang diberikan kepadanya, lalu mengumpulkan nilainya ke dalam sebuah vector.

<Listing number="12-1" file-name="src/main.rs" caption="Mengumpulkan argumen command line ke dalam vector dan mencetaknya">

```rust
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-01/src/main.rs}}
```

</Listing>

Pertama, kita memasukkan module `std::env` ke dalam scope dengan statement `use` agar bisa menggunakan fungsi `args`-nya. Perhatikan bahwa fungsi `std::env::args` bersarang dua tingkat di dalam module. Seperti yang kita bahas di [Chapter 7][ch7-idiomatic-use]<!-- ignore -->, ketika fungsi yang diinginkan bersarang di lebih dari satu module, kita memilih untuk memasukkan module induknya ke dalam scope alih-alih fungsinya. Dengan begitu, kita bisa dengan mudah menggunakan fungsi lain dari `std::env`. Cara ini juga lebih tidak ambigu daripada menambahkan `use std::env::args` lalu memanggil fungsinya cukup dengan `args`, karena `args` bisa dengan mudah dikira sebagai fungsi yang didefinisikan di module saat ini.

> ### Fungsi `args` dan Unicode yang Tidak Valid
>
> Perhatikan bahwa `std::env::args` akan panic jika ada argumen yang mengandung Unicode tidak valid. Jika program kamu perlu menerima argumen yang mengandung Unicode tidak valid, gunakan `std::env::args_os` sebagai gantinya. Fungsi itu mengembalikan iterator yang menghasilkan nilai `OsString`, bukan nilai `String`. Kita memilih memakai `std::env::args` di sini demi kesederhanaan karena nilai `OsString` berbeda-beda tiap platform dan lebih sulit dikerjakan daripada nilai `String`.

Di baris pertama `main`, kita memanggil `env::args`, lalu langsung menggunakan `collect` untuk mengubah iterator menjadi vector yang berisi semua nilai yang dihasilkan iterator tersebut. Kita bisa memakai fungsi `collect` untuk membuat berbagai macam koleksi, jadi kita secara eksplisit memberi anotasi tipe pada `args` untuk menentukan bahwa kita menginginkan vector berisi string. Meski kamu sangat jarang perlu memberi anotasi tipe di Rust, `collect` adalah salah satu fungsi yang sering kali perlu diberi anotasi karena Rust tidak bisa menyimpulkan jenis koleksi yang kamu inginkan.

Terakhir, kita mencetak vector tersebut menggunakan macro debug. Mari kita coba jalankan kode ini, pertama tanpa argumen, lalu dengan dua argumen:

```console
{{#include ../listings/ch12-an-io-project/listing-12-01/output.txt}}
```

```console
{{#include ../listings/ch12-an-io-project/output-only-01-with-args/output.txt}}
```

Perhatikan bahwa nilai pertama dalam vector adalah `"target/debug/minigrep"`, yaitu nama binary kita. Ini sesuai dengan perilaku daftar argumen di C, yang memungkinkan program memakai nama yang dipakai untuk memanggilnya saat dijalankan. Sering kali berguna untuk bisa mengakses nama program, misalnya jika kamu ingin mencetaknya di pesan atau mengubah perilaku program berdasarkan alias command line yang dipakai untuk memanggilnya. Namun untuk kebutuhan bab ini, kita akan mengabaikannya dan hanya menyimpan dua argumen yang kita butuhkan.

### Menyimpan Nilai Argumen dalam Variabel

Saat ini program sudah bisa mengakses nilai-nilai yang ditentukan sebagai argumen command line. Sekarang kita perlu menyimpan nilai kedua argumen itu dalam variabel agar bisa memakainya di seluruh sisa program. Kita melakukan itu di Listing 12-2.

<Listing number="12-2" file-name="src/main.rs" caption="Membuat variabel untuk menampung argumen query dan argumen path file">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-02/src/main.rs}}
```

</Listing>

Seperti yang kita lihat saat mencetak vector, nama program menempati nilai pertama di vector pada `args[0]`, jadi kita mulai argumen dari indeks 1. Argumen pertama yang diterima `minigrep` adalah string yang kita cari, jadi kita memasukkan reference ke argumen pertama ke dalam variabel `query`. Argumen kedua adalah path file, jadi kita memasukkan reference ke argumen kedua ke dalam variabel `file_path`.

Kita sementara mencetak nilai variabel-variabel ini untuk membuktikan bahwa kode bekerja sesuai rencana. Mari jalankan lagi program ini dengan argumen `test` dan `sample.txt`:

```console
{{#include ../listings/ch12-an-io-project/listing-12-02/output.txt}}
```

Mantap, programnya berhasil! Nilai argumen yang kita butuhkan tersimpan di variabel yang tepat. Nanti kita akan menambahkan penanganan error untuk mengatasi sejumlah situasi yang berpotensi bermasalah, misalnya saat pengguna tidak memberikan argumen; untuk sekarang, kita abaikan dulu situasi itu dan kerjakan penambahan kemampuan membaca file.

[ch13]: ch13-00-functional-features.html
[ch7-idiomatic-use]: ch07-04-bringing-paths-into-scope-with-the-use-keyword.html#creating-idiomatic-use-paths
