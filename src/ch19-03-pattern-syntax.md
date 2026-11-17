## Sintaksis Pattern

Di bagian ini, kita kumpulkan semua sintaksis yang valid di dalam pattern dan
membahas mengapa serta kapan kamu mungkin ingin memakai masing-masing.

### Mencocokkan Literal

Seperti yang kamu lihat di Bab 6, kamu bisa mencocokkan pattern langsung
terhadap literal. Kode berikut memberi beberapa contoh:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-01-literals/src/main.rs:here}}
```

Kode ini mencetak `one` karena nilai di `x` adalah `1`. Sintaksis ini berguna
ketika kamu ingin kode mengambil tindakan jika ia menerima sebuah nilai konkret
tertentu.

### Mencocokkan Variabel Bernama

Variabel bernama adalah pattern yang tak terbantahkan (*irrefutable*) yang
cocok dengan nilai apa pun, dan kita sudah memakainya berkali-kali dalam buku
ini. Namun, ada satu kerumitan ketika kamu memakai variabel bernama di dalam
ekspresi `match`, `if let`, atau `while let`. Karena masing-masing jenis
ekspresi ini membuka scope baru, variabel yang dideklarasikan sebagai bagian
dari pattern di dalam ekspresi tersebut akan menutupi (*shadow*) variabel
bernama sama di luar konstruksi itu, seperti yang berlaku bagi semua variabel.
Pada Listing 19-11, kita mendeklarasikan variabel bernama `x` dengan nilai
`Some(5)` dan variabel `y` dengan nilai `10`. Lalu kita membuat ekspresi
`match` atas nilai `x`. Perhatikan pattern di cabang-cabang match dan `println!`
di akhir, lalu coba tebak apa yang akan dicetak kode ini sebelum menjalankannya
atau membaca lebih lanjut.

<Listing number="19-11" file-name="src/main.rs" caption="Sebuah ekspresi `match` dengan cabang yang memperkenalkan variabel baru yang menutupi variabel `y` yang sudah ada">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-11/src/main.rs:here}}
```

</Listing>

Mari kita telusuri apa yang terjadi saat ekspresi `match` dijalankan. Pattern
di cabang match pertama tidak cocok dengan nilai `x` yang didefinisikan, jadi
kode berlanjut.

Pattern di cabang match kedua memperkenalkan variabel baru bernama `y` yang
akan cocok dengan nilai apa pun di dalam nilai `Some`. Karena kita berada di
scope baru di dalam ekspresi `match`, ini adalah variabel `y` yang baru,
bukan `y` yang kita deklarasikan di awal dengan nilai `10`. Binding `y` yang
baru ini akan cocok dengan nilai apa pun di dalam `Some`, dan itulah yang ada
di `x`. Karena itu, `y` yang baru ini terikat pada nilai dalam `Some` di `x`.
Nilainya adalah `5`, jadi ekspresi untuk cabang itu dijalankan dan mencetak
`Matched, y = 5`.

Seandainya `x` adalah nilai `None`, bukan `Some(5)`, pattern di dua cabang
pertama tidak akan cocok, sehingga nilainya akan cocok dengan garis bawah. Kita
tidak memperkenalkan variabel `x` di pattern cabang garis bawah, jadi `x` di
ekspresi tersebut tetap `x` dari luar yang belum ditutupi. Dalam skenario
hipotetis ini, `match` akan mencetak `Default case, x = None`.

Setelah ekspresi `match` selesai, scope-nya berakhir, dan begitu pula scope
dari `y` di dalamnya. `println!` terakhir menghasilkan `at the end: x = Some(5), y = 10`.

