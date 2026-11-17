<!-- Old headings. Do not remove or links may break. -->

<a id="turning-our-single-threaded-server-into-a-multithreaded-server"></a>
<a id="from-single-threaded-to-multithreaded-server"></a>

## Dari Server Single-Threaded ke Server Multithreaded

Saat ini, server memproses setiap request bergiliran, artinya ia tidak akan memproses koneksi kedua sampai koneksi pertama selesai diproses. Jika server menerima makin banyak request, eksekusi serial ini akan semakin tidak optimal. Jika server menerima request yang butuh waktu lama untuk diproses, request-request berikutnya harus menunggu sampai request yang lama itu selesai, meskipun request baru bisa diproses dengan cepat. Kita perlu memperbaiki ini, tetapi pertama-tama kita akan melihat masalahnya secara langsung.

<!-- Old headings. Do not remove or links may break. -->

<a id="simulating-a-slow-request-in-the-current-server-implementation"></a>

### Mensimulasikan Request yang Lambat

Kita akan melihat bagaimana sebuah request yang diproses secara lambat bisa memengaruhi request lain yang dikirim ke implementasi server kita saat ini. Listing 21-10 mengimplementasikan penanganan request ke _/sleep_ dengan respons lambat yang disimulasikan, yang membuat server tidur selama lima detik sebelum merespons.

<Listing number="21-10" file-name="src/main.rs" caption="Mensimulasikan request lambat dengan tidur selama lima detik">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-10/src/main.rs:here}}
```

</Listing>

Kita beralih dari `if` ke `match` sekarang karena kita punya tiga kasus. Kita perlu secara eksplisit mencocokkan slice dari `request_line` untuk melakukan pencocokan pola terhadap nilai literal string; `match` tidak melakukan referencing dan dereferencing otomatis seperti yang dilakukan metode equality.

Cabang pertama sama dengan blok `if` dari Listing 21-9. Cabang kedua mencocokkan request ke _/sleep_. Saat request itu diterima, server akan tidur selama lima detik sebelum merender halaman HTML yang berhasil. Cabang ketiga sama dengan blok `else` dari Listing 21-9.

Kamu bisa melihat betapa primitifnya server kita: library sungguhan akan menangani pengenalan banyak request dengan cara yang jauh lebih ringkas!

Jalankan server dengan `cargo run`. Lalu, buka dua jendela browser: satu untuk _http://127.0.0.1:7878_ dan satu lagi untuk _http://127.0.0.1:7878/sleep_. Jika kamu memasukkan URI _/_ beberapa kali, seperti sebelumnya, kamu akan melihatnya merespons dengan cepat. Tetapi jika kamu memasukkan _/sleep_ lalu memuat _/_, kamu akan melihat bahwa _/_ menunggu sampai `sleep` menyelesaikan tidurnya selama lima detik penuh sebelum dimuat.

Ada beberapa teknik yang bisa kita pakai untuk mencegah request menumpuk di belakang request yang lambat, termasuk memakai async seperti yang kita lakukan di Bab 17; teknik yang akan kita implementasikan adalah thread pool.

### Meningkatkan Throughput dengan Thread Pool

Sebuah _thread pool_ adalah sekumpulan thread yang sudah di-spawn dan siap menunggu untuk menangani sebuah tugas. Saat program menerima tugas baru, ia menugaskan salah satu thread di pool ke tugas itu, dan thread tersebut akan memprosesnya. Thread-thread lain di pool tetap tersedia untuk menangani tugas lain yang masuk selagi thread pertama masih memproses. Setelah thread pertama selesai memproses tugasnya, ia dikembalikan ke kumpulan thread yang menganggur, siap menangani tugas baru. Thread pool memungkinkan kamu memproses koneksi secara concurrent, sehingga throughput server kamu meningkat.

Kita akan membatasi jumlah thread di pool ke angka yang kecil untuk melindungi kita dari serangan DoS; jika program kita membuat thread baru untuk setiap request yang masuk, seseorang yang mengirim 10 juta request ke server kita bisa membuat kacau dengan menghabiskan semua sumber daya server dan menghentikan pemrosesan request sama sekali.

Jadi, alih-alih membuat thread tanpa batas, kita akan punya jumlah thread tetap yang menunggu di pool. Request yang masuk dikirim ke pool untuk diproses. Pool akan menjaga antrean request yang masuk. Setiap thread di pool akan mengambil sebuah request dari antrean ini, menanganinya, lalu meminta request lain dari antrean. Dengan desain ini, kita bisa memproses hingga _`N`_ request secara concurrent, dengan _`N`_ adalah jumlah thread. Jika setiap thread sedang merespons request yang berjalan lama, request berikutnya tetap bisa menumpuk di antrean, tetapi kita sudah menambah jumlah request berjalan lama yang bisa kita tangani sebelum mencapai titik itu.

Teknik ini hanyalah salah satu dari banyak cara untuk meningkatkan throughput server web. Opsi lain yang bisa kamu jelajahi adalah model fork/join, model I/O async single-threaded, dan model I/O async multithreaded. Jika kamu tertarik dengan topik ini, kamu bisa membaca lebih lanjut tentang solusi lain dan mencoba mengimplementasikannya; dengan bahasa setingkat rendah seperti Rust, semua opsi ini mungkin dilakukan.

Sebelum mulai mengimplementasikan thread pool, mari kita bicarakan seperti apa penggunaan pool ini seharusnya. Saat kamu merancang kode, menulis antarmuka klien terlebih dahulu bisa membantu memandu desainmu. Tulis API kode sedemikian rupa sehingga tersusun seperti yang kamu ingin panggil; lalu, implementasikan fungsionalitas di dalam struktur itu, bukan mengimplementasikan fungsionalitas dulu baru merancang API publiknya.

Mirip dengan cara kita memakai pengembangan berbasis test di proyek Bab 12, di sini kita akan memakai pengembangan berbasis compiler. Kita akan menulis kode yang memanggil fungsi-fungsi yang kita inginkan, lalu melihat error dari compiler untuk menentukan apa yang harus kita ubah berikutnya agar kode berjalan. Namun, sebelum melakukan itu, kita akan menjelajahi teknik yang tidak akan kita pakai sebagai titik awal.

<!-- Old headings. Do not remove or links may break. -->

<a id="code-structure-if-we-could-spawn-a-thread-for-each-request"></a>

#### Membuat Thread untuk Setiap Request

Pertama, mari kita lihat seperti apa kode kita jika ia benar-benar membuat thread baru untuk setiap koneksi. Seperti disebutkan sebelumnya, ini bukan rencana final kita karena masalah potensial dalam membuat thread dalam jumlah tak terbatas, tetapi ini adalah titik awal untuk mendapatkan server multithreaded yang berjalan dulu. Lalu, kita akan menambahkan thread pool sebagai perbaikan, dan membandingkan kedua solusi akan lebih mudah.

Listing 21-11 menunjukkan perubahan yang perlu dibuat pada `main` untuk membuat thread baru guna menangani setiap stream di dalam loop `for`.

<Listing number="21-11" file-name="src/main.rs" caption="Membuat thread baru untuk setiap stream">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-11/src/main.rs:here}}
```

