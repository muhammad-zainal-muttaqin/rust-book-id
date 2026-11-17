## Refactoring untuk Meningkatkan Modularitas dan Penanganan Error

Untuk memperbaiki program kita, kita akan mengatasi empat masalah yang berkaitan dengan struktur program dan cara ia menangani potensi error. Pertama, fungsi `main` kita sekarang melakukan dua tugas: mengurai argumen dan membaca file. Saat program kita bertambah besar, jumlah tugas terpisah yang ditangani fungsi `main` akan terus bertambah. Semakin banyak tanggung jawab suatu fungsi, semakin sulit dipahami, semakin sulit diuji, dan semakin sulit diubah tanpa merusak bagian lain. Sebaiknya kita memisahkan fungsionalitas agar setiap fungsi bertanggung jawab atas satu tugas.

Masalah ini juga berkaitan dengan masalah kedua: Meskipun `query` dan `file_path` adalah variabel konfigurasi program kita, variabel seperti `contents` dipakai untuk menjalankan logika program. Semakin panjang `main`, semakin banyak variabel yang perlu kita bawa ke dalam scope; semakin banyak variabel di dalam scope, semakin sulit kita melacak tujuan masing-masing. Sebaiknya kita mengelompokkan variabel konfigurasi ke dalam satu struktur agar tujuannya menjadi jelas.

Masalah ketiga adalah kita memakai `expect` untuk mencetak pesan error saat membaca file gagal, tetapi pesannya hanya `Should have been able to read the file`. Membaca file bisa gagal dengan berbagai cara: misalnya, filenya tidak ada, atau kita tidak punya izin untuk membukanya. Saat ini, apa pun situasinya, kita akan mencetak pesan error yang sama untuk semuanya, sehingga pengguna tidak mendapat informasi apa pun!

Keempat, kita memakai `expect` untuk menangani error, dan jika pengguna menjalankan program kita tanpa memberikan argumen yang cukup, mereka akan mendapat error `index out of bounds` dari Rust yang tidak menjelaskan masalahnya dengan jelas. Akan lebih baik jika semua kode penanganan error berada di satu tempat, sehingga orang yang merawat kode ini kelak hanya perlu melihat satu tempat jika logika penanganan error perlu diubah. Dengan mengumpulkan semua kode penanganan error di satu tempat, kita juga memastikan pesan yang kita cetak benar-benar bermakna bagi pengguna akhir kita.

Mari kita atasi keempat masalah ini dengan me-refactoring proyek kita.

<!-- Old headings. Do not remove or links may break. -->

<a id="separation-of-concerns-for-binary-projects"></a>

### Memisahkan Tanggung Jawab dalam Proyek Biner

Masalah organisasi dalam membebankan tanggung jawab atas banyak tugas kepada fungsi `main` umum terjadi di banyak proyek biner. Akibatnya, banyak programmer Rust merasa terbantu dengan memisahkan tanggung jawab yang berbeda dalam program biner ketika fungsi `main` mulai membesar. Proses ini terdiri dari langkah-langkah berikut:

- Pecah programmu menjadi file _main.rs_ dan file _lib.rs_, lalu pindahkan logika program ke _lib.rs_.
- Selama logika penguraian command line masih sederhana, logika itu boleh tetap berada di fungsi `main`.
- Saat logika penguraian command line mulai rumit, ekstrak dari fungsi `main` ke fungsi atau tipe lain.

Tanggung jawab yang tersisa di fungsi `main` setelah proses ini sebaiknya dibatasi pada hal-hal berikut:

- Memanggil logika penguraian command line dengan nilai-nilai argumen
- Menyiapkan konfigurasi lain yang diperlukan
- Memanggil fungsi `run` di _lib.rs_
- Menangani error jika `run` mengembalikan error

Pola ini bertujuan memisahkan tanggung jawab: _main.rs_ menangani menjalankan program, sementara _lib.rs_ menangani seluruh logika tugas yang sedang dikerjakan. Karena kamu tidak bisa menguji fungsi `main` secara langsung, struktur ini memungkinkan kamu menguji semua logika program dengan memindahkannya keluar dari `main`. Kode yang tersisa di fungsi `main` akan cukup pendek sehingga kebenarannya bisa diverifikasi hanya dengan membacanya. Mari kita kerjakan ulang program kita mengikuti proses ini.

