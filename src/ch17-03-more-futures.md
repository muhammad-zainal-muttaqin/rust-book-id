
<!-- Old headings. Do not remove or links may break. -->

<a id="yielding"></a>

### Menyerahkan Kontrol ke Runtime

Ingat dari bagian [“Program Async Pertama Kita”][async-program]<!-- ignore --> bahwa di setiap await point, Rust memberi runtime kesempatan untuk menjeda task dan beralih ke task lain jika future yang sedang di-await belum siap. Kebalikannya juga benar: Rust _hanya_ menjeda blok async dan menyerahkan kontrol kembali ke runtime di sebuah await point. Semua yang ada di antara await point bersifat sinkron.

Itu berarti jika kamu melakukan banyak pekerjaan di dalam blok async tanpa await point, future itu akan menghalangi future lain untuk maju. Kamu kadang akan mendengar hal ini disebut sebagai satu future _starving_ future lainnya. Dalam beberapa kasus, ini mungkin bukan masalah besar. Namun, jika kamu melakukan semacam inisialisasi yang mahal atau pekerjaan yang berjalan lama, atau jika kamu punya future yang akan terus melakukan suatu task tertentu tanpa henti, kamu perlu memikirkan kapan dan di mana menyerahkan kontrol kembali ke runtime.

Mari kita simulasikan operasi yang berjalan lama untuk menggambarkan masalah starvation, lalu kita bahas cara mengatasinya. Listing 17-14 memperkenalkan fungsi `slow`.

<Listing number="17-14" caption="Menggunakan `thread::sleep` untuk menyimulasikan operasi yang lambat" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-14/src/main.rs:slow}}
```

</Listing>

Kode ini menggunakan `std::thread::sleep`, bukan `trpl::sleep`, sehingga memanggil `slow` akan memblokir thread saat ini selama sejumlah milidetik. Kita bisa memakai `slow` sebagai pengganti operasi di dunia nyata yang berjalan lama sekaligus memblokir.

Di Listing 17-15, kita memakai `slow` untuk meniru pekerjaan yang terikat CPU semacam ini pada sepasang future.

<Listing number="17-15" caption="Memanggil fungsi `slow` untuk menyimulasikan operasi yang lambat" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-15/src/main.rs:slow-futures}}
```

</Listing>

Setiap future menyerahkan kontrol kembali ke runtime hanya _setelah_ menjalankan sejumlah operasi lambat. Jika kamu menjalankan kode ini, kamu akan melihat output ini:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-15/
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'a' ran for 10ms
'a' ran for 20ms
'b' started.
'b' ran for 75ms
'b' ran for 10ms
'b' ran for 15ms
'b' ran for 350ms
'a' finished.
```

Sama seperti Listing 17-5, tempat kita memakai `trpl::select` untuk membalapkan future-future yang mengambil dua URL, `select` tetap selesai begitu `a` selesai. Namun, tidak ada selang-seling di antara pemanggilan `slow` pada kedua future itu. Future `a` melakukan seluruh pekerjaannya sampai pemanggilan `trpl::sleep` di-await, lalu future `b` melakukan seluruh pekerjaannya sampai pemanggilan `trpl::sleep`-nya sendiri di-await, dan akhirnya future `a` selesai. Agar kedua future bisa maju di antara tugas-tugas lambatnya, kita butuh await point supaya bisa menyerahkan kontrol kembali ke runtime. Artinya, kita butuh sesuatu yang bisa kita await!

Kita sudah bisa melihat semacam serah-terima ini terjadi di Listing 17-15: jika kita menghapus `trpl::sleep` di akhir future `a`, future itu akan selesai tanpa future `b` berjalan _sama sekali_. Mari kita coba memakai fungsi `trpl::sleep` sebagai titik awal untuk membiarkan operasi bergantian maju, seperti yang ditunjukkan Listing 17-16.

<Listing number="17-16" caption="Menggunakan `trpl::sleep` untuk membiarkan operasi bergantian maju" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-16/src/main.rs:here}}
```

