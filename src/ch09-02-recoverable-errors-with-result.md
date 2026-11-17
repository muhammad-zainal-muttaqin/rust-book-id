## Error yang Bisa Dipulihkan dengan `Result`

Kebanyakan error tidak cukup serius sampai harus menghentikan program secara
keseluruhan. Kadang, saat sebuah fungsi gagal, penyebabnya bisa kamu mengerti
dan tangani dengan mudah. Misalnya, jika kamu mencoba membuka sebuah file dan
operasi itu gagal karena file-nya tidak ada, kamu mungkin ingin membuat filenya
alih-alih menghentikan proses.

Ingat dari [“Menangani Kemungkinan Kegagalan dengan `Result`”][handle_failure]<!--
ignore --> di Bab 2 bahwa enum `Result` didefinisikan dengan dua varian, `Ok` dan
`Err`, seperti berikut:

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

`T` dan `E` adalah parameter tipe generik: Kita akan membahas generic lebih
detail di Bab 10. Yang perlu kamu tahu sekarang adalah `T` mewakili tipe nilai
yang akan dikembalikan dalam kasus sukses di dalam varian `Ok`, dan `E` mewakili
tipe error yang akan dikembalikan dalam kasus gagal di dalam varian `Err`.
Karena `Result` punya parameter tipe generik ini, kita bisa memakai tipe `Result`
dan fungsi-fungsi yang didefinisikan di atasnya dalam banyak situasi berbeda,
di mana nilai sukses dan nilai error yang ingin kita kembalikan bisa berbeda.

Mari kita panggil sebuah fungsi yang mengembalikan nilai `Result`, karena fungsi
itu bisa saja gagal. Pada Listing 9-3, kita mencoba membuka sebuah file.

<Listing number="9-3" file-name="src/main.rs" caption="Membuka sebuah file">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-03/src/main.rs}}
```

</Listing>

Tipe kembalian dari `File::open` adalah `Result<T, E>`. Parameter generik `T`
sudah diisi oleh implementasi `File::open` dengan tipe nilai sukses,
`std::fs::File`, yang merupakan sebuah handle file. Tipe `E` yang dipakai dalam
nilai error adalah `std::io::Error`. Tipe kembalian ini berarti pemanggilan
`File::open` bisa berhasil dan mengembalikan handle file yang bisa kita baca atau
tulis. Pemanggilan fungsi itu juga bisa gagal: misalnya, file-nya mungkin tidak
ada, atau kita mungkin tidak punya izin untuk mengaksesnya. Fungsi `File::open`
perlu punya cara untuk memberi tahu kita apakah pemanggilan itu berhasil atau
gagal, dan sekaligus memberi kita handle file atau informasi error. Informasi
itulah yang justru disampaikan oleh enum `Result`.

Pada kasus saat `File::open` berhasil, nilai di dalam variabel
`greeting_file_result` akan berupa sebuah instance `Ok` yang berisi handle file.
Pada kasus saat gagal, nilai di `greeting_file_result` akan berupa sebuah
instance `Err` yang berisi informasi lebih lanjut tentang jenis error yang
terjadi.

Kita perlu menambahkan kode pada Listing 9-3 untuk mengambil tindakan yang
berbeda bergantung pada nilai yang dikembalikan `File::open`. Listing 9-4
menunjukkan satu cara menangani `Result` memakai alat dasar, yaitu ekspresi
`match` yang sudah kita bahas di Bab 6.

<Listing number="9-4" file-name="src/main.rs" caption="Memakai ekspresi `match` untuk menangani varian `Result` yang mungkin dikembalikan">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-04/src/main.rs}}
```

</Listing>

Perhatikan bahwa, seperti enum `Option`, enum `Result` dan varian-variannya sudah
dimasukkan ke dalam scope oleh prelude, jadi kita tidak perlu menuliskan
`Result::` sebelum varian `Ok` dan `Err` di cabang-cabang `match`.

Saat hasilnya `Ok`, kode ini akan mengembalikan nilai `file` di dalam varian
`Ok`, lalu kita menetapkan nilai handle file itu ke variabel `greeting_file`.
Setelah `match`, kita bisa memakai handle file tersebut untuk membaca atau
menulis.