</Listing>

Seperti yang kamu pelajari di Bab 16, `thread::spawn` akan membuat thread baru lalu menjalankan kode di dalam closure di thread baru itu. Jika kamu menjalankan kode ini dan memuat _/sleep_ di browser, lalu _/_ di dua tab browser lagi, kamu akan benar-benar melihat bahwa request ke _/_ tidak perlu menunggu _/sleep_ selesai. Namun, seperti yang kita sebutkan, pada akhirnya ini akan membebani sistem karena kamu membuat thread baru tanpa batas.

Kamu mungkin juga ingat dari Bab 17 bahwa ini adalah situasi yang tepat di mana async dan await benar-benar bersinar! Ingat itu saat kita membangun thread pool, dan pikirkan seperti apa perbedaan atau kesamaannya dengan async.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-a-similar-interface-for-a-finite-number-of-threads"></a>

<a id="creating-a-finite-number-of-threads"></a>
#### Membuat Jumlah Thread yang Terbatas

Kita ingin thread pool kita bekerja dengan cara yang serupa dan akrab, sehingga beralih dari thread ke thread pool tidak memerlukan perubahan besar pada kode yang memakai API kita. Listing 21-12 menunjukkan antarmuka hipotetis untuk struct `ThreadPool` yang ingin kita pakai sebagai pengganti `thread::spawn`.

