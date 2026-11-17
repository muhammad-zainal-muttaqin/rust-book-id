<a id="methods"></a>
## Method

Method mirip dengan fungsi: kita mendeklarasikannya dengan keyword `fn` beserta sebuah nama, method bisa punya parameter dan nilai balikan, dan di dalamnya ada kode yang dijalankan ketika method dipanggil dari tempat lain. Bedanya, method didefinisikan di dalam konteks sebuah struct (atau enum atau trait object, yang bahas masing-masing di [Bab 6][enums]<!-- ignore --> dan [Bab 18][trait-objects]<!-- ignore -->), dan parameter pertamanya selalu `self`, yang merepresentasikan instance struct tempat method itu dipanggil.

<!-- Old headings. Do not remove or links may break. -->

<a id="defining-methods"></a>

<a id="method-syntax"></a>
### Sintaks Method

Mari kita ubah fungsi `area` yang menerima sebuah instance `Rectangle` sebagai parameter, menjadi sebuah method `area` yang didefinisikan pada struct `Rectangle`, seperti pada Listing 5-13.

<Listing number="5-13" file-name="src/main.rs" caption="Mendefinisikan method `area` pada struct `Rectangle`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-13/src/main.rs}}
```

</Listing>

Untuk mendefinisikan fungsi itu di dalam konteks `Rectangle`, kita mulai sebuah blok `impl` (implementation) untuk `Rectangle`. Semua isi blok `impl` ini akan diasosiasikan dengan tipe `Rectangle`. Lalu, kita pindahkan fungsi `area` ke dalam kurung kurawal `impl` dan mengubah parameter pertama (yang dalam kasus ini satu-satunya) menjadi `self` baik pada signature maupun di seluruh isi body. Di `main`, yang tadinya memanggil fungsi `area` dengan `rect1` sebagai argumen, kita bisa memakai _method syntax_ untuk memanggil method `area` pada instance `Rectangle` kita. Method syntax diletakkan setelah sebuah instance: kita tambahkan titik, lalu nama method, tanda kurung, dan argumen apa pun.

Pada signature `area`, kita memakai `&self` alih-alih `rectangle: &Rectangle`. `&self` sebenarnya adalah bentuk singkat dari `self: &Self`. Di dalam sebuah blok `impl`, tipe `Self` adalah alias untuk tipe yang menjadi isi blok `impl` tersebut. Method harus punya parameter bernama `self` bertipe `Self` sebagai parameter pertamanya, jadi Rust mengizinkan kamu menyingkatnya hanya dengan nama `self` di posisi parameter pertama. Perhatikan bahwa kita tetap perlu menulis `&` di depan bentuk singkat `self` untuk menunjukkan bahwa method ini meminjam instance `Self`, persis seperti yang kita lakukan pada `rectangle: &Rectangle`. Method bisa mengambil ownership atas `self`, meminjam `self` secara immutable seperti yang kita lakukan di sini, atau meminjam `self` secara mutable—sama seperti yang bisa dilakukan pada parameter lain.

Kita memilih `&self` di sini dengan alasan yang sama seperti kita memakai `&Rectangle` pada versi fungsinya: kita tidak ingin mengambil ownership, dan kita hanya ingin membaca data di dalam struct, bukan menulisnya. Kalau kita ingin mengubah instance yang dipanggil method tersebut sebagai bagian dari kerja method-nya, kita akan memakai `&mut self` sebagai parameter pertama. Method yang mengambil ownership atas instance dengan menulis `self` saja sebagai parameter pertama sangat jarang; teknik ini biasanya dipakai ketika method mengubah `self` menjadi sesuatu yang lain dan kamu ingin mencegah pemanggil memakai instance asli setelah transformasi itu.

Alasan utama memakai method alih-alih fungsi, selain tersedianya method syntax dan tidak perlu mengulang tipe `self` di signature setiap method, adalah masalah organisasi. Kita menaruh semua hal yang bisa dilakukan pada sebuah instance tipe dalam satu blok `impl`, alih-alih membuat pengguna kode kita di masa depan mencari kemampuan `Rectangle` di berbagai tempat dalam library yang kita sediakan.

Perhatikan bahwa kita boleh memberi sebuah method nama yang sama dengan salah satu field struct. Sebagai contoh, kita bisa mendefinisikan sebuah method pada `Rectangle` yang juga bernama `width`:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-06-method-field-interaction/src/main.rs:here}}
```

</Listing>

