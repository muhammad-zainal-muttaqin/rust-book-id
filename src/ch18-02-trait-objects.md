<!-- Old headings. Do not remove or links may break. -->

<a id="using-trait-objects-that-allow-for-values-of-different-types"></a>

<a id="using-trait-objects-to-abstract-over-shared-behavior"></a>
## Menggunakan Trait Object untuk Abstraksi atas Perilaku Bersama

Di Bab 8, kita menyebutkan bahwa salah satu keterbatasan vector adalah hanya bisa menyimpan elemen dari satu tipe. Kita membuat solusi alternatif di Listing 8-9 dengan mendefinisikan enum `SpreadsheetCell` yang memiliki varian untuk menampung bilangan bulat, bilangan desimal, dan teks. Dengan begitu, kita bisa menyimpan berbagai tipe data di setiap sel dan tetap memiliki vector yang mewakili satu baris sel. Ini adalah solusi yang sangat baik ketika item-item yang bisa saling menggantikan merupakan sekumpulan tipe tetap yang sudah kita ketahui saat kode dikompilasi.

Namun, kadang kita ingin pengguna library kita bisa memperluas kumpulan tipe yang valid dalam situasi tertentu. Untuk menunjukkan bagaimana kita bisa mencapainya, kita akan membuat contoh alat antarmuka pengguna grafis (GUI) yang mengiterasi sebuah daftar item, memanggil method `draw` pada masing-masing item untuk menggambarnya ke layar—teknik yang umum dipakai alat GUI. Kita akan membuat library crate bernama `gui` yang berisi kerangka sebuah library GUI. Crate ini mungkin menyertakan beberapa tipe untuk dipakai orang, seperti `Button` atau `TextField`. Selain itu, pengguna `gui` akan ingin membuat tipe mereka sendiri yang bisa digambar: Misalnya, seorang programmer mungkin menambahkan `Image`, dan programmer lain menambahkan `SelectBox`.

Saat menulis library ini, kita tidak bisa mengetahui dan mendefinisikan semua tipe yang mungkin ingin dibuat programmer lain. Namun kita tahu bahwa `gui` perlu melacak banyak nilai dari berbagai tipe, dan perlu memanggil method `draw` pada masing-masing nilai yang berbeda tipe ini. `gui` tidak perlu tahu persis apa yang akan terjadi saat kita memanggil method `draw`, cukup bahwa nilainya memiliki method tersebut untuk bisa kita panggil.

Untuk melakukan ini dalam bahasa yang memiliki pewarisan, kita mungkin mendefinisikan class bernama `Component` yang memiliki method bernama `draw`. Class-class lain, seperti `Button`, `Image`, dan `SelectBox`, akan mewarisi dari `Component` dan dengan demikian mewarisi method `draw`. Masing-masing bisa menimpa method `draw` untuk mendefinisikan perilaku khusus mereka, tetapi framework bisa memperlakukan semua tipe seolah-olah mereka adalah instance `Component` dan memanggil `draw` padanya. Namun karena Rust tidak memiliki pewarisan, kita perlu cara lain untuk menyusun library `gui` agar pengguna bisa membuat tipe baru yang kompatibel dengan library tersebut.

### Mendefinisikan Trait untuk Perilaku Bersama

Untuk menerapkan perilaku yang kita inginkan pada `gui`, kita akan mendefinisikan trait bernama `Draw` yang memiliki satu method bernama `draw`. Lalu, kita bisa mendefinisikan vector yang mengambil trait object. Sebuah _trait object_ menunjuk baik ke instance dari tipe yang mengimplementasikan trait yang kita tentukan maupun ke tabel yang dipakai untuk mencari method trait pada tipe itu saat runtime. Kita membuat trait object dengan menentukan sejenis pointer, seperti reference atau smart pointer `Box<T>`, lalu kata kunci `dyn`, lalu menentukan trait yang relevan. (Kita akan membahas alasan trait object harus memakai pointer dalam [“Tipe Berukuran Dinamis dan Trait `Sized`”][dynamically-sized]<!-- ignore --> di Bab 20.) Kita bisa memakai trait object sebagai pengganti tipe generic atau konkret. Di mana pun kita memakai trait object, sistem tipe Rust akan memastikan saat kompilasi bahwa nilai apa pun yang dipakai dalam konteks itu mengimplementasikan trait dari trait object tersebut. Dengan demikian, kita tidak perlu mengetahui semua kemungkinan tipe saat kompilasi.

Kita sudah menyebutkan bahwa di Rust, kita sengaja tidak menyebut struct dan enum sebagai “objek” agar berbeda dari objek dalam bahasa lain. Pada struct atau enum, data di field struct dan perilaku di blok `impl` terpisah, sedangkan dalam bahasa lain, data dan perilaku yang digabung menjadi satu konsep sering disebut objek. Trait object berbeda dari objek dalam bahasa lain karena kita tidak bisa menambahkan data ke trait object. Trait object tidak seberguna objek dalam bahasa lain secara umum: tujuan khususnya adalah memungkinkan abstraksi atas perilaku yang bersama.

