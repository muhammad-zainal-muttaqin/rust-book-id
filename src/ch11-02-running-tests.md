<a id="controlling-how-tests-are-run"></a>
## Mengontrol Cara Test Dijalankan

Sama seperti `cargo run` yang mengompilasi kode kamu lalu menjalankan biner yang
dihasilkan, `cargo test` mengompilasi kode kamu dalam mode test dan menjalankan
biner test yang dihasilkan. Secara default, biner yang dihasilkan `cargo test`
menjalankan semua test secara paralel dan menangkap output yang dibuat selama
test berjalan, sehingga output itu tidak ditampilkan dan output yang berkaitan
dengan hasil test lebih mudah dibaca. Namun, kamu bisa menentukan opsi command
line untuk mengubah perilaku default ini.

Sebagian opsi command line ditujukan ke `cargo test`, dan sebagian lagi ke biner
test yang dihasilkan. Untuk memisahkan kedua jenis argumen ini, tuliskan argumen
untuk `cargo test` lebih dulu, lalu pemisah `--`, kemudian argumen untuk biner
test. Menjalankan `cargo test --help` menampilkan opsi yang bisa kamu pakai
dengan `cargo test`, sedangkan `cargo test -- --help` menampilkan opsi yang bisa
dipakai setelah pemisah. Opsi-opsi ini juga didokumentasikan di [bagian “Tests”
dalam _The `rustc` Book_][tests].

[tests]: https://doc.rust-lang.org/rustc/tests/index.html

### Menjalankan Test Secara Paralel atau Berurutan

Saat kamu menjalankan beberapa test, secara default test-test itu berjalan
secara paralel menggunakan thread, sehingga selesai lebih cepat dan kamu
mendapat umpan balik lebih awal. Karena test-test itu berjalan bersamaan, kamu
harus memastikan test-test kamu tidak saling bergantung atau bergantung pada
state bersama, termasuk lingkungan bersama, seperti direktori kerja saat ini
atau variabel lingkungan.

Misalnya, anggaplah setiap test kamu menjalankan kode yang membuat file di disk
bernama _test-output.txt_ dan menulis sejumlah data ke file itu. Lalu, setiap
test membaca data di file tersebut dan menegaskan bahwa file itu berisi nilai
tertentu yang berbeda di setiap test. Karena test-test itu berjalan bersamaan,
satu test bisa menimpa file di antara waktu test lain menulis dan membaca file
itu. Test kedua lalu gagal—bukan karena kodenya salah, melainkan karena
test-test itu saling mengganggu saat berjalan secara paralel. Salah satu
solusinya adalah memastikan setiap test menulis ke file yang berbeda; solusi
lainnya adalah menjalankan test satu per satu.

Jika kamu tidak ingin menjalankan test secara paralel atau ingin kontrol yang
lebih detail atas jumlah thread yang dipakai, kamu bisa mengirimkan flag
`--test-threads` beserta jumlah thread yang ingin kamu gunakan ke biner test.
Perhatikan contoh berikut:

```console
$ cargo test -- --test-threads=1
```

Kita menetapkan jumlah thread test menjadi `1`, memberi tahu program untuk tidak
memakai paralelisme sama sekali. Menjalankan test dengan satu thread memang
lebih lama dibanding menjalankannya secara paralel, tetapi test-test itu tidak
akan saling mengganggu jika mereka berbagi state.

### Menampilkan Output Fungsi

Secara default, jika sebuah test lulus, library test Rust menangkap apa pun yang
dicetak ke standard output. Misalnya, jika kita memanggil `println!` di dalam
test dan test itu lulus, kita tidak akan melihat output `println!` itu di
terminal; kita hanya akan melihat baris yang menandakan test itu lulus. Jika
test gagal, kita akan melihat apa pun yang dicetak ke standard output bersama
pesan kegagalan lainnya.

Sebagai contoh, Listing 11-10 berisi fungsi sederhana yang mencetak nilai
parameternya dan mengembalikan 10, serta sebuah test yang lulus dan sebuah test
yang gagal.

<Listing number="11-10" file-name="src/lib.rs" caption="Test untuk fungsi yang memanggil `println!`">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-10/src/lib.rs}}
```

</Listing>

Saat kita menjalankan test-test ini dengan `cargo test`, kita akan melihat
output berikut:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-10/output.txt}}
```

Perhatikan bahwa di seluruh output ini kita tidak melihat `I got the value 4`,
yang dicetak saat test yang lulus berjalan. Output itu sudah ditangkap. Output
dari test yang gagal, `I got the value 8`, muncul di bagian ringkasan hasil
test, yang juga menampilkan penyebab kegagalan test itu.

