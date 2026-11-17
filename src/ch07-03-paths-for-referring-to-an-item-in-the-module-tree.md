## Menunjuk ke Sebuah Item di Pohon Module dengan Path

Untuk memberi tahu Rust di mana menemukan sebuah item dalam pohon module, kita
memakai path dengan cara yang sama seperti kita memakai path saat menelusuri
file system. Untuk memanggil sebuah fungsi, kita perlu tahu path-nya.

Path punya dua bentuk:

- _Absolute path_ adalah path lengkap yang dimulai dari akar crate; untuk kode
  dari crate eksternal, path absolut diawali nama crate-nya, sedangkan untuk
  kode dari crate saat ini, path absolut diawali literal `crate`.
- _Relative path_ dimulai dari module saat ini dan memakai `self`, `super`,
  atau sebuah identifier di module tersebut.

Path absolut maupun relative keduanya diikuti oleh satu atau lebih identifier
yang dipisahkan oleh double colon (`::`).

Kembali ke Listing 7-1, misalnya kita ingin memanggil fungsi `add_to_waitlist`.
Pertanyaannya sama saja dengan: apa path fungsi `add_to_waitlist`? Listing 7-3
memuat Listing 7-1 dengan sebagian module dan fungsi yang dihapus.

Kita akan menunjukkan dua cara memanggil fungsi `add_to_waitlist` dari fungsi
baru `eat_at_restaurant` yang didefinisikan di akar crate. Path-path ini sudah
benar, tapi masih ada masalah lain yang membuat contoh ini belum bisa
mengompilasi apa adanya. Kita akan menjelaskan alasannya sebentar lagi.

Fungsi `eat_at_restaurant` adalah bagian dari API publik library crate kita,
jadi kita tandai dengan keyword `pub`. Pada bagian [“Mengekspos Path dengan
Keyword `pub`”][pub]<!-- ignore -->, kita akan membahas `pub` lebih rinci.

<Listing number="7-3" file-name="src/lib.rs" caption="Memanggil fungsi `add_to_waitlist` dengan path absolute dan relative">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-03/src/lib.rs}}
```

</Listing>

Pertama kali kita memanggil fungsi `add_to_waitlist` di `eat_at_restaurant`,
kita memakai path absolute. Fungsi `add_to_waitlist` didefinisikan di crate yang
sama dengan `eat_at_restaurant`, yang berarti kita bisa memakai keyword `crate`
untuk memulai path absolute. Setelah itu kita susuri module demi module sampai
tiba di `add_to_waitlist`. Bayangkan sebuah file system dengan struktur yang
sama: kita akan menuliskan path `/front_of_house/hosting/add_to_waitlist` untuk
menjalankan program `add_to_waitlist`; memakai nama `crate` untuk mulai dari
akar crate itu seperti memakai `/` untuk mulai dari root file system di shell.

Kedua kalinya kita memanggil `add_to_waitlist` di `eat_at_restaurant`, kita
memakai path relative. Path-nya diawali `front_of_house`, nama module yang
didefinisikan pada tingkat yang sama di pohon module dengan
`eat_at_restaurant`. Padanan file system-nya di sini adalah memakai path
`front_of_house/hosting/add_to_waitlist`. Diawali nama module berarti
path-nya relative.

Menentukan apakah memakai path relative atau absolute adalah keputusan yang
kamu buat berdasarkan proyekmu, dan keputusan itu bergantung pada mana yang
lebih mungkin: memindahkan kode definisi item terpisah dari kode yang
memakainya, atau memindahkannya bersamaan. Sebagai contoh, jika kita memindahkan
module `front_of_house` dan fungsi `eat_at_restaurant` ke dalam module bernama
`customer_experience`, kita perlu memperbarui path absolute ke
`add_to_waitlist`, tapi path relative-nya tetap valid. Sebaliknya, jika kita
memindahkan fungsi `eat_at_restaurant` sendirian ke module bernama `dining`,
path absolute ke pemanggilan `add_to_waitlist` tetap sama, tapi path
relative-nya perlu diperbarui. Secara umum kita lebih memilih path absolute
karena kemungkinan besar kita ingin memindahkan definisi kode dan pemanggilan
item secara terpisah satu sama lain.

Ayo coba mengompilasi Listing 7-3 dan cari tahu kenapa kode itu belum bisa
dikompilasi! Error yang kita dapatkan ditampilkan di Listing 7-4.

<Listing number="7-4" caption="Error compiler dari build kode pada Listing 7-3">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-03/output.txt}}
```

