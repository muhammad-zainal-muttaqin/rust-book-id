## Tipe Lanjutan

Sistem tipe Rust punya beberapa fitur yang sudah kita sebutkan sebelumnya tetapi belum kita bahas. Kita akan mulai dengan membahas newtype secara umum sambil melihat mengapa tipe-tipe itu berguna. Setelah itu, kita beralih ke alias tipe, fitur yang mirip dengan newtype tetapi dengan semantik yang sedikit beda. Kita juga akan membahas tipe `!` dan tipe yang ukurannya ditentukan saat runtime.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-newtype-pattern-for-type-safety-and-abstraction"></a>

### Keamanan Tipe dan Abstraksi dengan Pola Newtype

Bagian ini mengasumsikan kamu sudah membaca bagian sebelumnya, [“Mengimplementasikan Trait Eksternal dengan Pola Newtype”][newtype]<!-- ignore -->. Pola newtype juga berguna untuk tugas-tugas di luar yang sudah kita bahas sejauh ini, termasuk memberlakukan secara statis bahwa nilai-nilai tidak pernah tertukar dan menunjukkan satuan dari sebuah nilai. Kamu sudah melihat contoh penggunaan newtype untuk menunjukkan satuan di Listing 20-16: Ingat bahwa struct `Millimeters` dan `Meters` membungkus nilai `u32` di dalam newtype. Jika kita menulis fungsi dengan parameter bertipe `Millimeters`, kita tidak bisa mengompilasi program yang tanpa sengaja mencoba memanggil fungsi itu dengan nilai bertipe `Meters` atau `u32` biasa.

Kita juga bisa memakai pola newtype untuk menyembunyikan beberapa detail implementasi dari sebuah tipe: Tipe baru itu bisa mengekspos API publik yang berbeda dari API tipe dalam yang bersifat private.

Newtype juga bisa menyembunyikan implementasi internal. Misalnya, kita bisa menyediakan tipe `People` untuk membungkus `HashMap<i32, String>` yang menyimpan ID seseorang yang dikaitkan dengan namanya. Kode yang memakai `People` hanya akan berinteraksi dengan API publik yang kita sediakan, seperti metode untuk menambahkan string nama ke dalam koleksi `People`; kode itu tidak perlu tahu bahwa kita secara internal memberi ID `i32` pada nama. Pola newtype adalah cara ringan untuk mencapai enkapsulasi guna menyembunyikan detail implementasi, yang sudah kita bahas di bagian [“Enkapsulasi yang Menyembunyikan Detail Implementasi”][encapsulation-that-hides-implementation-details]<!-- ignore --> di Bab 18.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-type-synonyms-with-type-aliases"></a>

<a id="type-synonyms-and-type-aliases"></a>
### Sinonim Tipe dan Alias Tipe

Rust menyediakan kemampuan untuk mendeklarasikan _alias tipe_ agar sebuah tipe yang sudah ada punya nama lain. Untuk itu kita memakai keyword `type`. Misalnya, kita bisa membuat alias `Kilometers` untuk `i32` seperti ini:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:here}}
```

Sekarang alias `Kilometers` adalah _sinonim_ untuk `i32`; tidak seperti tipe `Millimeters` dan `Meters` yang kita buat di Listing 20-16, `Kilometers` bukan tipe baru yang terpisah. Nilai-nilai yang bertipe `Kilometers` akan diperlakukan sama seperti nilai bertipe `i32`:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:there}}
```

Karena `Kilometers` dan `i32` adalah tipe yang sama, kita bisa menjumlahkan nilai dari kedua tipe itu dan bisa mengoper nilai `Kilometers` ke fungsi yang menerima parameter `i32`. Akan tetapi, dengan cara ini kita tidak mendapatkan manfaat pemeriksaan tipe yang kita peroleh dari pola newtype yang dibahas sebelumnya. Dengan kata lain, jika kita mencampuradukkan nilai `Kilometers` dan `i32` di suatu tempat, compiler tidak akan memberi kita error.

Kasus penggunaan utama sinonim tipe adalah mengurangi pengulangan. Misalnya, kita mungkin punya tipe yang panjang seperti ini:

