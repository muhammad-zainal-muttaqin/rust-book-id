<!-- Old headings. Do not remove or links may break. -->

<a id="concurrency-with-async"></a>

## Menerapkan Concurrency dengan Async

Di bagian ini, kita akan menerapkan async pada beberapa tantangan concurrency yang sama yang kita tangani dengan thread di Bab 16. Karena kita sudah membahas banyak ide kunci di sana, di bagian ini kita akan fokus pada apa yang berbeda antara thread dan future.

Dalam banyak kasus, API untuk bekerja dengan concurrency memakai async sangat mirip dengan API untuk memakai thread. Dalam kasus lain, keduanya bisa jadi sangat berbeda. Bahkan ketika API-nya _tampak_ mirip antara thread dan async, perilakunya sering kali berbeda—dan hampir selalu karakteristik performanya pun berbeda.

<!-- Old headings. Do not remove or links may break. -->

<a id="counting"></a>

### Membuat Task Baru dengan `spawn_task`

Operasi pertama yang kita tangani di bagian ["Membuat Thread Baru dengan `spawn`"][thread-spawn]<!-- ignore --> di Bab 16 adalah menghitung pada dua thread terpisah. Mari kita lakukan hal yang sama dengan async. Crate `trpl` menyediakan fungsi `spawn_task` yang tampak sangat mirip dengan API `thread::spawn`, serta fungsi `sleep` yang merupakan versi async dari API `thread::sleep`. Kita bisa memakai keduanya untuk menerapkan contoh penghitungan itu, seperti yang ditunjukkan pada Listing 17-6.

<Listing number="17-6" caption="Membuat task baru untuk mencetak satu hal sementara task utama mencetak hal lain" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-06/src/main.rs:all}}
```

</Listing>

Sebagai titik awal, kita menyiapkan fungsi `main` dengan `trpl::block_on` agar fungsi tingkat atas kita bisa bersifat async.

> Catatan: Mulai dari sini sampai akhir bab, setiap contoh akan menyertakan
> kode pembungkus yang sama persis dengan `trpl::block_on` di `main`, jadi kita
> akan sering melewatkannya, seperti yang juga kita lakukan dengan `main`. Ingatlah
> untuk menyertakannya dalam kodemu!

Lalu kita menulis dua loop di dalam blok itu, masing-masing berisi pemanggilan `trpl::sleep`, yang menunggu setengah detik (500 milidetik) sebelum mengirim pesan berikutnya. Kita menaruh satu loop di dalam tubuh `trpl::spawn_task` dan yang lain di dalam loop `for` tingkat atas. Kita juga menambahkan `await` setelah pemanggilan `sleep` itu.

Kode ini berperilaku mirip dengan implementasi berbasis thread—termasuk fakta bahwa kamu mungkin melihat pesan-pesan muncul dalam urutan berbeda di terminalmu sendiri saat menjalankannya:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
```

Versi ini berhenti segera setelah loop `for` di dalam tubuh async blok utama selesai, karena task yang di-spawn oleh `spawn_task` dimatikan saat fungsi `main` berakhir. Jika kamu ingin kode itu berjalan sampai task-nya selesai, kamu perlu memakai join handle untuk menunggu task pertama selesai. Dengan thread, kita memakai metode `join` untuk "mem-blok" sampai thread selesai berjalan. Di Listing 17-7, kita bisa memakai `await` untuk melakukan hal yang sama, karena task handle itu sendiri adalah sebuah future. Tipe `Output`-nya adalah `Result`, jadi kita juga melakukan unwrap setelah menunggunya dengan `await`.

