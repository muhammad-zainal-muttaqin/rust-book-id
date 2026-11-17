## Membawa Path ke dalam Scope dengan Keyword `use`

Menulis path setiap kali ingin memanggil fungsi bisa terasa merepotkan dan
berulang. Pada Listing 7-7, entah kita memilih path absolut maupun relatif ke
fungsi `add_to_waitlist`, setiap kali kita ingin memanggil `add_to_waitlist`
kita juga harus menulis `front_of_house` dan `hosting`. Untungnya, ada cara
untuk menyederhanakan proses ini: kita bisa membuat jalan pintas ke sebuah path
dengan keyword `use` sekali saja, lalu memakai nama yang lebih pendek itu di
seluruh scope lainnya.

Pada Listing 7-11, kita membawa module `crate::front_of_house::hosting` ke
dalam scope fungsi `eat_at_restaurant` sehingga kita hanya perlu menulis
`hosting::add_to_waitlist` untuk memanggil fungsi `add_to_waitlist` di dalam
`eat_at_restaurant`.

<Listing number="7-11" file-name="src/lib.rs" caption="Membawa sebuah module ke dalam scope dengan `use`">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-11/src/lib.rs}}
```

</Listing>

Menambahkan `use` beserta path dalam sebuah scope mirip dengan membuat symbolic
link di filesystem. Dengan menambahkan `use crate::front_of_house::hosting` di
akar crate, `hosting` kini menjadi nama yang valid di scope tersebut, seolah-olah
module `hosting` memang didefinisikan di akar crate. Path yang dibawa ke dalam
scope dengan `use` juga memeriksa privasi, sama seperti path lainnya.

Perhatikan bahwa `use` hanya membuat jalan pintas itu untuk scope tertentu
tempat `use` tersebut berada. Listing 7-12 memindahkan fungsi `eat_at_restaurant`
ke dalam sebuah module anak bernama `customer`, yang merupakan scope berbeda dari
statement `use` itu, sehingga isi fungsi tersebut tidak akan terkompilasi.

<Listing number="7-12" file-name="src/lib.rs" caption="Statement `use` hanya berlaku di scope tempatnya berada.">

```rust,noplayground,test_harness,does_not_compile,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-12/src/lib.rs}}
```

</Listing>

Error compiler menunjukkan bahwa jalan pintas itu tidak lagi berlaku di dalam
module `customer`:

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-12/output.txt}}
```

Perhatikan juga adanya peringatan bahwa `use` tersebut sudah tidak terpakai lagi
di scope-nya! Untuk mengatasi masalah ini, pindahkan `use` itu ke dalam module
`customer` juga, atau rujuk jalan pintas tersebut dari module induk dengan
`super::hosting` di dalam module anak `customer`.

<a id="creating-idiomatic-use-paths"></a>
### Membuat Path `use` yang Idiomatis

Di Listing 7-11, kamu mungkin bertanya-tanya kenapa kita menulis
`use crate::front_of_house::hosting` lalu memanggil
`hosting::add_to_waitlist` di `eat_at_restaurant`, alih-alih menulis path `use`
sampai ke fungsi `add_to_waitlist` untuk mencapai hasil yang sama, seperti pada
Listing 7-13.

<Listing number="7-13" file-name="src/lib.rs" caption="Membawa fungsi `add_to_waitlist` ke dalam scope dengan `use`, yang bukan merupakan cara idiomatis">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-13/src/lib.rs}}
```

</Listing>

Meskipun Listing 7-11 dan Listing 7-13 sama-sama menyelesaikan tugas yang
sama, Listing 7-11 adalah cara idiomatis untuk membawa sebuah fungsi ke dalam
scope dengan `use`. Membawa module induk dari fungsi tersebut ke dalam scope
dengan `use` berarti kita harus menyebut module induk itu saat memanggil
fungsinya. Menyebut module induk saat memanggil fungsi membuat jelas bahwa
fungsi tersebut bukan didefinisikan secara lokal, sementara tetap meminimalkan
pengulangan path lengkap. Kode pada Listing 7-13 tidak jelas soal di mana
`add_to_waitlist` didefinisikan.

Sebaliknya, saat membawa struct, enum, dan item lain dengan `use`, yang
idiomatis adalah menulis path lengkapnya. Listing 7-14 menunjukkan cara
idiomatis untuk membawa struct `HashMap` dari standard library ke dalam scope
sebuah binary crate.

<Listing number="7-14" file-name="src/main.rs" caption="Membawa `HashMap` ke dalam scope secara idiomatis">

```rust
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-14/src/main.rs}}
```

</Listing>

Tidak ada alasan kuat di balik kebiasaan ini: itu hanyalah konvensi yang
muncul dengan sendirinya, dan orang-orang sudah terbiasa membaca serta menulis
kode Rust dengan cara begitu.

Pengecualian dari kebiasaan ini terjadi saat kita membawa dua item dengan nama
yang sama ke dalam scope lewat statement `use`, karena Rust tidak mengizinkan
hal itu. Listing 7-15 menunjukkan cara membawa dua tipe `Result` yang namanya
sama tetapi module induknya berbeda ke dalam scope, serta cara merujuknya.

<Listing number="7-15" file-name="src/lib.rs" caption="Membawa dua tipe dengan nama yang sama ke scope yang sama mengharuskan kita menyebut module induknya.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-15/src/lib.rs:here}}
```

