<!-- Old headings. Do not remove or links may break. -->

<a id="defining-modules-to-control-scope-and-privacy"></a>

## Mengontrol Scope dan Privasi dengan Module

Di bagian ini, kita akan membahas module dan bagian lain dari module system,
yaitu _path_, yang memungkinkan kamu menamai item; kata kunci `use` yang
membawa sebuah path ke dalam scope; serta kata kunci `pub` untuk membuat item
menjadi publik. Kita juga akan membahas kata kunci `as`, package eksternal,
dan operator glob.

### Cheat Sheet Module

Sebelum masuk ke detail module dan path, berikut kami sajikan referensi cepat
tentang cara module, path, kata kunci `use`, dan kata kunci `pub` bekerja di
compiler, serta cara sebagian besar developer mengorganisasi kode mereka.
Sepanjang bab ini kita akan menelusuri contoh untuk setiap aturan tersebut,
tetapi bagian ini adalah tempat yang bagus untuk dikunjungi kembali sebagai
pengingat cara kerja module.

- **Mulai dari crate root**: Saat mengompilasi sebuah crate, compiler pertama
  kali mencari kode yang akan dikompilasi di file crate root (biasanya
  _src/lib.rs_ untuk library crate dan _src/main.rs_ untuk binary crate).
- **Mendeklarasikan module**: Di file crate root, kamu bisa mendeklarasikan
  module baru; misalnya kamu mendeklarasikan module “garden” dengan
  `mod garden;`. Compiler akan mencari kode module itu di tempat-tempat
  berikut:
  - Inline, di dalam kurung kurawal yang menggantikan titik koma setelah `mod
    garden`
  - Di file _src/garden.rs_
  - Di file _src/garden/mod.rs_
- **Mendeklarasikan submodule**: Di file mana pun selain crate root, kamu bisa
  mendeklarasikan submodule. Sebagai contoh, kamu mungkin mendeklarasikan
  `mod vegetables;` di _src/garden.rs_. Compiler akan mencari kode submodule
  itu di dalam direktori yang dinamai sesuai module induknya, tepatnya di
  tempat-tempat berikut:
  - Inline, tepat setelah `mod vegetables`, di dalam kurung kurawal sebagai
    pengganti titik koma
  - Di file _src/garden/vegetables.rs_
  - Di file _src/garden/vegetables/mod.rs_
- **Path ke kode di dalam module**: Setelah sebuah module menjadi bagian dari
  crate kamu, kamu bisa merujuk ke kode di module itu dari mana pun di dalam
  crate yang sama, selama aturan privasi mengizinkan, dengan memakai path ke
  kode tersebut. Sebagai contoh, tipe `Asparagus` di module garden vegetables
  akan ditemukan di `crate::garden::vegetables::Asparagus`.
- **Privat vs. publik**: Kode di dalam sebuah module bersifat privat terhadap
  module induknya secara default. Untuk membuat sebuah module publik,
  deklarasikan dengan `pub mod` alih-alih `mod`. Agar item di dalam module
  publik juga ikut publik, gunakan `pub` sebelum deklarasinya.
- **Kata kunci `use`**: Di dalam sebuah scope, kata kunci `use` membuat jalan
  pintas ke suatu item agar kamu tidak perlu mengulang path yang panjang. Di
  scope mana pun yang bisa merujuk ke `crate::garden::vegetables::Asparagus`,
  kamu bisa membuat jalan pintas dengan `use
  crate::garden::vegetables::Asparagus;`, dan setelahnya kamu cukup menulis
  `Asparagus` untuk memakai tipe itu di scope tersebut.

Di sini, kita membuat binary crate bernama `backyard` yang mengilustrasikan
aturan-aturan ini. Direktori crate, yang juga bernama _backyard_, berisi file
dan direktori berikut:

```text
backyard
├── Cargo.lock
├── Cargo.toml
└── src
    ├── garden
    │   └── vegetables.rs
    ├── garden.rs
    └── main.rs
```

Dalam kasus ini, file crate root-nya adalah _src/main.rs_, dan isinya:

<Listing file-name="src/main.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/main.rs}}
```

</Listing>

Baris `pub mod garden;` memberi tahu compiler untuk menyertakan kode yang ia
temukan di _src/garden.rs_, yaitu:

<Listing file-name="src/garden.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden.rs}}
```

</Listing>

