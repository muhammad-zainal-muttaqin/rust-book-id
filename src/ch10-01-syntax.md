## Tipe Data Generic

Kita memakai generic untuk membuat definisi bagi item seperti tanda tangan fungsi
atau struct, yang kemudian bisa kita pakai dengan banyak tipe data konkret yang
berbeda. Mari kita lihat dulu cara mendefinisikan fungsi, struct, enum, dan
method menggunakan generic. Setelah itu, kita akan membahas bagaimana generic
memengaruhi performa kode.

### Di Dalam Definisi Fungsi

Saat mendefinisikan fungsi yang memakai generic, kita menaruh generic di tanda
tangan fungsi, tepat di tempat yang biasa kita pakai untuk menentukan tipe data
parameter dan nilai kembalian. Dengan begitu, kode kita jadi lebih fleksibel dan
memberi lebih banyak kemampuan kepada siapa pun yang memanggil fungsi tersebut,
sekaligus mencegah duplikasi kode.

Melanjutkan fungsi `largest` kita, Listing 10-4 menampilkan dua fungsi yang sama-sama
mencari nilai terbesar dalam sebuah slice. Setelah itu, kita akan menggabungkan
keduanya menjadi satu fungsi yang memakai generic.

<Listing number="10-4" file-name="src/main.rs" caption="Dua fungsi yang hanya berbeda pada nama dan pada tipe di tanda tangannya">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-04/src/main.rs:here}}
```

</Listing>

Fungsi `largest_i32` adalah fungsi yang kita ekstrak di Listing 10-3 untuk mencari
`i32` terbesar dalam sebuah slice. Fungsi `largest_char` mencari `char` terbesar
dalam sebuah slice. Isi kedua fungsi itu sama, jadi mari kita hilangkan duplikasi
dengan memperkenalkan parameter tipe generic dalam satu fungsi.

Untuk memparameterisasi tipe dalam satu fungsi baru, kita perlu memberi nama pada
parameter tipe itu, sama seperti yang kita lakukan pada parameter nilai fungsi.
Kamu bisa memakai identifier apa pun sebagai nama parameter tipe. Namun kita akan
memakai `T` karena, sesuai konvensi, nama parameter tipe di Rust itu pendek, sering
kali hanya satu huruf, dan konvensi penamaan tipe Rust memakai UpperCamelCase.
Karena `T` adalah kependekan dari _type_, itulah pilihan default kebanyakan
programmer Rust.

Saat kita memakai sebuah parameter di dalam isi fungsi, kita harus mendeklarasikan
nama parameter itu di tanda tangan agar compiler tahu apa arti nama tersebut.
Begitu pula saat kita memakai nama parameter tipe di tanda tangan fungsi, kita harus
mendeklarasikan nama parameter tipe itu sebelum memakainya. Untuk mendefinisikan
fungsi `largest` yang generic, kita menaruh deklarasi nama tipe di dalam tanda
kurung sudut, `<>`, antara nama fungsi dan daftar parameter, seperti ini:

```rust,ignore
fn largest<T>(list: &[T]) -> &T {
```

Kita membaca definisi ini sebagai “Fungsi `largest` bersifat generic untuk suatu
tipe `T`.” Fungsi ini punya satu parameter bernama `list`, yaitu slice dari nilai-
nilai bertipe `T`. Fungsi `largest` akan mengembalikan reference ke sebuah nilai
dengan tipe `T` yang sama.

Listing 10-5 menampilkan definisi fungsi `largest` gabungan yang memakai tipe data
generic di tanda tangannya. Listing itu juga menunjukkan cara kita bisa memanggil
fungsi tersebut dengan slice berisi nilai `i32` maupun nilai `char`. Perhatikan
bahwa kode ini belum bisa dikompilasi.

<Listing number="10-5" file-name="src/main.rs" caption="Fungsi `largest` yang memakai parameter tipe generic; ini belum bisa dikompilasi">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/src/main.rs}}
```

</Listing>

Jika kita mengompilasi kode ini sekarang, kita akan mendapat error ini:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/output.txt}}
```

Teks bantuan menyebut `std::cmp::PartialOrd`, yang merupakan sebuah trait, dan kita
akan membahas trait di bagian berikutnya. Untuk sementara, ketahuilah bahwa error
ini menyatakan isi fungsi `largest` tidak akan bekerja untuk semua tipe yang mungkin
dipakai `T`. Karena kita ingin membandingkan nilai bertipe `T` di dalam isi fungsi,
kita hanya bisa memakai tipe-tipe yang nilainya bisa diurutkan. Untuk mengaktifkan
perbandingan, pustaka standar menyediakan trait `std::cmp::PartialOrd` yang bisa
kamu implementasikan pada tipe-tipe (lihat Lampiran C untuk penjelasan lebih lanjut
tentang trait ini). Untuk memperbaiki Listing 10-5, kita bisa mengikuti saran dari
teks bantuan dan membatasi tipe yang sah untuk `T` hanya pada tipe-tipe yang
mengimplementasikan `PartialOrd`. Listing itu lalu akan bisa dikompilasi, karena
pustaka standar mengimplementasikan `PartialOrd` pada `i32` maupun `char`.

### Di Dalam Definisi Struct

Kita juga bisa mendefinisikan struct agar memakai parameter tipe generic pada satu
atau lebih field dengan sintaks `<>`. Listing 10-6 mendefinisikan struct `Point<T>`
untuk menyimpan nilai koordinat `x` dan `y` dari tipe apa pun.

<Listing number="10-6" file-name="src/main.rs" caption="Struct `Point<T>` yang menyimpan nilai `x` dan `y` bertipe `T`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-06/src/main.rs}}
```