</Listing>

Kita sudah menambahkan pemanggilan `trpl::sleep` dengan await point di antara setiap pemanggilan `slow`. Sekarang pekerjaan kedua future berselang-seling:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-16
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'b' started.
'b' ran for 75ms
'a' ran for 10ms
'b' ran for 10ms
'a' ran for 20ms
'b' ran for 15ms
'a' finished.
```

Future `a` masih berjalan sebentar sebelum menyerahkan kontrol ke `b`, karena ia memanggil `slow` sebelum sempat memanggil `trpl::sleep`, tetapi setelah itu kedua future bergantian setiap kali salah satunya mencapai await point. Dalam kasus ini, kita melakukannya setelah setiap pemanggilan `slow`, tetapi kita bisa memecah pekerjaan itu dengan cara apa pun yang paling masuk akal bagi kita.

Meski begitu, kita sebenarnya tidak ingin _tidur_ di sini: kita ingin maju secepat mungkin. Kita hanya perlu menyerahkan kontrol kembali ke runtime. Kita bisa melakukannya secara langsung dengan fungsi `trpl::yield_now`. Di Listing 17-17, kita mengganti semua pemanggilan `trpl::sleep` itu dengan `trpl::yield_now`.

<Listing number="17-17" caption="Menggunakan `yield_now` untuk membiarkan operasi bergantian maju" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-17/src/main.rs:yields}}
```

</Listing>

Kode ini lebih jelas soal niat sebenarnya dan bisa jauh lebih cepat daripada memakai `sleep`, karena timer seperti yang dipakai `sleep` sering punya batas seberapa halus granularitasnya. Versi `sleep` yang kita pakai, misalnya, selalu tidur setidaknya satu milidetik, bahkan jika kita memberinya `Duration` satu nanodetik. Sekali lagi, komputer modern itu _cepat_: mereka bisa melakukan banyak hal dalam satu milidetik!

Ini berarti async bisa berguna bahkan untuk task yang terikat komputasi, tergantung pada apa lagi yang dilakukan programmu, karena async menyediakan alat yang berguna untuk menyusun hubungan antarbagian program (meski dengan biaya overhead mesin state async). Ini adalah bentuk _cooperative multitasking_, tempat setiap future punya kuasa menentukan kapan ia menyerahkan kontrol lewat await point. Karena itu, setiap future juga punya tanggung jawab untuk tidak memblokir terlalu lama. Pada beberapa sistem operasi embedded berbasis Rust, ini adalah _satu-satunya_ jenis multitasking!

Dalam kode dunia nyata, tentu saja kamu tidak akan biasa bergantian antara pemanggilan fungsi dan await point di setiap baris. Meski menyerahkan kontrol dengan cara ini tergolong murah, hal itu tidaklah gratis. Dalam banyak kasus, mencoba memecah task yang terikat komputasi justru bisa membuatnya jauh lebih lambat, jadi kadang lebih baik bagi performa _keseluruhan_ membiarkan suatu operasi memblokir sebentar. Selalu ukur untuk melihat di mana sebenarnya bottleneck performa kodemu. Meski begitu, dinamika yang mendasari ini penting untuk diingat jika kamu _memang_ melihat banyak pekerjaan terjadi secara serial, padahal kamu mengharapkannya terjadi secara bersamaan!

### Membangun Abstraksi Async Kita Sendiri

Kita juga bisa menggabungkan future-future untuk menciptakan pola baru. Misalnya, kita bisa membangun fungsi `timeout` dari komponen dasar async yang sudah kita punya. Setelah selesai, hasilnya akan menjadi komponen dasar lain yang bisa kita pakai untuk membuat abstraksi async lagi.

Listing 17-18 menunjukkan bagaimana kita mengharapkan `timeout` ini bekerja dengan future yang lambat.