<Listing number="21-12" file-name="src/main.rs" caption="Antarmuka `ThreadPool` ideal kita">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-12/src/main.rs:here}}
```

</Listing>

Kita memakai `ThreadPool::new` untuk membuat thread pool baru dengan jumlah thread yang bisa dikonfigurasi, dalam hal ini empat. Lalu, di dalam loop `for`, `pool.execute` punya antarmuka yang mirip dengan `thread::spawn`, karena menerima closure yang harus dijalankan pool untuk setiap stream. Kita perlu mengimplementasikan `pool.execute` agar menerima closure itu dan memberikannya ke thread di pool untuk dijalankan. Kode ini belum akan terkompilasi, tetapi kita akan mencobanya agar compiler bisa memandu kita memperbaikinya.

<!-- Old headings. Do not remove or links may break. -->

<a id="building-the-threadpool-struct-using-compiler-driven-development"></a>

#### Membangun `ThreadPool` dengan Pengembangan Berbasis Compiler

Lakukan perubahan dari Listing 21-12 pada _src/main.rs_, lalu mari kita pakai error compiler dari `cargo check` untuk memandu pengembangan kita. Berikut adalah error pertama yang kita dapatkan:

```console
{{#include ../listings/ch21-web-server/listing-21-12/output.txt}}
```

Bagus! Error ini memberi tahu kita bahwa kita memerlukan tipe atau module `ThreadPool`, jadi kita akan membuatnya sekarang. Implementasi `ThreadPool` kita akan independen dari jenis pekerjaan yang dilakukan server web kita. Jadi, mari kita ubah crate `hello` dari binary crate menjadi library crate untuk menampung implementasi `ThreadPool` kita. Setelah berubah menjadi library crate, kita juga bisa memakai library thread pool yang terpisah untuk pekerjaan apa pun yang ingin kita lakukan dengan thread pool, tidak hanya untuk melayani request web.

Buat file _src/lib.rs_ yang berisi kode berikut, yaitu definisi paling sederhana dari struct `ThreadPool` yang bisa kita punya untuk saat ini:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/lib.rs}}
```

</Listing>


Lalu, edit file _main.rs_ untuk membawa `ThreadPool` ke dalam scope dari library crate dengan menambahkan kode berikut di bagian atas _src/main.rs_:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/main.rs:here}}
```

</Listing>

Kode ini masih belum berjalan, tetapi mari kita cek lagi untuk mendapatkan error berikutnya yang perlu kita tangani:

```console
{{#include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/output.txt}}
```

Error ini menunjukkan bahwa berikutnya kita perlu membuat fungsi asosiasi bernama `new` untuk `ThreadPool`. Kita juga tahu bahwa `new` perlu punya satu parameter yang bisa menerima `4` sebagai argumen dan harus mengembalikan instance `ThreadPool`. Mari kita implementasikan fungsi `new` paling sederhana yang punya karakteristik itu:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/src/lib.rs}}
```

</Listing>

Kita memilih `usize` sebagai tipe parameter `size` karena kita tahu bahwa jumlah thread negatif tidak masuk akal. Kita juga tahu kita akan memakai `4` ini sebagai jumlah elemen dalam koleksi thread, yang memang itulah kegunaan tipe `usize`, seperti dibahas di bagian [“Tipe Integer”][integer-types]<!-- ignore --> Bab 3.

Mari kita cek kode lagi:

```console
{{#include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/output.txt}}
```

Sekarang error muncul karena kita belum punya metode `execute` pada `ThreadPool`. Ingat dari bagian [“Membuat Jumlah Thread yang Terbatas”](#creating-a-finite-number-of-threads)<!-- ignore --> bahwa kita memutuskan thread pool kita harus punya antarmuka serupa dengan `thread::spawn`. Selain itu, kita akan mengimplementasikan fungsi `execute` agar menerima closure yang diberikan kepadanya dan memberikannya ke thread menganggur di pool untuk dijalankan.

Kita akan mendefinisikan metode `execute` pada `ThreadPool` untuk menerima closure sebagai parameter. Ingat dari [“Memindahkan Nilai yang Ditangkap keluar dari Closure”][moving-out-of-closures]<!-- ignore --> Bab 13 bahwa kita bisa menerima closure sebagai parameter dengan tiga trait berbeda: `Fn`, `FnMut`, dan `FnOnce`. Kita perlu memutuskan jenis closure mana yang dipakai di sini. Kita tahu kita akan melakukan sesuatu yang mirip dengan implementasi `thread::spawn` di library standar, jadi kita bisa melihat bound apa yang ada pada parameter di signature `thread::spawn`. Dokumentasi menunjukkan hal berikut:

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

Parameter tipe `F` adalah yang kita perhatikan di sini; parameter tipe `T` berkaitan dengan nilai kembalian, dan kita tidak memperhatikannya. Kita bisa melihat bahwa `spawn` memakai `FnOnce` sebagai trait bound pada `F`. Ini kemungkinan besar memang yang kita inginkan, karena pada akhirnya kita akan meneruskan argumen yang kita terima di `execute` ke `spawn`. Kita bisa makin yakin bahwa `FnOnce` adalah trait yang ingin kita pakai karena thread untuk menjalankan sebuah request hanya akan mengeksekusi closure request itu satu kali, yang sesuai dengan `Once` dalam `FnOnce`.

Parameter tipe `F` juga punya trait bound `Send` dan lifetime bound `'static`, yang berguna dalam situasi kita: Kita memerlukan `Send` untuk memindahkan closure dari satu thread ke thread lain dan `'static` karena kita tidak tahu berapa lama thread akan membutuhkan waktu untuk mengeksekusi. Mari kita buat metode `execute` pada `ThreadPool` yang menerima parameter generic bertipe `F` dengan bound-bound ini:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-03-define-execute/src/lib.rs:here}}
```

</Listing>

Kita tetap memakai `()` setelah `FnOnce` karena `FnOnce` ini mewakili closure yang tidak menerima parameter dan mengembalikan tipe unit `()`. Sama seperti definisi fungsi, tipe kembalian bisa dihilangkan dari signature, tetapi meskipun kita tidak punya parameter, tanda kurung tetap diperlukan.

Sekali lagi, ini adalah implementasi paling sederhana dari metode `execute`: ia tidak melakukan apa-apa, tetapi kita hanya berusaha membuat kode kita terkompilasi. Mari kita cek lagi:

```console
{{#include ../listings/ch21-web-server/no-listing-03-define-execute/output.txt}}
```

Kode itu terkompilasi! Tetapi perhatikan bahwa jika kamu mencoba `cargo run` dan mengirim request lewat browser, kamu akan melihat error di browser seperti yang kita lihat di awal bab. Library kita sebenarnya belum memanggil closure yang diteruskan ke `execute`!

> Catatan: Ada pepatah yang mungkin kamu dengar tentang bahasa dengan compiler yang ketat, seperti Haskell dan Rust, yaitu “Jika kode terkompilasi, kode itu berjalan.” Tetapi pepatah ini tidak selalu benar. Proyek kita terkompilasi, tetapi sama sekali tidak melakukan apa-apa! Jika kita sedang membangun proyek yang nyata dan lengkap, ini akan menjadi waktu yang tepat untuk mulai menulis unit test guna memeriksa bahwa kode terkompilasi _dan_ punya perilaku yang kita inginkan.

Pikirkan: Apa yang akan berbeda di sini jika kita akan mengeksekusi future alih-alih closure?

#### Memvalidasi Jumlah Thread di `new`

Kita belum melakukan apa-apa dengan parameter `new` dan `execute`. Mari kita implementasi isi kedua fungsi ini dengan perilaku yang kita inginkan. Untuk mulai, mari kita pikirkan tentang `new`. Sebelumnya kita memilih tipe unsigned untuk parameter `size` karena pool dengan jumlah thread negatif tidak masuk akal. Namun, pool dengan nol thread juga tidak masuk akal, sementara nol adalah nilai `usize` yang sepenuhnya valid. Kita akan menambahkan kode untuk memeriksa bahwa `size` lebih besar dari nol sebelum mengembalikan instance `ThreadPool`, dan kita akan membuat program panic jika menerima nol dengan memakai macro `assert!`, seperti ditunjukkan pada Listing 21-13.

<Listing number="21-13" file-name="src/lib.rs" caption="Mengimplementasikan `ThreadPool::new` agar panic jika `size` nol">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-13/src/lib.rs:here}}
```

</Listing>

Kita juga telah menambahkan dokumentasi untuk `ThreadPool` kita dengan doc comment. Perhatikan bahwa kita mengikuti praktik dokumentasi yang baik dengan menambahkan bagian yang menyebutkan situasi-situasi di mana fungsi kita bisa panic, seperti dibahas di Bab 14. Coba jalankan `cargo doc --open` dan klik struct `ThreadPool` untuk melihat seperti apa dokumentasi `new` yang dihasilkan!

Alih-alih menambahkan macro `assert!` seperti yang kita lakukan di sini, kita bisa mengubah `new` menjadi `build` dan mengembalikan `Result` seperti yang kita lakukan dengan `Config::build` di proyek I/O pada Listing 12-9. Tetapi kita memutuskan dalam kasus ini bahwa mencoba membuat thread pool tanpa thread sama sekali seharusnya menjadi error yang tidak bisa dipulihkan. Jika kamu merasa ambisius, coba tulis fungsi bernama `build` dengan signature berikut untuk dibandingkan dengan fungsi `new`:

```rust,ignore
pub fn build(size: usize) -> Result<ThreadPool, PoolCreationError> {
```

#### Membuat Ruang untuk Menyimpan Thread

Sekarang kita punya cara untuk mengetahui bahwa kita memiliki jumlah thread yang valid untuk disimpan di pool, kita bisa membuat thread-thread itu dan menyimpannya di struct `ThreadPool` sebelum mengembalikan struct tersebut. Tetapi bagaimana cara kita “menyimpan” sebuah thread? Mari kita lihat lagi signature `thread::spawn`:

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

Fungsi `spawn` mengembalikan `JoinHandle<T>`, dengan `T` adalah tipe yang dikembalikan closure. Mari kita coba memakai `JoinHandle` juga dan melihat apa yang terjadi. Dalam kasus kita, closure yang kita teruskan ke thread pool akan menangani koneksi dan tidak mengembalikan apa pun, sehingga `T` akan menjadi tipe unit `()`.

Kode pada Listing 21-14 akan terkompilasi, tetapi belum membuat thread apa pun. Kita telah mengubah definisi `ThreadPool` agar menyimpan vector berisi instance `thread::JoinHandle<()>`, menginisialisasi vector itu dengan kapasitas `size`, menyiapkan loop `for` yang akan menjalankan kode untuk membuat thread, dan mengembalikan instance `ThreadPool` yang berisi thread-thread itu.

<Listing number="21-14" file-name="src/lib.rs" caption="Membuat vector agar `ThreadPool` menyimpan thread">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-14/src/lib.rs:here}}
```

</Listing>

Kita telah membawa `std::thread` ke dalam scope di library crate karena kita memakai `thread::JoinHandle` sebagai tipe item di dalam vector pada `ThreadPool`.

Setelah ukuran yang valid diterima, `ThreadPool` kita membuat vector baru yang bisa menampung `size` item. Fungsi `with_capacity` melakukan tugas yang sama dengan `Vec::new`, tetapi dengan perbedaan penting: ia mengalokasikan ruang terlebih dahulu di vector. Karena kita tahu kita perlu menyimpan `size` elemen di vector, melakukan alokasi ini di awal sedikit lebih efisien daripada memakai `Vec::new`, yang mengubah ukurannya sendiri saat elemen disisipkan.

Saat kamu menjalankan `cargo check` lagi, seharusnya berhasil.

<!-- Old headings. Do not remove or links may break. -->
<a id ="a-worker-struct-responsible-for-sending-code-from-the-threadpool-to-a-thread"></a>

#### Mengirim Kode dari `ThreadPool` ke Thread

Kita meninggalkan komentar di loop `for` pada Listing 21-14 tentang pembuatan thread. Di sini, kita akan melihat bagaimana kita benar-benar membuat thread. Library standar menyediakan `thread::spawn` sebagai cara membuat thread, dan `thread::spawn` mengharapkan mendapat kode yang harus dijalankan thread begitu thread dibuat. Namun, dalam kasus kita, kita ingin membuat thread-thread itu dan membuat mereka _menunggu_ kode yang akan kita kirim nanti. Implementasi thread di library standar tidak punya cara untuk melakukan itu; kita harus mengimplementasikannya sendiri.

Kita akan mengimplementasikan perilaku ini dengan memperkenalkan struktur data baru antara `ThreadPool` dan thread-thread yang akan mengelola perilaku baru ini. Kita menyebut struktur data ini _Worker_, istilah yang umum dalam implementasi pooling. `Worker` mengambil kode yang perlu dijalankan dan menjalankannya di thread-nya.

Bayangkan orang-orang yang bekerja di dapur sebuah restoran: para pekerja menunggu sampai pesanan datang dari pelanggan, lalu mereka bertugas mengambil pesanan itu dan menyiapkannya.

Alih-alih menyimpan vector berisi instance `JoinHandle<()>` di thread pool, kita akan menyimpan instance struct `Worker`. Setiap `Worker` akan menyimpan satu instance `JoinHandle<()>`. Lalu, kita akan mengimplementasikan metode pada `Worker` yang menerima closure berisi kode untuk dijalankan dan mengirimkannya ke thread yang sudah berjalan agar dieksekusi. Kita juga akan memberi setiap `Worker` sebuah `id` agar bisa membedakan antar-instance `Worker` di pool saat mencatat log atau melakukan debug.

Berikut adalah proses baru yang terjadi saat kita membuat `ThreadPool`. Kita akan mengimplementasikan kode yang mengirim closure ke thread setelah `Worker` kita siapkan dengan cara ini:

1. Definisikan struct `Worker` yang menyimpan `id` dan `JoinHandle<()>`.
2. Ubah `ThreadPool` agar menyimpan vector berisi instance `Worker`.
3. Definisikan fungsi `Worker::new` yang menerima angka `id` dan mengembalikan instance `Worker` yang menyimpan `id` itu serta thread yang dibuat dengan closure kosong.
4. Di `ThreadPool::new`, gunakan penghitung loop `for` untuk menghasilkan `id`, buat `Worker` baru dengan `id` itu, dan simpan `Worker` tersebut di dalam vector.

Jika kamu siap menghadapi tantangan, coba implementasikan perubahan ini sendiri sebelum melihat kode pada Listing 21-15.

Siap? Berikut adalah Listing 21-15 dengan salah satu cara untuk melakukan perubahan di atas.

<Listing number="21-15" file-name="src/lib.rs" caption="Mengubah `ThreadPool` agar menyimpan instance `Worker`, bukan menyimpan thread secara langsung">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-15/src/lib.rs:here}}
```

</Listing>

Kita telah mengubah nama field pada `ThreadPool` dari `threads` menjadi `workers` karena sekarang ia menyimpan instance `Worker`, bukan instance `JoinHandle<()>`. Kita memakai penghitung di loop `for` sebagai argumen untuk `Worker::new`, dan kita menyimpan setiap `Worker` baru di vector bernama `workers`.

Kode eksternal (seperti server kita di _src/main.rs_) tidak perlu tahu detail implementasi tentang pemakaian struct `Worker` di dalam `ThreadPool`, jadi kita membuat struct `Worker` dan fungsi `new`-nya bersifat private. Fungsi `Worker::new` memakai `id` yang kita berikan dan menyimpan instance `JoinHandle<()>` yang dibuat dengan membuat thread baru memakai closure kosong.

> Catatan: Jika sistem operasi tidak bisa membuat thread karena sumber daya sistem tidak cukup, `thread::spawn` akan panic. Hal itu akan membuat seluruh server kita panic, meskipun pembuatan sebagian thread mungkin berhasil. Demi kesederhanaan, perilaku ini tidak apa-apa, tetapi dalam implementasi thread pool untuk produksi, kamu kemungkinan ingin memakai [`std::thread::Builder`][builder]<!-- ignore --> dan metode [`spawn`][builder-spawn]<!-- ignore -->-nya yang mengembalikan `Result`.

Kode ini akan terkompilasi dan menyimpan sejumlah instance `Worker` yang kita tentukan sebagai argumen untuk `ThreadPool::new`. Tetapi kita _masih_ belum memproses closure yang kita terima di `execute`. Mari kita lihat cara melakukannya berikutnya.

#### Mengirim Request ke Thread melalui Channel

Masalah berikutnya yang akan kita tangani adalah closure yang diberikan kepada `thread::spawn` sama sekali tidak melakukan apa-apa. Saat ini, kita mendapat closure yang ingin kita jalankan di metode `execute`. Tetapi kita perlu memberikan `thread::spawn` sebuah closure untuk dijalankan saat kita membuat setiap `Worker` selama pembuatan `ThreadPool`.

Kita ingin struct `Worker` yang baru kita buat mengambil kode untuk dijalankan dari antrean yang disimpan di `ThreadPool`, lalu mengirim kode itu ke thread-nya untuk dijalankan.

Channel yang kita pelajari di Bab 16—cara sederhana untuk berkomunikasi antara dua thread—sangat cocok untuk kasus ini. Kita akan memakai channel sebagai antrean pekerjaan, dan `execute` akan mengirim pekerjaan dari `ThreadPool` ke instance `Worker`, yang lalu akan meneruskan pekerjaan itu ke thread-nya. Berikut rencananya:

1. `ThreadPool` akan membuat channel dan menyimpan sender-nya.
2. Setiap `Worker` akan menyimpan receiver-nya.
3. Kita akan membuat struct `Job` baru yang menyimpan closure yang ingin kita kirim melalui channel.
4. Metode `execute` akan mengirim pekerjaan yang ingin dijalankannya melalui sender.
5. Di thread-nya, `Worker` akan melakukan loop pada receiver-nya dan mengeksekusi closure dari pekerjaan apa pun yang diterimanya.

Mari kita mulai dengan membuat channel di `ThreadPool::new` dan menyimpan sender di instance `ThreadPool`, seperti ditunjukkan pada Listing 21-16. Struct `Job` untuk saat ini tidak menyimpan apa pun, tetapi akan menjadi tipe item yang kita kirim melalui channel.

<Listing number="21-16" file-name="src/lib.rs" caption="Mengubah `ThreadPool` agar menyimpan sender dari channel yang mengirimkan instance `Job`">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-16/src/lib.rs:here}}
```

</Listing>

Di `ThreadPool::new`, kita membuat channel baru dan membiarkan pool menyimpan sender-nya. Ini akan berhasil terkompilasi.

Mari kita coba meneruskan receiver channel ke setiap `Worker` saat thread pool membuat channel. Kita tahu kita ingin memakai receiver di thread yang dibuat oleh instance `Worker`, jadi kita akan mereferensikan parameter `receiver` di dalam closure. Kode pada Listing 21-17 belum sepenuhnya terkompilasi.

<Listing number="21-17" file-name="src/lib.rs" caption="Meneruskan receiver ke setiap `Worker`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-17/src/lib.rs:here}}
```

</Listing>

Kita telah membuat beberapa perubahan kecil dan langsung: kita meneruskan receiver ke `Worker::new`, lalu memakainya di dalam closure.

Saat kita mencoba mengecek kode ini, kita mendapat error ini:

```console
{{#include ../listings/ch21-web-server/listing-21-17/output.txt}}
```

Kode ini berusaha meneruskan `receiver` ke banyak instance `Worker`. Ini tidak akan berhasil, seperti yang kamu ingat dari Bab 16: implementasi channel yang disediakan Rust adalah _producer_ ganda, _consumer_ tunggal. Ini berarti kita tidak bisa sekadar meng-clone ujung konsumsi dari channel untuk memperbaiki kode ini. Kita juga tidak ingin mengirim sebuah pesan berkali-kali ke banyak consumer; kita ingin satu daftar pesan dengan banyak instance `Worker` sehingga setiap pesan diproses satu kali.

Selain itu, mengambil pekerjaan dari antrean channel melibatkan perubahan pada `receiver`, sehingga thread-thread itu butuh cara aman untuk berbagi dan mengubah `receiver`; jika tidak, kita bisa mengalami race condition (seperti dibahas di Bab 16).

Ingat smart pointer yang aman untuk thread yang dibahas di Bab 16: Untuk berbagi ownership ke beberapa thread dan mengizinkan thread-thread itu mengubah nilainya, kita perlu memakai `Arc<Mutex<T>>`. Tipe `Arc` akan memungkinkan banyak instance `Worker` memiliki receiver, dan `Mutex` akan memastikan hanya satu `Worker` yang mendapat pekerjaan dari receiver pada satu waktu. Listing 21-18 menunjukkan perubahan yang perlu kita buat.