Untuk membuat ekspresi `match` yang membandingkan nilai `x` dan `y` dari luar,
bukan memperkenalkan variabel baru yang menutupi variabel `y` yang sudah ada,
kita perlu memakai kondisi match guard sebagai gantinya. Kita akan membahas
match guard nanti di bagian [“Menambahkan Kondisi dengan Match
Guards”](#adding-conditionals-with-match-guards)<!-- ignore -->.

<!-- Old headings. Do not remove or links may break. -->
<a id="multiple-patterns"></a>

### Mencocokkan Beberapa Pattern

Dalam ekspresi `match`, kamu bisa mencocokkan beberapa pattern memakai
sintaksis `|`, yaitu operator pattern _atau_ (_or_). Misalnya, pada kode
berikut, kita mencocokkan nilai `x` terhadap cabang-cabang match, yang pertama
di antaranya punya opsi _or_, artinya jika nilai `x` cocok dengan salah satu
nilai di cabang itu, kode cabang itu akan dijalankan:


```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-02-multiple-patterns/src/main.rs:here}}
```

Kode ini mencetak `one or two`.

### Mencocokkan Rentang Nilai dengan `..=`

Sintaksis `..=` memungkinkan kita mencocokkan ke dalam rentang nilai inklusif.
Pada kode berikut, ketika sebuah pattern cocok dengan nilai apa pun di dalam
rentang yang diberikan, cabang itu akan dijalankan:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-03-ranges/src/main.rs:here}}
```

Jika `x` adalah `1`, `2`, `3`, `4`, atau `5`, cabang pertama akan cocok.
Sintaksis ini lebih nyaman untuk banyak nilai pencocokan daripada memakai
operator `|` untuk menyampaikan maksud yang sama; jika kita memakai `|`, kita
harus menulis `1 | 2 | 3 | 4 | 5`. Menentukan sebuah rentang jauh lebih
singkat, terutama jika kita ingin mencocokkan, misalnya, angka berapa pun
antara 1 dan 1.000!

Compiler memeriksa bahwa rentang itu tidak kosong saat dikompilasi, dan karena
satu-satunya tipe yang bisa diketahui Rust apakah sebuah rentang kosong atau
tidak adalah `char` serta nilai numerik, rentang hanya diizinkan dengan nilai
numerik atau `char`.

Berikut contoh memakai rentang nilai `char`:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-04-ranges-of-char/src/main.rs:here}}
```

Rust bisa mengetahui bahwa `'c'` berada di dalam rentang pattern pertama dan
mencetak `early ASCII letter`.

### Destructuring untuk Memecah Nilai

Kita juga bisa memakai pattern untuk melakukan destructure terhadap struct,
enum, dan tuple agar bisa memakai bagian-bagian berbeda dari nilai tersebut.
Mari kita telusuri satu per satu.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-structs"></a>

#### Struct

Listing 19-12 menunjukkan struct `Point` dengan dua field, `x` dan `y`, yang
bisa kita pecah memakai sebuah pattern dengan pernyataan `let`.

<Listing number="19-12" file-name="src/main.rs" caption="Melakukan destructure field struct ke dalam variabel terpisah">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-12/src/main.rs}}
```

</Listing>

Kode ini membuat variabel `a` dan `b` yang cocok dengan nilai field `x` dan
`y` dari struct `p`. Contoh ini menunjukkan bahwa nama variabel di dalam
pattern tidak harus sama dengan nama field struct. Namun, lazimnya kita
menyamakan nama variabel dengan nama field agar lebih mudah diingat variabel
mana berasal dari field mana. Karena kebiasaan ini, dan karena menulis
`let Point { x: x, y: y } = p;` mengandung banyak pengulangan, Rust punya
singkatan untuk pattern yang cocok dengan field struct: kamu cukup mencantumkan
nama field struct, dan variabel yang dibuat dari pattern akan punya nama yang
sama. Listing 19-13 berperilaku sama dengan kode di Listing 19-12, tetapi
variabel yang dibuat dalam pattern `let` adalah `x` dan `y`, bukan `a` dan `b`.

<Listing number="19-13" file-name="src/main.rs" caption="Melakukan destructure field struct memakai singkatan field struct">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-13/src/main.rs}}
```

</Listing>

Kode ini membuat variabel `x` dan `y` yang cocok dengan field `x` dan `y` dari
variabel `p`. Hasilnya, variabel `x` dan `y` berisi nilai dari struct `p`.

