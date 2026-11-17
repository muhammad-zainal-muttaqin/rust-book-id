## Bekerja dengan Environment Variable

Kita akan menyempurnakan biner `minigrep` dengan menambahkan fitur ekstra: opsi pencarian yang tidak membedakan huruf besar-kecil yang bisa dinyalakan pengguna lewat sebuah environment variable. Kita bisa saja menjadikan fitur ini sebagai opsi command line dan mewajibkan pengguna mengetikkannya setiap kali ingin menggunakannya, tetapi dengan menjadikannya sebuah environment variable, pengguna cukup mengaturnya sekali lalu semua pencarian mereka dalam sesi terminal itu menjadi tidak membedakan huruf besar-kecil.

<!-- Old headings. Do not remove or links may break. -->
<a id="writing-a-failing-test-for-the-case-insensitive-search-function"></a>

### Menulis Test yang Gagal untuk Pencarian yang Tidak Membedakan Huruf Besar-Kecil

Pertama, kita tambahkan fungsi baru `search_case_insensitive` ke library `minigrep` yang akan dipanggil ketika environment variable memiliki nilai. Kita terus mengikuti proses TDD, jadi langkah pertama kembali adalah menulis test yang gagal. Kita akan menambahkan test baru untuk fungsi `search_case_insensitive` dan mengganti nama test lama kita dari `one_result` menjadi `case_sensitive` agar perbedaan antara kedua test menjadi jelas, seperti yang ditunjukkan pada Listing 12-20.

<Listing number="12-20" file-name="src/lib.rs" caption="Menambahkan test gagal baru untuk fungsi yang tidak membedakan huruf besar-kecil yang akan kita tambahkan">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-20/src/lib.rs:here}}
```

</Listing>

Perhatikan bahwa kita juga mengedit `contents` pada test lama. Kita menambahkan baris baru dengan teks `"Duct tape."` yang memakai huruf _D_ kapital yang seharusnya tidak cocok dengan query `"duct"` ketika kita mencari dengan cara yang membedakan huruf besar-kecil. Mengubah test lama dengan cara ini membantu memastikan kita tidak tanpa sengaja merusak fungsi pencarian yang membedakan huruf besar-kecil yang sudah kita terapkan. Test ini seharusnya lulus sekarang dan harus terus lulus saat kita mengerjakan pencarian yang tidak membedakan huruf besar-kecil.

Test baru untuk pencarian yang _tidak_ membedakan huruf besar-kecil memakai `"rUsT"` sebagai query. Pada fungsi `search_case_insensitive` yang akan kita tambahkan, query `"rUsT"` harus cocok dengan baris yang berisi `"Rust:"` dengan _R_ kapital dan cocok dengan baris `"Trust me."` meskipun keduanya memiliki huruf yang berbeda dari query. Ini adalah test kita yang gagal, dan ia akan gagal dikompilasi karena kita belum mendefinisikan fungsi `search_case_insensitive`. Silakan tambahkan implementasi kerangka yang selalu mengembalikan vector kosong, mirip dengan yang kita lakukan untuk fungsi `search` pada Listing 12-16, untuk melihat test tersebut terkompilasi dan gagal.

### Mengimplementasikan Fungsi `search_case_insensitive`

Fungsi `search_case_insensitive`, yang ditunjukkan pada Listing 12-21, hampir sama dengan fungsi `search`. Satu-satunya perbedaan adalah kita akan mengubah `query` dan setiap `line` menjadi huruf kecil, sehingga apa pun huruf pada argumen masukan, keduanya akan memiliki huruf yang sama ketika kita memeriksa apakah baris tersebut memuat query.

<Listing number="12-21" file-name="src/lib.rs" caption="Mendefinisikan fungsi `search_case_insensitive` untuk mengubah query dan baris menjadi huruf kecil sebelum membandingkannya">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-21/src/lib.rs:here}}
```

</Listing>

Pertama, kita mengubah string `query` menjadi huruf kecil dan menyimpannya dalam variabel baru dengan nama yang sama, sehingga menimpa `query` yang semula. Memanggil `to_lowercase` pada query itu perlu agar, apa pun query pengguna—`"rust"`, `"RUST"`, `"Rust"`, atau `"rUsT"`—kita memperlakukannya seolah-olah `"rust"` dan tidak mempedulikan hurufnya. Meskipun `to_lowercase` menangani Unicode dasar, hasilnya tidak 100 persen akurat. Jika kita menulis aplikasi sungguhan, kita pasti ingin melakukan sedikit lebih banyak di sini, tetapi bagian ini membahas environment variable, bukan Unicode, jadi kita biarkan saja di sini.

Perhatikan bahwa `query` sekarang adalah `String`, bukan string slice, karena memanggil `to_lowercase` menciptakan data baru alih-alih mereferensikan data yang sudah ada. Misalkan query-nya `"rUsT"`: string slice itu tidak memuat `u` atau `t` huruf kecil yang bisa kita pakai, jadi kita harus mengalokasikan `String` baru yang berisi `"rust"`. Ketika kita sekarang meneruskan `query` sebagai argumen ke method `contains`, kita perlu menambahkan ampersand karena signature `contains` didefinisikan untuk menerima string slice.

Berikutnya, kita menambahkan panggilan `to_lowercase` pada setiap `line` untuk mengubah semua karakter menjadi huruf kecil. Sekarang setelah `line` dan `query` diubah ke huruf kecil, kita akan menemukan kecocokan apa pun huruf pada query.

Mari kita lihat apakah implementasi ini lolos pada test-test:

```console
{{#include ../listings/ch12-an-io-project/listing-12-21/output.txt}}
```

