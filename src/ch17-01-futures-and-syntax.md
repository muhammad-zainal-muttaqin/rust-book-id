## Future dan Sintaks Async

Elemen kunci dari pemrograman asinkron di Rust adalah _future_ dan kata kunci `async` serta `await` dalam Rust.

Sebuah _future_ adalah nilai yang mungkin belum siap sekarang, tetapi akan siap pada suatu titik di kemudian hari. (Konsep yang sama muncul di banyak bahasa, kadang dengan nama lain seperti _task_ atau _promise_.) Rust menyediakan trait `Future` sebagai balok penyusun agar berbagai operasi async bisa diimplementasikan dengan struktur data yang berbeda, tetapi melalui antarmuka yang sama. Di Rust, future adalah tipe yang mengimplementasikan trait `Future`. Setiap future menyimpan informasinya sendiri tentang sejauh mana progresnya dan apa arti "siap".

Kamu bisa menerapkan kata kunci `async` pada blok dan fungsi untuk menandakan bahwa keduanya bisa dijeda dan dilanjutkan kembali. Di dalam blok async atau fungsi async, kamu bisa memakai kata kunci `await` untuk _menunggu sebuah future_ (artinya, menunggu sampai future itu siap). Setiap titik tempat kamu menunggu sebuah future di dalam blok atau fungsi async adalah titik potensial tempat blok atau fungsi itu berhenti dan dilanjutkan lagi. Proses memeriksa sebuah future untuk melihat apakah nilainya sudah tersedia disebut _polling_.

Beberapa bahasa lain, seperti C# dan JavaScript, juga memakai kata kunci `async` dan `await` untuk pemrograman async. Kalau kamu sudah akrab dengan bahasa-bahasa itu, kamu mungkin akan melihat beberapa perbedaan besar dalam cara Rust menangani sintaksnya. Ada alasan bagus untuk itu, seperti akan kita lihat nanti!

Saat menulis async Rust, kita memakai kata kunci `async` dan `await` hampir sepanjang waktu. Rust mengompilasi keduanya menjadi kode yang setara dengan memakai trait `Future`, sama seperti ia mengompilasi loop `for` menjadi kode yang setara dengan memakai trait `Iterator`. Namun, karena Rust menyediakan trait `Future`, kamu juga bisa mengimplementasikannya untuk tipe data milikmu sendiri saat perlu. Banyak fungsi yang akan kita lihat sepanjang bab ini mengembalikan tipe dengan implementasi `Future` mereka sendiri. Kita akan kembali ke definisi trait itu di akhir bab dan mendalami cara kerjanya lebih lanjut, tapi untuk sekarang ini sudah cukup untuk kita lanjutkan.

Semua ini mungkin terasa agak abstrak, jadi mari kita tulis program async pertama kita: sebuah web scraper kecil. Kita akan memasukkan dua URL dari command line, mengambil keduanya secara konkuren, dan mengembalikan hasil dari yang selesai lebih dulu. Contoh ini punya cukup banyak sintaks baru, tapi jangan khawatir—kita akan menjelaskan semua yang perlu kamu tahu seiring berjalannya.

<a id="our-first-async-program"></a>
## Program Async Pertama Kita

Agar fokus bab ini tetap pada belajar async, bukan pada repot mengatur berbagai bagian ekosistem, kami membuat crate `trpl` (`trpl` adalah singkatan dari "The Rust Programming Language"). Crate ini mengekspor ulang semua tipe, trait, dan fungsi yang kamu butuhkan, terutama dari crate [`futures`][futures-crate]<!-- ignore --> dan [`tokio`][tokio]<!-- ignore -->. Crate `futures` adalah rumah resmi eksperimen Rust untuk kode async, dan di situlah trait `Future` awalnya dirancang. Tokio adalah async runtime yang paling banyak dipakai di Rust saat ini, terutama untuk aplikasi web. Ada runtime bagus lainnya di luar sana, dan mungkin ada yang lebih cocok untuk kebutuhanmu. Kita memakai crate `tokio` di balik layar untuk `trpl` karena sudah teruji dan luas dipakai.