Di sini, kita memilih membuat method `width` mengembalikan `true` jika nilai pada field `width` instance lebih besar dari `0`, dan `false` jika nilainya `0`: kita bisa memakai field di dalam method dengan nama yang sama untuk tujuan apa pun. Di `main`, ketika kita menulis `rect1.width` lalu diikuti tanda kurung, Rust tahu yang kita maksud adalah method `width`. Ketika tanpa tanda kurung, Rust tahu yang kita maksud adalah field `width`.

Sering, tapi tidak selalu, ketika kita memberi sebuah method nama yang sama dengan sebuah field, kita ingin method itu hanya mengembalikan nilai di dalam field dan tidak melakukan apa pun lagi. Method seperti ini disebut _getter_, dan Rust tidak mengimplementasikannya secara otomatis untuk field struct seperti beberapa bahasa lain. Getter berguna karena kamu bisa membuat field itu private tetapi method-nya public, sehingga membuka akses baca-saja terhadap field tersebut sebagai bagian dari API publik tipe kita. Kita akan membahas apa itu public dan private serta cara menentukan sebuah field atau method sebagai public atau private di [Bab 7][public]<!-- ignore -->.

> <a id="wheres-the---operator"></a>
> ### Di Mana Operator `->`?
>
> Di C dan C++, ada dua operator berbeda untuk memanggil method: kamu memakai `.` jika memanggil method pada objek secara langsung, dan `->` jika memanggil method pada pointer ke objek dan perlu men-dereference pointer itu terlebih dahulu. Dengan kata lain, jika `object` adalah sebuah pointer, `object->something()` mirip dengan `(*object).something()`.
>
> Rust tidak punya padanan untuk operator `->`; sebagai gantinya, Rust punya fitur yang disebut _automatic referencing and dereferencing_. Memanggil method adalah salah satu dari sedikit tempat di Rust yang punya perilaku ini.
>
> Begini cara kerjanya: ketika kamu memanggil method dengan `object.something()`, Rust otomatis menambahkan `&`, `&mut`, atau `*` agar `object` cocok dengan signature method-nya. Dengan kata lain, dua baris berikut ini sama saja:
>
> <!-- CAN'T EXTRACT SEE BUG https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust
> # #[derive(Debug,Copy,Clone)]
> # struct Point {
> #     x: f64,
> #     y: f64,
> # }
> #
> # impl Point {
> #    fn distance(&self, other: &Point) -> f64 {
> #        let x_squared = f64::powi(other.x - self.x, 2);
> #        let y_squared = f64::powi(other.y - self.y, 2);
> #
> #        f64::sqrt(x_squared + y_squared)
> #    }
> # }
> # let p1 = Point { x: 0.0, y: 0.0 };
> # let p2 = Point { x: 5.0, y: 6.5 };
> p1.distance(&p2);
> (&p1).distance(&p2);
> ```
>
> Baris pertama jauh lebih rapi. Perilaku automatic referencing ini bisa terjadi karena method punya receiver yang jelas, yaitu tipe `self`. Dengan receiver dan nama sebuah method, Rust bisa memastikan secara pasti apakah method itu membaca (`&self`), mengubah (`&mut self`), atau mengonsumsi (`self`). Fakta bahwa Rust membuat borrowing menjadi implisit bagi receiver method adalah bagian besar dari menjadikan ownership terasa ergonomis dalam praktik.

### Method dengan Lebih Banyak Parameter

Mari berlatih memakai method dengan mengimplementasikan method kedua pada struct `Rectangle`. Kali ini kita ingin sebuah instance `Rectangle` menerima instance `Rectangle` lain dan mengembalikan `true` jika `Rectangle` kedua muat sepenuhnya di dalam `self` (yaitu `Rectangle` pertama); selainnya, method harus mengembalikan `false`. Artinya, setelah kita mendefinisikan method `can_hold`, kita harus bisa menulis program yang ditampilkan pada Listing 5-14.

<Listing number="5-14" file-name="src/main.rs" caption="Memakai method `can_hold` yang belum ditulis">

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-14/src/main.rs}}
```

</Listing>

Keluaran yang diharapkan akan terlihat seperti berikut, karena kedua dimensi `rect2` lebih kecil daripada dimensi `rect1`, sedangkan `rect3` lebih lebar dari `rect1`:

```text
Can rect1 hold rect2? true
Can rect1 hold rect3? false
```