<Listing number="21-18" file-name="src/lib.rs" caption="Berbagi receiver antar-instance `Worker` memakai `Arc` dan `Mutex`">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-18/src/lib.rs:here}}
```

</Listing>

Di `ThreadPool::new`, kita menaruh receiver di dalam `Arc` dan `Mutex`. Untuk setiap `Worker` baru, kita meng-clone `Arc` untuk menaikkan jumlah reference agar instance `Worker` bisa berbagi ownership atas receiver.

Dengan perubahan ini, kode terkompilasi! Kita makin dekat!

#### Mengimplementasikan Metode `execute`

Akhirnya, mari kita implementasikan metode `execute` pada `ThreadPool`. Kita juga akan mengubah `Job` dari struct menjadi alias tipe untuk trait object yang menyimpan tipe closure yang diterima `execute`. Seperti dibahas di bagian [“Sinonim Tipe dan Alias Tipe”][type-aliases]<!-- ignore --> Bab 20, alias tipe memungkinkan kita membuat tipe yang panjang menjadi lebih pendek agar lebih mudah dipakai. Lihat Listing 21-19.

<Listing number="21-19" file-name="src/lib.rs" caption="Membuat alias tipe `Job` untuk `Box` yang menyimpan setiap closure, lalu mengirim pekerjaan melalui channel">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-19/src/lib.rs:here}}
```