Cabang `match` yang lain menangani kasus saat kita mendapat nilai `Err` dari
`File::open`. Pada contoh ini, kita memilih untuk memanggil macro `panic!`. Jika
tidak ada file bernama _hello.txt_ di direktori saat ini dan kita menjalankan
kode ini, kita akan melihat keluaran berikut dari macro `panic!`:

```console
{{#include ../listings/ch09-error-handling/listing-09-04/output.txt}}
```

Seperti biasa, keluaran ini memberi tahu kita dengan tepat apa yang salah.

### Mencocokkan Berbagai Jenis Error

Kode di Listing 9-4 akan `panic!` tidak peduli mengapa `File::open` gagal.
Namun, kita ingin mengambil tindakan berbeda untuk alasan kegagalan yang
berbeda. Jika `File::open` gagal karena file-nya tidak ada, kita ingin membuat
filenya dan mengembalikan handle ke file baru itu. Jika `File::open` gagal karena
alasan lain—misalnya karena kita tidak punya izin untuk membuka file-nya—kita
tetap ingin kode-nya `panic!` dengan cara yang sama seperti di Listing 9-4. Untuk
itu, kita menambahkan ekspresi `match` di dalam, seperti yang ditunjukkan Listing
9-5.

<Listing number="9-5" file-name="src/main.rs" caption="Menangani berbagai jenis error dengan cara yang berbeda">

<!-- ignore this test because otherwise it creates hello.txt which causes other
tests to fail lol -->

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-05/src/main.rs}}
```

</Listing>

Tipe nilai yang dikembalikan `File::open` di dalam varian `Err` adalah
`io::Error`, sebuah struct yang disediakan oleh standard library. Struct ini
punya sebuah method, `kind`, yang bisa kita panggil untuk mendapatkan nilai
`io::ErrorKind`. Enum `io::ErrorKind` disediakan oleh standard library dan
mempunyai varian-varian yang mewakili berbagai jenis error yang mungkin
dihasilkan oleh operasi `io`. Varian yang ingin kita pakai adalah
`ErrorKind::NotFound`, yang menandakan file yang ingin kita buka belum ada.
Jadi, kita mencocokkan `greeting_file_result`, tetapi kita juga punya `match` di
dalam untuk `error.kind()`.

Kondisi yang ingin kita cek di `match` dalam adalah apakah nilai yang
dikembalikan oleh `error.kind()` adalah varian `NotFound` dari enum
`ErrorKind`. Jika ya, kita mencoba membuat filenya dengan `File::create`.
Namun, karena `File::create` juga bisa gagal, kita butuh cabang kedua dalam
ekspresi `match` dalam itu. Saat file tidak bisa dibuat, pesan error yang
berbeda akan dicetak. Cabang kedua dari `match` luar tetap sama, sehingga
program melakukan panic pada error apa pun selain error file tidak ditemukan.

> #### Alternatif Memakai `match` dengan `Result<T, E>`
>
> Itu `match` yang cukup banyak! Ekspresi `match` sangat berguna, tetapi juga
> tergolong primitif. Di Bab 13, kamu akan belajar tentang closure, yang dipakai
> bersama banyak method yang didefinisikan pada `Result<T, E>`. Method-method ini
> bisa lebih ringkas daripada memakai `match` saat menangani nilai `Result<T, E>`
> dalam kode kamu.
>
> Misalnya, ini cara lain untuk menulis logika yang sama seperti di Listing 9-5,
> kali ini memakai closure dan method `unwrap_or_else`:
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore
> use std::fs::File;
> use std::io::ErrorKind;
>
> fn main() {
>     let greeting_file = File::open("hello.txt").unwrap_or_else(|error| {
>         if error.kind() == ErrorKind::NotFound {
>             File::create("hello.txt").unwrap_or_else(|error| {
>                 panic!("Problem creating the file: {error:?}");
>             })
>         } else {
>             panic!("Problem opening the file: {error:?}");
>         }
>     });
> }
> ```
>
> Meski kode ini punya perilaku yang sama dengan Listing 9-5, kode ini tidak
> memuat ekspresi `match` apa pun dan lebih bersih dibaca. Kembali ke contoh ini
> setelah kamu membaca Bab 13 dan lihat method `unwrap_or_else` dalam dokumentasi
> standard library. Masih banyak method lain seperti ini yang bisa merapikan
> ekspresi `match` bertingkat yang besar saat kamu menangani error.