Listing 18-3 menunjukkan cara mendefinisikan trait bernama `Draw` dengan satu method bernama `draw`.

<Listing number="18-3" file-name="src/lib.rs" caption="Definisi trait `Draw`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-03/src/lib.rs}}
```

</Listing>

Sintaks ini harusnya terasa akrab dari pembahasan kita tentang cara mendefinisikan trait di Bab 10. Berikutnya muncul sintaks baru: Listing 18-4 mendefinisikan struct bernama `Screen` yang menyimpan vector bernama `components`. Vector ini bertipe `Box<dyn Draw>`, yaitu sebuah trait object; ia menjadi pengganti untuk tipe apa pun di dalam `Box` yang mengimplementasikan trait `Draw`.

<Listing number="18-4" file-name="src/lib.rs" caption="Definisi struct `Screen` dengan field `components` yang menyimpan vector trait object yang mengimplementasikan trait `Draw`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-04/src/lib.rs:here}}
```

</Listing>

Pada struct `Screen`, kita akan mendefinisikan method bernama `run` yang akan memanggil method `draw` pada setiap `components` miliknya, seperti ditunjukkan di Listing 18-5.

<Listing number="18-5" file-name="src/lib.rs" caption="Method `run` pada `Screen` yang memanggil method `draw` pada setiap komponen">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-05/src/lib.rs:here}}
```

</Listing>

Ini bekerja berbeda dari mendefinisikan struct yang memakai parameter tipe generic dengan trait bound. Sebuah parameter tipe generic hanya bisa diganti dengan satu tipe konkret pada satu waktu, sedangkan trait object memungkinkan beberapa tipe konkret mengisi posisi trait object saat runtime. Misalnya, kita bisa saja mendefinisikan struct `Screen` memakai tipe generic dan trait bound, seperti di Listing 18-6.

<Listing number="18-6" file-name="src/lib.rs" caption="Implementasi alternatif struct `Screen` dan method `run`-nya memakai generic dan trait bound">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-06/src/lib.rs:here}}
```

</Listing>

Ini membatasi kita pada instance `Screen` yang berisi daftar komponen yang semuanya bertipe `Button` atau semuanya bertipe `TextField`. Jika kamu hanya akan punya koleksi yang homogen, memakai generic dan trait bound lebih disukai karena definisinya akan dimonomorfiskan saat kompilasi untuk memakai tipe-tipe konkret tersebut.

Di sisi lain, dengan pendekatan yang memakai trait object, satu instance `Screen` bisa menyimpan `Vec<T>` yang berisi `Box<Button>` sekaligus `Box<TextField>`. Mari kita lihat cara kerjanya, lalu kita akan membahas dampaknya terhadap performa runtime.

### Mengimplementasikan Trait

Sekarang kita akan menambahkan beberapa tipe yang mengimplementasikan trait `Draw`. Kita akan menyediakan tipe `Button`. Sekali lagi, benar-benar mengimplementasikan library GUI berada di luar cakupan buku ini, jadi method `draw` tidak akan punya implementasi yang berguna di dalam tubuhnya. Untuk membayangkan seperti apa implementasinya, struct `Button` mungkin memiliki field untuk `width`, `height`, dan `label`, seperti ditunjukkan di Listing 18-7.

<Listing number="18-7" file-name="src/lib.rs" caption="Struct `Button` yang mengimplementasikan trait `Draw`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-07/src/lib.rs:here}}
```

</Listing>

Field `width`, `height`, dan `label` pada `Button` akan berbeda dari field komponen lain; misalnya, tipe `TextField` mungkin memiliki field-field yang sama plus field `placeholder`. Setiap tipe yang ingin kita gambar di layar akan mengimplementasikan trait `Draw`, tetapi memakai kode berbeda di method `draw` untuk menentukan cara menggambar tipe tertentu itu, seperti yang dilakukan `Button` di sini (tanpa kode GUI yang sebenarnya, seperti sudah disebutkan). Tipe `Button`, misalnya, mungkin memiliki blok `impl` tambahan yang berisi method-method terkait apa yang terjadi saat pengguna mengklik tombol. Method semacam ini tidak akan berlaku bagi tipe seperti `TextField`.

Jika seseorang yang memakai library kita memutuskan untuk mengimplementasikan struct `SelectBox` yang memiliki field `width`, `height`, dan `options`, mereka juga akan mengimplementasikan trait `Draw` pada tipe `SelectBox`, seperti ditunjukkan di Listing 18-8.

<Listing number="18-8" file-name="src/main.rs" caption="Crate lain yang memakai `gui` dan mengimplementasikan trait `Draw` pada struct `SelectBox`">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-08/src/main.rs:here}}
```

</Listing>

Pengguna library kita kini bisa menulis fungsi `main` mereka untuk membuat instance `Screen`. Ke instance `Screen` itu, mereka bisa menambahkan `SelectBox` dan `Button` dengan memasukkan masing-masing ke dalam `Box<T>` agar menjadi trait object. Lalu mereka bisa memanggil method `run` pada instance `Screen`, yang akan memanggil `draw` pada masing-masing komponen. Listing 18-9 menunjukkan implementasi ini.

