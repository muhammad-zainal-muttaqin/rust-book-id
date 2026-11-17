<!-- Old headings. Do not remove or links may break. -->

<a id="using-message-passing-to-transfer-data-between-threads"></a>

## Mentransfer Data Antar-Thread dengan Message Passing

Salah satu pendekatan yang makin populer untuk memastikan concurrency yang aman
adalah message passing, yaitu ketika thread atau aktor saling berkomunikasi dengan
cara mengirim satu sama lain pesan yang berisi data. Berikut gagasannya dalam
slogan dari [dokumentasi bahasa Go](https://golang.org/doc/effective_go.html#concurrency):
“Jangan berkomunikasi dengan berbagi memori; sebaliknya, bagikan memori dengan
berkomunikasi.”

Untuk mewujudkan concurrency dengan pengiriman pesan, pustaka standar Rust
menyediakan implementasi channel. Sebuah _channel_ adalah konsep pemrograman umum
yang dipakai untuk mengirim data dari satu thread ke thread lain.

Kamu bisa membayangkan channel dalam pemrograman seperti saluran air berarah,
misalnya sungai kecil atau sungai besar. Jika kamu melempar sesuatu seperti bebek
karet ke sungai, benda itu akan hanyut ke hilir sampai ke ujung aliran air.

Sebuah channel punya dua bagian: transmitter dan receiver. Bagian transmitter
adalah lokasi di hulu tempat kamu memasukkan bebek karet ke sungai, sedangkan
bagian receiver adalah tempat bebek karet itu berakhir di hilir. Satu bagian kode
kamu memanggil method pada transmitter dengan data yang ingin kamu kirim, dan
bagian lain memeriksa ujung penerima untuk pesan yang datang. Sebuah channel
dikatakan _closed_ jika bagian transmitter atau receiver di-drop.

Di sini, kita akan membangun program yang memiliki satu thread untuk menghasilkan
nilai dan mengirimkannya lewat channel, serta thread lain yang menerima
nilai-nilai itu dan mencetaknya. Kita akan mengirim nilai-nilai sederhana
antar-thread memakai channel untuk mengilustrasikan fitur ini. Begitu kamu
terbiasa dengan tekniknya, kamu bisa memakai channel untuk thread mana pun yang
perlu saling berkomunikasi, misalnya sistem chat atau sistem di mana banyak
thread mengerjakan bagian-bagian dari sebuah perhitungan lalu mengirim bagian itu
ke satu thread yang menggabungkan hasilnya.

Pertama, pada Listing 16-6, kita akan membuat channel tetapi belum melakukan apa
pun dengannya. Perhatikan bahwa kode ini belum akan dikompilasi karena Rust belum
bisa mengetahui tipe nilai apa yang ingin kita kirim lewat channel.

<Listing number="16-6" file-name="src/main.rs" caption="Membuat channel dan menetapkan kedua bagiannya ke `tx` dan `rx`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-06/src/main.rs}}
```

</Listing>

Kita membuat channel baru memakai fungsi `mpsc::channel`; `mpsc` adalah singkatan
dari _multiple producer, single consumer_. Singkatnya, cara pustaka standar Rust
mengimplementasikan channel berarti sebuah channel bisa punya banyak ujung
_pengirim_ yang menghasilkan nilai, tetapi hanya satu ujung _penerima_ yang
mengonsumsi nilai itu. Bayangkan beberapa sungai kecil yang mengalir bersama
menjadi satu sungai besar: Semua yang dikirim lewat sungai mana pun akan berakhir
di satu sungai pada akhirnya. Untuk sementara kita mulai dengan satu producer,
tapi kita akan menambahkan beberapa producer begitu contoh ini sudah berjalan.

Fungsi `mpsc::channel` mengembalikan sebuah tuple yang elemen pertamanya adalah
ujung pengirim—transmitter—dan elemen keduanya adalah ujung penerima—receiver.
Singkatan `tx` dan `rx` secara tradisional dipakai di banyak bidang untuk
_transmitter_ dan _receiver_, jadi kita menamai variabel kita demikian untuk
menandakan tiap ujung. Kita memakai statement `let` dengan pattern yang
mendekonstruksi tuple; kita akan membahas pemakaian pattern dalam statement `let`
dan dekonstruksi di Bab 19. Untuk sekarang, cukup ketahui bahwa memakai statement
`let` dengan cara ini adalah cara praktis untuk mengambil bagian-bagian dari tuple
yang dikembalikan oleh `mpsc::channel`.

Mari pindahkan ujung pengirim ke dalam thread yang di-spawn dan biarkan ia
mengirim satu string sehingga thread yang di-spawn itu berkomunikasi dengan thread
utama, seperti pada Listing 16-7. Ini seperti meletakkan bebek karet ke sungai di
hulu atau mengirim pesan chat dari satu thread ke thread lain.

<Listing number="16-7" file-name="src/main.rs" caption='Memindahkan `tx` ke thread yang di-spawn dan mengirim `"hi"`'>

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-07/src/main.rs}}
```

</Listing>

Sekali lagi, kita memakai `thread::spawn` untuk membuat thread baru lalu memakai
`move` untuk memindahkan `tx` ke dalam closure sehingga thread yang di-spawn itu
memiliki `tx`. Thread yang di-spawn perlu memiliki transmitter agar bisa mengirim
pesan lewat channel.

Transmitter punya method `send` yang menerima nilai yang ingin kita kirim. Method
`send` mengembalikan tipe `Result<T, E>`, jadi jika receiver sudah di-drop dan
tidak ada tempat lagi untuk mengirim nilai, operasi pengiriman akan mengembalikan
error. Pada contoh ini, kita memanggil `unwrap` untuk panic jika terjadi error.
Namun dalam aplikasi nyata, kita akan menanganinya dengan benar: Kembali ke Bab 9
untuk mengulas strategi penanganan error yang tepat.

Pada Listing 16-8, kita akan mengambil nilai dari receiver di thread utama. Ini
seperti mengambil bebek karet dari air di ujung sungai atau menerima pesan chat.

<Listing number="16-8" file-name="src/main.rs" caption='Menerima nilai `"hi"` di thread utama dan mencetaknya'>

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-08/src/main.rs}}
```

</Listing>

Receiver punya dua method yang berguna: `recv` dan `try_recv`. Kita memakai
`recv`, singkatan dari _receive_, yang akan memblokir eksekusi thread utama dan
menunggu sampai sebuah nilai dikirim lewat channel. Begitu nilai dikirim, `recv`
akan mengembalikannya dalam `Result<T, E>`. Saat transmitter ditutup, `recv` akan
mengembalikan error untuk menandakan bahwa tidak ada nilai lagi yang akan datang.

Method `try_recv` tidak memblokir, tetapi sebaliknya akan mengembalikan
`Result<T, E>` segera: nilai `Ok` yang berisi pesan jika ada pesan yang tersedia,
dan nilai `Err` jika tidak ada pesan untuk saat ini. Memakai `try_recv` berguna
jika thread ini punya pekerjaan lain sambil menunggu pesan: Kita bisa menulis loop
yang memanggil `try_recv` sesekali, menangani pesan jika ada, dan jika tidak
melakukan pekerjaan lain sebentar sampai memeriksa lagi.

Kita memakai `recv` dalam contoh ini demi kesederhanaan; kita tidak punya
pekerjaan lain untuk thread utama selain menunggu pesan, jadi memblokir thread
utama sudah tepat.

Saat kita menjalankan kode di Listing 16-8, kita akan melihat nilai yang dicetak
dari thread utama:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
```

