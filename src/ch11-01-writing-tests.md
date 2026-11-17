<a id="how-to-write-tests"></a>
## Cara Menulis Test

_Test_ adalah fungsi Rust yang memverifikasi bahwa kode non-test berjalan sebagaimana mestinya. Isi dari fungsi test biasanya melakukan tiga tindakan ini:

- Menyiapkan data atau state yang dibutuhkan.
- Menjalankan kode yang ingin kamu test.
- Memastikan bahwa hasilnya sesuai dengan yang kamu harapkan.

Mari kita lihat fitur-fitur yang disediakan Rust khusus untuk menulis test yang melakukan tindakan-tindakan ini, antara lain atribut `test`, beberapa macro, dan atribut `should_panic`.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-anatomy-of-a-test-function"></a>

### Menyusun Fungsi Test

Paling sederhana, sebuah test dalam Rust adalah fungsi yang diberi anotasi atribut `test`. Atribut adalah metadata tentang bagian-bagian kode Rust; salah satu contohnya adalah atribut `derive` yang kita pakai pada struct di Bab 5. Untuk mengubah sebuah fungsi menjadi fungsi test, tambahkan `#[test]` pada baris sebelum `fn`. Saat kamu menjalankan test dengan perintah `cargo test`, Rust membangun biner test runner yang menjalankan fungsi-fungsi yang diberi anotasi dan melaporkan apakah setiap fungsi test lulus atau gagal.

Setiap kali kita membuat proyek library baru dengan Cargo, sebuah module test beserta sebuah fungsi test di dalamnya otomatis dibuatkan untuk kita. Module ini memberi kamu templat untuk menulis test sehingga kamu tidak perlu mencari tahu struktur dan sintaks pastinya setiap kali memulai proyek baru. Kamu bisa menambahkan sebanyak mana pun fungsi test dan module test yang kamu mau!

Kita akan menjelajahi beberapa aspek cara kerja test dengan bereksperimen pada test templat sebelum kita benar-benar mengetes kode apa pun. Lalu, kita akan menulis beberapa test dunia nyata yang memanggil kode yang sudah kita tulis dan memastikan bahwa perilakunya benar.

Mari kita buat proyek library baru bernama `adder` yang akan menjumlahkan dua angka:

```console
$ cargo new adder --lib
     Created library `adder` project
$ cd adder
```

Isi file _src/lib.rs_ di library `adder` kamu harusnya terlihat seperti Daftar 11-1.

<Listing number="11-1" file-name="src/lib.rs" caption="Kode yang dibuat secara otomatis oleh `cargo new`">

<!-- manual-regeneration
cd listings/ch11-writing-automated-tests
rm -rf listing-11-01
cargo new listing-11-01 --lib --name adder
cd listing-11-01
echo "$ cargo test" > output.txt
RUSTFLAGS="-A unused_variables -A dead_code" RUST_TEST_THREADS=1 cargo test >> output.txt 2>&1
git diff output.txt # commit any relevant changes; discard irrelevant ones
cd ../../..
-->

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

</Listing>

File ini dimulai dengan sebuah fungsi `add` contoh agar kita punya sesuatu untuk ditest.

Untuk sekarang, mari kita fokus hanya pada fungsi `it_works`. Perhatikan anotasi `#[test]`: atribut ini menandakan bahwa ini adalah fungsi test, sehingga test runner tahu harus memperlakukan fungsi ini sebagai test. Kita mungkin juga punya fungsi non-test di module `tests` untuk membantu menyiapkan skenario umum atau melakukan operasi yang biasa dilakukan, jadi kita selalu perlu menandakan fungsi mana yang merupakan test.

Isi fungsi contoh tersebut menggunakan macro `assert_eq!` untuk memastikan bahwa `result`, yang berisi hasil pemanggilan `add` dengan 2 dan 2, sama dengan 4. Assertion ini menjadi contoh format untuk test pada umumnya. Mari kita jalankan untuk melihat bahwa test ini lulus.