#### Mengekstrak Parser Argumen

Kita akan mengekstrak fungsionalitas penguraian argumen ke dalam fungsi yang akan dipanggil `main`. Listing 12-5 menunjukkan awal baru fungsi `main` yang memanggil fungsi baru `parse_config`, yang akan kita definisikan di _src/main.rs_.

<Listing number="12-5" file-name="src/main.rs" caption="Mengekstrak fungsi `parse_config` dari `main`">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-05/src/main.rs:here}}
```

</Listing>

Kita tetap mengumpulkan argumen command line ke dalam vector, tetapi alih-alih menetapkan nilai argumen pada indeks 1 ke variabel `query` dan nilai argumen pada indeks 2 ke variabel `file_path` di dalam fungsi `main`, kita meneruskan seluruh vector ke fungsi `parse_config`. Fungsi `parse_config` kini memegang logika yang menentukan argumen mana masuk ke variabel mana, lalu mengembalikan nilai-nilai itu ke `main`. Kita tetap membuat variabel `query` dan `file_path` di `main`, tetapi `main` tidak lagi bertugas menentukan bagaimana argumen command line dan variabel saling berhubungan.

Perubahan ini mungkin terasa berlebihan untuk program kita yang kecil, tetapi kita sedang me-refactoring dengan langkah-langkah kecil dan bertahap. Setelah melakukan perubahan ini, jalankan lagi programnya untuk memastikan penguraian argumen tetap berfungsi. Sebaiknya kamu sering mengecek progres agar lebih mudah menemukan penyebab masalah saat muncul.

#### Mengelompokkan Nilai Konfigurasi

Kita bisa mengambil satu langkah kecil lagi untuk memperbaiki fungsi `parse_config`. Saat ini kita mengembalikan tuple, lalu langsung memecah tuple itu menjadi bagian-bagian terpisah lagi. Ini pertanda bahwa abstraksi kita mungkin belum tepat.

Indikator lain yang menunjukkan masih ada ruang untuk perbaikan adalah bagian `config` pada `parse_config`, yang menyiratkan bahwa dua nilai yang kita kembalikan saling terkait dan keduanya merupakan bagian dari satu nilai konfigurasi. Saat ini kita belum menyampaikan makna itu lewat struktur data, selain dengan mengelompokkan kedua nilai ke dalam tuple. Sebagai gantinya, kita akan memasukkan kedua nilai itu ke dalam satu struct dan memberi setiap field struct nama yang bermakna. Dengan begitu, orang yang merawat kode ini kelak lebih mudah memahami hubungan antarnilai dan tujuan masing-masing.

Listing 12-6 menunjukkan perbaikan pada fungsi `parse_config`.

<Listing number="12-6" file-name="src/main.rs" caption="Me-refactoring `parse_config` agar mengembalikan instance struct `Config`">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-06/src/main.rs:here}}
```

</Listing>

Kita telah menambahkan struct bernama `Config` dengan field bernama `query` dan `file_path`. Tanda tangan `parse_config` sekarang menunjukkan bahwa fungsi itu mengembalikan nilai `Config`. Di tubuh `parse_config`, dulu kita mengembalikan string slice yang merujuk ke nilai `String` di `args`; sekarang kita mendefinisikan `Config` agar berisi nilai `String` yang dimiliki sendiri. Variabel `args` di `main` adalah pemilik nilai-nilai argumen dan hanya meminjamkannya ke fungsi `parse_config`, yang berarti kita akan melanggar aturan borrowing Rust jika `Config` mencoba mengambil kepemilikan nilai di `args`.

Ada beberapa cara untuk mengelola data `String`; cara termudah, meski agak boros, adalah memanggil method `clone` pada nilai-nilai itu. Ini akan membuat salinan penuh data agar bisa dimiliki oleh instance `Config`, yang memakan lebih banyak waktu dan memori daripada menyimpan reference ke data string tersebut. Namun, meng-clone data juga membuat kode kita sangat lugas karena kita tidak perlu mengelola lifetime dari reference-reference itu; dalam situasi ini, mengorbankan sedikit kinerja demi kesederhanaan adalah kompromi yang sepadan.

