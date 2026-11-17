## Meningkatkan Proyek I/O Kita

Dengan pengetahuan baru tentang iterator ini, kita bisa meningkatkan proyek I/O dari Bab 12 dengan memakai iterator untuk membuat beberapa bagian kode lebih jelas dan lebih ringkas. Mari kita lihat bagaimana iterator bisa menyempurnakan implementasi fungsi `Config::build` dan fungsi `search`.

### Menghapus `clone` dengan Iterator

Di Listing 12-6, kita menambahkan kode yang mengambil slice nilai `String` dan membuat instance struct `Config` dengan mengindeks slice itu serta meng-clone nilainya, sehingga struct `Config` bisa memiliki nilai-nilai tersebut. Di Listing 13-17, kita menampilkan ulang implementasi fungsi `Config::build` seperti yang ada di Listing 12-23.

<Listing number="13-17" file-name="src/main.rs" caption="Implementasi ulang fungsi `Config::build` dari Listing 12-23">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-23-reproduced/src/main.rs:ch13}}
```

</Listing>

Saat itu, kita bilang supaya jangan khawatir tentang pemanggilan `clone` yang tidak efisien karena akan kita hapus kelak. Nah, waktunya sudah tiba!

Kita membutuhkan `clone` di sini karena parameter `args` berupa slice dengan elemen `String`, tetapi fungsi `build` tidak memiliki `args`. Untuk mengembalikan ownership sebuah instance `Config`, kita harus meng-clone nilai dari field `query` dan `file_path` pada `Config` supaya instance `Config` itu bisa memiliki nilainya sendiri.

Dengan pengetahuan baru tentang iterator, kita bisa mengubah fungsi `build` agar mengambil alih ownership sebuah iterator sebagai argumennya, alih-alih meminjam slice. Kita akan memakai kemampuan iterator menggantikan kode yang memeriksa panjang slice dan mengindeks lokasi tertentu. Ini membuat apa yang dilakukan `Config::build` lebih jelas, karena iterator-lah yang akan mengakses nilainya.

Begitu `Config::build` mengambil alih ownership iterator dan berhenti memakai operasi indeks yang meminjam, kita bisa memindahkan nilai `String` dari iterator ke dalam `Config`, alih-alih memanggil `clone` dan membuat alokasi baru.

#### Memakai Iterator yang Dikembalikan Secara Langsung

Buka file _src/main.rs_ proyek I/O kamu, yang seharusnya terlihat seperti ini:

<span class="filename">Nama file: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-24-reproduced/src/main.rs:ch13}}
```

Pertama, kita akan mengubah awal fungsi `main` yang kita punya di Listing 12-24 menjadi kode di Listing 13-18, yang kali ini memakai iterator. Kode ini belum akan terkompilasi sampai kita memperbarui `Config::build` juga.

<Listing number="13-18" file-name="src/main.rs" caption="Meneruskan nilai kembalian `env::args` ke `Config::build`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-18/src/main.rs:here}}
```

</Listing>

Fungsi `env::args` mengembalikan sebuah iterator! Alih-alih mengumpulkan nilai iterator ke dalam vector lalu meneruskan slice ke `Config::build`, sekarang kita meneruskan ownership iterator yang dikembalikan `env::args` langsung ke `Config::build`.

Selanjutnya, kita perlu memperbarui definisi `Config::build`. Mari ubah signature `Config::build` menjadi seperti di Listing 13-19. Kode ini masih belum akan terkompilasi karena kita perlu memperbarui tubuh fungsinya.

<Listing number="13-19" file-name="src/main.rs" caption="Memperbarui signature `Config::build` agar menerima iterator">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-19/src/main.rs:here}}
```

</Listing>

Dokumentasi standard library untuk fungsi `env::args` menunjukkan bahwa tipe iterator yang dikembalikannya adalah `std::env::Args`, dan tipe itu mengimplementasikan trait `Iterator` serta mengembalikan nilai `String`.

Kita sudah memperbarui signature fungsi `Config::build` sehingga parameter `args` memiliki tipe generic dengan trait bound `impl Iterator<Item = String>`, bukan `&[String]`. Penggunaan sintaks `impl Trait` yang kita bahas di bagian ["Memakai Trait sebagai Parameter"][impl-trait]<!-- ignore --> dari Bab 10 ini berarti `args` bisa berupa tipe apa pun yang mengimplementasikan trait `Iterator` dan mengembalikan item `String`.

Karena kita mengambil alih ownership `args` dan akan mengubah `args` dengan mengiterasinya, kita bisa menambahkan kata kunci `mut` pada deklarasi parameter `args` supaya bersifat mutable.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-iterator-trait-methods-instead-of-indexing"></a>

#### Memakai Metode Trait `Iterator`

Selanjutnya, kita akan memperbaiki tubuh `Config::build`. Karena `args` mengimplementasikan trait `Iterator`, kita tahu kita bisa memanggil metode `next` padanya! Listing 13-20 memperbarui kode dari Listing 12-23 agar memakai metode `next`.