Kita juga bisa melakukan destructure dengan nilai literal sebagai bagian dari
pattern struct, alih-alih membuat variabel untuk semua field. Dengan begitu,
kita bisa menguji beberapa field untuk nilai tertentu sambil membuat variabel
untuk melakukan destructure pada field lainnya.

Pada Listing 19-14, kita punya ekspresi `match` yang memisahkan nilai `Point`
ke dalam tiga kasus: titik yang terletak tepat di sumbu `x` (benar ketika
`y = 0`), di sumbu `y` (`x = 0`), atau tidak di kedua sumbu itu.

<Listing number="19-14" file-name="src/main.rs" caption="Melakukan destructure dan mencocokkan nilai literal dalam satu pattern">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-14/src/main.rs:here}}
```

</Listing>

Cabang pertama akan cocok dengan titik mana pun yang terletak di sumbu `x`
dengan menentukan bahwa field `y` cocok jika nilainya sama dengan literal `0`.
Pattern itu tetap membuat variabel `x` yang bisa kita pakai di kode cabang
tersebut.

Demikian pula, cabang kedua cocok dengan titik mana pun di sumbu `y` dengan
menentukan bahwa field `x` cocok jika nilainya `0`, dan membuat variabel `y`
untuk nilai field `y`. Cabang ketiga tidak menentukan literal apa pun, jadi ia
cocok dengan `Point` lainnya dan membuat variabel untuk field `x` maupun `y`.

Pada contoh ini, nilai `p` cocok dengan cabang kedua karena `x` berisi `0`,
sehingga kode ini akan mencetak `On the y axis at 7`.

Ingat bahwa ekspresi `match` berhenti memeriksa cabang begitu ia menemukan
pattern yang cocok pertama, jadi meskipun `Point { x: 0, y: 0 }` berada di
sumbu `x` dan sumbu `y`, kode ini hanya akan mencetak `On the x axis at 0`.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-enums"></a>

#### Enum

Kita sudah melakukan destructure terhadap enum dalam buku ini (misalnya,
Listing 6-5 di Bab 6), tetapi kita belum secara eksplisit membahas bahwa
pattern untuk melakukan destructure terhadap enum sesuai dengan cara data yang
tersimpan di dalam enum itu didefinisikan. Sebagai contoh, pada Listing 19-15,
kita memakai enum `Message` dari Listing 6-2 dan menulis `match` dengan pattern
yang akan melakukan destructure terhadap tiap nilai dalamnya.

<Listing number="19-15" file-name="src/main.rs" caption="Melakukan destructure varian enum yang menyimpan berbagai jenis nilai">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-15/src/main.rs}}
```

</Listing>

Kode ini akan mencetak `Change color to red 0, green 160, and blue 255`. Coba
ubah nilai `msg` untuk melihat kode dari cabang lain dijalankan.

Untuk varian enum yang tidak punya data sama sekali, seperti
`Message::Quit`, kita tidak bisa melakukan destructure lebih lanjut. Kita hanya
bisa mencocokkan nilai literal `Message::Quit`, dan tidak ada variabel dalam
pattern itu.

Untuk varian enum yang menyerupai struct, seperti `Message::Move`, kita bisa
memakai pattern yang mirip dengan pattern yang kita tulis untuk mencocokkan
struct. Setelah nama varian, kita menaruh kurung kurawal lalu mencantumkan
field beserta variabelnya agar kita bisa memecah bagian-bagiannya untuk dipakai
di kode cabang ini. Di sini kita memakai bentuk singkat seperti di Listing 19-13.

Untuk varian enum yang menyerupai tuple, seperti `Message::Write` yang menyimpan
tuple berisi satu elemen dan `Message::ChangeColor` yang menyimpan tuple berisi
tiga elemen, pattern-nya mirip dengan pattern yang kita tulis untuk mencocokkan
tuple. Jumlah variabel dalam pattern harus sama dengan jumlah elemen pada
varian yang kita cocokkan.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-nested-structs-and-enums"></a>

#### Struct dan Enum Bersarang

Sejauh ini, semua contoh kita mencocokkan struct atau enum hanya satu level,
tetapi pencocokan juga bisa bekerja pada item bersarang! Misalnya, kita bisa
merefaktor kode di Listing 19-15 agar mendukung warna RGB dan HSV pada pesan
`ChangeColor`, seperti yang ditunjukkan Listing 19-16.

<Listing number="19-16" caption="Mencocokkan enum bersarang">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-16/src/main.rs}}
```

</Listing>

Pattern pada cabang pertama dalam ekspresi `match` cocok dengan varian enum
`Message::ChangeColor` yang berisi varian `Color::Rgb`; lalu, pattern itu
mengikat ketiga nilai `i32` di dalamnya. Pattern pada cabang kedua juga cocok
dengan varian enum `Message::ChangeColor`, tetapi enum di dalamnya cocok dengan
`Color::Hsv` sebagai gantinya. Kita bisa menentukan kondisi yang kompleks ini
dalam satu ekspresi `match`, meskipun dua enum terlibat di sini.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-structs-and-tuples"></a>

#### Struct dan Tuple

Kita bisa mencampur, mencocokkan, dan menyarangkan pattern destructuring dengan
cara yang lebih kompleks lagi. Contoh berikut menunjukkan destructure yang
rumit, di mana kita menyarangkan struct dan tuple di dalam sebuah tuple lalu
melakukan destructure terhadap semua nilai primitifnya:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-05-destructuring-structs-and-tuples/src/main.rs:here}}
```

Kode ini memungkinkan kita memecah tipe yang kompleks menjadi bagian-bagian
penyusunnya agar bisa memakai nilai yang kita minati secara terpisah.

Melakukan destructure dengan pattern adalah cara praktis untuk memakai
bagian-bagian nilai, misalnya nilai dari tiap field dalam struct, secara
terpisah satu sama lain.

<a id="ignoring-values-in-a-pattern"></a>
### Mengabaikan Nilai dalam Pattern

Kamu sudah melihat bahwa kadang berguna untuk mengabaikan nilai dalam pattern,
misalnya pada cabang terakhir sebuah `match`, untuk mendapatkan penampung semua
(*catch-all*) yang sebenarnya tidak melakukan apa pun tetapi tetap memperhitungkan
semua nilai yang tersisa. Ada beberapa cara untuk mengabaikan seluruh nilai atau
bagian dari nilai dalam pattern: memakai pattern `_` (yang sudah kamu lihat),
memakai pattern `_` di dalam pattern lain, memakai nama yang diawali garis
bawah, atau memakai `..` untuk mengabaikan bagian nilai yang tersisa. Mari kita
jelajahi cara dan alasan memakai masing-masing pattern ini.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-an-entire-value-with-_"></a>

#### Seluruh Nilai dengan `_`

Kita sudah memakai garis bawah sebagai pattern wildcard yang cocok dengan nilai
apa pun tetapi tidak mengikat nilai itu. Ini sangat berguna sebagai cabang
terakhir dalam ekspresi `match`, tetapi kita juga bisa memakainya di pattern
mana pun, termasuk parameter fungsi, seperti yang ditunjukkan Listing 19-17.

<Listing number="19-17" file-name="src/main.rs" caption="Memakai `_` dalam tanda tangan fungsi">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-17/src/main.rs}}
```

</Listing>

Kode ini akan sepenuhnya mengabaikan nilai `3` yang dilewatkan sebagai argumen
pertama, dan akan mencetak `This code only uses the y parameter: 4`.

Pada kebanyakan kasus, saat kamu tidak lagi membutuhkan parameter fungsi
tertentu, kamu akan mengubah tanda tangannya agar tidak menyertakan parameter
yang tidak terpakai itu. Mengabaikan parameter fungsi bisa sangat berguna dalam
kasus-kasus seperti saat kamu mengimplementasikan trait ketika kamu memerlukan
tanda tangan tipe tertentu, tetapi isi fungsi dalam implementasimu tidak
membutuhkan salah satu parameternya. Dengan begitu, kamu terhindar dari
peringatan compiler tentang parameter fungsi yang tidak terpakai, yang akan
kamu dapatkan jika memakai sebuah nama.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-parts-of-a-value-with-a-nested-_"></a>

#### Bagian dari Nilai dengan `_` Bersarang

Kita juga bisa memakai `_` di dalam pattern lain untuk mengabaikan hanya
sebagian nilai, misalnya ketika kita ingin menguji hanya sebagian nilai tetapi
tidak memerlukan bagian lainnya dalam kode yang ingin kita jalankan. Listing
19-18 menunjukkan kode yang mengelola nilai sebuah pengaturan. Kebutuhan
bisnisnya adalah pengguna tidak boleh menimpa kustomisasi yang sudah ada pada
sebuah pengaturan, tetapi boleh mengosongkan pengaturan itu dan memberinya nilai
jika saat ini pengaturan tersebut kosong.

<Listing number="19-18" caption="Memakai garis bawah di dalam pattern yang cocok dengan varian `Some` ketika kita tidak perlu memakai nilai di dalam `Some`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-18/src/main.rs:here}}
```