Sempurna!

<!-- Old headings. Do not remove or links may break. -->

<a id="channels-and-ownership-transference"></a>

### Mentransfer Ownership Lewat Channel

Aturan ownership berperan penting dalam pengiriman pesan karena aturan itu
membantumu menulis kode concurrent yang aman. Mencegah error dalam pemrograman
concurrent adalah keuntungan dari memikirkan ownership di seluruh program Rust
kamu. Mari kita lakukan eksperimen untuk menunjukkan bagaimana channel dan
ownership bekerja sama mencegah masalah: Kita akan mencoba memakai nilai `val` di
thread yang di-spawn _setelah_ kita mengirimnya lewat channel. Coba kompilasi kode
di Listing 16-9 untuk melihat mengapa kode ini tidak diizinkan.

<Listing number="16-9" file-name="src/main.rs" caption="Mencoba memakai `val` setelah kita mengirimnya lewat channel">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-09/src/main.rs}}
```

</Listing>

Di sini, kita mencoba mencetak `val` setelah kita mengirimnya lewat channel melalui
`tx.send`. Mengizinkan hal itu akan menjadi ide yang buruk: Begitu nilai dikirim ke
thread lain, thread itu bisa memodifikasi atau me-drop-nya sebelum kita sempat
memakai nilai itu lagi. Bisa jadi, modifikasi dari thread lain itu menyebabkan
error atau hasil yang tidak terduga karena data yang tidak konsisten atau sudah
tidak ada. Namun, Rust memberi kita error jika kita mencoba mengompilasi kode di
Listing 16-9:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-09/output.txt}}
```