```rust,ignore
Box<dyn Fn() + Send + 'static>
```

Menulis tipe panjang itu di signature fungsi dan sebagai anotasi tipe di seluruh kode bisa melelahkan dan rawan salah. Bayangkan sebuah proyek yang penuh dengan kode seperti di Listing 20-25.

<Listing number="20-25" caption="Memakai tipe panjang di banyak tempat">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-25/src/main.rs:here}}
```

</Listing>

Alias tipe membuat kode ini lebih mudah dikelola dengan mengurangi pengulangan. Di Listing 20-26, kita memperkenalkan alias bernama `Thunk` untuk tipe yang panjang itu, lalu bisa mengganti semua pemakaian tipe tersebut dengan alias yang lebih pendek, `Thunk`.

<Listing number="20-26" caption="Memperkenalkan alias tipe, `Thunk`, untuk mengurangi pengulangan">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-26/src/main.rs:here}}
```

</Listing>

Kode ini jauh lebih mudah dibaca dan ditulis! Memilih nama yang bermakna untuk alias tipe juga bisa membantu menyampaikan maksud kamu (_thunk_ adalah istilah untuk kode yang akan dievaluasi nanti, jadi nama itu pas untuk closure yang disimpan).

Alias tipe juga umum dipakai bersama tipe `Result<T, E>` untuk mengurangi pengulangan. Perhatikan module `std::io` di pustaka standar. Operasi I/O sering mengembalikan `Result<T, E>` untuk menangani situasi ketika operasi gagal. Pustaka ini punya struct `std::io::Error` yang mewakili semua kemungkinan error I/O. Banyak fungsi di `std::io` akan mengembalikan `Result<T, E>` dengan `E` berupa `std::io::Error`, seperti fungsi-fungsi berikut di trait `Write`:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-05-write-trait/src/lib.rs}}
```

`Result<..., Error>` diulang berkali-kali. Karena itu, `std::io` punya deklarasi alias tipe ini:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:here}}
```

Karena deklarasi ini berada di module `std::io`, kita bisa memakai alias yang sepenuhnya memenuhi syarat, `std::io::Result<T>`; yaitu `Result<T, E>` dengan `E` diisi sebagai `std::io::Error`. Signature fungsi di trait `Write` akhirnya terlihat seperti ini:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:there}}
```

Alias tipe membantu dalam dua cara: kode jadi lebih mudah ditulis _dan_ kita mendapatkan antarmuka yang konsisten di seluruh `std::io`. Karena ini adalah alias, tipe itu hanyalah `Result<T, E>` lain, yang berarti kita bisa memakai metode apa pun yang bekerja pada `Result<T, E>` dengannya, serta sintaks khusus seperti operator `?`.

### Tipe Never yang Tidak Pernah Kembali

Rust punya tipe khusus bernama `!` yang dalam istilah teori tipe disebut _tipe kosong_ karena tidak punya nilai sama sekali. Kita lebih suka menyebutnya _tipe never_ karena tipe ini berdiri di tempat tipe kembalian ketika sebuah fungsi tidak akan pernah kembali. Berikut contohnya:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-07-never-type/src/lib.rs:here}}
```

Kode ini dibaca sebagai “fungsi `bar` tidak pernah kembali.” Fungsi yang tidak pernah kembali disebut _fungsi yang divergen_. Kita tidak bisa membuat nilai bertipe `!`, jadi `bar` tidak mungkin kembali.

Tapi apa gunanya tipe yang tidak bisa kita buat nilainya? Ingat kode di Listing 2-5, bagian dari game tebak angka; kita sajikan kembali sebagiannya di Listing 20-27.

<Listing number="20-27" caption="Sebuah `match` dengan cabang yang diakhiri `continue`">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:ch19}}
```

</Listing>

Saat itu, kita melewati beberapa detail dalam kode ini. Di bagian [“Kontrol Alur `match`”][the-match-control-flow-construct]<!-- ignore --> di Bab 6, kita sudah membahas bahwa semua cabang `match` harus mengembalikan tipe yang sama. Jadi, misalnya, kode berikut tidak bekerja:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-08-match-arms-different-types/src/main.rs:here}}
```