</Listing>

Sintaks untuk memakai generic dalam definisi struct mirip dengan yang dipakai dalam
definisi fungsi. Pertama, kita mendeklarasikan nama parameter tipe di dalam tanda
kurung sudut tepat setelah nama struct. Lalu, kita memakai tipe generic itu di
dalam definisi struct pada tempat-tempat yang seharusnya kita sebutkan tipe data
konkret.

Perhatikan bahwa karena kita hanya memakai satu tipe generic untuk mendefinisikan
`Point<T>`, definisi ini menyatakan bahwa struct `Point<T>` bersifat generic untuk
suatu tipe `T`, dan field `x` serta `y` _keduanya_ bertipe sama, apa pun tipe itu.
Jika kita membuat instance `Point<T>` yang nilainya bertipe berbeda, seperti di
Listing 10-7, kode kita tidak akan bisa dikompilasi.

<Listing number="10-7" file-name="src/main.rs" caption="Field `x` dan `y` harus bertipe sama karena keduanya memakai tipe data generic `T` yang sama.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/src/main.rs}}
```

</Listing>

Pada contoh ini, saat kita menetapkan nilai integer `5` ke `x`, kita memberi tahu
compiler bahwa tipe generic `T` akan menjadi integer untuk instance `Point<T>` ini.
Lalu, saat kita menetapkan `4.0` untuk `y`, yang telah kita definisikan bertipe sama
dengan `x`, kita akan mendapat error ketidaksesuaian tipe seperti ini:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/output.txt}}
```

Untuk mendefinisikan struct `Point` di mana `x` dan `y` sama-sama generic tetapi
boleh bertipe berbeda, kita bisa memakai beberapa parameter tipe generic. Misalnya,
di Listing 10-8 kita mengubah definisi `Point` agar bersifat generic untuk tipe `T`
dan `U`, dengan `x` bertipe `T` dan `y` bertipe `U`.

