<!-- Old headings. Do not remove or links may break. -->

<a id="writing-error-messages-to-standard-error-instead-of-standard-output"></a>

## Mengarahkan Error ke Standard Error

Saat ini, kita menulis seluruh output ke terminal menggunakan macro `println!`. Di sebagian besar terminal, ada dua jenis output: _standard output_ (`stdout`) untuk informasi umum dan _standard error_ (`stderr`) untuk pesan error. Pembedaan ini memungkinkan pengguna memilih untuk mengarahkan output program yang berhasil ke sebuah file, tetapi tetap menampilkan pesan error di layar.

Macro `println!` hanya bisa mencetak ke standard output, jadi kita perlu memakai sesuatu yang lain untuk mencetak ke standard error.

### Memeriksa ke Mana Error Ditulis

Pertama, mari kita lihat bagaimana konten yang dicetak oleh `minigrep` saat ini ditulis ke standard output, termasuk pesan error yang sebenarnya ingin kita tulis ke standard error. Kita akan melakukannya dengan mengarahkan aliran standard output ke sebuah file sambil sengaja memicu sebuah error. Kita tidak akan mengarahkan aliran standard error, sehingga konten apa pun yang dikirim ke standard error akan tetap tampil di layar.

Program command line seharusnya mengirim pesan error ke aliran standard error agar kita tetap bisa melihat pesan error di layar meskipun kita mengarahkan aliran standard output ke sebuah file. Program kita saat ini belum berperilaku baik: sebentar lagi kita akan melihat bahwa program justru menyimpan output pesan error ke dalam file!

Untuk mendemonstrasikan perilaku ini, kita akan menjalankan program dengan `>` dan path file _output.txt_ yang ingin kita jadikan tujuan aliran standard output. Kita tidak akan memberikan argumen apa pun, yang seharusnya memicu sebuah error:

```console
$ cargo run > output.txt
```

Sintaks `>` memberi tahu shell untuk menulis isi standard output ke _output.txt_, bukan ke layar. Kita tidak melihat pesan error yang kita harapkan tampil di layar, yang berarti pesan itu pasti berakhir di file. Begini isi _output.txt_:

```text
Problem parsing arguments: not enough arguments
```

Yup, pesan error kita dicetak ke standard output. Akan jauh lebih berguna jika pesan error seperti ini dicetak ke standard error, sehingga hanya data dari proses yang berhasil yang masuk ke file. Kita akan mengubahnya.

### Mencetak Error ke Standard Error

Kita akan memakai kode pada Listing 12-24 untuk mengubah cara pesan error dicetak. Berkat refactoring yang kita lakukan sebelumnya dalam bab ini, semua kode yang mencetak pesan error berkumpul dalam satu fungsi, `main`. Pustaka standar menyediakan macro `eprintln!` yang mencetak ke aliran standard error, jadi mari kita ubah dua tempat di mana kita memanggil `println!` untuk mencetak error agar memakai `eprintln!`.

<Listing number="12-24" file-name="src/main.rs" caption="Menulis pesan error ke standard error, bukan ke standard output, menggunakan `eprintln!`">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-24/src/main.rs:here}}
```

</Listing>

Sekarang mari kita jalankan lagi program dengan cara yang sama, tanpa argumen apa pun dan mengarahkan standard output dengan `>`:

```console
$ cargo run > output.txt
Problem parsing arguments: not enough arguments
```

Sekarang kita melihat error di layar dan _output.txt_ tidak berisi apa pun—itulah perilaku yang kita harapkan dari program command line.

Mari kita jalankan lagi program dengan argumen yang tidak memicu error, tetapi tetap mengarahkan standard output ke sebuah file, seperti ini:

```console
$ cargo run -- to poem.txt > output.txt
```

Kita tidak akan melihat output apa pun di terminal, dan _output.txt_ akan berisi hasil kita:

<span class="filename">Nama file: output.txt</span>

```text
Are you nobody, too?
How dreary to be somebody!
```

Ini menunjukkan bahwa kita kini memakai standard output untuk output yang berhasil dan standard error untuk output error, sebagaimana mestinya.

## Ringkasan

Bab ini mengulas kembali beberapa konsep utama yang sudah kamu pelajari sejauh ini dan membahas cara melakukan operasi I/O umum di Rust. Dengan memakai argumen command line, file, variabel lingkungan, dan macro `eprintln!` untuk mencetak error, kamu kini siap menulis aplikasi command line. Dipadukan dengan konsep-konsep di bab sebelumnya, kode kamu akan terstruktur dengan rapi, menyimpan data secara efektif dalam struktur data yang tepat, menangani error dengan baik, dan memiliki pengujian yang memadai.

Berikutnya, kita akan menjelajahi beberapa fitur Rust yang dipengaruhi oleh bahasa fungsional: closure dan iterator.