</Listing>

Kode ini akan mencetak `Can't overwrite an existing customized value` lalu
`setting is Some(5)`. Pada cabang match pertama, kita tidak perlu mencocokkan
atau memakai nilai di salah pun varian `Some`, tetapi kita perlu menguji kasus
ketika `setting_value` dan `new_setting_value` adalah varian `Some`. Dalam
kasus itu, kita mencetak alasan mengapa `setting_value` tidak diubah, dan
nilainya tidak berubah.

Pada semua kasus lain (jika `setting_value` atau `new_setting_value` adalah
`None`) yang dinyatakan oleh pattern `_` di cabang kedua, kita ingin mengizinkan
`new_setting_value` menjadi `setting_value`.

Kita juga bisa memakai garis bawah di beberapa tempat dalam satu pattern untuk
mengabaikan nilai-nilai tertentu. Listing 19-19 menunjukkan contoh mengabaikan
nilai kedua dan keempat dalam tuple berisi lima item.

<Listing number="19-19" caption="Mengabaikan beberapa bagian dari tuple">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-19/src/main.rs:here}}
```

</Listing>

Kode ini akan mencetak `Some numbers: 2, 8, 32`, dan nilai `4` serta `16` akan
diabaikan.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-an-unused-variable-by-starting-its-name-with-_"></a>

#### Variabel yang Tidak Dipakai dengan Mengawali Namanya dengan `_`

Jika kamu membuat variabel tetapi tidak memakainya di mana pun, Rust biasanya
akan mengeluarkan peringatan karena variabel yang tidak terpakai bisa jadi
sebuah bug. Namun, kadang berguna untuk bisa membuat variabel yang belum akan
kamu pakai, misalnya saat kamu sedang membuat prototipe atau baru memulai
sebuah proyek. Dalam situasi ini, kamu bisa memberi tahu Rust agar tidak
memberi peringatan tentang variabel yang tidak terpakai itu dengan mengawali
nama variabelnya dengan garis bawah. Pada Listing 19-20, kita membuat dua
variabel yang tidak terpakai, tetapi saat mengompilasi kode ini, kita seharusnya
hanya mendapat satu peringatan untuk salah satunya.

<Listing number="19-20" file-name="src/main.rs" caption="Mengawali nama variabel dengan garis bawah untuk menghindari peringatan variabel tidak terpakai">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-20/src/main.rs}}
```

</Listing>

Di sini, kita mendapat peringatan karena tidak memakai variabel `y`, tetapi kita
tidak mendapat peringatan karena tidak memakai `_x`.

Perhatikan bahwa ada perbedaan halus antara memakai hanya `_` dan memakai nama
yang diawali garis bawah. Sintaksis `_x` tetap mengikat nilai ke variabel,
sedangkan `_` sama sekali tidak mengikat. Untuk menunjukkan kasus di mana
perbedaan ini penting, Listing 19-21 akan memberi kita sebuah error.

