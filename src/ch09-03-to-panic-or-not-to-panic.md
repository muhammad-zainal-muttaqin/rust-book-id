<a id="to-panic-or-not-to-panic"></a>
## `panic!` atau Tidak `panic!`

Jadi, bagaimana kamu memutuskan kapan harus memanggil `panic!` dan kapan harus mengembalikan `Result`? Saat kode melakukan panic, tak ada jalan untuk pulih. Kamu bisa saja memanggil `panic!` untuk situasi error apa pun, baik ada kemungkinan pulih atau tidak, tetapi dengan begitu kamu mengambil keputusan atas nama kode yang memanggil bahwa suatu situasi tidak bisa dipulihkan. Saat kamu memilih untuk mengembalikan nilai `Result`, kamu memberi kode pemanggil sejumlah pilihan. Kode itu bisa mencoba pulih dengan cara yang sesuai untuk situasinya, atau memutuskan bahwa nilai `Err` dalam kasus ini tidak bisa dipulihkan, lalu memanggil `panic!` untuk mengubah error yang bisa dipulihkan menjadi tidak bisa dipulihkan. Karena itu, mengembalikan `Result` adalah pilihan awal yang baik saat kamu mendefinisikan fungsi yang mungkin gagal.

Dalam situasi seperti contoh, kode prototipe, dan test, lebih tepat menulis kode yang melakukan panic daripada mengembalikan `Result`. Mari kita lihat alasannya, lalu bahas situasi di mana compiler tidak bisa mengetahui bahwa kegagalan mustahil terjadi, tetapi kamu sebagai manusia bisa. Bab ini akan ditutup dengan beberapa pedoman umum tentang cara memutuskan apakah akan melakukan panic di kode library.

### Contoh, Kode Prototipe, dan Test

Saat kamu menulis contoh untuk mengilustrasikan suatu konsep, menyertakan kode penanganan error yang tangguh justru bisa membuat contoh itu kurang jelas. Dalam contoh, sudah dipahami bahwa pemanggilan metode seperti `unwrap` yang bisa melakukan panic dimaksudkan sebagai placeholder untuk cara yang ingin kamu pakai agar aplikasi menangani error—cara yang bisa berbeda tergantung pada apa yang dilakukan kode kamu lainnya.

Demikian pula, metode `unwrap` dan `expect` sangat berguna saat kamu membuat prototipe dan belum siap memutuskan cara menangani error. Keduanya meninggalkan penanda yang jelas di kode kamu untuk nanti, saat kamu siap membuat program menjadi lebih tangguh.

Jika sebuah pemanggilan metode gagal dalam sebuah test, kamu ingin seluruh test itu gagal, meski metode tersebut bukan fungsionalitas yang sedang diuji. Karena `panic!` adalah cara sebuah test ditandai sebagai gagal, memanggil `unwrap` atau `expect` justru merupakan hal yang tepat.

<!-- Old headings. Do not remove or links may break. -->

<a id="cases-in-which-you-have-more-information-than-the-compiler"></a>

### Saat Kamu Punya Informasi Lebih Banyak daripada Compiler

Memanggil `expect` juga tepat saat kamu punya logika lain yang memastikan `Result` akan berisi nilai `Ok`, tetapi logika itu bukan sesuatu yang dipahami compiler. Kamu tetap akan memiliki nilai `Result` yang perlu ditangani: Operasi apa pun yang kamu panggil masih mungkin gagal secara umum, meski secara logika mustahil dalam situasi khusus kamu. Jika kamu bisa memastikan dengan memeriksa kode secara manual bahwa kamu tidak akan pernah mendapat varian `Err`, maka sangat boleh memanggil `expect` dan mendokumentasikan alasan kamu yakin tidak akan pernah ada varian `Err` di teks argumennya. Ini contohnya:

```rust
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-08-unwrap-that-cant-fail/src/main.rs:here}}
```

Kita membuat instance `IpAddr` dengan mengurai string yang ditanam langsung di kode. Kita bisa melihat bahwa `127.0.0.1` adalah alamat IP yang valid, jadi boleh saja memakai `expect` di sini. Namun, string yang valid dan ditanam langsung itu tidak mengubah tipe kembalian metode `parse`: Kita tetap mendapat nilai `Result`, dan compiler tetap akan menyuruh kita menangani `Result` itu seolah varian `Err` mungkin terjadi, karena compiler tidak cukup pintar untuk melihat bahwa string ini selalu merupakan alamat IP yang valid. Seandainya string alamat IP itu berasal dari pengguna, bukan ditanam di program, dan dengan demikian _memang_ punya kemungkinan gagal, kita tentu ingin menangani `Result` dengan cara yang lebih tangguh. Menyebut asumsi bahwa alamat IP ini ditanam langsung akan mengingatkan kita untuk mengganti `expect` dengan kode penanganan error yang lebih baik jika kelak kita perlu mengambil alamat IP dari sumber lain.

<a id="guidelines-for-error-handling"></a>
### Pedoman Penanganan Error

Sebaiknya biarkan kode kamu melakukan panic ketika ada kemungkinan kode itu berakhir dalam keadaan buruk. Dalam konteks ini, _keadaan buruk_ terjadi ketika suatu asumsi, jaminan, kontrak, atau invarian dilanggar—misalnya ketika nilai yang tidak valid, nilai yang bertentangan, atau nilai yang hilang diberikan ke kode kamu—serta satu atau lebih dari kondisi berikut:

- Keadaan buruk itu sesuatu yang tidak terduga, bukan sesuatu yang kemungkinan besar akan terjadi sesekali, seperti pengguna memasukkan data dengan format yang salah.
- Kode kamu setelah titik ini perlu mengandalkan asumsi bahwa keadaan buruk itu tidak terjadi, daripada memeriksa masalah itu di setiap langkah.
- Tidak ada cara yang baik untuk menyandikan informasi ini ke dalam tipe yang kamu pakai. Kita akan membahas contohnya dalam [“Menyandikan Keadaan dan Perilaku sebagai Tipe”][encoding]<!-- ignore --> di Bab 18.

Jika seseorang memanggil kode kamu dan memberikan nilai yang tidak masuk akal, sebaiknya kembalikan error jika memungkinkan agar pengguna library bisa memutuskan apa yang ingin mereka lakukan dalam kasus itu. Namun, dalam situasi di mana melanjutkan bisa saja tidak aman atau merugikan, pilihan terbaik mungkin memanggil `panic!` dan memberi tahu pengguna library bahwa ada bug di kode mereka, supaya mereka bisa memperbaikinya saat pengembangan. Begitu pula, `panic!` sering tepat dipakai jika kamu memanggil kode eksternal yang tidak bisa kamu kendalikan dan mengembalikan keadaan yang tidak valid yang tidak ada cara bagimu untuk memperbaikinya.

Namun, ketika kegagalan memang diperkirakan terjadi, lebih tepat mengembalikan `Result` daripada memanggil `panic!`. Contohnya adalah parser yang diberi data yang rusak atau permintaan HTTP yang mengembalikan status yang menandakan kamu telah mencapai batas jumlah permintaan. Dalam kasus ini, mengembalikan `Result` menunjukkan bahwa kegagalan adalah kemungkinan yang memang diharapkan dan kode pemanggil harus memutuskan cara menanganinya.

Ketika kode kamu melakukan operasi yang bisa membahayakan pengguna jika dipanggil dengan nilai yang tidak valid, kode kamu harus memverifikasi dulu bahwa nilainya valid dan melakukan panic jika tidak valid. Ini terutama demi alasan keamanan: Mencoba memproses data yang tidak valid bisa membuat kode kamu rentan. Ini adalah alasan utama standard library memanggil `panic!` jika kamu mencoba mengakses memori di luar batas: Mencoba mengakses memori yang bukan milik struktur data saat ini adalah masalah keamanan yang umum. Fungsi sering kali memiliki _kontrak_: perilakunya hanya dijamin jika input memenuhi persyaratan tertentu. Melakukan panic saat kontrak dilanggar masuk akal karena pelanggaran kontrak selalu menandakan bug di sisi pemanggil, dan ini bukan jenis error yang ingin kamu paksa ditangani secara eksplisit oleh kode pemanggil. Malah, tidak ada cara yang masuk akal bagi kode pemanggil untuk pulih; _programmer_ yang memanggillah yang perlu memperbaiki kodenya. Kontrak sebuah fungsi, terutama ketika pelanggarannya akan menyebabkan panic, sebaiknya dijelaskan di dokumentasi API fungsi tersebut.

