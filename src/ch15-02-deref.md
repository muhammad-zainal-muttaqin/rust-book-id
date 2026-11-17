<!-- Old headings. Do not remove or links may break. -->

<a id="treating-smart-pointers-like-regular-references-with-the-deref-trait"></a>
<a id="treating-smart-pointers-like-regular-references-with-deref"></a>

<a id="treating-smart-pointers-like-regular-references"></a>
## Memperlakukan Smart Pointer Seperti Reference Biasa

Dengan mengimplementasikan trait `Deref`, kamu bisa mengatur perilaku _operator
dereference_ `*` (jangan tertukar dengan operator perkalian atau glob). Kalau
`Deref` diimplementasikan sedemikian rupa sehingga smart pointer bisa
diperlakukan seperti reference biasa, kamu bisa menulis kode yang bekerja pada
reference lalu memakai kode itu juga pada smart pointer.

Mula-mula, kita lihat dulu cara kerja operator dereference pada reference biasa.
Setelah itu, kita coba mendefinisikan tipe sendiri yang berperilaku seperti
`Box<T>` dan melihat mengapa operator dereference tidak bekerja seperti
reference pada tipe baru kita. Kita akan menjelajahi bagaimana mengimplementasikan
trait `Deref` membuat smart pointer bisa bekerja dengan cara yang mirip
reference. Lalu, kita bahas fitur deref coercion di Rust dan cara fitur itu
membiarkan kita bekerja dengan reference maupun smart pointer.

<!-- Old headings. Do not remove or links may break. -->

<a id="following-the-pointer-to-the-value-with-the-dereference-operator"></a>
<a id="following-the-pointer-to-the-value"></a>

### Mengikuti Reference ke Nilainya

Reference biasa adalah salah satu jenis pointer, dan cara mudah membayangkan
pointer adalah sebagai panah yang menunjuk ke nilai yang tersimpan di tempat
lain. Di Listing 15-6, kita membuat reference ke nilai `i32`, lalu memakai
operator dereference untuk mengikuti reference itu ke nilainya.