Jika kita ingin melihat nilai yang dicetak oleh test yang lulus juga, kita bisa
meminta Rust untuk menampilkan output test yang berhasil dengan `--show-output`:

```console
$ cargo test -- --show-output
```

Saat kita menjalankan kembali test di Listing 11-10 dengan flag `--show-output`,
kita melihat output berikut:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-01-show-output/output.txt}}
```

<a id="running-a-subset-of-tests-by-name"></a>
### Menjalankan Sebagian Test Berdasarkan Nama

Menjalankan seluruh rangkaian test kadang bisa memakan waktu lama. Jika kamu
sedang mengerjakan kode di area tertentu, kamu mungkin ingin menjalankan hanya
test yang berkaitan dengan kode itu. Kamu bisa memilih test mana yang dijalankan
dengan memberikan nama satu atau beberapa test yang ingin kamu jalankan sebagai
argumen ke `cargo test`.

Untuk menunjukkan cara menjalankan sebagian test, kita akan membuat tiga test
untuk fungsi `add_two` kita, seperti yang ditunjukkan di Listing 11-11, lalu
memilih mana yang akan dijalankan.

<Listing number="11-11" file-name="src/lib.rs" caption="Tiga test dengan tiga nama yang berbeda">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-11/src/lib.rs}}
```

</Listing>

Jika kita menjalankan test tanpa memberikan argumen apa pun, seperti yang kita
lihat sebelumnya, semua test akan berjalan secara paralel:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-11/output.txt}}
```

#### Menjalankan Satu Test

Kita bisa memberikan nama fungsi test mana pun ke `cargo test` untuk menjalankan
hanya test itu:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-02-single-test/output.txt}}
```

Hanya test bernama `one_hundred` yang dijalankan; dua test lainnya tidak cocok
dengan nama itu. Output test memberi tahu kita bahwa ada test lain yang tidak
dijalankan dengan menampilkan `2 filtered out` di akhir.

Kita tidak bisa menentukan nama beberapa test dengan cara ini; hanya nilai
pertama yang diberikan ke `cargo test` yang dipakai. Tetapi ada cara untuk
menjalankan beberapa test.

#### Memfilter untuk Menjalankan Beberapa Test

Kita bisa menentukan sebagian nama test, dan test mana pun yang namanya cocok
dengan nilai itu akan dijalankan. Misalnya, karena dua nama test kita mengandung
`add`, kita bisa menjalankan keduanya dengan `cargo test add`:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-03-multiple-tests/output.txt}}
```

Perintah ini menjalankan semua test yang memiliki `add` di namanya dan menyaring
test bernama `one_hundred`. Perhatikan juga bahwa module tempat sebuah test
berada menjadi bagian dari nama test itu, sehingga kita bisa menjalankan semua
test dalam sebuah module dengan memfilter berdasarkan nama module-nya.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-some-tests-unless-specifically-requested"></a>

<a id="ignoring-tests-unless-specifically-requested"></a>
### Mengabaikan Test Kecuali Diminta Secara Khusus

Kadang beberapa test tertentu bisa sangat memakan waktu untuk dijalankan,
sehingga kamu mungkin ingin mengecualikannya pada sebagian besar jalannya
`cargo test`. Alih-alih mencantumkan sebagai argumen semua test yang memang ingin
kamu jalankan, kamu bisa menandai test yang memakan waktu itu dengan atribut
`ignore` agar dikecualikan, seperti yang ditunjukkan di sini:

<span class="filename">Nama file: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/src/lib.rs:here}}
```

Setelah `#[test]`, kita menambahkan baris `#[ignore]` pada test yang ingin kita
kecualikan. Sekarang saat kita menjalankan test, `it_works` berjalan, tetapi
`expensive_test` tidak:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/output.txt}}
```

Fungsi `expensive_test` tercantum sebagai `ignored`. Jika kita ingin menjalankan
hanya test yang diabaikan, kita bisa memakai `cargo test -- --ignored`:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-04-running-ignored/output.txt}}
```

Dengan mengontrol test mana yang dijalankan, kamu bisa memastikan hasil
`cargo test` dikembalikan dengan cepat. Saat tibanya waktu yang tepat untuk
memeriksa hasil test `ignored` dan kamu punya waktu untuk menunggu, kamu bisa
menjalankan `cargo test -- --ignored` sebagai gantinya. Jika kamu ingin
menjalankan semua test, baik yang diabaikan maupun tidak, kamu bisa menjalankan
`cargo test -- --include-ignored`.