<Listing number="18-9" file-name="src/main.rs" caption="Memakai trait object untuk menyimpan nilai dari berbagai tipe yang mengimplementasikan trait yang sama">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-09/src/main.rs:here}}
```

</Listing>

Saat menulis library ini, kita tidak tahu bahwa seseorang mungkin akan menambahkan tipe `SelectBox`, tetapi implementasi `Screen` kita mampu beroperasi pada tipe baru itu dan menggambarnya karena `SelectBox` mengimplementasikan trait `Draw`, yang berarti ia mengimplementasikan method `draw`.

Konsep ini—yang hanya peduli pada pesan yang bisa direspons oleh sebuah nilai, bukan pada tipe konkret nilai itu—mirip dengan konsep _duck typing_ dalam bahasa bertipe dinamis: Kalau ia berjalan seperti bebek dan bersuara seperti bebek, pastilah ia bebek! Dalam implementasi `run` pada `Screen` di Listing 18-5, `run` tidak perlu tahu apa tipe konkret masing-masing komponen. Ia tidak memeriksa apakah sebuah komponen adalah instance dari `Button` atau `SelectBox`, ia hanya memanggil method `draw` pada komponen itu. Dengan menentukan `Box<dyn Draw>` sebagai tipe nilai di dalam vector `components`, kita sudah mendefinisikan `Screen` agar membutuhkan nilai yang bisa kita panggil method `draw`-nya.

Keuntungan memakai trait object dan sistem tipe Rust untuk menulis kode yang mirip kode dengan duck typing adalah kita tidak perlu memeriksa apakah sebuah nilai mengimplementasikan method tertentu saat runtime, juga tidak perlu khawatir akan mendapat error jika sebuah nilai tidak mengimplementasikan method tetapi tetap kita panggil. Rust tidak akan mengompilasi kode kita jika nilainya tidak mengimplementasikan trait yang dibutuhkan trait object.

Misalnya, Listing 18-10 menunjukkan apa yang terjadi jika kita mencoba membuat `Screen` dengan `String` sebagai komponen.

<Listing number="18-10" file-name="src/main.rs" caption="Mencoba memakai tipe yang tidak mengimplementasikan trait dari trait object">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-10/src/main.rs}}
```

</Listing>

Kita akan mendapat error ini karena `String` tidak mengimplementasikan trait `Draw`:

```console
{{#include ../listings/ch18-oop/listing-18-10/output.txt}}
```

Error ini memberi tahu kita bahwa entah kita mengirim sesuatu ke `Screen` yang memang tidak ingin kita kirim dan sebaiknya mengirim tipe lain, atau kita sebaiknya mengimplementasikan `Draw` pada `String` agar `Screen` bisa memanggil `draw` padanya.

<!-- Old headings. Do not remove or links may break. -->

<a id="trait-objects-perform-dynamic-dispatch"></a>

### Melakukan Dynamic Dispatch

Ingat pembahasan kita tentang [“Performa Kode yang Memakai Generic”][performance-of-code-using-generics]<!-- ignore --> di Bab 10 mengenai proses monomorfisasi yang dilakukan compiler pada generic: compiler menghasilkan implementasi non-generic dari fungsi dan method untuk setiap tipe konkret yang kita pakai sebagai pengganti parameter tipe generic. Kode yang dihasilkan dari monomorfisasi melakukan _static dispatch_, yaitu ketika compiler mengetahui method mana yang kamu panggil saat kompilasi. Ini berbeda dengan _dynamic dispatch_, yaitu ketika compiler tidak bisa mengetahui saat kompilasi method mana yang dipanggil. Dalam kasus dynamic dispatch, compiler menghasilkan kode yang saat runtime akan mengetahui method mana yang harus dipanggil.

Saat kita memakai trait object, Rust harus memakai dynamic dispatch. Compiler tidak mengetahui semua tipe yang mungkin dipakai dengan kode yang memakai trait object, jadi ia tidak tahu method mana yang diimplementasikan pada tipe mana yang harus dipanggil. Sebaliknya, saat runtime, Rust memakai pointer di dalam trait object untuk mengetahui method mana yang dipanggil. Pencarian ini menimbulkan biaya runtime yang tidak terjadi pada static dispatch. Dynamic dispatch juga mencegah compiler memilih untuk meng-inline kode sebuah method, yang pada gilirannya mencegah beberapa optimasi, dan Rust punya beberapa aturan tentang di mana kamu bisa dan tidak bisa memakai dynamic dispatch, yang disebut _dyn compatibility_. Aturan-aturan itu berada di luar cakupan pembahasan ini, tetapi kamu bisa membacanya lebih lanjut [di reference][dyn-compatibility]<!-- ignore -->. Meski demikian, kita memang mendapat fleksibilitas ekstra pada kode yang kita tulis di Listing 18-5 dan bisa kita dukung di Listing 18-9, jadi ini adalah trade-off yang perlu dipertimbangkan.

[performance-of-code-using-generics]: ch10-01-syntax.html#performance-of-code-using-generics
[dynamically-sized]: ch20-03-advanced-types.html#dynamically-sized-types-and-the-sized-trait
[dyn-compatibility]: https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility
