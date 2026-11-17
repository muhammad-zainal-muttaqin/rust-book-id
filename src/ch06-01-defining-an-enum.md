## Mendefinisikan Enum

Jika struct memberimu cara untuk mengelompokkan field dan data yang saling
berkaitan, seperti `Rectangle` dengan `width` dan `height`-nya, enum memberimu
cara untuk menyatakan bahwa sebuah nilai adalah salah satu dari sekumpulan
nilai yang mungkin. Sebagai contoh, kita mungkin ingin menyatakan bahwa
`Rectangle` adalah salah satu dari bentuk-bentuk yang mungkin, yang juga
mencakup `Circle` dan `Triangle`. Untuk melakukan itu, Rust mengizinkan kita
mengodekan kemungkinan-kemungkinan tersebut sebagai sebuah enum.

Mari kita lihat situasi yang ingin kita ekspresikan dalam kode untuk melihat
mengapa enum berguna dan lebih tepat dibanding struct dalam kasus ini. Katakan
kita harus bekerja dengan alamat IP. Saat ini, ada dua standar utama yang
digunakan untuk alamat IP: versi empat dan versi enam. Karena hanya itulah
kemungkinan alamat IP yang akan ditemui program kita, kita bisa _mengenumerasi_
semua varian yang mungkin — di situlah istilah *enumeration* berasal.

Alamat IP mana pun bisa berupa alamat versi empat atau versi enam, tetapi
tidak keduanya sekaligus. Sifat alamat IP inilah yang membuat struktur data
enum tepat digunakan, karena nilai enum hanya bisa berupa salah satu
variannya. Alamat versi empat dan versi enam tetap pada dasarnya merupakan
alamat IP, jadi keduanya harus diperlakukan sebagai tipe yang sama ketika kode
menangani situasi yang berlaku untuk segala jenis alamat IP.

Kita bisa mengekspresikan konsep ini dalam kode dengan mendefinisikan sebuah
enumerasi `IpAddrKind` dan menyebutkan jenis IP address yang mungkin, yaitu
`V4` dan `V6`. Inilah varian dari enum tersebut:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:def}}
```

`IpAddrKind` kini menjadi tipe data kustom yang bisa kita gunakan di bagian
kode lainnya.

<a id="enum-values"></a>
### Nilai Enum

Kita bisa membuat instance dari masing-masing dua varian `IpAddrKind` seperti
ini:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:instance}}
```

Perhatikan bahwa varian enum berada dalam namespace yang ditentukan oleh
identifikasinya, dan kita menggunakan dua titik dua untuk memisahkan keduanya.
Ini berguna karena kini kedua nilai `IpAddrKind::V4` dan `IpAddrKind::V6`
memiliki tipe yang sama: `IpAddrKind`. Dengan begitu, misalnya, kita bisa
mendefinisikan sebuah fungsi yang menerima `IpAddrKind` apa pun:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn}}
```

Dan kita bisa memanggil fungsi ini dengan varian mana pun:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn_call}}
```

Menggunakan enum punya lebih banyak lagi keuntungannya. Jika kita pikirkan lagi
tipe alamat IP kita, saat ini kita belum punya cara untuk menyimpan *data*
alamat IP yang sebenarnya; kita hanya tahu *jenis*-nya. Mengingat kamu baru
saja mempelajari struct di Bab 5, kamu mungkin tergoda untuk menyelesaikan
masalah ini dengan struct seperti yang ditampilkan di Listing 6-1.

<Listing number="6-1" caption="Menyimpan data dan varian `IpAddrKind` dari sebuah alamat IP menggunakan `struct`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-01/src/main.rs:here}}
```

</Listing>

Di sini, kita telah mendefinisikan struct `IpAddr` yang punya dua field: field
`kind` bertipe `IpAddrKind` (enum yang kita definisikan sebelumnya) dan field
`address` bertipe `String`. Kita punya dua instance struct ini. Yang pertama
adalah `home`, dengan nilai `IpAddrKind::V4` sebagai `kind`-nya beserta data
alamat `127.0.0.1` yang terkait. Instance kedua adalah `loopback`. Instance ini
memiliki varian `IpAddrKind` lainnya sebagai nilai `kind`-nya, yaitu `V6`,
beserta alamat `::1` yang terkait dengannya. Kita telah menggunakan struct
untuk mengikat nilai `kind` dan `address` bersama, sehingga kini varian tersebut
terkait dengan nilainya.

Namun, mewakili konsep yang sama hanya dengan enum jauh lebih ringkas: Alih-alih
menaruh enum di dalam struct, kita bisa langsung menaruh data ke dalam setiap
varian enum. Definisi baru dari enum `IpAddr` ini menyatakan bahwa kedua varian
`V4` dan `V6` akan memiliki nilai `String` yang terkait:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-02-enum-with-data/src/main.rs:here}}
```