</Listing>

Pesan error menyatakan bahwa module `hosting` bersifat private. Dengan kata
lain, path untuk module `hosting` dan fungsi `add_to_waitlist` sudah benar,
tapi Rust tidak mengizinkan kita memakainya karena kita tidak punya akses ke
bagian yang private. Di Rust, semua item (fungsi, method, struct, enum, module,
dan konstanta) bersifat private terhadap module induknya secara default. Jika
kamu ingin membuat sebuah item seperti fungsi atau struct menjadi private, kamu
taruh item itu di dalam sebuah module.

Item di module induk tidak bisa memakai item private di dalam module anak,
tapi item di module anak bisa memakai item di module leluhurnya. Ini karena
module anak membungkus dan menyembunyikan detail implementasinya, sementara
module anak tersebut bisa melihat konteks di mana ia didefinisikan. Lanjutkan
metafora kita, bayangkan aturan privasi seperti kantor belakang sebuah
restoran: yang terjadi di sana adalah hal private bagi para pelanggan restoran,
tapi manajer kantor bisa melihat dan melakukan apa saja di restoran yang mereka
kelola.

Rust memilih membuat sistem module bekerja dengan cara ini agar penyembunyian
detail implementasi inner menjadi default. Dengan begitu, kamu tahu bagian mana
dari kode inner yang boleh kamu ubah tanpa merusak kode luar. Meski begitu,
Rust tetap memberimu pilihan untuk mengekspos bagian inner dari kode module
anak ke module leluhur di luar dengan memakai keyword `pub` agar sebuah item
menjadi publik.

<a id="exposing-paths-with-the-pub-keyword"></a>
### Mengekspos Path dengan Keyword `pub`

Kembali ke error pada Listing 7-4 yang memberi tahu kita bahwa module
`hosting` private. Kita ingin fungsi `eat_at_restaurant` di module induk punya
akses ke fungsi `add_to_waitlist` di module anak, jadi kita tandai module
`hosting` dengan keyword `pub`, seperti ditunjukkan Listing 7-5.

<Listing number="7-5" file-name="src/lib.rs" caption="Mendeklarasikan module `hosting` sebagai `pub` agar bisa dipakai dari `eat_at_restaurant`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-05/src/lib.rs:here}}
```

</Listing>

Sayangnya, kode pada Listing 7-5 tetap menghasilkan error compiler, seperti
ditunjukkan Listing 7-6.

<Listing number="7-6" caption="Error compiler dari build kode pada Listing 7-5">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-05/output.txt}}
```

</Listing>

Apa yang terjadi? Menambahkan keyword `pub` di depan `mod hosting` membuat
module tersebut publik. Dengan perubahan itu, jika kita bisa mengakses
`front_of_house`, kita bisa mengakses `hosting`. Tapi _isi_ dari `hosting`
masih private; membuat module menjadi publik tidak membuat isinya publik.
Keyword `pub` pada sebuah module hanya memungkinkan kode di module leluhurnya
merujuk ke module tersebut, bukan mengakses kode innernya. Karena module adalah
wadah, tidak banyak yang bisa kita lakukan hanya dengan membuat module-nya
publik; kita perlu melangkah lebih jauh dan memilih membuat satu atau lebih item
di dalam module tersebut publik juga.

Error pada Listing 7-6 menyatakan bahwa fungsi `add_to_waitlist` private.
Aturan privasi berlaku untuk struct, enum, fungsi, dan method sama seperti
module.

Mari kita buat juga fungsi `add_to_waitlist` menjadi publik dengan
menambahkan keyword `pub` sebelum definisinya, seperti pada Listing 7-7.

