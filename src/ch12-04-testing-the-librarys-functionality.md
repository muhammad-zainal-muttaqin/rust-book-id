<!-- Old headings. Do not remove or links may break. -->
<a id="developing-the-librarys-functionality-with-test-driven-development"></a>

## Menambahkan Fungsionalitas dengan Test-Driven Development

Sekarang setelah logika pencarian di _src/lib.rs_ terpisah dari fungsi `main`, jauh lebih mudah menulis test untuk fungsionalitas inti kode kita. Kita bisa memanggil fungsi secara langsung dengan berbagai argumen dan memeriksa nilai kembalian tanpa harus memanggil binary kita dari command line.

Di bagian ini, kita akan menambahkan logika pencarian ke program `minigrep` menggunakan proses test-driven development (TDD) dengan langkah-langkah berikut:

1. Tulis test yang gagal, lalu jalankan untuk memastikan test itu gagal karena alasan yang kamu harapkan.
2. Tulis atau ubah kode secukupnya agar test baru tersebut lulus.
3. Refactor kode yang baru saja kamu tambahkan atau ubah, dan pastikan test tetap lulus.
4. Ulangi dari langkah 1!

Meski TDD hanya salah satu dari banyak cara menulis perangkat lunak, pendekatan ini bisa membantu membentuk desain kode. Menulis test sebelum menulis kode yang membuatnya lulus membantu menjaga cakupan test tetap tinggi sepanjang proses.

Kita akan menggunakan pendekatan test-driven untuk mengimplementasikan fungsionalitas yang benar-benar mencari string query dalam isi file dan menghasilkan daftar baris yang cocok dengan query. Kita akan menambahkan fungsionalitas ini dalam sebuah fungsi bernama `search`.

### Menulis Test yang Gagal

Di _src/lib.rs_, kita akan menambahkan module `tests` dengan sebuah fungsi test, seperti yang kita lakukan di [Bab 11][ch11-anatomy]<!-- ignore -->. Fungsi test ini menentukan perilaku yang kita inginkan dari fungsi `search`: fungsi itu akan menerima sebuah query dan teks yang akan dicari, lalu mengembalikan hanya baris-baris dari teks tersebut yang mengandung query. Listing 12-15 menunjukkan test ini.

<Listing number="12-15" file-name="src/lib.rs" caption="Membuat test yang gagal untuk fungsi `search` bagi fungsionalitas yang kita inginkan">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-15/src/lib.rs:here}}
```

</Listing>

Test ini mencari string `"duct"`. Teks yang kita cari terdiri dari tiga baris, dan hanya satu yang mengandung `"duct"` (perhatikan bahwa backslash setelah tanda kutip ganda di awal memberi tahu Rust untuk tidak menaruh karakter newline di awal isi string literal ini). Kita menegaskan bahwa nilai yang dikembalikan dari fungsi `search` hanya berisi baris yang kita harapkan.

Jika kita menjalankan test ini, saat ini test akan gagal karena macro `unimplemented!` melakukan panic dengan pesan “not implemented”. Sesuai prinsip TDD, kita akan mengambil langkah kecil dengan menambahkan kode secukupnya agar test tidak panic saat memanggil fungsi itu, yaitu dengan mendefinisikan fungsi `search` untuk selalu mengembalikan vector kosong, seperti ditunjukkan pada Listing 12-16. Setelah itu, test seharusnya bisa dikompilasi dan tetap gagal karena vector kosong tidak cocok dengan vector yang berisi baris `"safe, fast, productive."`.

<Listing number="12-16" file-name="src/lib.rs" caption="Mendefinisikan fungsi `search` secukupnya agar memanggilnya tidak menyebabkan panic">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-16/src/lib.rs:here}}
```

</Listing>

Sekarang mari kita bahas mengapa kita perlu mendefinisikan lifetime `'a` secara eksplisit dalam signature `search` dan menggunakan lifetime itu pada argumen `contents` serta nilai kembalian. Ingat di [Bab 10][ch10-lifetimes]<!-- ignore --> bahwa parameter lifetime menentukan lifetime argumen mana yang terhubung dengan lifetime nilai kembalian. Dalam kasus ini, kita menunjukkan bahwa vector yang dikembalikan seharusnya berisi string slice yang mereferensikan slice dari argumen `contents` (bukan dari argumen `query`).

Dengan kata lain, kita memberi tahu Rust bahwa data yang dikembalikan oleh fungsi `search` akan hidup selama data yang diberikan ke fungsi `search` melalui argumen `contents`. Ini penting! Data yang direferensikan _oleh_ sebuah slice harus tetap valid agar reference-nya valid; jika compiler mengira kita membuat string slice dari `query`, bukan dari `contents`, pemeriksaan keamanannya akan menjadi salah.

Jika kita lupa menuliskan anotasi lifetime dan mencoba mengompilasi fungsi ini, kita akan mendapatkan error ini:

```console
{{#include ../listings/ch12-an-io-project/output-only-02-missing-lifetimes/output.txt}}
```

Rust tidak bisa tahu parameter mana dari dua parameter yang kita butuhkan untuk hasil keluaran, jadi kita harus memberitahunya secara eksplisit. Perhatikan bahwa teks bantuan menyarankan penggunaan parameter lifetime yang sama untuk semua parameter dan tipe keluaran—dan saran itu salah! Karena `contents` adalah parameter yang berisi seluruh teks kita dan kita ingin mengembalikan bagian-bagian teks itu yang cocok, kita tahu bahwa `contents` adalah satu-satunya parameter yang harus dihubungkan dengan nilai kembalian menggunakan sintaks lifetime.