Dalam beberapa kasus, `trpl` juga mengganti nama atau membungkus API aslinya agar kamu tetap fokus pada detail yang relevan dengan bab ini. Kalau kamu ingin memahami apa yang dilakukan crate ini, kami menyarankanmu melihat [kode sumbernya][crate-source]. Kamu bisa melihat crate mana asal setiap ekspor ulang, dan kami menyisakan banyak komentar yang menjelaskan apa yang dilakukan crate itu.

Buat proyek biner baru bernama `hello-async` dan tambahkan crate `trpl` sebagai dependensi:

```console
$ cargo new hello-async
$ cd hello-async
$ cargo add trpl
```

Sekarang kita bisa memakai berbagai bagian yang disediakan `trpl` untuk menulis program async pertama kita. Kita akan membuat alat command line kecil yang mengambil dua halaman web, mengambil elemen `<title>` dari masing-masing, lalu mencetak judul halaman yang paling cepat menyelesaikan seluruh proses itu.

### Mendefinisikan Fungsi page_title

Mari mulai dengan menulis fungsi yang menerima satu URL halaman sebagai parameter, mengirim permintaan ke sana, dan mengembalikan teks elemen `<title>` (lihat Listing 17-1).

<Listing number="17-1" file-name="src/main.rs" caption="Mendefinisikan fungsi async untuk mendapatkan elemen title dari sebuah halaman HTML">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-01/src/main.rs:all}}
```

</Listing>

Pertama, kita mendefinisikan fungsi bernama `page_title` dan menandainya dengan kata kunci `async`. Lalu kita memakai fungsi `trpl::get` untuk mengambil URL apa pun yang diberikan dan menambahkan kata kunci `await` untuk menunggu responsnya. Untuk mendapatkan teks dari `response`, kita memanggil metode `text`-nya dan sekali lagi menunggunya dengan kata kunci `await`. Kedua langkah ini bersifat asinkron. Untuk fungsi `get`, kita harus menunggu server mengirim bagian awal responsnya, yang berisi header HTTP, cookie, dan sebagainya, dan bisa dikirim terpisah dari isi respons. Apalagi kalau isinya sangat besar, bisa butuh waktu sampai semuanya tiba. Karena kita harus menunggu _seluruh_ respons tiba, metode `text` juga bersifat async.

Kita harus secara eksplisit menunggu kedua future ini, karena future di Rust bersifat _lazy_: mereka tidak melakukan apa pun sampai kamu memintanya dengan kata kunci `await`. (Sebenarnya, Rust akan menampilkan peringatan compiler kalau kamu tidak memakai sebuah future.) Ini mungkin mengingatkanmu pada pembahasan iterator di bagian [“Memproses Deretan Item dengan Iterator”][iterators-lazy]<!-- ignore --> Bab 13. Iterator tidak melakukan apa pun kecuali kamu memanggil metode `next`-nya—baik langsung maupun dengan memakai loop `for` atau metode seperti `map` yang memakai `next` di balik layar. Begitu pula, future tidak melakukan apa pun kecuali kamu secara eksplisit memintanya. Sifat malas ini membuat Rust bisa menghindari menjalankan kode async sampai kode itu benar-benar dibutuhkan.

> Catatan: Ini berbeda dengan perilaku yang kita lihat saat memakai `thread::spawn` di bagian [“Membuat Thread Baru dengan spawn”][thread-spawn]<!-- ignore --> Bab 16, di mana closure yang kita berikan ke thread lain langsung mulai berjalan. Ini juga berbeda dengan cara banyak bahasa lain menangani async. Tapi bagi Rust, hal ini penting agar bisa menjaga jaminan performanya, sama seperti halnya dengan iterator.

Setelah punya `response_text`, kita bisa menguraikannya menjadi instance dari tipe `Html` dengan `Html::parse`. Alih-alih string mentah, sekarang kita punya tipe data yang bisa dipakai untuk bekerja dengan HTML sebagai struktur data yang lebih kaya. Khususnya, kita bisa memakai metode `select_first` untuk mencari kemunculan pertama dari sebuah selector CSS. Dengan memberikan string `"title"`, kita akan mendapat elemen `<title>` pertama dalam dokumen, kalau ada. Karena mungkin saja tidak ada elemen yang cocok, `select_first` mengembalikan `Option<ElementRef>`. Terakhir, kita memakai metode `Option::map`, yang memungkinkan kita bekerja dengan isi `Option` kalau ada, dan tidak melakukan apa-apa kalau tidak ada. (Kita juga bisa memakai ekspresi `match` di sini, tapi `map` lebih idiomatik.) Di badan fungsi yang kita berikan ke `map`, kita memanggil `inner_html` pada `title` untuk mendapat isinya, yaitu sebuah `String`. Pada akhirnya, kita punya `Option<String>`.

Perhatikan bahwa kata kunci `await` dalam Rust diletakkan _setelah_ ekspresi yang kamu tunggu, bukan sebelumnya. Artinya, kata kunci ini bersifat _postfix_. Ini mungkin berbeda dari kebiasaanmu kalau kamu pernah memakai `async` di bahasa lain, tapi di Rust ini membuat rangkaian metode jauh lebih enak dipakai. Hasilnya, kita bisa mengubah badan `page_title` untuk merangkai pemanggilan fungsi `trpl::get` dan `text` dengan `await` di antaranya, seperti ditunjukkan pada Listing 17-2.

<Listing number="17-2" file-name="src/main.rs" caption="Merangkai dengan kata kunci `await`">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-02/src/main.rs:chaining}}
```