Perintah `cargo test` menjalankan semua test di proyek kita, seperti yang ditunjukkan Daftar 11-2.

<Listing number="11-2" caption="Keluaran dari menjalankan test yang dibuat secara otomatis">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-01/output.txt}}
```

</Listing>

Cargo mengompilasi dan menjalankan test tersebut. Kita melihat baris `running 1 test`. Baris berikutnya menampilkan nama fungsi test yang dibuat, yaitu `tests::it_works`, dan bahwa hasil menjalankan test itu adalah `ok`. Ringkasan keseluruhan `test result: ok.` berarti semua test lulus, dan bagian yang bertuliskan `1 passed; 0 failed` menjumlahkan test yang lulus dan yang gagal.

Dimungkinkan untuk menandai sebuah test sebagai diabaikan agar tidak dijalankan dalam situasi tertentu; kita akan membahasnya di bagian [“Mengabaikan Test Kecuali Diminta Secara Khusus”][ignoring]<!-- ignore --> nanti dalam bab ini. Karena kita belum melakukan itu di sini, ringkasan menampilkan `0 ignored`. Kita juga bisa memberikan argumen pada perintah `cargo test` untuk hanya menjalankan test yang namanya cocok dengan sebuah string; ini disebut _filtering_, dan kita akan membahasnya di bagian [“Menjalankan Sebagian Test berdasarkan Nama”][subset]<!-- ignore -->. Di sini, kita tidak memfilter test yang dijalankan, sehingga akhir ringkasan menampilkan `0 filtered out`.

Statistik `0 measured` untuk test benchmark yang mengukur kinerja. Test benchmark, pada saat tulisan ini dibuat, hanya tersedia di Rust nightly. Lihat [dokumentasi tentang test benchmark][bench] untuk mempelajari lebih lanjut.

Bagian berikutnya dari keluaran test yang dimulai dari `Doc-tests adder` adalah hasil dari documentation test. Kita belum punya documentation test apa pun, tetapi Rust bisa mengompilasi contoh kode apa pun yang muncul di dokumentasi API kita. Fitur ini membantu menjaga dokumentasi dan kode kamu tetap sinkron! Kita akan membahas cara menulis documentation test di bagian [“Komentar Dokumentasi sebagai Test”][doc-comments]<!-- ignore --> Bab 14. Untuk sekarang, kita abaikan keluaran `Doc-tests`.

Mari kita mulai menyesuaikan test sesuai kebutuhan kita. Pertama, ubah nama fungsi `it_works` menjadi nama lain, misalnya `exploration`, seperti ini:

<span class="filename">Nama file: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/src/lib.rs}}
```

Lalu, jalankan `cargo test` lagi. Keluaran sekarang menampilkan `exploration`, bukan `it_works`:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/output.txt}}
```

Sekarang kita akan menambahkan test lagi, tetapi kali ini kita buat test yang gagal! Sebuah test gagal ketika ada sesuatu di dalam fungsi test yang panic. Setiap test dijalankan di thread baru, dan ketika thread utama melihat bahwa thread test telah mati, test ditandai sebagai gagal. Di Bab 9, kita sudah berbicara bahwa cara paling sederhana untuk panic adalah memanggil macro `panic!`. Masukkan test baru sebagai fungsi bernama `another`, sehingga file _src/lib.rs_ kamu terlihat seperti Daftar 11-3.

<Listing number="11-3" file-name="src/lib.rs" caption="Menambahkan test kedua yang akan gagal karena kita memanggil macro `panic!`">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-03/src/lib.rs}}
```

</Listing>

Jalankan test lagi menggunakan `cargo test`. Keluarannya harusnya terlihat seperti Daftar 11-4, yang menunjukkan bahwa test `exploration` kita lulus dan `another` gagal.

