## Unsafe Rust

Semua kode yang sudah kita bahas sejauh ini memberlakukan jaminan keamanan memori Rust saat kompilasi. Namun, Rust punya bahasa kedua yang tersembunyi di dalamnya dan tidak memberlakukan jaminan keamanan memori itu: bahasa itu disebut _unsafe Rust_ dan bekerja seperti Rust biasa, tetapi memberi kita kekuatan ekstra.

Unsafe Rust ada karena analisis statis pada dasarnya bersifat konservatif. Saat compiler mencoba menentukan apakah kode memenuhi jaminan tersebut, lebih baik ia menolak beberapa program yang valid daripada menerima program yang tidak valid. Meski kodenya _mungkin_ saja aman, jika compiler Rust tidak punya cukup informasi untuk yakin, ia akan menolak kode itu. Dalam kasus seperti ini, kamu bisa memakai kode unsafe untuk memberitahu compiler, “Percayalah, aku tahu apa yang kulakukan.” Perlu diingat, kamu memakai unsafe Rust dengan risiko sendiri: Jika kamu memakai kode unsafe secara keliru, masalah bisa muncul akibat ketidakamanan memori, seperti dereferensi null pointer.

Alasan lain Rust punya sisi unsafe adalah perangkat keras komputer pada dasarnya memang tidak aman. Jika Rust tidak mengizinkanmu melakukan operasi unsafe, kamu tidak bisa menyelesaikan beberapa tugas. Rust perlu mengizinkanmu melakukan pemrograman sistem tingkat rendah, seperti berinteraksi langsung dengan sistem operasi atau bahkan menulis sistem operasimu sendiri. Pemrograman sistem tingkat rendah adalah salah satu tujuan bahasa ini. Mari kita jelajahi apa yang bisa kita lakukan dengan unsafe Rust dan caranya.

<!-- Old headings. Do not remove or links may break. -->

<a id="unsafe-superpowers"></a>

### Melakukan Kekuatan Super Unsafe

Untuk beralih ke unsafe Rust, pakai keyword `unsafe`, lalu buat blok baru yang berisi kode unsafe. Ada lima tindakan yang bisa kamu lakukan di unsafe Rust tetapi tidak di safe Rust; kita menyebutnya _unsafe superpowers_. Kekuatan itu mencakup kemampuan untuk:

1. Mendereferensikan raw pointer.
1. Memanggil fungsi atau method unsafe.
1. Mengakses atau mengubah variabel static yang mutable.
1. Mengimplementasikan trait unsafe.
1. Mengakses field dari `union`s.

Penting untuk dipahami bahwa `unsafe` tidak mematikan borrow checker atau menonaktifkan pemeriksaan keamanan lain di Rust: Jika kamu memakai reference dalam kode unsafe, reference itu tetap diperiksa. Keyword `unsafe` hanya memberi kamu akses ke lima fitur ini, yang kemudian tidak diperiksa compiler dari sisi keamanan memori. Kamu tetap mendapatkan sebagian keamanan di dalam blok unsafe.

Selain itu, `unsafe` tidak berarti kode di dalam blok itu pasti berbahaya atau pasti punya masalah keamanan memori: Maksudnya, sebagai programmer, kamu yang memastikan kode di dalam blok `unsafe` mengakses memori dengan cara yang valid.

Manusia bisa salah dan kesalahan pasti terjadi, tetapi dengan mewajibkan kelima operasi unsafe ini berada di dalam blok yang ditandai `unsafe`, kamu tahu bahwa error apa pun yang terkait keamanan memori pasti ada di dalam blok `unsafe`. Jaga agar blok `unsafe` tetap kecil; kamu akan bersyukur nanti saat menyelidiki bug memori.

Untuk mengisolasi kode unsafe sebisa mungkin, sebaiknya bungkus kode seperti itu dalam abstraksi aman dan sediakan API yang aman; kita akan membahasnya nanti di bab ini saat meninjau fungsi dan method unsafe. Sebagian dari standard library diimplementasikan sebagai abstraksi aman di atas kode unsafe yang sudah diaudit. Membungkus kode unsafe dalam abstraksi aman mencegah pemakaian `unsafe` bocor ke semua tempat yang mungkin dipakai oleh kamu atau penggunamu untuk memakai fungsionalitas yang diimplementasikan dengan kode `unsafe`, karena memakai abstraksi aman itu aman.

