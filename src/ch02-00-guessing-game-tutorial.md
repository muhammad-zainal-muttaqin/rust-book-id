# Memprogram Game Tebak-Tebakan

Ayo langsung praktik dengan Rust lewat sebuah proyek nyata! Bab ini memperkenalkan beberapa konsep Rust yang umum dengan menunjukkan cara menggunakannya dalam program sungguhan. Kamu akan belajar tentang `let`, `match`, method, fungsi terkait, crate eksternal, dan masih banyak lagi! Pada bab-bab berikutnya, kita akan membahas ide-ide ini lebih rinci. Di bab ini, kamu cukup berlatih dasar-dasarnya.

Kita akan mengimplementasikan sebuah soal pemrograman pemula yang klasik: game tebak-tebakan. Begini cara kerjanya: program akan menghasilkan bilangan bulat acak antara 1 dan 100. Lalu program meminta pemain memasukkan tebakan. Setelah tebakan dimasukkan, program memberi tahu apakah tebakan itu terlalu kecil atau terlalu besar. Jika tebakannya tepat, game akan mencetak pesan selamat dan keluar.

## Menyiapkan Proyek Baru

Untuk menyiapkan proyek baru, buka direktori _projects_ yang kamu buat di Bab 1 dan buat proyek baru dengan Cargo, seperti ini:

```console
$ cargo new guessing_game
$ cd guessing_game
```

Perintah pertama, `cargo new`, menerima nama proyek (`guessing_game`) sebagai argumen pertama. Perintah kedua berpindah ke direktori proyek baru itu.

Lihat file _Cargo.toml_ yang dihasilkan:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial
rm -rf no-listing-01-cargo-new
cargo new no-listing-01-cargo-new --name guessing_game
cd no-listing-01-cargo-new
cargo run > output.txt 2>&1
cd ../../..
-->

<span class="filename">Filename: Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/Cargo.toml}}
```

Seperti yang kamu lihat di Bab 1, `cargo new` menghasilkan program “Hello, world!” untukmu. Lihat file _src/main.rs_:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/src/main.rs}}
```

Sekarang ayo kompilasi program “Hello, world!” ini dan jalankan sekaligus dalam satu langkah dengan perintah `cargo run`:

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/output.txt}}
```

Perintah `run` sangat berguna saat kamu perlu iterasi cepat pada sebuah proyek, seperti yang akan kita lakukan dalam game ini, menguji setiap iterasi dengan cepat sebelum lanjut ke berikutnya.

Buka lagi file _src/main.rs_. Kamu akan menulis semua kode di file ini.

## Memproses Sebuah Tebakan

Bagian pertama dari program game tebak-tebakan akan meminta masukan pengguna, memproses masukan itu, dan memeriksa bahwa masukan sesuai bentuk yang diharapkan. Untuk mulai, kita izinkan pemain memasukkan sebuah tebakan. Ketik kode di Listing 2-1 ke dalam _src/main.rs_.

<Listing number="2-1" file-name="src/main.rs" caption="Kode yang mengambil tebakan dari pengguna lalu mencetaknya">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:all}}
```

</Listing>

Kode ini memuat banyak informasi, jadi mari kita bahas baris demi baris. Untuk menerima masukan pengguna lalu mencetak hasilnya sebagai keluaran, kita perlu membawa library masukan/keluaran `io` ke dalam scope. Library `io` berasal dari standard library, yang dikenal sebagai `std`:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:io}}
```

Secara default, Rust punya sekumpulan item yang didefinisikan di standard library dan dibawanya ke dalam scope setiap program. Kumpulan ini disebut _prelude_, dan kamu bisa melihat seluruh isinya [di dokumentasi standard library][prelude].

Jika tipe yang ingin kamu gunakan tidak ada di prelude, kamu harus membawa tipe itu ke dalam scope secara eksplisit dengan statement `use`. Menggunakan library `std::io` memberimu sejumlah fitur berguna, termasuk kemampuan menerima masukan pengguna.

Seperti yang kamu lihat di Bab 1, fungsi `main` adalah titik masuk ke program:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:main}}
```

Sintaks `fn` mendeklarasikan fungsi baru; tanda kurung, `()`, menunjukkan tidak ada parameter; dan kurung kurawal, `{`, memulai badan fungsi.

Seperti yang juga kamu pelajari di Bab 1, `println!` adalah macro yang mencetak string ke layar:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print}}
```

Kode ini mencetak prompt yang menjelaskan tentang game ini sekaligus meminta masukan dari pengguna.

<a id="storing-values-with-variables"></a>
### Menyimpan Nilai dengan Variabel

Berikutnya, kita akan membuat sebuah _variabel_ untuk menyimpan masukan pengguna, seperti ini:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:string}}
```

Sekarang programnya jadi menarik! Ada banyak yang terjadi di satu baris kecil ini. Kita memakai statement `let` untuk membuat variabelnya. Berikut contoh lain:

```rust,ignore
let apples = 5;
```

Baris ini membuat variabel baru bernama `apples` dan mengikatkannya ke nilai `5`. Di Rust, variabel bersifat immutable secara default, artinya begitu kita memberi nilai ke variabel itu, nilainya tidak akan berubah. Kita akan membahas konsep ini secara rinci di bagian [“Variables and Mutability”][variables-and-mutability]<!-- ignore --> di Bab 3. Untuk membuat variabel menjadi mutable, kita tambahkan `mut` sebelum nama variabelnya:

```rust,ignore
let apples = 5; // immutable
let mut bananas = 5; // mutable
```

