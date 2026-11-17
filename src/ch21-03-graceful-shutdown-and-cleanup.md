## Graceful Shutdown dan Cleanup

Kode di Listing 21-20 merespons permintaan secara asinkron melalui thread pool, seperti yang kita rencanakan. Kita mendapat beberapa peringatan tentang field `workers`, `id`, dan `thread` yang tidak kita gunakan secara langsung—peringatan itu mengingatkan kita bahwa kita belum membersihkan apa pun. Saat kita memakai cara yang kurang elegan, <kbd>ctrl</kbd>-<kbd>C</kbd>, untuk menghentikan thread utama, semua thread lain juga langsung berhenti, bahkan jika mereka sedang melayani sebuah permintaan.

Berikutnya, kita akan mengimplementasikan trait `Drop` untuk memanggil `join` pada setiap thread di pool, agar mereka bisa menyelesaikan permintaan yang sedang dikerjakan sebelum ditutup. Setelah itu, kita akan membuat cara untuk memberi tahu thread agar berhenti menerima permintaan baru dan melakukan shutdown. Untuk melihat kode ini berjalan, kita akan memodifikasi server agar hanya menerima dua permintaan sebelum melakukan graceful shutdown pada thread pool-nya.

Satu hal yang perlu diperhatikan sepanjang proses ini: tidak ada satu pun dari perubahan ini yang memengaruhi bagian kode yang menangani eksekusi closure, jadi semua yang kita lakukan di sini akan sama saja jika kita memakai thread pool untuk sebuah async runtime.

### Mengimplementasikan Trait `Drop` pada `ThreadPool`

Mari mulai dengan mengimplementasikan `Drop` pada thread pool kita. Saat pool di-drop, semua thread kita harus di-join untuk memastikan mereka menyelesaikan pekerjaannya. Listing 21-22 menunjukkan percobaan pertama kita dalam mengimplementasikan `Drop`; kode ini belum sepenuhnya berjalan.

