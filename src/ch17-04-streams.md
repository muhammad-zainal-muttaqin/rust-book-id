<!-- Old headings. Do not remove or links may break. -->

<a id="streams"></a>

## Stream: Future secara Berurutan

Ingat kembali bagaimana kita memakai receiver untuk async channel kita tadi di bab ini, di bagian [“Message Passing”][17-02-messages]<!-- ignore -->. Metode `recv` yang async menghasilkan serangkaian item dari waktu ke waktu. Ini adalah contoh dari pola yang jauh lebih umum yang dikenal sebagai _stream_. Banyak konsep secara alami bisa digambarkan sebagai stream: item yang tersedia secara bertahap dalam antrean, potongan data yang diambil sedikit demi sedikit dari filesystem ketika keseluruhan data terlalu besar untuk memori komputer, atau data yang datang lewat jaringan dari waktu ke waktu. Karena stream adalah future, kita bisa memakainya bersama jenis future lain dan menggabungkannya dengan cara yang menarik. Misalnya, kita bisa mengumpulkan beberapa event menjadi satu batch agar tidak memicu terlalu banyak panggilan jaringan, memasang timeout pada rangkaian operasi yang berjalan lama, atau membatasi event antarmuka pengguna supaya tidak melakukan pekerjaan yang tidak perlu.

Kita sudah melihat serangkaian item di Bab 13, ketika membahas trait Iterator di bagian [“The Iterator Trait and the `next` Method”][iterator-trait]<!-- ignore -->, tetapi ada dua perbedaan antara iterator dan receiver channel async. Perbedaan pertama adalah waktu: iterator bersifat sinkron, sementara receiver channel bersifat asinkron. Perbedaan kedua adalah API-nya. Saat bekerja langsung dengan `Iterator`, kita memanggil metode `next`-nya yang sinkron. Dengan stream `trpl::Receiver`, kita justru memanggil metode `recv` yang asinkron. Selain itu, kedua API ini terasa sangat mirip, dan kemiripan itu bukan kebetulan. Stream ibarat bentuk async dari iterasi. Akan tetapi, jika `trpl::Receiver` secara khusus menunggu pesan, API stream yang umum jauh lebih luas: ia menyediakan item berikutnya seperti yang dilakukan `Iterator`, tetapi secara asinkron.

Kemiripan antara iterator dan stream di Rust berarti kita sebenarnya bisa membuat stream dari iterator mana pun. Sama seperti iterator, kita bisa bekerja dengan stream dengan memanggil metode `next`-nya lalu menunggu (await) hasilnya, seperti pada Listing 17-21, yang belum akan terkompilasi.

<Listing number="17-21" caption="Membuat stream dari iterator dan mencetak nilainya" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-21/src/main.rs:stream}}
```

</Listing>

Kita mulai dengan array angka, yang kita ubah menjadi iterator lalu kita panggil `map`-nya untuk menggandakan semua nilai. Setelah itu kita ubah iterator tersebut menjadi stream memakai fungsi `trpl::stream_from_iter`. Berikutnya, kita melakukan loop atas item-item di stream dengan loop `while let` selagi item itu datang.

Sayangnya, ketika kita mencoba menjalankan kode tersebut, kode itu tidak terkompilasi. Sebaliknya, compiler melaporkan bahwa tidak ada metode `next` yang tersedia:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-21
cargo build
copy only the error output
-->

```text
error[E0599]: no method named `next` found for struct `tokio_stream::iter::Iter` in the current scope
  --> src/main.rs:10:40
   |
10 |         while let Some(value) = stream.next().await {
   |                                        ^^^^
   |
   = help: items from traits can only be used if the trait is in scope
help: the following traits which provide `next` are implemented but not in scope; perhaps you want to import one of them
   |
1  + use crate::trpl::StreamExt;
   |
1  + use futures_util::stream::stream::StreamExt;
   |
1  + use std::iter::Iterator;
   |
1  + use std::str::pattern::Searcher;
   |
help: there is a method `try_next` with a similar name
   |
10 |         while let Some(value) = stream.try_next().await {
   |                                        ~~~~~~~~
```

Seperti yang dijelaskan keluaran ini, penyebab error compiler adalah kita memerlukan trait yang tepat di dalam scope agar bisa memakai metode `next`. Melihat pembahasan sejauh ini, kamu mungkin wajar mengira trait itu adalah `Stream`, tetapi ternyata `StreamExt`. Kependekan dari _extension_, `Ext` adalah pola umum di komunitas Rust untuk memperluas sebuah trait dengan trait lain.

Trait `Stream` mendefinisikan antarmuka tingkat rendah yang pada dasarnya menggabungkan trait `Iterator` dan `Future`. `StreamExt` menyediakan sekumpulan API tingkat tinggi di atas `Stream`, termasuk metode `next` serta metode utilitas lain yang mirip dengan yang disediakan trait `Iterator`. `Stream` dan `StreamExt` belum menjadi bagian dari pustaka standar Rust, tetapi sebagian besar crate ekosistem memakai definisi yang serupa.

Perbaikan untuk error compiler ini adalah menambahkan pernyataan `use` untuk `trpl::StreamExt`, seperti pada Listing 17-22.

<Listing number="17-22" caption="Berhasil memakai iterator sebagai dasar stream" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-22/src/main.rs:all}}
```

</Listing>

Dengan semua bagian yang sudah digabungkan, kode ini bekerja seperti yang kita inginkan! Lebih dari itu, sekarang setelah `StreamExt` ada di dalam scope, kita bisa memakai semua metode utilitasnya, sama seperti saat memakai iterator.

[17-02-messages]: ch17-02-concurrency-with-async.html#message-passing
[iterator-trait]: ch13-02-iterators.html#the-iterator-trait-and-the-next-method