</Listing>

Dengan begitu, kita berhasil menulis fungsi async pertama kita! Sebelum kita menambahkan kode di `main` untuk memanggilnya, mari kita bicara sedikit lagi tentang apa yang sudah kita tulis dan apa artinya.

Saat Rust melihat sebuah _blok_ yang ditandai dengan kata kunci `async`, ia mengompilasinya menjadi tipe data anonim yang unik dan mengimplementasikan trait `Future`. Saat Rust melihat sebuah _fungsi_ yang ditandai `async`, ia mengompilasinya menjadi fungsi non-async yang badannya adalah sebuah blok async. Tipe kembalian fungsi async adalah tipe data anonim yang dibuat compiler untuk blok async itu.

Jadi, menulis `async fn` setara dengan menulis fungsi yang mengembalikan sebuah _future_ dari tipe kembaliannya. Bagi compiler, definisi fungsi seperti `async fn page_title` pada Listing 17-1 kira-kira setara dengan fungsi non-async yang didefinisikan seperti ini:

```rust
# extern crate trpl; // required for mdbook test
use std::future::Future;
use trpl::Html;

fn page_title(url: &str) -> impl Future<Output = Option<String>> {
    async move {
        let text = trpl::get(url).await.text().await;
        Html::parse(&text)
            .select_first("title")
            .map(|title| title.inner_html())
    }
}
```

Mari kita telusuri setiap bagian dari versi yang sudah diubah ini:

- Ini memakai sintaks `impl Trait` yang kita bahas di Bab 10, di bagian [“Trait sebagai Parameter”][impl-trait]<!-- ignore -->.
- Nilai yang dikembalikan mengimplementasikan trait `Future` dengan tipe asosiasi `Output`. Perhatikan bahwa tipe `Output` adalah `Option<String>`, sama dengan tipe kembalian asli dari versi `async fn` dari `page_title`.
- Semua kode yang dipanggil di badan fungsi asli dibungkus dalam blok `async move`. Ingat bahwa blok adalah ekspresi. Seluruh blok ini adalah ekspresi yang dikembalikan fungsi.
- Blok async ini menghasilkan nilai bertipe `Option<String>`, seperti yang baru saja dijelaskan. Nilai itu cocok dengan tipe `Output` pada tipe kembalian. Sama seperti blok lain yang pernah kamu lihat.
- Badan fungsi yang baru adalah blok `async move` karena cara ia memakai parameter `url`. (Kita akan membahas `async` versus `async move` lebih jauh nanti di bab ini.)

Sekarang kita bisa memanggil `page_title` di `main`.

<!-- Old headings. Do not remove or links may break. -->

<a id ="determining-a-single-pages-title"></a>

### Menjalankan Fungsi Async dengan Runtime

Untuk mulai, kita akan mengambil judul dari satu halaman saja, seperti ditunjukkan pada Listing 17-3. Sayangnya, kode ini belum bisa dikompilasi.

<Listing number="17-3" file-name="src/main.rs" caption="Memanggil fungsi `page_title` dari `main` dengan argumen yang diberikan pengguna">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-03/src/main.rs:main}}
```

</Listing>

Kita mengikuti pola yang sama seperti saat mengambil argumen command line di bagian [“Menerima Argumen Command Line”][cli-args]<!-- ignore --> Bab 12. Lalu kita memberikan argumen URL ke `page_title` dan menunggu hasilnya. Karena nilai yang dihasilkan future adalah `Option<String>`, kita memakai ekspresi `match` untuk mencetak pesan yang berbeda, tergantung apakah halaman itu punya `<title>` atau tidak.

Satu-satunya tempat kita bisa memakai kata kunci `await` adalah di dalam fungsi atau blok async, dan Rust tidak membiarkan kita menandai fungsi istimewa `main` sebagai `async`.

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-03
cargo build
copy just the compiler error
-->

```text
error[E0752]: `main` function is not allowed to be `async`
 --> src/main.rs:6:1
  |