Kesalahan concurrency kita menyebabkan error saat kompilasi. Fungsi `send`
mengambil ownership parameter-nya, dan saat nilai itu di-move, receiver yang
mengambil ownership-nya. Ini mencegah kita secara tidak sengaja memakai nilai itu
lagi setelah mengirimnya; sistem ownership memeriksa bahwa semuanya baik-baik saja.

<!-- Old headings. Do not remove or links may break. -->

<a id="sending-multiple-values-and-seeing-the-receiver-waiting"></a>

### Mengirim Beberapa Nilai

Kode di Listing 16-8 berhasil dikompilasi dan dijalankan, tetapi tidak jelas
menunjukkan bahwa dua thread terpisah saling berbicara lewat channel.

Pada Listing 16-10, kita membuat beberapa perubahan yang akan membuktikan bahwa
kode di Listing 16-8 berjalan secara concurrent: Thread yang di-spawn sekarang
akan mengirim beberapa pesan dan berhenti sejenak satu detik di antara tiap
pesan.

<Listing number="16-10" file-name="src/main.rs" caption="Mengirim beberapa pesan dan berhenti sejenak di antara tiap pesan">

```rust,noplayground
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-10/src/main.rs}}
```

</Listing>

Kali ini, thread yang di-spawn punya vector string yang ingin kita kirim ke thread
utama. Kita mengiterasinya, mengirim tiap string secara terpisah, dan berhenti
sejenak di antaranya dengan memanggil fungsi `thread::sleep` dengan nilai
`Duration` satu detik.

Di thread utama, kita tidak lagi memanggil fungsi `recv` secara eksplisit:
Sebaliknya, kita memperlakukan `rx` sebagai iterator. Untuk tiap nilai yang
diterima, kita mencetaknya. Saat channel ditutup, iterasi akan berakhir.

Saat menjalankan kode di Listing 16-10, kamu akan melihat keluaran berikut dengan
jeda satu detik di antara tiap baris:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
Got: from
Got: the
Got: thread
```

Karena kita tidak punya kode yang berhenti atau menunda di loop `for` pada thread
utama, kita bisa tahu bahwa thread utama sedang menunggu menerima nilai dari
thread yang di-spawn.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-multiple-producers-by-cloning-the-transmitter"></a>

### Membuat Beberapa Producer

Sebelumnya kita menyebut bahwa `mpsc` adalah singkatan dari _multiple producer,
single consumer_. Mari kita pakai `mpsc` dan kembangkan kode di Listing 16-10 untuk
membuat beberapa thread yang semuanya mengirim nilai ke receiver yang sama. Kita
bisa melakukannya dengan meng-clone transmitter, seperti pada Listing 16-11.

<Listing number="16-11" file-name="src/main.rs" caption="Mengirim beberapa pesan dari beberapa producer">

```rust,noplayground
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-11/src/main.rs:here}}
```

</Listing>

Kali ini, sebelum membuat thread yang di-spawn pertama, kita memanggil `clone`
pada transmitter. Ini akan memberi kita transmitter baru yang bisa kita berikan
ke thread yang di-spawn pertama. Kita memberikan transmitter yang semula ke thread
yang di-spawn kedua. Dengan begitu kita punya dua thread, masing-masing mengirim
pesan berbeda ke receiver yang sama.

Saat kamu menjalankan kode, keluaran kamu akan terlihat seperti ini:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
Got: more
Got: from
Got: messages
Got: for
Got: the
Got: thread
Got: you
```

Kamu mungkin melihat nilainya dalam urutan lain, bergantung pada sistem kamu.
Inilah yang membuat concurrency itu menarik sekaligus sulit. Jika kamu
bereksperimen dengan `thread::sleep`, memberi nilai berbeda di tiap thread, setiap
kali dijalankan akan makin nondeterministik dan menghasilkan keluaran yang berbeda
setiap waktu.

Sekarang setelah kita melihat cara kerja channel, mari kita lihat metode
concurrency yang berbeda.
