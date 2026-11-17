## Concurrency Shared-State

Mengirim pesan adalah cara yang baik untuk menangani concurrency, tetapi bukan satu-satunya cara. Cara lain adalah dengan membiarkan beberapa thread mengakses data bersama yang sama. Ingat lagi bagian dari slogan dokumentasi bahasa Go ini: “Jangan berkomunikasi dengan berbagi memori.”

Bagaimana rasanya berkomunikasi dengan berbagi memori? Lalu, mengapa para pendukung pengiriman pesan memperingatkan kita untuk tidak memakai berbagi memori?

Secara tertentu, channel di bahasa pemrograman apa pun mirip dengan single ownership, karena begitu kamu mengirimkan sebuah nilai melalui channel, kamu tidak boleh lagi memakai nilai itu. Concurrency shared-memory mirip dengan multiple ownership: beberapa thread bisa mengakses lokasi memori yang sama pada saat bersamaan. Seperti yang kamu lihat di Bab 15, smart pointer memungkinkan multiple ownership. Kepemilikan ganda bisa menambah kompleksitas karena semua pemiliknya perlu dikelola. Sistem tipe dan aturan ownership Rust sangat membantu agar pengelolaan ini berjalan benar. Sebagai contoh, mari kita lihat mutex, salah satu primitif concurrency yang paling umum untuk shared memory.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-mutexes-to-allow-access-to-data-from-one-thread-at-a-time"></a>

### Mengontrol Akses dengan Mutex

_Mutex_ adalah singkatan dari _mutual exclusion_, artinya mutex hanya mengizinkan satu thread mengakses sebagian data pada waktu tertentu. Untuk mengakses data di dalam mutex, sebuah thread harus memberi tahu bahwa ia ingin mengaksesnya dengan meminta memperoleh lock mutex tersebut. _Lock_ adalah struktur data yang merupakan bagian dari mutex dan mencatat siapa yang saat ini memiliki akses eksklusif ke data itu. Karena itu, mutex disebut sebagai _menjaga_ data yang disimpannya melalui sistem penguncian ini.

Mutex punya reputasi sulit digunakan karena kamu harus mengingat dua aturan:

1. Kamu harus mencoba memperoleh lock sebelum memakai data.
2. Setelah selesai dengan data yang dijaga mutex, kamu harus membuka lock-nya agar thread lain bisa memperolehnya.

Untuk analogi mutex di dunia nyata, bayangkan sebuah diskusi panel di konferensi yang hanya punya satu mikrofon. Sebelum bisa bicara, setiap panelis harus bertanya atau memberi isyarat bahwa ia ingin memakai mikrofon. Setelah mendapat mikrofon, ia bisa bicara selama yang ia mau, lalu menyerahkan mikrofonnya ke panelis berikutnya yang ingin berbicara. Jika seorang panelis lupa menyerahkan mikrofon setelah selesai, tak ada orang lain yang bisa bicara. Jika pengelolaan mikrofon bersama ini berantakan, diskusi panel tidak akan berjalan seperti rencana!

Mengelola mutex dengan benar bisa sangat rumit, itulah sebabnya banyak orang antusias dengan channel. Namun, berkat sistem tipe dan aturan ownership Rust, kamu tidak bisa salah dalam mengunci dan membuka lock.

#### API dari `Mutex<T>`

Sebagai contoh cara memakai mutex, mari kita mulai dengan menggunakannya dalam konteks single-threaded, seperti yang ditunjukkan pada Listing 16-12.

<Listing number="16-12" file-name="src/main.rs" caption="Exploring the API of `Mutex<T>` in a single-threaded context for simplicity">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-12/src/main.rs}}
```

</Listing>

Seperti banyak tipe lainnya, kita membuat `Mutex<T>` dengan fungsi asosiasi `new`. Untuk mengakses data di dalam mutex, kita memakai method `lock` untuk memperoleh lock-nya. Panggilan ini akan memblokir thread saat ini sehingga ia tidak bisa melakukan apa pun sampai giliran kita untuk mendapat lock.

Panggilan ke `lock` akan gagal jika thread lain yang memegang lock mengalami panic. Dalam kasus itu, tak ada yang bisa mendapatkan lock lagi, maka kita memilih untuk `unwrap` dan membiarkan thread ini panic jika situasi itu terjadi.

Setelah mendapat lock, kita bisa memperlakukan nilai kembaliannya—disebut `num` di sini—sebagai mutable reference ke data di dalamnya. Sistem tipe memastikan kita memperoleh lock sebelum memakai nilai di `m`. Tipe `m` adalah `Mutex<i32>`, bukan `i32`, jadi kita _harus_ memanggil `lock` agar bisa memakai nilai `i32` itu. Kita tidak bisa lupa; kalau tidak, sistem tipe tidak akan mengizinkan kita mengakses `i32` di dalamnya.

Panggilan ke `lock` mengembalikan tipe bernama `MutexGuard`, yang dibungkus dalam `LockResult` dan kita tangani dengan panggilan `unwrap`. Tipe `MutexGuard` mengimplementasikan `Deref` untuk menunjuk ke data di dalamnya; tipe ini juga punya implementasi `Drop` yang melepas lock secara otomatis ketika `MutexGuard` keluar dari scope, yaitu di akhir scope dalam. Hasilnya, kita tidak perlu khawatir lupa melepas lock dan menghalangi mutex dipakai thread lain, karena pelepasan lock terjadi otomatis.

Setelah lock dijatuhkan, kita bisa mencetak nilai mutex dan melihat rằng kita berhasil mengubah `i32` di dalamnya menjadi `6`.

<!-- Old headings. Do not remove or links may break. -->

<a id="sharing-a-mutext-between-multiple-threads"></a>

<a id="shared-access-to-mutext"></a>
#### Akses Bersama ke `Mutex<T>`

Sekarang mari kita coba berbagi nilai antar beberapa thread menggunakan `Mutex<T>`. Kita akan menjalankan 10 thread, masing-masing menambah nilai counter sebanyak 1, sehingga counter naik dari 0 menjadi 10. Contoh pada Listing 16-13 akan menghasilkan error compiler, dan kita akan memakai error itu untuk belajar lebih banyak tentang `Mutex<T>` serta bagaimana Rust membantu kita menggunakannya dengan benar.

<Listing number="16-13" file-name="src/main.rs" caption="Ten threads, each incrementing a counter guarded by a `Mutex<T>`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-13/src/main.rs}}
```

</Listing>

Kita membuat variabel `counter` untuk menyimpan `i32` di dalam `Mutex<T>`, seperti yang kita lakukan di Listing 16-12. Berikutnya, kita membuat 10 thread dengan mengiterasi atas rentang angka. Kita memakai `thread::spawn` dan memberi semua thread closure yang sama: closure yang memindahkan counter ke dalam thread, memperoleh lock pada `Mutex<T>` dengan memanggil method `lock`, lalu menambah 1 pada nilai di mutex. Saat sebuah thread selesai menjalankan closure-nya, `num` akan keluar dari scope dan melepas lock agar thread lain bisa memperolehnya.

Di thread utama, kita mengumpulkan semua join handle. Lalu, seperti di Listing 16-2, kita memanggil `join` pada setiap handle untuk memastikan semua thread selesai. Pada titik itu, thread utama akan memperoleh lock dan mencetak hasil program ini.

Kita sudah mengisyaratkan bahwa contoh ini tidak akan terkompilasi. Sekarang mari kita cari tahu mengapa!

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-13/output.txt}}
```

Pesan error menyatakan bahwa nilai `counter` dipindahkan pada iterasi loop sebelumnya. Rust memberi tahu kita bahwa kita tidak bisa memindahkan ownership `counter` ke dalam beberapa thread. Mari kita perbaiki error compiler ini dengan metode multiple ownership yang kita bahas di Bab 15.

#### Multiple Ownership dengan Beberapa Thread

Di Bab 15, kita memberikan sebuah nilai kepada beberapa pemilik dengan memakai smart pointer `Rc<T>` untuk membuat nilai yang menggunakan reference counting. Mari kita lakukan hal yang sama di sini dan melihat apa yang terjadi. Kita akan membungkus `Mutex<T>` dengan `Rc<T>` pada Listing 16-14 dan meng-clone `Rc<T>` sebelum memindahkan ownership ke thread.

<Listing number="16-14" file-name="src/main.rs" caption="Attempting to use `Rc<T>` to allow multiple threads to own the `Mutex<T>`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-14/src/main.rs}}
```

</Listing>

