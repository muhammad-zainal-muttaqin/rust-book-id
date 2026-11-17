## Contoh Program yang Menggunakan Struct

Untuk memahami kapan kita ingin menggunakan struct, mari kita tulis program yang menghitung luas sebuah persegi panjang. Kita akan mulai dengan variabel tunggal, lalu me-refactor program itu sampai kita menggantinya dengan struct.

Mari kita buat project binary baru dengan Cargo bernama _rectangles_ yang menerima lebar dan tinggi sebuah persegi panjang dalam satuan piksel lalu menghitung luas persegi panjang itu. Listing 5-8 menunjukkan program singkat yang melakukan tepat hal tersebut di _src/main.rs_ project kita.

<Listing number="5-8" file-name="src/main.rs" caption="Menghitung luas persegi panjang yang ditentukan oleh variabel lebar dan tinggi yang terpisah">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:all}}
```

</Listing>

Sekarang, jalankan program ini dengan `cargo run`:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/output.txt}}
```

Kode ini berhasil menemukan luas persegi panjang dengan memanggil fungsi `area` untuk tiap dimensi, tapi masih ada yang bisa kita perbaiki agar kode ini lebih jelas dan mudah dibaca.

Masalah kode ini terlihat jelas dari signature `area`:

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:here}}
```

Fungsi `area` seharusnya menghitung luas satu persegi panjang, tapi fungsi yang kita tulis punya dua parameter, dan tidak ada satu pun bagian program kita yang menjelaskan bahwa kedua parameter itu saling berkaitan. Lebar dan tinggi akan lebih mudah dibaca dan diatur kalau kita kelompokkan bersama. Kita sudah membahas salah satu caranya di bagian [“Tipe Tuple”][the-tuple-type]<!-- ignore --> Bab 3, yaitu dengan menggunakan tuple.

### Refactoring dengan Tuple

Listing 5-9 menunjukkan versi lain dari program kita yang menggunakan tuple.

<Listing number="5-9" file-name="src/main.rs" caption="Menentukan lebar dan tinggi persegi panjang dengan tuple">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-09/src/main.rs}}
```

</Listing>

Dalam satu hal, program ini lebih baik. Tuple memberi sedikit struktur, dan kini kita hanya mengoper satu argumen. Tapi di sisi lain, versi ini kurang jelas: tuple tidak memberi nama pada elemennya, jadi kita harus mengakses bagian tuple lewat indeks, sehingga perhitungan kita jadi kurang terlihat jelas.

Tertukarnya lebar dan tinggi tidak masalah untuk perhitungan luas, tapi kalau kita ingin menggambar persegi panjang di layar, itu jadi masalah! Kita harus selalu mengingat bahwa `width` ada di indeks tuple `0` dan `height` ada di indeks tuple `1`. Bagi orang lain, hal itu justru lebih sulit ditebak dan diingat kalau mereka memakai kode kita. Karena kita belum menyampaikan makna data kita di dalam kode, error jadi lebih mudah muncul.

<!-- Old headings. Do not remove or links may break. -->

<a id="refactoring-with-structs-adding-more-meaning"></a>

### Refactoring dengan Struct

Kita menggunakan struct untuk menambah makna dengan memberi label pada data. Tuple yang kita pakai bisa kita ubah menjadi struct yang punya nama untuk keseluruhannya sekaligus nama untuk tiap bagiannya, seperti ditunjukkan Listing 5-10.

