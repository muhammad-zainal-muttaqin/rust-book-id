<!-- Old headings. Do not remove or links may break. -->

<a id="closures-anonymous-functions-that-can-capture-their-environment"></a>
<a id="closures-anonymous-functions-that-capture-their-environment"></a>

## Closures

Closure di Rust adalah fungsi anonim yang bisa kamu simpan dalam variabel atau teruskan sebagai argumen ke fungsi lain. Kamu bisa membuat closure di satu tempat, lalu memanggilnya di tempat lain untuk mengevaluasinya dalam konteks yang berbeda. Berbeda dengan fungsi, closure bisa menangkap nilai dari scope tempat ia didefinisikan. Kita akan menunjukkan bagaimana fitur-fitur closure ini memungkinkan penggunaan kembali kode dan penyesuaian perilaku.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-an-abstraction-of-behavior-with-closures"></a>
<a id="refactoring-using-functions"></a>
<a id="refactoring-with-closures-to-store-code"></a>
<a id="capturing-the-environment-with-closures"></a>

### Menangkap Lingkungan

Pertama, kita akan melihat bagaimana closure bisa menangkap nilai dari lingkungan tempat ia didefinisikan untuk digunakan nanti. Berikut skenarionya: Sesekali, perusahaan kaos kita memberikan kaos edisi terbatas dan eksklusif kepada seseorang di daftar mailing kita sebagai promosi. Orang-orang di daftar mailing bisa secara opsional menambahkan warna favorit mereka ke profil. Jika orang yang terpilih mendapat kaos gratis sudah menentukan warna favoritnya, ia mendapat kaos dengan warna itu. Jika orang tersebut belum menentukan warna favorit, ia mendapat kaos warna apa pun yang saat ini paling banyak dimiliki perusahaan.

Ada banyak cara untuk menerapkan ini. Untuk contoh ini, kita akan memakai enum bernama `ShirtColor` yang memiliki varian `Red` dan `Blue` (kita batasi jumlah warnanya agar sederhana). Kita merepresentasikan inventaris perusahaan dengan struct `Inventory` yang memiliki field bernama `shirts` berisi `Vec<ShirtColor>` yang mewakili warna kaos yang saat ini tersedia. Metode `giveaway` yang didefinisikan pada `Inventory` menerima preferensi warna kaos opsional dari pemenang kaos gratis, lalu mengembalikan warna kaos yang akan diterima orang tersebut. Susunan ini ditunjukkan pada Listing 13-1.