<!-- Old headings. Do not remove or links may break. -->

<a id="shortcuts-for-panic-on-error-unwrap-and-expect"></a>

#### Jalan Pintas untuk Panic saat Error

Memakai `match` sudah cukup baik, tetapi bisa agak panjang dan tidak selalu
menyampaikan maksud dengan jelas. Tipe `Result<T, E>` punya banyak method
pembantu yang didefinisikan di atasnya untuk melakukan berbagai tugas yang lebih
spesifik. Method `unwrap` adalah method jalan pintas yang diimplementasikan
persis seperti ekspresi `match` yang kita tulis di Listing 9-4. Jika nilai
`Result` adalah varian `Ok`, `unwrap` akan mengembalikan nilai di dalam `Ok`.
Jika `Result` adalah varian `Err`, `unwrap` akan memanggil macro `panic!` untuk
kita. Berikut contoh `unwrap` dalam aksi:

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-04-unwrap/src/main.rs}}
```

</Listing>

Jika kita menjalankan kode ini tanpa file _hello.txt_, kita akan melihat pesan
error dari pemanggilan `panic!` yang dilakukan method `unwrap`:

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-04-unwrap
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:4:49:
called `Result::unwrap()` on an `Err` value: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

Demikian pula, method `expect` memungkinkan kita juga memilih pesan error
`panic!`. Memakai `expect` alih-alih `unwrap` serta memberikan pesan error yang
bagus bisa menyampaikan maksud kamu dan memudahkan pelacakan sumber panic.
Sintaks `expect` terlihat seperti ini:

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-05-expect/src/main.rs}}
```

</Listing>

Kita memakai `expect` dengan cara yang sama seperti `unwrap`: untuk
mengembalikan handle file atau memanggil macro `panic!`. Pesan error yang dipakai
`expect` dalam pemanggilan `panic!`-nya akan berupa parameter yang kita berikan
ke `expect`, alih-alih pesan `panic!` bawaan yang dipakai `unwrap`. Berikut
tampilannya:

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-05-expect
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:5:10:
hello.txt should be included in this project: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

Pada kode siap produksi, kebanyakan Rustacean memilih `expect` daripada `unwrap`
dan memberikan lebih banyak konteks tentang mengapa suatu operasi diharapkan
selalu berhasil. Dengan begitu, jika asumsi kamu ternyata salah, kamu punya
lebih banyak informasi untuk dipakai saat melakukan debug.

### Menyebarkan Error

Saat implementasi sebuah fungsi memanggil sesuatu yang bisa gagal, alih-alih
menangani error itu di dalam fungsi tersebut, kamu bisa mengembalikan error itu
ke kode pemanggil agar kode itulah yang memutuskan apa yang harus dilakukan.
Ini dikenal dengan _menyebarkan_ error dan memberi lebih banyak kendali kepada
kode pemanggil, di mana mungkin ada lebih banyak informasi atau logika yang
menentukan bagaimana error sebaiknya ditangani daripada yang tersedia dalam
konteks kode kamu.

Misalnya, Listing 9-6 menunjukkan sebuah fungsi yang membaca nama pengguna dari
sebuah file. Jika file-nya tidak ada atau tidak bisa dibaca, fungsi ini akan
mengembalikan error-error itu ke kode yang memanggil fungsi tersebut.