> Catatan: Sintaks `//` memulai komentar yang berlanjut hingga akhir baris. Rust mengabaikan semua isi komentar. Kita akan membahas komentar lebih rinci di [Bab 3][comments]<!-- ignore -->.

Kembali ke program game tebak-tebakan, sekarang kamu tahu bahwa `let mut guess` akan memperkenalkan variabel mutable bernama `guess`. Tanda sama dengan (`=`) memberi tahu Rust bahwa kita ingin mengikat sesuatu ke variabel itu sekarang. Di sebelah kanan tanda sama adalah nilai yang diikat oleh `guess`, yaitu hasil pemanggilan `String::new`, sebuah fungsi yang mengembalikan instance baru dari `String`. [`String`][string]<!-- ignore --> adalah tipe string yang disediakan standard library berupa potongan teks yang bisa diperluas dan berbasis UTF-8.

Sintaks `::` di baris `::new` menunjukkan bahwa `new` adalah fungsi terkait dari tipe `String`. Sebuah _fungsi terkait_ adalah fungsi yang diimplementasikan pada sebuah tipe, dalam kasus ini `String`. Fungsi `new` ini membuat string baru yang kosong. Kamu akan menemukan fungsi `new` di banyak tipe karena itu nama yang lazim untuk fungsi yang membuat nilai baru dari semacam jenis tertentu.

Secara keseluruhan, baris `let mut guess = String::new();` telah membuat variabel mutable yang saat ini terikat ke sebuah instance `String` baru yang kosong. Fiuh!

### Menerima Masukan Pengguna

Ingat bahwa kita sudah menyertakan fungsionalitas masukan/keluaran dari standard library dengan `use std::io;` di baris pertama program. Sekarang kita akan memanggil fungsi `stdin` dari module `io`, yang memungkinkan kita menangani masukan pengguna:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:read}}
```

Jika kita tidak mengimpor module `io` dengan `use std::io;` di awal program, kita tetap bisa menggunakan fungsi itu dengan menulis pemanggilan fungsi sebagai `std::io::stdin`. Fungsi `stdin` mengembalikan sebuah instance dari [`std::io::Stdin`][iostdin]<!-- ignore -->, yaitu tipe yang merepresentasikan handle ke standard input terminalmu.

Berikutnya, baris `.read_line(&mut guess)` memanggil method [`read_line`][read_line]<!-- ignore --> pada handle standard input untuk mengambil masukan dari pengguna. Kita juga mengoper `&mut guess` sebagai argumen ke `read_line` untuk memberi tahu string mana yang akan menyimpan masukan pengguna. Pekerjaan utama `read_line` adalah mengambil apa pun yang diketik pengguna ke standard input dan menambahkannya ke dalam sebuah string (tanpa menimpa isinya), karena itu kita oper string itu sebagai argumen. Argumen string harus mutable agar method itu bisa mengubah isi string.

Tanda `&` menunjukkan bahwa argumen ini adalah sebuah _reference_, yang memberimu cara agar beberapa bagian kode-mu bisa mengakses satu data tanpa perlu menyalin data itu ke memori berkali-kali. Reference adalah fitur yang rumit, dan salah satu keunggulan utama Rust adalah betapa aman dan mudahnya menggunakan reference. Kamu tidak perlu tahu banyak detail itu untuk menyelesaikan program ini. Untuk saat ini, yang perlu kamu ketahui saja adalah bahwa seperti variabel, reference bersifat immutable secara default. Karena itu, kamu perlu menulis `&mut guess` alih-alih `&guess` untuk membuatnya mutable. (Bab 4 akan menjelaskan reference lebih menyeluruh.)

<!-- Old headings. Do not remove or links may break. -->

<a id="handling-potential-failure-with-the-result-type"></a>

<a id="handling-potential-failure-with-result"></a>
### Menangani Kegagalan Potensial dengan `Result`

Kita masih mengerjakan baris kode yang sama. Kita kini membahas baris teks ketiga, tetapi perhatikan bahwa itu masih bagian dari satu baris kode logis. Bagian berikutnya adalah method ini:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:expect}}
```

Kita bisa saja menulis kode ini sebagai:

```rust,ignore
io::stdin().read_line(&mut guess).expect("Failed to read line");
```

Namun, satu baris panjang sulit dibaca, jadi sebaiknya dipecah. Sering kali bijaksana untuk memasukkan baris baru dan whitespace lain untuk membantu memecah baris panjang saat kamu memanggil method dengan sintaks `.method_name()`. Sekarang mari kita bahas apa yang dilakukan baris ini.

Seperti disebutkan sebelumnya, `read_line` menaruh apa pun yang dimasukkan pengguna ke dalam string yang kita oper padanya, tetapi fungsi itu juga mengembalikan sebuah nilai [`Result`][result]<!-- ignore -->. `Result` adalah sebuah [_enumeration_][enums]<!-- ignore -->, yang sering disebut _enum_, yaitu sebuah tipe yang bisa berada dalam salah satu dari beberapa keadaan yang mungkin. Kita menyebut tiap keadaan yang mungkin itu sebuah _variant_.

[Bab 6][enums]<!-- ignore --> akan membahas enum lebih rinci. Tujuan tipe `Result` ini adalah mengkodekan informasi penanganan error.

Variant `Result` adalah `Ok` dan `Err`. Variant `Ok` menunjukkan operasi berhasil, dan di dalamnya berisi nilai yang berhasil dihasilkan. Variant `Err` berarti operasi gagal, dan di dalamnya berisi informasi tentang bagaimana atau mengapa operasi itu gagal.