<Listing number="21-22" file-name="src/lib.rs" caption="Meng-join Setiap Thread Saat Thread Pool Keluar dari Scope">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-22/src/lib.rs:here}}
```

</Listing>

Pertama, kita melakukan loop melalui setiap `workers` di thread pool. Kita memakai `&mut` untuk ini karena `self` adalah mutable reference, dan kita juga perlu bisa mengubah `worker`. Untuk setiap `worker`, kita mencetak pesan yang mengatakan bahwa instance `Worker` ini sedang melakukan shutdown, lalu memanggil `join` pada thread milik instance `Worker` tersebut. Jika panggilan `join` gagal, kita memakai `unwrap` agar Rust panic dan melakukan shutdown yang tidak graceful.

Berikut error yang kita dapatkan saat mengompilasi kode ini:

```console
{{#include ../listings/ch21-web-server/listing-21-22/output.txt}}
```

Error itu memberi tahu kita bahwa kita tidak bisa memanggil `join` karena kita hanya punya borrowing mutable dari setiap `worker`, sementara `join` mengambil ownership atas argumennya. Untuk mengatasi masalah ini, kita perlu memindahkan thread keluar dari instance `Worker` yang memilikinya agar `join` bisa mengonsumsi thread tersebut. Salah satu caranya adalah mengambil pendekatan yang sama seperti di Listing 18-15. Jika `Worker` menyimpan `Option<thread::JoinHandle<()>>`, kita bisa memanggil method `take` pada `Option` itu untuk memindahkan nilai keluar dari varian `Some` dan meninggalkan varian `None` di tempatnya. Dengan kata lain, sebuah `Worker` yang sedang berjalan akan memiliki varian `Some` di `thread`, dan saat kita ingin membersihkan sebuah `Worker`, kita mengganti `Some` dengan `None` agar `Worker` itu tidak punya thread untuk dijalankan.

Namun, _satu-satunya_ saat hal ini muncul adalah ketika `Worker` di-drop. Sebagai gantinya, kita harus berurusan dengan `Option<thread::JoinHandle<()>>` di mana pun kita mengakses `worker.thread`. Rust yang idiomatik memang sering memakai `Option`, tetapi ketika kamu mendapati diri membungkus sesuatu yang kamu tahu akan selalu ada di dalam `Option` hanya sebagai jalan pintas seperti ini, ada baiknya mencari pendekatan alternatif agar kode lebih bersih dan lebih sedikit rawan error.

Dalam kasus ini, ada alternatif yang lebih baik: method `Vec::drain`. Method ini menerima parameter range untuk menentukan item mana yang akan dihapus dari vector, lalu mengembalikan iterator dari item-item tersebut. Dengan memakai sintaks range `..`, *semua* nilai di dalam vector akan dihapus.

Jadi, kita perlu memperbarui implementasi `drop` pada `ThreadPool` seperti ini:

<Listing file-name="src/lib.rs">

```rust
{{#rustdoc_include ../listings/ch21-web-server/no-listing-04-update-drop-definition/src/lib.rs:here}}
```

</Listing>

Ini mengatasi error compiler dan tidak memerlukan perubahan lain pada kode kita. Perlu dicatat bahwa karena drop bisa dipanggil saat panic, unwrap juga bisa panic dan menyebabkan double panic, yang langsung membuat program crash dan menghentikan pembersihan yang sedang berjalan. Ini tidak masalah untuk program contoh, tetapi tidak disarankan untuk kode produksi.

### Memberi Sinyal pada Thread agar Berhenti Menunggu Pekerjaan

Dengan semua perubahan yang sudah kita buat, kode kita terkompilasi tanpa peringatan apa pun. Akan tetapi, kabar buruknya, kode ini belum berfungsi seperti yang kita inginkan. Kuncinya ada pada logika di dalam closure yang dijalankan oleh thread-thread `Worker`: saat ini kita memanggil `join`, tetapi itu tidak akan mematikan thread-thread tersebut, karena mereka `loop` selamanya mencari pekerjaan. Jika kita mencoba me-drop `ThreadPool` dengan implementasi `drop` kita saat ini, thread utama akan terblokir selamanya, menunggu thread pertama selesai.

Untuk mengatasi masalah ini, kita perlu mengubah implementasi `drop` pada `ThreadPool`, lalu mengubah loop pada `Worker`.

Pertama, kita akan mengubah implementasi `drop` pada `ThreadPool` agar secara eksplisit me-drop `sender` sebelum menunggu thread-thread selesai. Listing 21-23 menunjukkan perubahan pada `ThreadPool` untuk secara eksplisit me-drop `sender`. Berbeda dengan thread, di sini kita _memang_ perlu memakai `Option` agar bisa memindahkan `sender` keluar dari `ThreadPool` dengan `Option::take`.

<Listing number="21-23" file-name="src/lib.rs" caption="Secara Eksplisit Me-drop `sender` Sebelum Meng-join Semua Thread `Worker`">

```rust,noplayground,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-23/src/lib.rs:here}}
```

</Listing>

Me-drop `sender` menutup channel, yang menandakan tidak ada lagi pesan yang akan dikirim. Saat itu terjadi, semua panggilan `recv` yang dilakukan instance-instance `Worker` di loop tak berujung akan mengembalikan error. Di Listing 21-24, kita mengubah loop `Worker` agar keluar dengan halus saat kondisi itu terjadi, yang berarti thread-thread akan selesai ketika implementasi `drop` pada `ThreadPool` memanggil `join` pada mereka.

<Listing number="21-24" file-name="src/lib.rs" caption="Secara Eksplisit Keluar dari Loop Saat `recv` Mengembalikan Error">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-24/src/lib.rs:here}}
```

</Listing>

Untuk melihat kode ini berjalan, mari ubah `main` agar hanya menerima dua permintaan sebelum melakukan graceful shutdown pada server, seperti yang ditunjukkan Listing 21-25.

<Listing number="21-25" file-name="src/main.rs" caption="Mematikan Server Setelah Melayani Dua Permintaan dengan Keluar dari Loop">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/listing-21-25/src/main.rs:here}}
```

</Listing>

Tentu kamu tidak ingin web server di dunia nyata mati setelah melayani dua permintaan saja. Kode ini hanya menunjukkan bahwa proses graceful shutdown dan pembersihan berjalan dengan baik.

Method `take` didefinisikan dalam trait `Iterator` dan membatasi iterasi paling banyak pada dua item pertama. `ThreadPool` akan keluar dari scope di akhir `main`, dan implementasi `drop` akan dijalankan.

Jalankan server dengan `cargo run` dan kirim tiga permintaan. Permintaan ketiga seharusnya mengalami error, dan di terminal kamu, kamu akan melihat keluaran seperti ini:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-25
cargo run
curl http://127.0.0.1:7878
curl http://127.0.0.1:7878
curl http://127.0.0.1:7878
third request will error because server will have shut down
copy output below
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.41s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Shutting down.
Shutting down worker 0
Worker 3 got a job; executing.
Worker 1 disconnected; shutting down.
Worker 2 disconnected; shutting down.
Worker 3 disconnected; shutting down.
Worker 0 disconnected; shutting down.
Shutting down worker 1
Shutting down worker 2
Shutting down worker 3
```