<Listing number="5-10" file-name="src/main.rs" caption="Mendefinisikan struct `Rectangle`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-10/src/main.rs}}
```

</Listing>

Di sini kita sudah mendefinisikan sebuah struct dan menamainya `Rectangle`. Di dalam kurung kurawal, kita mendefinisikan field `width` dan `height`, yang keduanya bertipe `u32`. Lalu, di `main`, kita membuat sebuah instance `Rectangle` dengan lebar `30` dan tinggi `50`.

Fungsi `area` kita kini didefinisikan dengan satu parameter yang kita beri nama `rectangle`, bertipe borrow immutable atas sebuah instance struct `Rectangle`. Seperti disebutkan di Bab 4, kita ingin meminjam struct itu alih-alih mengambil ownership-nya. Dengan begitu, `main` tetap memegang ownership dan bisa terus menggunakan `rect1`—itulah alasan kita memakai `&` pada signature fungsi dan pada saat kita memanggil fungsi itu.

Fungsi `area` mengakses field `width` dan `height` dari instance `Rectangle` (perhatikan bahwa mengakses field sebuah instance struct yang dipinjam tidak memindahkan nilai field itu, itulah sebabnya kamu sering melihat struct dipinjam). Signature fungsi `area` kita kini mengatakan persis apa yang kita maksud: hitung luas `Rectangle` menggunakan field `width` dan `height`-nya. Dengan begitu terlihat bahwa lebar dan tinggi saling berkaitan, dan kita memberi nama yang deskriptif pada nilai-nilai itu alih-alih memakai indeks tuple `0` dan `1`. Ini sebuah kemenangan untuk kejelasan.

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-useful-functionality-with-derived-traits"></a>

### Menambah Kemampuan dengan Trait yang Di-derive

Akan sangat berguna kalau kita bisa mencetak sebuah instance `Rectangle` beserta nilai semua field-nya saat sedang debug program. Listing 5-11 mencoba memakai macro [`println!`][println]<!-- ignore --> seperti yang kita gunakan di bab-bab sebelumnya. Tapi cara ini tidak akan berhasil.

<Listing number="5-11" file-name="src/main.rs" caption="Mencoba mencetak sebuah instance `Rectangle`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/src/main.rs}}
```

</Listing>

Ketika kita mengompilasi kode ini, kita mendapat error dengan pesan inti berikut:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:3}}
```

Macro `println!` bisa melakukan banyak jenis penataan, dan secara bawaan, kurung kurawal memberi tahu `println!` untuk memakai penataan yang dikenal sebagai `Display`: keluaran yang ditujukan langsung bagi pengguna akhir. Tipe-tipe primitif yang sudah kita lihat sejauh ini mengimplementasikan `Display` secara bawaan karena hanya ada satu cara kamu ingin menampilkan `1` atau tipe primitif lain kepada pengguna. Tapi dengan struct, cara `println!` menata keluarannya jadi tidak jelas karena ada lebih banyak kemungkinan tampilan: Mau pakai koma atau tidak? Mau mencetak kurung kurawalnya? Apakah semua field harus ditampilkan? Karena ambiguitas ini, Rust tidak menebak apa yang kita inginkan, dan struct tidak punya implementasi `Display` yang disediakan untuk dipakai bersama `println!` dan placeholder `{}`.

Kalau kita lanjut membaca error-nya, kita akan menemukan catatan yang membantu ini:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:9:10}}
```

Mari kita coba! Pemanggilan macro `println!` kini akan menjadi `println!("rect1 is
{rect1:?}");`. Menaruh spesifier `:?` di dalam kurung kurawal memberi tahu `println!` bahwa kita ingin memakai format keluaran bernama `Debug`. Trait `Debug` membuat kita bisa mencetak struct dengan cara yang berguna bagi developer sehingga kita bisa melihat nilainya saat debug kode.

Kompilasi kode dengan perubahan ini. Yah! Kita masih mendapat error:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:3}}
```

Tapi sekali lagi, compiler memberi kita catatan yang membantu:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:9:10}}
```

Rust _memang_ menyediakan kemampuan untuk mencetak informasi debug, tapi kita harus secara eksplisit memilih mengaktifkan kemampuan itu agar tersedia untuk struct kita. Caranya, kita menambahkan atribut luar `#[derive(Debug)]` tepat sebelum definisi struct, seperti ditunjukkan Listing 5-12.

<Listing number="5-12" file-name="src/main.rs" caption="Menambahkan atribut untuk men-derive trait `Debug` dan mencetak instance `Rectangle` dengan penataan debug">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/src/main.rs}}
```

</Listing>

Sekarang ketika kita menjalankan program, tidak ada error yang muncul, dan kita akan melihat keluaran berikut:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/output.txt}}
```

