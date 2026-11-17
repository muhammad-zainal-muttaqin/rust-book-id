## Menjalankan Kode saat Pembersihan dengan Trait `Drop`

Trait kedua yang penting bagi pola smart pointer adalah `Drop`, yang membiarkan
kamu menentukan apa yang terjadi ketika sebuah nilai akan keluar dari scope. Kamu
bisa menyediakan implementasi trait `Drop` pada tipe apa pun, dan kode tersebut
dapat dipakai untuk melepaskan sumber daya seperti file atau koneksi jaringan.

Kita memperkenalkan `Drop` dalam konteks smart pointer karena fungsi trait `Drop`
hampir selalu dipakai saat mengimplementasikan sebuah smart pointer. Misalnya,
ketika sebuah `Box<T>` di-drop, ia akan membebaskan ruang di heap yang ditunjuk
oleh box tersebut.

Pada beberapa bahasa, untuk beberapa tipe, programmer harus memanggil kode untuk
membebaskan memori atau sumber daya setiap kali selesai memakai sebuah instance
dari tipe tersebut. Contohnya meliputi file handle, socket, dan lock. Jika
programmer lupa, sistem bisa menjadi kewalahan dan crash. Di Rust, kamu bisa
menentukan bahwa sepotong kode tertentu dijalankan setiap kali sebuah nilai
keluar dari scope, dan compiler akan menyisipkan kode itu secara otomatis.
Hasilnya, kamu tidak perlu repot memasang kode pembersihan di mana-mana dalam
program setiap kali sebuah instance dari suatu tipe selesai dipakai—kamu tetap
tidak akan membocorkan sumber daya!

Kamu menentukan kode yang dijalankan ketika sebuah nilai keluar dari scope dengan
mengimplementasikan trait `Drop`. Trait `Drop` mewajibkan kamu mengimplementasikan
satu metode bernama `drop` yang menerima reference mutable ke `self`. Untuk
melihat kapan Rust memanggil `drop`, mari kita implementasikan `drop` dengan
pernyataan `println!` untuk sementara ini.

Listing 15-14 menunjukkan sebuah struct `CustomSmartPointer` yang satu-satunya
fungsi khususnya adalah mencetak `Dropping CustomSmartPointer!` ketika instance
keluar dari scope, agar kita bisa melihat kapan Rust menjalankan metode `drop`.

<Listing number="15-14" file-name="src/main.rs" caption="Struct `CustomSmartPointer` yang mengimplementasikan trait `Drop` di tempat kita akan meletakkan kode pembersihan">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-14/src/main.rs}}
```

</Listing>

Trait `Drop` sudah termasuk dalam prelude, jadi kita tidak perlu membawanya ke
dalam scope. Kita mengimplementasikan trait `Drop` pada `CustomSmartPointer` dan
menyediakan implementasi metode `drop` yang memanggil `println!`. Tubuh metode
`drop` adalah tempat kamu meletakkan logika apa pun yang ingin kamu jalankan
ketika sebuah instance dari tipemu keluar dari scope. Di sini kita mencetak
beberapa teks agar terlihat secara visual kapan Rust akan memanggil `drop`.

Di `main`, kita membuat dua instance `CustomSmartPointer` lalu mencetak
`CustomSmartPointers created`. Di akhir `main`, instance `CustomSmartPointer`
kita akan keluar dari scope, dan Rust akan memanggil kode yang kita letakkan di
dalam metode `drop`, lalu mencetak pesan terakhir kita. Perhatikan bahwa kita
tidak perlu memanggil metode `drop` secara eksplisit.

Ketika kita menjalankan program ini, kita akan melihat keluaran berikut:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-14/output.txt}}
```

Rust otomatis memanggil `drop` untuk kita ketika instance kita keluar dari scope,
menjalankan kode yang kita tentukan. Variabel di-drop dalam urutan terbalik dari
urutan pembuatannya, jadi `d` di-drop sebelum `c`. Tujuan contoh ini adalah
memberi kamu gambaran visual tentang cara kerja metode `drop`; biasanya kamu akan
menentukan kode pembersihan yang dibutuhkan tipemu, bukan sebuah pesan cetak.

<!-- Old headings. Do not remove or links may break. -->

<a id="dropping-a-value-early-with-std-mem-drop"></a>