Bahasa pemrograman lain tidak mengharuskan kamu menghubungkan argumen dengan nilai kembalian dalam signature, tetapi praktik ini akan terasa lebih mudah seiring berjalannya waktu. Kamu bisa membandingkan contoh ini dengan contoh-contoh di bagian ["Validating References with Lifetimes"][validating-references-with-lifetimes]<!-- ignore --> di Bab 10.

### Menulis Kode agar Test Lulus

Saat ini, test kita gagal karena kita selalu mengembalikan vector kosong. Untuk memperbaikinya dan mengimplementasikan `search`, program kita perlu mengikuti langkah-langkah ini:

1. Iterasi melalui setiap baris dari isi teks.
2. Periksa apakah baris tersebut mengandung string query kita.
3. Jika iya, tambahkan ke daftar nilai yang akan kita kembalikan.
4. Jika tidak, tidak usah melakukan apa pun.
5. Kembalikan daftar hasil yang cocok.

Mari kita bahas setiap langkah, dimulai dengan iterasi melalui baris.

#### Mengiterasi Baris dengan Method `lines`

Rust punya method yang berguna untuk melakukan iterasi string baris per baris, bernama `lines`, yang bekerja seperti ditunjukkan pada Listing 12-17. Perhatikan bahwa kode ini belum bisa dikompilasi.

<Listing number="12-17" file-name="src/lib.rs" caption="Mengiterasi setiap baris dalam `contents`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-17/src/lib.rs:here}}
```

</Listing>

Method `lines` mengembalikan sebuah iterator. Kita akan membahas iterator secara mendalam di [Bab 13][ch13-iterators]<!-- ignore -->. Namun ingat bahwa kamu sudah melihat cara menggunakan iterator seperti ini di [Listing 3-5][ch3-iter]<!-- ignore -->, di mana kita menggunakan loop `for` bersama iterator untuk menjalankan beberapa kode pada setiap item dalam sebuah collection.

#### Mencari Query di Setiap Baris

Berikutnya, kita akan memeriksa apakah baris saat ini mengandung string query kita. Untungnya, string punya method bernama `contains` yang melakukan ini untuk kita! Tambahkan pemanggilan method `contains` di dalam fungsi `search`, seperti ditunjukkan pada Listing 12-18. Perhatikan bahwa kode ini masih belum bisa dikompilasi.

<Listing number="12-18" file-name="src/lib.rs" caption="Menambahkan fungsionalitas untuk melihat apakah baris mengandung string dalam `query`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-18/src/lib.rs:here}}
```

</Listing>

Saat ini, kita sedang membangun fungsionalitasnya. Agar kode bisa dikompilasi, kita perlu mengembalikan nilai dari tubuh fungsi, seperti yang sudah kita nyatakan dalam signature fungsi tersebut.

#### Menyimpan Baris yang Cocok

Untuk menyelesaikan fungsi ini, kita butuh cara menyimpan baris-baris yang cocok yang ingin kita kembalikan. Untuk itu, kita bisa membuat vector mutable sebelum loop `for` dan memanggil method `push` untuk menyimpan sebuah `line` ke dalam vector. Setelah loop `for`, kita mengembalikan vector tersebut, seperti ditunjukkan pada Listing 12-19.

<Listing number="12-19" file-name="src/lib.rs" caption="Menyimpan baris-baris yang cocok agar bisa kita kembalikan">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:here}}
```

</Listing>

Sekarang fungsi `search` seharusnya hanya mengembalikan baris-baris yang mengandung `query`, dan test kita seharusnya lulus. Mari kita jalankan test-nya:

```console
{{#include ../listings/ch12-an-io-project/listing-12-19/output.txt}}
```

Test kita lulus, jadi kita tahu fungsinya bekerja!

Pada titik ini, kita bisa mempertimbangkan peluang untuk me-refactor implementasi fungsi search sambil tetap menjaga test agar fungsionalitasnya tetap sama. Kode di dalam fungsi search sebenarnya tidak terlalu buruk, tetapi belum memanfaatkan beberapa fitur berguna dari iterator. Kita akan kembali ke contoh ini di [Bab 13][ch13-iterators]<!-- ignore -->, di mana kita akan menjelajahi iterator secara detail dan melihat cara memperbaikinya.

Sekarang seluruh program seharusnya sudah bekerja! Mari kita coba, pertama dengan sebuah kata yang seharusnya mengembalikan tepat satu baris dari puisi Emily Dickinson: _frog_.

```console
{{#include ../listings/ch12-an-io-project/no-listing-02-using-search-in-run/output.txt}}
```

Keren! Sekarang mari kita coba kata yang akan cocok dengan beberapa baris, seperti _body_:

```console
{{#include ../listings/ch12-an-io-project/output-only-03-multiple-matches/output.txt}}
```

Dan terakhir, mari kita pastikan bahwa kita tidak mendapat baris sama sekali saat mencari kata yang tidak ada di mana pun dalam puisi itu, seperti _monomorphization_:

```console
{{#include ../listings/ch12-an-io-project/output-only-04-no-matches/output.txt}}
```

Luar biasa! Kita sudah membangun versi mini kita sendiri dari sebuah tool klasik dan banyak belajar tentang cara menyusun aplikasi. Kita juga belajar sedikit tentang input dan output file, lifetime, testing, dan parsing command line.

Untuk melengkapi proyek ini, kita akan singgung singkat cara bekerja dengan environment variables dan cara mencetak ke standard error, keduanya berguna saat kamu menulis program command line.

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[ch11-anatomy]: ch11-01-writing-tests.html#the-anatomy-of-a-test-function
[ch10-lifetimes]: ch10-03-lifetime-syntax.html
[ch3-iter]: ch03-05-control-flow.html#looping-through-a-collection-with-for
[ch13-iterators]: ch13-02-iterators.html
