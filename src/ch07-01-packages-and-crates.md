## Package dan Crate

Bagian pertama dari sistem module yang akan kita bahas adalah package dan crate.

_Crate_ adalah satuan kode terkecil yang diproses oleh compiler Rust pada satu
waktu. Bahkan kalau kamu menjalankan `rustc` alih-alih `cargo` dan mengirimkan
satu file kode sumber (seperti yang kita lakukan jauh sebelumnya di [“Dasar
Program Rust”][basics]<!-- ignore --> pada Bab 1), compiler tetap menganggap
file itu sebagai sebuah crate. Crate bisa berisi module, dan module tersebut
bisa didefinisikan di file lain yang ikut dikompilasi bersama crate-nya, seperti
yang akan kita lihat pada bagian-bagian berikutnya.

Crate bisa hadir dalam salah satu dari dua bentuk: binary crate atau library
crate. _Binary crate_ adalah program yang bisa kamu kompilasi menjadi executable
yang bisa dijalankan, misalnya program command line atau server. Setiap binary
crate harus punya fungsi bernama `main` yang mendefinisikan apa yang terjadi
ketika executable dijalankan. Semua crate yang kita buat sejauh ini semuanya
binary crate.

_Library crate_ tidak punya fungsi `main` dan tidak dikompilasi menjadi
executable. Sebagai gantinya, library crate mendefinisikan fungsionalitas yang
dipakai bersama oleh banyak proyek. Sebagai contoh, crate `rand` yang kita
gunakan di [Bab 2][rand]<!-- ignore --> menyediakan fungsionalitas untuk
menghasilkan angka acak. Sebagian besar waktu, ketika Rustacean menyebut
“crate”, yang mereka maksud adalah library crate, dan mereka memakai “crate”
sebagai padanan konsep pemrograman umum yaitu “library”.

_Crate root_ adalah file sumber tempat compiler Rust mulai bekerja, dan file itu
membentuk root module dari crate kamu (kita akan menjelaskan module secara
mendalam di [“Mengontrol Scope dan Privasi dengan Module”][modules]<!-- ignore
-->).

_Package_ adalah bundel berisi satu atau lebih crate yang menyediakan satu
kumpulan fungsionalitas. Package berisi file _Cargo.toml_ yang menjelaskan
cara build crate-crate tersebut. Sebenarnya Cargo adalah sebuah package yang
berisi binary crate untuk tool command line yang selama ini kamu pakai untuk
build kode kamu. Package Cargo juga berisi sebuah library crate yang menjadi
dependensi binary crate itu. Proyek lain bisa bergantung pada library crate
Cargo untuk memakai logika yang sama dengan yang dipakai tool command line
Cargo.

Sebuah package boleh berisi binary crate sebanyak yang kamu mau, tetapi paling
banyak hanya satu library crate. Package wajib berisi minimal satu crate, baik
itu library crate maupun binary crate.

Mari kita telusuri apa yang terjadi ketika kita membuat sebuah package.
Pertama, kita masukkan perintah `cargo new my-project`:

```console
$ cargo new my-project
     Created binary (application) `my-project` package
$ ls my-project
Cargo.toml
src
$ ls my-project/src
main.rs
```

Setelah menjalankan `cargo new my-project`, kita memakai `ls` untuk melihat apa
yang dibuat Cargo. Di direktori _my-project_ ada file _Cargo.toml_, sehingga
kita punya sebuah package. Di sana juga ada direktori _src_ yang berisi
_file main.rs_. Buka _Cargo.toml_ di text editor kamu dan perhatikan bahwa tidak
ada penyebutan _src/main.rs_. Cargo mengikuti konvensi bahwa _src/main.rs_ adalah
crate root dari binary crate yang namanya sama dengan nama package. Dengan cara
yang sama, Cargo tahu bahwa jika direktori package berisi _src/lib.rs_, berarti
package tersebut berisi library crate dengan nama yang sama dengan nama package,
dan _src/lib.rs_ adalah crate root-nya. Cargo meneruskan file-file crate root
tersebut ke `rustc` untuk build library atau binary-nya.

Di sini, kita punya package yang hanya berisi _src/main.rs_, artinya package itu
hanya berisi sebuah binary crate bernama `my-project`. Jika sebuah package berisi
_src/main.rs_ dan _src/lib.rs_, package itu punya dua crate: sebuah binary dan
sebuah library, keduanya bernama sama dengan nama package. Sebuah package bisa
punya beberapa binary crate dengan menempatkan file-file di direktori _src/bin_: Setiap file akan menjadi
binary crate yang terpisah.

[basics]: ch01-02-hello-world.html#rust-program-basics
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number