Mari kita bahas satu per satu kelima kekuatan super unsafe itu. Kita juga akan melihat beberapa abstraksi yang menyediakan antarmuka aman untuk kode unsafe.

### Mendereferensikan Raw Pointer

Di Bab 4, di bagian [“Reference yang Menggantung”][dangling-references]<!-- ignore -->, kita menyebutkan bahwa compiler memastikan reference selalu valid. Unsafe Rust punya dua tipe baru bernama _raw pointers_ yang mirip dengan reference. Seperti reference, raw pointer bisa immutable atau mutable dan ditulis sebagai `*const T` dan `*mut T`. Tanda bintang itu bukan operator dereferensi; ia bagian dari nama tipe. Dalam konteks raw pointer, _immutable_ berarti pointer itu tidak bisa ditetapkan langsung setelah didereferensikan.

Berbeda dengan reference dan smart pointer, raw pointer:

- Boleh mengabaikan aturan borrowing dengan memiliki pointer immutable dan mutable sekaligus, atau beberapa pointer mutable ke lokasi yang sama
- Tidak dijamin menunjuk ke memori yang valid
- Boleh bernilai null
- Tidak menerapkan pembersihan otomatis apa pun

Dengan memilih untuk tidak memberlakukan jaminan ini, kamu bisa melepaskan keamanan yang dijamin demi performa yang lebih tinggi atau kemampuan berantarmuka dengan bahasa atau perangkat keras lain yang tidak tunduk pada jaminan Rust.

Listing 20-1 menunjukkan cara membuat raw pointer yang immutable dan yang mutable.

<Listing number="20-1" caption="Membuat raw pointer dengan operator peminjaman raw">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-01/src/main.rs:here}}
```

</Listing>

Perhatikan bahwa kita tidak menyertakan keyword `unsafe` di kode ini. Kita bisa membuat raw pointer dalam kode aman; kita hanya tidak bisa mendereferensikannya di luar blok unsafe, seperti yang akan kamu lihat sebentar lagi.

Kita membuat raw pointer dengan operator peminjaman raw: `&raw const num` membuat raw pointer immutable `*const i32`, dan `&raw mut num` membuat raw pointer mutable `*mut i32`. Karena kita membuatnya langsung dari variabel lokal, kita tahu raw pointer khusus ini valid, tetapi kita tidak bisa menganggap hal yang sama untuk raw pointer sembarang.

Untuk menunjukkan hal itu, berikutnya kita akan membuat raw pointer yang validitasnya tidak bisa kita pastikan, dengan memakai keyword `as` untuk mengubah nilai alih-alih memakai operator peminjaman raw. Listing 20-2 menunjukkan cara membuat raw pointer ke lokasi sembarang di memori. Mencoba memakai memori sembarang adalah perilaku yang tidak terdefinisi: Mungkin ada data di alamat itu atau mungkin tidak, compiler bisa mengoptimasi kode sehingga tidak ada akses memori, atau program bisa berhenti dengan segmentation fault. Biasanya, tidak ada alasan bagus untuk menulis kode seperti ini, terutama dalam kasus di mana kamu bisa memakai operator peminjaman raw, tetapi hal itu memang memungkinkan.

<Listing number="20-2" caption="Membuat raw pointer ke alamat memori sembarang">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-02/src/main.rs:here}}
```

</Listing>

Ingat bahwa kita bisa membuat raw pointer dalam kode aman, tetapi kita tidak bisa mendereferensikannya dan membaca data yang ditunjuknya. Di Listing 20-3, kita memakai operator dereferensi `*` pada raw pointer yang membutuhkan blok `unsafe`.