<Listing number="13-1" file-name="src/main.rs" caption="Situasi giveaway perusahaan kaos">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-01/src/main.rs}}
```

</Listing>

`store` yang didefinisikan di `main` masih memiliki dua kaos biru dan satu kaos merah yang belum dibagikan untuk promosi edisi terbatas ini. Kita memanggil metode `giveaway` untuk pengguna yang menyukai kaos merah dan pengguna yang tidak punya preferensi apa pun.

Sekali lagi, kode ini bisa diterapkan dengan banyak cara, dan di sini, agar fokus tetap pada closure, kita memakai konsep-konsep yang sudah kamu pelajari, kecuali isi metode `giveaway` yang memakai closure. Di metode `giveaway`, kita menerima preferensi pengguna sebagai parameter bertipe `Option<ShirtColor>` dan memanggil metode `unwrap_or_else` pada `user_preference`. [Metode `unwrap_or_else` pada `Option<T>`][unwrap-or-else]<!-- ignore --> didefinisikan oleh pustaka standar. Metode ini menerima satu argumen: sebuah closure tanpa argumen apa pun yang mengembalikan nilai `T` (tipe yang sama seperti yang disimpan di varian `Some` dari `Option<T>`, dalam kasus ini `ShirtColor`). Jika `Option<T>` adalah varian `Some`, `unwrap_or_else` mengembalikan nilai di dalam `Some` tersebut. Jika `Option<T>` adalah varian `None`, `unwrap_or_else` memanggil closure dan mengembalikan nilai yang dikembalikan closure itu.

Kita menentukan ekspresi closure `|| self.most_stocked()` sebagai argumen untuk `unwrap_or_else`. Ini adalah closure yang tidak menerima parameter (jika closure itu memiliki parameter, parameternya akan muncul di antara dua tanda pipa vertikal). Isi closure memanggil `self.most_stocked()`. Kita mendefinisikan closure di sini, dan implementasi `unwrap_or_else` akan mengevaluasi closure itu nanti jika hasilnya dibutuhkan.

Menjalankan kode ini mencetak hal berikut:

```console
{{#include ../listings/ch13-functional-features/listing-13-01/output.txt}}
```

Satu hal menarik di sini adalah kita telah meneruskan closure yang memanggil `self.most_stocked()` pada instance `Inventory` saat ini. Pustaka standar tidak perlu tahu apa pun tentang tipe `Inventory` atau `ShirtColor` yang kita definisikan, maupun logika yang ingin kita pakai dalam skenario ini. Closure menangkap reference immutable ke instance `Inventory` pada `self`, lalu meneruskannya beserta kode yang kita tentukan ke metode `unwrap_or_else`. Fungsi, di sisi lain, tidak bisa menangkap lingkungannya dengan cara seperti ini.

<!-- Old headings. Do not remove or links may break. -->

<a id="closure-type-inference-and-annotation"></a>

### Menyimpulkan dan Menganotasi Tipe Closure

Ada lebih banyak perbedaan antara fungsi dan closure. Closure biasanya tidak mengharuskan kamu menganotasi tipe parameter atau nilai pengembalian seperti yang dilakukan fungsi `fn`. Anotasi tipe diperlukan pada fungsi karena tipe merupakan bagian dari antarmuka eksplisit yang diekspos kepada pengguna. Mendefinisikan antarmuka ini dengan ketat penting untuk memastikan semua orang sepakat tentang tipe nilai apa yang dipakai dan dikembalikan suatu fungsi. Closure, sebaliknya, tidak dipakai dalam antarmuka yang terekspos seperti itu: closure disimpan dalam variabel, dan dipakai tanpa perlu diberi nama atau diekspos kepada pengguna library kita.

Closure biasanya pendek dan hanya relevan dalam konteks yang sempit, bukan dalam skenario sembarangan. Dalam konteks yang terbatas ini, compiler bisa menyimpulkan tipe parameter dan tipe pengembalian, mirip dengan cara ia menyimpulkan tipe sebagian besar variabel (ada kasus langka di mana compiler juga membutuhkan anotasi tipe closure).

Sama seperti variabel, kita bisa menambahkan anotasi tipe jika ingin lebih eksplisit dan jelas, meski harus lebih panjang dari yang benar-benar diperlukan. Menganotasi tipe untuk closure akan terlihat seperti definisi pada Listing 13-2. Pada contoh ini, kita mendefinisikan closure dan menyimpannya dalam variabel, alih-alih mendefinisikan closure tepat di tempat kita meneruskannya sebagai argumen seperti yang kita lakukan di Listing 13-1.

<Listing number="13-2" file-name="src/main.rs" caption="Menambahkan anotasi tipe opsional untuk parameter dan nilai pengembalian pada closure">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-02/src/main.rs:here}}
```

</Listing>

Dengan anotasi tipe ditambahkan, sintaks closure tampak lebih mirip sintaks fungsi. Di sini, kita mendefinisikan fungsi yang menambahkan 1 pada parameternya dan closure yang perilakunya sama, sebagai perbandingan. Kita menambahkan beberapa spasi agar bagian-bagian yang relevan sejajar. Ini mengilustrasikan bahwa sintaks closure mirip sintaks fungsi, kecuali penggunaan pipa dan jumlah sintaks yang bersifat opsional:

```rust,ignore
fn  add_one_v1   (x: u32) -> u32 { x + 1 }
let add_one_v2 = |x: u32| -> u32 { x + 1 };
let add_one_v3 = |x|             { x + 1 };
let add_one_v4 = |x|               x + 1  ;
```

Baris pertama menunjukkan definisi fungsi dan baris kedua menunjukkan definisi closure yang dianotasi lengkap. Pada baris ketiga, kita menghapus anotasi tipe dari definisi closure. Pada baris keempat, kita menghapus kurung kurawal, yang bersifat opsional karena isi closure hanya memiliki satu ekspresi. Semua ini adalah definisi yang valid dan akan menghasilkan perilaku yang sama saat dipanggil. Baris `add_one_v3` dan `add_one_v4` mengharuskan closure dievaluasi agar bisa dikompilasi, karena tipenya akan disimpulkan dari cara penggunaannya. Ini mirip dengan `let v = Vec::new();` yang membutuhkan anotasi tipe atau nilai dari suatu tipe untuk dimasukkan ke dalam `Vec` agar Rust bisa menyimpulkan tipenya.

Untuk definisi closure, compiler akan menyimpulkan satu tipe konkret untuk setiap parameter dan untuk nilai pengembaliannya. Misalnya, Listing 13-3 menunjukkan definisi closure pendek yang hanya mengembalikan nilai yang diterimanya sebagai parameter. Closure ini tidak terlalu berguna kecuali untuk keperluan contoh ini. Perhatikan bahwa kita tidak menambahkan anotasi tipe apa pun pada definisinya. Karena tidak ada anotasi tipe, kita bisa memanggil closure dengan tipe apa pun, yang dalam hal ini kita lakukan dengan `String` pada pemanggilan pertama. Jika kita lalu mencoba memanggil `example_closure` dengan bilangan bulat, kita akan mendapat error.

<Listing number="13-3" file-name="src/main.rs" caption="Mencoba memanggil closure yang tipenya disimpulkan dengan dua tipe berbeda">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-03/src/main.rs:here}}
```

</Listing>

Compiler memberi kita error ini:

```console
{{#include ../listings/ch13-functional-features/listing-13-03/output.txt}}
```

Pertama kali kita memanggil `example_closure` dengan nilai `String`, compiler menyimpulkan tipe `x` dan tipe pengembalian closure adalah `String`. Tipe-tipe itu lalu terkunci pada closure di `example_closure`, dan kita mendapat error tipe saat mencoba memakai tipe lain dengan closure yang sama.

<a id="capturing-references-or-moving-ownership"></a>
### Menangkap Reference atau Memindahkan Ownership

Closure bisa menangkap nilai dari lingkungannya dengan tiga cara, yang secara langsung sesuai dengan tiga cara fungsi menerima parameter: borrowing immutable, borrowing mutable, atau mengambil *ownership*. Closure akan memutuskan mana yang dipakai berdasarkan apa yang dilakukan isi fungsi terhadap nilai yang ditangkap.

Pada Listing 13-4, kita mendefinisikan closure yang menangkap reference immutable ke vector bernama `list`, karena ia hanya butuh reference immutable untuk mencetak nilainya.

<Listing number="13-4" file-name="src/main.rs" caption="Mendefinisikan dan memanggil closure yang menangkap reference immutable">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-04/src/main.rs}}
```

</Listing>

Contoh ini juga menunjukkan bahwa sebuah variabel bisa terikat pada definisi closure, dan kita bisa memanggil closure itu belakangan dengan memakai nama variabel dan tanda kurung seolah-olah nama variabel itu adalah nama fungsi.

Karena kita bisa memiliki beberapa reference immutable ke `list` secara bersamaan, `list` tetap bisa diakses dari kode sebelum definisi closure, setelah definisi closure tetapi sebelum closure dipanggil, dan setelah closure dipanggil. Kode ini dikompilasi, dijalankan, dan mencetak:

```console
{{#include ../listings/ch13-functional-features/listing-13-04/output.txt}}
```

Berikutnya, pada Listing 13-5, kita mengubah isi closure agar menambahkan elemen ke vector `list`. Sekarang closure menangkap reference mutable.

<Listing number="13-5" file-name="src/main.rs" caption="Mendefinisikan dan memanggil closure yang menangkap reference mutable">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-05/src/main.rs}}
```

</Listing>

Kode ini dikompilasi, dijalankan, dan mencetak:

```console
{{#include ../listings/ch13-functional-features/listing-13-05/output.txt}}
```

Perhatikan bahwa tidak ada lagi `println!` di antara definisi dan pemanggilan closure `borrows_mutably`: Saat `borrows_mutably` didefinisikan, ia menangkap reference mutable ke `list`. Kita tidak memakai closure itu lagi setelah dipanggil, sehingga borrowing mutable berakhir. Di antara definisi closure dan pemanggilan closure, borrowing immutable untuk mencetak tidak diperbolehkan, karena borrowing lain tidak diizinkan saat ada borrowing mutable. Coba tambahkan `println!` di sana untuk melihat pesan error apa yang kamu dapatkan!

Jika kamu ingin memaksa closure mengambil ownership atas nilai-nilai yang digunakannya dari lingkungan, meskipun isi closure itu sebenarnya tidak benar-benar membutuhkan ownership, kamu bisa memakai kata kunci `move` sebelum daftar parameter.

Teknik ini paling berguna saat meneruskan closure ke thread baru untuk memindahkan data sehingga dimiliki oleh thread baru itu. Kita akan membahas thread dan alasan memakainya secara rinci di Bab 16 saat berbicara tentang konkurensi, tetapi untuk sekarang, mari kita lihat secara singkat cara memunculkan thread baru memakai closure yang membutuhkan kata kunci `move`. Listing 13-6 menunjukkan Listing 13-4 yang diubah untuk mencetak vector di thread baru, bukan di thread utama.

<Listing number="13-6" file-name="src/main.rs" caption="Memakai `move` untuk memaksa closure bagi thread mengambil ownership atas `list`">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-06/src/main.rs}}
```

</Listing>

Kita memunculkan thread baru dengan memberikan closure untuk dijalankan sebagai argumen. Isi closure mencetak daftar tersebut. Di Listing 13-4, closure hanya menangkap `list` memakai reference immutable karena itu adalah akses paling sedikit ke `list` yang dibutuhkan untuk mencetaknya. Pada contoh ini, meskipun isi closure masih hanya membutuhkan reference immutable, kita perlu menentukan bahwa `list` harus dipindahkan ke dalam closure dengan menaruh kata kunci `move` di awal definisi closure. Jika thread utama melakukan lebih banyak operasi sebelum memanggil `join` pada thread baru, thread baru bisa selesai sebelum sisa thread utama selesai, atau thread utama bisa selesai lebih dulu. Jika thread utama tetap menyimpan ownership atas `list` tetapi berakhir lebih dulu daripada thread baru dan menghapus `list`, reference immutable di thread itu akan menjadi tidak valid. Karena itu, compiler mengharuskan `list` dipindahkan ke dalam closure yang diberikan ke thread baru agar reference tetap valid. Coba hapus kata kunci `move` atau pakai `list` di thread utama setelah closure didefinisikan untuk melihat error compiler apa yang kamu dapatkan!

<!-- Old headings. Do not remove or links may break. -->

<a id="storing-closures-using-generic-parameters-and-the-fn-traits"></a>
<a id="limitations-of-the-cacher-implementation"></a>
<a id="moving-captured-values-out-of-the-closure-and-the-fn-traits"></a>
<a id="moving-captured-values-out-of-closures-and-the-fn-traits"></a>

<a id="moving-captured-values-out-of-closures"></a>
### Memindahkan Nilai yang Ditangkap Keluar dari Closure

Setelah closure menangkap reference atau ownership atas nilai dari lingkungan tempat ia didefinisikan (sehingga memengaruhi apa, jika ada, yang dipindahkan _ke dalam_ closure), kode di dalam isi closure menentukan apa yang terjadi pada reference atau nilai tersebut saat closure dievaluasi nanti (sehingga memengaruhi apa, jika ada, yang dipindahkan _keluar dari_ closure).

Sebuah isi closure bisa melakukan salah satu dari hal-hal berikut: memindahkan nilai yang ditangkap ke luar closure, mengubah nilai yang ditangkap, tidak memindahkan maupun mengubah nilai itu, atau tidak menangkap apa pun dari lingkungan sejak awal.

Cara closure menangkap dan mengelola nilai dari lingkungan memengaruhi trait mana yang diimplementasikan closure, dan trait adalah cara fungsi serta struct menentukan jenis closure apa yang bisa mereka pakai. Closure akan secara otomatis mengimplementasikan satu, dua, atau ketiga `Fn` trait ini, secara aditif, tergantung bagaimana isi closure mengelola nilai tersebut:

* `FnOnce` berlaku untuk closure yang bisa dipanggil sekali. Semua closure mengimplementasikan setidaknya trait ini karena semua closure bisa dipanggil. Closure yang memindahkan nilai yang ditangkap keluar dari isinya hanya akan mengimplementasikan `FnOnce` dan tidak satu pun `Fn` trait lainnya, karena ia hanya bisa dipanggil sekali.
* `FnMut` berlaku untuk closure yang tidak memindahkan nilai yang ditangkap keluar dari isinya, tetapi mungkin mengubah nilai yang ditangkap itu. Closure seperti ini bisa dipanggil lebih dari sekali.
* `Fn` berlaku untuk closure yang tidak memindahkan nilai yang ditangkap keluar dari isinya dan tidak mengubah nilai yang ditangkap, juga closure yang tidak menangkap apa pun dari lingkungannya. Closure ini bisa dipanggil lebih dari sekali tanpa mengubah lingkungannya, yang penting dalam kasus seperti memanggil closure beberapa kali secara konkuren.

Mari kita lihat definisi metode `unwrap_or_else` pada `Option<T>` yang kita pakai di Listing 13-1:

```rust,ignore
impl<T> Option<T> {
    pub fn unwrap_or_else<F>(self, f: F) -> T
    where
        F: FnOnce() -> T
    {
        match self {
            Some(x) => x,
            None => f(),
        }
    }
}
```

Ingat bahwa `T` adalah tipe generic yang mewakili tipe nilai di varian `Some` dari sebuah `Option`. Tipe `T` itu juga merupakan tipe pengembalian fungsi `unwrap_or_else`: Kode yang memanggil `unwrap_or_else` pada `Option<String>`, misalnya, akan mendapat sebuah `String`.

Berikutnya, perhatikan bahwa fungsi `unwrap_or_else` memiliki parameter tipe generic tambahan `F`. Tipe `F` adalah tipe dari parameter bernama `f`, yaitu closure yang kita berikan saat memanggil `unwrap_or_else`.

Trait bound yang ditentukan pada tipe generic `F` adalah `FnOnce() -> T`, yang berarti `F` harus bisa dipanggil sekali, tidak menerima argumen, dan mengembalikan sebuah `T`. Memakai `FnOnce` dalam trait bound menyatakan batasan bahwa `unwrap_or_else` tidak akan memanggil `f` lebih dari sekali. Di dalam isi `unwrap_or_else`, kita bisa melihat bahwa jika `Option` adalah `Some`, `f` tidak akan dipanggil. Jika `Option` adalah `None`, `f` akan dipanggil sekali. Karena semua closure mengimplementasikan `FnOnce`, `unwrap_or_else` menerima ketiga jenis closure dan sefleksibel mungkin.

> Catatan: Jika apa yang ingin kita lakukan tidak memerlukan penangkapan nilai dari lingkungan, kita bisa memakai nama fungsi alih-alih closure di tempat yang membutuhkan sesuatu yang mengimplementasikan salah satu `Fn` trait. Misalnya, pada nilai `Option<Vec<T>>`, kita bisa memanggil `unwrap_or_else(Vec::new)` untuk mendapat vector baru yang kosong jika nilainya adalah `None`. Compiler secara otomatis mengimplementasikan `Fn` trait mana pun yang sesuai untuk definisi fungsi.

Sekarang mari kita lihat metode pustaka standar `sort_by_key`, yang didefinisikan pada slice, untuk melihat bagaimana metode itu berbeda dari `unwrap_or_else` dan mengapa `sort_by_key` memakai `FnMut`, bukan `FnOnce`, sebagai trait bound. Closure menerima satu argumen berupa reference ke item saat ini dalam slice yang sedang dipertimbangkan, lalu mengembalikan nilai bertipe `K` yang bisa diurutkan. Fungsi ini berguna saat kamu ingin mengurutkan slice berdasarkan atribut tertentu dari setiap item. Di Listing 13-7, kita punya daftar instance `Rectangle`, dan kita memakai `sort_by_key` untuk mengurutkannya berdasarkan atribut `width` dari yang terendah ke tertinggi.

<Listing number="13-7" file-name="src/main.rs" caption="Memakai `sort_by_key` untuk mengurutkan persegi panjang berdasarkan lebar">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-07/src/main.rs}}
```

</Listing>

Kode ini mencetak:

```console
{{#include ../listings/ch13-functional-features/listing-13-07/output.txt}}
```

Alasan `sort_by_key` didefinisikan untuk menerima closure `FnMut` adalah karena ia memanggil closure itu berkali-kali: sekali untuk setiap item dalam slice. Closure `|r| r.width` tidak menangkap, mengubah, atau memindahkan apa pun dari lingkungannya, sehingga memenuhi persyaratan trait bound.

Sebaliknya, Listing 13-8 menunjukkan contoh closure yang hanya mengimplementasikan trait `FnOnce`, karena ia memindahkan sebuah nilai keluar dari lingkungan. Compiler tidak akan mengizinkan kita memakai closure ini dengan `sort_by_key`.

<Listing number="13-8" file-name="src/main.rs" caption="Mencoba memakai closure `FnOnce` dengan `sort_by_key`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-08/src/main.rs}}
```

</Listing>

Ini adalah cara yang dibuat-buat dan berbelit (yang tidak berhasil) untuk mencoba menghitung berapa kali `sort_by_key` memanggil closure saat mengurutkan `list`. Kode ini mencoba melakukan penghitungan itu dengan mendorong `value`—sebuah `String` dari lingkungan closure—ke dalam vector `sort_operations`. Closure menangkap `value`, lalu memindahkan `value` keluar dari closure dengan mentransfer ownership `value` ke vector `sort_operations`. Closure ini bisa dipanggil sekali; mencoba memanggilnya kedua kalinya tidak akan berhasil, karena `value` tidak lagi ada di lingkungan untuk didorong ke `sort_operations` lagi! Karena itu, closure ini hanya mengimplementasikan `FnOnce`. Saat kita mencoba mengompilasi kode ini, kita mendapat error bahwa `value` tidak bisa dipindahkan keluar dari closure karena closure harus mengimplementasikan `FnMut`:

```console
{{#include ../listings/ch13-functional-features/listing-13-08/output.txt}}
```

Error itu menunjuk ke baris dalam isi closure yang memindahkan `value` keluar dari lingkungan. Untuk memperbaikinya, kita perlu mengubah isi closure agar tidak memindahkan nilai keluar dari lingkungan. Menyimpan penghitung di lingkungan dan menambah nilainya di dalam isi closure adalah cara yang lebih lugas untuk menghitung berapa kali closure dipanggil. Closure di Listing 13-9 bekerja dengan `sort_by_key` karena hanya menangkap reference mutable ke penghitung `num_sort_operations`, sehingga bisa dipanggil lebih dari sekali.

<Listing number="13-9" file-name="src/main.rs" caption="Memakai closure `FnMut` dengan `sort_by_key` diperbolehkan.">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-09/src/main.rs}}
```

</Listing>

`Fn` trait penting saat mendefinisikan atau memakai fungsi atau tipe yang memanfaatkan closure. Di bagian berikutnya, kita akan membahas iterator. Banyak metode iterator menerima argumen closure, jadi ingat detail-detail closure ini saat kita lanjut!

[unwrap-or-else]: ../std/option/enum.Option.html#method.unwrap_or_else