Nilai bertipe `Result`, seperti nilai bertipe apa pun, punya method yang didefinisikan padanya. Sebuah instance `Result` punya [`expect` method][expect]<!-- ignore --> yang bisa kamu panggil. Jika instance `Result` ini adalah nilai `Err`, `expect` akan membuat program crash dan menampilkan pesan yang kamu berikan sebagai argumen ke `expect`. Jika method `read_line` mengembalikan `Err`, kemungkinan itu berasal dari error sistem operasi di baliknya. Jika instance `Result` ini adalah nilai `Ok`, `expect` akan mengambil nilai kembalian yang dipegang `Ok` dan mengembalikan hanya nilai itu kepadamu agar bisa kamu gunakan. Dalam kasus ini, nilainya adalah jumlah byte dalam masukan pengguna.

Jika kamu tidak memanggil `expect`, program akan tetap mengompilasi, tetapi kamu akan mendapat warning:

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-02-without-expect/output.txt}}
```

Rust memperingatkan bahwa kamu belum memakai nilai `Result` yang dikembalikan dari `read_line`, yang menandakan program belum menangani error yang mungkin terjadi.

Cara yang tepat untuk menekan warning itu adalah dengan benar-benar menulis kode penanganan error, tetapi dalam kasus kita kita hanya ingin membuat program ini crash saat masalah terjadi, jadi kita bisa memakai `expect`. Kamu akan belajar tentang pemulihan dari error di [Bab 9][recover]<!-- ignore -->.

### Mencetak Nilai dengan Placeholder `println!`

Selain kurung kurawal penutup, hanya ada satu baris lagi yang perlu dibahas dalam kode sejauh ini:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print_guess}}
```

Baris ini mencetak string yang kini berisi masukan pengguna. Sekumpulan kurung kurawal `{}` adalah sebuah placeholder: bayangkan `{}` sebagai capit kepiting kecil yang mengunci sebuah nilai di tempatnya. Saat mencetak nilai sebuah variabel, nama variabelnya bisa diletakkan di dalam kurung kurawal. Saat mencetak hasil evaluasi sebuah ekspresi, letakkan kurung kurawal kosong di format string, lalu ikuti format string itu dengan daftar ekspresi yang dipisahkan koma untuk dicetak di tiap placeholder kurung kurawal kosong dengan urutan yang sama. Mencetak sebuah variabel sekaligus hasil sebuah ekspresi dalam satu pemanggilan `println!` akan terlihat seperti ini:

```rust
let x = 5;
let y = 10;

println!("x = {x} and y + 2 = {}", y + 2);
```

Kode ini akan mencetak `x = 5 and y + 2 = 12`.

### Menguji Bagian Pertama

Ayo uji bagian pertama dari game tebak-tebakan. Jalankan dengan `cargo run`:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-01/
cargo clean
cargo run
input 6 -->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 6.44s
     Running `target/debug/guessing_game`
Guess the number!
Please input your guess.
6
You guessed: 6
```

Pada titik ini, bagian pertama game sudah selesai: kita menerima masukan dari keyboard lalu mencetaknya.

## Menghasilkan Angka Rahasia

Berikutnya, kita perlu menghasilkan angka rahasia yang akan ditebak pengguna. Angka rahasia harus berbeda setiap kali agar game ini seru dimainkan berulang kali. Kita akan memakai angka acak antara 1 dan 100 agar game ini tidak terlalu sulit. Rust belum menyertakan fungsionalitas angka acak di standard library-nya. Namun, tim Rust menyediakan [crate `rand`][randcrate] dengan fungsionalitas tersebut.

<!-- Old headings. Do not remove or links may break. -->
<a id="using-a-crate-to-get-more-functionality"></a>

### Menambah Fungsionalitas dengan Crate

Ingat bahwa crate adalah kumpulan file kode sumber Rust. Proyek yang sedang kita bangun adalah sebuah binary crate, yaitu sesuatu yang bisa dieksekusi. Crate `rand` adalah library crate, yang berisi kode yang dimaksudkan untuk digunakan di program lain dan tidak bisa dieksekusi sendirian.

Koordinasi crate eksternal oleh Cargo adalah bagian di mana Cargo benar-benar bersinar. Sebelum kita bisa menulis kode yang memakai `rand`, kita perlu mengubah file _Cargo.toml_ agar menyertakan crate `rand` sebagai dependensi. Buka file itu sekarang dan tambahkan baris berikut di bagian bawah, di bawah header bagian `[dependencies]` yang dibuat Cargo untukmu. Pastikan menuliskan `rand` persis seperti di sini, dengan nomor versi ini, atau contoh kode dalam tutorial ini mungkin tidak akan berfungsi:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
* ch14-03-cargo-workspaces.md
-->

<span class="filename">Filename: Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:8:}}
```

Di dalam file _Cargo.toml_, semua yang mengikuti sebuah header adalah bagian dari bagian itu dan berlanjut sampai bagian lain dimulai. Di `[dependencies]`, kamu memberi tahu Cargo crate eksternal mana yang jadi dependensi proyekmu dan versi mana dari crate-crate itu yang kamu butuhkan. Dalam kasus ini, kita menetapkan crate `rand` dengan penanda versi semantik `0.10.1`. Cargo memahami [Semantic Versioning][semver]<!-- ignore --> (kadang disebut _SemVer_), yaitu standar untuk menulis nomor versi. Penanda `0.10.1` sebenarnya adalah bentuk singkat dari `^0.10.1`, yang berarti versi apa pun yang minimal 0.10.1 tetapi di bawah 0.11.0.