</Listing>

Seperti yang bisa kamu lihat, menyebut module induk membedakan kedua tipe
`Result` itu. Jika kita menulis `use std::fmt::Result` dan
`use std::io::Result`, kita akan punya dua tipe `Result` dalam satu scope, dan
Rust tidak akan tahu mana yang kita maksud saat kita menulis `Result`.

### Memberi Nama Baru dengan Keyword `as`

Ada solusi lain untuk masalah membawa dua tipe dengan nama yang sama ke dalam
scope yang sama dengan `use`: setelah path, kita bisa menulis `as` beserta nama
lokal yang baru, atau _alias_, untuk tipe tersebut. Listing 7-16 menunjukkan
cara lain untuk menulis kode pada Listing 7-15 dengan mengganti nama salah satu
tipe `Result` memakai `as`.

<Listing number="7-16" file-name="src/lib.rs" caption="Mengganti nama sebuah tipe saat dibawa ke dalam scope dengan keyword `as`">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-16/src/lib.rs:here}}
```

</Listing>

Pada statement `use` kedua, kita memilih nama baru `IoResult` untuk tipe
`std::io::Result`, yang tidak akan bertabrakan dengan `Result` dari `std::fmt`
yang juga sudah kita bawa ke dalam scope. Listing 7-15 dan Listing 7-16 sama-sama
dianggap idiomatis, jadi pilihannya terserah kamu!

### Mengekspor Ulang Nama dengan `pub use`

Saat kita membawa sebuah nama ke dalam scope dengan keyword `use`, nama itu
bersifat private untuk scope tempat kita mengimpornya. Agar kode di luar scope
tersebut bisa merujuk nama itu seolah-olah ia didefinisikan di scope tersebut,
kita bisa menggabungkan `pub` dan `use`. Teknik ini disebut _re-exporting_
(kemengeksporan ulang) karena kita membawa sebuah item ke dalam scope sekaligus
membuat item itu tersedia bagi orang lain untuk dibawa ke scope mereka.

Listing 7-17 menunjukkan kode dari Listing 7-11 dengan `use` di root module
diubah menjadi `pub use`.

<Listing number="7-17" file-name="src/lib.rs" caption="Membuat sebuah nama tersedia bagi kode mana pun untuk dipakai dari scope baru dengan `pub use`">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-17/src/lib.rs}}
```

</Listing>

Sebelum perubahan ini, kode eksternal harus memanggil fungsi `add_to_waitlist`
dengan menggunakan path
`restaurant::front_of_house::hosting::add_to_waitlist()`, yang juga mensyaratkan
module `front_of_house` ditandai sebagai `pub`. Karena `pub use` ini sudah
mengekspor ulang module `hosting` dari root module, kode eksternal kini bisa
memakai path `restaurant::hosting::add_to_waitlist()` sebagai gantinya.

Re-exporting berguna saat struktur internal kode kamu berbeda dari cara para
programmer yang memanggil kode kamu memandang domain tersebut. Sebagai contoh,
dalam metafora restoran ini, orang-orang yang menjalankan restoran berpikir soal
"front of house" dan "back of house." Namun pelanggan yang mengunjungi restoran
kemungkinan tidak akan memikirkan bagian-bagian restoran dengan istilah
tersebut. Dengan `pub use`, kita bisa menulis kode dengan satu struktur tetapi
mengekspos struktur yang berbeda. Dengan begitu, library kita menjadi terorganisasi
baik baik untuk programmer yang mengerjakan library maupun programmer yang
memanggil library. Kita akan melihat contoh lain dari `pub use` dan pengaruhnya
terhadap dokumentasi crate kamu di [“Mengekspor API Publik yang
Praktis”][ch14-pub-use]<!-- ignore --> di Bab 14.

### Menggunakan Package Eksternal

Di Bab 2, kita membuat sebuah proyek permainan tebakan yang memakai package
eksternal bernama `rand` untuk menghasilkan angka acak. Untuk memakai `rand`
di proyek kita, kita menambahkan baris berikut ke _Cargo.toml_:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch01-01-installation.md
* ch02-00-guessing-game-tutorial.md
* ch14-03-cargo-workspaces.md
-->

<Listing file-name="Cargo.toml">

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:9:}}
```

</Listing>

Menambahkan `rand` sebagai dependency di _Cargo.toml_ memberi tahu Cargo untuk
mengunduh package `rand` beserta dependensinya dari [crates.io](https://crates.io/)
dan membuat `rand` tersedia bagi proyek kita.

Selanjutnya, untuk membawa definisi-definisi `rand` ke dalam scope package kita,
kita menambahkan sebuah baris `use` yang diawali nama crate, `rand`, lalu
mendaftarkan item-item yang ingin kita bawa ke dalam scope. Ingat bahwa di
[“Menghasilkan Angka Acak”][rand]<!-- ignore --> di Bab 2, kita membawa
item-item dari module `rand::prelude` ke dalam scope dan memanggil fungsi
`rand::rng`:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:ch07-04}}
```