Namun, memiliki banyak pemeriksaan error di semua fungsi kamu akan terasa bertele-tele dan menjengkelkan. Untungnya, kamu bisa memakai sistem tipe Rust (dan dengan demikian pemeriksaan tipe yang dilakukan compiler) untuk melakukan banyak pemeriksaan itu untukmu. Jika fungsi kamu memiliki tipe tertentu sebagai parameter, kamu bisa melanjutkan logika kode dengan keyakinan bahwa compiler sudah memastikan kamu memiliki nilai yang valid. Misalnya, jika kamu memiliki tipe tertentu alih-alih `Option`, program kamu mengharapkan _sesuatu_ daripada _tidak ada apa-apa_. Kode kamu lalu tidak perlu menangani dua kasus untuk varian `Some` dan `None`: ia hanya perlu satu kasus, yaitu memang memiliki nilai. Kode yang mencoba meneruskan "tidak ada" ke fungsi kamu bahkan tidak akan terkompilasi, jadi fungsi kamu tidak perlu memeriksa kasus itu saat runtime. Contoh lain adalah memakai tipe integer tak bertanda seperti `u32`, yang memastikan parameter tidak pernah negatif.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-custom-types-for-validation"></a>

### Tipe Kustom untuk Validasi

Mari kita selangkah lebih jauh dengan gagasan memakai sistem tipe Rust untuk memastikan kita memiliki nilai yang valid, dan melihat pembuatan tipe kustom untuk validasi. Ingat permainan tebak-tebakan di Bab 2, di mana kode kita meminta pengguna menebak angka antara 1 dan 100. Kita tidak pernah memvalidasi apakah tebakan pengguna berada di rentang itu sebelum membandingkannya dengan angka rahasia; kita hanya memvalidasi bahwa tebakannya positif. Dalam kasus ini, akibatnya tidak terlalu parah: Keluaran “Terlalu tinggi” atau “Terlalu rendah” tetap benar. Namun, akan berguna jika kita menuntun pengguna agar menebak angka yang valid, dan memberikan perilaku yang berbeda ketika pengguna menebak angka di luar rentang dibandingkan ketika mereka, misalnya, mengetik huruf.

Satu cara melakukan ini adalah mengurai tebakan sebagai `i32`, bukan hanya `u32`, agar angka negatif juga mungkin, lalu menambahkan pemeriksaan apakah angkanya berada dalam rentang, seperti ini:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-09-guess-out-of-range/src/main.rs:here}}
```

</Listing>

Ekspresi `if` memeriksa apakah nilai kita di luar rentang, memberi tahu pengguna tentang masalah itu, dan memanggil `continue` untuk memulai iterasi berikutnya dari loop dan meminta tebakan lain. Setelah ekspresi `if`, kita bisa melanjutkan perbandingan antara `guess` dan angka rahasia dengan keyakinan bahwa `guess` berada antara 1 dan 100.

Namun, ini bukan solusi yang ideal: Seandainya sangat penting bahwa program hanya beroperasi pada nilai antara 1 dan 100, dan ada banyak fungsi dengan persyaratan seperti itu, memiliki pemeriksaan seperti ini di setiap fungsi akan melelahkan (dan bisa berdampak pada performa).

Sebagai gantinya, kita bisa membuat tipe baru di module khusus dan menaruh validasi di dalam fungsi yang membuat instance tipe itu, daripada mengulang validasi di mana-mana. Dengan begitu, aman bagi fungsi untuk memakai tipe baru itu di signature mereka dan dengan percaya diri memakai nilai yang mereka terima. Listing 9-13 menunjukkan salah satu cara mendefinisikan tipe `Guess` yang hanya akan membuat instance `Guess` jika fungsi `new` menerima nilai antara 1 dan 100.

<Listing number="9-13" caption="Tipe `Guess` yang hanya akan melanjutkan dengan nilai antara 1 dan 100" file-name="src/guessing_game.rs">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-13/src/guessing_game.rs}}
```