<Listing number="9-6" file-name="src/main.rs" caption="Sebuah fungsi yang mengembalikan error ke kode pemanggil memakai `match`">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-06/src/main.rs:here}}
```

</Listing>

Fungsi ini bisa ditulis dengan jauh lebih pendek, tetapi kita akan mulai dengan
melakukan banyak hal secara manual untuk menjelajahi penanganan error; pada
akhirnya, kita akan menunjukkan cara yang lebih pendek. Mari kita lihat dulu
tipe kembalian fungsinya: `Result<String, io::Error>`. Ini berarti fungsi itu
mengembalikan nilai bertipe `Result<T, E>`, di mana parameter generik `T` sudah
diisi dengan tipe konkret `String` dan parameter tipe generik `E` sudah diisi
dengan tipe konkret `io::Error`.

Jika fungsi ini berhasil tanpa masalah, kode yang memanggil fungsi ini akan
menerima nilai `Ok` yang berisi sebuah `String`—`username` yang dibaca fungsi ini
dari file. Jika fungsi ini mengalami masalah, kode pemanggil akan menerima nilai
`Err` yang berisi sebuah instance `io::Error` dengan informasi lebih lanjut
tentang masalahnya. Kita memilih `io::Error` sebagai tipe kembalian fungsi ini
karena kebetulan itulah tipe nilai error yang dikembalikan oleh kedua operasi
yang kita panggil dalam tubuh fungsi ini dan bisa gagal: fungsi `File::open` dan
method `read_to_string`.

Tubuh fungsi dimulai dengan memanggil fungsi `File::open`. Lalu, kita menangani
nilai `Result` dengan `match` yang mirip dengan `match` di Listing 9-4. Jika
`File::open` berhasil, handle file dalam variabel pattern `file` menjadi nilai di
variabel mutable `username_file`, dan fungsi pun berlanjut. Pada kasus `Err`,
alih-alih memanggil `panic!`, kita memakai keyword `return` untuk kembali lebih
awal dari seluruh fungsi dan meneruskan nilai error dari `File::open`, yang kini
ada di variabel pattern `e`, kembali ke kode pemanggil sebagai nilai error fungsi
ini.

Jadi, jika kita punya handle file di `username_file`, fungsi lalu membuat `String`
baru di variabel `username` dan memanggil method `read_to_string` pada handle
file di `username_file` untuk membaca isi file ke dalam `username`. Method
`read_to_string` juga mengembalikan `Result` karena bisa gagal, meskipun
`File::open` sudah berhasil. Jadi, kita butuh `match` lain untuk menangani
`Result` itu: Jika `read_to_string` berhasil, maka fungsi kita berhasil, dan kita
mengembalikan username dari file yang sekarang ada di `username` dalam bungkus
`Ok`. Jika `read_to_string` gagal, kita mengembalikan nilai error dengan cara
yang sama seperti kita mengembalikan nilai error pada `match` yang menangani
kembalian `File::open`. Namun, kita tidak perlu secara eksplisit menuliskan
`return`, karena ini adalah ekspresi terakhir dalam fungsi.

Kode yang memanggil kode ini lalu akan menangani apakah ia mendapat nilai `Ok`
yang berisi username atau nilai `Err` yang berisi `io::Error`. Terserah kode
pemanggil untuk memutuskan apa yang harus dilakukan dengan nilai-nilai itu. Jika
kode pemanggil mendapat nilai `Err`, kode itu bisa memanggil `panic!` dan
meng crash program, memakai username bawaan, atau mencari username dari tempat
lain selain file, misalnya. Kita tidak punya cukup informasi tentang apa yang
sebenarnya sedang dilakukan kode pemanggil, jadi kita menyebarkan semua
informasi sukses atau error ke atas agar kode itulah yang menangani dengan
tepat.

Pola penyebaran error ini sangat umum di Rust, sampai-sampai Rust menyediakan
operator tanya `?` untuk memudahkannya.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-shortcut-for-propagating-errors-the--operator"></a>

#### Jalan Pintas Operator `?` untuk Menyebarkan Error

Listing 9-7 menunjukkan implementasi `read_username_from_file` yang punya
fungsionalitas sama seperti di Listing 9-6, tetapi implementasi ini memakai
operator `?`.

<Listing number="9-7" file-name="src/main.rs" caption="Sebuah fungsi yang mengembalikan error ke kode pemanggil memakai operator `?`">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-07/src/main.rs:here}}
```

</Listing>

`?` yang ditempatkan setelah nilai `Result` didefinisikan untuk bekerja hampir
sama seperti ekspresi `match` yang kita buat untuk menangani nilai `Result` di
Listing 9-6. Jika nilai `Result` adalah `Ok`, nilai di dalam `Ok` akan
dikembalikan dari ekspresi ini, dan program pun berlanjut. Jika nilainya `Err`,
maka `Err` akan dikembalikan dari seluruh fungsi seolah-olah kita memakai keyword
`return`, sehingga nilai error tersebut tersebar ke kode pemanggil.