<Listing number="7-7" file-name="src/lib.rs" caption="Menambahkan keyword `pub` ke `mod hosting` dan `fn add_to_waitlist` membuat kita bisa memanggil fungsi tersebut dari `eat_at_restaurant`.">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-07/src/lib.rs:here}}
```

</Listing>

Sekarang kodenya bisa dikompilasi! Untuk melihat kenapa penambahan keyword `pub`
membuat kita bisa memakai path-path ini di `eat_at_restaurant` menurut aturan
privasi, mari kita bahas path absolute dan path relative-nya.

Pada path absolute, kita mulai dari `crate`, akar pohon module crate kita.
Module `front_of_house` didefinisikan di akar crate. Meski `front_of_house`
bukan publik, karena fungsi `eat_at_restaurant` didefinisikan di module yang
sama dengan `front_of_house` (yaitu `eat_at_restaurant` dan `front_of_house`
saudara), kita bisa merujuk ke `front_of_house` dari `eat_at_restaurant`.
Berikutnya adalah module `hosting` yang ditandai `pub`. Kita bisa mengakses
module induk dari `hosting`, jadi kita bisa mengakses `hosting`. Terakhir,
fungsi `add_to_waitlist` ditandai `pub`, dan kita bisa mengakses module
induknya, jadi pemanggilan fungsi ini berhasil!

Pada path relative, logikanya sama dengan path absolute kecuali pada langkah
pertama: alih-alih mulai dari akar crate, path-nya dimulai dari
`front_of_house`. Module `front_of_house` didefinisikan di dalam module yang
sama dengan `eat_at_restaurant`, jadi path relative yang dimulai dari module
tempat `eat_at_restaurant` didefinisikan berhasil dipakai. Lalu, karena
`hosting` dan `add_to_waitlist` ditandai `pub`, sisa path-nya berfungsi, dan
pemanggilan fungsi ini valid!

Jika kamu berencana membagikan library crate-mu agar proyek lain bisa memakai
kode kamu, API publikmu adalah kontrak dengan pengguna crate kamu yang
menentukan bagaimana mereka bisa berinteraksi dengan kode kamu. Ada banyak
pertimbangan seputar mengelola perubahan pada API publikmu agar lebih mudah
bagi orang untuk memakai crate kamu. Pertimbangan-pertimbangan itu di luar
cakupan buku ini; jika kamu tertarik pada topik ini, lihat [the Rust API
Guidelines][api-guidelines].

> #### Praktik Terbaik untuk Package dengan Binary dan Library
>
> Kita sudah menyebutkan bahwa sebuah package bisa berisi akar binary crate
> _src/main.rs_ sekaligus akar library crate _src/lib.rs_, dan kedua crate
> tersebut akan memakai nama package secara default. Biasanya, package dengan
> pola yang memuat library crate dan binary crate sekaligus hanya punya kode
> secukupnya di binary crate untuk memulai executable yang memanggil kode yang
> didefinisikan di library crate. Dengan begitu, proyek lain bisa memanfaatkan
> sebagian besar fungsionalitas yang diberikan package karena kode library
> crate-nya bisa dibagikan.
>
> Pohon module seharusnya didefinisikan di _src/lib.rs_. Setelah itu, item
> publik mana pun bisa dipakai di binary crate dengan memulai path dari nama
> package. Binary crate menjadi pengguna library crate seperti crate eksternal
> sepenuhnya memakai library crate: ia hanya bisa memakai API publik. Ini
> membantumu merancang API yang baik; bukan hanya kamu sebagai penulis, tapi
> kamu juga seorang klien!
>
> Pada [Bab 12][ch12]<!-- ignore -->, kita akan mendemonstrasikan praktik
> organisasi ini dengan program command line yang memuat binary crate sekaligus
> library crate.

### Memulai Path Relative dengan `super`

Kita bisa membentuk path relative yang dimulai dari module induk, bukan dari
module saat ini atau akar crate, dengan memakai `super` di awal path. Ini
seperti memulai path file system dengan sintaks `..` yang berarti pergi ke
direktori induk. Memakai `super` memungkinkan kita merujuk ke sebuah item yang
kita tahu berada di module induk, yang bisa mempermudah penataan ulang pohon
module saat module tersebut berkaitan erat dengan induknya tapi suatu saat
induknya mungkin dipindah ke tempat lain dalam pohon module.

Perhatikan kode pada Listing 7-8 yang memodelkan situasi di mana seorang koki
memperbaiki pesanan yang salah dan mengantarkannya sendiri kepada pelanggan.
Fungsi `fix_incorrect_order` yang didefinisikan di module `back_of_house`
memanggil fungsi `deliver_order` yang didefinisikan di module induk dengan
menentukan path ke `deliver_order`, diawali `super`.

<Listing number="7-8" file-name="src/lib.rs" caption="Memanggil fungsi dengan path relative yang diawali `super`">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-08/src/lib.rs}}
```