Sayangnya, menonaktifkan fungsi `drop` otomatis itu tidak langsung gampang.
Menonaktifkan `drop` biasanya memang tidak perlu; seluruh tujuan trait `Drop`
adalah agar semuanya ditangani secara otomatis. Namun, kadang kamu mungkin ingin
membersihkan sebuah nilai lebih awal. Salah satu contohnya adalah saat memakai
smart pointer yang mengelola lock: Kamu mungkin ingin memaksa metode `drop` yang
melepaskan lock itu agar kode lain dalam scope yang sama bisa mendapatkan lock
tersebut. Rust tidak mengizinkan kamu memanggil metode `drop` dari trait `Drop`
secara manual; sebagai gantinya, kamu harus memanggil fungsi `std::mem::drop`
yang disediakan oleh library standar jika ingin memaksa sebuah nilai di-drop
sebelum akhir scope-nya.

Mencoba memanggil metode `drop` dari trait `Drop` secara manual dengan mengubah
fungsi `main` dari Listing 15-14 tidak akan berhasil, seperti yang ditunjukkan
dalam Listing 15-15.

<Listing number="15-15" file-name="src/main.rs" caption="Mencoba memanggil metode `drop` dari trait `Drop` secara manual untuk membersihkan lebih awal">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-15/src/main.rs:here}}
```

</Listing>

Ketika kita mencoba mengompilasi kode ini, kita akan mendapat error ini:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-15/output.txt}}
```

Pesan error ini menyatakan bahwa kita tidak diperbolehkan memanggil `drop` secara
eksplisit. Pesan error tersebut memakai istilah _destructor_, yaitu istilah umum
dalam pemrograman untuk fungsi yang membersihkan sebuah instance. Sebuah
_destructor_ mirip dengan _constructor_, yang membuat sebuah instance. Fungsi
`drop` di Rust adalah salah satu destructor tertentu.

Rust tidak membiarkan kita memanggil `drop` secara eksplisit, karena Rust tetap
akan memanggil `drop` pada nilai itu secara otomatis di akhir `main`. Hal itu akan
menyebabkan error double free karena Rust mencoba membersihkan nilai yang sama
dua kali.

Kita tidak bisa menonaktifkan penyisipan otomatis `drop` ketika sebuah nilai
keluar dari scope, dan kita tidak bisa memanggil metode `drop` secara eksplisit.
Jadi, jika kita perlu memaksa sebuah nilai dibersihkan lebih awal, kita memakai
fungsi `std::mem::drop`.

Fungsi `std::mem::drop` berbeda dengan metode `drop` dalam trait `Drop`. Kita
memanggilnya dengan memberikan sebagai argumen nilai yang ingin kita paksa
untuk di-drop. Fungsi ini ada dalam prelude, jadi kita bisa mengubah `main` dalam
Listing 15-15 agar memanggil fungsi `drop`, seperti yang ditunjukkan dalam Listing
15-16.

<Listing number="15-16" file-name="src/main.rs" caption="Memanggil `std::mem::drop` untuk secara eksplisit me-drop sebuah nilai sebelum ia keluar dari scope">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-16/src/main.rs:here}}
```

</Listing>

Menjalankan kode ini akan mencetak hal berikut:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-16/output.txt}}
```

Teks ``Dropping CustomSmartPointer with data `some data`!`` dicetak di antara
teks `CustomSmartPointer created` dan `CustomSmartPointer dropped before the end
of main`, menunjukkan bahwa kode metode `drop` dipanggil untuk me-drop `c` pada
titik itu.

Kamu bisa memakai kode yang ditentukan dalam implementasi trait `Drop` dengan
berbagai cara agar pembersihan menjadi mudah dan aman: Misalnya, kamu bisa
memakainya untuk membuat alokator memorimu sendiri! Dengan trait `Drop` dan
sistem ownership Rust, kamu tidak perlu mengingat untuk membersihkan, karena
Rust melakukannya secara otomatis.

Kamu juga tidak perlu khawatir akan masalah yang timbul akibat tidak sengaja
membersihkan nilai yang masih dipakai: Sistem ownership yang memastikan reference
selalu valid juga memastikan bahwa `drop` hanya dipanggil sekali ketika nilai
tersebut tidak lagi dipakai.

Sekarang setelah kita mempelajari `Box<T>` dan beberapa karakteristik smart
pointer, mari kita lihat beberapa smart pointer lain yang didefinisikan dalam
library standar.