Kita melampirkan data ke setiap varian enum secara langsung, sehingga tidak
perlu struct tambahan. Di sini, kita juga lebih mudah melihat detail lain
tentang cara kerja enum: Nama setiap varian enum yang kita definisikan juga
menjadi sebuah fungsi yang membuat instance dari enum tersebut. Artinya,
`IpAddr::V4()` adalah pemanggilan fungsi yang menerima argumen `String` dan
mengembalikan sebuah instance tipe `IpAddr`. Kita otomatis mendapatkan fungsi
konstruktor ini sebagai hasil dari pendefinisian enum tersebut.

Ada keuntungan lain menggunakan enum alih-alih struct: Setiap varian bisa
memiliki tipe dan jumlah data terkait yang berbeda. Alamat IP versi empat akan
selalu punya empat komponen numerik dengan nilai antara 0 dan 255. Jika kita
ingin menyimpan alamat `V4` sebagai empat nilai `u8` tetapi tetap
mengekspresikan alamat `V6` sebagai satu nilai `String`, hal itu tidak bisa
kita lakukan dengan struct. Enum menangani kasus ini dengan mudah:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-03-variants-with-different-data/src/main.rs:here}}
```

Kita telah menunjukkan beberapa cara berbeda untuk mendefinisikan struktur
data yang menyimpan alamat IP versi empat dan versi enam. Namun, ternyata
keinginan untuk menyimpan alamat IP dan mengodekan jenisnya begitu umum
sehingga [standard library punya definisi yang bisa kita gunakan!][IpAddr]<!-- ignore -->
Mari kita lihat bagaimana standard library mendefinisikan `IpAddr`. Library
tersebut punya enum dan varian yang persis sama dengan yang kita definisikan
dan gunakan, tetapi ia menanamkan data alamat di dalam varian-varian tersebut
dalam bentuk dua struct berbeda, yang definisinya berbeda untuk tiap varian:

```rust
struct Ipv4Addr {
    // --snip--
}

struct Ipv6Addr {
    // --snip--
}

enum IpAddr {
    V4(Ipv4Addr),
    V6(Ipv6Addr),
}
```

Kode ini menggambarkan bahwa kamu bisa menaruh data apa pun di dalam varian
enum: string, tipe numerik, atau struct, sebagai contoh. Kamu bahkan bisa
menyertakan enum lain! Selain itu, tipe dari standard library sering kali
tidak jauh lebih rumit dari apa yang bisa kamu pikirkan sendiri.

Perhatikan bahwa meskipun standard library sudah berisi definisi untuk `IpAddr`,
kita tetap bisa membuat dan menggunakan definisi kita sendiri tanpa konflik
karena kita belum membawa definisi dari standard library tersebut ke dalam
scope kita. Kita akan membahas lebih lanjut tentang membawa tipe ke dalam scope
di Bab 7.

Mari kita lihat contoh lain dari sebuah enum di Listing 6-2: enum ini punya
beragam tipe yang tertanam di dalam variannya.

<Listing number="6-2" caption="Enum `Message` yang variannya menyimpan nilai dengan tipe dan jumlah berbeda">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-02/src/main.rs:here}}
```

</Listing>

Enum ini punya empat varian dengan tipe berbeda:

- `Quit`: Tidak punya data sama sekali
- `Move`: Memiliki field bernama, seperti struct
- `Write`: Memuat satu buah `String`
- `ChangeColor`: Memuat tiga nilai `i32`

Mendefinisikan enum dengan varian seperti pada Listing 6-2 mirip dengan
mendefinisikan beberapa definisi struct yang berbeda, kecuali enum tidak
menggunakan keyword `struct` dan semua varian dikelompokkan bersama di dalam
tipe `Message`. Struct berikut bisa menyimpan data yang sama dengan yang
disimpan oleh varian enum sebelumnya:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-04-structs-similar-to-message-enum/src/main.rs:here}}
```

Tetapi jika kita menggunakan struct yang berbeda-beda, yang masing-masing
memiliki tipe sendiri, kita tidak bisa semudah itu mendefinisikan fungsi yang
menerima segala jenis pesan seperti yang bisa kita lakukan dengan enum
`Message` pada Listing 6-2, yang merupakan satu tipe tunggal.

Masih ada satu kemiripan lain antara enum dan struct: Sama seperti kita bisa
mendefinisikan method pada struct menggunakan `impl`, kita juga bisa
mendefinisikan method pada enum. Berikut method bernama `call` yang bisa kita
definisikan pada enum `Message` kita:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-05-methods-on-enums/src/main.rs:here}}
```