<Listing number="17-18" caption="Memakai `timeout` bayangan kita untuk menjalankan operasi lambat dengan batas waktu" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-18/src/main.rs:here}}
```

</Listing>

Mari kita terapkan ini! Untuk mulai, mari kita pikirkan API untuk `timeout`:

- Fungsi ini harus berupa fungsi async agar bisa kita await.
- Parameter pertamanya seharusnya future yang akan dijalankan. Kita bisa menjadikannya generic agar bisa bekerja dengan future apa pun.
- Parameter keduanya adalah waktu tunggu maksimum. Jika kita memakai `Duration`, itu akan memudahkan kita meneruskannya ke `trpl::sleep`.
- Fungsi ini harus mengembalikan `Result`. Jika future selesai dengan sukses, `Result`-nya akan berupa `Ok` dengan nilai yang dihasilkan future. Jika waktu habis lebih dulu, `Result`-nya akan berupa `Err` dengan durasi yang sudah ditunggu timeout.

Listing 17-19 menunjukkan deklarasi ini.

<!-- This is not tested because it intentionally does not compile. -->

<Listing number="17-19" caption="Mendefinisikan signature dari `timeout`" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-19/src/main.rs:declaration}}
```

</Listing>

Itu memenuhi tujuan kita untuk tipe-tipe tersebut. Sekarang mari kita pikirkan _perilaku_ yang kita butuhkan: kita ingin membalapkan future yang diteruskan dengan durasi itu. Kita bisa memakai `trpl::sleep` untuk membuat timer dari durasi tersebut, lalu memakai `trpl::select` untuk menjalankan timer itu bersama future yang diteruskan pemanggil.

Di Listing 17-20, kita menerapkan `timeout` dengan mencocokkan hasil dari await `trpl::select`.

<Listing number="17-20" caption="Mendefinisikan `timeout` dengan `select` dan `sleep`" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-20/src/main.rs:implementation}}
```

</Listing>

Implementasi `trpl::select` tidak adil: ia selalu melakukan poll argumen sesuai urutan saat argumen itu diteruskan (implementasi `select` lain akan memilih secara acak argumen mana yang di-poll lebih dulu). Karena itu, kita meneruskan `future_to_try` ke `select` lebih dulu agar ia punya kesempatan selesai bahkan jika `max_time` sangat singkat. Jika `future_to_try` selesai lebih dulu, `select` akan mengembalikan `Left` dengan hasil dari `future_to_try`. Jika `timer` selesai lebih dulu, `select` akan mengembalikan `Right` dengan hasil timer berupa `()`.

Jika `future_to_try` berhasil dan kita mendapat `Left(output)`, kita mengembalikan `Ok(output)`. Jika sebaliknya timer sleep habis dan kita mendapat `Right(())`, kita mengabaikan `()` dengan `_` dan mengembalikan `Err(max_time)` sebagai gantinya.

Dengan begitu, kita punya `timeout` yang berfungsi, dibangun dari dua helper async lainnya. Jika kita menjalankan kode kita, ia akan mencetak pesan kegagalan setelah timeout:

```text
Failed after 2 seconds
```

Karena future bisa digabung dengan future lain, kamu bisa membangun alat yang sangat kuat dari komponen dasar async yang lebih kecil. Misalnya, kamu bisa memakai pendekatan yang sama untuk menggabungkan timeout dengan retry, lalu memakai hasilnya untuk operasi seperti panggilan jaringan (seperti yang ada di Listing 17-5).

Dalam praktiknya, kamu biasanya akan bekerja langsung dengan `async` dan `await`, lalu secara sekunder dengan fungsi seperti `select` dan macro seperti macro `join!` untuk mengontrol cara future paling luar dijalankan.

Kita sudah melihat sejumlah cara untuk bekerja dengan banyak future secara bersamaan. Selanjutnya, kita akan melihat bagaimana kita bisa bekerja dengan banyak future secara berurutan dari waktu ke waktu memakai _streams_.

[async-program]: ch17-01-futures-and-syntax.html#our-first-async-program