<Listing number="20-3" caption="Mendereferensikan raw pointer di dalam blok `unsafe`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-03/src/main.rs:here}}
```

</Listing>

Membuat pointer tidak menimbulkan masalah; masalah muncul hanya saat kita mencoba mengakses nilai yang ditunjuknya, yang bisa membuat kita berhadapan dengan nilai yang tidak valid.

Perhatikan juga bahwa di Listing 20-1 dan 20-3, kita membuat raw pointer `*const i32` dan `*mut i32` yang keduanya menunjuk ke lokasi memori yang sama, tempat `num` disimpan. Jika kita mencoba membuat reference immutable dan mutable ke `num`, kode itu tidak akan dikompilasi karena aturan _ownership_ Rust tidak mengizinkan reference mutable bersamaan dengan reference immutable mana pun. Dengan raw pointer, kita bisa membuat pointer mutable dan pointer immutable ke lokasi yang sama serta mengubah data melalui pointer mutable, yang berpotensi menciptakan data race. Hati-hati!

Dengan semua bahaya ini, mengapa kamu harus memakai raw pointer? Salah satu kasus penggunaan utamanya adalah saat berantarmuka dengan kode C, seperti yang akan kamu lihat di bagian berikutnya. Kasus lain adalah saat membangun abstraksi aman yang tidak dipahami borrow checker. Kita akan memperkenalkan fungsi unsafe, lalu melihat contoh abstraksi aman yang memakai kode unsafe.

### Memanggil Fungsi atau Method Unsafe

Jenis operasi kedua yang bisa kamu lakukan dalam blok unsafe adalah memanggil fungsi unsafe. Fungsi dan method unsafe tampak persis seperti fungsi dan method biasa, tetapi ada tambahan `unsafe` sebelum bagian definisi lainnya. Keyword `unsafe` di sini menunjukkan bahwa fungsi itu punya syarat yang harus kita penuhi saat memanggilnya, karena Rust tidak bisa menjamin kita sudah memenuhinya. Dengan memanggil fungsi unsafe di dalam blok `unsafe`, kita menyatakan bahwa kita sudah membaca dokumentasi fungsi itu dan kita bertanggung jawab memenuhi kontraknya.

Berikut adalah fungsi unsafe bernama `dangerous` yang tidak melakukan apa pun di dalam tubuhnya:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-01-unsafe-fn/src/main.rs:here}}
```

Kita harus memanggil fungsi `dangerous` di dalam blok `unsafe` tersendiri. Jika kita mencoba memanggil `dangerous` tanpa blok `unsafe`, kita akan mendapat error:

```console
{{#include ../listings/ch20-advanced-features/output-only-01-missing-unsafe/output.txt}}
```

Dengan blok `unsafe`, kita menyatakan kepada Rust bahwa kita sudah membaca dokumentasi fungsi itu, memahami cara memakainya dengan benar, dan sudah memverifikasi bahwa kita memenuhi kontrak fungsi tersebut.

Untuk melakukan operasi unsafe di dalam tubuh fungsi `unsafe`, kamu tetap perlu memakai blok `unsafe`, sama seperti di fungsi biasa, dan compiler akan memberi peringatan jika kamu lupa. Ini membantu kita menjaga blok `unsafe` tetap sekecil mungkin, karena operasi unsafe mungkin tidak diperlukan di seluruh tubuh fungsi.

#### Membuat Abstraksi Aman di Atas Kode Unsafe

Hanya karena sebuah fungsi berisi kode unsafe bukan berarti kita harus menandai seluruh fungsi itu sebagai unsafe. Faktanya, membungkus kode unsafe dalam fungsi aman adalah abstraksi yang umum. Sebagai contoh, mari kita pelajari fungsi `split_at_mut` dari standard library yang membutuhkan sedikit kode unsafe. Kita akan menjelajahi bagaimana kita bisa mengimplementasikannya. Method aman ini didefinisikan pada slice mutable: Method ini mengambil satu slice dan menjadikannya dua dengan membelah slice pada indeks yang diberikan sebagai argumen. Listing 20-4 menunjukkan cara memakai `split_at_mut`.

<Listing number="20-4" caption="Memakai fungsi aman `split_at_mut`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-04/src/main.rs:here}}
```

</Listing>

Kita tidak bisa mengimplementasikan fungsi ini hanya dengan safe Rust. Percobaan mungkin terlihat seperti Listing 20-5, yang tidak akan dikompilasi. Untuk menyederhanakan, kita akan mengimplementasikan `split_at_mut` sebagai fungsi, bukan method, dan hanya untuk slice bernilai `i32`, bukan untuk tipe generic `T`.

<Listing number="20-5" caption="Percobaan implementasi `split_at_mut` hanya dengan safe Rust">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-05/src/main.rs:here}}
```