Badan method akan menggunakan `self` untuk mendapatkan nilai yang kita panggil
method-nya. Dalam contoh ini, kita telah membuat variabel `m` dengan nilai
`Message::Write(String::from("hello"))`, dan itulah yang akan menjadi `self`
di dalam badan method `call` ketika `m.call()` berjalan.

Mari kita lihat enum lain di standard library yang sangat umum dan berguna:
`Option`.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-option-enum-and-its-advantages-over-null-values"></a>

### Enum `Option`

Bagian ini membahas studi kasus tentang `Option`, sebuah enum lain yang
didefinisikan oleh standard library. Tipe `Option` mengodekan skenario yang
sangat umum, di mana sebuah nilai mungkin berisi sesuatu, atau mungkin kosong.

Sebagai contoh, jika kamu meminta item pertama pada list yang tidak kosong,
kamu akan mendapatkan sebuah nilai. Jika kamu meminta item pertama pada list
yang kosong, kamu tidak akan mendapatkan apa pun. Mengekspresikan konsep ini
dalam sistem tipe berarti compiler bisa memeriksa apakah kamu sudah menangani
semua kasus yang seharusnya kamu tangani; kemampuan ini bisa mencegah bug yang
sangat umum terjadi di bahasa pemrograman lain.

Desain bahasa pemrograman sering dipikirkan dari sudut fitur apa saja yang
kamu sertakan, tetapi fitur yang kamu kecualikan pun penting. Rust tidak punya
fitur null yang dimiliki banyak bahasa lain. *Null* adalah nilai yang berarti
tidak ada nilai di sana. Dalam bahasa yang punya null, variabel selalu bisa
berada dalam salah satu dari dua keadaan: null atau bukan-null.

Dalam presentasinya tahun 2009 berjudul "Null References: The Billion Dollar
Mistake," Tony Hoare, penemu null, berkata begini:

> Saya menyebutnya kesalahan sen dolar miliar saya. Saat itu, saya sedang
> merancang sistem tipe komprehensif pertama untuk reference dalam sebuah
> bahasa berorientasi objek. Tujuan saya adalah memastikan penggunaan
> reference apa pun harus benar-benar aman, dengan pemeriksaan yang
> dilakukan otomatis oleh compiler. Tetapi saya tidak bisa menahan godaan
> untuk memasukkan sebuah null reference, semata-mata karena itu terlalu
> mudah diimplementasikan. Hal ini telah menyebabkan kesalahan,
> kerentanan, dan crash sistem yang tak terhitung jumlahnya, yang mungkin
> telah menyebabkan penderitaan dan kerugian sen dolar miliar dalam
> empat puluh tahun terakhir.

Masalah dengan nilai null adalah jika kamu mencoba menggunakan nilai null
sebagai nilai bukan-null, kamu akan mendapatkan error semacam ini. Karena sifat
null atau bukan-null ini ada di mana-mana, sangatlah mudah untuk membuat
kesalahan semacam ini.

Namun, konsep yang ingin diekspresikan oleh null tetap berguna: null adalah
nilai yang saat ini tidak valid atau absen karena suatu alasan.

Masalahnya sebenarnya bukan pada konsepnya, melainkan pada implementasi
khususnya. Karena itu, Rust tidak punya null, tetapi ia punya sebuah enum yang
bisa mengodekan konsep keberadaan atau ketiadaan sebuah nilai. Enum ini adalah
`Option<T>`, dan ia [didefinisikan oleh standard library][option]<!-- ignore -->
sebagai berikut:

```rust
enum Option<T> {
    None,
    Some(T),
}
```

Enum `Option<T>` sangat berguna sehingga ikut disertakan dalam prelude; kamu
tidak perlu membawanya ke dalam scope secara eksplisit. Varian-variannya juga
ikut disertakan dalam prelude: Kamu bisa langsung menggunakan `Some` dan `None`
tanpa awalan `Option::`. Enum `Option<T>` tetap hanyalah enum biasa, dan
`Some(T)` serta `None` tetap merupakan varian bertipe `Option<T>`.