> ### Kompromi Memakai `clone`
>
> Ada kecenderungan di kalangan Rustacean untuk menghindari `clone` saat memperbaiki masalah ownership karena biaya runtime-nya. Di
> [Bab 13][ch13]<!-- ignore -->, kamu akan belajar memakai metode yang lebih efisien
> dalam situasi seperti ini. Tapi untuk sekarang, tidak apa-apa menyalin beberapa
> string demi terus maju, karena salinan itu hanya kamu buat sekali, dan path file
> serta string query-mu sangat kecil. Lebih baik punya program yang berfungsi meski
> agak boros daripada mencoba mengoptimalkan kode secara berlebihan pada percobaan
> pertama. Saat kamu makin berpengalaman dengan Rust, akan lebih mudah mulai dengan
> solusi paling efisien, tetapi untuk sekarang, memanggil `clone` sudah sepenuhnya
> boleh.

Kita telah memperbarui `main` agar menyimpan instance `Config` yang dikembalikan `parse_config` ke dalam variabel bernama `config`, dan kita memperbarui kode yang sebelumnya memakai variabel `query` dan `file_path` secara terpisah agar sekarang memakai field pada struct `Config`.

Sekarang kode kita lebih jelas menyampaikan bahwa `query` dan `file_path` saling terkait serta bertujuan mengonfigurasi cara program bekerja. Kode mana pun yang memakai nilai-nilai ini tahu harus mencarinya di instance `config`, pada field yang diberi nama sesuai tujuannya.

#### Membuat Constructor untuk `Config`

Sejauh ini, kita telah mengekstrak logika penguraian argumen command line dari `main` dan menempatkannya di fungsi `parse_config`. Hal itu membantu kita melihat bahwa nilai `query` dan `file_path` saling terkait, dan hubungan itu sebaiknya tercermin dalam kode kita. Lalu kita menambahkan struct `Config` untuk memberi nama pada tujuan bersama `query` dan `file_path`, serta agar `parse_config` bisa mengembalikan nilai-nilai itu dengan nama sebagai field struct.

Karena kini tujuan fungsi `parse_config` adalah membuat instance `Config`, kita bisa mengubah `parse_config` dari fungsi biasa menjadi fungsi bernama `new` yang berkaitan dengan struct `Config`. Perubahan ini membuat kode lebih idiomatik. Kita bisa membuat instance tipe di standard library, seperti `String`, dengan memanggil `String::new`. Begitu pula, dengan mengubah `parse_config` menjadi fungsi `new` yang terkait dengan `Config`, kita bisa membuat instance `Config` lewat `Config::new`. Listing 12-7 menunjukkan perubahan yang perlu kita lakukan.