</Listing>

Perlu dicatat bahwa kode dalam *src/guessing_game.rs* ini bergantung pada penambahan deklarasi module `mod guessing_game;` di *src/lib.rs* yang belum kita tampilkan di sini. Di dalam file module baru itu, kita mendefinisikan struct bernama `Guess` yang memiliki field bernama `value` yang menyimpan `i32`. Di sinilah angka itu akan disimpan.

Lalu, kita mengimplementasikan fungsi asosiasi bernama `new` pada `Guess` yang membuat instance nilai `Guess`. Fungsi `new` didefinisikan dengan satu parameter bernama `value` bertipe `i32` dan mengembalikan `Guess`. Kode di tubuh fungsi `new` menguji `value` untuk memastikan nilainya antara 1 dan 100. Jika `value` tidak lolos uji ini, kita memanggil `panic!`, yang akan memberi tahu programmer yang menulis kode pemanggil bahwa mereka punya bug yang perlu diperbaiki, karena membuat `Guess` dengan `value` di luar rentang itu akan melanggar kontrak yang diandalkan `Guess::new`. Kondisi-kondisi di mana `Guess::new` bisa melakukan panic sebaiknya dibahas di dokumentasi API yang menghadap publik; kita akan membahas konvensi dokumentasi untuk menandai kemungkinan `panic!` dalam dokumentasi API yang kamu buat di Bab 14. Jika `value` lolos uji, kita membuat `Guess` baru dengan field `value` diisi dari parameter `value`, lalu mengembalikan `Guess` itu.

Selanjutnya, kita mengimplementasikan metode bernama `value` yang meminjam `self`, tidak punya parameter lain, dan mengembalikan `i32`. Jenis metode ini kadang disebut _getter_ karena tujuannya mengambil data dari field-nya lalu mengembalikannya. Metode publik ini diperlukan karena field `value` dari struct `Guess` bersifat private. Penting bahwa field `value` itu private agar kode yang memakai struct `Guess` tidak boleh menetapkan `value` secara langsung: Kode di luar module `guessing_game` _harus_ memakai fungsi `Guess::new` untuk membuat instance `Guess`, sehingga tidak ada cara bagi sebuah `Guess` untuk memiliki `value` yang belum diperiksa oleh kondisi di fungsi `Guess::new`.

Sebuah fungsi yang memiliki parameter atau hanya mengembalikan angka antara 1 dan 100 lalu bisa menyatakan di signature-nya bahwa ia menerima atau mengembalikan `Guess`, bukan `i32`, dan tidak perlu melakukan pemeriksaan tambahan di tubuhnya.

## Ringkasan

Fitur penanganan error Rust dirancang untuk membantumu menulis kode yang lebih tangguh. Macro `panic!` menandakan bahwa program kamu berada dalam keadaan yang tidak bisa ditangani, dan membiarkan kamu memerintahkan proses untuk berhenti alih-alih mencoba melanjutkan dengan nilai yang tidak valid atau salah. Enum `Result` memakai sistem tipe Rust untuk menunjukkan bahwa operasi bisa gagal dengan cara yang masih bisa dipulihkan oleh kode kamu. Kamu bisa memakai `Result` untuk memberi tahu kode yang memanggil kode kamu bahwa ia juga perlu menangani kemungkinan berhasil atau gagal. Memakai `panic!` dan `Result` dalam situasi yang tepat akan membuat kode kamu lebih andal saat menghadapi masalah yang tak terelakkan.

Setelah kamu melihat cara-cara berguna standard library memakai generic dengan enum `Option` dan `Result`, kita akan membahas cara kerja generic dan cara memakainya dalam kode kamu.

[encoding]: ch18-03-oo-design-patterns.html#encoding-states-and-behavior-as-types