<Listing number="11-4" caption="Hasil test ketika satu test lulus dan satu test gagal">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-03/output.txt}}
```

</Listing>

<!-- manual-regeneration
rg panicked listings/ch11-writing-automated-tests/listing-11-03/output.txt
check the line number of the panic matches the line number in the following paragraph
  -->

Alih-alih `ok`, baris `test tests::another` menampilkan `FAILED`. Dua bagian baru muncul di antara hasil per test dan ringkasan: yang pertama menampilkan alasan terperinci untuk setiap kegagalan test. Dalam kasus ini, kita mendapat rincian bahwa `tests::another` gagal karena panic dengan pesan `Make this test fail` pada baris 17 di file _src/lib.rs_. Bagian berikutnya hanya mencantumkan nama semua test yang gagal, yang berguna ketika ada banyak test dan banyak keluaran rinci tentang test yang gagal. Kita bisa memakai nama test yang gagal untuk menjalankan hanya test itu agar lebih mudah di-debug; kita akan berbicara lebih banyak tentang cara menjalankan test di bagian [“Mengontrol Cara Test Dijalankan”][controlling-how-tests-are-run]<!-- ignore -->.

Baris ringkasan muncul di akhir: Secara keseluruhan, hasil test kita adalah `FAILED`. Kita punya satu test yang lulus dan satu yang gagal.

Sekarang setelah kamu melihat seperti apa hasil test dalam berbagai skenario, mari kita lihat beberapa macro selain `panic!` yang berguna dalam test.

<!-- Old headings. Do not remove or links may break. -->

<a id="checking-results-with-the-assert-macro"></a>

### Memeriksa Hasil dengan `assert!`

Macro `assert!`, yang disediakan oleh library standar, berguna ketika kamu ingin memastikan bahwa suatu kondisi dalam test bernilai `true`. Kita memberikan macro `assert!` sebuah argumen yang mengevaluasi ke nilai Boolean. Jika nilainya `true`, tidak ada yang terjadi dan test lulus. Jika nilainya `false`, macro `assert!` memanggil `panic!` untuk membuat test gagal. Memakai macro `assert!` membantu kita memeriksa bahwa kode kita berjalan sesuai yang kita maksud.

Di Bab 5, Daftar 5-15, kita memakai struct `Rectangle` dan method `can_hold`, yang diulang di sini pada Daftar 11-5. Mari kita letakkan kode ini di file _src/lib.rs_, lalu tulis beberapa test untuknya memakai macro `assert!`.

<Listing number="11-5" file-name="src/lib.rs" caption="Struct `Rectangle` dan method `can_hold`-nya dari Bab 5">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-05/src/lib.rs}}
```

</Listing>

Method `can_hold` mengembalikan nilai Boolean, yang berarti ini adalah kasus penggunaan yang pas untuk macro `assert!`. Di Daftar 11-6, kita menulis test yang mencoba method `can_hold` dengan membuat instance `Rectangle` yang lebar 8 dan tinggi 7, lalu memastikan bahwa instance itu bisa menampung instance `Rectangle` lain yang lebar 5 dan tinggi 1.

<Listing number="11-6" file-name="src/lib.rs" caption="Sebuah test untuk `can_hold` yang memeriksa apakah persegi panjang yang lebih besar memang bisa menampung persegi panjang yang lebih kecil">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-06/src/lib.rs:here}}
```

</Listing>

Perhatikan baris `use super::*;` di dalam module `tests`. Module `tests` adalah module biasa yang mengikuti aturan visibilitas seperti biasa yang kita bahas di Bab 7 pada bagian [“Path untuk Merujuk ke Item di Pohon Module”][paths-for-referring-to-an-item-in-the-module-tree]<!-- ignore -->. Karena module `tests` adalah module dalam, kita perlu membawa kode yang ditest di module luar ke dalam scope module dalam. Kita memakai glob di sini, sehingga apa pun yang kita definisikan di module luar tersedia bagi module `tests` ini.

Kita menamai test kita `larger_can_hold_smaller`, dan kita sudah membuat dua instance `Rectangle` yang kita butuhkan. Lalu, kita memanggil macro `assert!` dan memberikan hasil pemanggilan `larger.can_hold(&smaller)`. Ekspresi ini seharusnya mengembalikan `true`, jadi test kita harusnya lulus. Mari kita lihat!

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-06/output.txt}}
```