Hebat! Semua lolos. Sekarang mari kita panggil fungsi baru `search_case_insensitive` dari fungsi `run`. Pertama, kita akan menambahkan opsi konfigurasi ke struct `Config` untuk beralih antara pencarian yang membedakan dan yang tidak membedakan huruf besar-kecil. Menambahkan field ini akan menimbulkan error compiler karena kita belum menginisialisasi field ini di mana pun:

<span class="filename">Nama file: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:here}}
```

Kita menambahkan field `ignore_case` yang menyimpan nilai Boolean. Berikutnya, kita perlu membuat fungsi `run` memeriksa nilai field `ignore_case` dan memakainya untuk memutuskan apakah akan memanggil fungsi `search` atau fungsi `search_case_insensitive`, seperti yang ditunjukkan pada Listing 12-22. Ini masih belum akan terkompilasi.

<Listing number="12-22" file-name="src/main.rs" caption="Memanggil `search` atau `search_case_insensitive` berdasarkan nilai di `config.ignore_case`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:there}}
```

</Listing>

Akhirnya, kita perlu memeriksa environment variable tersebut. Fungsi-fungsi untuk bekerja dengan environment variable ada di module `env` dalam standard library, yang sudah berada dalam scope di bagian atas _src/main.rs_. Kita akan memakai fungsi `var` dari module `env` untuk memeriksa apakah ada nilai yang sudah ditetapkan untuk environment variable bernama `IGNORE_CASE`, seperti yang ditunjukkan pada Listing 12-23.

<Listing number="12-23" file-name="src/main.rs" caption="Memeriksa nilai apa pun dalam environment variable bernama `IGNORE_CASE`">

```rust,ignore,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-23/src/main.rs:here}}
```

</Listing>

Di sini kita membuat variabel baru, `ignore_case`. Untuk menetapkan nilainya, kita memanggil fungsi `env::var` dan meneruskan nama environment variable `IGNORE_CASE` kepadanya. Fungsi `env::var` mengembalikan `Result` yang akan menjadi varian `Ok` yang sukses dan memuat nilai environment variable jika variable tersebut ditetapkan ke suatu nilai. Ia akan mengembalikan varian `Err` jika environment variable itu tidak ditetapkan.

Kita memakai method `is_ok` pada `Result` untuk memeriksa apakah environment variable sudah ditetapkan, yang berarti program harus melakukan pencarian yang tidak membedakan huruf besar-kecil. Jika environment variable `IGNORE_CASE` tidak ditetapkan ke apa pun, `is_ok` akan mengembalikan `false` dan program akan melakukan pencarian yang membedakan huruf besar-kecil. Kita tidak peduli dengan _nilai_ environment variable itu, hanya apakah ia ditetapkan atau tidak, jadi kita memeriksa `is_ok` alih-alih memakai `unwrap`, `expect`, atau method lain yang sudah kita lihat pada `Result`.

Kita meneruskan nilai dalam variabel `ignore_case` ke instance `Config` agar fungsi `run` bisa membaca nilai itu dan memutuskan apakah akan memanggil `search_case_insensitive` atau `search`, seperti yang kita terapkan pada Listing 12-22.

Mari kita coba! Pertama, kita akan menjalankan program tanpa environment variable ditetapkan dan dengan query `to`, yang seharusnya cocok dengan baris apa pun yang memuat kata _to_ dalam huruf kecil semua:

```console
{{#include ../listings/ch12-an-io-project/listing-12-23/output.txt}}
```

Tampaknya itu masih berhasil! Sekarang mari kita jalankan program dengan `IGNORE_CASE` ditetapkan ke `1` tetapi dengan query `to` yang sama:

```console
$ IGNORE_CASE=1 cargo run -- to poem.txt
```

Jika kamu memakai PowerShell, kamu perlu menetapkan environment variable dan menjalankan program sebagai perintah-perintah terpisah:

```console
PS> $Env:IGNORE_CASE=1; cargo run -- to poem.txt
```

Ini akan membuat `IGNORE_CASE` tetap berlaku selama sisa sesi shell kamu. Nilainya bisa dihapus dengan cmdlet `Remove-Item`:

```console
PS> Remove-Item Env:IGNORE_CASE
```

Kita seharusnya mendapat baris-baris yang memuat _to_ yang mungkin memiliki huruf kapital:

<!-- manual-regeneration
cd listings/ch12-an-io-project/listing-12-23
IGNORE_CASE=1 cargo run -- to poem.txt
can't extract because of the environment variable
-->

```console
Are you nobody, too?
How dreary to be somebody!
To tell your name the livelong day
To an admiring bog!
```

Luar biasa, kita juga mendapat baris-baris yang memuat _To_! Program `minigrep` kita sekarang bisa melakukan pencarian yang tidak membedakan huruf besar-kecil yang dikendalikan oleh environment variable. Sekarang kamu tahu cara mengelola opsi yang ditetapkan baik lewat argumen command line maupun environment variable.

Beberapa program mengizinkan argumen _dan_ environment variable untuk konfigurasi yang sama. Dalam kasus seperti itu, program memutuskan mana yang lebih diutamakan. Untuk latihan mandiri lainnya, coba kendalikan sensitivitas huruf besar-kecil lewat argumen command line atau environment variable. Putuskan apakah argumen command line atau environment variable yang harus diutamakan jika program dijalankan dengan salah satunya ditetapkan untuk membedakan huruf besar-kecil dan yang lain untuk mengabaikannya.

Module `std::env` memuat banyak fitur berguna lain untuk bekerja dengan environment variable: lihat dokumentasinya untuk mengetahui apa saja yang tersedia.
