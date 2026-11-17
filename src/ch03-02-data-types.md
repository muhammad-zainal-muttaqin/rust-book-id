<a id="data-types"></a>
## Tipe Data

Setiap nilai di Rust memiliki suatu _tipe data_ tertentu. Tipe itu memberi tahu
Rust jenis data apa yang sedang kamu tentukan, sehingga Rust tahu cara bekerja
dengan data tersebut. Kita akan melihat dua kelompok tipe data: skalar dan
komposit.

Perlu diingat bahwa Rust adalah bahasa yang _bertipe statis_, artinya Rust
harus mengetahui tipe semua variabel pada waktu kompilasi. Biasanya compiler
bisa menyimpulkan tipe yang ingin kita pakai berdasarkan nilai dan cara kita
menggunakannya. Pada kasus di mana banyak tipe yang mungkin—seperti ketika kita
mengonversi `String` ke tipe numerik menggunakan `parse` di bagian
["Membandingkan Tebakannya dengan Angka
Rahasia"][comparing-the-guess-to-the-secret-number]<!-- ignore --> di Bab 2—kita
harus menambahkan anotasi tipe, seperti ini:

```rust
let guess: u32 = "42".parse().expect("Not a number!");
```

Jika kita tidak menambahkan anotasi tipe `: u32` seperti pada kode sebelumnya,
Rust akan menampilkan error berikut, yang berarti compiler butuh informasi
lebih dari kita untuk mengetahui tipe mana yang ingin kita pakai:

```console
{{#include ../listings/ch03-common-programming-concepts/output-only-01-no-type-annotations/output.txt}}
```

Kamu akan melihat anotasi tipe yang berbeda untuk tipe data lainnya.

### Tipe Skalar

Tipe _skalar_ merepresentasikan satu nilai. Rust punya empat tipe skalar
utama: bilangan bulat, bilangan floating-point, Boolean, dan karakter. Mungkin
kamu mengenalnya dari bahasa pemrograman lain. Mari kita bahas cara kerjanya
di Rust.

<a id="integer-types"></a>
#### Tipe Bilangan Bulat

_Bilangan bulat_ adalah angka tanpa komponen pecahan. Kita sudah memakai satu
tipe bilangan bulat di Bab 2, yaitu tipe `u32`. Deklarasi tipe ini menunjukkan
bahwa nilai yang terkait dengannya harus berupa bilangan bulat signed (tipe
bilangan bulat signed diawali `i`, bukan `u`) yang memakan ruang 32 bit.
Tabel 3-1 menunjukkan tipe bilangan bulat bawaan di Rust. Kita bisa memakai
varian mana pun untuk mendeklarasikan tipe sebuah nilai bilangan bulat.

<span class="caption">Tabel 3-1: Tipe Bilangan Bulat di Rust</span>

| Panjang  | Bertanda  | Tanpa Tanda |
| ------- | ------- | -------- |
| 8-bit   | `i8`    | `u8`     |
| 16-bit  | `i16`   | `u16`    |
| 32-bit  | `i32`   | `u32`    |
| 64-bit  | `i64`   | `u64`    |
| 128-bit | `i128`  | `u128`   |
| Bergantung arsitektur | `isize` | `usize`  |

Setiap varian bisa berupa signed atau unsigned dan punya ukuran yang eksplisit.
_Signed_ dan _unsigned_ menunjukkan apakah sebuah angka bisa bernegatif—dengan
kata lain, apakah angka itu perlu membawa tanda (signed), atau apakah angka itu
hanya akan selalu positif sehingga bisa direpresentasikan tanpa tanda
(unsigned). Seperti menulis angka di kertas: ketika tandanya penting, sebuah
angka ditampilkan dengan tanda plus atau minus; tetapi ketika aman
mengasumsikan angka itu positif, angka itu ditampilkan tanpa tanda. Angka
signed disimpan menggunakan representasi [two’s
complement][twos-complement]<!-- ignore
-->.

Setiap varian signed bisa menyimpan angka dari −(2<sup>n − 1</sup>) sampai
2<sup>n − 1</sup> − 1 inklusif, di mana _n_ adalah jumlah bit yang dipakai
varian tersebut. Jadi, sebuah `i8` bisa menyimpan angka dari −(2<sup>7</sup>)
sampai 2<sup>7</sup> − 1, yang sama dengan −128 sampai 127. Varian unsigned
bisa menyimpan angka dari 0 sampai 2<sup>n</sup> − 1, sehingga sebuah `u8`
bisa menyimpan angka dari 0 sampai 2<sup>8</sup> − 1, yang sama dengan 0
sampai 255.

Selain itu, tipe `isize` dan `usize` bergantung pada arsitektur komputer tempat
program kamu berjalan: 64 bit jika kamu berada di arsitektur 64-bit dan 32 bit
jika kamu berada di arsitektur 32-bit.

Kamu bisa menulis literal bilangan bulat dalam bentuk apa pun yang ditampilkan
di Tabel 3-2. Perhatikan bahwa literal angka yang bisa berupa beberapa tipe
numerik mengizinkan sebuah akhiran tipe, seperti `57u8`, untuk menentukan
tipenya. Literal angka juga bisa memakai `_` sebagai pemisah visual agar
angkanya lebih mudah dibaca, seperti `1_000`, yang punya nilai sama dengan
jika kamu menulis `1000`.

<span class="caption">Tabel 3-2: Literal Bilangan Bulat di Rust</span>

| Literal angka  | Contoh       |
| ---------------- | ------------- |
| Desimal          | `98_222`      |
| Heksadesimal     | `0xff`        |
| Oktal            | `0o77`        |
| Biner            | `0b1111_0000` |
| Byte (hanya `u8`) | `b'A'`        |

Lalu bagaimana kamu tahu harus memakai tipe bilangan bulat yang mana? Jika
kamu ragu, nilai default Rust biasanya tempat yang baik untuk memulai: tipe
bilangan bulat secara default adalah `i32`. Situasi utama di mana kamu akan
memakai `isize` atau `usize` adalah saat mengindeks semacam kumpulan.

> ##### Overflow Bilangan Bulat
>
> Misalnya kamu punya variabel bertipe `u8` yang bisa menampung nilai antara 0
> dan 255. Jika kamu mencoba mengubah variabel itu ke nilai di luar rentang
> tersebut, seperti 256, _overflow bilangan bulat_ akan terjadi, yang bisa
> menghasilkan salah satu dari dua perilaku. Saat kamu mengompilasi dalam mode
> debug, Rust menyertakan pemeriksaan overflow bilangan bulat yang membuat
> program kamu _panic_ pada runtime jika perilaku ini terjadi. Rust memakai
> istilah _panicking_ ketika program keluar karena sebuah error; kita akan
> membahas panic lebih dalam di bagian ["Error yang Tidak Bisa Dipulihkan dengan
> `panic!`"][unrecoverable-errors-with-panic]<!-- ignore --> di Bab 9.
>
> Saat kamu mengompilasi dalam mode release dengan flag `--release`, Rust
> _tidak_ menyertakan pemeriksaan overflow bilangan bulat yang memicu panic.
> Sebaliknya, jika overflow terjadi, Rust melakukan _two’s complement
> wrapping_. Singkatnya, nilai yang lebih besar dari nilai maksimum yang bisa
> ditampung tipe tersebut akan "wrap around" ke nilai minimum yang bisa
> ditampung tipe itu. Pada kasus `u8`, nilai 256 menjadi 0, nilai 257 menjadi
> 1, dan seterusnya. Program tidak akan panic, tetapi variabel itu akan punya
> nilai yang mungkin bukan yang kamu harapkan. Mengandalkan perilaku wrapping
> dari overflow bilangan bulat dianggap sebagai sebuah error.
>
> Untuk menangani kemungkinan overflow secara eksplisit, kamu bisa memakai
> kelompok method berikut yang disediakan library standar untuk tipe numerik
> primitif:
>
> - Membungkus (wrap) di semua mode kompilasi dengan method `wrapping_*`,
>   seperti `wrapping_add`.
> - Mengembalikan nilai `None` jika terjadi overflow, dengan method
>   `checked_*`.
> - Mengembalikan nilai serta Boolean yang menunjukkan apakah terjadi overflow,
>   dengan method `overflowing_*`.
> - Menjenuhkan ke nilai minimum atau maksimum dengan method `saturating_*`.

#### Tipe Floating-Point

Rust juga punya dua tipe primitif untuk _bilangan floating-point_, yaitu angka
yang punya titik desimal. Tipe floating-point di Rust adalah `f32` dan `f64`,
yang berukuran 32 bit dan 64 bit secara berturut-turut. Tipe defaultnya adalah
`f64` karena di CPU modern, kecepatannya kira-kira sama dengan `f32` tetapi
mampu memberikan presisi lebih tinggi. Semua tipe floating-point bersifat
signed.

Berikut contoh yang menunjukkan bilangan floating-point dalam aksi:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-06-floating-point/src/main.rs}}
```

Bilangan floating-point direpresentasikan sesuai standar IEEE-754.

#### Operasi Numerik

Rust mendukung operasi matematika dasar yang kamu harapkan untuk semua tipe
angka: penjumlahan, pengurangan, perkalian, pembagian, dan sisa bagi. Pembagian
bilangan bulat membuang bagian pecahannya menuju nol. Kode berikut menunjukkan
cara memakai setiap operasi numerik dalam sebuah statement `let`:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-07-numeric-operations/src/main.rs}}
```