Cargo menganggap versi-versi ini punya API publik yang kompatibel dengan versi 0.10.1, dan spesifikasi ini memastikan kamu akan mendapat patch release terbaru yang tetap bisa mengompilasi kode di bab ini. Versi 0.11.0 ke atas tidak dijamin punya API yang sama dengan yang dipakai contoh-contoh berikut.

Sekarang, tanpa mengubah kode apa pun, ayo build proyeknya, seperti di Listing 2-2.

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
rm Cargo.lock
cargo clean
cargo build -->

<Listing number="2-2" caption="Keluaran dari menjalankan `cargo build` setelah menambahkan crate `rand` sebagai dependensi">

```console
$ cargo build
    Updating crates.io index
     Locking 8 packages to latest Rust 1.96.0 compatible versions
  Downloaded rand_core v0.10.1
  Downloaded chacha20 v0.10.1
  Downloaded rand v0.10.1
  Downloaded 3 crates (162.9KiB) in 0.59s
   Compiling libc v0.2.186
   Compiling rand_core v0.10.1
   Compiling getrandom v0.4.3
   Compiling cfg-if v1.0.4
   Compiling chacha20 v0.10.1
   Compiling rand v0.10.1
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 2.03s
```

</Listing>

Kamu mungkin melihat nomor versi yang berbeda (tetapi semuanya akan kompatibel dengan kode, berkat SemVer!) dan baris yang berbeda (tergantung sistem operasinya), serta baris-barisnya bisa dalam urutan yang berbeda.

Saat kita menyertakan dependensi eksternal, Cargo mengambil versi terbaru dari semua yang dibutuhkan dependensi itu dari _registry_, yaitu salinan data dari [Crates.io][cratesio]. Crates.io adalah tempat orang-orang di ekosistem Rust membagikan proyek Rust open source mereka untuk dipakai orang lain.

Setelah memperbarui registry, Cargo memeriksa bagian `[dependencies]` dan mengunduh crate-crate yang tercantum tetapi belum diunduh. Dalam kasus ini, meskipun kita hanya mencantumkan `rand` sebagai dependensi, Cargo juga mengambil crate-crate lain yang dibutuhkan `rand` untuk bekerja. Setelah mengunduh crate-crate itu, Rust mengompilasinya lalu mengompilasi proyek dengan dependensi yang tersedia.

Jika kamu langsung menjalankan `cargo build` lagi tanpa mengubah apa pun, kamu tidak akan dapat keluaran apa pun selain baris `Finished`. Cargo tahu ia sudah mengunduh dan mengompilasi dependensi, dan kamu tidak mengubah apa pun tentangnya di file _Cargo.toml_-mu. Cargo juga tahu kamu tidak mengubah apa pun tentang kodenya, jadi ia tidak mengompilasi ulang kode itu juga. Tidak ada yang harus dikerjakan, jadi ia cukup keluar.

Jika kamu membuka file _src/main.rs_, membuat perubahan sepele, lalu menyimpannya dan build lagi, kamu hanya akan melihat dua baris keluaran:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
touch src/main.rs
cargo build -->

```console
$ cargo build
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
```

Baris-baris ini menunjukkan Cargo hanya memperbarui build dengan perubahan kecilmu di file _src/main.rs_. Dependensimu tidak berubah, jadi Cargo tahu ia bisa memakai ulang apa yang sudah diunduh dan dikompilasi untuk dependensi itu.

<!-- Old headings. Do not remove or links may break. -->
<a id="ensuring-reproducible-builds-with-the-cargo-lock-file"></a>

#### Memastikan Build yang Reproduksibel

Punya Cargo sebuah mekanisme yang memastikan kamu bisa membangun ulang artefak yang sama setiap kali kamu atau orang lain membangun kodenya: Cargo hanya akan memakai versi-versi dependensi yang kamu tetapkan sampai kamu menyatakan sebaliknya. Sebagai contoh, misalkan minggu depan versi 0.10.2 dari crate `rand` dirilis, dan versi itu memuat perbaikan bug penting, tetapi juga memuat regresi yang akan merusak kode-mu. Untuk menanganinya, Rust membuat file _Cargo.lock_ saat pertama kali kamu menjalankan `cargo build`, jadi kini kita punya file itu di direktori _guessing_game_.

Saat kamu build sebuah proyek untuk pertama kali, Cargo menentukan semua versi dependensi yang memenuhi kriteria lalu menulisnya ke file _Cargo.lock_. Saat kamu build proyekmu di kemudian hari, Cargo akan melihat file _Cargo.lock_ sudah ada dan akan memakai versi-versi yang ditetapkan di sana alih-alih mengerjakan semua penentuan versi dari awal. Dengan begitu kamu otomatis mendapat build yang reproducible. Dengan kata lain, proyekmu akan tetap di 0.10.1 sampai kamu secara eksplisit meng-upgrade, berkat file _Cargo.lock_. Karena file _Cargo.lock_ penting untuk build yang reproducible, file itu sering ikut dikirim ke source control bersama kode lain di proyekmu.

#### Meng-update Crate untuk Mendapat Versi Baru

