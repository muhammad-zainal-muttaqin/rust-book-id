## Alur Kontrol Ringkas dengan `if let` dan `let...else`

Sintaks `if let` memungkinkan kamu menggabungkan `if` dan `let` menjadi cara yang
lebih ringkas untuk menangani nilai yang cocok dengan satu pola sementara
mengabaikan sisanya. Perhatikan program pada Listing 6-6 yang melakukan match
pada nilai `Option<u8>` di variabel `config_max`, tetapi hanya ingin mengeksekusi
kode jika nilai tersebut adalah varian `Some`.

<Listing number="6-6" caption="Sebuah `match` yang hanya peduli mengeksekusi kode ketika nilainya `Some`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-06/src/main.rs:here}}
```

</Listing>

Jika nilainya `Some`, kita mencetak nilai di dalam varian `Some` dengan
mengikat nilai tersebut ke variabel `max` di dalam pola. Kita tidak ingin
melakukan apa pun dengan nilai `None`. Untuk memenuhi ekspresi `match`, kita harus
menambahkan `_ => ()` setelah memproses hanya satu varian, dan itu adalah
boilerplate yang menyebalkan untuk ditambahkan.

Sebagai gantinya, kita bisa menulisnya dengan cara yang lebih pendek memakai
`if let`. Kode berikut berperilaku sama dengan `match` di Listing 6-6:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-12-if-let/src/main.rs:here}}
```

Sintaks `if let` menerima sebuah pola dan sebuah ekspresi yang dipisahkan oleh
tanda sama dengan. Cara kerjanya sama dengan `match`, di mana ekspresi tersebut
diberikan ke `match` dan polanya adalah arm pertamanya. Dalam kasus ini, polanya
adalah `Some(max)`, dan `max` terikat ke nilai di dalam `Some`. Setelah itu kita
bisa memakai `max` di dalam blok `if let` dengan cara yang sama seperti kita
memakai `max` di arm `match` yang bersangkutan. Kode di dalam blok `if let`
hanya berjalan jika nilai tersebut cocok dengan pola.

Memakai `if let` berarti lebih sedikit mengetik, lebih sedikit indentasi, dan
lebih sedikit boilerplate. Namun, kamu kehilangan pengecekan menyeluruh yang
dipaksakan `match`, yang memastikan kamu tidak lupa menangani satu kasus pun.
Pilihan antara `match` dan `if let` tergantung pada apa yang sedang kamu kerjakan
dalam situasi tertentu, dan apakah keuntungan dari sisi kerapian sepadan dengan
kehilangan pengecekan menyeluruh.

Dengan kata lain, kamu bisa memperlakukan `if let` sebagai gula sintaks untuk
sebuah `match` yang menjalankan kode ketika nilai cocok dengan satu pola, lalu
mengabaikan semua nilai lainnya.

Kita bisa menambahkan `else` pada sebuah `if let`. Blok kode yang menyertai
`else` sama dengan blok kode yang akan menyertai kasus `_` pada ekspresi `match`
yang setara dengan `if let` dan `else` tersebut. Ingat kembali definisi enum
`Coin` di Listing 6-4, di mana varian `Quarter` juga menyimpan sebuah nilai
`UsState`. Jika kita ingin menghitung semua koin selain quarter yang kita lihat
sekaligus mengumumkan negara bagi setiap quarter, kita bisa melakukannya dengan
ekspresi `match` seperti ini:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-13-count-and-announce-match/src/main.rs:here}}
```

Atau kita bisa memakai ekspresi `if let` dan `else`, seperti ini:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-14-count-and-announce-if-let-else/src/main.rs:here}}
```

## Tetap di “Jalur Bahagia” dengan `let...else`