<Listing number="13-20" file-name="src/main.rs" caption="Mengubah tubuh `Config::build` agar memakai metode iterator">

```rust,ignore,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-20/src/main.rs:here}}
```

</Listing>

Ingat bahwa nilai pertama dalam kembalian `env::args` adalah nama program. Kita ingin mengabaikannya dan lanjut ke nilai berikutnya, jadi pertama kita memanggil `next` dan tidak melakukan apa pun dengan nilai kembaliannya. Lalu kita memanggil `next` lagi untuk mendapatkan nilai yang akan kita masukkan ke field `query` dari `Config`. Jika `next` mengembalikan `Some`, kita memakai `match` untuk mengambil nilainya. Jika mengembalikan `None`, itu berarti argumen yang diberikan tidak cukup, dan kita kembali lebih awal dengan nilai `Err`. Kita melakukan hal yang sama untuk nilai `file_path`.

<!-- Old headings. Do not remove or links may break. -->

<a id="making-code-clearer-with-iterator-adapters"></a>

### Memperjelas Kode dengan Iterator Adapter

Kita juga bisa memanfaatkan iterator dalam fungsi `search` di proyek I/O kita, yang ditampilkan ulang di Listing 13-21 seperti yang ada di Listing 12-19.

<Listing number="13-21" file-name="src/lib.rs" caption="Implementasi fungsi `search` dari Listing 12-19">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:ch13}}
```

</Listing>

Kita bisa menulis kode ini lebih ringkas dengan memakai metode iterator adapter. Dengan begitu, kita juga bisa menghindari vector `results` perantara yang mutable. Gaya pemrograman fungsional lebih suka meminimalkan jumlah state mutable agar kode lebih jelas. Menghilangkan state mutable ini bisa membuka peluang untuk pengembangan di kemudian hari yang menjalankan pencarian secara paralel, karena kita tidak perlu mengelola akses konkuren ke vector `results`. Listing 13-22 menunjukkan perubahan ini.

<Listing number="13-22" file-name="src/lib.rs" caption="Memakai metode iterator adapter dalam implementasi fungsi `search`">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-22/src/lib.rs:here}}
```

</Listing>

Ingat bahwa tujuan fungsi `search` adalah mengembalikan semua baris dalam `contents` yang mengandung `query`. Mirip dengan contoh `filter` di Listing 13-16, kode ini memakai adapter `filter` untuk menyimpan hanya baris yang membuat `line.contains(query)` mengembalikan `true`. Lalu kita mengumpulkan baris-baris yang cocok ke vector lain dengan `collect`. Jauh lebih sederhana! Silakan lakukan perubahan yang sama untuk memakai metode iterator pada fungsi `search_case_insensitive` juga.

Untuk penyempurnaan lebih lanjut, kembalikan sebuah iterator dari fungsi `search` dengan menghapus pemanggilan `collect` dan mengubah tipe kembalian menjadi `impl Iterator<Item = &'a str>` sehingga fungsi itu menjadi sebuah iterator adapter. Perhatikan bahwa kamu juga perlu memperbarui test! Cari pada file besar memakai alat `minigrep` kamu sebelum dan sesudah perubahan ini untuk melihat perbedaan perilakunya. Sebelum perubahan ini, program tidak akan mencetak hasil apa pun sampai semua hasil terkumpul, tetapi setelah perubahan, hasil akan dicetak begitu setiap baris yang cocok ditemukan, karena loop `for` dalam fungsi `run` bisa memanfaatkan sifat malas iterator.

<!-- Old headings. Do not remove or links may break. -->

<a id="choosing-between-loops-or-iterators"></a>

### Memilih Antara Loop dan Iterator

Pertanyaan logis berikutnya adalah gaya mana yang sebaiknya kamu pilih dalam kode kamu sendiri, dan mengapa: implementasi awal di Listing 13-21 atau versi yang memakai iterator di Listing 13-22 (dengan asumsi kita mengumpulkan semua hasil sebelum mengembalikannya, bukan mengembalikan iterator). Kebanyakan programmer Rust lebih suka gaya iterator. Agak lebih sulit dipahami pada awalnya, tetapi begitu kamu terbiasa dengan berbagai iterator adapter dan cara kerjanya, iterator bisa lebih mudah dipahami. Alih-alih repot dengan berbagai bagian loop dan pembentukan vector baru, kode berfokus pada tujuan tingkat tinggi dari loop itu. Ini menyembunyikan sebagian kode yang umum, sehingga lebih mudah melihat konsep yang unik bagi kode ini, misalnya kondisi filter yang harus dipenuhi setiap elemen dalam iterator.

Tapi apakah kedua implementasi ini benar-benar setara? Pertimbangan awalnya mungkin loop yang lebih rendah levelnya akan lebih cepat. Mari kita bicara soal performa.

[impl-trait]: ch10-02-traits.html#traits-as-parameters