Ada perbedaan antara apa yang dilakukan ekspresi `match` di Listing 9-6 dan apa
yang dilakukan operator `?`: Nilai error yang dikenai operator `?` melewati
fungsi `from`, yang didefinisikan dalam trait `From` di standard library dan
dipakai untuk mengonversi nilai dari satu tipe ke tipe lain. Saat operator `?`
memanggil fungsi `from`, tipe error yang diterima dikonversi menjadi tipe error
yang didefinisikan dalam tipe kembalian fungsi saat ini. Ini berguna saat sebuah
fungsi mengembalikan satu tipe error untuk mewakili semua cara fungsi itu bisa
gagal, meskipun bagian-bagian tertentu bisa gagal karena banyak alasan berbeda.

Misalnya, kita bisa mengubah fungsi `read_username_from_file` di Listing 9-7
agar mengembalikan tipe error kustom bernama `OurError` yang kita definisikan.
Jika kita juga mendefinisikan `impl From<io::Error> for OurError` untuk
membangun sebuah instance `OurError` dari sebuah `io::Error`, maka pemanggilan
operator `?` dalam tubuh `read_username_from_file` akan memanggil `from` dan
mengonversi tipe-tipe error tanpa perlu menambah kode apa pun ke dalam fungsi.

Dalam konteks Listing 9-7, `?` di akhir pemanggilan `File::open` akan
mengembalikan nilai di dalam `Ok` ke variabel `username_file`. Jika terjadi
error, operator `?` akan kembali lebih awal dari seluruh fungsi dan memberikan
nilai `Err` apa pun ke kode pemanggil. Hal yang sama berlaku untuk `?` di akhir
pemanggilan `read_to_string`.

Operator `?` menghilangkan banyak boilerplate dan membuat implementasi fungsi ini
lebih sederhana. Kita bahkan bisa mempersingkat kode ini lebih jauh dengan
merangkai pemanggilan method tepat setelah `?`, seperti yang ditunjukkan Listing
9-8.

<Listing number="9-8" file-name="src/main.rs" caption="Merangkai pemanggilan method setelah operator `?`">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-08/src/main.rs:here}}
```

</Listing>

Kita memindahkan pembuatan `String` baru di `username` ke awal fungsi; bagian itu
tidak berubah. Alih-alih membuat variabel `username_file`, kita merangkai
pemanggilan `read_to_string` langsung ke hasil dari `File::open("hello.txt")?`.
Kita tetap punya `?` di akhir pemanggilan `read_to_string`, dan kita tetap
mengembalikan nilai `Ok` yang berisi `username` saat `File::open` dan
`read_to_string` keduanya berhasil alih-alih mengembalikan error. Fungsionalitasnya
sekali lagi sama seperti di Listing 9-6 dan Listing 9-7; ini hanya cara lain yang
lebih ergonomis untuk menuliskannya.

Listing 9-9 menunjukkan cara membuat ini bahkan lebih pendek dengan memakai
`fs::read_to_string`.

<Listing number="9-9" file-name="src/main.rs" caption="Memakai `fs::read_to_string` alih-alih membuka lalu membaca file">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-09/src/main.rs:here}}
```

</Listing>

Membaca sebuah file ke dalam string adalah operasi yang cukup umum, sehingga
standard library menyediakan fungsi `fs::read_to_string` yang praktis, yang
membuka file, membuat `String` baru, membaca isi file, memasukkan isinya ke
dalam `String` itu, dan mengembalikannya. Tentu saja, memakai `fs::read_to_string`
tidak memberi kita kesempatan untuk menjelaskan semua penanganan error, itulah
sebabnya kita melakukannya dengan cara panjang terlebih dahulu.

<!-- Old headings. Do not remove or links may break. -->

<a id="where-the--operator-can-be-used"></a>

#### Di Mana Operator `?` Bisa Dipakai

Operator `?` hanya bisa dipakai dalam fungsi yang tipe kembaliannya kompatibel
dengan nilai yang dikenai `?`. Ini karena operator `?` didefinisikan untuk
melakukan pengembalian awal sebuah nilai dari fungsi, dengan cara yang sama
seperti ekspresi `match` yang kita buat di Listing 9-6. Di Listing 9-6, `match`
memakai nilai `Result`, dan cabang pengembalian awalnya mengembalikan nilai
`Err(e)`. Tipe kembalian fungsi haruslah sebuah `Result` agar kompatibel dengan
`return` ini.