Test itu memang lulus! Mari kita tambahkan test lagi, kali ini memastikan bahwa persegi panjang yang lebih kecil tidak bisa menampung persegi panjang yang lebih besar:

<span class="filename">Nama file: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/src/lib.rs:here}}
```

Karena hasil yang benar dari fungsi `can_hold` dalam kasus ini adalah `false`, kita perlu membalik hasil itu sebelum memberikannya ke macro `assert!`. Dengan demikian, test kita akan lulus jika `can_hold` mengembalikan `false`:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/output.txt}}
```

Dua test yang lulus! Sekarang mari kita lihat apa yang terjadi pada hasil test ketika kita memasukkan bug ke dalam kode. Kita akan mengubah implementasi method `can_hold` dengan mengganti tanda lebih besar (`>`) dengan tanda lebih kecil (`<`) saat membandingkan lebar:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/src/lib.rs:here}}
```

Menjalankan test sekarang menghasilkan ini:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/output.txt}}
```

Test kita berhasil menangkap bug! Karena `larger.width` adalah `8` dan `smaller.width` adalah `5`, perbandingan lebar di `can_hold` sekarang mengembalikan `false`: 8 tidak lebih kecil dari 5.

<!-- Old headings. Do not remove or links may break. -->

<a id="testing-equality-with-the-assert_eq-and-assert_ne-macros"></a>

### Menguji Kesetaraan dengan `assert_eq!` dan `assert_ne!`

Cara umum untuk memverifikasi fungsi adalah menguji kesetaraan antara hasil kode yang ditest dan nilai yang kamu harapkan dikembalikan kode itu. Kamu bisa melakukan ini dengan memakai macro `assert!` dan memberinya ekspresi yang memakai operator `==`. Namun, test semacam ini sangat umum sehingga library standar menyediakan sepasang macro—`assert_eq!` dan `assert_ne!`—untuk melakukan test ini dengan lebih praktis. Kedua macro ini membandingkan dua argumen untuk kesetaraan atau ketidaksetaraan. Keduanya juga akan mencetak kedua nilai jika assertion gagal, sehingga lebih mudah melihat _mengapa_ test gagal; sebaliknya, macro `assert!` hanya menunjukkan bahwa ia mendapat nilai `false` untuk ekspresi `==`, tanpa mencetak nilai-nilai yang menyebabkan nilai `false` itu.

Di Daftar 11-7, kita menulis fungsi bernama `add_two` yang menambahkan `2` pada parameternya, lalu kita test fungsi ini memakai macro `assert_eq!`.

<Listing number="11-7" file-name="src/lib.rs" caption="Menguji fungsi `add_two` memakai macro `assert_eq!`">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-07/src/lib.rs}}
```

</Listing>

Mari kita cek bahwa test ini lulus!

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-07/output.txt}}
```

Kita membuat variabel bernama `result` yang menyimpan hasil pemanggilan `add_two(2)`. Lalu, kita memberikan `result` dan `4` sebagai argumen macro `assert_eq!`. Baris keluaran untuk test ini adalah `test tests::it_adds_two ... ok`, dan teks `ok` menunjukkan bahwa test kita lulus!

Mari kita masukkan bug ke dalam kode untuk melihat seperti apa `assert_eq!` ketika gagal. Ubah implementasi fungsi `add_two` sehingga menambahkan `3`:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/src/lib.rs:here}}
```

Jalankan test lagi:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/output.txt}}
```