<Listing number="12-7" file-name="src/main.rs" caption="Mengubah `parse_config` menjadi `Config::new`">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-07/src/main.rs:here}}
```

</Listing>

Kita telah memperbarui `main`: tempat dulu kita memanggil `parse_config`, sekarang kita memanggil `Config::new`. Kita mengubah nama `parse_config` menjadi `new` dan memindahkannya ke dalam blok `impl`, yang mengaitkan fungsi `new` dengan `Config`. Coba kompilasi lagi kode ini untuk memastikan semuanya berfungsi.

### Memperbaiki Penanganan Error

Sekarang kita akan memperbaiki penanganan error. Ingat bahwa mencoba mengakses nilai di vector `args` pada indeks 1 atau indeks 2 akan membuat program panic jika vector itu berisi kurang dari tiga item. Coba jalankan program tanpa argumen; tampilannya akan seperti ini:

```console
{{#include ../listings/ch12-an-io-project/listing-12-07/output.txt}}
```

Baris `index out of bounds: the len is 1 but the index is 1` adalah pesan error yang ditujukan untuk programmer. Pesan itu tidak membantu pengguna akhir kita memahami apa yang seharus mereka lakukan. Mari kita perbaiki sekarang.

#### Memperbaiki Pesan Error

Di Listing 12-8, kita menambahkan pengecekan di fungsi `new` untuk memastikan slice cukup panjang sebelum mengakses indeks 1 dan indeks 2. Jika slice tidak cukup panjang, program akan panic dan menampilkan pesan error yang lebih baik.

<Listing number="12-8" file-name="src/main.rs" caption="Menambahkan pengecekan jumlah argumen">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-08/src/main.rs:here}}
```

</Listing>

Kode ini mirip dengan [fungsi `Guess::new` yang kita tulis di Listing 9-13][ch9-custom-types]<!-- ignore -->, tempat kita memanggil `panic!` ketika argumen `value` berada di luar rentang nilai yang valid. Alih-alih memeriksa rentang nilai, di sini kita memeriksa bahwa panjang `args` minimal `3`, sehingga sisa fungsi bisa berjalan dengan anggapan kondisi itu terpenuhi. Jika `args` berisi kurang dari tiga item, kondisi tersebut akan bernilai `true`, dan kita memanggil macro `panic!` untuk menghentikan program seketika.

Dengan beberapa baris kode tambahan di `new`, mari jalankan lagi program tanpa argumen untuk melihat seperti apa error-nya sekarang:

```console
{{#include ../listings/ch12-an-io-project/listing-12-08/output.txt}}
```

Hasil ini lebih baik: kita sekarang punya pesan error yang masuk akal. Namun, ada juga informasi tambahan yang tidak ingin kita berikan kepada pengguna. Mungkin teknik yang kita pakai di Listing 9-13 bukanlah pilihan terbaik di sini: memanggil `panic!` lebih cocok untuk masalah pemrograman daripada masalah penggunaan, [seperti yang dibahas di Bab 9][ch9-error-guidelines]<!-- ignore -->. Sebagai gantinya, kita akan memakai teknik lain yang kamu pelajari di Bab 9—[mengembalikan `Result`][ch9-result]<!-- ignore --> yang menandakan baik keberhasilan maupun error.

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-a-result-from-new-instead-of-calling-panic"></a>

#### Mengembalikan `Result` Alih-alih Memanggil `panic!`

Sebagai gantinya, kita bisa mengembalikan nilai `Result` yang berisi instance `Config` saat berhasil dan menjelaskan masalahnya saat gagal. Kita juga akan mengubah nama fungsi dari `new` menjadi `build`, karena banyak programmer mengira fungsi `new` tidak akan pernah gagal. Saat `Config::build` berkomunikasi dengan `main`, kita bisa memakai tipe `Result` untuk menandakan bahwa ada masalah. Lalu kita bisa mengubah `main` agar menerjemahkan varian `Err` menjadi error yang lebih praktis bagi pengguna, tanpa teks tambahan tentang `thread 'main'` dan `RUST_BACKTRACE` yang muncul akibat panggilan `panic!`.

Listing 12-9 menunjukkan perubahan yang perlu kita lakukan pada nilai kembalian fungsi yang kini bernama `Config::build`, serta tubuh fungsi yang diperlukan agar mengembalikan `Result`. Perhatikan bahwa kode ini belum akan terkompilasi sampai kita memperbarui `main` juga, yang akan kita lakukan di listing berikutnya.

<Listing number="12-9" file-name="src/main.rs" caption="Mengembalikan `Result` dari `Config::build`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-09/src/main.rs:here}}
```

</Listing>

Fungsi `build` kita mengembalikan `Result` dengan instance `Config` saat berhasil dan string literal saat gagal. Nilai error kita selalu berupa string literal yang memiliki lifetime `'static`.

Kita membuat dua perubahan di tubuh fungsi: alih-alih memanggil `panic!` saat pengguna tidak memberikan argumen yang cukup, sekarang kita mengembalikan nilai `Err`, dan kita membungkus nilai kembalian `Config` dengan `Ok`. Perubahan ini membuat fungsi sesuai dengan tanda tangan tipenya yang baru.

Dengan mengembalikan nilai `Err` dari `Config::build`, fungsi `main` bisa menangani nilai `Result` yang dikembalikan `build` dan menghentikan proses dengan lebih rapi saat terjadi error.

<!-- Old headings. Do not remove or links may break. -->

<a id="calling-confignew-and-handling-errors"></a>

#### Memanggil `Config::build` dan Menangani Error

Untuk menangani kondisi error dan mencetak pesan yang ramah pengguna, kita perlu memperbarui `main` agar menangani `Result` yang dikembalikan `Config::build`, seperti ditunjukkan Listing 12-10. Kita juga akan mengambil alih tanggung jawab keluar dari command line tool dengan kode error bukan nol dari `panic!`, lalu menerapkannya sendiri. Status keluar bukan nol adalah konvensi untuk memberi tahu proses yang memanggil program kita bahwa program berakhir dalam keadaan error.

<Listing number="12-10" file-name="src/main.rs" caption="Keluar dengan kode error jika pembuatan `Config` gagal">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-10/src/main.rs:here}}
```

</Listing>

Di listing ini, kita memakai method yang belum kita bahas secara rinci: `unwrap_or_else`, yang didefinisikan pada `Result<T, E>` oleh standard library. Dengan `unwrap_or_else`, kita bisa menentukan penanganan error sendiri yang bukan `panic!`. Jika `Result` bernilai `Ok`, perilaku method ini mirip `unwrap`: ia mengembalikan nilai dalam yang dibungkus `Ok`. Namun, jika nilainya adalah `Err`, method ini memanggil kode di dalam closure, yaitu fungsi anonim yang kita definisikan dan berikan sebagai argumen kepada `unwrap_or_else`. Kita akan membahas closure lebih rinci di [Bab 13][ch13]<!-- ignore -->. Untuk sekarang, kamu hanya perlu tahu bahwa `unwrap_or_else` akan meneruskan nilai dalam dari `Err`—dalam kasus ini string statis `"not enough arguments"` yang kita tambahkan di Listing 12-9—ke closure kita lewat argumen `err` yang muncul di antara dua tanda pipa vertikal. Kode di dalam closure lalu bisa memakai nilai `err` saat dijalankan.

Kita menambahkan baris `use` baru untuk membawa `process` dari standard library ke dalam scope. Kode di dalam closure yang dijalankan saat error hanya dua baris: kita mencetak nilai `err`, lalu memanggil `process::exit`. Fungsi `process::exit` akan menghentikan program seketika dan mengembalikan angka yang diberikan sebagai kode status keluar. Ini mirip penanganan berbasis `panic!` yang kita pakai di Listing 12-8, tetapi kini kita tidak mendapat semua keluaran tambahan itu. Mari kita coba:

```console
{{#include ../listings/ch12-an-io-project/listing-12-10/output.txt}}
```

Bagus! Keluaran ini jauh lebih ramah bagi pengguna kita.

<!-- Old headings. Do not remove or links may break. -->

<a id="extracting-logic-from-the-main-function"></a>

### Mengekstrak Logika dari `main`

Setelah selesai me-refactoring penguraian konfigurasi, mari kita beralih ke logika program. Seperti yang kita katakan di [“Memisahkan Tanggung Jawab dalam Proyek Biner”](#separation-of-concerns-for-binary-projects)<!-- ignore -->, kita akan mengekstrak fungsi bernama `run` yang menampung semua logika yang saat ini ada di `main` dan tidak berkaitan dengan penyiapan konfigurasi atau penanganan error. Setelah selesai, fungsi `main` akan ringkas dan mudah diverifikasi hanya dengan dibaca, dan kita bisa menulis test untuk semua logika lainnya.

Listing 12-11 menunjukkan perbaikan kecil dan bertahap dengan mengekstrak fungsi `run`.

<Listing number="12-11" file-name="src/main.rs" caption="Mengekstrak fungsi `run` yang berisi sisa logika program">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-11/src/main.rs:here}}
```

</Listing>

Fungsi `run` sekarang berisi semua logika yang tersisa dari `main`, mulai dari membaca file. Fungsi `run` menerima instance `Config` sebagai argumen.

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-errors-from-the-run-function"></a>

#### Mengembalikan Error dari `run`

Dengan logika program yang tersisa sudah dipisahkan ke dalam fungsi `run`, kita bisa memperbaiki penanganan error seperti yang kita lakukan pada `Config::build` di Listing 12-9. Alih-alih membiarkan program panic karena memanggil `expect`, fungsi `run` akan mengembalikan `Result<T, E>` saat terjadi masalah. Ini memungkinkan kita mengumpulkan lebih banyak logika penanganan error di `main` dengan cara yang ramah pengguna. Listing 12-12 menunjukkan perubahan yang perlu kita lakukan pada tanda tangan dan tubuh `run`.

<Listing number="12-12" file-name="src/main.rs" caption="Mengubah fungsi `run` agar mengembalikan `Result`">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-12/src/main.rs:here}}
```

</Listing>

Kita membuat tiga perubahan penting di sini. Pertama, kita mengubah tipe kembalian fungsi `run` menjadi `Result<(), Box<dyn Error>>`. Sebelumnya fungsi ini mengembalikan tipe unit, `()`, dan kita tetap memakainya sebagai nilai yang dikembalikan dalam kasus `Ok`.

Untuk tipe error-nya, kita memakai trait object `Box<dyn Error>` (dan kita membawa `std::error::Error` ke dalam scope dengan statement `use` di bagian atas). Kita akan membahas trait object di [Bab 18][ch18]<!-- ignore -->. Untuk sekarang, cukup ketahuilah bahwa `Box<dyn Error>` berarti fungsi akan mengembalikan tipe yang mengimplementasikan trait `Error`, tetapi kita tidak perlu menentukan secara spesifik tipe nilai kembaliannya. Ini memberi kita keleluasaan untuk mengembalikan nilai error yang bisa berbeda tipenya dalam kasus error yang berbeda. Keyword `dyn` adalah singkatan dari _dynamic_.

Kedua, kita menghapus panggilan `expect` dan menggantinya dengan operator `?`, seperti yang kita bahas di [Bab 9][ch9-question-mark]<!-- ignore -->. Alih-alih `panic!` saat terjadi error, `?` akan mengembalikan nilai error dari fungsi saat ini agar ditangani oleh pemanggilnya.

Ketiga, fungsi `run` sekarang mengembalikan nilai `Ok` saat berhasil. Kita mendeklarasikan tipe keberhasilan `run` sebagai `()` di tanda tangan, yang berarti kita perlu membungkus nilai tipe unit itu di dalam nilai `Ok`. Sintaks `Ok(())` ini mungkin tampak agak aneh pada awalnya. Namun, memakai `()` seperti itu adalah cara idiomatik untuk menandakan bahwa kita memanggil `run` hanya demi efek sampingnya; fungsi itu tidak mengembalikan nilai yang kita butuhkan.

Saat kamu menjalankan kode ini, kode tersebut akan terkompilasi tetapi menampilkan peringatan:

```console
{{#include ../listings/ch12-an-io-project/listing-12-12/output.txt}}
```

Rust memberi tahu kita bahwa kode kita mengabaikan nilai `Result`, dan nilai `Result` itu mungkin menandakan terjadi error. Kita tidak memeriksa apakah ada error atau tidak, dan compiler mengingatkan kita bahwa kita mungkin seharusnya punya kode penanganan error di sini! Mari kita perbaiki masalah itu sekarang.

#### Menangani Error yang Dikembalikan `run` di `main`

Kita akan memeriksa error dan menanganinya dengan teknik yang mirip dengan yang kita pakai pada `Config::build` di Listing 12-10, tetapi dengan sedikit perbedaan:

<span class="filename">Nama file: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/no-listing-01-handling-errors-in-main/src/main.rs:here}}
```

Kita memakai `if let`, bukan `unwrap_or_else`, untuk memeriksa apakah `run` mengembalikan nilai `Err` dan memanggil `process::exit(1)` jika ya. Fungsi `run` tidak mengembalikan nilai yang ingin kita `unwrap` seperti halnya `Config::build` yang mengembalikan instance `Config`. Karena `run` mengembalikan `()` saat berhasil, kita hanya peduli mendeteksi error, jadi kita tidak perlu `unwrap_or_else` untuk mengembalikan nilai yang dibuka, yang nilainya hanya `()`.

Tubuh `if let` dan `unwrap_or_else` sama dalam kedua kasus: kita mencetak error lalu keluar.

### Memecah Kode ke dalam Library Crate

Proyek `minigrep` kita sekarang terlihat bagus! Selanjutnya kita akan memecah file _src/main.rs_ dan memindahkan sebagian kode ke file _src/lib.rs_. Dengan begitu, kita bisa menguji kode itu dan memiliki file _src/main.rs_ dengan lebih sedikit tanggung jawab.

Mari kita definisikan kode yang bertugas mencari teks di _src/lib.rs_, bukan di _src/main.rs_. Ini memungkinkan kita—atau siapa pun yang memakai library `minigrep` kita—memanggil fungsi pencarian dari lebih banyak konteks daripada sekadar binary `minigrep` kita.

Pertama, mari kita definisikan tanda tangan fungsi `search` di _src/lib.rs_ seperti ditunjukkan Listing 12-13, dengan tubuh yang memanggil macro `unimplemented!`. Kita akan menjelaskan tanda tangan itu lebih rinci saat mengisi implementasinya.

<Listing number="12-13" file-name="src/lib.rs" caption="Mendefinisikan fungsi `search` di *src/lib.rs*">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-13/src/lib.rs}}
```

</Listing>

Kita memakai keyword `pub` pada definisi fungsi untuk menandakan `search` sebagai bagian dari API publik library crate kita. Kini kita punya library crate yang bisa dipakai dari binary crate kita dan bisa kita uji!

Sekarang kita perlu membawa kode yang didefinisikan di _src/lib.rs_ ke dalam scope binary crate di _src/main.rs_ dan memanggilnya, seperti ditunjukkan Listing 12-14.

<Listing number="12-14" file-name="src/main.rs" caption="Memakai fungsi `search` dari library crate `minigrep` di *src/main.rs*">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-14/src/main.rs:here}}
```