Di sini, `pub mod vegetables;` berarti kode di _src/garden/vegetables.rs_ juga
ikut disertakan. Kode tersebut adalah:

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden/vegetables.rs}}
```

Sekarang, mari kita masuk ke detail aturan-aturan itu dan membuktikannya
secara langsung!

### Mengelompokkan Kode yang Berkaitan dalam Module

_Module_ memungkinkan kita mengorganisasi kode di dalam sebuah crate agar
mudah dibaca dan mudah dipakai ulang. Module juga mengontrol _privasi_ sebuah
item karena kode di dalam module bersifat privat secara default. Item yang
privat adalah detail implementasi internal yang tidak tersedia untuk dipakai
dari luar. Kita bisa memilih membuat module dan isinya menjadi publik, sehingga
kode eksternal bisa memakai dan bergantung padanya.

Sebagai contoh, kita tulis sebuah library crate yang menyediakan fungsionalitas
sebuah restoran. Kita akan mendefinisikan signature fungsi-fungsi tersebut
tetapi membiarkan body-nya kosong, supaya fokus kita pada organisasi kode,
bukan pada implementasi sebuah restoran.

Di dunia restoran, sebagian bagian restoran disebut _front of house_ dan
sisanya _back of house_. _Front of house_ adalah area yang didapati pelanggan;
di situ penerima tamu menempatkan pelanggan, pelayan menerima pesanan dan
pembayaran, dan bartender meracik minuman. _Back of house_ adalah area tempat
chef dan koki bekerja di dapur, tukang cuci piring membersihkan peralatan, dan
manajer mengurus pekerjaan administratif.

Untuk menata crate kita seperti itu, kita bisa mengorganisasi fungsi-fungsi ke
dalam module bersarang. Buat library baru bernama `restaurant` dengan
menjalankan `cargo new restaurant --lib`. Lalu, masukkan kode pada Listing 7-1
ke dalam _src/lib.rs_ untuk mendefinisikan beberapa module dan signature
fungsi; kode ini adalah bagian front of house.

<Listing number="7-1" file-name="src/lib.rs" caption="Module `front_of_house` yang berisi module lain yang di dalamnya terdapat fungsi">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-01/src/lib.rs}}
```

</Listing>

Kita mendefinisikan sebuah module dengan kata kunci `mod` diikuti nama module
(dalam kasus ini, `front_of_house`). Lalu body module diletakkan di dalam
kurung kurawal. Di dalam module, kita bisa menempatkan module lain, seperti
pada kasus ini dengan module `hosting` dan `serving`. Module juga bisa
menyimpan definisi item lain, seperti struct, enum, konstanta, trait, dan
seperti pada Listing 7-1, fungsi.

Dengan memakai module, kita bisa mengelompokkan definisi yang berkaitan, lalu
menamai alasan definisi itu berkaitan. Programmer yang memakai kode ini bisa
menelusuri kode berdasarkan kelompok tersebut alih-alih harus membaca semua
definisi, sehingga lebih mudah menemukan definisi yang relevan bagi mereka.
Programmer yang menambahkan fungsionalitas baru ke kode ini pun tahu di mana
harus menaruh kode agar program tetap terorganisasi.

Tadi, kita menyebut _src/main.rs_ dan _src/lib.rs_ sebagai _crate root_.
Penamaan itu karena isi kedua file tersebut membentuk module bernama `crate` di
root struktur module crate, yang dikenal sebagai _pohon module_.

Listing 7-2 menunjukkan pohon module untuk struktur pada Listing 7-1.

<Listing number="7-2" caption="Pohon module untuk kode pada Listing 7-1">

```text
crate
 └── front_of_house
     ├── hosting
     │   ├── add_to_waitlist
     │   └── seat_at_table
     └── serving
         ├── take_order
         ├── serve_order
         └── take_payment
```

</Listing>

Pohon ini menunjukkan bagaimana beberapa module bersarang di dalam module
lain; misalnya, `hosting` bersarang di dalam `front_of_house`. Pohon ini juga
menunjukkan bahwa beberapa module bersifat _siblings_, artinya mereka
didefinisikan di module yang sama; `hosting` dan `serving` adalah siblings yang
didefinisikan di dalam `front_of_house`. Jika module A berada di dalam module
B, kita menyebut module A sebagai _child_ dari module B dan module B sebagai
_parent_ dari module A. Perhatikan bahwa seluruh pohon module berakar pada
module implisit bernama `crate`.

Pohon module mungkin mengingatkan kamu pada pohon direktori di filesystem
komputermu; perbandingan ini memang sangat tepat! Sama seperti direktori di
filesystem, kamu memakai module untuk mengorganisasi kode. Dan sama seperti
file di dalam sebuah direktori, kita memerlukan cara untuk menemukan module
kita.