<Listing number="10-8" file-name="src/main.rs" caption="`Point<T, U>` yang generic untuk dua tipe sehingga `x` dan `y` bisa berisi nilai bertipe berbeda">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-08/src/main.rs}}
```

</Listing>

Sekarang semua instance `Point` yang ditampilkan diperbolehkan! Kamu bisa memakai
parameter tipe generic sebanyak yang kamu mau dalam sebuah definisi, tetapi memakai
lebih dari beberapa saja bisa membuat kode sulit dibaca. Jika kamu merasa perlu
banyak tipe generic dalam kode, itu bisa jadi tanda bahwa kode perlu dipecah menjadi
bagian-bagian yang lebih kecil.

### Di Dalam Definisi Enum

Sama seperti yang kita lakukan pada struct, kita bisa mendefinisikan enum agar
menyimpan tipe data generic di variant-nya. Mari kita lihat sekali lagi enum
`Option<T>` yang disediakan pustaka standar dan kita pakai di Bab 6:

```rust
enum Option<T> {
    Some(T),
    None,
}
```

Definisi ini sekarang seharusnya lebih masuk akal bagimu. Seperti yang kamu lihat,
enum `Option<T>` bersifat generic untuk tipe `T` dan punya dua variant: `Some`, yang
menyimpan satu nilai bertipe `T`, dan variant `None` yang tidak menyimpan nilai apa
pun. Dengan memakai enum `Option<T>`, kita bisa menyampaikan konsep abstrak dari
sebuah nilai opsional, dan karena `Option<T>` itu generic, kita bisa memakai
abstraksi ini tidak peduli apa pun tipe nilai opsionalnya.

Enum juga bisa memakai beberapa tipe generic. Definisi enum `Result` yang kita pakai
di Bab 9 adalah salah satu contohnya:

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

Enum `Result` bersifat generic untuk dua tipe, `T` dan `E`, dan punya dua variant:
`Ok`, yang menyimpan nilai bertipe `T`, dan `Err`, yang menyimpan nilai bertipe `E`.
Definisi ini membuat enum `Result` nyaman dipakai di mana pun kita punya operasi
yang bisa berhasil (mengembalikan nilai dari suatu tipe `T`) atau gagal
(mengembalikan error dari suatu tipe `E`). Faktanya, inilah yang kita pakai untuk
membuka file di Listing 9-3, di mana `T` diisi dengan tipe `std::fs::File` saat file
berhasil dibuka dan `E` diisi dengan tipe `std::io::Error` saat ada masalah saat
membuka file.

Saat kamu mengenali situasi dalam kode di mana ada beberapa definisi struct atau
enum yang hanya berbeda pada tipe nilai yang mereka simpan, kamu bisa menghindari
duplikasi dengan memakai tipe generic sebagai gantinya.

### Di Dalam Definisi Method

Kita bisa mengimplementasikan method pada struct dan enum (seperti yang kita lakukan
di Bab 5) dan memakai tipe generic pula dalam definisinya. Listing 10-9 menampilkan
struct `Point<T>` yang kita definisikan di Listing 10-6 dengan sebuah method bernama
`x` yang diimplementasikan padanya.

<Listing number="10-9" file-name="src/main.rs" caption="Mengimplementasikan method bernama `x` pada struct `Point<T>` yang akan mengembalikan reference ke field `x` bertipe `T`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-09/src/main.rs}}
```

</Listing>

Di sini, kita telah mendefinisikan method bernama `x` pada `Point<T>` yang
mengembalikan reference ke data di field `x`.

Perhatikan bahwa kita harus mendeklarasikan `T` tepat setelah `impl` agar bisa
memakai `T` untuk menyatakan bahwa kita mengimplementasikan method pada tipe
`Point<T>`. Dengan mendeklarasikan `T` sebagai tipe generic setelah `impl`, Rust bisa
mengenali bahwa tipe di dalam tanda kurung sudut pada `Point` adalah tipe generic,
bukan tipe konkret. Kita sebenarnya bisa memilih nama yang berbeda untuk parameter
generic ini dibanding parameter generic yang dideklarasikan dalam definisi struct,
tetapi memakai nama yang sama adalah hal yang lazim. Jika kamu menulis sebuah method
dalam `impl` yang mendeklarasikan tipe generic, method itu akan didefinisikan pada
semua instance tipe tersebut, tidak peduli tipe konkret apa yang akhirnya
menggantikan tipe generic itu.

Kita juga bisa menentukan batasan pada tipe generic saat mendefinisikan method pada
tipe itu. Misalnya, kita bisa mengimplementasikan method hanya pada instance
`Point<f32>`, alih-alih pada instance `Point<T>` dengan tipe generic apa pun. Di
Listing 10-10, kita memakai tipe konkret `f32`, yang berarti kita tidak
mendeklarasikan tipe apa pun setelah `impl`.

<Listing number="10-10" file-name="src/main.rs" caption="Blok `impl` yang hanya berlaku untuk struct dengan tipe konkret tertentu bagi parameter tipe generic `T`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-10/src/main.rs:here}}
```

</Listing>

Kode ini berarti tipe `Point<f32>` akan punya method `distance_from_origin`;
instance lain dari `Point<T>` di mana `T` bukan bertipe `f32` tidak akan punya
method ini. Method tersebut mengukur seberapa jauh titik kita dari titik di
koordinat (0.0, 0.0) dan memakai operasi matematika yang hanya tersedia untuk tipe
angka-desimal.

Parameter tipe generic dalam definisi struct tidak selalu sama dengan yang kita
pakai dalam tanda tangan method struct yang sama. Listing 10-11 memakai tipe generic
`X1` dan `Y1` untuk struct `Point` serta `X2` dan `Y2` untuk tanda tangan method
`mixup` agar contohnya lebih jelas. Method itu membuat instance `Point` baru dengan
nilai `x` dari `Point` `self` (bertipe `X1`) dan nilai `y` dari `Point` yang
diteruskan (bertipe `Y2`).

<Listing number="10-11" file-name="src/main.rs" caption="Method yang memakai tipe generic yang berbeda dari definisi struct-nya">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-11/src/main.rs}}
```