Kita tahu kita ingin mendefinisikan sebuah method, jadi method itu akan berada di dalam blok `impl Rectangle`. Nama method-nya adalah `can_hold`, dan method itu menerima immutable borrow dari sebuah `Rectangle` lain sebagai parameter. Kita bisa mengetahui tipe parameter itu dengan melihat kode yang memanggil method: `rect1.can_hold(&rect2)` mengoper `&rect2`, yaitu immutable borrow ke `rect2`, sebuah instance `Rectangle`. Ini masuk akal karena kita hanya perlu membaca `rect2` (bukan menulis, yang berarti kita butuh mutable borrow), dan kita ingin `main` tetap memiliki ownership atas `rect2` agar bisa memakainya lagi setelah memanggil method `can_hold`. Nilai balikan `can_hold` berupa Boolean, dan implementasinya akan memeriksa apakah width dan height dari `self` lebih besar daripada width dan height dari `Rectangle` lainnya, masing-masing. Mari tambahkan method baru `can_hold` ke blok `impl` dari Listing 5-13, seperti ditampilkan pada Listing 5-15.

<Listing number="5-15" file-name="src/main.rs" caption="Mengimplementasikan method `can_hold` pada `Rectangle` yang menerima sebuah instance `Rectangle` lain sebagai parameter">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-15/src/main.rs:here}}
```

</Listing>

Ketika kita menjalankan kode ini bersama fungsi `main` pada Listing 5-14, kita akan mendapat keluaran yang kita inginkan. Method bisa menerima beberapa parameter yang kita tambahkan pada signature setelah parameter `self`, dan parameter-parameter itu bekerja sama seperti parameter pada fungsi.

### Fungsi Terkait

Semua fungsi yang didefinisikan di dalam sebuah blok `impl` disebut _fungsi terkait_ (_associated functions_) karena diasosiasikan dengan tipe yang dinamai oleh `impl` tersebut. Kita bisa mendefinisikan fungsi terkait yang tidak punya `self` sebagai parameter pertama (dan karena itu bukan method) karena mereka tidak butuh instance tipe untuk bekerja. Kita sudah pernah memakai satu fungsi seperti ini: fungsi `String::from` yang didefinisikan pada tipe `String`.

Fungsi terkait yang bukan method sering dipakai sebagai konstruktor yang mengembalikan instance baru dari struct. Konstruktor ini sering diberi nama `new`, tapi `new` bukan nama khusus dan tidak bawaan bahasa. Sebagai contoh, kita bisa memilih menyediakan fungsi terkait bernama `square` yang menerima satu parameter dimensi dan memakainya baik sebagai width maupun height, sehingga lebih mudah membuat sebuah `Rectangle` persegi tanpa harus menyebut nilai yang sama dua kali:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-03-associated-functions/src/main.rs:here}}
```

Keyword `Self` pada tipe balikan dan di dalam isi fungsi adalah alias untuk tipe yang muncul setelah keyword `impl`, yaitu `Rectangle` dalam kasus ini.

Untuk memanggil fungsi terkait ini, kita memakai sintaks `::` bersama nama struct; `let sq = Rectangle::square(3);` adalah sebuah contoh. Fungsi ini berada dalam namespace milik struct: sintaks `::` dipakai baik untuk fungsi terkait maupun namespace yang dibuat oleh module. Kita akan membahas module di [Bab 7][modules]<!-- ignore -->.

### Beberapa Blok `impl`

Setiap struct boleh punya lebih dari satu blok `impl`. Sebagai contoh, Listing 5-15 setara dengan kode pada Listing 5-16, yang menaruh tiap method di blok `impl`-nya sendiri.

<Listing number="5-16" caption="Menulis ulang Listing 5-15 dengan beberapa blok `impl`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-16/src/main.rs:here}}
```

</Listing>

Tidak ada alasan untuk memisahkan method-method ini ke beberapa blok `impl` di sini, tapi ini tetap sintaks yang valid. Kita akan melihat kasus di mana beberapa blok `impl` berguna pada Bab 10, ketika kita membahas tipe generic dan trait.

## Ringkasan

Struct memungkinkan kamu membuat tipe kustom yang bermakna bagi domain kamu. Dengan memakai struct, kamu bisa menjaga bagian-bagian data yang saling terhubung tetap terhubung dan menamai tiap bagian agar kode kamu jelas. Di dalam blok `impl`, kamu bisa mendefinisikan fungsi yang diasosiasikan dengan tipe kamu, dan method adalah sejenis fungsi terkait yang memungkinkan kamu menentukan perilaku yang dimiliki oleh instance struct kamu.

Tapi struct bukan satu-satunya cara membuat tipe kustom: mari beralih ke fitur enum di Rust untuk menambahkan satu lagi ke kotak perkakasmu.

[enums]: ch06-00-enums.html
[trait-objects]: ch18-02-trait-objects.md
[public]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html