Saat kamu _mau_ meng-update sebuah crate, Cargo menyediakan perintah `update`, yang akan mengabaikan file _Cargo.lock_ dan menentukan semua versi terbaru yang memenuhi spesifikasimu di _Cargo.toml_. Cargo lalu menulis versi-versi itu ke file _Cargo.lock_. Selain itu, secara default, Cargo hanya akan mencari versi yang lebih besar dari 0.10.1 dan kurang dari 0.11.0. Jika crate `rand` sudah merilis dua versi baru, 0.10.2 dan 0.999.0, kamu akan melihat hal berikut jika menjalankan `cargo update`:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
cargo update
assuming there is a new version of rand; otherwise use another update
as a guide to creating the hypothetical output shown here -->

```console
$ cargo update
    Updating crates.io index
     Locking 1 package to latest Rust 1.96.0 compatible version
    Updating rand v0.10.1 -> v0.10.2 (available: v0.999.0)
```

Cargo mengabaikan rilis 0.999.0. Pada titik ini, kamu juga akan melihat perubahan di file _Cargo.lock_-mu yang menandai bahwa versi crate `rand` yang kini kamu pakai adalah 0.10.2. Untuk memakai `rand` versi 0.999.0 atau versi apa pun di seri 0.999._x_, kamu harus mengubah file _Cargo.toml_ agar terlihat seperti ini (jangan benar-benar mengubahnya karena contoh-contoh berikut mengasumsikan kamu memakai `rand` 0.10):

```toml
[dependencies]
rand = "0.999.0"
```

Berikutnya saat kamu menjalankan `cargo build`, Cargo akan memperbarui registry crate yang tersedia dan mengevaluasi ulang kebutuhan `rand`-mu sesuai versi baru yang kamu tetapkan.

Masih banyak hal yang bisa dikatakan tentang [Cargo][doccargo]<!-- ignore --> dan [ekosistemnya][doccratesio]<!-- ignore -->, yang akan kita bahas di Bab 14, tetapi untuk saat ini, itu semua yang perlu kamu ketahui. Cargo membuatnya sangat mudah untuk memakai ulang library, sehingga Rustacean bisa menulis proyek-proyek kecil yang disusun dari sejumlah package.

<a id="generating-a-random-number"></a>
### Menghasilkan Angka Acak

Ayo mulai memakai `rand` untuk menghasilkan angka yang akan ditebak. Langkah berikutnya adalah memperbarui _src/main.rs_, seperti di Listing 2-3.

<Listing number="2-3" file-name="src/main.rs" caption="Menambahkan kode untuk menghasilkan angka acak">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:all}}
```

</Listing>

Pertama, kita tambahkan baris `use rand::prelude::*;`. Module `prelude` berisi bagian-bagian yang paling sering dipakai dari crate `rand`, dan `use` membuat item-item itu tersedia di scope program kita.

Berikutnya, kita menambahkan dua baris di tengah. Pada baris pertama, kita memanggil fungsi `rand::rng` yang memberi kita pembangkit angka acak khusus yang akan kita gunakan: yang lokal untuk thread eksekusi saat ini dan di-seed oleh sistem operasi. Lalu, kita memanggil method `random_range` pada pembangkit angka acak itu. Method ini didefinisikan oleh trait `RngExt` yang merupakan bagian dari module `rand::prelude` yang kita bawa ke dalam scope dengan statement `use rand::prelude::*;`. Method `random_range` menerima sebuah ekspresi range sebagai argumen dan menghasilkan angka acak di dalam range itu. Jenis ekspresi range yang kita pakai di sini berbentuk `start..=end` dan inklusif di batas bawah serta atas, jadi kita perlu menetapkan `1..=100` untuk meminta angka antara 1 dan 100.

> Catatan: Kamu tidak akan serta-merta tahu apa yang harus dibawa ke dalam scope serta method dan fungsi mana yang dipanggil dari sebuah crate, jadi tiap crate punya dokumentasi berisi petunjuk penggunaannya. Fitur keren lain dari Cargo adalah menjalankan perintah `cargo doc --open` akan build dokumentasi yang disediakan semua dependensimu secara lokal lalu membukanya di browser-mu. Jika kamu tertarik dengan fungsionalitas lain di crate `rand`, misalnya, jalankan `cargo doc --open` dan klik `rand` di sidebar sebelah kiri.

Baris baru kedua mencetak angka rahasia. Ini berguna saat kita sedang mengembangkan program agar bisa menguji, tetapi kita akan menghapusnya dari versi akhir. Bukan game yang menarik jika program mencetak jawabannya begitu program dimulai!

Coba jalankan program beberapa kali:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-03/
cargo run
4
cargo run
5
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 7
Please input your guess.
4
You guessed: 4

$ cargo run
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 83
Please input your guess.
5
You guessed: 5
```

Kamu seharusnya mendapat angka acak yang berbeda-beda, dan semuanya berada di antara 1 dan 100. Jika kamu mendapat warning, warning itu aman diabaikan. Jika kamu mendapat error, periksa bahwa kamu punya `rand = "0.10.1"` di *Cargo.toml*-mu karena versi `rand` di kemudian hari mungkin punya API yang berbeda, tetapi versi apa pun di seri `0.10` seharusnya berfungsi dengan kode di bab ini.

<a id="comparing-the-guess-to-the-secret-number"></a>
## Membandingkan Tebakan dengan Angka Rahasia

Sekarang kita punya masukan pengguna dan angka acak, kita bisa membandingkannya. Langkah itu ditunjukkan di Listing 2-4. Perhatikan bahwa kode ini belum bisa dikompilasi, seperti yang akan kita jelaskan.