Tipe `guess` dalam kode ini seharusnya harus berupa integer _dan_ string, sementara Rust mengharuskan `guess` hanya punya satu tipe. Jadi, apa yang dikembalikan `continue`? Bagaimana kita bisa mengembalikan `u32` dari satu cabang dan memiliki cabang lain yang diakhiri `continue` di Listing 20-27?

Seperti yang mungkin sudah kamu duga, `continue` punya nilai `!`. Artinya, saat Rust menghitung tipe `guess`, ia melihat kedua cabang match, yang pertama dengan nilai `u32` dan yang kedua dengan nilai `!`. Karena `!` tidak mungkin punya nilai, Rust memutuskan bahwa tipe `guess` adalah `u32`.

Cara formal untuk menggambarkan perilaku ini adalah ekspresi bertipe `!` bisa dipaksa menjadi tipe lain apa pun. Kita boleh mengakhiri cabang `match` ini dengan `continue` karena `continue` tidak mengembalikan nilai; sebagai gantinya, ia mengembalikan kendali ke bagian atas loop, sehingga dalam kasus `Err`, kita tidak pernah memberi nilai pada `guess`.

Tipe never juga berguna bersama macro `panic!`. Ingat fungsi `unwrap` yang kita panggil pada nilai `Option<T>` untuk menghasilkan sebuah nilai atau panic, dengan definisi berikut:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-09-unwrap-definition/src/lib.rs:here}}
```

Dalam kode ini, hal yang sama terjadi seperti pada `match` di Listing 20-27: Rust melihat bahwa `val` bertipe `T` dan `panic!` bertipe `!`, sehingga hasil dari seluruh ekspresi `match` adalah `T`. Kode ini bekerja karena `panic!` tidak menghasilkan nilai; ia mengakhiri program. Dalam kasus `None`, kita tidak akan mengembalikan nilai dari `unwrap`, jadi kode ini valid.

Satu ekspresi terakhir yang bertipe `!` adalah loop:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-10-loop-returns-never/src/main.rs:here}}
```

Di sini, loop tidak pernah berakhir, jadi `!` adalah nilai dari ekspresi itu. Akan tetapi, hal itu tidak berlaku jika kita menyertakan `break`, karena loop akan berhenti saat mencapai `break`.

<a id="dynamically-sized-types-and-the-sized-trait"></a>
### Tipe yang Ukurannya Ditentukan Saat Runtime dan Trait `Sized`

Rust perlu mengetahui detail tertentu tentang tipe-tipenya, seperti berapa banyak ruang yang harus dialokasikan untuk sebuah nilai dari tipe tertentu. Hal ini membuat satu sudut dari sistem tipenya agak membingungkan pada awalnya: konsep _tipe yang ukurannya ditentukan saat runtime_. Kadang disebut _DST_ atau _tipe tanpa ukuran_, tipe-tipe ini memungkinkan kita menulis kode dengan nilai yang ukurannya hanya bisa kita ketahui saat runtime.