<Listing number="15-6" file-name="src/main.rs" caption="Memakai operator dereference untuk mengikuti reference ke nilai `i32`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-06/src/main.rs}}
```

</Listing>

Variabel `x` menyimpan nilai `i32` sebesar `5`. Kita menetapkan `y` sebagai
reference ke `x`. Kita bisa menegaskan bahwa `x` sama dengan `5`. Namun, kalau
kita ingin menegaskan nilai di dalam `y`, kita harus memakai `*y` untuk
mengikuti reference itu ke nilai yang ditunjuknya (makanya disebut
_dereference_) agar compiler bisa membandingkan nilai yang sebenarnya. Setelah
kita mendereference `y`, kita bisa mengakses nilai integer yang ditunjuk `y`
lalu membandingkannya dengan `5`.

Kalau kita mencoba menulis `assert_eq!(5, y);` sebagai gantinya, kita akan
mendapat error kompilasi ini:

```console
{{#include ../listings/ch15-smart-pointers/output-only-01-comparing-to-reference/output.txt}}
```

Membandingkan sebuah angka dengan reference ke angka tidak diperbolehkan karena
keduanya bertipe berbeda. Kita harus memakai operator dereference untuk
mengikuti reference itu ke nilai yang ditunjuknya.

### Memakai `Box<T>` Seperti Reference

Kita bisa menulis ulang kode di Listing 15-6 agar memakai `Box<T>` sebagai
pengganti reference; operator dereference yang dipakai pada `Box<T>` di Listing
15-7 bekerja dengan cara yang sama seperti operator dereference pada reference
di Listing 15-6.

<Listing number="15-7" file-name="src/main.rs" caption="Memakai operator dereference pada `Box<i32>`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-07/src/main.rs}}
```

</Listing>

Perbedaan utama antara Listing 15-7 dan Listing 15-6 adalah di sini kita
menetapkan `y` sebagai sebuah instance box yang menunjuk ke salinan nilai `x`,
bukan reference yang menunjuk ke nilai `x`. Pada penegasan terakhir, kita bisa
memakai operator dereference untuk mengikuti pointer milik box itu dengan cara
yang sama seperti saat `y` masih berupa reference. Berikutnya, kita akan
menjelajahi apa yang istimewa dari `Box<T>` sehingga kita bisa memakai operator
dereference, dengan mendefinisikan tipe box kita sendiri.

### Mendefinisikan Smart Pointer Sendiri

Mari kita bangun tipe pembungkus yang mirip dengan tipe `Box<T>` yang
disediakan pustaka standar, agar kita bisa merasakan bagaimana tipe smart
pointer berperilaku berbeda dari reference secara bawaan. Setelah itu, kita lihat
cara menambahkan kemampuan memakai operator dereference.

> Catatan: Ada satu perbedaan besar antara tipe `MyBox<T>` yang akan kita bangun
> dan `Box<T>` yang asli: versi kita tidak akan menyimpan datanya di heap. Kita
> memusatkan contoh ini pada `Deref`, jadi tempat data itu sebenarnya disimpan
> kurang penting dibanding perilaku menyerupai pointer.

Tipe `Box<T>` pada akhirnya didefinisikan sebagai tuple struct dengan satu
elemen, jadi Listing 15-8 mendefinisikan tipe `MyBox<T>` dengan cara yang sama.
Kita juga akan mendefinisikan fungsi `new` agar sepadan dengan fungsi `new` yang
didefinisikan pada `Box<T>`.

<Listing number="15-8" file-name="src/main.rs" caption="Mendefinisikan tipe `MyBox<T>`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-08/src/main.rs:here}}
```

</Listing>

Kita mendefinisikan struct bernama `MyBox` dan mendeklarasikan parameter generic
`T` karena kita ingin tipe kita bisa menyimpan nilai dari tipe apa pun. Tipe
`MyBox` adalah tuple struct dengan satu elemen bertipe `T`. Fungsi `MyBox::new`
menerima satu parameter bertipe `T` dan mengembalikan instance `MyBox` yang
menyimpan nilai yang diberikan.

Mari kita coba menambahkan fungsi `main` dari Listing 15-7 ke Listing 15-8 dan
mengubahnya agar memakai tipe `MyBox<T>` yang sudah kita definisikan, bukan
`Box<T>`. Kode di Listing 15-9 tidak akan terkompilasi karena Rust belum tahu
cara mendereference `MyBox`.

<Listing number="15-9" file-name="src/main.rs" caption="Mencoba memakai `MyBox<T>` dengan cara yang sama seperti kita memakai reference dan `Box<T>`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-09/src/main.rs:here}}
```

</Listing>

Berikut error kompilasi yang dihasilkan:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-09/output.txt}}
```

Tipe `MyBox<T>` kita belum bisa didereference karena kita belum
mengimplementasikan kemampuan itu pada tipe kita. Agar dereferencing dengan
operator `*` bisa dilakukan, kita mengimplementasikan trait `Deref`.

<!-- Old headings. Do not remove or links may break. -->

<a id="treating-a-type-like-a-reference-by-implementing-the-deref-trait"></a>

### Mengimplementasikan Trait `Deref`

Seperti yang kita bahas di [“Mengimplementasikan Trait pada Tipe”][impl-trait]<!-- ignore --> di Bab 10, untuk mengimplementasikan sebuah trait kita perlu
menyediakan implementasi untuk method-method wajibnya. Trait `Deref`, yang
disediakan pustaka standar, mewajibkan kita mengimplementasikan satu method
bernama `deref` yang meminjam `self` dan mengembalikan reference ke data di
dalamnya. Listing 15-10 berisi implementasi `Deref` yang bisa ditambahkan ke
definisi `MyBox<T>`.

<Listing number="15-10" file-name="src/main.rs" caption="Mengimplementasikan `Deref` pada `MyBox<T>`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-10/src/main.rs:here}}
```

</Listing>

Sintaks `type Target = T;` mendefinisikan associated type yang dipakai oleh
trait `Deref`. Associated type adalah cara yang sedikit berbeda untuk
mendeklarasikan parameter generic, tetapi kamu tidak perlu memikirkannya
sekarang; kita akan membahasnya lebih rinci di Bab 20.

Kita mengisi tubuh method `deref` dengan `&self.0` agar `deref` mengembalikan
reference ke nilai yang ingin kita akses dengan operator `*`; ingat dari
[“Membuat Tipe Berbeda dengan Tuple Struct”][tuple-structs]<!-- ignore --> di Bab 5 bahwa `.0` mengakses nilai pertama dalam tuple struct. Fungsi `main`
di Listing 15-9 yang memanggil `*` pada nilai `MyBox<T>` sekarang bisa
terkompilasi, dan penegasan-penegasannya lolos!