Test kita menangkap bug! Test `tests::it_adds_two` gagal, dan pesannya memberi tahu kita bahwa assertion yang gagal adalah `left == right` serta apa nilai `left` dan `right`-nya. Pesan ini membantu kita mulai melakukan debug: argumen `left`, tempat kita menyimpan hasil `add_two(2)`, adalah `5`, tetapi argumen `right` adalah `4`. Kamu bisa bayangkan betapa bergunanya ini ketika ada banyak test yang berjalan.

Perlu dicatat bahwa di beberapa bahasa dan framework test, parameter fungsi assertion kesetaraan disebut `expected` dan `actual`, dan urutan kita menentukan argumen itu penting. Namun, di Rust keduanya disebut `left` dan `right`, dan urutan kita menentukan nilai yang kita harapkan serta nilai yang dihasilkan kode tidak penting. Kita bisa menulis assertion dalam test ini sebagai `assert_eq!(4, result)`, yang akan menghasilkan pesan kegagalan yang sama yaitu `` assertion `left == right` failed ``.

Macro `assert_ne!` akan lulus jika dua nilai yang kita berikan tidak sama dan akan gagal jika keduanya sama. Macro ini paling berguna untuk kasus ketika kita tidak yakin apa nilai sesuatu _akan_ menjadi, tetapi kita tahu nilai itu pasti _tidak boleh_ menjadi apa. Misalnya, jika kita mengetes fungsi yang dijamin akan mengubah inputnya dengan cara tertentu, tetapi cara input itu diubah bergantung pada hari dalam seminggu saat kita menjalankan test, hal terbaik untuk ditegaskan mungkin bahwa keluaran fungsi tidak sama dengan inputnya.

Di balik permukaan, macro `assert_eq!` dan `assert_ne!` memakai operator `==` dan `!=`. Saat assertion gagal, kedua macro ini mencetak argumennya memakai format debug, yang berarti nilai yang dibandingkan harus mengimplementasikan trait `PartialEq` dan `Debug`. Semua tipe primitif dan sebagian besar tipe di library standar mengimplementasikan trait ini. Untuk struct dan enum yang kamu definisikan sendiri, kamu perlu mengimplementasikan `PartialEq` untuk menyatakan kesetaraan tipe-tipe itu. Kamu juga perlu mengimplementasikan `Debug` untuk mencetak nilai ketika assertion gagal. Karena kedua trait tersebut adalah trait yang bisa diturunkan (derivable), seperti disebutkan di Daftar 5-12 Bab 5, ini biasanya semudah menambahkan anotasi `#[derive(PartialEq, Debug)]` pada definisi struct atau enum kamu. Lihat Lampiran C, [“Trait yang Bisa Diturunkan,”][derivable-traits]<!-- ignore --> untuk rincian lebih lanjut tentang trait ini dan trait lain yang bisa diturunkan.

### Menambahkan Pesan Kegagalan Kustom

Kamu juga bisa menambahkan pesan kustom untuk dicetak bersama pesan kegagalan sebagai argumen opsional pada macro `assert!`, `assert_eq!`, dan `assert_ne!`. Argumen apa pun yang ditentukan setelah argumen wajib diteruskan ke macro `format!` (dibahas di [“Menggabungkan dengan `+` atau `format!`”][concatenating]<!-- ignore --> Bab 8), jadi kamu bisa memberikan string format yang berisi placeholder `{}` dan nilai-nilai untuk mengisi placeholder itu. Pesan kustom berguna untuk mendokumentasikan maksud sebuah assertion; ketika test gagal, kamu akan lebih paham apa masalahnya dengan kode kamu.

Misalnya, kita punya fungsi yang menyapa orang berdasarkan nama, dan kita ingin mengetes bahwa nama yang kita berikan ke fungsi itu muncul di keluaran:

<span class="filename">Nama file: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-05-greeter/src/lib.rs}}
```

Persyaratan program ini belum disepakati, dan kita cukup yakin teks `Hello` di awal sapaan akan berubah. Kita memutuskan tidak ingin harus memperbarui test ketika persyaratan berubah, jadi alih-alih memeriksa kesetaraan persis dengan nilai yang dikembalikan fungsi `greeting`, kita cukup memastikan bahwa keluarannya mengandung teks dari parameter masukan.

Sekarang mari kita masukkan bug ke kode ini dengan mengubah `greeting` agar tidak menyertakan `name`, untuk melihat seperti apa kegagalan test bawaan:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/src/lib.rs:here}}
```

Menjalankan test ini menghasilkan sebagai berikut:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/output.txt}}
```

Hasil ini hanya menunjukkan bahwa assertion gagal dan di baris mana assertion itu berada. Pesan kegagalan yang lebih berguna akan mencetak nilai dari fungsi `greeting`. Mari kita tambahkan pesan kegagalan kustom yang terdiri dari string format dengan placeholder yang diisi nilai aktual yang kita dapat dari fungsi `greeting`:

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/src/lib.rs:here}}
```

Sekarang saat kita menjalankan test, kita akan mendapat pesan error yang lebih informatif:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/output.txt}}
```

Kita bisa melihat nilai yang benar-benar kita dapat di keluaran test, yang membantu kita melakukan debug tentang apa yang terjadi alih-alih apa yang kita harapkan terjadi.

### Memeriksa Panic dengan `should_panic`

Selain memeriksa nilai kembalian, penting juga untuk memeriksa bahwa kode kita menangani kondisi error sesuai yang kita harapkan. Misalnya, pertimbangkan tipe `Guess` yang kita buat di Bab 9, Daftar 9-13. Kode lain yang memakai `Guess` bergantung pada jaminan bahwa instance `Guess` hanya berisi nilai antara 1 dan 100. Kita bisa menulis test yang memastikan bahwa percobaan membuat instance `Guess` dengan nilai di luar rentang itu menyebabkan panic.

Kita melakukan ini dengan menambahkan atribut `should_panic` pada fungsi test kita. Test lulus jika kode di dalam fungsi itu panic; test gagal jika kode di dalam fungsi itu tidak panic.

Daftar 11-8 menampilkan test yang memeriksa bahwa kondisi error dari `Guess::new` terjadi pada saat yang kita harapkan.

<Listing number="11-8" file-name="src/lib.rs" caption="Menguji bahwa suatu kondisi akan menyebabkan `panic!`">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-08/src/lib.rs}}
```

</Listing>

Kita menempatkan atribut `#[should_panic]` setelah atribut `#[test]` dan sebelum fungsi test yang dikenainya. Mari kita lihat hasilnya ketika test ini lulus:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-08/output.txt}}
```

Terlihat bagus! Sekarang mari kita masukkan bug ke dalam kode dengan menghapus kondisi bahwa fungsi `new` akan panic jika nilainya lebih dari 100:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/src/lib.rs:here}}
```

Saat kita menjalankan test di Daftar 11-8, test itu akan gagal:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/output.txt}}
```

Kita tidak mendapat pesan yang terlalu membantu dalam kasus ini, tetapi ketika melihat fungsi testnya, kita mendapati bahwa ia diberi anotasi `#[should_panic]`. Kegagalan yang kita dapat berarti kode di dalam fungsi test itu tidak menyebabkan panic.

Test yang memakai `should_panic` bisa kurang tepat. Sebuah test `should_panic` akan lulus meskipun test panic karena alasan yang berbeda dari yang kita harapkan. Agar test `should_panic` lebih tepat, kita bisa menambahkan parameter opsional `expected` pada atribut `should_panic`. Test harness akan memastikan bahwa pesan kegagalan mengandung teks yang diberikan. Misalnya, pertimbangkan kode `Guess` yang dimodifikasi di Daftar 11-9, di mana fungsi `new` panic dengan pesan berbeda bergantung pada apakah nilainya terlalu kecil atau terlalu besar.

