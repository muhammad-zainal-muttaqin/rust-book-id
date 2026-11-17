## Menggabungkan Semuanya: Future, Task, dan Thread

Seperti yang kita lihat di [Bab 16][ch16]<!-- ignore -->, thread menyediakan satu pendekatan untuk concurrency. Di bab ini kita sudah melihat pendekatan lain: memakai async bersama future dan stream. Kalau kamu bertanya-tanya kapan harus memilih satu metode dibanding yang lain, jawabannya: tergantung! Dan dalam banyak kasus, pilihannya bukan thread _atau_ async, melainkan thread _dan_ async.

Berbagai sistem operasi sudah menyediakan model concurrency berbasis thread selama beberapa dekade, dan sebagai hasilnya banyak bahasa pemrograman mendukung model tersebut. Meski begitu, model-model ini bukannya tanpa kompromi. Di banyak sistem operasi, tiap thread memakan memori yang cukup besar. Thread juga hanya menjadi pilihan kalau sistem operasi dan perangkat kerasmu mendukungnya. Berbeda dengan komputer desktop dan seluler pada umumnya, sebagian sistem embedded bahkan tidak punya OS sama sekali, jadi mereka juga tidak punya thread.

Model async menyediakan seperangkat kompromi yang berbeda—dan pada akhirnya saling melengkapi. Dalam model async, operasi yang berjalan secara concurrent tidak memerlukan thread sendiri. Sebaliknya, operasi itu bisa berjalan di atas task, seperti saat kita memakai `trpl::spawn_task` untuk memulai pekerjaan dari fungsi sinkron di bagian stream. Sebuah task mirip dengan thread, tetapi alih-alih dikelola oleh sistem operasi, task dikelola oleh kode di level library: runtime.

Ada alasan mengapa API untuk membuat thread dan membuat task begitu mirip. Thread bertindak sebagai batas bagi sekumpulan operasi sinkron; concurrency memungkinkan _antar_ thread. Task bertindak sebagai batas bagi sekumpulan operasi _asinkron_; concurrency memungkinkan baik _antar_ maupun _di dalam_ task, karena sebuah task bisa berpindah-pindah antarfuture di dalam tubuhnya. Terakhir, future adalah unit concurrency paling kecil di Rust, dan tiap future bisa mewakili pohon dari future-future lain. Runtime—khususnya executor-nya—mengelola task, dan task mengelola future. Dengan begitu, task mirip dengan thread ringan yang dikelola runtime, dengan kemampuan tambahan yang didapat karena dikelola oleh runtime, bukan oleh sistem operasi.

Ini bukan berarti task async selalu lebih baik daripada thread (atau sebaliknya). Concurrency dengan thread dalam beberapa hal adalah model pemrograman yang lebih sederhana daripada concurrency dengan `async`. Itu bisa menjadi kekuatan sekaligus kelemahan. Thread agak bersifat "fire and forget"; mereka tidak punya padanan alami untuk future, jadi mereka begitu saja berjalan sampai selesai tanpa interupsi, kecuali oleh sistem operasi sendiri.

Ternyata thread dan task sering bekerja sama dengan sangat baik, karena task bisa (setidaknya di sebagian runtime) dipindah-pindahkan antarthread. Malah, di balik layar, runtime yang selama ini kita pakai—termasuk fungsi `spawn_blocking` dan `spawn_task`—secara default bersifat multithread! Banyak runtime memakai pendekatan yang disebut _work stealing_ untuk memindahkan task antarthread secara transparan, berdasarkan seberapa sibuk thread-thread itu saat ini, demi meningkatkan performa keseluruhan sistem. Pendekatan itu sebenarnya memerlukan thread _dan_ task, dan karenanya future juga.

Saat memikirkan metode mana yang dipakai kapan, pertimbangkan pedoman umum ini:

- Kalau pekerjaannya _sangat bisa diparalelkan_ (artinya, terikat CPU), seperti memproses sekumpulan data yang tiap bagiannya bisa diproses terpisah, thread adalah pilihan yang lebih baik.
- Kalau pekerjaannya _sangat concurrent_ (artinya, terikat I/O), seperti menangani pesan dari sejumlah sumber berbeda yang bisa datang pada interval atau laju yang berbeda-beda, async adalah pilihan yang lebih baik.

Dan kalau kamu memerlukan paralelisme sekaligus concurrency, kamu tidak harus memilih antara thread dan async. Kamu bisa memakai keduanya bersamaan dengan leluasa, membiarkan masing-masing memainkan peran yang paling cocok. Misalnya, Listing 17-25 menunjukkan contoh yang cukup umum dari perpaduan seperti ini dalam kode Rust dunia nyata.

<Listing number="17-25" caption="Mengirim pesan dengan kode blocking di dalam thread dan menunggu pesan-pesan itu di dalam blok async" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-25/src/main.rs:all}}
```

</Listing>

Kita mulai dengan membuat channel async, lalu memunculkan thread yang mengambil *ownership* sisi pengirim dari channel itu dengan kata kunci `move`. Di dalam thread, kita mengirim angka 1 sampai 10, dengan jeda satu detik di antaranya. Terakhir, kita menjalankan future yang dibuat dari blok async yang diberikan ke `trpl::block_on`, seperti yang sudah kita lakukan sepanjang bab ini. Di future itu, kita menanti pesan-pesan tersebut, sama seperti pada contoh-contoh pertukaran pesan lain yang sudah kita lihat.

Kembali ke skenario yang kita pakai untuk membuka bab ini, bayangkan menjalankan sekumpulan task pengkodean video dengan thread khusus (karena pengkodean video terikat komputasi), lalu memberi tahu UI bahwa operasi-operasi itu sudah selesai lewat channel async. Ada contoh-contoh tak terhitung dari perpaduan seperti ini dalam kasus penggunaan dunia nyata.

## Ringkasan

Ini bukan terakhir kalinya kamu berjumpa dengan concurrency dalam buku ini. Proyek di [Bab 21][ch21]<!-- ignore --> akan menerapkan konsep-konsep ini dalam situasi yang lebih realistis daripada contoh-contoh sederhana yang dibahas di sini, serta membandingkan pemecahan masalah dengan threading versus task dan future secara lebih langsung.

Apa pun pendekatan yang kamu pilih di antara semua ini, Rust memberi kamu alat-alat yang dibutuhkan untuk menulis kode concurrent yang aman dan cepat—baik untuk server web ber-throughput tinggi maupun sistem operasi embedded.

Berikutnya, kita akan membahas cara-cara idiomatik untuk memodelkan masalah dan menyusun solusi saat program Rust-mu makin besar. Selain itu, kita akan membahas bagaimana idiom-idiom Rust berkaitan dengan idiom yang mungkin sudah kamu kenal dari pemrograman berorientasi objek.

[ch16]: ch16-00-concurrency.html
[combining-futures]: ch17-03-more-futures.html#building-our-own-async-abstractions
[streams]: ch17-04-streams.html#composing-streams
[ch21]: ch21-00-final-project-a-web-server.html