<Listing number="2-4" file-name="src/main.rs" caption="Menangani nilai kembalian yang mungkin dari membandingkan dua angka">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-04/src/main.rs:here}}
```

</Listing>

Pertama, kita tambahkan statement `use` lain, membawa tipe bernama `std::cmp::Ordering` ke dalam scope dari standard library. Tipe `Ordering` adalah enum lain dan punya variant `Less`, `Greater`, dan `Equal`. Ketiganya adalah tiga hasil yang mungkin saat kamu membandingkan dua nilai.

Lalu, kita tambahkan lima baris baru di bagian bawah yang memakai tipe `Ordering`. Method `cmp` membandingkan dua nilai dan bisa dipanggil pada apa pun yang bisa dibandingkan. Method itu menerima reference ke apa pun yang ingin kamu bandingkan: Di sini, ia membandingkan `guess` dengan `secret_number`. Lalu, method itu mengembalikan sebuah variant enum `Ordering` yang kita bawa ke dalam scope dengan statement `use`. Kita memakai ekspresi [`match`][match]<!-- ignore --> untuk memutuskan apa yang harus dilakukan berikutnya berdasarkan variant `Ordering` mana yang dikembalikan dari pemanggilan `cmp` dengan nilai `guess` dan `secret_number`.

Sebuah ekspresi `match` tersusun atas _arm_. Sebuah arm terdiri dari sebuah _pattern_ untuk dicocokkan, dan kode yang harus dijalankan jika nilai yang diberikan ke `match` cocok dengan pattern arm itu. Rust mengambil nilai yang diberikan ke `match` lalu memeriksa tiap pattern arm satu per satu. Pattern dan konstruk `match` adalah fitur Rust yang kuat: fitur-fitur itu memungkinkanmu menyatakan berbagai situasi yang mungkin dihadapi kode-mu, dan memastikan kamu menanganinya semua. Fitur-fitur ini akan dibahas rinci di Bab 6 dan Bab 19, masing-masing.

Ayo telusuri sebuah contoh dengan ekspresi `match` yang kita pakai di sini. Misalkan pengguna sudah menebak 50 dan angka rahasia yang dihasilkan secara acak kali ini adalah 38.

Saat kode membandingkan 50 dengan 38, method `cmp` akan mengembalikan `Ordering::Greater` karena 50 lebih besar dari 38. Ekspresi `match` menerima nilai `Ordering::Greater` lalu mulai memeriksa pattern tiap arm. Ia melihat pattern arm pertama, `Ordering::Less`, dan melihat bahwa nilai `Ordering::Greater` tidak cocok dengan `Ordering::Less`, jadi ia mengabaikan kode di arm itu dan lanjut ke arm berikutnya. Pattern arm berikutnya adalah `Ordering::Greater`, yang _memang_ cocok dengan `Ordering::Greater`! Kode terkait di arm itu akan dieksekusi dan mencetak `Too big!` ke layar. Ekspresi `match` berakhir setelah kecocokan pertama yang berhasil, jadi ia tidak akan melihat arm terakhir dalam skenario ini.

Namun, kode di Listing 2-4 belum bisa dikompilasi. Ayo coba:

<!--
The error numbers in this output should be that of the code **WITHOUT** the
anchor or snip comments
-->

```console
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-04/output.txt}}
```

Inti error menyatakan bahwa terdapat _mismatched types_. Rust punya sistem tipe yang kuat dan statis. Namun, Rust juga punya type inference. Saat kita menulis `let mut guess = String::new()`, Rust bisa menyimpulkan bahwa `guess` harus berupa `String` dan tidak membuat kita menulis tipe itu. `secret_number`, di sisi lain, adalah sebuah tipe angka. Beberapa tipe angka di Rust bisa bernilai antara 1 dan 100: `i32`, angka 32-bit; `u32`, angka unsigned 32-bit; `i64`, angka 64-bit; serta lainnya. Kecuali ditentukan sebaliknya, Rust secara default memakai `i32`, yang merupakan tipe dari `secret_number` kecuali kamu menambahkan informasi tipe di tempat lain yang membuat Rust menyimpulkan tipe numerik yang berbeda. Alasan error ini ada adalah karena Rust tidak bisa membandingkan sebuah string dengan sebuah tipe angka.

Pada akhirnya, kita ingin mengubah `String` yang dibaca program sebagai input menjadi sebuah tipe angka agar kita bisa membandingkannya secara numerik dengan angka rahasia. Kita melakukan itu dengan menambahkan baris ini ke badan fungsi `main`:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/src/main.rs:here}}
```

Barisnya adalah:

```rust,ignore
let guess: u32 = guess.trim().parse().expect("Please type a number!");
```

Kita membuat variabel bernama `guess`. Tetapi tunggu, bukankah program sudah punya variabel bernama `guess`? Memang, tetapi dengan membantu Rust mengizinkan kita menimpa nilai `guess` sebelumnya dengan yang baru. _Shadowing_ memungkinkan kita memakai ulang nama variabel `guess` alih-alih memaksa kita membuat dua variabel unik, seperti `guess_str` dan `guess`, misalnya. Kita akan membahas ini lebih rinci di [Bab 3][shadowing]<!-- ignore -->, tetapi untuk saat ini, ketahui saja bahwa fitur ini sering digunakan saat kamu ingin mengubah sebuah nilai dari satu tipe ke tipe lain.