Kamu mungkin melihat urutan ID `Worker` dan pesan yang tercetak berbeda. Dari pesan-pesan itu, kita bisa melihat cara kerja kode ini: instance `Worker` 0 dan 3 mendapatkan dua permintaan pertama. Server berhenti menerima koneksi setelah koneksi kedua, dan implementasi `Drop` pada `ThreadPool` mulai dieksekusi sebelum `Worker 3` sempat memulai pekerjaannya. Me-drop `sender` memutus semua instance `Worker` dan memberi tahu mereka untuk melakukan shutdown. Setiap instance `Worker` mencetak pesan saat terputus, lalu thread pool memanggil `join` untuk menunggu setiap thread `Worker` selesai.

Perhatikan satu hal menarik dari eksekusi kali ini: `ThreadPool` me-drop `sender`, dan sebelum ada `Worker` yang menerima error, kita mencoba meng-join `Worker 0`. `Worker 0` belum mendapat error dari `recv`, sehingga thread utama terblokir, menunggu `Worker 0` selesai. Sementara itu, `Worker 3` menerima sebuah pekerjaan, lalu semua thread menerima error. Saat `Worker 0` selesai, thread utama menunggu instance `Worker` sisanya selesai. Pada titik itu, mereka semua sudah keluar dari loop masing-masing dan berhenti.

Selamat! Proyek kita sudah selesai; kita punya web server dasar yang memakai thread pool untuk merespons secara asinkron. Kita bisa melakukan graceful shutdown pada server, yang membersihkan semua thread di dalam pool.

Berikut kode lengkapnya sebagai referensi:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-07-final-code/src/main.rs}}
```

</Listing>

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-07-final-code/src/lib.rs}}
```

</Listing>

Kita masih bisa melakukan lebih banyak lagi! Jika kamu ingin terus mengembangkan proyek ini, berikut beberapa ide:

- Tambahkan lebih banyak dokumentasi pada `ThreadPool` dan method publiknya.
- Tambahkan test untuk fungsionalitas library.
- Ganti panggilan `unwrap` dengan penanganan error yang lebih tangguh.
- Pakai `ThreadPool` untuk melakukan tugas lain selain melayani permintaan web.
- Cari crate thread pool di [crates.io](https://crates.io/) dan implementasikan web server serupa dengan memakai crate itu sebagai gantinya. Lalu, bandingkan API dan ketangguhannya dengan thread pool yang kita implementasikan.

## Ringkasan

Bagus sekali! Kamu sudah sampai di akhir buku ini! Kami ingin berterima kasih karena sudah menemani kami dalam perjalanan menjelajahi Rust ini. Sekarang kamu siap membangun proyek Rust-mu sendiri dan membantu proyek orang lain. Ingatlah bahwa ada komunitas Rustacean lain yang ramah dan dengan senang hati akan membantumu menghadapi tantangan apa pun yang kamu temui dalam perjalananmu bersama Rust.