Pola yang umum adalah melakukan sejumlah komputasi ketika sebuah nilai tersedia,
dan mengembalikan nilai default sebaliknya. Menyinggung contoh koin dengan nilai
`UsState` tadi, jika kita ingin mengatakan sesuatu yang lucu tergantung pada
seberapa tua negara pada quarter tersebut, kita bisa menambahkan sebuah method
pada `UsState` untuk memeriksa usia sebuah negara, seperti ini:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:state}}
```

Lalu, kita bisa memakai `if let` untuk match pada jenis koin, dengan memperkenalkan
sebuah variabel `state` di dalam body kondisi tersebut, seperti di Listing 6-7.

<Listing number="6-7" caption="Memeriksa apakah sebuah negara sudah ada pada tahun 1900 dengan kondisi bersarang di dalam sebuah `if let`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:describe}}
```

</Listing>

Cara itu sudah cukup, tetapi pekerjanya didorong ke dalam body statement
`if let`. Jika pekerjaan yang harus dilakukan lebih rumit, bisa jadi sulit
mengikuti bagaimana cabang-cabang di tingkat atas saling berkaitan. Kita juga
bisa memanfaatkan kenyataan bahwa ekspresi menghasilkan sebuah nilai, baik untuk
menghasilkan `state` dari `if let` maupun untuk mengembalikan lebih awal, seperti
di Listing 6-8. (Kamu juga bisa melakukan hal serupa dengan `match`, tentu saja.)

<Listing number="6-8" caption="Memakai `if let` untuk menghasilkan sebuah nilai atau mengembalikan lebih awal">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-08/src/main.rs:describe}}
```

</Listing>

Ini pun sedikit menyebalkan untuk diikuti dengan caranya sendiri! Satu cabang
`if let` menghasilkan sebuah nilai, sementara cabang lainnya mengembalikan
keluar dari fungsi sepenuhnya.

Untuk membuat pola umum ini lebih enak diekspresikan, Rust punya `let...else`.
Sintaks `let...else` menerima sebuah pola di sisi kiri dan sebuah ekspresi di
sisi kanan, sangat mirip dengan `if let`, tetapi tanpa cabang `if`, hanya ada
cabang `else`. Jika polanya cocok, ia akan mengikat nilai dari pola tersebut ke
scope luar. Jika polanya _tidak_ cocok, program akan mengalir ke arm `else`,
yang harus mengembalikan keluar dari fungsi.

Di Listing 6-9, kamu bisa melihat bagaimana tampilan Listing 6-8 ketika memakai
`let...else` menggantikan `if let`.

<Listing number="6-9" caption="Memakai `let...else` untuk memperjelas alur melalui fungsi">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-09/src/main.rs:describe}}
```

</Listing>

Perhatikan bahwa dengan cara ini ia tetap berada di “jalur bahagia” pada body
utama fungsi, tanpa harus punya alur kontrol yang jauh berbeda untuk dua cabang
sebagaimana halnya `if let`.

Jika kamu menghadapi situasi di mana logika programmu terlalu panjang untuk
diekspresikan dengan `match`, ingatlah bahwa `if let` dan `let...else` juga ada
di kotak perkakasmu sebagai programmer Rust.

## Ringkasan

Kita telah membahas cara memakai enum untuk membuat tipe kustom yang bisa menjadi
salah satu dari sekumpulan nilai berenumerasi. Kita telah menunjukkan bagaimana
tipe `Option<T>` dari standard library membantumu memakai sistem tipe untuk
mencegah error. Ketika nilai enum memiliki data di dalamnya, kamu bisa memakai
`match` atau `if let` untuk mengekstrak dan memakai nilai-nilai tersebut,
tergantung pada berapa banyak kasus yang perlu kamu tangani.

Program Rust-mu kini bisa mengekspresikan konsep di domainmu memakai struct dan
enum. Membuat tipe kustom untuk dipakai di API-mu memastikan tipe aman: compiler
akan memastikan fungsi-fungsimu hanya menerima nilai dengan tipe yang diharapkan
oleh masing-masing fungsi.

Untuk menyediakan sebuah API yang tersusun rapi bagi penggunamu, mudah dipakai,
dan hanya mengekspos persis apa yang mereka butuhkan, sekarang mari kita beralih
ke module-module Rust.
