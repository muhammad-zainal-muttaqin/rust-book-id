## Fungsi dan Closure Lanjutan

Bagian ini membahas beberapa fitur lanjutan yang berkaitan dengan fungsi dan
closure, termasuk pointer fungsi dan cara mengembalikan closure.

### Pointer Fungsi

Kita sudah bicara soal cara mengoper closure ke fungsi; ternyata kamu juga bisa
mengoper fungsi biasa ke fungsi! Teknik ini berguna saat kamu ingin mengoper
sebuah fungsi yang sudah kamu definisikan, alih-alih mendefinisikan closure baru.
Fungsi berubah menjadi tipe `fn` (dengan huruf _f_ kecil), jangan tertukar dengan
trait closure `Fn`. Tipe `fn` disebut sebagai _function pointer_. Dengan
mengoper fungsi memakai function pointer, kamu bisa memakai fungsi sebagai
argumen untuk fungsi lain.

Sintaks untuk menyatakan bahwa sebuah parameter adalah function pointer mirip
dengan sintaks closure, seperti yang kamu lihat di Listing 20-28. Di sana kita
mendefinisikan fungsi `add_one` yang menambah 1 pada parameternya. Fungsi
`do_twice` menerima dua parameter: sebuah function pointer ke fungsi apa pun
yang menerima parameter `i32` dan mengembalikan `i32`, serta sebuah nilai `i32`.
Fungsi `do_twice` memanggil fungsi `f` dua kali dengan mengoper nilai `arg`, lalu
menjumlahkan kedua hasil pemanggilan tersebut. Fungsi `main` memanggil `do_twice`
dengan argumen `add_one` dan `5`.

<Listing number="20-28" file-name="src/main.rs" caption="Memakai tipe `fn` untuk menerima function pointer sebagai argumen">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-28/src/main.rs}}
```

</Listing>

Kode ini mencetak `The answer is: 12`. Kita menyatakan bahwa parameter `f` di
`do_twice` adalah sebuah `fn` yang menerima satu parameter bertipe `i32` dan
mengembalikan `i32`. Setelah itu kita bisa memanggil `f` di dalam tubuh
`do_twice`. Di `main`, kita bisa mengoper nama fungsi `add_one` sebagai argumen
pertama ke `do_twice`.

Berbeda dengan closure, `fn` adalah sebuah tipe, bukan trait. Jadi kita
menuliskan `fn` langsung sebagai tipe parameter, alih-alih mendeklarasikan
parameter tipe generic dengan salah satu trait `Fn` sebagai trait bound.

Function pointer mengimplementasikan ketiga trait closure (`Fn`, `FnMut`, dan
`FnOnce`), artinya kamu selalu bisa mengoper function pointer sebagai argumen ke
fungsi yang mengharapkan closure. Sebaiknya tulis fungsi memakai tipe generic dan
salah satu trait closure agar fungsimu bisa menerima baik fungsi maupun closure.

Meski begitu, ada kalanya kamu hanya ingin menerima `fn`, bukan closure—
misalnya saat berhubungan dengan kode eksternal yang tidak punya closure:
fungsi C bisa menerima fungsi sebagai argumen, tetapi C tidak mengenal closure.

Sebagai contoh kasus di mana kamu bisa memakai closure yang ditulis langsung
maupun fungsi bernama, mari kita lihat penggunaan method `map` yang disediakan
oleh trait `Iterator` di pustaka standar. Untuk memakai method `map` mengubah
vector angka menjadi vector string, kita bisa memakai closure seperti di Listing
20-29.

<Listing number="20-29" caption="Memakai closure dengan method `map` untuk mengubah angka menjadi string">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-29/src/main.rs:here}}
```

</Listing>

Atau kita bisa menyebut sebuah fungsi sebagai argumen `map`, menggantikan
closure. Listing 20-30 menunjukkan tampilannya.

<Listing number="20-30" caption="Memakai fungsi `String::to_string` dengan method `map` untuk mengubah angka menjadi string">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-30/src/main.rs:here}}
```

</Listing>

Perhatikan bahwa kita harus memakai sintaks nama lengkap yang sudah kita bahas
di bagian [“Advanced Traits”][advanced-traits]<!-- ignore -->, karena ada
beberapa fungsi bernama `to_string` yang tersedia.

Di sini kita memakai fungsi `to_string` yang didefinisikan dalam trait
`ToString`, yang sudah diimplementasikan pustaka standar untuk tipe apa pun yang
mengimplementasikan `Display`.

Ingat dari bagian [“Enum Values”][enum-values]<!-- ignore --> di Bab 6 bahwa
nama setiap varian enum yang kita definisikan juga menjadi fungsi inisialisasi.
Kita bisa memakai fungsi-fungsi inisialisasi ini sebagai function pointer yang
mengimplementasikan trait closure. Artinya, kita bisa menyebut fungsi
inisialisasi sebagai argumen untuk method yang menerima closure, seperti yang
kamu lihat di Listing 20-31.

<Listing number="20-31" caption="Memakai inisialisasi enum dengan method `map` untuk membuat instance `Status` dari angka">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-31/src/main.rs:here}}
```