<Listing number="19-21" caption="Variabel tidak terpakai yang diawali garis bawah tetap mengikat nilai, yang bisa saja mengambil ownership nilai itu.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-21/src/main.rs:here}}
```

</Listing>

Kita akan menerima error karena nilai `s` tetap akan dipindahkan ke `_s`, yang
mencegah kita memakai `s` lagi. Namun, memakai garis bawah sendirian tidak
pernah mengikat ke nilai. Listing 19-22 akan dikompilasi tanpa error apa pun
karena `s` tidak dipindahkan ke `_`.

<Listing number="19-22" caption="Memakai garis bawah tidak mengikat nilai.">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-22/src/main.rs:here}}
```

</Listing>

Kode ini bekerja dengan baik karena kita tidak pernah mengikat `s` ke apa pun;
nilainya tidak dipindahkan.

<a id="ignoring-remaining-parts-of-a-value-with-"></a>

#### Bagian Nilai yang Tersisa dengan `..`

Pada nilai yang punya banyak bagian, kita bisa memakai sintaksis `..` untuk
memakai bagian tertentu dan mengabaikan sisanya, sehingga tidak perlu
mencantumkan garis bawah untuk setiap nilai yang diabaikan. Pattern `..`
mengabaikan bagian mana pun dari nilai yang belum kita cocokkan secara eksplisit
di bagian pattern lainnya. Pada Listing 19-23, kita punya struct `Point` yang
menyimpan koordinat dalam ruang tiga dimensi. Dalam ekspresi `match`, kita ingin
hanya beroperasi pada koordinat `x` dan mengabaikan nilai pada field `y` dan
`z`.

<Listing number="19-23" caption="Mengabaikan semua field `Point` kecuali `x` dengan memakai `..`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-23/src/main.rs:here}}
```

</Listing>

Kita mencantumkan nilai `x` lalu cukup menyertakan pattern `..`. Ini lebih
cepat daripada harus menulis `y: _` dan `z: _`, terutama ketika kita bekerja
dengan struct yang punya banyak field dalam situasi yang hanya satu atau dua
field yang relevan.

Sintaksis `..` akan mengembang menjadi sebanyak nilai yang dibutuhkannya.
Listing 19-24 menunjukkan cara memakai `..` dengan tuple.

<Listing number="19-24" file-name="src/main.rs" caption="Mencocokkan hanya nilai pertama dan terakhir dalam tuple dan mengabaikan semua nilai lainnya">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-24/src/main.rs}}
```

</Listing>

Pada kode ini, nilai pertama dan terakhir dicocokkan dengan `first` dan `last`.
`..` akan cocok dengan dan mengabaikan semua yang ada di tengah.

Namun, memakai `..` harus tidak ambigu. Jika tidak jelas nilai mana yang
dimaksud untuk dicocokkan dan mana yang harus diabaikan, Rust akan memberi kita
error. Listing 19-25 menunjukkan contoh pemakaian `..` yang ambigu, jadi kode
ini tidak akan dikompilasi.

<Listing number="19-25" file-name="src/main.rs" caption="Sebuah percobaan memakai `..` dengan cara yang ambigu">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-25/src/main.rs}}
```

</Listing>

Saat kita mengompilasi contoh ini, kita mendapat error ini:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-25/output.txt}}
```

Mustahil bagi Rust untuk menentukan berapa banyak nilai dalam tuple yang harus
diabaikan sebelum mencocokkan sebuah nilai dengan `second`, lalu berapa banyak
nilai lagi yang harus diabaikan setelahnya. Kode ini bisa berarti kita ingin
mengabaikan `2`, mengikat `second` ke `4`, lalu mengabaikan `8`, `16`, dan `32`;
atau bahwa kita ingin mengabaikan `2` dan `4`, mengikat `second` ke `8`, lalu
mengabaikan `16` dan `32`; dan seterusnya. Nama variabel `second` tidak punya
arti khusus bagi Rust, jadi kita mendapat error compiler karena memakai `..` di
dua tempat seperti ini adalah hal yang ambigu.

<!-- Old headings. Do not remove or links may break. -->

<a id="extra-conditionals-with-match-guards"></a>

<a id="adding-conditionals-with-match-guards"></a>
### Menambahkan Kondisi dengan Match Guards

Sebuah _match guard_ adalah kondisi `if` tambahan, yang ditentukan setelah
pattern dalam cabang `match`, yang juga harus cocok agar cabang itu dipilih.
Match guard berguna untuk menyampaikan ide yang lebih kompleks daripada yang
bisa dilakukan oleh pattern saja. Perlu dicatat, namun, bahwa match guard hanya
tersedia dalam ekspresi `match`, bukan ekspresi `if let` atau `while let`.

Kondisi itu bisa memakai variabel yang dibuat dalam pattern. Listing 19-26
menunjukkan sebuah `match` yang cabang pertamanya punya pattern `Some(x)` dan
juga punya match guard `if x % 2 == 0` (yang akan bernilai `true` jika angkanya
genap).

<Listing number="19-26" caption="Menambahkan match guard ke sebuah pattern">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-26/src/main.rs:here}}
```

</Listing>

Contoh ini akan mencetak `The number 4 is even`. Saat `num` dibandingkan dengan
pattern di cabang pertama, keduanya cocok karena `Some(4)` cocok dengan
`Some(x)`. Lalu, match guard memeriksa apakah sisa hasil bagi `x` dengan 2 sama
dengan 0, dan karena memang sama, cabang pertama dipilih.

Seandainya `num` adalah `Some(5)`, match guard di cabang pertama akan bernilai
`false` karena sisa 5 dibagi 2 adalah 1, yang tidak sama dengan 0. Rust lalu
akan lanjut ke cabang kedua, yang cocok karena cabang kedua tidak punya match
guard dan karena itu cocok dengan varian `Some` apa pun.

Tidak ada cara untuk menyampaikan kondisi `if x % 2 == 0` di dalam sebuah
pattern, jadi match guard memberi kita kemampuan untuk menyatakan logika ini.
Kelemahan dari ekspresivitas tambahan ini adalah compiler tidak mencoba
memeriksa kehabisan (*exhaustiveness*) ketika ekspresi match guard terlibat.

Saat membahas Listing 19-11, kita menyebut bahwa kita bisa memakai match guard
untuk menyelesaikan masalah penutupan pattern kita. Ingat bahwa kita membuat
variabel baru di dalam pattern pada ekspresi `match`, alih-alih memakai variabel
di luar `match`. Variabel baru itu berarti kita tidak bisa menguji nilai variabel
luar. Listing 19-27 menunjukkan cara memakai match guard untuk memperbaiki
masalah ini.

<Listing number="19-27" file-name="src/main.rs" caption="Memakai match guard untuk menguji kesetaraan dengan variabel luar">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-27/src/main.rs}}
```

</Listing>

Kode ini sekarang akan mencetak `Default case, x = Some(5)`. Pattern di cabang
match kedua tidak memperkenalkan variabel baru `y` yang akan menutupi `y` luar,
yang berarti kita bisa memakai `y` luar di dalam match guard. Alih-alih
menentukan pattern sebagai `Some(y)`, yang akan menutupi `y` luar, kita
menentukan `Some(n)`. Ini membuat variabel baru `n` yang tidak menutupi apa pun
karena tidak ada variabel `n` di luar `match`.

Match guard `if n == y` bukan sebuah pattern dan karena itu tidak memperkenalkan
variabel baru. `y` ini _adalah_ `y` luar, bukan `y` baru yang menutupinya, dan
kita bisa mencari nilai yang sama dengan `y` luar dengan membandingkan `n` dan
`y`.

Kamu juga bisa memakai operator _atau_ (`or`) `|` dalam match guard untuk
menentukan beberapa pattern; kondisi match guard akan berlaku untuk semua
pattern itu. Listing 19-28 menunjukkan prioritas saat menggabungkan pattern yang
memakai `|` dengan match guard. Bagian penting dari contoh ini adalah match
guard `if y` berlaku untuk `4`, `5`, _dan_ `6`, meskipun sekilas tampak seperti
`if y` hanya berlaku untuk `6`.