Anggota komunitas Rust telah membuat banyak package tersedia di
[crates.io](https://crates.io/), dan menarik salah satunya ke dalam package kamu
melibatkan langkah-langkah yang sama: mendaftarkannya di file _Cargo.toml_
package kamu dan memakai `use` untuk membawa item dari crate mereka ke dalam
scope.

Perhatikan bahwa standard library `std` juga merupakan crate yang eksternal
terhadap package kita. Karena standard library dikirim bersama bahasa Rust, kita
tidak perlu mengubah _Cargo.toml_ untuk menyertakan `std`. Namun kita perlu
merujuknya dengan `use` agar bisa membawa item dari sana ke dalam scope package
kita. Sebagai contoh, untuk `HashMap` kita akan memakai baris ini:

```rust
use std::collections::HashMap;
```

Ini adalah path absolut yang diawali `std`, nama dari crate standard library.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-nested-paths-to-clean-up-large-use-lists"></a>

### Memakai Nested Path untuk Merapikan Daftar `use`

Jika kita memakai banyak item yang didefinisikan dalam crate atau module yang
sama, menuliskan setiap item di barisnya sendiri bisa memakan banyak ruang
vertikal di file kita. Sebagai contoh, dua statement `use` yang kita punya di
permainan tebakan pada Listing 2-4 membawa item-item dari `std` ke dalam scope:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-01-use-std-unnested/src/main.rs:here}}
```

</Listing>

Sebagai gantinya, kita bisa memakai nested path untuk membawa item-item yang
sama ke dalam scope dalam satu baris. Caranya dengan menulis bagian path yang
sama, diikuti dua titik dua, lalu kurung kurawal berisi daftar bagian-bagian
path yang berbeda, seperti ditunjukkan Listing 7-18.

<Listing number="7-18" file-name="src/main.rs" caption="Menulis nested path untuk membawa banyak item dengan prefiks yang sama ke dalam scope">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-18/src/main.rs:here}}
```

</Listing>

Di program yang lebih besar, membawa banyak item ke dalam scope dari crate atau
module yang sama memakai nested path bisa mengurangi jumlah statement `use`
terpisah yang dibutuhkan secara drastis!

Kita bisa memakai nested path di tingkat mana pun dalam sebuah path, dan ini
berguna saat menggabungkan dua statement `use` yang memiliki subpath yang sama.
Sebagai contoh, Listing 7-19 menunjukkan dua statement `use`: satu yang membawa
`std::io` ke dalam scope dan satu yang membawa `std::io::Write` ke dalam scope.

<Listing number="7-19" file-name="src/lib.rs" caption="Dua statement `use` di mana salah satu merupakan subpath dari yang lain">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-19/src/lib.rs}}
```

</Listing>

Bagian yang sama dari kedua path ini adalah `std::io`, dan itu juga merupakan
path pertama yang lengkap. Untuk menggabungkan kedua path ini menjadi satu
statement `use`, kita bisa memakai `self` di dalam nested path, seperti
ditunjukkan Listing 7-20.

<Listing number="7-20" file-name="src/lib.rs" caption="Menggabungkan path pada Listing 7-19 menjadi satu statement `use`">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-20/src/lib.rs}}
```

</Listing>

Baris ini membawa `std::io` dan `std::io::Write` ke dalam scope.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-glob-operator"></a>

### Mengimpor Item dengan Operator Glob

Jika kita ingin membawa _semua_ item publik yang didefinisikan dalam sebuah
path ke dalam scope, kita bisa menulis path tersebut diikuti operator glob `*`:

```rust
use std::collections::*;
```

Statement `use` ini membawa semua item publik yang didefinisikan di
`std::collections` ke dalam scope saat ini. Hati-hati saat memakai operator
glob! Glob bisa membuatnya lebih sulit untuk mengetahui nama-nama apa saja yang
berada di scope dan di mana nama yang dipakai di program kamu didefinisikan.
Selain itu, jika dependensi mengubah definisinya, apa yang kamu impor juga
berubah, yang bisa menyebabkan error compiler saat kamu meng-upgrade dependensi
misalnya dependensi tersebut menambahkan definisi dengan nama yang sama seperti
definisi milikmu di scope yang sama.

Operator glob sering dipakai saat melakukan test untuk membawa semua yang sedang
diuji ke dalam module `tests`; kita akan membahasnya di [“Cara Menulis
Test”][writing-tests]<!-- ignore --> di Bab 11. Operator glob juga kadang
dipakai sebagai bagian dari pola prelude: lihat
[dokumentasi standard library](../std/prelude/index.html#other-preludes)<!-- ignore -->
untuk informasi lebih lanjut tentang pola tersebut.

[ch14-pub-use]: ch14-02-publishing-to-crates-io.html#exporting-a-convenient-public-api
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number
[writing-tests]: ch11-01-writing-tests.html#how-to-write-tests