<Listing number="17-7" caption="Memakai `await` dengan join handle untuk menjalankan task sampai selesai" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-07/src/main.rs:handle}}
```

</Listing>

Versi yang diperbarui ini berjalan sampai _kedua_ loop selesai:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

Sejauh ini, tampaknya async dan thread memberi kita hasil yang serupa, hanya dengan sintaks yang berbeda: memakai `await` alih-alih memanggil `join` pada join handle, serta meng-await pemanggilan `sleep`.

Perbedaan yang lebih besar adalah kita tidak perlu membuat thread sistem operasi lain untuk melakukan ini. Bahkan, di sini kita bahkan tidak perlu membuat task sama sekali. Karena blok async dikompilasi menjadi future anonim, kita bisa menaruh setiap loop di dalam blok async dan membiarkan runtime menjalankan keduanya sampai selesai dengan fungsi `trpl::join`.

Di bagian ["Menunggu Semua Thread Selesai"][join-handles]<!-- ignore --> di Bab 16, kita menunjukkan cara memakai metode `join` pada tipe `JoinHandle` yang dikembalikan saat kamu memanggil `std::thread::spawn`. Fungsi `trpl::join` mirip, tetapi untuk future. Saat kamu memberinya dua future, fungsi itu menghasilkan satu future baru yang keluarannya adalah tuple berisi keluaran dari masing-masing future yang kamu berikan setelah keduanya _sama-sama_ selesai. Jadi, di Listing 17-8, kita memakai `trpl::join` untuk menunggu `fut1` dan `fut2` selesai. Kita _tidak_ meng-await `fut1` dan `fut2`, melainkan future baru yang dihasilkan oleh `trpl::join`. Kita mengabaikan keluarannya, karena itu hanya tuple yang berisi dua nilai unit.

<Listing number="17-8" caption="Memakai `trpl::join` untuk meng-await dua future anonim" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-08/src/main.rs:join}}
```

</Listing>

Saat kita menjalankan ini, kita melihat kedua future berjalan sampai selesai:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the first task!
hi number 1 from the second task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

Sekarang, kamu akan melihat urutan yang persis sama setiap kali, yang sangat berbeda dari apa yang kita lihat dengan thread dan dengan `trpl::spawn_task` di Listing 17-7. Itu karena fungsi `trpl::join` bersifat _adil_, artinya ia memeriksa setiap future dengan frekuensi yang sama, bergantian di antaranya, dan tidak pernah membiarkan satu future melesat lebih dulu jika yang lain sudah siap. Dengan thread, sistem operasi yang memutuskan thread mana yang diperiksa dan berapa lama ia boleh berjalan. Dengan async Rust, runtime yang memutuskan task mana yang diperiksa. (Dalam praktiknya, detailnya jadi rumit karena runtime async mungkin memakai thread sistem operasi di balik layar sebagai bagian dari cara ia mengelola concurrency, jadi menjamin keadilan bisa menjadi pekerjaan ekstra bagi runtime—tapi itu tetap mungkin!) Runtime tidak harus menjamin keadilan untuk setiap operasi, dan mereka sering menyediakan API berbeda agar kamu bisa memilih apakah kamu menginginkan keadilan atau tidak.

Cobalah beberapa variasi ini pada cara meng-await future tersebut dan lihat apa yang terjadi:

- Hilangkan blok async dari salah satu atau kedua loop.
- Await setiap blok async segera setelah mendefinisikannya.
- Bungkus hanya loop pertama dalam blok async, lalu await future yang dihasilkan
  setelah tubuh loop kedua.

Sebagai tantangan tambahan, coba tebak apa keluarannya untuk setiap kasus _sebelum_ menjalankan kodenya!

<!-- Old headings. Do not remove or links may break. -->

<a id="message-passing"></a>
<a id="counting-up-on-two-tasks-using-message-passing"></a>

<a id="sending-data-between-two-tasks-using-message-passing"></a>
### Mengirim Data Antara Dua Task dengan Message Passing

Berbagi data antar future juga akan terasa akrab: kita akan memakai message passing lagi, tetapi kali ini dengan versi async dari tipe dan fungsinya. Kita akan mengambil jalur yang sedikit berbeda dari yang kita lakukan di bagian ["Mentransfer Data Antar Thread dengan Message Passing"][message-passing-threads]<!-- ignore --> di Bab 16 untuk mengilustrasikan beberapa perbedaan utama antara concurrency berbasis thread dan berbasis future. Di Listing 17-9, kita akan mulai hanya dengan satu blok async—_bukan_ membuat task terpisah seperti kita membuat thread terpisah.