Keren! Bukan keluaran yang paling cantik, tapi keluaran ini menampilkan nilai semua field dari instance tersebut, yang jelas sangat membantu saat debug. Kalau kita punya struct yang lebih besar, akan berguna kalau keluarannya sedikit lebih mudah dibaca; untuk itu, kita bisa memakai `{:#?}` alih-alih `{:?}` di dalam string `println!`. Pada contoh ini, gaya `{:#?}` akan menghasilkan keluaran berikut:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-02-pretty-debug/output.txt}}
```

Cara lain untuk mencetak nilai dengan format `Debug` adalah memakai macro [`dbg!`][dbg]<!-- ignore -->, yang mengambil ownership atas sebuah ekspresi (berbeda dengan `println!` yang mengambil reference), mencetak file dan nomor baris tempat pemanggilan macro `dbg!` itu berada di kode kamu beserta nilai hasil ekspresi tersebut, lalu mengembalikan ownership atas nilai itu.

> Catatan: Memanggil macro `dbg!` mencetak ke stream console standard error (`stderr`), berbeda dengan `println!` yang mencetak ke stream console standard output (`stdout`). Kita akan membahas `stderr` dan `stdout` lebih lanjut di [bagian “Mengalihkan Error ke Standard Error” di Bab 12][err]<!-- ignore -->.

Berikut contoh di mana kita ingin melihat nilai yang ditetapkan ke field `width`, sekaligus nilai keseluruhan struct di `rect1`:

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/src/main.rs}}
```

Kita bisa membungkus ekspresi `30 * scale` dengan `dbg!` dan, karena `dbg!` mengembalikan ownership atas nilai ekspresi itu, field `width` akan mendapat nilai yang sama seolah-olah tidak ada pemanggilan `dbg!` di sana. Kita tidak ingin `dbg!` mengambil ownership atas `rect1`, jadi pada pemanggilan berikutnya kita memakai reference ke `rect1`. Berikut keluaran dari contoh ini:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/output.txt}}
```

Kita bisa melihat keluaran pertama berasal dari _src/main.rs_ baris 10, tempat kita men-debug ekspresi `30 * scale`, dan nilai hasilnya adalah `60` (penataan `Debug` yang diimplementasikan untuk integer hanya mencetak nilainya saja). Pemanggilan `dbg!` di baris 14 _src/main.rs_ mengeluarkan nilai `&rect1`, yaitu struct `Rectangle`. Keluaran ini memakai penataan `Debug` yang rapi dari tipe `Rectangle`. Macro `dbg!` bisa sangat membantu ketika kamu berusaha memahami apa yang dilakukan kode kamu!

Selain trait `Debug`, Rust menyediakan sejumlah trait yang bisa kita gunakan bersama atribut `derive` untuk menambahkan perilaku berguna pada tipe kustom kita. Trait-trait beserta perilakunya terdaftar di [Lampiran C][app-c]<!-- ignore -->. Kita akan membahas cara mengimplementasikan trait-trait itu dengan perilaku kustom, sekaligus cara membuat trait milikmu sendiri, di Bab 10. Selain `derive`, masih banyak atribut lain; untuk informasi lebih lanjut, lihat [bagian “Atribut” pada Rust Reference][attributes].

Fungsi `area` kita sangat spesifik: ia hanya menghitung luas persegi panjang. Akan lebih baik kalau kita kaitkan perilaku ini lebih erat dengan struct `Rectangle` kita karena fungsi itu tidak akan bekerja dengan tipe lain. Mari kita lihat bagaimana kita bisa melanjutkan refactor kode ini dengan mengubah fungsi `area` menjadi method `area` yang didefinisikan pada tipe `Rectangle` kita.

[the-tuple-type]: ch03-02-data-types.html#the-tuple-type
[app-c]: appendix-03-derivable-traits.md
[println]: ../std/macro.println.html
[dbg]: ../std/macro.dbg.html
[err]: ch12-06-writing-to-stderr-instead-of-stdout.html
[attributes]: ../reference/attributes.html