</Listing>

Fungsi ini pertama-tama mengambil panjang total slice. Lalu, fungsi itu menegaskan bahwa indeks yang diberikan sebagai parameter masih berada di dalam slice dengan memeriksa apakah indeks itu kurang dari atau sama dengan panjangnya. Penegasan itu berarti jika kita memberikan indeks yang lebih besar dari panjang untuk membelah slice, fungsi akan panic sebelum mencoba memakai indeks tersebut.

Kemudian, kita mengembalikan dua slice mutable dalam sebuah tuple: satu dari awal slice asli hingga indeks `mid`, dan satu lagi dari `mid` hingga akhir slice.

Saat kita mencoba mengompilasi kode di Listing 20-5, kita akan mendapat error:

```console
{{#include ../listings/ch20-advanced-features/listing-20-05/output.txt}}
```

Borrow checker Rust tidak bisa memahami bahwa kita meminjam bagian-bagian yang berbeda dari slice; ia hanya tahu bahwa kita meminjam dari slice yang sama dua kali. Meminjam bagian yang berbeda dari sebuah slice pada dasarnya tidak masalah karena kedua slice itu tidak tumpang tindih, tetapi Rust tidak cukup pintar untuk mengetahui hal itu. Saat kita tahu kode itu aman tetapi Rust tidak tahu, inilah waktunya beralih ke kode unsafe.

Listing 20-6 menunjukkan cara memakai blok `unsafe`, raw pointer, dan beberapa panggilan ke fungsi unsafe agar implementasi `split_at_mut` berhasil.

<Listing number="20-6" caption="Memakai kode unsafe dalam implementasi fungsi `split_at_mut`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-06/src/main.rs:here}}
```

</Listing>

Ingat dari bagian [“Tipe Slice”][the-slice-type]<!-- ignore --> di Bab 4 bahwa slice adalah pointer ke beberapa data beserta panjang slice itu. Kita memakai method `len` untuk mendapatkan panjang slice dan method `as_mut_ptr` untuk mengakses raw pointer dari slice. Dalam kasus ini, karena kita punya slice mutable bernilai `i32`, `as_mut_ptr` mengembalikan raw pointer bertipe `*mut i32`, yang kita simpan dalam variabel `ptr`.

Kita tetap mempertahankan penegasan bahwa indeks `mid` berada di dalam slice. Lalu, kita sampai ke kode unsafe: Fungsi `slice::from_raw_parts_mut` menerima raw pointer dan panjang, lalu membuat slice. Kita memakai fungsi itu untuk membuat slice yang dimulai dari `ptr` dan panjangnya `mid` item. Kemudian, kita memanggil method `add` pada `ptr` dengan `mid` sebagai argumen untuk mendapatkan raw pointer yang dimulai di `mid`, lalu kita membuat slice memakai pointer itu dan jumlah item yang tersisa setelah `mid` sebagai panjangnya.

Fungsi `slice::from_raw_parts_mut` bersifat unsafe karena menerima raw pointer dan harus mempercayai bahwa pointer itu valid. Method `add` pada raw pointer juga unsafe karena harus mempercayai bahwa lokasi hasil offset juga merupakan pointer yang valid. Oleh karena itu, kita harus menaruh blok `unsafe` di sekitar panggilan ke `slice::from_raw_parts_mut` dan `add` agar bisa memanggil keduanya. Dengan melihat kode dan menambahkan penegasan bahwa `mid` harus kurang dari atau sama dengan `len`, kita bisa memastikan bahwa semua raw pointer yang dipakai di dalam blok `unsafe` adalah pointer yang valid ke data di dalam slice. Ini adalah penggunaan `unsafe` yang dapat diterima dan tepat.

Perhatikan bahwa kita tidak perlu menandai fungsi `split_at_mut` yang dihasilkan sebagai `unsafe`, dan kita bisa memanggil fungsi ini dari safe Rust. Kita telah membuat abstraksi aman atas kode unsafe dengan implementasi fungsi yang memakai kode `unsafe` secara aman, karena fungsi itu hanya membuat pointer yang valid dari data yang bisa diaksesnya.

Sebaliknya, pemakaian `slice::from_raw_parts_mut` di Listing 20-7 kemungkinan besar akan menyebabkan crash saat slice itu dipakai. Kode ini mengambil lokasi memori sembarang dan membuat slice sepanjang 10.000 item.

<Listing number="20-7" caption="Membuat slice dari lokasi memori sembarang">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-07/src/main.rs:here}}
```