Kita mengikat variabel baru ini ke ekspresi `guess.trim().parse()`. `guess` dalam ekspresi itu merujuk ke variabel `guess` asli yang berisi input sebagai string. Method `trim` pada sebuah instance `String` akan menghilangkan whitespace di awal dan akhir, yang harus kita lakukan sebelum bisa mengubah string menjadi `u32`, yang hanya bisa berisi data numerik. Pengguna harus menekan <kbd>enter</kbd> untuk memuaskan `read_line` dan memasukkan tebakannya, yang menambahkan karakter newline ke string. Sebagai contoh, jika pengguna mengetik <kbd>5</kbd> lalu menekan <kbd>enter</kbd>, `guess` akan terlihat seperti ini: `5\n`. `\n` mewakili “newline.” (Di Windows, menekan <kbd>enter</kbd> menghasilkan carriage return sekaligus newline, `\r\n`.) Method `trim` menghilangkan `\n` atau `\r\n`, menyisakan hanya `5`.

[`parse` method on strings][parse]<!-- ignore --> mengubah string ke tipe lain. Di sini, kita memakainya untuk mengubah dari string menjadi angka. Kita perlu memberi tahu Rust tipe angka persis yang kita inginkan dengan memakai `let guess: u32`. Tanda titik dua (`:`) setelah `guess` memberi tahu Rust bahwa kita akan menganotasi tipe variabel itu. Punya Rust beberapa tipe angka bawaan; `u32` yang terlihat di sini adalah bilangan bulat unsigned 32-bit. Ini pilihan default yang baik untuk angka positif kecil. Kamu akan belajar tentang tipe angka lain di [Bab 3][integers]<!-- ignore -->.

Selain itu, anotasi `u32` dalam program contoh ini sekaligus perbandingan dengan `secret_number` berarti Rust akan menyimpulkan bahwa `secret_number` juga harus berupa `u32`. Jadi, kini perbandingannya antara dua nilai bertipe sama!