Sintaks `<T>` adalah fitur Rust yang belum kita bicarakan. Ini adalah parameter
tipe generic, dan kita akan membahas generic lebih rinci di Bab 10. Untuk
sekarang, yang perlu kamu ketahui hanya bahwa `<T>` berarti varian `Some` dari
enum `Option` bisa menampung satu buah data bertipe apa pun, dan bahwa setiap
tipe konkret yang dipakai menggantikan `T` membuat keseluruhan tipe
`Option<T>` menjadi tipe yang berbeda. Berikut beberapa contoh penggunaan
nilai `Option` untuk menampung tipe angka dan tipe char:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-06-option-examples/src/main.rs:here}}
```

Tipe dari `some_number` adalah `Option<i32>`. Tipe dari `some_char` adalah
`Option<char>`, yang merupakan tipe berbeda. Rust bisa menyimpulkan tipe-tipe
ini karena kita telah menentukan sebuah nilai di dalam varian `Some`. Untuk
`absent_number`, Rust mensyaratkan kita memberi anotasi tipe `Option` secara
keseluruhan: Compiler tidak bisa menyimpulkan tipe yang akan dipegang oleh
varian `Some` yang bersangkutan hanya dengan melihat nilai `None`. Di sini,
kita memberi tahu Rust bahwa kita menginginkan `absent_number` bertipe
`Option<i32>`.

Ketika kita punya nilai `Some`, kita tahu bahwa sebuah nilai ada, dan nilai
tersebut dipegang di dalam `Some` itu. Ketika kita punya nilai `None`, dalam
artian tertentu itu berarti hal yang sama dengan null: Kita tidak punya nilai
yang valid. Lalu, mengapa memiliki `Option<T>` lebih baik daripada memiliki
null?

Singkatnya, karena `Option<T>` dan `T` (di mana `T` bisa berupa tipe apa pun)
adalah tipe yang berbeda, compiler tidak akan membiarkan kita menggunakan nilai
`Option<T>` seolah-olah nilai itu pasti valid. Sebagai contoh, kode ini tidak
akan mengompilasi, karena mencoba menambahkan `i8` dengan `Option<i8>`:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/src/main.rs:here}}
```

Jika kita menjalankan kode ini, kita akan mendapatkan pesan error seperti ini:

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/output.txt}}
```

Luar biasa! Pada dasarnya, pesan error ini berarti Rust tidak mengerti cara
menambahkan `i8` dengan `Option<i8>`, karena keduanya bertipe berbeda. Ketika
kita punya nilai bertipe seperti `i8` di Rust, compiler akan memastikan bahwa
kita selalu punya nilai yang valid. Kita bisa melangkah dengan percaya diri
tanpa harus memeriksa null sebelum menggunakan nilai tersebut. Baru ketika kita
punya `Option<i8>` (atau tipe nilai apa pun yang sedang kita kerjakan) kita
perlu khawatir soal kemungkinan tidak punya nilai, dan compiler akan memastikan
kita menangani kasus tersebut sebelum menggunakan nilai itu.

Dengan kata lain, kamu harus mengonversi `Option<T>` menjadi `T` sebelum kamu
bisa melakukan operasi `T` dengannya. Secara umum, ini membantu menangkap salah
satu masalah paling umum dengan null: menganggap sesuatu bukan-null padahal
sebenarnya null.

Menghilangkan risiko asumsi yang keliru terhadap sebuah nilai bukan-null
membantu kamu lebih percaya diri dengan kodemu. Untuk punya nilai yang mungkin
null, kamu harus secara eksplisit memilihnya dengan membuat tipe nilai
tersebut menjadi `Option<T>`. Lalu, ketika kamu menggunakan nilai itu, kamu
diwajibkan menangani secara eksplisit kasus ketika nilai tersebut null. Di
mana pun sebuah nilai bertipe yang bukan `Option<T>`, kamu *bisa* dengan aman
mengasumsikan bahwa nilai tersebut bukan-null. Ini adalah keputusan desain yang
sengaja dibuat oleh Rust untuk membatasi penyebaran null dan meningkatkan
keamanan kode Rust.

Lalu bagaimana kamu mengeluarkan nilai `T` dari varian `Some` ketika kamu punya
nilai bertipe `Option<T>` agar bisa menggunakan nilai itu? Enum `Option<T>`
punya sangat banyak method yang berguna untuk berbagai situasi; kamu bisa
menjelajahinya di [dokumentasinya][docs]<!-- ignore -->. Membiasakan diri dengan
method-method pada `Option<T>` akan sangat berguna dalam perjalananmu
mempelajari Rust.

Secara umu, untuk menggunakan nilai `Option<T>`, kamu ingin punya kode yang
menangani setiap varian. Kamu ingin kode yang hanya berjalan ketika kamu punya
nilai `Some(T)`, dan kode ini boleh menggunakan `T` di dalamnya. Kamu ingin
kode lain yang hanya berjalan jika kamu punya nilai `None`, dan kode tersebut
tidak punya nilai `T` yang tersedia. Ekspresi `match` adalah konstruk alur
kontrol yang melakukan tepat hal itu ketika digunakan dengan enum: Ia akan
menjalankan kode yang berbeda tergantung varian enum yang dimilikinya, dan
kode tersebut bisa menggunakan data di dalam nilai yang cocok.

[IpAddr]: ../std/net/enum.IpAddr.html
[option]: ../std/option/enum.Option.html
[docs]: ../std/option/enum.Option.html
