## Membaca File

Sekarang kita akan menambahkan fungsionalitas untuk membaca file yang ditentukan dalam argumen `file_path`. Pertama, kita butuh sebuah file contoh untuk mengujinya. Kita akan memakai file dengan sedikit teks dalam beberapa baris yang berisi beberapa kata yang berulang. Listing 12-3 berisi puisi Emily Dickinson yang sangat cocok! Buatlah sebuah file bernama _poem.txt_ di level root proyekmu, lalu masukkan puisi “I’m Nobody! Who are you?”

<Listing number="12-3" file-name="poem.txt" caption="Sebuah puisi karya Emily Dickinson menjadi kasus uji yang bagus.">

```text
{{#include ../listings/ch12-an-io-project/listing-12-03/poem.txt}}
```

</Listing>

Dengan teks sudah tersedia, edit _src/main.rs_ dan tambahkan kode untuk membaca file, seperti yang ditunjukkan pada Listing 12-4.

<Listing number="12-4" file-name="src/main.rs" caption="Membaca isi file yang ditentukan oleh argumen kedua">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-04/src/main.rs:here}}
```

</Listing>

Pertama, kita mengambil bagian yang relevan dari library standar dengan statement `use`: kita membutuhkan `std::fs` untuk menangani file.

Di `main`, statement baru `fs::read_to_string` menerima `file_path`, membuka file tersebut, dan mengembalikan nilai bertipe `std::io::Result<String>` yang berisi isi file.

Setelah itu, kita menambahkan lagi statement `println!` sementara yang mencetak nilai `contents` setelah file dibaca, supaya kita bisa memeriksa bahwa program berjalan dengan baik sejauh ini.

Mari jalankan kode ini dengan string apa pun sebagai argumen command line pertama (karena kita belum mengimplementasikan bagian pencarian) dan file _poem.txt_ sebagai argumen kedua:

```console
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-04/output.txt}}
```

Bagus! Kode tersebut membaca lalu mencetak isi file. Namun, kode ini punya beberapa kelemahan. Saat ini, fungsi `main` punya banyak tanggung jawab: secara umum, fungsi menjadi lebih jelas dan lebih mudah dirawat jika setiap fungsi hanya bertanggung jawab atas satu ide. Masalah lainnya adalah kita belum menangani error sebaik yang bisa kita lakukan. Programnya masih kecil, jadi kelemahan-kelemahan ini bukan masalah besar, tetapi seiring pertumbuhan program, akan lebih sulit memperbaikinya dengan rapi. Sebaiknya mulai refactor lebih awal saat mengembangkan program, karena jauh lebih mudah merefactor kode dalam jumlah kecil. Itu yang akan kita lakukan berikutnya.