Method `parse` hanya bekerja pada karakter yang secara logis bisa diubah menjadi angka sehingga mudah menyebabkan error. Jika, misalnya, string berisi `A👍%`, tidak ada cara mengubahnya menjadi angka. Karena bisa gagal, method `parse` mengembalikan tipe `Result`, sama seperti method `read_line` (dibahas sebelumnya di [“Handling Potential Failure with `Result`”](#handling-potential-failure-with-result)<!-- ignore -->). Kita akan menangani `Result` ini dengan cara yang sama memakai method `expect` lagi. Jika `parse` mengembalikan variant `Err` dari `Result` karena tidak bisa membuat angka dari string itu, pemanggilan `expect` akan membuat game crash dan mencetak pesan yang kita berikan. Jika `parse` berhasil mengubah string menjadi angka, ia akan mengembalikan variant `Ok` dari `Result`, dan `expect` akan mengembalikan angka yang kita inginkan dari nilai `Ok` itu.

Ayo jalankan programnya sekarang:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/
touch src/main.rs
cargo run
  76
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.26s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 58
Please input your guess.
  76
You guessed: 76
Too big!
```

Bagus! Meskipun ada spasi sebelum tebakan, program tetap bisa menangkap bahwa pengguna menebak 76. Jalankan program beberapa kali untuk memverifikasi perilaku berbeda dengan berbagai jenis masukan: tebak angkanya dengan benar, tebak angka yang terlalu besar, dan tebak angka yang terlalu kecil.

Sebagian besar game sudah berfungsi sekarang, tetapi pengguna hanya bisa menebak sekali. Ayo ubah itu dengan menambahkan sebuah loop!

## Mengizinkan Beberapa Tebakan dengan Looping

Kata kunci `loop` membuat loop tak terhingga. Kita akan menambahkan loop agar pengguna punya lebih banyak kesempatan menebak angkanya:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-04-looping/src/main.rs:here}}
```

Seperti yang bisa kamu lihat, kita memindahkan semua yang ada dari prompt masukan tebakan dan seterusnya ke dalam sebuah loop. Pastikan memberi indentasi empat spasi lagi pada baris-baris di dalam loop, lalu jalankan programnya lagi. Program kini akan terus meminta tebakan selamanya, yang sebenarnya memperkenalkan masalah baru. Sepertinya pengguna tidak bisa keluar!

Pengguna selalu bisa menyela program dengan pintasan keyboard <kbd>ctrl</kbd>-<kbd>C</kbd>. Tetapi ada cara lain untuk kabur dari monster rakus ini, seperti disebutkan dalam pembahasan `parse` di [“Comparing the Guess to the Secret Number”](#comparing-the-guess-to-the-secret-number)<!-- ignore -->: Jika pengguna memasukkan jawaban yang bukan angka, program akan crash. Kita bisa memanfaatkan itu untuk mengizinkan pengguna keluar, seperti ditunjukkan di sini:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-04-looping/
touch src/main.rs
cargo run
(too small guess)
(too big guess)
(correct guess)
quit
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.23s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 59
Please input your guess.
45
You guessed: 45
Too small!
Please input your guess.
60
You guessed: 60
Too big!
Please input your guess.
59
You guessed: 59
You win!
Please input your guess.
quit

thread 'main' (6694925) panicked at src/main.rs:28:47:
Please type a number!: ParseIntError { kind: InvalidDigit }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Mengetik `quit` akan mengakhiri game, tetapi seperti yang akan kamu perhatikan, memasukkan masukan non-angka apa pun juga akan mengakhirinya. Ini kurang ideal, setidaknya begitu; kita ingin game juga berhenti saat angka yang benar berhasil ditebak.

<a id="quitting-after-a-correct-guess"></a>
### Keluar Setelah Tebakan yang Benar

Ayo buat game keluar saat pengguna menang dengan menambahkan statement `break`:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-05-quitting/src/main.rs:here}}
```

Menambahkan baris `break` setelah `You win!` membuat program keluar dari loop saat pengguna menebak angka rahasia dengan benar. Keluar dari loop juga berarti keluar dari program, karena loop itu adalah bagian terakhir dari `main`.

### Menangani Masukan yang Tidak Valid

Untuk menyempurnakan perilaku game lebih jauh, alih-alih membuat program crash saat pengguna memasukkan non-angka, buat game mengabaikan non-angka agar pengguna bisa terus menebak. Kita bisa melakukan itu dengan mengubah baris tempat `guess` diubah dari `String` menjadi `u32`, seperti di Listing 2-5.

<Listing number="2-5" file-name="src/main.rs" caption="Mengabaikan tebakan non-angka dan meminta tebakan lain alih-alih membuat program crash">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:here}}
```

</Listing>

Kita beralih dari pemanggilan `expect` ke ekspresi `match` untuk berpindah dari crash saat error menjadi menangani error. Ingat bahwa `parse` mengembalikan tipe `Result` dan `Result` adalah enum yang punya variant `Ok` dan `Err`. Kita memakai ekspresi `match` di sini, seperti yang kita lakukan dengan hasil `Ordering` dari method `cmp`.

Jika `parse` berhasil mengubah string menjadi angka, ia akan mengembalikan sebuah nilai `Ok` yang berisi angka hasilnya. Nilai `Ok` itu akan cocok dengan pattern arm pertama, dan ekspresi `match` akan mengembalikan nilai `num` yang dihasilkan `parse` dan diletakkan di dalam nilai `Ok`. Angka itu akan berakhir tepat di tempat yang kita inginkan, yaitu di variabel `guess` baru yang kita buat.

Jika `parse` _tidak_ berhasil mengubah string menjadi angka, ia akan mengembalikan sebuah nilai `Err` yang berinformasi lebih rinci tentang error itu. Nilai `Err` tidak cocok dengan pattern `Ok(num)` di arm `match` pertama, tetapi memang cocok dengan pattern `Err(_)` di arm kedua. Tanda bawah, `_`, adalah nilai catch-all; dalam contoh ini, kita menyatakan ingin mencocokkan semua nilai `Err`, tanpa peduli informasi apa pun di dalamnya. Jadi, program akan mengeksekusi kode arm kedua, `continue`, yang memberi tahu program untuk lanjut ke iterasi berikutnya dari `loop` dan meminta tebakan lain. Jadi, secara efektif, program mengabaikan semua error yang mungkin dihadapi `parse`!

Sekarang semua yang ada di program seharusnya berfungsi sebagaimana mestinya. Ayo coba:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-05/
cargo run
(too small guess)
(too big guess)
foo
(correct guess)
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 61
Please input your guess.
10
You guessed: 10
Too small!
Please input your guess.
99
You guessed: 99
Too big!
Please input your guess.
foo
Please input your guess.
61
You guessed: 61
You win!
```

Luar biasa! Dengan satu penyesuaian kecil terakhir, kita akan menyelesaikan game tebak-tebakan. Ingat bahwa program masih mencetak angka rahasia. Itu berguna untuk pengujian, tetapi merusak game. Ayo hapus `println!` yang mengeluarkan angka rahasia. Listing 2-6 menunjukkan kode akhirnya.

<Listing number="2-6" file-name="src/main.rs" caption="Kode game tebak-tebakan yang lengkap">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-06/src/main.rs}}
```

</Listing>

Pada titik ini, kamu sudah berhasil membangun game tebak-tebakan. Selamat!

## Ringkasan

Proyek ini adalah cara praktis memperkenalkan banyak konsep Rust baru kepadamu: `let`, `match`, fungsi, penggunaan crate eksternal, dan masih banyak lagi. Pada beberapa bab berikutnya, kamu akan mempelajari konsep-konsep ini lebih rinci. Bab 3 membahas konsep yang dimiliki sebagian besar bahasa pemrograman, seperti variabel, tipe data, dan fungsi, serta menunjukkan cara menggunakannya di Rust. Bab 4 menjelajahi ownership, sebuah fitur yang membuat Rust berbeda dari bahasa lain. Bab 5 membahas struct dan sintaks method, dan Bab 6 menjelaskan cara kerja enum.

[prelude]: ../std/prelude/index.html
[variables-and-mutability]: ch03-01-variables-and-mutability.html#variables-and-mutability
[comments]: ch03-04-comments.html
[string]: ../std/string/struct.String.html
[iostdin]: ../std/io/struct.Stdin.html
[read_line]: ../std/io/struct.Stdin.html#method.read_line
[result]: ../std/result/enum.Result.html
[enums]: ch06-00-enums.html
[expect]: ../std/result/enum.Result.html#method.expect
[recover]: ch09-02-recoverable-errors-with-result.html
[randcrate]: https://crates.io/crates/rand
[semver]: http://semver.org
[cratesio]: https://crates.io/
[doccargo]: https://doc.rust-lang.org/cargo/
[doccratesio]: https://doc.rust-lang.org/cargo/reference/publishing.html
[match]: ch06-02-match.html
[shadowing]: ch03-01-variables-and-mutability.html#shadowing
[parse]: ../std/primitive.str.html#method.parse
[integers]: ch03-02-data-types.html#integer-types