<Listing number="17-9" caption="Membuat channel async dan menetapkan dua bagiannya ke `tx` dan `rx`" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-09/src/main.rs:channel}}
```

</Listing>

Di sini, kita memakai `trpl::channel`, versi async dari API channel multiple-producer, single-consumer yang kita pakai dengan thread di Bab 16. Versi async dari API ini hanya sedikit berbeda dari versi berbasis thread: ia memakai receiver `rx` yang mutable alih-alih yang immutable, dan metode `recv`-nya menghasilkan future yang perlu kita await alih-alih menghasilkan nilai secara langsung. Sekarang kita bisa mengirim pesan dari pengirim ke penerima. Perhatikan bahwa kita tidak perlu membuat thread terpisah, bahkan task pun tidak; kita hanya perlu meng-await pemanggilan `rx.recv`.

Metode `Receiver::recv` yang sinkron di `std::mpsc::channel` mem-blok sampai ia menerima pesan. Metode `trpl::Receiver::recv` tidak demikian, karena ia async. Alih-alih mem-blok, ia mengembalikan kontrol ke runtime sampai pesan diterima atau sisi pengirim channel ditutup. Sebaliknya, kita tidak meng-await pemanggilan `send`, karena pemanggilan itu tidak mem-blok. Ia tidak perlu demikian, karena channel yang kita kirimi bersifat unbounded.

> Catatan: Karena semua kode async ini berjalan di dalam blok async dalam
> pemanggilan `trpl::block_on`, semua yang ada di dalamnya bisa menghindari
> pem-blokan. Namun, kode di _luar_ itu akan mem-blok sampai fungsi `block_on`
> kembali. Itulah seluruh tujuan dari fungsi `trpl::block_on`: fungsi itu
> membiarkan kamu _memilih_ di mana ingin mem-blok pada sekumpulan kode async,
> dan dengan demikian di mana transisi antara kode sinkron dan async terjadi.

Perhatikan dua hal tentang contoh ini. Pertama, pesan akan tiba seketika. Kedua, meskipun kita memakai future di sini, belum ada concurrency sama sekali. Semua yang ada di listing terjadi secara berurutan, sama seperti ketika tidak ada future yang terlibat.

Mari kita atasi bagian pertama dengan mengirim serangkaian pesan dan menyisipkan jeda `sleep` di antaranya, seperti yang ditunjukkan pada Listing 17-10.

<!-- We cannot test this one because it never stops! -->

<Listing number="17-10" caption="Mengirim dan menerima beberapa pesan melalui channel async dengan menyisipkan `sleep` dan `await` di antara setiap pesan" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-10/src/main.rs:many-messages}}
```

</Listing>

Selain mengirim pesan, kita perlu menerimanya. Dalam hal ini, karena kita tahu berapa banyak pesan yang akan datang, kita bisa melakukannya secara manual dengan memanggil `rx.recv().await` empat kali. Namun, di dunia nyata, kita umumnya akan menunggu sejumlah pesan yang _tidak diketahui_, jadi kita perlu terus menunggu sampai kita menemukan bahwa tidak ada pesan lagi.

Di Listing 16-10, kita memakai loop `for` untuk memproses semua item yang diterima dari channel sinkron. Namun, Rust belum punya cara untuk memakai loop `for` dengan serangkaian item yang _dihasilkan secara async_, jadi kita perlu memakai loop yang belum pernah kita lihat: loop kondisional `while let`. Ini adalah versi loop dari konstruksi `if let` yang kita lihat di bagian ["Alur Kontrol Ringkas dengan `if let` dan `let...else`"][if-let]<!-- ignore --> di Bab 6. Loop akan terus berjalan selama pattern yang ditentukannya terus cocok dengan nilainya.

Pemanggilan `rx.recv` menghasilkan future, yang kita await. Runtime akan menjeda future itu sampai ia siap. Setelah pesan tiba, future akan menghasilkan `Some(message)` setiap kali pesan tiba. Saat channel ditutup, terlepas dari apakah _ada_ pesan yang telah tiba atau tidak, future itu akan menghasilkan `None` sebagai penanda bahwa tidak ada nilai lagi dan karena itu kita harus berhenti melakukan polling—yakni, berhenti meng-await.