</Listing>

Kita tidak memiliki memori di lokasi sembarang ini, dan tidak ada jaminan bahwa slice yang dibuat kode ini berisi nilai `i32` yang valid. Mencoba memakai `values` seolah-olah itu slice yang valid menghasilkan perilaku yang tidak terdefinisi.

#### Memakai Fungsi `extern` untuk Memanggil Kode Eksternal

Kadang kode Rust kamu perlu berinteraksi dengan kode yang ditulis dalam bahasa lain. Untuk itu, Rust punya keyword `extern` yang memudahkan pembuatan dan pemakaian _Foreign Function Interface (FFI)_, yaitu cara bagi sebuah bahasa pemrograman untuk mendefinisikan fungsi dan memungkinkan bahasa pemrograman lain (asing) memanggil fungsi-fungsi itu.

Listing 20-8 menunjukkan cara menyiapkan integrasi dengan fungsi `abs` dari standard library C. Fungsi yang dideklarasikan di dalam blok `extern` umumnya tidak aman dipanggil dari kode Rust, sehingga blok `extern` juga harus ditandai `unsafe`. Alasannya, bahasa lain tidak memberlakukan aturan dan jaminan Rust, dan Rust tidak bisa memeriksanya, jadi tanggung jawab memastikan keamanan jatuh ke programmer.

<Listing number="20-8" file-name="src/main.rs" caption="Mendeklarasikan dan memanggil fungsi `extern` yang didefinisikan dalam bahasa lain">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-08/src/main.rs}}
```

</Listing>

Di dalam blok `unsafe extern "C"`, kita mencantumkan nama dan signature fungsi eksternal dari bahasa lain yang ingin kita panggil. Bagian `"C"` menentukan _application binary interface (ABI)_ yang dipakai fungsi eksternal itu: ABI mendefinisikan cara memanggil fungsi tersebut di level assembly. ABI `"C"` adalah yang paling umum dan mengikuti ABI bahasa pemrograman C. Informasi tentang semua ABI yang didukung Rust tersedia di [Rust Reference][ABI].

Setiap item yang dideklarasikan di dalam blok `unsafe extern` secara implisit bersifat unsafe. Namun, beberapa fungsi FFI *memang* aman dipanggil. Misalnya, fungsi `abs` dari standard library C tidak punya pertimbangan keamanan memori, dan kita tahu fungsi itu bisa dipanggil dengan `i32` apa pun. Dalam kasus seperti ini, kita bisa memakai keyword `safe` untuk menyatakan bahwa fungsi khusus ini aman dipanggil meski ia berada di dalam blok `unsafe extern`. Setelah kita membuat perubahan itu, memanggilnya tidak lagi memerlukan blok `unsafe`, seperti ditunjukkan di Listing 20-9.

<Listing number="20-9" file-name="src/main.rs" caption="Menandai fungsi secara eksplisit sebagai `safe` di dalam blok `unsafe extern` dan memanggilnya dengan aman">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-09/src/main.rs}}
```

</Listing>

Menandai fungsi sebagai `safe` tidak otomatis membuatnya aman! Sebaliknya, itu seperti janji yang kamu buat kepada Rust bahwa fungsi itu aman. Tanggung jawab memastikan janji itu ditepati tetap ada di tanganmu!

#### Memanggil Fungsi Rust dari Bahasa Lain