6 | async fn main() {
  | ^^^^^^^^^^^^^^^ `main` function is not allowed to be `async`
```

Alasan `main` tidak bisa ditandai `async` adalah karena kode async membutuhkan sebuah _runtime_: crate Rust yang mengatur detail pelaksanaan kode asinkron. Fungsi `main` sebuah program bisa _menginisialisasi_ runtime, tapi fungsi itu bukan runtime _itu sendiri_. (Nanti kita akan melihat lebih jauh mengapa demikian.) Setiap program Rust yang menjalankan kode async punya setidaknya satu tempat yang menyiapkan runtime untuk menjalankan future-future itu.

Kebanyakan bahasa yang mendukung async menyertakan runtime, tapi Rust tidak. Sebagai gantinya, ada banyak async runtime yang tersedia, masing-masing dengan pertimbangan berbeda yang sesuai untuk kasus penggunaannya. Misalnya, server web dengan throughput tinggi, banyak core CPU, dan RAM besar punya kebutuhan yang sangat berbeda dari mikrokontroler dengan satu core, RAM kecil, dan tanpa kemampuan alokasi heap. Crate yang menyediakan runtime itu juga sering kali menyediakan versi async dari fungsi umum seperti I/O file atau jaringan.

Di sini, dan sepanjang sisa bab ini, kita akan memakai fungsi `block_on` dari crate `trpl`, yang menerima sebuah future sebagai argumen dan memblokir thread saat ini sampai future itu selesai dijalankan. Di balik layar, memanggil `block_on` menyiapkan runtime dengan memakai crate `tokio` yang dipakai untuk menjalankan future yang diberikan (perilaku `block_on` crate `trpl` mirip dengan fungsi `block_on` di crate runtime lain). Setelah future selesai, `block_on` mengembalikan nilai apa pun yang dihasilkan future itu.

Kita bisa saja memberikan future yang dikembalikan `page_title` langsung ke `block_on` dan, setelah selesai, melakukan `match` pada `Option<String>` yang dihasilkan seperti yang kita coba lakukan di Listing 17-3. Namun, untuk sebagian besar contoh di bab ini (dan sebagian besar kode async di dunia nyata), kita akan melakukan lebih dari satu pemanggilan fungsi async. Karena itu, kita akan memberikan sebuah blok `async` dan secara eksplisit menunggu hasil pemanggilan `page_title`, seperti di Listing 17-4.

<Listing number="17-4" caption="Menunggu sebuah blok async dengan `trpl::block_on`" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook test does not pass args -->

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-04/src/main.rs:run}}
```

</Listing>

Saat kita menjalankan kode ini, kita mendapat perilaku yang semula kita harapkan:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-04
cargo build # skip all the build noise
cargo run -- "https://www.rust-lang.org"
# copy the output here
-->

```console
$ cargo run -- "https://www.rust-lang.org"
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.05s
     Running `target/debug/async_await 'https://www.rust-lang.org'`
The title for https://www.rust-lang.org was
            Rust Programming Language
```

Huuuh—akhirnya kita punya kode async yang berfungsi! Tapi sebelum kita menambahkan kode untuk mengadu dua situs, mari kita alihkan perhatian sebentar kembali ke cara kerja future.

Setiap _titik await_—artinya, setiap tempat kode memakai kata kunci `await`—adalah titik tempat kendali diserahkan kembali ke runtime. Agar ini bisa terjadi, Rust perlu melacak keadaan yang terlibat dalam blok async agar runtime bisa memulai pekerjaan lain, lalu kembali saat sudah siap mencoba melanjutkan pekerjaan yang pertama. Ini adalah mesin keadaan yang tak terlihat, seolah-olah kamu menulis enum seperti ini untuk menyimpan keadaan saat ini di setiap titik await:

```rust
{{#rustdoc_include ../listings/ch17-async-await/no-listing-state-machine/src/lib.rs:enum}}
```

Menulis kode untuk berpindah dari satu keadaan ke keadaan lain secara manual akan melelahkan dan rawan error, apalagi kalau nanti kamu perlu menambahkan lebih banyak fungsi dan keadaan ke kode itu. Untungnya, compiler Rust membuat dan mengelola struktur data mesin keadaan untuk kode async secara otomatis. Aturan borrowing dan ownership biasa pada struktur data tetap berlaku, dan untungnya compiler juga menangani pemeriksaannya untuk kita serta memberikan pesan error yang berguna. Kita akan membahas beberapa di antaranya nanti di bab ini.

Pada akhirnya, sesuatu harus menjalankan mesin keadaan ini, dan sesuatu itu adalah runtime. (Ini sebabnya kamu mungkin menemukan penyebutan _executor_ saat mempelajari runtime: executor adalah bagian dari runtime yang bertugas menjalankan kode async.)

Sekarang kamu bisa melihat mengapa compiler menghentikan kita saat ingin membuat `main` sendiri menjadi fungsi async di Listing 17-3. Kalau `main` adalah fungsi async, sesuatu yang lain perlu mengelola mesin keadaan untuk future apa pun yang dikembalikan `main`, tapi `main` adalah titik awal program! Sebagai gantinya, kita memanggil fungsi `trpl::block_on` di `main` untuk menyiapkan runtime dan menjalankan future yang dikembalikan blok `async` sampai selesai.

> Catatan: Beberapa runtime menyediakan macro agar kamu _bisa_ menulis fungsi `main` yang async. Macro itu menulis ulang `async fn main() { ... }` menjadi `fn main` biasa, yang melakukan hal yang sama dengan apa yang kita lakukan secara manual di Listing 17-4: memanggil fungsi yang menjalankan future sampai selesai, seperti yang dilakukan `trpl::block_on`.

Sekarang mari kita gabungkan bagian-bagian ini dan lihat bagaimana kita bisa menulis kode konkuren.

<!-- Old headings. Do not remove or links may break. -->

<a id="racing-our-two-urls-against-each-other"></a>

### Mengadu Dua URL Secara Konkuren

Di Listing 17-5, kita memanggil `page_title` dengan dua URL berbeda yang diberikan dari command line dan mengadukannya dengan memilih future mana yang selesai lebih dulu.

<Listing number="17-5" caption="Memanggil `page_title` untuk dua URL untuk melihat mana yang kembali lebih dulu" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook does not pass args -->

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-05/src/main.rs:all}}
```

</Listing>

Kita mulai dengan memanggil `page_title` untuk masing-masing URL yang diberikan pengguna. Kita menyimpan future yang dihasilkan sebagai `title_fut_1` dan `title_fut_2`. Ingat, keduanya belum melakukan apa pun, karena future bersifat malas dan kita belum menunggunya. Lalu kita memberikan future-future itu ke `trpl::select`, yang mengembalikan nilai untuk menunjukkan future mana di antaranya yang selesai lebih dulu.

> Catatan: Di balik layar, `trpl::select` dibangun di atas fungsi `select` yang lebih umum dan didefinisikan di crate `futures`. Fungsi `select` dari crate `futures` bisa melakukan banyak hal yang tidak bisa dilakukan `trpl::select`, tapi fungsi itu juga punya kompleksitas tambahan yang untuk sekarang bisa kita lewati.

Future mana pun bisa secara sah "menang", jadi tidak masuk akal untuk mengembalikan `Result`. Sebagai gantinya, `trpl::select` mengembalikan tipe yang belum pernah kita lihat, yaitu `trpl::Either`. Tipe `Either` agak mirip `Result` karena punya dua kasus. Namun, berbeda dengan `Result`, tidak ada konsep sukses atau gagal yang melekat pada `Either`. Sebagai gantinya, tipe ini memakai `Left` dan `Right` untuk menunjukkan "salah satu dari keduanya":

```rust
enum Either<A, B> {
    Left(A),
    Right(B),
}
```

Fungsi `select` mengembalikan `Left` beserta hasil future itu kalau argumen pertama yang menang, dan `Right` beserta hasil argumen future kedua kalau _argumen itu_ yang menang. Ini sesuai dengan urutan argumen saat fungsi dipanggil: argumen pertama berada di sebelah kiri argumen kedua.

Kita juga memperbarui `page_title` agar mengembalikan URL yang sama seperti yang diberikan. Dengan begitu, kalau halaman yang kembali lebih dulu tidak punya `<title>` yang bisa kita ambil, kita tetap bisa mencetak pesan yang bermakna. Dengan informasi itu tersedia, kita menutup dengan memperbarui keluaran `println!` agar menunjukkan URL mana yang selesai lebih dulu dan apa `<title>` halaman web di URL itu, kalau ada.

Sekarang kamu sudah membuat web scraper kecil yang berfungsi! Pilih beberapa URL dan jalankan alat command line itu. Kamu mungkin akan menemukan bahwa beberapa situs konsisten lebih cepat dari yang lain, sementara dalam kasus lain situs yang lebih cepat berubah-ubah dari satu kali menjalankan ke berikutnya. Yang lebih penting, kamu sudah mempelajari dasar-dasar bekerja dengan future, jadi sekarang kita bisa mendalami apa yang bisa kita lakukan dengan async.

[impl-trait]: ch10-02-traits.html#traits-as-parameters
[iterators-lazy]: ch13-02-iterators.html
[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[cli-args]: ch12-01-accepting-command-line-arguments.html

<!-- TODO: map source link version to version of Rust? -->

[crate-source]: https://github.com/rust-lang/book/tree/main/packages/trpl
[futures-crate]: https://crates.io/crates/futures
[tokio]: https://tokio.rs