</Listing>

Di sini kita membuat instance `Status::Value` dari setiap nilai `u32` dalam
rentang yang dipakai `map`, dengan memanggil fungsi inisialisasi
`Status::Value`. Ada yang lebih suka gaya ini, ada pula yang lebih suka memakai
closure. Keduanya dikompilasi menjadi kode yang sama, jadi pilih gaya yang paling
jelas menurutmu.

### Mengembalikan Closure

Closure direpresentasikan oleh trait, yang berarti kamu tidak bisa
mengembalikan closure secara langsung. Pada kebanyakan kasus di mana kamu ingin
mengembalikan sebuah trait, kamu bisa memakai tipe konkret yang mengimplementasi
trait itu sebagai nilai kembalian fungsi. Namun, untuk closure kamu biasanya
tidak bisa melakukan itu karena closure tidak punya tipe konkret yang bisa
dikembalikan. Kamu juga tidak boleh memakai function pointer `fn` sebagai tipe
kembalian jika closure tersebut menangkap nilai apa pun dari scope-nya, misalnya.

Sebagai gantinya, kamu biasanya akan memakai sintaks `impl Trait` yang sudah kita
pelajari di Bab 10. Kamu bisa mengembalikan tipe fungsi apa pun, memakai `Fn`,
`FnOnce`, dan `FnMut`. Misalnya, kode di Listing 20-32 akan terkompilasi dengan
baik.

<Listing number="20-32" caption="Mengembalikan closure dari fungsi memakai sintaks `impl Trait`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-32/src/lib.rs}}
```

</Listing>

Meski begitu, seperti yang kita catat di bagian [“Inferring and Annotating Closure
Types”][closure-types]<!-- ignore --> dalam Bab 13, setiap closure juga punya
tipenya sendiri yang berbeda. Jika kamu perlu bekerja dengan beberapa fungsi
yang punya tanda tangan sama tetapi implementasi berbeda, kamu perlu memakai
trait object untuk mereka. Perhatikan apa yang terjadi jika kamu menulis kode
seperti di Listing 20-33.

<Listing file-name="src/main.rs" number="20-33" caption="Membuat `Vec<T>` berisi closure yang didefinisikan oleh fungsi yang mengembalikan tipe `impl Fn`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-33/src/main.rs}}
```

</Listing>

Di sini kita punya dua fungsi, `returns_closure` dan
`returns_initialized_closure`, yang keduanya mengembalikan `impl Fn(i32) ->
i32`. Perhatikan bahwa closure yang mereka kembalikan berbeda, meskipun keduanya
mengimplementasikan tipe yang sama. Jika kita mencoba mengompilasi kode ini,
Rust memberi tahu kita bahwa kode itu tidak akan jalan:

```text
{{#include ../listings/ch20-advanced-features/listing-20-33/output.txt}}
```

Pesan error itu menjelaskan bahwa setiap kali kita mengembalikan `impl Trait`,
Rust membuat _opaque type_ yang unik—sebuah tipe yang detailnya tidak bisa kita
lihat dari apa yang Rust bangun untuk kita, dan kita juga tidak bisa menebak tipe
yang akan dihasilkan Rust untuk ditulis sendiri. Jadi, meskipun fungsi-fungsi ini
mengembalikan closure yang mengimplementasikan trait yang sama, yaitu
`Fn(i32) -> i32`, opaque type yang Rust hasilkan untuk masing-masing tetap
berbeda. (Ini mirip dengan cara Rust menghasilkan tipe konkret yang berbeda
untuk blok async yang berbeda, bahkan ketika tipe keluarannya sama, seperti yang
kita lihat di [“The `Pin` Type and the `Unpin` Trait”][future-types]<!-- ignore -->
di Bab 17.) Kita sudah beberapa kali melihat solusi untuk masalah ini: kita bisa
memakai trait object, seperti di Listing 20-34.

<Listing number="20-34" caption="Membuat `Vec<T>` berisi closure yang didefinisikan oleh fungsi yang mengembalikan `Box<dyn Fn>` agar tipenya sama">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-34/src/main.rs:here}}
```

</Listing>

Kode ini akan terkompilasi dengan baik. Untuk penjelasan lebih lanjut soal trait
object, lihat bagian [“Using Trait Objects To Abstract over Shared
Behavior”][trait-objects]<!-- ignore --> di Bab 18.

Selanjutnya, mari kita bahas macro!

[advanced-traits]: ch20-02-advanced-traits.html#advanced-traits
[enum-values]: ch06-01-defining-an-enum.html#enum-values
[closure-types]: ch13-01-closures.html#closure-type-inference-and-annotation
[future-types]: ch17-03-more-futures.html
[trait-objects]: ch18-02-trait-objects.html