</Listing>

Di `main`, kita telah mendefinisikan `Point` yang `x`-nya bertipe `i32` (dengan nilai
`5`) dan `y`-nya bertipe `f64` (dengan nilai `10.4`). Variabel `p2` adalah struct
`Point` yang `x`-nya berupa string slice (dengan nilai `"Hello"`) dan `y`-nya berupa
`char` (dengan nilai `c`). Memanggil `mixup` pada `p1` dengan argumen `p2` memberi
kita `p3`, yang akan punya `i32` untuk `x` karena `x` berasal dari `p1`. Variabel
`p3` akan punya `char` untuk `y` karena `y` berasal dari `p2`. Pemanggilan macro
`println!` akan mencetak `p3.x = 5, p3.y = c`.

Tujuan contoh ini adalah menunjukkan situasi di mana sebagian parameter generic
dideklarasikan dengan `impl` dan sebagian lagi dideklarasikan bersama definisi
method. Di sini, parameter generic `X1` dan `Y1` dideklarasikan setelah `impl`
karena keduanya mengikuti definisi struct. Parameter generic `X2` dan `Y2`
dideklarasikan setelah `fn mixup` karena keduanya hanya relevan bagi method itu.

<a id="performance-of-code-using-generics"></a>
### Performa Kode yang Memakai Generic

Kamu mungkin bertanya-tanya apakah ada biaya saat runtime saat memakai parameter
tipe generic. Kabar baiknya, memakai tipe generic tidak membuat programmu berjalan
lebih lambat dibandingkan saat memakai tipe konkret.

Rust mewujudkan hal ini dengan melakukan monomorfisasi pada kode yang memakai
generic saat waktu kompilasi. _Monomorfisasi_ adalah proses mengubah kode generic
menjadi kode spesifik dengan mengisi tipe-tipe konkret yang dipakai saat
dikompilasi. Dalam proses ini, compiler melakukan kebalikan dari langkah-langkah
yang kita pakai untuk membuat fungsi generic di Listing 10-5: compiler melihat
semua tempat di mana kode generic dipanggil dan menghasilkan kode untuk tipe-tipe
konkret yang dipakai saat memanggil kode generic tersebut.

Mari kita lihat cara kerjanya dengan memakai enum generic `Option<T>` dari pustaka
standar:

```rust
let integer = Some(5);
let float = Some(5.0);
```

Saat Rust mengompilasi kode ini, Rust melakukan monomorfisasi. Selama proses itu,
compiler membaca nilai-nilai yang dipakai dalam instance `Option<T>` dan mengenali
dua macam `Option<T>`: salah satunya bertipe `i32` dan yang lain bertipe `f64`.
Dengan demikian, compiler mengembangkan definisi generic `Option<T>` menjadi dua
definisi yang dikhususkan untuk `i32` dan `f64`, sehingga definisi generic itu
digantikan oleh definisi-definisi spesifik tersebut.

Versi hasil monomorfisasi dari kode itu tampak seperti berikut (compiler memakai
nama yang berbeda dari yang kita pakai di sini untuk keperluan ilustrasi):

<Listing file-name="src/main.rs">

```rust
enum Option_i32 {
    Some(i32),
    None,
}

enum Option_f64 {
    Some(f64),
    None,
}

fn main() {
    let integer = Option_i32::Some(5);
    let float = Option_f64::Some(5.0);
}
```

</Listing>

`Option<T>` yang generic digantikan dengan definisi-definisi spesifik yang dibuat
oleh compiler. Karena Rust mengompilasi kode generic menjadi kode yang menyebutkan
tipe di setiap instance, kita tidak membayar biaya runtime apa pun untuk memakai
generic. Saat kode dijalankan, kode itu bekerja persis seperti seandainya kita
menduplikasi setiap definisi secara manual. Proses monomorfisasi inilah yang membuat
generic Rust sangat efisien di runtime.
