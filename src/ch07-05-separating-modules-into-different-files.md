## Memisahkan Module ke File yang Berbeda

Sejauh ini, semua contoh di bab ini mendefinisikan beberapa module dalam satu
file. Ketika module sudah besar, kamu mungkin ingin memindahkan definisinya ke
file terpisah agar kode lebih mudah dinavigasi.

Sebagai contoh, kita mulai dari kode pada Listing 7-17 yang berisi beberapa
module restoran. Kita akan mengekstrak module-module itu ke dalam file, alih-alih
mendefinisikan semuanya di file root crate. Dalam kasus ini, file root crate
adalah _src/lib.rs_, tetapi prosedur ini juga berlaku untuk crate binary yang
file root-nya adalah _src/main.rs_.

Pertama, kita ekstrak module `front_of_house` ke file-nya sendiri. Hapus kode di
dalam kurung kurawal untuk module `front_of_house`, sisakan hanya deklarasi
`mod front_of_house;`, sehingga _src/lib.rs_ berisi kode seperti pada Listing
7-21. Perhatikan bahwa ini belum bisa dikompilasi sampai kita membuat file
_src/front_of_house.rs_ seperti pada Listing 7-22.

<Listing number="7-21" file-name="src/lib.rs" caption="Deklarasi module `front_of_house` yang body-nya akan berada di *src/front_of_house.rs*">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-21-and-22/src/lib.rs}}
```

</Listing>

Selanjutnya, letakkan kode yang tadi ada di dalam kurung kurawal ke file baru
bernama _src/front_of_house.rs_, seperti pada Listing 7-22. Compiler tahu untuk
mencari di file ini karena ia menemukan deklarasi module di root crate dengan
nama `front_of_house`.

<Listing number="7-22" file-name="src/front_of_house.rs" caption="Definisi di dalam module `front_of_house` di *src/front_of_house.rs*">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-21-and-22/src/front_of_house.rs}}
```

</Listing>

Perhatikan bahwa kamu hanya perlu memuat file menggunakan deklarasi `mod`
_satu kali_ di pohon module-mu. Setelah compiler tahu file itu bagian dari
proyek (dan tahu di mana kode itu berada di pohon module berkat penempatan
pernyataan `mod`-mu), file lain di proyekmu sebaiknya merujuk ke kode file
tersebut lewat path ke tempat ia dideklarasikan, seperti yang dibahas di bagian
[“Path untuk Merujuk ke Item di Pohon Module”][paths]<!-- ignore -->. Dengan
kata lain, `mod` _bukan_ operasi “include” seperti yang mungkin kamu lihat di
bahasa pemrograman lain.

Berikutnya, kita ekstrak module `hosting` ke file-nya sendiri. Prosesnya sedikit
berbeda karena `hosting` adalah child module dari `front_of_house`, bukan dari
module root. Kita akan menempatkan file untuk `hosting` di direktori baru yang
dinamai berdasarkan leluhurnya di pohon module, dalam kasus ini
_src/front_of_house_.

Untuk mulai memindahkan `hosting`, kita ubah _src/front_of_house.rs_ agar
berisi hanya deklarasi module `hosting`:

<Listing file-name="src/front_of_house.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-02-extracting-hosting/src/front_of_house.rs}}
```

</Listing>

Lalu, kita buat direktori _src/front_of_house_ dan file _hosting.rs_ untuk
menampung definisi yang dibuat di module `hosting`:

<Listing file-name="src/front_of_house/hosting.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-02-extracting-hosting/src/front_of_house/hosting.rs}}
```

</Listing>

Jika kita malah menaruh _hosting.rs_ di direktori _src_, compiler akan
mengharapkan kode _hosting.rs_ berada di module `hosting` yang dideklarasikan
di root crate, bukan sebagai child dari module `front_of_house`. Aturan compiler
tentang file mana yang harus diperiksa untuk kode module tertentu membuat
direktori dan file lebih cocok dengan pohon module.

> <a id="alternate-file-paths"></a>
> ### Path File Alternatif
>
> Sejauh ini kita sudah membahas path file paling idiomatik yang dipakai
> compiler Rust, tetapi Rust juga mendukung gaya path file yang lebih lama.
> Untuk module bernama `front_of_house` yang dideklarasikan di root crate,
> compiler akan mencari kode module itu di:
>
> - _src/front_of_house.rs_ (yang kita bahas)
> - _src/front_of_house/mod.rs_ (gaya lama, path yang masih didukung)
>
> Untuk module bernama `hosting` yang merupakan submodule dari
> `front_of_house`, compiler akan mencari kode module itu di:
>
> - _src/front_of_house/hosting.rs_ (yang kita bahas)
> - _src/front_of_house/hosting/mod.rs_ (gaya lama, path yang masih didukung)
>
> Jika kamu memakai kedua gaya untuk module yang sama, kamu akan mendapat error
> compiler. Memadukan kedua gaya untuk module yang berbeda dalam proyek yang
> sama itu boleh, tetapi bisa membingungkan bagi orang yang menelusuri
> proyekmu.
>
> Kekurangan utama gaya yang memakai file bernama _mod.rs_ adalah proyekmu bisa
> berakhir dengan banyak file bernama _mod.rs_, yang bisa membingungkan saat
> kamu membukanya bersamaan di editor.

Kita sudah memindahkan kode setiap module ke file terpisah, dan pohon module
tetap sama. Pemanggilan fungsi di `eat_at_restaurant` akan tetap berfungsi
tanpa perubahan apa pun, meskipun definisinya hidup di file yang berbeda.
Teknik ini memungkinkan kamu memindahkan module ke file baru seiring
bertambah besar ukurannya.

Perhatikan bahwa pernyataan `pub use crate::front_of_house::hosting` di
_src/lib.rs_ juga tidak berubah, dan `use` pun tidak berdampak pada file mana
yang dikompilasi sebagai bagian dari crate. Kata kunci `mod` mendeklarasikan
module, dan Rust mencari kode yang masuk ke module itu di file dengan nama
sama dengan module tersebut.

## Ringkasan

Rust memungkinkan kamu memecah package menjadi beberapa crate dan sebuah crate
menjadi module, sehingga kamu bisa merujuk ke item yang didefinisikan di satu
module dari module lain. Kamu bisa melakukan ini dengan menentukan path absolut
atau relatif. Path-path itu bisa dibawa ke scope dengan pernyataan `use`
sehingga kamu bisa memakai path yang lebih pendek saat item itu dipakai
berulang kali di scope tersebut. Kode module bersifat private secara default,
tetapi kamu bisa membuat definisinya publik dengan menambahkan kata kunci `pub`.

Di bab berikutnya, kita akan melihat beberapa struktur data collection di
standard library yang bisa kamu pakai dalam kode yang sudah tersusun rapi.

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