</Listing>

Setelah membuat instance `Job` baru dengan closure yang kita dapatkan di `execute`, kita mengirim pekerjaan itu melalui ujung pengirim channel. Kita memanggil `unwrap` pada `send` untuk mengantisipasi kasus pengiriman gagal. Ini bisa terjadi, misalnya, jika kita menghentikan semua thread kita dari eksekusi, yang berarti ujung penerima sudah berhenti menerima pesan baru. Saat ini, kita tidak bisa menghentikan thread-thread kita dari eksekusi: thread kita terus berjalan selama pool ada. Alasan kita memakai `unwrap` adalah kita tahu kasus gagal itu tidak akan terjadi, tetapi compiler tidak tahu itu.

Tapi kita belum sepenuhnya selesai! Di `Worker`, closure yang kita teruskan ke `thread::spawn` masih hanya _mereferensikan_ ujung penerima channel. Sebaliknya, kita perlu closure itu melakukan loop selamanya, meminta pekerjaan dari ujung penerima channel dan menjalankannya saat mendapat satu. Mari kita buat perubahan seperti ditunjukkan pada Listing 21-20 pada `Worker::new`.

<Listing number="21-20" file-name="src/lib.rs" caption="Menerima dan mengeksekusi pekerjaan di thread milik instance `Worker`">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-20/src/lib.rs:here}}
```

</Listing>

Di sini, kita pertama memanggil `lock` pada `receiver` untuk mendapatkan mutex, lalu memanggil `unwrap` agar panic jika ada error. Mendapatkan lock bisa gagal jika mutex berada dalam keadaan _poisoned_, yang bisa terjadi jika thread lain panic saat memegang lock, alih-alih melepaskannya. Dalam situasi ini, memanggil `unwrap` agar thread ini panic adalah tindakan yang tepat. Silakan ubah `unwrap` ini menjadi `expect` dengan pesan error yang bermakna bagimu.

Jika kita berhasil mendapat lock pada mutex, kita memanggil `recv` untuk menerima `Job` dari channel. Sebuah `unwrap` terakhir juga mengabaikan error di sini, yang bisa terjadi jika thread yang memegang sender sudah mati, mirip dengan cara metode `send` mengembalikan `Err` jika receiver mati.

Panggilan ke `recv` memblokir, jadi jika belum ada pekerjaan, thread saat ini akan menunggu sampai ada pekerjaan tersedia. `Mutex<T>` memastikan bahwa hanya satu thread `Worker` pada satu waktu yang mencoba meminta pekerjaan.

Thread pool kita sekarang sudah berfungsi! Coba `cargo run` dan kirim beberapa request:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-20
cargo run
make some requests to 127.0.0.1:7878
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
warning: field `workers` is never read
 --> src/lib.rs:7:5
  |
6 | pub struct ThreadPool {
  |            ---------- field in this struct
7 |     workers: Vec<Worker>,
  |     ^^^^^^^
  |
  = note: `#[warn(dead_code)]` on by default