Mari kita dalami detail dari sebuah tipe yang ukurannya ditentukan saat runtime bernama `str`, yang sudah kita pakai sepanjang buku ini. Benar, bukan `&str`, melainkan `str` sendirian adalah sebuah DST. Dalam banyak kasus, seperti saat menyimpan teks yang dimasukkan pengguna, kita tidak bisa tahu seberapa panjang string itu sampai runtime. Itu berarti kita tidak bisa membuat variabel bertipe `str`, juga tidak bisa menerima argumen bertipe `str`. Perhatikan kode berikut, yang tidak bekerja:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-11-cant-create-str/src/main.rs:here}}
```

Rust perlu tahu berapa banyak memori yang harus dialokasikan untuk nilai apa pun dari tipe tertentu, dan semua nilai dari sebuah tipe harus memakai jumlah memori yang sama. Jika Rust mengizinkan kita menulis kode ini, kedua nilai `str` itu perlu menempati ruang yang sama. Tetapi panjangnya berbeda: `s1` butuh 12 byte penyimpanan dan `s2` butuh 15. Inilah alasan mengapa tidak mungkin membuat variabel yang menampung tipe yang ukurannya ditentukan saat runtime.

Jadi, apa yang kita lakukan? Dalam hal ini, kamu sudah tahu jawabannya: Kita buat tipe `s1` dan `s2` menjadi string slice (`&str`) alih-alih `str`. Ingat dari bagian [“String Slice”][string-slices]<!-- ignore --> di Bab 4 bahwa struktur data slice hanya menyimpan posisi awal dan panjang slice. Jadi, meskipun `&T` adalah satu nilai yang menyimpan alamat memori tempat `T` berada, string slice adalah _dua_ nilai: alamat dari `str` dan panjangnya. Dengan demikian, kita bisa mengetahui ukuran nilai string slice saat compile time: besarnya dua kali panjang `usize`. Artinya, kita selalu tahu ukuran string slice, tidak peduli seberapa panjang string yang ditunjuknya. Secara umum, beginilah cara tipe yang ukurannya ditentukan saat runtime dipakai di Rust: Mereka punya metadata tambahan yang menyimpan ukuran informasi dinamisnya. Aturan emas tipe yang ukurannya ditentukan saat runtime adalah kita harus selalu menaruh nilainya di belakang semacam pointer.

Kita bisa menggabungkan `str` dengan berbagai macam pointer: misalnya, `Box<str>` atau `Rc<str>`. Faktanya, kamu sudah pernah melihat ini sebelumnya tetapi dengan tipe yang ukurannya ditentukan saat runtime yang berbeda: trait. Setiap trait adalah tipe yang ukurannya ditentukan saat runtime yang bisa kita rujuk dengan memakai nama trait itu. Di bagian [“Memakai Trait Object untuk Berabstraksi atas Perilaku Bersama”][using-trait-objects-to-abstract-over-shared-behavior]<!-- ignore --> di Bab 18, kita menyebutkan bahwa untuk memakai trait sebagai trait object, kita harus menaruhnya di belakang pointer, seperti `&dyn Trait` atau `Box<dyn Trait>` (`Rc<dyn Trait>` juga bisa).

Untuk bekerja dengan DST, Rust menyediakan trait `Sized` guna menentukan apakah ukuran sebuah tipe diketahui saat compile time atau tidak. Trait ini otomatis diimplementasikan untuk apa pun yang ukurannya diketahui saat compile time. Selain itu, Rust secara implisit menambahkan bound `Sized` pada setiap fungsi generic. Artinya, definisi fungsi generic seperti ini:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-12-generic-fn-definition/src/lib.rs}}
```

sebenarnya diperlakukan seolah-olah kita menulis ini:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-13-generic-implicit-sized-bound/src/lib.rs}}
```

Secara default, fungsi generic hanya bekerja pada tipe yang ukurannya diketahui saat compile time. Akan tetapi, kamu bisa memakai sintaks khusus berikut untuk melonggarkan pembatasan itu:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-14-generic-maybe-sized/src/lib.rs}}
```

Sebuah trait bound pada `?Sized` berarti “`T` boleh `Sized` atau tidak,” dan notasi ini menggantikan aturan default bahwa tipe generic harus punya ukuran yang diketahui saat compile time. Sintaks `?Trait` dengan makna ini hanya tersedia untuk `Sized`, bukan untuk trait lain.

Perhatikan juga bahwa kita mengganti tipe parameter `t` dari `T` menjadi `&T`. Karena tipe itu mungkin tidak `Sized`, kita perlu memakainya di belakang semacam pointer. Dalam hal ini, kita memilih reference.

Berikutnya, kita akan membahas fungsi dan closure!

[encapsulation-that-hides-implementation-details]: ch18-01-what-is-oo.html#encapsulation-that-hides-implementation-details
[string-slices]: ch04-03-slices.html#string-slices
[the-match-control-flow-construct]: ch06-02-match.html#the-match-control-flow-construct
[using-trait-objects-to-abstract-over-shared-behavior]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern
