## Fungsi

Fungsi sangat lazim di kode Rust. Kamu sudah melihat salah satu fungsi paling
penting dalam bahasa ini: fungsi `main`, yang menjadi titik masuk banyak program.
Kamu juga sudah melihat keyword `fn`, yang dipakai untuk mendeklarasikan fungsi
baru.

Kode Rust memakai _snake case_ sebagai gaya baku untuk nama fungsi dan variabel:
semua huruf ditulis kecil dan kata-kata dipisahkan oleh garis bawah. Berikut
program yang memuat contoh definisi fungsi:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-16-functions/src/main.rs}}
```

Kita mendefinisikan fungsi di Rust dengan menulis `fn`, diikuti nama fungsi dan
sepasang tanda kurung. Kurung kurawal memberi tahu compiler di mana badan fungsi
dimulai dan berakhir.

Kita bisa memanggil fungsi apa pun yang sudah kita definisikan dengan menulis
namanya, lalu sepasang tanda kurung. Karena `another_function` didefinisikan di
dalam program, fungsi itu bisa dipanggil dari dalam fungsi `main`. Perhatikan
bahwa kita mendefinisikan `another_function` _setelah_ fungsi `main` di kode
sumber; kita juga bisa mendefinisikannya sebelumnya. Rust tidak peduli di mana
kamu mendefinisikan fungsi-fungsimu, asalkan fungsi tersebut didefinisikan di
suatu scope yang bisa dilihat oleh pemanggil.

Mari kita mulai proyek biner baru bernama _functions_ untuk mengeksplorasi fungsi
lebih jauh. Letakkan contoh `another_function` di _src/main.rs_ lalu jalankan.
Kamu akan melihat output berikut:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-16-functions/output.txt}}
```

Baris-baris dieksekusi sesuai urutan kemunculannya di dalam fungsi `main`.
Pertama, pesan “Hello, world!” dicetak, lalu `another_function` dipanggil dan
pesan dari fungsi itu dicetak.

### Parameter

Kita bisa mendefinisikan fungsi yang memiliki _parameter_, yaitu variabel khusus
yang menjadi bagian dari signature fungsi. Ketika sebuah fungsi punya parameter,
kamu bisa memberinya nilai konkret untuk parameter tersebut. Secara teknis, nilai
konkret itu disebut _argumen_, tapi dalam percakapan sehari-hari orang cenderung
memakai kata _parameter_ dan _argumen_ secara bergantian, baik untuk variabel di
definisi maupun untuk nilai konkret yang dikirim saat memanggil fungsi.

Pada versi `another_function` berikut, kita menambahkan satu parameter:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/src/main.rs}}
```

Coba jalankan program ini; kamu akan mendapatkan output berikut:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/output.txt}}
```

Deklarasi `another_function` punya satu parameter bernama `x`. Tipe `x`
ditentukan sebagai `i32`. Saat kita mengirim `5` ke `another_function`, macro
`println!` menempatkan `5` di tempat pasangan kurung kurawal berisi `x` pada
format string.

Di dalam signature fungsi, kamu _wajib_ mendeklarasikan tipe setiap parameter.
Ini adalah keputusan yang disengaja dalam desain Rust: mewajibkan anotasi tipe
di definisi fungsi berarti hampir tidak pernah ada situasi di mana compiler
meminta kamu menuliskan anotasi itu di bagian kode lain untuk menentukan tipe
yang kamu maksud. Compiler juga bisa memberi pesan error yang lebih membantu
jika ia mengetahui tipe apa yang diharapkan sebuah fungsi.

Saat mendefinisikan beberapa parameter, pisahkan deklarasi parameter dengan koma,
seperti ini:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/src/main.rs}}
```

Contoh ini membuat fungsi bernama `print_labeled_measurement` dengan dua
parameter. Parameter pertama bernama `value` bertipe `i32`. Parameter kedua
bernama `unit_label` bertipe `char`. Fungsi itu lalu mencetak teks yang memuat
baik `value` maupun `unit_label`.

Mari kita jalankan kode ini. Ganti isi file _src/main.rs_ di proyek _functions_
kamu dengan contoh di atas, lalu jalankan dengan `cargo run`:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/output.txt}}
```

Karena kita memanggil fungsi tersebut dengan `5` sebagai nilai `value` dan `'h'`
sebagai nilai `unit_label`, output program memuat kedua nilai itu.

### Statement dan Ekspresi

Badan fungsi tersusun dari serangkaian statement yang secara opsional diakhiri
sebuah ekspresi. Sejauh ini, fungsi-fungsi yang kita bahas belum memuat ekspresi
penutup, tapi kamu sudah melihat ekspresi sebagai bagian dari sebuah statement.
Karena Rust adalah bahasa berbasis ekspresi, perbedaan ini penting untuk kamu
pahami. Bahasa lain tidak punya pemisahan yang sama, jadi mari kita lihat apa
itu statement dan ekspresi, serta bagaimana perbedaan keduanya memengaruhi badan
fungsi.

- _Statement_ adalah instruksi yang menjalankan suatu aksi dan tidak
  mengembalikan nilai.
- _Ekspresi_ dievaluasi menjadi nilai hasil.

Mari kita lihat beberapa contoh.

Sebenarnya kita sudah memakai statement dan ekspresi. Membuat variabel dan
membuatkannya sebuah nilai dengan keyword `let` adalah sebuah statement. Pada
Listing 3-1, `let y = 6;` adalah sebuah statement.

<Listing number="3-1" file-name="src/main.rs" caption="A `main` function declaration containing one statement">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-01/src/main.rs}}
```

</Listing>

Definisi fungsi juga merupakan statement; seluruh contoh di atas adalah sebuah
statement dengan sendirinya. (Seperti yang akan kita lihat sebentar lagi,
memanggil fungsi bukanlah statement, meski begitu.)

Statement tidak mengembalikan nilai. Karena itu, kamu tidak bisa memberikan
sebuah statement `let` ke variabel lain, seperti yang dicoba kode berikut; kamu
akan mendapatkan error:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/src/main.rs}}
```

Saat kamu menjalankan program ini, error yang muncul akan terlihat seperti ini:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/output.txt}}
```

Statement `let y = 6` tidak mengembalikan nilai, jadi tidak ada apa pun yang
bisa diikat oleh `x`. Ini berbeda dari yang terjadi di bahasa lain, seperti C
dan Ruby, di mana penugasan mengembalikan nilai yang ditugaskan. Di bahasa-bahasa
itu, kamu bisa menulis `x = y = 6` dan membuat `x` dan `y` sama-sama bernilai `6`; hal
itu tidak berlaku di Rust.

Ekspresi dievaluasi menjadi sebuah nilai dan menyusun sebagian besar sisa kode
yang akan kamu tulis di Rust. Pertimbangkan operasi aritmetika, seperti `5 + 6`,
yang merupakan ekspresi yang dievaluasi menjadi nilai `11`. Ekspresi bisa menjadi
bagian dari sebuah statement: Pada Listing 3-1, angka `6` pada statement
`let y = 6;` adalah ekspresi yang dievaluasi menjadi nilai `6`. Memanggil sebuah
fungsi adalah ekspresi. Memanggil macro adalah ekspresi. Blok scope baru yang
dibuat dengan kurung kurawal juga merupakan ekspresi, misalnya:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-20-blocks-are-expressions/src/main.rs}}
```

Ekspresi berikut:

```rust,ignore
{
    let x = 3;
    x + 1
}
```

adalah sebuah blok yang, pada kasus ini, dievaluasi menjadi `4`. Nilai itu
diikat ke `y` sebagai bagian dari statement `let`. Perhatikan baris `x + 1` yang
tidak diakhiri titik koma, berbeda dari kebanyakan baris yang kamu lihat sejauh
ini. Ekspresi tidak diakhiri titik koma. Jika kamu menambahkan titik koma di
akhir sebuah ekspresi, kamu mengubahnya menjadi statement, dan statement itu
tidak akan mengembalikan nilai. Ingat hal ini saat kamu mengeksplorasi nilai
kembalian fungsi dan ekspresi pada bagian berikut.

### Fungsi dengan Nilai Kembalian

Fungsi bisa mengembalikan nilai ke kode yang memanggilnya. Kita tidak memberi
nama pada nilai kembalian, tapi kita wajib mendeklarasikan tipenya setelah tanda
panah (`->`). Di Rust, nilai kembalian sebuah fungsi identik dengan nilai dari
ekspresi terakhir di dalam blok badan fungsi. Kamu bisa keluar lebih awal dari
sebuah fungsi dengan memakai keyword `return` dan menyebutkan sebuah nilai,
tapi sebagian besar fungsi mengembalikan ekspresi terakhir secara implisit.
Berikut contoh fungsi yang mengembalikan sebuah nilai:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/src/main.rs}}
```

Tidak ada pemanggilan fungsi, macro, atau bahkan statement `let` di dalam fungsi
`five`—hanya angka `5` yang berdiri sendiri. Itu adalah fungsi yang sepenuhnya
valid di Rust. Perhatikan bahwa tipe kembalian fungsi juga dideklarasikan, yaitu
`-> i32`. Coba jalankan kode ini; outputnya akan terlihat seperti ini:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/output.txt}}
```

Angka `5` di dalam `five` adalah nilai kembalian fungsi tersebut, itulah
mengapa tipe kembaliannya `i32`. Mari kita bahas ini lebih rinci. Ada dua bagian
penting: Pertama, baris `let x = five();` menunjukkan bahwa kita memakai nilai
kembalian sebuah fungsi untuk menginisialisasi sebuah variabel. Karena fungsi
`five` mengembalikan `5`, baris itu sama dengan baris berikut:

```rust
let x = 5;
```

Kedua, fungsi `five` tidak punya parameter dan mendefinisikan tipe nilai
kembalian, tapi badan fungsi itu hanya berisi angka `5` yang kesepian tanpa
titik koma, karena angka itu adalah ekspresi yang nilainya ingin kita kembalikan.

Mari kita lihat contoh lain:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-22-function-parameter-and-return/src/main.rs}}
```

Menjalankan kode ini akan mencetak `The value of x is: 6`. Tapi apa yang terjadi
jika kita menambahkan titik koma di akhir baris yang memuat `x + 1`, sehingga
baris itu berubah dari ekspresi menjadi statement?

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/src/main.rs}}
```

Mengompilasi kode ini akan menghasilkan error sebagai berikut:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/output.txt}}
```

Pesan error utama, `mismatched types`, menyingkap inti masalah dari kode ini.
Definisi fungsi `plus_one` menyatakan bahwa fungsi itu akan mengembalikan sebuah
`i32`, tapi statement tidak dievaluasi menjadi sebuah nilai, yang dinyatakan oleh
`()`, tipe unit. Karena itu, tidak ada nilai yang dikembalikan, dan hal itu
bertentangan dengan definisi fungsi sehingga menghasilkan error. Pada output ini,
Rust memberikan pesan yang mungkin bisa membantu memperbaiki masalah tersebut:
Rust menyarankan untuk menghapus titik koma, yang akan memperbaiki error itu.