Kita juga bisa memakai `extern` untuk membuat antarmuka yang memungkinkan bahasa lain memanggil fungsi Rust. Alih-alih membuat blok `extern` penuh, kita menambahkan keyword `extern` dan menentukan ABI yang dipakai tepat sebelum keyword `fn` pada fungsi yang bersangkutan. Kita juga perlu menambahkan anotasi `#[unsafe(no_mangle)]` untuk memberitahu compiler Rust agar tidak mengubah nama fungsi ini. _Mangling_ adalah proses ketika compiler mengubah nama yang kita berikan pada fungsi menjadi nama lain yang memuat lebih banyak informasi untuk dikonsumsi oleh bagian lain dari proses kompilasi, tetapi lebih sulit dibaca manusia. Compiler setiap bahasa pemrograman melakukan mangling dengan cara yang sedikit berbeda, jadi agar fungsi Rust bisa dipanggil oleh bahasa lain, kita harus menonaktifkan name mangling compiler Rust. Ini unsafe karena tanpa mangling bawaan bisa terjadi benturan nama antar-library, jadi tanggung jawab kita untuk memastikan nama yang kita pilih aman untuk diekspor tanpa mangling.

Pada contoh berikut, kita membuat fungsi `call_from_c` bisa diakses dari kode C, setelah dikompilasi menjadi shared library dan ditautkan dari C:

```
#[unsafe(no_mangle)]
pub extern "C" fn call_from_c() {
    println!("Just called a Rust function from C!");
}
```

Penggunaan `extern` ini memerlukan `unsafe` hanya pada atribut, bukan pada blok `extern`.

### Mengakses atau Mengubah Variabel Static yang Mutable

Di buku ini, kita belum membahas variabel global. Rust memang mendukungnya, tetapi variabel global bisa bermasalah dengan aturan ownership Rust. Jika dua thread mengakses variabel global mutable yang sama, hal itu bisa menyebabkan data race.

Di Rust, variabel global disebut variabel _static_. Listing 20-10 menunjukkan contoh deklarasi dan pemakaian variabel static dengan string slice sebagai nilainya.

<Listing number="20-10" file-name="src/main.rs" caption="Mendefinisikan dan memakai variabel static yang immutable">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-10/src/main.rs}}
```

</Listing>

Variabel static mirip dengan konstanta, yang kita bahas di bagian [“Mendeklarasikan Konstanta”][constants]<!-- ignore --> di Bab 3. Nama variabel static menggunakan `SCREAMING_SNAKE_CASE` sesuai konvensi. Variabel static hanya bisa menyimpan reference dengan lifetime `'static`, yang berarti compiler Rust bisa menentukan lifetime-nya sendiri dan kita tidak perlu menulis anotasinya secara eksplisit. Mengakses variabel static yang immutable itu aman.

Perbedaan halus antara konstanta dan variabel static yang immutable adalah nilai dalam variabel static punya alamat tetap di memori. Memakai nilainya akan selalu mengakses data yang sama. Konstanta, di sisi lain, boleh menduplikasi datanya setiap kali dipakai. Perbedaan lain adalah variabel static bisa mutable. Mengakses dan mengubah variabel static yang mutable bersifat _unsafe_. Listing 20-11 menunjukkan cara mendeklarasikan, mengakses, dan mengubah variabel static mutable bernama `COUNTER`.

<Listing number="20-11" file-name="src/main.rs" caption="Membaca dari atau menulis ke variabel static yang mutable itu unsafe.">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-11/src/main.rs}}
```

</Listing>

Seperti variabel biasa, kita menentukan sifat mutable memakai keyword `mut`. Kode apa pun yang membaca atau menulis `COUNTER` harus berada di dalam blok `unsafe`. Kode di Listing 20-11 dikompilasi dan mencetak `COUNTER: 3` seperti yang kita harapkan karena programnya single threaded. Jika beberapa thread mengakses `COUNTER`, kemungkinan besar akan terjadi data race, sehingga itu adalah perilaku yang tidak terdefinisi. Oleh karena itu, kita perlu menandai seluruh fungsi sebagai `unsafe` dan mendokumentasikan batasan keamanannya agar siapa pun yang memanggil fungsi itu tahu apa yang boleh dan tidak boleh mereka lakukan dengan aman.

Setiap kali kita menulis fungsi unsafe, sudah menjadi kebiasaan untuk menulis komentar yang diawali `SAFETY` dan menjelaskan apa yang harus dilakukan pemanggil agar bisa memanggil fungsi itu dengan aman. Demikian pula, setiap kali kita melakukan operasi unsafe, kebiasaannya adalah menulis komentar yang diawali `SAFETY` untuk menjelaskan bagaimana aturan keamanan dipenuhi.

Selain itu, compiler secara default akan menolak setiap upaya membuat reference ke variabel static mutable melalui lint compiler. Kamu harus secara eksplisit keluar dari perlindungan lint itu dengan menambahkan anotasi `#[allow(static_mut_refs)]`, atau mengakses variabel static mutable itu lewat raw pointer yang dibuat dengan salah satu operator peminjaman raw. Ini termasuk kasus ketika reference dibuat tanpa terlihat, seperti saat ia dipakai dalam `println!` di listing kode ini. Dengan mewajibkan reference ke variabel static mutable dibuat lewat raw pointer, persyaratan keamanan untuk memakainya jadi lebih jelas.