Di Listing 9-10, mari kita lihat error yang akan kita dapatkan jika memakai
operator `?` dalam fungsi `main` dengan tipe kembalian yang tidak kompatibel
dengan tipe nilai yang kita kenai `?`.

<Listing number="9-10" file-name="src/main.rs" caption="Mencoba memakai `?` dalam fungsi `main` yang mengembalikan `()` tidak akan terkompilasi.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-10/src/main.rs}}
```

</Listing>

Kode ini membuka sebuah file, yang bisa saja gagal. Operator `?` mengikuti nilai
`Result` yang dikembalikan `File::open`, tetapi fungsi `main` ini punya tipe
kembalian `()`, bukan `Result`. Saat kita mengompilasi kode ini, kita mendapat
pesan error berikut:

```console
{{#include ../listings/ch09-error-handling/listing-09-10/output.txt}}
```

Error ini menunjukkan bahwa kita hanya boleh memakai operator `?` dalam fungsi
yang mengembalikan `Result`, `Option`, atau tipe lain yang mengimplementasikan
`FromResidual`.

Untuk memperbaiki error itu, kamu punya dua pilihan. Salah satu pilihannya adalah
mengubah tipe kembalian fungsimu agar kompatibel dengan nilai yang kamu kenai
operator `?`, selama tidak ada pembatasan yang melarangnya. Pilihan lainnya
adalah memakai `match` atau salah satu method `Result<T, E>` untuk menangani
`Result<T, E>` dengan cara yang sesuai.

Pesan error itu juga menyebutkan bahwa `?` bisa dipakai dengan nilai `Option<T>`
juga. Sama seperti memakai `?` pada `Result`, kamu hanya bisa memakai `?` pada
`Option` dalam fungsi yang mengembalikan `Option`. Perilaku operator `?` saat
dipakai pada `Option<T>` mirip dengan perilakunya saat dipakai pada `Result<T, E>`:
Jika nilainya `None`, maka `None` akan dikembalikan lebih awal dari fungsi pada
titik itu. Jika nilainya `Some`, nilai di dalam `Some` adalah nilai hasil dari
ekspresi tersebut, dan fungsi pun berlanjut. Listing 9-11 punya contoh fungsi yang
mencari karakter terakhir dari baris pertama dalam teks yang diberikan.

<Listing number="9-11" caption="Memakai operator `?` pada nilai `Option<T>`">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-11/src/main.rs:here}}
```

</Listing>

Fungsi ini mengembalikan `Option<char>` karena memungkinkan ada karakter di sana,
tetapi juga memungkinkan tidak ada. Kode ini mengambil argumen string slice
`text` dan memanggil method `lines` padanya, yang mengembalikan sebuah iterator
atas baris-baris dalam string. Karena fungsi ini ingin memeriksa baris pertama,
fungsi memanggil `next` pada iterator itu untuk mendapatkan nilai pertama darinya.
Jika `text` adalah string kosong, pemanggilan `next` ini akan mengembalikan
`None`, dan dalam hal itu kita memakai `?` untuk berhenti dan mengembalikan `None`
dari `last_char_of_first_line`. Jika `text` bukan string kosong, `next` akan
mengembalikan nilai `Some` yang berisi string slice dari baris pertama dalam
`text`.

`?` mengekstrak string slice itu, dan kita bisa memanggil `chars` pada string
slice tersebut untuk mendapatkan iterator atas karakter-karakterannya. Kita
tertarik pada karakter terakhir di baris pertama ini, jadi kita memanggil `last`
untuk mengembalikan item terakhir dalam iterator. Ini adalah `Option` karena
memungkinkan baris pertama adalah string kosong; misalnya, jika `text` diawali
dengan baris kosong tetapi punya karakter di baris lain, seperti `"\nhi"`.
Namun, jika ada karakter terakhir di baris pertama, karakter itu akan
dikembalikan dalam varian `Some`. Operator `?` di tengah memberi kita cara ringkas
untuk menyatakan logika ini, memungkinkan kita mengimplementasikan fungsi dalam
satu baris. Seandainya kita tidak bisa memakai operator `?` pada `Option`, kita
harus mengimplementasikan logika ini dengan lebih banyak pemanggilan method atau
sebuah ekspresi `match`.

Perhatikan bahwa kamu bisa memakai operator `?` pada sebuah `Result` dalam fungsi
yang mengembalikan `Result`, dan kamu bisa memakai operator `?` pada sebuah
`Option` dalam fungsi yang mengembalikan `Option`, tetapi kamu tidak bisa
mencampur-adukkannya. Operator `?` tidak akan otomatis mengonversi `Result` menjadi
`Option` atau sebaliknya; dalam kasus seperti itu, kamu bisa memakai method
seperti method `ok` pada `Result` atau method `ok_or` pada `Option` untuk melakukan
konversi secara eksplisit.

Sejauh ini, semua fungsi `main` yang kita pakai mengembalikan `()`. Fungsi `main`
bersifat khusus karena merupakan titik masuk dan titik keluar dari sebuah program
yang dapat dijalankan, dan ada batasan tentang apa yang boleh menjadi tipe
kembaliannya agar program berperilaku seperti yang diharapkan.

Untungnya, `main` juga bisa mengembalikan `Result<(), E>`. Listing 9-12 memuat kode
dari Listing 9-10, tetapi kita sudah mengubah tipe kembalian `main` menjadi
`Result<(), Box<dyn Error>>` dan menambahkan nilai kembalian `Ok(())` di akhir.
Kode ini sekarang akan terkompilasi.

<Listing number="9-12" file-name="src/main.rs" caption="Mengubah `main` agar mengembalikan `Result<(), E>` membolehkan pemakaian operator `?` pada nilai `Result`.">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-12/src/main.rs}}
```

</Listing>

Tipe `Box<dyn Error>` adalah sebuah trait object, yang akan kita bahas dalam
[“Memakai Trait Object untuk Abstraksi atas Perilaku Bersama”][trait-objects]<!-- ignore -->
di Bab 18. Untuk sementara, kamu bisa membaca `Box<dyn Error>` sebagai “jenis error
apa pun.” Memakai `?` pada nilai `Result` dalam fungsi `main` dengan tipe error
`Box<dyn Error>` dibolehkan karena tipe itu membolehkan nilai `Err` apa pun
dikembalikan lebih awal. Meskipun tubuh fungsi `main` ini hanya akan pernah
mengembalikan error bertipe `std::io::Error`, dengan menentukan `Box<dyn Error>`,
tanda tangan ini akan tetap benar bahkan jika lebih banyak kode yang mengembalikan
error lain ditambahkan ke tubuh `main`.

Saat sebuah fungsi `main` mengembalikan `Result<(), E>`, program yang dapat
dijalankan akan keluar dengan nilai `0` jika `main` mengembalikan `Ok(())` dan akan
keluar dengan nilai bukan nol jika `main` mengembalikan nilai `Err`. Program yang
dapat dijalankan yang ditulis dalam C mengembalikan bilangan bulat saat keluar:
Program yang keluar dengan sukses mengembalikan bilangan bulat `0`, dan program
yang mengalami error mengembalikan bilangan bulat selain `0`. Rust juga
mengembalikan bilangan bulat dari program yang dapat dijalankan agar kompatibel
dengan konvensi ini.

Fungsi `main` boleh mengembalikan tipe apa pun yang mengimplementasikan [trait
`std::process::Termination`][termination]<!-- ignore -->, yang memuat sebuah fungsi
`report` yang mengembalikan `ExitCode`. Konsultasikan dokumentasi standard library
untuk informasi lebih lanjut tentang mengimplementasikan trait `Termination` bagi
tipe-tipe kamu sendiri.

Sekarang setelah kita membahas detail tentang memanggil `panic!` atau
mengembalikan `Result`, mari kita kembali ke topik tentang cara memutuskan mana
yang tepat dipakai dalam kasus yang mana.

[handle_failure]: ch02-00-guessing-game-tutorial.html#handling-potential-failure-with-result
[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[termination]: ../std/process/trait.Termination.html
