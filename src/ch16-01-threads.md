## Menggunakan Thread untuk Menjalankan Kode Secara Bersamaan

Di sebagian besar sistem operasi masa kini, kode dari program yang dijalankan berada di dalam sebuah _proses_, dan sistem operasi mengelola beberapa proses sekaligus. Di dalam sebuah program, kamu juga bisa punya bagian-bagian independen yang berjalan secara bersamaan. Fitur yang menjalankan bagian-bagian independen ini disebut _thread_. Misalnya, sebuah web server bisa punya beberapa thread agar dapat merespons lebih dari satu permintaan pada saat yang sama.

Memecah komputasi dalam programmu menjadi beberapa thread untuk menjalankan banyak tugas sekaligus bisa meningkatkan kinerja, tapi juga menambah kompleksitas. Karena thread bisa berjalan secara bersamaan, tidak ada jaminan bawaan tentang urutan bagian kode di thread yang berbeda akan dieksekusi. Hal ini bisa menimbulkan masalah, misalnya:

- Race condition, ketika beberapa thread mengakses data atau resource dengan urutan yang tidak konsisten
- Deadlock, ketika dua thread saling menunggu sehingga keduanya tidak bisa melanjutkan
- Bug yang hanya muncul dalam situasi tertentu dan sulit direproduksi serta diperbaiki secara konsisten

Rust berusaha mengurangi dampak negatif penggunaan thread, tapi pemrograman dalam konteks multithread tetap membutuhkan pemikiran yang matang dan struktur kode yang berbeda dari program yang berjalan di satu thread.

Bahasa pemrograman mengimplementasikan thread dengan beberapa cara, dan banyak sistem operasi menyediakan API yang bisa dipanggil bahasa tersebut untuk membuat thread baru. Pustaka standar Rust memakai model implementasi thread _1:1_, di mana sebuah program memakai satu thread sistem operasi untuk setiap satu thread bahasa. Ada crate yang mengimplementasikan model threading lain dengan trade-off yang berbeda dari model 1:1. (Sistem async Rust, yang akan kita lihat di bab berikutnya, juga menyediakan pendekatan lain untuk concurrency.)

<a id="creating-a-new-thread-with-spawn"></a>
### Membuat Thread Baru dengan `spawn`

Untuk membuat thread baru, kita memanggil fungsi `thread::spawn` dan memberinya closure (yang sudah kita bahas di Bab 13) berisi kode yang ingin kita jalankan di thread baru itu. Contoh di Listing 16-1 mencetak beberapa teks dari thread utama dan teks lain dari thread baru.

<Listing number="16-1" file-name="src/main.rs" caption="Membuat thread baru untuk mencetak sesuatu sementara thread utama mencetak hal lain">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-01/src/main.rs}}
```

</Listing>

Perhatikan bahwa ketika thread utama program Rust selesai, semua thread yang di-spawn akan dimatikan, terlepas dari sudah selesai berjalan atau tidak. Output program ini mungkin sedikit berbeda setiap kali dijalankan, tapi akan terlihat mirip seperti berikut:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the main thread!
hi number 1 from the spawned thread!
hi number 2 from the main thread!
hi number 2 from the spawned thread!
hi number 3 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the main thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
```

Pemanggilan `thread::sleep` memaksa sebuah thread menghentikan eksekusinya untuk waktu singkat, memberi kesempatan thread lain untuk berjalan. Thread-thread itu kemungkinan bergiliran, tapi tidak ada jaminan: semuanya tergantung cara sistem operasi menjadwalkan thread. Pada menjalankan kali ini, thread utama mencetak lebih dulu, meskipun pernyataan cetak dari thread spawned muncul lebih awal di kode. Dan meskipun kita meminta thread spawned mencetak hingga `i` mencapai `9`, ia hanya sampai di `5` sebelum thread utama mematikkannya.

Jika kamu menjalankan kode ini dan hanya melihat output dari thread utama, atau tidak melihat adanya selang-seling, coba besarkan angka-angka pada range agar sistem operasi punya lebih banyak kesempatan berpindah antar-thread.

<!-- Old headings. Do not remove or links may break. -->