Dengan data mutable yang bisa diakses secara global, sulit memastikan tidak ada data race; itulah sebabnya Rust menganggap variabel static mutable itu unsafe. Jika memungkinkan, lebih baik memakai teknik concurrency dan smart pointer yang aman untuk thread yang kita bahas di Bab 16 agar compiler bisa memeriksa bahwa akses data dari thread berbeda dilakukan dengan aman.

### Mengimplementasikan Trait Unsafe

Kita bisa memakai `unsafe` untuk mengimplementasikan trait unsafe. Sebuah trait bersifat unsafe ketika minimal salah satu method-nya punya invariant yang tidak bisa diverifikasi compiler. Kita menyatakan bahwa sebuah trait itu `unsafe` dengan menambahkan keyword `unsafe` sebelum `trait` dan menandai implementasi trait itu sebagai `unsafe` juga, seperti ditunjukkan di Listing 20-12.

<Listing number="20-12" caption="Mendefinisikan dan mengimplementasikan trait unsafe">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-12/src/main.rs:here}}
```

</Listing>

Dengan memakai `unsafe impl`, kita berjanji akan menjaga invariant yang tidak bisa diverifikasi compiler.

Sebagai contoh, ingat trait marker `Send` dan `Sync` yang kita bahas di bagian [“Concurrency yang Dapat Dikembangkan dengan `Send` dan `Sync`”][send-and-sync]<!-- ignore --> di Bab 16: Compiler mengimplementasikan trait ini secara otomatis jika tipe kita seluruhnya tersusun dari tipe-tipe yang mengimplementasikan `Send` dan `Sync`. Jika kita mengimplementasikan tipe yang berisi tipe yang tidak mengimplementasikan `Send` atau `Sync`, seperti raw pointer, dan kita ingin menandai tipe itu sebagai `Send` atau `Sync`, kita harus memakai `unsafe`. Rust tidak bisa memverifikasi bahwa tipe kita memenuhi jaminan bahwa ia bisa dikirim ke thread lain atau diakses dari beberapa thread dengan aman; oleh karena itu, kita perlu melakukan pemeriksaan itu secara manual dan menandakannya dengan `unsafe`.

### Mengakses Field dari Union

Tindakan terakhir yang hanya bisa dilakukan dengan `unsafe` adalah mengakses field dari union. Sebuah *union* mirip dengan `struct`, tetapi hanya satu field yang dideklarasikan yang dipakai dalam sebuah instance pada satu waktu. Union terutama dipakai untuk berantarmuka dengan union dalam kode C. Mengakses field union itu unsafe karena Rust tidak bisa menjamin tipe data yang saat ini tersimpan di instance union itu. Kamu bisa mempelajari lebih lanjut tentang union di [Rust Reference][unions].

### Memakai Miri untuk Memeriksa Kode Unsafe

Saat menulis kode unsafe, kamu mungkin ingin memeriksa apakah kode yang kamu tulis benar-benar aman dan benar. Salah satu cara terbaik untuk melakukannya adalah memakai Miri, alat resmi Rust untuk mendeteksi perilaku yang tidak terdefinisi. Jika borrow checker adalah alat _statik_ yang bekerja saat kompilasi, Miri adalah alat _dinamis_ yang bekerja saat runtime. Miri memeriksa kodemu dengan menjalankan programmu, atau test suite-nya, dan mendeteksi saat kamu melanggar aturan yang ia pahami tentang cara kerja Rust.

Memakai Miri membutuhkan build nightly dari Rust (yang kita bahas lebih lanjut di [Lampiran G: Bagaimana Rust Dibuat dan “Nightly Rust”][nightly]<!-- ignore -->). Kamu bisa memasang versi nightly Rust dan alat Miri dengan mengetik `rustup +nightly component add miri`. Ini tidak mengubah versi Rust yang dipakai proyekmu; ia hanya menambahkan alat itu ke sistemmu agar bisa kamu pakai kapanpun kamu mau. Kamu bisa menjalankan Miri pada sebuah proyek dengan mengetik `cargo +nightly miri run` atau `cargo +nightly miri test`.

Sebagai contoh betapa bergunanya alat ini, pertimbangkan apa yang terjadi saat kita menjalankannya pada Listing 20-7.

```console
{{#include ../listings/ch20-advanced-features/listing-20-07/output.txt}}
```

Miri dengan tepat memperingatkan kita bahwa kita mengubah bilangan bulat menjadi pointer, yang bisa menjadi masalah, tetapi Miri tidak bisa menentukan apakah masalah itu benar-benar ada karena ia tidak tahu dari mana pointer itu berasal. Lalu, Miri mengembalikan error di titik mana Listing 20-7 memiliki perilaku yang tidak terdefinisi karena kita punya dangling pointer. Berkat Miri, kita sekarang tahu ada risiko perilaku yang tidak terdefinisi, dan kita bisa memikirkan cara membuat kode itu aman. Dalam beberapa kasus, Miri bahkan bisa memberi rekomendasi tentang cara memperbaiki error.

Miri tidak menangkap semua kesalahan yang mungkin kamu buat saat menulis kode unsafe. Miri adalah alat analisis dinamis, jadi ia hanya menangkap masalah pada kode yang benar-benar dijalankan. Itu berarti kamu perlu memakainya bersama teknik pengujian yang baik untuk meningkatkan keyakinanmu terhadap kode unsafe yang kamu tulis. Miri juga tidak mencakup semua kemungkinan cara kodemu bisa menjadi unsound.

Dengan kata lain: Jika Miri _memang_ menangkap masalah, kamu tahu ada bug, tetapi hanya karena Miri _tidak_ menangkap bug bukan berarti tidak ada masalah. Meski begitu, Miri bisa menangkap banyak hal. Coba jalankan pada contoh kode unsafe lain di bab ini dan lihat apa yang dikatakannya!

Kamu bisa mempelajari lebih lanjut tentang Miri di [repositori GitHub-nya][miri].

<!-- Old headings. Do not remove or links may break. -->

<a id="when-to-use-unsafe-code"></a>

### Memakai Kode Unsafe dengan Benar

Memakai `unsafe` untuk menggunakan salah satu dari lima kekuatan super yang baru kita bahas bukanlah hal yang salah atau bahkan tercela, tetapi lebih sulit membuat kode `unsafe` menjadi benar karena compiler tidak bisa membantu menjaga keamanan memori. Saat kamu punya alasan untuk memakai kode `unsafe`, kamu boleh melakukannya, dan adanya anotasi `unsafe` yang eksplisit memudahkanmu melacak sumber masalah saat masalah itu muncul. Setiap kali kamu menulis kode unsafe, kamu bisa memakai Miri untuk membantumu lebih yakin bahwa kode yang kamu tulis memenuhi aturan Rust.

Untuk pengajahan yang jauh lebih mendalam tentang cara bekerja secara efektif dengan unsafe Rust, bacalah panduan resmi Rust untuk `unsafe`, yaitu [The Rustonomicon][nomicon].

[dangling-references]: ch04-02-references-and-borrowing.html#dangling-references
[ABI]: ../reference/items/external-blocks.html#abi
[constants]: ch03-01-variables-and-mutability.html#declaring-constants
[send-and-sync]: ch16-04-extensible-concurrency-sync-and-send.html
[the-slice-type]: ch04-03-slices.html#the-slice-type
[unions]: ../reference/items/unions.html
[miri]: https://github.com/rust-lang/miri
[editions]: appendix-05-editions.html
[nightly]: appendix-07-nightly-rust.html
[nomicon]: https://doc.rust-lang.org/nomicon/