Tanpa trait `Deref`, compiler hanya bisa mendereference reference `&`. Method
`deref` memberi compiler kemampuan untuk mengambil nilai dari tipe apa pun yang
mengimplementasikan `Deref` lalu memanggil method `deref` guna mendapatkan
reference yang tahu cara didereference.

Saat kita menulis `*y` di Listing 15-9, di balik layar Rust sebenarnya menjalankan
kode ini:

```rust,ignore
*(y.deref())
```

Rust mengganti operator `*` dengan panggilan ke method `deref`, lalu melakukan
dereference biasa, sehingga kita tidak perlu memikirkan apakah harus memanggil
method `deref` atau tidak. Fitur Rust ini membiarkan kita menulis kode yang
bekerja dengan cara yang sama, baik kita punya reference biasa maupun tipe yang
mengimplementasikan `Deref`.

Alasan method `deref` mengembalikan reference ke nilai, dan dereference biasa di
luar tanda kurung pada `*(y.deref())` tetap diperlukan, berkaitan dengan sistem
ownership. Kalau method `deref` mengembalikan nilai secara langsung, bukan
reference ke nilai itu, nilai tersebut akan dipindahkan keluar dari `self`. Kita
tidak ingin mengambil ownership atas nilai di dalam `MyBox<T>` dalam kasus ini,
maupun dalam kebanyakan kasus saat kita memakai operator dereference.

Perhatikan bahwa operator `*` diganti dengan panggilan ke method `deref` lalu
panggilan ke operator `*` hanya sekali, setiap kali kita memakai `*` dalam kode
kita. Karena penggantian operator `*` itu tidak berulang tanpa henti, kita
akhirnya mendapat data bertipe `i32`, yang cocok dengan `5` pada `assert_eq!` di
Listing 15-9.

<!-- Old headings. Do not remove or links may break. -->

<a id="implicit-deref-coercions-with-functions-and-methods"></a>
<a id="using-deref-coercions-in-functions-and-methods"></a>

### Memakai Deref Coercion dalam Fungsi dan Method

_Deref coercion_ mengubah reference ke tipe yang mengimplementasikan trait
`Deref` menjadi reference ke tipe lain. Misalnya, deref coercion bisa mengubah
`&String` menjadi `&str` karena `String` mengimplementasikan trait `Deref`
sedemikian rupa sehingga mengembalikan `&str`. Deref coercion adalah kemudahan
yang Rust lakukan pada argumen fungsi dan method, dan hanya bekerja pada
tipe-tipe yang mengimplementasikan trait `Deref`. Hal ini terjadi otomatis saat
kita memberikan reference ke nilai dari suatu tipe sebagai argumen kepada fungsi
atau method yang tipenya tidak cocok dengan parameter dalam definisi fungsi atau
method itu. Rangkaian panggilan ke method `deref` mengubah tipe yang kita
berikan menjadi tipe yang dibutuhkan parameter.

Deref coercion ditambahkan ke Rust agar programmer yang menulis panggilan fungsi
dan method tidak perlu menambahkan terlalu banyak reference dan dereference
eksplisit dengan `&` dan `*`. Fitur deref coercion juga membiarkan kita menulis
lebih banyak kode yang bisa bekerja baik dengan reference maupun smart pointer.

Untuk melihat deref coercion beraksi, mari kita pakai tipe `MyBox<T>` yang kita
definisikan di Listing 15-8 beserta implementasi `Deref` yang kita tambahkan di
Listing 15-10. Listing 15-11 menampilkan definisi fungsi yang memiliki parameter
string slice.

<Listing number="15-11" file-name="src/main.rs" caption="Fungsi `hello` yang memiliki parameter `name` bertipe `&str`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-11/src/main.rs:here}}
```

</Listing>

Kita bisa memanggil fungsi `hello` dengan string slice sebagai argumen, misalnya
`hello("Rust");`. Deref coercion memungkinkan kita memanggil `hello` dengan
reference ke nilai bertipe `MyBox<String>`, seperti yang ditampilkan Listing
15-12.

<Listing number="15-12" file-name="src/main.rs" caption="Memanggil `hello` dengan reference ke nilai `MyBox<String>`, yang berhasil karena deref coercion">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-12/src/main.rs:here}}
```