warning: fields `id` and `thread` are never read
  --> src/lib.rs:48:5
   |
47 | struct Worker {
   |        ------ fields in this struct
48 |     id: usize,
   |     ^^
49 |     thread: thread::JoinHandle<()>,
   |     ^^^^^^

warning: `hello` (lib) generated 2 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 4.91s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
```

Berhasil! Sekarang kita punya thread pool yang mengeksekusi koneksi secara asynchronous. Jumlah thread yang dibuat tidak pernah lebih dari empat, sehingga sistem kita tidak akan kewalahan jika server menerima banyak request. Jika kita mengirim request ke _/sleep_, server akan tetap bisa melayani request lain dengan menjalankannya di thread lain.

> Catatan: Jika kamu membuka _/sleep_ di beberapa jendela browser secara bersamaan, halaman itu mungkin memuat satu per satu dengan interval lima detik. Beberapa browser web menjalankan beberapa instance dari request yang sama secara berurutan demi alasan caching. Keterbatasan ini bukan disebabkan oleh server web kita.

Ini adalah waktu yang tepat untuk berhenti sejenak dan memikirkan seperti apa kode di Listing 21-18, 21-19, dan 21-20 jika kita memakai future alih-alih closure untuk pekerjaan yang dilakukan. Tipe apa yang akan berubah? Bagaimana signature metode akan berbeda, jika ada? Bagian kode mana yang tetap sama?

Setelah mempelajari loop `while let` di Bab 17 dan Bab 19, kamu mungkin bertanya-tanya mengapa kita tidak menulis kode thread `Worker` seperti ditunjukkan pada Listing 21-21.

<Listing number="21-21" file-name="src/lib.rs" caption="Implementasi alternatif `Worker::new` memakai `while let`">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-21/src/lib.rs:here}}
```

</Listing>

Kode ini terkompilasi dan berjalan, tetapi tidak menghasilkan perilaku thread yang diinginkan: request yang lambat tetap akan membuat request lain menunggu untuk diproses. Alasannya agak halus: struct `Mutex` tidak punya metode `unlock` publik karena ownership atas lock didasarkan pada lifetime dari `MutexGuard<T>` di dalam `LockResult<MutexGuard<T>>` yang dikembalikan metode `lock`. Saat kompilasi, borrow checker lalu bisa menegakkan aturan bahwa sumber daya yang dijaga oleh `Mutex` tidak bisa diakses kecuali kita memegang locknya. Namun, implementasi ini juga bisa membuat lock dipegang lebih lama dari yang dimaksudkan jika kita tidak memperhatikan lifetime dari `MutexGuard<T>`.

Kode pada Listing 21-20 yang memakai `let job = receiver.lock().unwrap().recv().unwrap();` berhasil karena dengan `let`, semua nilai sementara yang dipakai dalam ekspresi di sisi kanan tanda sama dengan langsung dihapus saat statement `let` berakhir. Namun, `while let` (dan `if let` serta `match`) tidak menghapus nilai sementara sampai akhir blok terkait. Di Listing 21-21, lock tetap dipegang selama panggilan `job()` berlangsung, yang berarti instance `Worker` lain tidak bisa menerima pekerjaan.

[type-aliases]: ch20-03-advanced-types.html#type-synonyms-and-type-aliases
[integer-types]: ch03-02-data-types.html#integer-types
[moving-out-of-closures]: ch13-01-closures.html#moving-captured-values-out-of-closures
[builder]: ../std/thread/struct.Builder.html
[builder-spawn]: ../std/thread/struct.Builder.html#method.spawn