<Listing number="11-9" file-name="src/lib.rs" caption="Menguji `panic!` dengan pesan panic yang berisi substring tertentu">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-09/src/lib.rs:here}}
```

</Listing>

Test ini akan lulus karena nilai yang kita letakkan pada parameter `expected` atribut `should_panic` adalah substring dari pesan yang dipakai `Guess::new` saat panic. Kita bisa saja menentukan seluruh pesan panic yang kita harapkan, yang dalam kasus ini adalah `Guess value must be less than or equal to 100, got 200`. Apa yang kamu pilih untuk ditentukan bergantung pada seberapa unik atau dinamis pesan panic itu dan seberapa tepat kamu ingin test kamu. Dalam kasus ini, substring dari pesan panic sudah cukup untuk memastikan bahwa kode dalam fungsi test menjalankan cabang `else if value > 100`.

Untuk melihat apa yang terjadi ketika test `should_panic` dengan pesan `expected` gagal, mari kita masukkan bug lagi ke dalam kode dengan menukar isi blok `if value < 1` dan `else if value > 100`:

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/src/lib.rs:here}}
```

Kali ini saat kita menjalankan test `should_panic`, test itu akan gagal:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/output.txt}}
```

Pesan kegagalan menunjukkan bahwa test ini memang panic seperti yang kita harapkan, tetapi pesan panicnya tidak memuat string yang diharapkan `less than or equal to 100`. Pesan panic yang benar-benar kita dapat dalam kasus ini adalah `Guess value must be greater than or equal to 1, got 200`. Sekarang kita bisa mulai mencari tahu di mana bug kita!

### Memakai `Result<T, E>` dalam Test

Semua test kita sejauh ini panic saat gagal. Kita juga bisa menulis test yang memakai `Result<T, E>`! Ini test dari Daftar 11-1, yang ditulis ulang untuk memakai `Result<T, E>` dan mengembalikan `Err` alih-alih panic:

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-10-result-in-tests/src/lib.rs:here}}
```

Fungsi `it_works` sekarang memiliki tipe kembalian `Result<(), String>`. Di dalam badan fungsi, alih-alih memanggil macro `assert_eq!`, kita mengembalikan `Ok(())` ketika test lulus dan `Err` yang berisi `String` ketika test gagal.

Menulis test sehingga mengembalikan `Result<T, E>` memungkinkan kamu memakai operator tanda tanya di dalam badan test, yang bisa menjadi cara praktis untuk menulis test yang seharusnya gagal jika ada operasi di dalamnya yang mengembalikan varian `Err`.

Kamu tidak bisa memakai anotasi `#[should_panic]` pada test yang memakai `Result<T, E>`. Untuk menyatakan bahwa sebuah operasi mengembalikan varian `Err`, _jangan_ pakai operator tanda tanya pada nilai `Result<T, E>` itu. Sebagai gantinya, pakai `assert!(value.is_err())`.

Sekarang setelah kamu tahu beberapa cara menulis test, mari kita lihat apa yang terjadi saat kita menjalankan test dan menjelajahi berbagai opsi yang bisa kita pakai dengan `cargo test`.

[concatenating]: ch08-02-strings.html#concatenating-with--or-format
[bench]: ../unstable-book/library-features/test.html
[ignoring]: ch11-02-running-tests.html#ignoring-tests-unless-specifically-requested
[subset]: ch11-02-running-tests.html#running-a-subset-of-tests-by-name
[controlling-how-tests-are-run]: ch11-02-running-tests.html#controlling-how-tests-are-run
[derivable-traits]: appendix-03-derivable-traits.html
[doc-comments]: ch14-02-publishing-to-crates-io.html#documentation-comments-as-tests
[paths-for-referring-to-an-item-in-the-module-tree]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
