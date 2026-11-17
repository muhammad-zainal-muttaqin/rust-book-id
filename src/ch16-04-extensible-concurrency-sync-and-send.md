<!-- Old headings. Do not remove or links may break. -->

<a id="extensible-concurrency-with-the-sync-and-send-traits"></a>
<a id="extensible-concurrency-with-the-send-and-sync-traits"></a>

## Concurrency yang Dapat Dikembangkan dengan `Send` dan `Sync`

Menariknya, hampir setiap fitur concurrency yang sudah kita bahas sejauh ini di
bab ini merupakan bagian dari standard library, bukan dari bahasa itu sendiri.
Pilihan kita untuk menangani concurrency tidak terbatas pada bahasa atau
standard library; kita bisa menulis fitur concurrency sendiri atau memakai yang
ditulis orang lain.

Namun, beberapa konsep concurrency utama justru tertanam dalam bahasa, bukan di
standard library—yaitu trait `std::marker` `Send` dan `Sync`.

<!-- Old headings. Do not remove or links may break. -->

<a id="allowing-transference-of-ownership-between-threads-with-send"></a>

### Memindahkan Ownership Antar-Thread

Trait marker `Send` menandakan bahwa ownership atas nilai dari tipe yang
mengimplementasikan `Send` bisa dipindahkan antar-thread. Hampir setiap tipe
Rust mengimplementasikan `Send`, tetapi ada beberapa pengecualian, termasuk
`Rc<T>`: tipe ini tidak bisa mengimplementasikan `Send` karena jika kamu
meng-clone nilai `Rc<T>` lalu mencoba memindahkan ownership clone itu ke thread
lain, kedua thread bisa memperbarui reference count pada saat yang sama. Karena
alasan ini, `Rc<T>` diimplementasikan untuk dipakai dalam situasi single-threaded
di mana kamu tidak ingin membayar biaya performa demi thread safety.

Dengan demikian, sistem tipe dan trait bound Rust memastikan kamu tidak pernah
bisa mengirim nilai `Rc<T>` lintas thread secara tidak aman. Saat kita mencoba
melakukan ini di Listing 16-14, kita mendapat error `` the trait `Send` is not implemented for `Rc<Mutex<i32>>` ``. Saat kita beralih ke `Arc<T>`, yang memang
mengimplementasikan `Send`, kode tersebut berhasil dikompilasi.

Tipe apa pun yang seluruhnya terdiri dari tipe-tipe `Send` juga otomatis
ditandai sebagai `Send`. Hampir semua tipe primitif adalah `Send`, kecuali raw
pointer, yang akan kita bahas di Bab 20.

<!-- Old headings. Do not remove or links may break. -->

<a id="allowing-access-from-multiple-threads-with-sync"></a>

### Mengakses dari Beberapa Thread

Trait marker `Sync` menandakan bahwa aman bagi tipe yang mengimplementasikan
`Sync` untuk di-reference dari beberapa thread. Dengan kata lain, tipe `T` apa
pun mengimplementasikan `Sync` jika `&T` (reference immutable ke `T`)
mengimplementasikan `Send`, yang berarti reference itu bisa dikirim dengan aman
ke thread lain. Sama seperti `Send`, semua tipe primitif mengimplementasikan
`Sync`, dan tipe yang seluruhnya terdiri dari tipe-tipe yang mengimplementasikan
`Sync` juga mengimplementasikan `Sync`.

Smart pointer `Rc<T>` juga tidak mengimplementasikan `Sync` karena alasan yang
sama dengan mengapa ia tidak mengimplementasikan `Send`. Tipe `RefCell<T>` (yang
kita bahas di Bab 15) dan keluarga tipe `Cell<T>` terkait tidak mengimplementasikan
`Sync`. Implementasi borrow checking yang dilakukan `RefCell<T>` saat runtime
tidaklah thread-safe. Smart pointer `Mutex<T>` mengimplementasikan `Sync` dan
bisa dipakai untuk berbagi akses dengan beberapa thread, seperti yang kamu lihat
di [“Akses Bersama ke `Mutex<T>`”][shared-access]<!-- ignore -->.

### Mengimplementasikan `Send` dan `Sync` Secara Manual Itu Unsafe

Karena tipe yang seluruhnya terdiri dari tipe-tipe lain yang mengimplementasikan
trait `Send` dan `Sync` juga otomatis mengimplementasikan `Send` dan `Sync`, kita
tidak perlu mengimplementasikan trait itu secara manual. Sebagai marker trait,
keduanya bahkan tidak punya metode yang perlu diimplementasikan. Keduanya hanya
berguna untuk menegakkan invariant yang terkait dengan concurrency.

Mengimplementasikan trait ini secara manual berarti menulis kode Rust unsafe.
Kita akan membahas penggunaan kode Rust unsafe di Bab 20; untuk sekarang, yang
penting adalah membangun tipe concurrency baru yang tidak tersusun dari
bagian-bagian `Send` dan `Sync` memerlukan pertimbangan matang untuk menjaga
jaminan keamanan. [“The Rustonomicon”][nomicon] punya informasi lebih lanjut
tentang jaminan ini dan cara menjaganya.

## Ringkasan

Ini bukan terakhir kalinya kamu berjumpa dengan concurrency di buku ini: bab
berikutnya berfokus pada pemrograman async, dan proyek di Bab 21 akan memakai
konsep-konsep dari bab ini dalam situasi yang lebih realistis daripada
contoh-contoh kecil yang dibahas di sini.

Seperti yang sudah disebut sebelumnya, karena sangat sedikit dari cara Rust
menangani concurrency yang merupakan bagian dari bahasa, banyak solusi
concurrency diimplementasikan sebagai crate. Crate-crate ini berkembang lebih
cepat daripada standard library, jadi pastikan untuk mencari secara online
crate terbaru dan tercanggih yang bisa dipakai dalam situasi multithreaded.

Standard library Rust menyediakan channel untuk message passing dan tipe smart
pointer seperti `Mutex<T>` dan `Arc<T>` yang aman dipakai dalam konteks
concurrency. Sistem tipe dan borrow checker memastikan kode yang memakai
solusi-solusi ini tidak akan berujung pada data race atau reference yang tidak
valid. Begitu kode kamu berhasil dikompilasi, kamu bisa yakin bahwa kode itu
akan berjalan dengan senang di beberapa thread tanpa bug yang sulit dilacak
seperti yang umum terjadi di bahasa lain. Pemrograman concurrency bukan lagi
konsep yang perlu ditakuti: silakan buat program kamu mendukung concurrency
tanpa rasa takut!

[shared-access]: ch16-03-shared-state.html#shared-access-to-mutext
[nomicon]: ../nomicon/index.html
