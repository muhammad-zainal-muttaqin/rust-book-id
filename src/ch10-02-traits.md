<!-- Old headings. Do not remove or links may break. -->

<a id="traits-defining-shared-behavior"></a>

## Mendefinisikan Perilaku Bersama dengan Trait

Sebuah _trait_ mendefinisikan fungsionalitas yang dimiliki suatu tipe dan bisa dibagikan dengan tipe lain. Kita bisa memakai trait untuk mendefinisikan perilaku bersama secara abstrak. Kita bisa memakai _trait bounds_ untuk menentukan bahwa sebuah tipe generic boleh berupa tipe apa pun yang memiliki perilaku tertentu.

> Catatan: Trait mirip dengan fitur yang sering disebut _interfaces_ di bahasa
> lain, meski ada beberapa perbedaan.

### Mendefinisikan Sebuah Trait

Perilaku suatu tipe terdiri dari method-method yang bisa kita panggil pada tipe itu. Tipe-tipe yang berbeda memiliki perilaku yang sama jika kita bisa memanggil method yang sama pada semuanya. Definisi trait adalah cara untuk mengelompokkan signature method guna mendefinisikan sekumpulan perilaku yang diperlukan untuk mencapai suatu tujuan.

Misalnya, katakanlah kita punya beberapa struct yang menyimpan berbagai jenis dan jumlah teks: struct `NewsArticle` yang menyimpan sebuah berita yang dilaporkan dari lokasi tertentu, dan `SocialPost` yang paling banyak berisi 280 karakter beserta metadata yang menunjukkan apakah postingan itu baru, repost, atau balasan untuk postingan lain.

Kita ingin membuat library crate agregator media bernama `aggregator` yang bisa menampilkan ringkasan data yang mungkin tersimpan dalam instance `NewsArticle` atau `SocialPost`. Untuk melakukan itu, kita memerlukan ringkasan dari tiap tipe, dan kita akan memintanya dengan memanggil method `summarize` pada sebuah instance. Listing 10-12 menunjukkan definisi trait `Summary` publik yang menyatakan perilaku ini.

<Listing number="10-12" file-name="src/lib.rs" caption="Trait `Summary` yang terdiri dari perilaku yang disediakan oleh method `summarize`">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-12/src/lib.rs}}
```

</Listing>

Di sini, kita mendeklarasikan trait dengan kata kunci `trait` lalu nama trait-nya, dalam hal ini `Summary`. Kita juga mendeklarasikan trait itu sebagai `pub` agar crate yang bergantung pada crate ini bisa memakai trait itu juga, seperti yang akan kita lihat pada beberapa contoh. Di dalam tanda kurung kurawal, kita mendeklarasikan signature method yang menggambarkan perilaku tipe-tipe yang mengimplementasikan trait ini, yang dalam hal ini adalah `fn summarize(&self) -> String`.

Setelah signature method, alih-alih memberikan implementasi di dalam kurung kurawal, kita memakai titik koma. Tiap tipe yang mengimplementasikan trait ini harus menyediakan perilakunya sendiri untuk isi method tersebut. compiler akan memastikan bahwa tipe apa pun yang memiliki trait `Summary` akan memiliki method `summarize` yang didefinisikan persis dengan signature ini.

Sebuah trait bisa memiliki beberapa method di dalamnya: signature method ditulis satu per baris, dan tiap baris diakhiri titik koma.

<a id="implementing-a-trait-on-a-type"></a>
### Mengimplementasikan Trait pada Sebuah Tipe

Setelah kita mendefinisikan signature yang diinginkan untuk method-method trait `Summary`, kita bisa mengimplementasikannya pada tipe-tipe di agregator media kita. Listing 10-13 menunjukkan implementasi trait `Summary` pada struct `NewsArticle` yang memakai judul, penulis, dan lokasi untuk membuat nilai yang dikembalikan `summarize`. Untuk struct `SocialPost`, kita mendefinisikan `summarize` sebagai nama pengguna diikuti seluruh teks postingan, dengan asumsi isi postingan sudah dibatasi 280 karakter.

<Listing number="10-13" file-name="src/lib.rs" caption="Mengimplementasikan trait `Summary` pada tipe `NewsArticle` dan `SocialPost`">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-13/src/lib.rs:here}}
```