Setiap ekspresi dalam statement ini memakai sebuah operator matematika dan
dievaluasi menjadi satu nilai, yang kemudian diikat ke sebuah variabel.
[Lampiran B][appendix_b]<!-- ignore --> berisi daftar semua operator yang
disediakan Rust.

#### Tipe Boolean

Seperti kebanyakan bahasa pemrograman lain, tipe Boolean di Rust punya dua
nilai yang mungkin: `true` dan `false`. Boolean berukuran satu byte. Tipe
Boolean di Rust didefinisikan dengan `bool`. Sebagai contoh:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-08-boolean/src/main.rs}}
```

Cara utama memakai nilai Boolean adalah melalui kondisional, seperti ekspresi
`if`. Kita akan membahas cara kerja ekspresi `if` di Rust di bagian ["Alur
Kontrol"][control-flow]<!-- ignore -->.

#### Tipe Karakter

Tipe `char` di Rust adalah tipe alfabet paling primitif dalam bahasa ini.
Berikut beberapa contoh deklarasi nilai `char`:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-09-char/src/main.rs}}
```

Perhatikan bahwa kita menulis literal `char` dengan tanda kutip tunggal,
berbeda dengan literal string yang memakai tanda kutip ganda. Tipe `char` di
Rust berukuran 4 byte dan merepresentasikan sebuah nilai skalar Unicode,
artinya ia bisa mewakili jauh lebih banyak dari sekadar ASCII. Huruf beraksen;
karakter Tionghoa, Jepang, dan Korea; emoji; serta spasi lebar nol semuanya
merupakan nilai `char` yang valid di Rust. Nilai skalar Unicode berkisar dari
`U+0000` sampai `U+D7FF` dan `U+E000` sampai `U+10FFFF` inklusif. Namun,
"karakter" sebenarnya bukan konsep dalam Unicode, jadi intuisi manusiawi kamu
tentang apa itu "karakter" mungkin tidak cocok dengan pengertian `char` di
Rust. Kita akan membahas topik ini secara detail di ["Menyimpan Teks Terenkripsi
UTF-8 dengan String"][strings]<!-- ignore --> di Bab 8.

### Tipe Komposit

_Tipe komposit_ bisa mengelompokkan beberapa nilai ke dalam satu tipe. Rust
punya dua tipe komposit primitif: tuple dan array.

<a id="the-tuple-type"></a>
#### Tipe Tuple

_Tuple_ adalah cara umum untuk mengelompokkan sejumlah nilai dengan berbagai
tipe ke dalam satu tipe komposit. Tuple punya panjang tetap: sekali
dideklarasikan, ukurannya tidak bisa membesar atau mengecil.

Kita membuat tuple dengan menulis daftar nilai yang dipisahkan koma di dalam
tanda kurung bulat. Setiap posisi dalam tuple punya sebuah tipe, dan tipe dari
nilai-nilai berbeda dalam tuple tidak harus sama. Pada contoh ini kita
menambahkan anotasi tipe yang opsional:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-10-tuples/src/main.rs}}
```

Variabel `tup` mengikat ke seluruh tuple karena tuple dianggap sebagai satu
elemen komposit. Untuk mengambil nilai-nilai individual dari sebuah tuple, kita
bisa memakai pencocokan pola untuk mendestruksi nilai tuple, seperti ini:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-11-destructuring-tuples/src/main.rs}}
```

Program ini pertama-tama membuat sebuah tuple dan mengikatnya ke variabel
`tup`. Lalu ia memakai sebuah pola bersama `let` untuk mengambil `tup` dan
mengubahnya menjadi tiga variabel terpisah, yaitu `x`, `y`, dan `z`. Hal ini
disebut _destructuring_ karena memecah tuple tunggal tersebut menjadi tiga
bagian. Terakhir, program mencetak nilai `y`, yaitu `6.4`.

Kita juga bisa mengakses elemen tuple secara langsung dengan titik (`.`)
diikuti indeks nilai yang ingin diakses. Sebagai contoh:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-12-tuple-indexing/src/main.rs}}
```

Program ini membuat tuple `x` lalu mengakses setiap elemennya menggunakan
indeks masing-masing. Seperti kebanyakan bahasa pemrograman, indeks pertama
dalam sebuah tuple adalah 0.

Tuple tanpa nilai apa pun punya nama khusus, yaitu _unit_. Nilai ini dan tipe
yang bersangkutan sama-sama ditulis `()` dan merepresentasikan nilai kosong
atau tipe kembalian kosong. Ekspresi secara implisit mengembalikan nilai unit
jika tidak mengembalikan nilai lain.

#### Tipe Array

Cara lain untuk punya kumpulan beberapa nilai adalah dengan sebuah _array_.
Berbeda dengan tuple, setiap elemen array harus punya tipe yang sama. Berbeda
dengan array di beberapa bahasa lain, array di Rust punya panjang tetap.

Kita menulis nilai dalam sebuah array sebagai daftar yang dipisahkan koma di
dalam kurung siku:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-13-arrays/src/main.rs}}
```

Array berguna ketika kamu ingin data kamu dialokasikan di stack, sama seperti
tipe-tipe lain yang sudah kita lihat sejauh ini, alih-alih di heap (kita akan
membahas stack dan heap lebih lanjut di [Bab 4][stack-and-heap]<!-- ignore -->),
atau ketika kamu ingin memastikan selalu punya jumlah elemen yang tetap.
Namun, array tidak sefleksibel tipe vector. _Vector_ adalah tipe kumpulan
serupa yang disediakan library standar dan boleh membesar atau mengecil
ukurannya karena isinya hidup di heap. Jika kamu ragu harus memakai array atau
vector, kemungkinan besar kamu sebaiknya memakai vector. [Bab
8][vectors]<!-- ignore --> membahas vector lebih lanjut.

Namun, array lebih berguna ketika kamu tahu jumlah elemennya tidak akan
berubah. Sebagai contoh, jika kamu memakai nama bulan dalam sebuah program,
kamu mungkin akan memakai array alih-alih vector karena kamu tahu isinya
selalu 12 elemen:

```rust
let months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];
```

Kamu menulis tipe sebuah array dengan kurung siku berisi tipe setiap elemen,
lalu titik koma, dan terakhir jumlah elemen dalam array, seperti ini:

```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
```

Di sini, `i32` adalah tipe setiap elemen. Setelah titik koma, angka `5`
menunjukkan array berisi lima elemen.

Kamu juga bisa menginisialisasi array agar setiap elemennya punya nilai yang
sama dengan menentukan nilai awal, diikuti titik koma, lalu panjang array di
dalam kurung siku, seperti ini:

```rust
let a = [3; 5];
```

Array bernama `a` akan berisi `5` elemen yang semuanya diatur ke nilai `3`
pada awalnya. Ini sama dengan menulis `let a = [3, 3, 3, 3, 3];` tetapi dengan
cara yang lebih ringkas.

<!-- Old headings. Do not remove or links may break. -->
<a id="accessing-array-elements"></a>

#### Akses Elemen Array

Array adalah satu blok memori berukuran tetap yang sudah diketahui dan bisa
dialokasikan di stack. Kamu bisa mengakses elemen array menggunakan indeks,
seperti ini:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-14-array-indexing/src/main.rs}}
```

Pada contoh ini, variabel bernama `first` akan mendapat nilai `1` karena nilai
itu berada di indeks `[0]` dalam array. Variabel bernama `second` akan mendapat
nilai `2` dari indeks `[1]` dalam array.

#### Akses Elemen Array yang Tidak Valid

Mari kita lihat apa yang terjadi jika kamu mencoba mengakses elemen array yang
berada melewati akhir array. Misalnya kamu menjalankan kode berikut, mirip
dengan game tebak-tebakan di Bab 2, untuk mendapatkan indeks array dari
pengguna:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,panics
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access/src/main.rs}}
```

Kode ini berhasil dikompilasi. Jika kamu menjalankan kode ini dengan `cargo
run` lalu memasukkan `0`, `1`, `2`, `3`, atau `4`, program akan mencetak nilai
yang sesuai di indeks tersebut dalam array. Sebaliknya, jika kamu memasukkan
angka yang melewati akhir array, misalnya `10`, kamu akan melihat keluaran
seperti ini:

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access
cargo run
10
-->

```console
thread 'main' panicked at src/main.rs:19:19:
index out of bounds: the len is 5 but the index is 10
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Program menghasilkan error runtime pada saat nilai tidak valid dipakai dalam
operasi indeks. Program keluar dengan pesan error dan tidak mengeksekusi
statement `println!` terakhir. Saat kamu mencoba mengakses elemen menggunakan
indeks, Rust akan memeriksa bahwa indeks yang kamu tentukan lebih kecil dari
panjang array. Jika indeksnya lebih besar atau sama dengan panjangnya, Rust
akan panic. Pemeriksaan ini harus terjadi pada runtime, terutama dalam kasus
ini, karena compiler tidak mungkin tahu nilai apa yang akan dimasukkan
pengguna saat menjalankan kode tersebut nanti.

Ini adalah contoh prinsip keamanan memori Rust dalam aksi. Di banyak bahasa
tingkat rendah, pemeriksaan semacam ini tidak dilakukan, dan ketika kamu
memberikan indeks yang salah, memori yang tidak valid bisa diakses. Rust
melindungi kamu dari error semacam ini dengan langsung keluar, alih-alih
mengizinkan akses memori itu terjadi lalu melanjutkan program. Bab 9 membahas
lebih lanjut tentang penanganan error di Rust dan bagaimana kamu bisa menulis
kode yang mudah dibaca dan aman, yang tidak panic maupun mengizinkan akses
memori yang tidak valid.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[twos-complement]: https://en.wikipedia.org/wiki/Two%27s_complement
[control-flow]: ch03-05-control-flow.html#control-flow
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[stack-and-heap]: ch04-01-what-is-ownership.html#the-stack-and-the-heap
[vectors]: ch08-01-vectors.html
[unrecoverable-errors-with-panic]: ch09-01-unrecoverable-errors-with-panic.html
[appendix_b]: appendix-02-operators.md