</Listing>

Fungsi `fix_incorrect_order` berada di module `back_of_house`, jadi kita bisa
memakai `super` untuk pergi ke module induk `back_of_house`, yang dalam kasus
ini adalah `crate`, akarnya. Dari sana, kita mencari `deliver_order` dan
menemukannya. Sukses! Kami rasa module `back_of_house` dan fungsi
`deliver_order` kemungkinan akan tetap mempertahankan hubungan yang sama satu
sama lain dan dipindah bersamaan jika kita memutuskan menata ulang pohon module
crate. Karena itu kita memakai `super` agar nanti ada lebih sedikit tempat yang
perlu kita perbarui kodenya jika kode ini dipindah ke module lain.

### Membuat Struct dan Enum Menjadi Publik

Kita juga bisa memakai `pub` untuk menandai struct dan enum sebagai publik,
tapi ada beberapa detail tambahan tentang penggunaan `pub` bersama struct dan
enum. Jika kita memakai `pub` sebelum sebuah definisi struct, kita membuat
struct tersebut publik, tapi field-field struct-nya tetap private. Kita bisa
membuat setiap field publik atau tidak, kasus demi kasus. Pada Listing 7-9,
kita mendefinisikan struct publik `back_of_house::Breakfast` dengan field
`toast` yang publik dan field `seasonal_fruit` yang private. Ini memodelkan
kasus di sebuah restoran di mana pelanggan bisa memilih jenis roti yang
menyertai hidangan, tapi koki yang memilih buah pendamping hidangan berdasarkan
musim dan stok yang tersedia. Buah yang tersedia cepat berubah, jadi pelanggan
tidak bisa memilih buahnya atau bahkan melihat buah apa yang akan mereka
dapatkan.

<Listing number="7-9" file-name="src/lib.rs" caption="Sebuah struct dengan sebagian field publik dan sebagian field private">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-09/src/lib.rs}}
```

</Listing>

Karena field `toast` pada struct `back_of_house::Breakfast` publik, di
`eat_at_restaurant` kita bisa menulis dan membaca field `toast` dengan
notasi titik. Perhatikan bahwa kita tidak bisa memakai field `seasonal_fruit`
di `eat_at_restaurant`, karena `seasonal_fruit` private. Coba hapus tanda
komentar pada baris yang mengubah nilai field `seasonal_fruit` untuk melihat
error apa yang kamu dapatkan!

Perhatikan juga bahwa karena `back_of_house::Breakfast` punya field private,
struct tersebut perlu menyediakan fungsi terkait (associated function) publik
yang membuat instance `Breakfast` (di sini kita menamainya `summer`). Jika
`Breakfast` tidak punya fungsi seperti itu, kita tidak bisa membuat instance
`Breakfast` di `eat_at_restaurant`, karena kita tidak bisa mengatur nilai field
private `seasonal_fruit` di `eat_at_restaurant`.

Sebaliknya, jika kita membuat sebuah enum menjadi publik, semua variant-nya
menjadi publik. Kita hanya perlu `pub` sebelum keyword `enum`, seperti
ditunjukkan Listing 7-10.

<Listing number="7-10" file-name="src/lib.rs" caption="Menandai sebuah enum sebagai publik membuat semua variant-nya publik.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-10/src/lib.rs}}
```

</Listing>

Karena kita membuat enum `Appetizer` publik, kita bisa memakai variant `Soup`
dan `Salad` di `eat_at_restaurant`.

Enum tidak terlalu berguna jika variant-nya tidak publik; akan merepotkan jika
harus menandai semua variant enum dengan `pub` di setiap kasus, jadi default
untuk variant enum adalah publik. Struct sering tetap berguna tanpa field-nya
publik, jadi field struct mengikuti aturan umum bahwa semuanya private secara
default kecuali ditandai dengan `pub`.

Ada satu situasi lagi yang melibatkan `pub` yang belum kita bahas, dan itu
adalah fitur module terakhir kita: keyword `use`. Kita akan membahas `use`
terlebih dulu, lalu kita akan menunjukkan cara menggabungkan `pub` dan `use`.

[pub]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[api-guidelines]: https://rust-lang.github.io/api-guidelines/
[ch12]: ch12-00-an-io-project.html