Sekali lagi kita mengompilasi dan mendapat... error yang berbeda! Compiler mengajari kita banyak hal:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-14/output.txt}}
```

Wah, pesan error-nya sangat panjang! Ini bagian penting yang perlu diperhatikan: `` `Rc<Mutex<i32>>` cannot be sent between threads safely ``. Compiler juga memberi tahu alasannya: `` the trait `Send` is not implemented for `Rc<Mutex<i32>>` ``. Kita akan membahas `Send` di bagian berikutnya: ia adalah salah satu trait yang memastikan tipe yang kita pakai dengan thread memang ditujukan untuk situasi concurrency.

Sayangnya, `Rc<T>` tidak aman untuk dibagikan lintas thread. Saat `Rc<T>` mengelola reference count, ia menambah jumlahnya untuk setiap panggilan `clone` dan menguranginya ketika setiap clone dijatuhkan. Namun ia tidak memakai primitif concurrency apa pun untuk memastikan perubahan pada jumlah itu tidak bisa disela oleh thread lain. Hal ini bisa menyebabkan jumlah yang salah—bug halus yang pada gilirannya bisa memicu kebocoran memori atau nilai yang dijatuhkan sebelum kita selesai menggunakannya. Yang kita butuhkan adalah tipe yang persis seperti `Rc<T>`, tetapi mengubah reference count dengan cara yang aman untuk thread.

#### Atomic Reference Counting dengan `Arc<T>`

Untungnya, `Arc<T>` _memang_ tipe seperti `Rc<T>` yang aman dipakai dalam situasi concurrency. Huruf _a_ singkatan dari _atomic_, artinya tipe ini adalah _atomically reference-counted_. Atomik adalah jenis primitif concurrency tambahan yang tidak akan kita bahas secara rinci di sini: lihat dokumentasi standard library untuk [`std::sync::atomic`][atomic]<!-- ignore --> jika ingin tahu lebih banyak. Untuk saat ini, kamu hanya perlu tahu bahwa tipe atomik bekerja seperti tipe primitif, tetapi aman dibagikan lintas thread.

Kamu mungkin bertanya mengapa tidak semua tipe primitif bersifat atomik, dan mengapa tipe di standard library tidak diimplementasikan memakai `Arc<T>` secara default. Alasannya, keamanan thread datang dengan biaya performa yang hanya ingin kamu bayar saat benar-benar membutuhkannya. Jika kamu hanya melakukan operasi pada nilai di dalam satu thread, kodemu bisa berjalan lebih cepat jika tidak perlu menjamin hal-hal yang dijamin atomik.

Kembali ke contoh kita: `Arc<T>` dan `Rc<T>` punya API yang sama, jadi kita perbaiki program dengan mengubah baris `use`, panggilan ke `new`, dan panggilan ke `clone`. Kode pada Listing 16-15 akhirnya akan terkompilasi dan berjalan.

<Listing number="16-15" file-name="src/main.rs" caption="Using an `Arc<T>` to wrap the `Mutex<T>` to be able to share ownership across multiple threads">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-15/src/main.rs}}
```

</Listing>

Kode ini akan mencetak hal berikut:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Result: 10
```

Kita berhasil! Kita menghitung dari 0 sampai 10, yang mungkin tidak terlalu mengesankan, tapi ini mengajarkan kita banyak hal tentang `Mutex<T>` dan keamanan thread. Kamu juga bisa memakai struktur program ini untuk operasi yang lebih rumit sekadar menambah counter. Dengan strategi ini, kamu bisa membagi sebuah perhitungan menjadi bagian-bagian independen, menyebarkannya ke beberapa thread, lalu memakai `Mutex<T>` agar setiap thread memperbarui hasil akhir dengan bagiannya.

Perlu dicatat, jika kamu melakukan operasi numerik sederhana, ada tipe yang lebih sederhana daripada `Mutex<T>` yang disediakan oleh [modul `std::sync::atomic` dari standard library][atomic]<!-- ignore -->. Tipe-tipe ini menyediakan akses atomik yang aman dan concurrent ke tipe primitif. Kita memilih memakai `Mutex<T>` dengan tipe primitif dalam contoh ini agar bisa fokus pada cara kerja `Mutex<T>`.

<!-- Old headings. Do not remove or links may break. -->

<a id="similarities-between-refcelltrct-and-mutextarct"></a>

### Membandingkan `RefCell<T>`/`Rc<T>` dan `Mutex<T>`/`Arc<T>`

Kamu mungkin memperhatikan bahwa `counter` bersifat immutable, tetapi kita bisa mendapat mutable reference ke nilai di dalamnya; ini berarti `Mutex<T>` menyediakan interior mutability, seperti yang dilakukan keluarga `Cell`. Sama seperti kita memakai `RefCell<T>` di Bab 15 untuk mengubah isi di dalam `Rc<T>`, kita memakai `Mutex<T>` untuk mengubah isi di dalam `Arc<T>`.

Detail lain yang perlu dicatat: Rust tidak bisa melindungimu dari semua jenis error logika saat kamu memakai `Mutex<T>`. Ingat dari Bab 15 bahwa memakai `Rc<T>` membawa risiko terbentuknya reference cycle: dua nilai `Rc<T>` saling merujuk sehingga menyebabkan kebocoran memori. Begitu pula, `Mutex<T>` membawa risiko munculnya _deadlock_. Deadlock terjadi ketika sebuah operasi perlu mengunci dua sumber daya, sementara dua thread masing-masing sudah memperoleh salah satu lock, sehingga mereka saling menunggu selamanya. Jika kamu tertarik dengan deadlock, coba buat program Rust yang mengalami deadlock; lalu, cari strategi mitigasi deadlock untuk mutex dalam bahasa apa pun dan coba terapkan dalam Rust. Dokumentasi API standard library untuk `Mutex<T>` dan `MutexGuard` menyediakan informasi yang berguna.

Kita akan menutup bab ini dengan membahas trait `Send` dan `Sync`, serta cara memakainya dengan tipe buatanmu sendiri.

[atomic]: ../std/sync/atomic/index.html