</Listing>

Kita menambahkan baris `use minigrep::search` untuk membawa fungsi `search` dari library crate ke dalam scope binary crate. Lalu, di fungsi `run`, alih-alih mencetak isi file, kita memanggil fungsi `search` dan meneruskan nilai `config.query` serta `contents` sebagai argumen. Setelah itu, `run` memakai loop `for` untuk mencetak setiap baris yang dikembalikan `search` dan cocok dengan query. Ini juga saat yang tepat untuk menghapus panggilan `println!` di fungsi `main` yang menampilkan query dan path file, agar program kita hanya mencetak hasil pencarian (jika tidak ada error).

Perhatikan bahwa fungsi search akan mengumpulkan semua hasil ke dalam vector yang dikembalikannya sebelum ada pencetakan. Implementasi ini bisa lambat menampilkan hasil saat mencari file besar, karena hasil tidak dicetak begitu ditemukan; kita akan membahas kemungkinan cara memperbaikinya dengan iterator di Bab 13.

Wah, itu banyak sekali pekerjaannya! Tetapi kita sudah menyiapkan diri untuk sukses di kemudian hari. Sekarang menangani error jauh lebih mudah, dan kode kita lebih modular. Hampir semua pekerjaan kita dari sekarang akan dilakukan di _src/lib.rs_.

Mari kita manfaatkan modularitas yang baru kita dapatkan dengan melakukan sesuatu yang dulu sulit dilakukan pada kode lama, tetapi mudah pada kode baru: kita akan menulis beberapa test!

[ch13]: ch13-00-functional-features.html
[ch9-custom-types]: ch09-03-to-panic-or-not-to-panic.html#creating-custom-types-for-validation
[ch9-error-guidelines]: ch09-03-to-panic-or-not-to-panic.html#guidelines-for-error-handling
[ch9-result]: ch09-02-recoverable-errors-with-result.html
[ch18]: ch18-00-oop.html
[ch9-question-mark]: ch09-02-recoverable-errors-with-result.html#a-shortcut-for-propagating-errors-the--operator