Loop `while let` menyatukan semuanya. Jika hasil pemanggilan `rx.recv().await` adalah `Some(message)`, kita mendapatkan akses ke pesan itu dan bisa memakainya di tubuh loop, seperti yang bisa kita lakukan dengan `if let`. Jika hasilnya `None`, loop berakhir. Setiap kali loop selesai satu putaran, ia mencapai titik await lagi, sehingga runtime menjedanya lagi sampai pesan berikutnya tiba.

Kode ini sekarang berhasil mengirim dan menerima semua pesan. Sayangnya, masih ada beberapa masalah. Salah satunya, pesan-pesan itu tidak tiba dalam jeda setengah detik. Mereka tiba sekaligus, 2 detik (2.000 milidetik) setelah kita menjalankan program. Masalah lainnya, program ini juga tidak pernah keluar! Alih-alih, ia menunggu pesan baru selamanya. Kamu perlu mematikannya dengan <kbd>ctrl</kbd>-<kbd>C</kbd>.

#### Kode di Dalam Satu Async Block Berjalan Secara Linear

Mari kita mulai dengan memeriksa mengapa pesan-pesan tiba sekaligus setelah jeda penuh, alih-alih tiba dengan jeda di antara masing-masing pesan. Di dalam sebuah blok async, urutan kemunculan kata kunci `await` dalam kode juga merupakan urutan eksekusinya saat program berjalan.

Hanya ada satu blok async di Listing 17-10, jadi semuanya di dalamnya berjalan secara linear. Masih belum ada concurrency. Semua pemanggilan `tx.send` terjadi, diselingi oleh semua pemanggilan `trpl::sleep` dan titik-titik await yang menyertainya. Baru setelah itu loop `while let` menjalani titik-titik `await` pada pemanggilan `recv`.

Untuk mendapatkan perilaku yang kita inginkan, di mana jeda `sleep` terjadi di antara setiap pesan, kita perlu menaruh operasi `tx` dan `rx` di blok async mereka sendiri, seperti yang ditunjukkan pada Listing 17-11. Lalu runtime bisa menjalankan masing-masing secara terpisah dengan `trpl::join`, seperti di Listing 17-8. Sekali lagi, kita meng-await hasil pemanggilan `trpl::join`, bukan future-future individualnya. Jika kita meng-await future-future itu secara berurutan, kita akan kembali ke alur sekuensial—tepatnya apa yang _tidak_ ingin kita lakukan.

<!-- We cannot test this one because it never stops! -->

<Listing number="17-11" caption="Memisahkan `send` dan `recv` ke dalam blok `async` mereka sendiri dan meng-await future dari blok-blok itu" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-11/src/main.rs:futures}}
```

</Listing>

Dengan kode yang diperbarui di Listing 17-11, pesan-pesan dicetak dalam jeda 500 milidetik, alih-alih semua tiba sekaligus setelah 2 detik.

#### Memindahkan Ownership ke Dalam Async Block

Program itu tetap tidak pernah keluar, karena cara loop `while let` berinteraksi dengan `trpl::join`:

- Future yang dikembalikan oleh `trpl::join` selesai hanya setelah _kedua_ future yang diberikan kepadanya selesai.
- Future `tx_fut` selesai setelah ia menyelesaikan `sleep` terakhir usai mengirim pesan terakhir di `vals`.
- Future `rx_fut` tidak akan selesai sampai loop `while let` berakhir.
- Loop `while let` tidak akan berakhir sampai meng-await `rx.recv` menghasilkan `None`.
- Meng-await `rx.recv` akan mengembalikan `None` hanya setelah ujung channel yang lain ditutup.
- Channel akan ditutup hanya jika kita memanggil `rx.close` atau ketika sisi pengirim, `tx`, di-drop.
- Kita tidak memanggil `rx.close` di mana pun, dan `tx` tidak akan di-drop sampai blok async paling luar yang diberikan ke `trpl::block_on` berakhir.
- Blok itu tidak bisa berakhir karena ia terblok menunggu `trpl::join` selesai, yang membawa kita kembali ke awal daftar ini.

Saat ini, blok async tempat kita mengirim pesan hanya _meminjam_ `tx` karena mengirim pesan tidak memerlukan ownership, tetapi jika kita bisa _memindahkan_ `tx` ke dalam blok async itu, `tx` akan di-drop begitu blok tersebut berakhir. Di bagian ["Menangkap Reference atau Memindahkan Ownership"][capture-or-move]<!-- ignore --> di Bab 13, kamu belajar cara memakai kata kunci `move` dengan closure, dan, seperti yang dibahas di bagian ["Memakai Closure `move` dengan Thread"][move-threads]<!-- ignore --> di Bab 16, kita sering perlu memindahkan data ke dalam closure saat bekerja dengan thread. Dinamika dasar yang sama berlaku untuk blok async, jadi kata kunci `move` bekerja pada blok async sama seperti pada closure.

Di Listing 17-12, kita mengubah blok yang dipakai untuk mengirim pesan dari `async` menjadi `async move`.

<Listing number="17-12" caption="Revisi kode dari Listing 17-11 yang dimatikan dengan benar setelah selesai" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-12/src/main.rs:with-move}}
```