<a id="waiting-for-all-threads-to-finish-using-join-handles"></a>

<a id="waiting-for-all-threads-to-finish"></a>
### Menunggu Semua Thread Selesai

Kode di Listing 16-1 tidak hanya menghentikan thread spawned terlalu awal pada sebagian besar kasus karena thread utama berakhir, tapi karena tidak ada jaminan tentang urutan thread berjalan, kita juga tidak bisa menjamin bahwa thread spawned itu akan berjalan sama sekali!

Kita bisa mengatasi masalah thread spawned yang tidak berjalan atau berakhir terlalu awal dengan menyimpan nilai kembalian `thread::spawn` ke dalam sebuah variabel. Tipe kembalian `thread::spawn` adalah `JoinHandle<T>`. Sebuah `JoinHandle<T>` adalah nilai owned yang, ketika kita memanggil method `join` padanya, akan menunggu thread-nya selesai. Listing 16-2 menunjukkan cara memakai `JoinHandle<T>` dari thread yang kita buat di Listing 16-1 dan cara memanggil `join` untuk memastikan thread spawned selesai sebelum `main` keluar.

<Listing number="16-2" file-name="src/main.rs" caption="Menyimpan `JoinHandle<T>` dari `thread::spawn` untuk menjamin thread dijalankan hingga selesai">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-02/src/main.rs}}
```

</Listing>

Memanggil `join` pada handle memblokir thread yang sedang berjalan sampai thread yang diwakili handle itu berakhir. _Memblokir_ sebuah thread berarti thread itu dicegah melakukan pekerjaan atau keluar. Karena kita meletakkan pemanggilan `join` setelah loop `for` thread utama, menjalankan Listing 16-2 seharusnya menghasilkan output seperti ini:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 1 from the spawned thread!
hi number 3 from the main thread!
hi number 2 from the spawned thread!
hi number 4 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
```

Kedua thread terus bergiliran, tapi thread utama menunggu karena pemanggilan `handle.join()` dan tidak berakhir sampai thread spawned selesai.

Tapi mari kita lihat apa yang terjadi jika kita memindahkan `handle.join()` sebelum loop `for` di `main`, seperti ini:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/no-listing-01-join-too-early/src/main.rs}}
```

</Listing>

Thread utama akan menunggu thread spawned selesai lalu menjalankan loop `for`-nya, sehingga output tidak lagi selang-seling, seperti yang ditunjukkan di sini:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the spawned thread!
hi number 2 from the spawned thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 3 from the main thread!
hi number 4 from the main thread!
```

Detail kecil, seperti di mana `join` dipanggil, bisa memengaruhi apakah thread-mu berjalan bersamaan atau tidak.

<a id="using-move-closures-with-threads"></a>
### Memakai Closure `move` dengan Thread

Kita akan sering memakai keyword `move` dengan closure yang diteruskan ke `thread::spawn`, karena closure itu akan mengambil ownership nilai-nilai yang dipakainya dari lingkungan, sehingga memindahkan ownership nilai-nilai itu dari satu thread ke thread lain. Di [“Menangkap Reference atau Memindahkan Ownership”][capture]<!-- ignore --> Bab 13, kita sudah membahas `move` dalam konteks closure. Sekarang kita akan lebih fokus pada interaksi antara `move` dan `thread::spawn`.

Perhatikan di Listing 16-1 bahwa closure yang kita berikan ke `thread::spawn` tidak menerima argumen: kita tidak memakai data dari thread utama di kode thread spawned. Untuk memakai data dari thread utama di dalam thread spawned, closure thread spawned harus menangkap nilai-nilai yang dibutuhkannya. Listing 16-3 menunjukkan percobaan membuat sebuah vector di thread utama lalu memakainya di thread spawned. Namun, kode ini belum akan berjalan, seperti yang akan kamu lihat sebentar lagi.