</Listing>

Mengimplementasikan trait pada sebuah tipe mirip dengan mengimplementasikan method biasa. Bedanya, setelah `impl` kita menuliskan nama trait yang ingin kita implementasikan, lalu memakai kata kunci `for`, lalu menentukan nama tipe yang ingin kita beri implementasi trait tersebut. Di dalam blok `impl`, kita menuliskan signature method yang telah didefinisikan dalam definisi trait. Alih-alih menambahkan titik koma setelah tiap signature, kita memakai kurung kurawal dan mengisi isi method dengan perilaku spesifik yang kita inginkan dari method-method trait itu untuk tipe tertentu tersebut.

Setelah library mengimplementasikan trait `Summary` pada `NewsArticle` dan `SocialPost`, pengguna crate bisa memanggil method trait pada instance `NewsArticle` dan `SocialPost` dengan cara yang sama seperti kita memanggil method biasa. Satu-satunya perbedaan adalah pengguna harus membawa trait itu ke dalam scope, selain tipe-tipenya. Berikut contoh bagaimana sebuah binary crate bisa memakai library crate `aggregator` kita:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-01-calling-trait-method/src/main.rs}}
```

Kode ini mencetak `1 new post: horse_ebooks: of course, as you probably already know, people`.

Crate lain yang bergantung pada crate `aggregator` juga bisa membawa trait `Summary` ke dalam scope untuk mengimplementasikan `Summary` pada tipe mereka sendiri. Satu pembatasan yang perlu dicatat: kita bisa mengimplementasikan sebuah trait pada sebuah tipe hanya jika trait-nya, tipe-nya, atau keduanya, lokal terhadap crate kita. Misalnya, kita bisa mengimplementasikan trait library standar seperti `Display` pada tipe buatan sendiri seperti `SocialPost` sebagai bagian dari fungsionalitas crate `aggregator` kita karena tipe `SocialPost` lokal terhadap crate `aggregator` kita. Kita juga bisa mengimplementasikan `Summary` pada `Vec<T>` di crate `aggregator` kita karena trait `Summary` lokal terhadap crate `aggregator` kita.

Tapi kita tidak bisa mengimplementasikan trait eksternal pada tipe eksternal. Misalnya, kita tidak bisa mengimplementasikan trait `Display` pada `Vec<T>` di dalam crate `aggregator` kita, karena `Display` dan `Vec<T>` sama-sama didefinisikan di library standar dan tidak lokal terhadap crate `aggregator` kita. Pembatasan ini bagian dari sifat yang disebut _coherence_, lebih tepatnya _orphan rule_, yang dinamakan demikian karena tipe induknya tidak hadir. Aturan ini memastikan kode orang lain tidak bisa merusak kode kamu, dan sebaliknya. Tanpa aturan itu, dua crate bisa mengimplementasikan trait yang sama untuk tipe yang sama, dan Rust tidak akan tahu implementasi mana yang harus dipakai.

<!-- Old headings. Do not remove or links may break. -->

<a id="default-implementations"></a>

### Memakai Implementasi Default

Kadang berguna untuk memiliki perilaku default untuk sebagian atau semua method dalam sebuah trait, daripada mewajibkan implementasi untuk semua method pada setiap tipe. Dengan begitu, saat kita mengimplementasikan trait pada tipe tertentu, kita bisa mempertahankan atau menimpa perilaku default tiap method.

Pada Listing 10-14, kita menentukan string default untuk method `summarize` dari trait `Summary`, alih-alih hanya mendefinisikan signature method-nya seperti yang kita lakukan pada Listing 10-12.

<Listing number="10-14" file-name="src/lib.rs" caption="Mendefinisikan trait `Summary` dengan implementasi default dari method `summarize`">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-14/src/lib.rs:here}}
```

</Listing>

Untuk memakai implementasi default guna merangkum instance `NewsArticle`, kita menentukan blok `impl` kosong dengan `impl Summary for NewsArticle {}`.