</Listing>

Di sini kita memanggil fungsi `hello` dengan argumen `&m`, yaitu reference ke
nilai `MyBox<String>`. Karena kita mengimplementasikan trait `Deref` pada
`MyBox<T>` di Listing 15-10, Rust bisa mengubah `&MyBox<String>` menjadi
`&String` dengan memanggil `deref`. Pustaka standar menyediakan implementasi
`Deref` pada `String` yang mengembalikan string slice, dan ini ada di dokumentasi
API untuk `Deref`. Rust memanggil `deref` lagi untuk mengubah `&String` menjadi
`&str`, yang cocok dengan definisi fungsi `hello`.

Kalau Rust tidak mengimplementasikan deref coercion, kita harus menulis kode di
Listing 15-13, bukan kode di Listing 15-12, untuk memanggil `hello` dengan nilai
bertipe `&MyBox<String>`.

<Listing number="15-13" file-name="src/main.rs" caption="Kode yang harus kita tulis jika Rust tidak memiliki deref coercion">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-13/src/main.rs:here}}
```

</Listing>

`(*m)` mendereference `MyBox<String>` menjadi `String`. Lalu, `&` dan `[..]`
mengambil string slice dari `String` yang sama dengan keseluruhan string agar
cocok dengan tanda tangan `hello`. Kode tanpa deref coercion ini lebih sulit
dibaca, ditulis, dan dipahami dengan semua simbol itu terlibat. Deref coercion
membiarkan Rust menangani konversi-konversi ini untuk kita secara otomatis.

Saat trait `Deref` didefinisikan untuk tipe-tipe yang terlibat, Rust akan
menganalisis tipe-tipe itu dan memakai `Deref::deref` sebanyak yang diperlukan
untuk mendapatkan reference yang cocok dengan tipe parameter. Jumlah pemanggilan
`Deref::deref` yang perlu disisipkan ditentukan saat kompilasi, jadi tidak ada
penalti runtime saat memanfaatkan deref coercion!

<!-- Old headings. Do not remove or links may break. -->

<a id="how-deref-coercion-interacts-with-mutability"></a>

### Menangani Deref Coercion dengan Reference Mutable

Sama seperti kamu memakai trait `Deref` untuk menimpa operator `*` pada reference
immutable, kamu bisa memakai trait `DerefMut` untuk menimpa operator `*` pada
reference mutable.

Rust melakukan deref coercion saat menemukan tipe dan implementasi trait dalam
tiga kasus:

1. Dari `&T` ke `&U` saat `T: Deref<Target=U>`
2. Dari `&mut T` ke `&mut U` saat `T: DerefMut<Target=U>`
3. Dari `&mut T` ke `&U` saat `T: Deref<Target=U>`

Dua kasus pertama sama, hanya saja kasus kedua melibatkan mutabilitas. Kasus
pertama menyatakan bahwa kalau kamu punya `&T`, dan `T` mengimplementasikan
`Deref` ke suatu tipe `U`, kamu bisa mendapat `&U` secara transparan. Kasus kedua
menyatakan hal yang sama terjadi pada reference mutable.

Kasus ketiga lebih rumit: Rust juga akan mengubah reference mutable menjadi
immutable. Namun sebaliknya _tidak_ mungkin: reference immutable tidak akan
pernah diubah menjadi reference mutable. Karena aturan borrowing, kalau kamu
punya reference mutable, reference mutable itu harus menjadi satu-satunya
reference ke data tersebut (jika tidak, program tidak akan terkompilasi).
Mengubah satu reference mutable menjadi satu reference immutable tidak akan
pernah melanggar aturan borrowing. Mengubah reference immutable menjadi
reference mutable mensyaratkan bahwa reference immutable awal itu adalah
satu-satunya reference immutable ke data tersebut, tetapi aturan borrowing tidak
menjamin hal itu. Oleh karena itu, Rust tidak bisa mengasumsikan bahwa mengubah
reference immutable menjadi reference mutable itu mungkin.

[impl-trait]: ch10-02-traits.html#implementing-a-trait-on-a-type
[tuple-structs]: ch05-01-defining-structs.html#creating-different-types-with-tuple-structs