<Listing number="19-28" caption="Menggabungkan beberapa pattern dengan match guard">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-28/src/main.rs:here}}
```

</Listing>

Kondisi match menyatakan bahwa cabang hanya cocok jika nilai `x` sama dengan
`4`, `5`, atau `6` _dan_ jika `y` bernilai `true`. Saat kode ini dijalankan,
pattern cabang pertama cocok karena `x` adalah `4`, tetapi match guard `if y`
bernilai `false`, jadi cabang pertama tidak dipilih. Kode lanjut ke cabang
kedua, yang memang cocok, dan program ini mencetak `no`. Alasannya adalah
kondisi `if` berlaku untuk seluruh pattern `4 | 5 | 6`, bukan hanya nilai
terakhir `6`. Dengan kata lain, prioritas match guard terhadap sebuah pattern
berperilaku seperti ini:

```text
(4 | 5 | 6) if y => ...
```

bukan seperti ini:

```text
4 | 5 | (6 if y) => ...
```

Setelah menjalankan kode, perilaku prioritas itu menjadi jelas: Seandainya match
guard diterapkan hanya pada nilai terakhir dalam daftar nilai yang ditentukan
memakai operator `|`, cabang itu akan cocok dan program akan mencetak `yes`.

<!-- Old headings. Do not remove or links may break. -->

<a id="-bindings"></a>

### Memakai Binding `@`

Operator _at_ `@` memungkinkan kita membuat variabel yang menyimpan sebuah nilai
pada saat yang sama ketika kita menguji nilai itu untuk pencocokan pattern. Pada
Listing 19-29, kita ingin menguji apakah field `id` dari `Message::Hello`
berada dalam rentang `3..=7`. Kita juga ingin mengikat nilai itu ke variabel
`id` agar bisa memakainya di kode yang terkait dengan cabang tersebut.

<Listing number="19-29" caption="Memakai `@` untuk mengikat nilai dalam pattern sembari mengujinya">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-29/src/main.rs:here}}
```

</Listing>

Contoh ini akan mencetak `Found an id in range: 5`. Dengan menentukan `id @`
sebelum rentang `3..=7`, kita menangkap nilai apa pun yang cocok dengan rentang
itu ke dalam variabel bernama `id`, sembari menguji bahwa nilainya memang cocok
dengan pattern rentang tersebut.

Pada cabang kedua, di mana pattern hanya menentukan sebuah rentang, kode yang
terkait dengan cabang itu tidak punya variabel yang berisi nilai aktual dari
field `id`. Nilai field `id` bisa saja 10, 11, atau 12, tetapi kode yang mengikuti
pattern itu tidak tahu mana yang benar. Kode pattern itu tidak bisa memakai nilai
dari field `id` karena kita tidak menyimpan nilai `id` ke dalam variabel.

Pada cabang terakhir, di mana kita menentukan sebuah variabel tanpa rentang, kita
memang punya nilai yang bisa dipakai di kode cabang dalam variabel bernama `id`.
Alasannya adalah kita memakai sintaksis singkatan field struct. Namun, kita tidak
menerapkan pengujian apa pun pada nilai field `id` di cabang ini, seperti yang
kita lakukan di dua cabang pertama: nilai apa pun akan cocok dengan pattern ini.

Memakai `@` memungkinkan kita menguji sebuah nilai dan menyimpannya dalam
variabel di dalam satu pattern.

## Ringkasan

Pattern Rust sangat berguna untuk membedakan berbagai jenis data. Saat dipakai
dalam ekspresi `match`, Rust memastikan bahwa pattern-mu mencakup setiap nilai
yang mungkin, atau programmu tidak akan dikompilasi. Pattern dalam pernyataan
`let` dan parameter fungsi membuat konstruksi itu lebih berguna, memungkinkan
nilai dipecah menjadi bagian-bagian lebih kecil dan bagian-bagian itu ditetapkan
ke variabel. Kita bisa membuat pattern sederhana maupun kompleks sesuai
kebutuhan kita.

Selanjutnya, untuk bab kedua dari akhir buku ini, kita akan melihat beberapa
aspek lanjutan dari beragam fitur Rust.