Meski kita tidak lagi mendefinisikan method `summarize` pada `NewsArticle` secara langsung, kita sudah menyediakan implementasi default dan menentukan bahwa `NewsArticle` mengimplementasikan trait `Summary`. Hasilnya, kita tetap bisa memanggil method `summarize` pada instance `NewsArticle`, seperti ini:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-02-calling-default-impl/src/main.rs:here}}
```

Kode ini mencetak `New article available! (Read more...)`.

Membuat implementasi default tidak mengharuskan kita mengubah apa pun pada implementasi `Summary` untuk `SocialPost` di Listing 10-13. Alasannya, sintaks untuk menimpa implementasi default sama dengan sintaks untuk mengimplementasikan method trait yang tidak memiliki implementasi default.

Implementasi default bisa memanggil method lain dalam trait yang sama, meski method-method itu tidak memiliki implementasi default. Dengan cara ini, sebuah trait bisa menyediakan banyak fungsionalitas yang berguna dan hanya meminta implementator menentukan sebagian kecil saja. Misalnya, kita bisa mendefinisikan trait `Summary` dengan method `summarize_author` yang implementasinya wajib, lalu mendefinisikan method `summarize` yang memiliki implementasi default yang memanggil method `summarize_author`:

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:here}}
```

Untuk memakai versi `Summary` ini, kita hanya perlu mendefinisikan `summarize_author` saat mengimplementasikan trait pada sebuah tipe:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:impl}}
```

Setelah kita mendefinisikan `summarize_author`, kita bisa memanggil `summarize` pada instance struct `SocialPost`, dan implementasi default `summarize` akan memanggil definisi `summarize_author` yang sudah kita berikan. Karena kita telah mengimplementasikan `summarize_author`, trait `Summary` memberi kita perilaku method `summarize` tanpa meminta kita menulis kode lagi. Begini tampilannya:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/main.rs:here}}
```

Kode ini mencetak `1 new post: (Read more from @horse_ebooks...)`.

Perlu dicatat bahwa kita tidak bisa memanggil implementasi default dari implementasi yang menimpanya pada method yang sama.

<!-- Old headings. Do not remove or links may break. -->

<a id="traits-as-parameters"></a>

### Memakai Trait sebagai Parameter