<Listing number="16-3" file-name="src/main.rs" caption="Mencoba memakai vector yang dibuat thread utama di thread lain">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-03/src/main.rs}}
```

</Listing>

Closure itu memakai `v`, jadi ia akan menangkap `v` dan menjadikannya bagian dari lingkungan closure. Karena `thread::spawn` menjalankan closure ini di thread baru, seharusnya kita bisa mengakses `v` di dalam thread baru itu. Tapi ketika kita mengompilasi contoh ini, kita mendapat error berikut:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-03/output.txt}}
```

Rust _menyimpulkan_ cara menangkap `v`, dan karena `println!` hanya butuh reference ke `v`, closure itu mencoba meminjam `v`. Namun, ada masalah: Rust tidak bisa tahu berapa lama thread spawned akan berjalan, jadi ia tidak tahu apakah reference ke `v` akan selalu valid.

Listing 16-4 memberi skenario yang lebih mungkin menghasilkan reference ke `v` yang tidak valid.

<Listing number="16-4" file-name="src/main.rs" caption="Sebuah thread dengan closure yang mencoba menangkap reference ke `v` dari thread utama yang me-drop `v`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-04/src/main.rs}}
```

</Listing>

Jika Rust mengizinkan kita menjalankan kode ini, ada kemungkinan thread spawned langsung dijadikan background tanpa berjalan sama sekali. Thread spawned punya reference ke `v` di dalamnya, tapi thread utama langsung me-drop `v` memakai fungsi `drop` yang kita bahas di Bab 15. Lalu, ketika thread spawned mulai dieksekusi, `v` sudah tidak valid lagi, sehingga reference kepadanya juga tidak valid. Oh, tidak!

Untuk memperbaiki error compiler di Listing 16-3, kita bisa mengikuti saran dari pesan error tersebut:

<!-- manual-regeneration
after automatic regeneration, look at listings/ch16-fearless-concurrency/listing-16-03/output.txt and copy the relevant part
-->

```text
help: to force the closure to take ownership of `v` (and any other referenced variables), use the `move` keyword
  |
6 |     let handle = thread::spawn(move || {
  |                                ++++
```

Dengan menambahkan keyword `move` sebelum closure, kita memaksa closure itu mengambil ownership nilai-nilai yang dipakainya, alih-alih membiarkan Rust menyimpulkan bahwa nilai-nilai itu harus dipinjam. Perubahan pada Listing 16-3 yang ditunjukkan di Listing 16-5 akan terkompilasi dan berjalan sesuai yang kita inginkan.

<Listing number="16-5" file-name="src/main.rs" caption="Memakai keyword `move` untuk memaksa closure mengambil ownership nilai-nilai yang dipakainya">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-05/src/main.rs}}
```

</Listing>

Kita mungkin tergoda mencoba hal yang sama untuk memperbaiki kode di Listing 16-4, di mana thread utama memanggil `drop`, dengan memakai closure `move`. Namun, perbaikan ini tidak akan berhasil karena apa yang dicoba Listing 16-4 dilarang demi alasan yang berbeda. Jika kita menambahkan `move` ke closure, kita akan memindahkan `v` ke dalam lingkungan closure, dan kita tidak bisa lagi memanggil `drop` padanya di thread utama. Sebaliknya, kita akan mendapat error compiler ini:

```console
{{#include ../listings/ch16-fearless-concurrency/output-only-01-move-drop/output.txt}}
```

Aturan ownership Rust menyelamatkan kita lagi! Kita mendapat error dari kode di Listing 16-3 karena Rust bersikap konservatif dan hanya meminjam `v` untuk thread itu, yang berarti secara teori thread utama bisa membatalkan reference thread spawned. Dengan memberi tahu Rust untuk memindahkan ownership `v` ke thread spawned, kita menjamin pada Rust bahwa thread utama tidak akan memakai `v` lagi. Jika kita mengubah Listing 16-4 dengan cara yang sama, kita justru melanggar aturan ownership ketika mencoba memakai `v` di thread utama. Keyword `move` menimpa default konservatif Rust berupa peminjaman; keyword ini tidak membiarkan kita melanggar aturan ownership.

Sekarang setelah kita membahas apa itu thread dan method yang disediakan API thread, mari kita lihat beberapa situasi di mana kita bisa memakai thread.

[capture]: ch13-01-closures.html#capturing-references-or-moving-ownership