</Listing>

Saat kita menjalankan versi kode _ini_, ia dimatikan dengan anggun setelah pesan terakhir dikirim dan diterima. Berikutnya, mari kita lihat apa yang perlu diubah untuk mengirim data dari lebih dari satu future.

#### Menggabungkan Sejumlah Future dengan Macro `join!`

Channel async ini juga merupakan channel multiple-producer, jadi kita bisa memanggil `clone` pada `tx` jika kita ingin mengirim pesan dari beberapa future, seperti yang ditunjukkan pada Listing 17-13.

<Listing number="17-13" caption="Memakai beberapa producer dengan blok async" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-13/src/main.rs:here}}
```

</Listing>

Pertama, kita melakukan clone pada `tx`, membuat `tx1` di luar blok async pertama. Kita memindahkan `tx1` ke dalam blok itu seperti yang sebelumnya kita lakukan dengan `tx`. Lalu, kemudian, kita memindahkan `tx` yang semula ke dalam blok async _baru_, tempat kita mengirim lebih banyak pesan dengan jeda yang sedikit lebih lambat. Kebetulan kita menaruh blok async baru ini setelah blok async untuk menerima pesan, tetapi ia juga bisa ditempatkan sebelum blok itu. Kuncinya adalah urutan future-future itu di-await, bukan urutan saat ia dibuat.

Kedua blok async untuk mengirim pesan perlu menjadi blok `async move` agar baik `tx` maupun `tx1` di-drop ketika blok-blok itu selesai. Jika tidak, kita akan kembali ke loop tak hingga yang sama seperti saat kita mulai.

Terakhir, kita beralih dari `trpl::join` ke `trpl::join!` untuk menangani future tambahan itu: macro `join!` meng-await sejumlah future sembarang di mana kita mengetahui jumlah future tersebut pada waktu kompilasi. Kita akan membahas peng-awaitan sekumpulan future dengan jumlah yang tidak diketahui nanti di bab ini.

Sekarang kita melihat semua pesan dari kedua future pengirim, dan karena future-future pengirim itu memakai jeda yang sedikit berbeda setelah mengirim, pesan-pesannya juga diterima pada jeda yang berbeda-beda:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
received 'hi'
received 'more'
received 'from'
received 'the'
received 'messages'
received 'future'
received 'for'
received 'you'
```

Kita sudah menjelajahi cara memakai message passing untuk mengirim data antar future, cara kode di dalam blok async berjalan secara sekuensial, cara memindahkan ownership ke dalam blok async, dan cara menggabungkan beberapa future. Berikutnya, mari kita bahas cara dan alasan memberi tahu runtime bahwa ia bisa beralih ke task lain.

[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[join-handles]: ch16-01-threads.html#waiting-for-all-threads-to-finish
[message-passing-threads]: ch16-02-message-passing.html
[if-let]: ch06-03-if-let.html
[capture-or-move]: ch13-01-closures.html#capturing-references-or-moving-ownership
[move-threads]: ch16-01-threads.html#using-move-closures-with-threads