Sekarang kamu tahu cara mendefinisikan dan mengimplementasikan trait, kita bisa menjelajahi cara memakai trait untuk mendefinisikan fungsi yang menerima banyak tipe berbeda. Kita akan memakai trait `Summary` yang sudah kita implementasikan pada tipe `NewsArticle` dan `SocialPost` di Listing 10-13 untuk mendefinisikan fungsi `notify` yang memanggil method `summarize` pada parameter `item`-nya, yang berupa tipe tertentu yang mengimplementasikan trait `Summary`. Untuk melakukan ini, kita memakai sintaks `impl Trait`, seperti ini:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-04-traits-as-parameters/src/lib.rs:here}}
```

Alih-alih menentukan tipe konkret untuk parameter `item`, kita menuliskan kata kunci `impl` dan nama trait. Parameter ini menerima tipe apa pun yang mengimplementasikan trait yang ditentukan. Di dalam isi `notify`, kita bisa memanggil method-method pada `item` yang berasal dari trait `Summary`, seperti `summarize`. Kita bisa memanggil `notify` dan memberikan instance `NewsArticle` atau `SocialPost` apa pun. Kode yang memanggil fungsi itu dengan tipe lain, seperti `String` atau `i32`, tidak akan terompilasi, karena tipe-tipe itu tidak mengimplementasikan `Summary`.

<!-- Old headings. Do not remove or links may break. -->

<a id="fixing-the-largest-function-with-trait-bounds"></a>

#### Sintaks Trait Bound

Sintaks `impl Trait` berhasil untuk kasus yang sederhana, tetapi sebenarnya adalah syntax sugar untuk bentuk yang lebih panjang yang disebut _trait bound_; tampilannya seperti ini:

```rust,ignore
pub fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}
```

Bentuk yang lebih panjang ini setara dengan contoh di bagian sebelumnya, tetapi lebih panjang lebar. Kita menaruh trait bound bersama deklarasi parameter tipe generic, setelah titik dua dan di dalam tanda kurung sudut.

Sintaks `impl Trait` praktis dan menghasilkan kode yang lebih ringkas pada kasus sederhana, sementara sintaks trait bound yang lengkap bisa menyuarakan kompleksitas yang lebih tinggi dalam kasus lain. Misalnya, kita bisa memiliki dua parameter yang mengimplementasikan `Summary`. Melakukannya dengan sintaks `impl Trait` tampak seperti ini:

```rust,ignore
pub fn notify(item1: &impl Summary, item2: &impl Summary) {
```

Memakai `impl Trait` tepat jika kita ingin fungsi ini mengizinkan `item1` dan `item2` memiliki tipe yang berbeda (selama keduanya mengimplementasikan `Summary`). Namun, jika kita ingin memaksa kedua parameter memiliki tipe yang sama, kita harus memakai trait bound, seperti ini:

```rust,ignore
pub fn notify<T: Summary>(item1: &T, item2: &T) {
```

Tipe generic `T` yang ditentukan sebagai tipe parameter `item1` dan `item2` membatasi fungsi tersebut sehingga tipe konkret dari nilai yang diberikan sebagai argumen untuk `item1` dan `item2` harus sama.

<!-- Old headings. Do not remove or links may break. -->

<a id="specifying-multiple-trait-bounds-with-the--syntax"></a>

#### Beberapa Trait Bound dengan Sintaks `+`

Kita juga bisa menentukan lebih dari satu trait bound. Katakanlah kita ingin `notify` memakai format tampilan serta `summarize` pada `item`: kita menentukan dalam definisi `notify` bahwa `item` harus mengimplementasikan `Display` dan `Summary`. Kita bisa melakukan itu dengan sintaks `+`:

```rust,ignore
pub fn notify(item: &(impl Summary + Display)) {
```

Sintaks `+` juga berlaku untuk trait bound pada tipe generic:

```rust,ignore
pub fn notify<T: Summary + Display>(item: &T) {
```

Dengan kedua trait bound ditentukan, isi `notify` bisa memanggil `summarize` dan memakai `{}` untuk memformat `item`.

#### Trait Bound yang Lebih Jelas dengan Klausa `where`

Memakai terlalu banyak trait bound ada kerugiannya. Tiap generic memiliki trait bound-nya sendiri, sehingga fungsi dengan beberapa parameter tipe generic bisa memuat banyak informasi trait bound di antara nama fungsi dan daftar parameternya, membuat signature fungsi sulit dibaca. Karena itu, Rust menyediakan sintaks alternatif untuk menentukan trait bound di dalam klausa `where` setelah signature fungsi. Jadi, alih-alih menulis ini:

```rust,ignore
fn some_function<T: Display + Clone, U: Clone + Debug>(t: &T, u: &U) -> i32 {
```

kita bisa memakai klausa `where`, seperti ini:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-07-where-clause/src/lib.rs:here}}
```

Signature fungsi ini lebih rapi: nama fungsi, daftar parameter, dan tipe kembalian berdekatan, seperti fungsi yang tidak memiliki banyak trait bound.

### Mengembalikan Tipe yang Mengimplementasikan Trait

Kita juga bisa memakai sintaks `impl Trait` pada posisi kembalian untuk mengembalikan nilai dari tipe tertentu yang mengimplementasikan sebuah trait, seperti yang ditunjukkan di sini:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-05-returning-impl-trait/src/lib.rs:here}}
```

Dengan memakai `impl Summary` sebagai tipe kembalian, kita menentukan bahwa fungsi `returns_summarizable` mengembalikan tipe tertentu yang mengimplementasikan trait `Summary` tanpa menyebut tipe konkretnya. Dalam hal ini, `returns_summarizable` mengembalikan `SocialPost`, tetapi kode yang memanggil fungsi ini tidak perlu mengetahui hal itu.

Kemampuan untuk menentukan tipe kembalian hanya berdasarkan trait yang diimplementasikannya sangat berguna dalam konteks closure dan iterator, yang akan kita bahas di Bab 13. Closure dan iterator menciptakan tipe yang hanya diketahui compiler atau tipe yang sangat panjang untuk dituliskan. Sintaks `impl Trait` memungkinkan kamu menentukan secara ringkas bahwa sebuah fungsi mengembalikan tipe tertentu yang mengimplementasikan trait `Iterator` tanpa perlu menuliskan tipe yang sangat panjang.

Namun, kamu hanya bisa memakai `impl Trait` jika mengembalikan satu tipe tunggal. Misalnya, kode ini yang mengembalikan `NewsArticle` atau `SocialPost` dengan tipe kembalian ditentukan sebagai `impl Summary` tidak akan berhasil:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-06-impl-trait-returns-one-type/src/lib.rs:here}}
```

Mengembalikan `NewsArticle` atau `SocialPost` tidak diperbolehkan karena pembatasan pada cara sintaks `impl Trait` diimplementasikan di compiler. Kita akan membahas cara menulis fungsi dengan perilaku seperti itu di bagian ["Memakai Trait Object untuk Mengabstraksi Perilaku Bersama"][trait-objects]<!-- ignore --> Bab 18.

### Memakai Trait Bound untuk Mengimplementasikan Method secara Bersyarat

Dengan memakai trait bound pada blok `impl` yang memakai parameter tipe generic, kita bisa mengimplementasikan method secara bersyarat untuk tipe-tipe yang mengimplementasikan trait yang ditentukan. Misalnya, tipe `Pair<T>` di Listing 10-15 selalu mengimplementasikan fungsi `new` untuk mengembalikan instance baru dari `Pair<T>` (ingat dari bagian ["Sintaks Method"][methods]<!-- ignore --> Bab 5 bahwa `Self` adalah alias untuk tipe dari blok `impl`, dalam hal ini `Pair<T>`). Namun pada blok `impl` berikutnya, `Pair<T>` hanya mengimplementasikan method `cmp_display` jika tipe dalamnya `T` mengimplementasikan trait `PartialOrd` yang memungkinkan perbandingan _dan_ trait `Display` yang memungkinkan pencetakan.

<Listing number="10-15" file-name="src/lib.rs" caption="Mengimplementasikan method secara bersyarat pada tipe generic bergantung pada trait bound">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-15/src/lib.rs}}
```

</Listing>

Kita juga bisa mengimplementasikan sebuah trait secara bersyarat untuk tipe apa pun yang mengimplementasikan trait lain. Implementasi sebuah trait pada tipe apa pun yang memenuhi trait bound disebut _blanket implementations_ dan digunakan secara luas di library standar Rust. Misalnya, library standar mengimplementasikan trait `ToString` pada tipe apa pun yang mengimplementasikan trait `Display`. Blok `impl` di library standar tampak mirip dengan kode ini:

```rust,ignore
impl<T: Display> ToString for T {
    // --snip--
}
```

Karena library standar memiliki blanket implementation ini, kita bisa memanggil method `to_string` yang didefinisikan oleh trait `ToString` pada tipe apa pun yang mengimplementasikan trait `Display`. Misalnya, kita bisa mengubah bilangan bulat menjadi nilai `String` yang bersesuaian seperti ini karena bilangan bulat mengimplementasikan `Display`:

```rust
let s = 3.to_string();
```

Blanket implementation muncul dalam dokumentasi trait pada bagian "Implementors".

Trait dan trait bound memungkinkan kita menulis kode yang memakai parameter tipe generic untuk mengurangi duplikasi, sekaligus memberi tahu compiler bahwa kita ingin tipe generic itu memiliki perilaku tertentu. compiler lalu bisa memakai informasi trait bound untuk memeriksa bahwa semua tipe konkret yang dipakai dengan kode kita menyediakan perilaku yang benar. Pada bahasa dengan pengetikan dinamis, kita akan mendapat error saat runtime jika memanggil method pada tipe yang tidak mendefinisikan method itu. Tetapi Rust memindahkan error-error ini ke waktu kompilasi sehingga kita dipaksa memperbaiki masalahnya sebelum kode kita sempat berjalan. Selain itu, kita tidak perlu menulis kode yang memeriksa perilaku saat runtime, karena kita sudah memeriksanya saat kompilasi. Dengan begitu, performanya meningkat tanpa harus mengorbankan fleksibilitas generic.

[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[methods]: ch05-03-method-syntax.html#method-syntax
