## `RefCell<T>` dan Pola Interior Mutability

_Interior mutability_ adalah pola desain di Rust yang memungkinkan kamu mengubah data bahkan ketika ada reference immutable ke data itu; biasanya, aturan borrowing melarang tindakan ini. Untuk mengubah data, pola ini memakai kode `unsafe` di dalam struktur data guna melonggarkan aturan biasa Rust yang mengatur perubahan dan borrowing. Kode unsafe memberi tahu compiler bahwa kita memeriksa aturan itu secara manual, bukan bergantung pada compiler untuk melakukannya; kita akan membahas kode unsafe lebih lanjut di Bab 20.

Kita bisa memakai tipe yang mengikuti pola interior mutability hanya ketika kita bisa memastikan aturan borrowing akan dipatuhi saat runtime, meski compiler tidak bisa menjaminnya. Kode `unsafe` yang terlibat lalu dibungkus dalam API yang aman, dan tipe di luarnya tetap immutable.

Mari kita jelajahi konsep ini dengan melihat tipe `RefCell<T>` yang mengikuti pola interior mutability.

<!-- Old headings. Do not remove or links may break. -->

<a id="enforcing-borrowing-rules-at-runtime-with-refcellt"></a>

### Menegakkan Aturan Borrowing saat Runtime

Tidak seperti `Rc<T>`, tipe `RefCell<T>` mewakili ownership tunggal atas data yang disimpannya. Jadi, apa yang membuat `RefCell<T>` berbeda dari tipe seperti `Box<T>`? Ingat aturan borrowing yang kamu pelajari di Bab 4:

- Pada waktu tertentu, kamu bisa memiliki _entah_ satu mutable reference atau sejumlah immutable reference (tapi tidak keduanya).
- Reference harus selalu valid.

Dengan reference dan `Box<T>`, invarian aturan borrowing ditegakkan saat compile time. Dengan `RefCell<T>`, invarian ini ditegakkan _saat runtime_. Dengan reference, jika kamu melanggar aturan ini, kamu akan mendapat error dari compiler. Dengan `RefCell<T>`, jika kamu melanggar aturan ini, program kamu akan panic dan keluar.

Keuntungan memeriksa aturan borrowing saat compile time adalah error akan tertangkap lebih awal dalam proses pengembangan, dan tidak ada dampak pada performa runtime karena semua analisis sudah selesai sebelumnya. Atas alasan itu, memeriksa aturan borrowing saat compile time adalah pilihan terbaik dalam sebagian besar kasus, dan itulah sebabnya ini menjadi pilihan default Rust.

Keuntungan memeriksa aturan borrowing saat runtime justru adalah beberapa skenario yang aman terhadap memori jadi diperbolehkan, padahal pemeriksaan compile time akan melarangnya. Analisis statis, seperti yang dilakukan compiler Rust, pada dasarnya konservatif. Beberapa sifat kode mustahil terdeteksi hanya dengan menganalisis kodenya: Contoh paling terkenal adalah Halting Problem, yang berada di luar cakupan buku ini tetapi merupakan topik menarik untuk diteliti.

Karena sebagian analisis mustahil dilakukan, jika compiler Rust tidak bisa memastikan kode mematuhi aturan ownership, compiler bisa menolak program yang sebenarnya benar; dengan begitu, compiler bersifat konservatif. Jika Rust menerima program yang salah, pengguna tidak bisa mempercayai jaminan yang diberikan Rust. Namun, jika Rust menolak program yang benar, programmer hanya akan merasa tidak nyaman, dan tidak ada hal katastropik yang terjadi. Tipe `RefCell<T>` berguna ketika kamu yakin kode kamu mematuhi aturan borrowing, tetapi compiler tidak bisa memahami dan menjaminnya.

Mirip dengan `Rc<T>`, `RefCell<T>` hanya dipakai dalam skenario single-threaded dan akan memberi error saat compile time jika kamu mencoba menggunakannya dalam konteks multithreaded. Kita akan membahas cara mendapatkan fungsionalitas `RefCell<T>` dalam program multithreaded di Bab 16.

Berikut ringkasan alasan memilih `Box<T>`, `Rc<T>`, atau `RefCell<T>`:

- `Rc<T>` memungkinkan banyak owner atas data yang sama; `Box<T>` dan `RefCell<T>` memiliki satu owner.
- `Box<T>` membolehkan borrow immutable atau mutable yang diperiksa saat compile time; `Rc<T>` hanya membolehkan borrow immutable yang diperiksa saat compile time; `RefCell<T>` membolehkan borrow immutable atau mutable yang diperiksa saat runtime.
- Karena `RefCell<T>` membolehkan borrow mutable yang diperiksa saat runtime, kamu bisa mengubah nilai di dalam `RefCell<T>` bahkan ketika `RefCell<T>` itu sendiri immutable.

Mengubah nilai di dalam nilai yang immutable adalah pola interior mutability. Mari kita lihat situasi di mana interior mutability berguna dan kita telusuri bagaimana hal itu bisa terjadi.

<!-- Old headings. Do not remove or links may break. -->

<a id="interior-mutability-a-mutable-borrow-to-an-immutable-value"></a>

### Memakai Interior Mutability

Konsekuensi dari aturan borrowing adalah ketika kamu memiliki nilai immutable, kamu tidak bisa meminjamnya secara mutable. Misalnya, kode ini tidak akan terkompilasi:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/no-listing-01-cant-borrow-immutable-as-mutable/src/main.rs}}
```

Jika kamu mencoba mengompilasi kode ini, kamu akan mendapat error berikut:

```console
{{#include ../listings/ch15-smart-pointers/no-listing-01-cant-borrow-immutable-as-mutable/output.txt}}
```

Namun, ada situasi di mana sebuah nilai akan lebih berguna jika bisa mengubah dirinya sendiri di dalam method-nya, tetapi tampak immutable bagi kode lain. Kode di luar method nilai itu tidak bisa mengubahnya. Memakai `RefCell<T>` adalah salah satu cara untuk mendapatkan kemampuan interior mutability, tetapi `RefCell<T>` tidak sepenuhnya mengakali aturan borrowing: borrow checker di compiler membolehkan interior mutability ini, dan aturan borrowing justru diperiksa saat runtime. Jika kamu melanggar aturan itu, kamu akan mendapat `panic!`, bukan error dari compiler.

Mari kita bahas contoh praktis di mana kita bisa memakai `RefCell<T>` untuk mengubah nilai immutable dan melihat mengapa hal itu berguna.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-use-case-for-interior-mutability-mock-objects"></a>

#### Menguji dengan Mock Object

Kadang saat menguji, programmer memakai sebuah tipe sebagai pengganti tipe lain untuk mengamati perilaku tertentu dan memastikan perilaku itu diterapkan dengan benar. Tipe pengganti ini disebut _test double_. Bayangkan seperti pemeran pengganti dalam pembuatan film, di mana seseorang turun tangan menggantikan aktor untuk melakukan adegan yang sangat sulit. Test double berperan sebagai pengganti tipe lain ketika kita menjalankan test. _Mock object_ adalah jenis test double tertentu yang mencatat apa yang terjadi selama sebuah test sehingga kamu bisa memastikan tindakan yang tepat benar-benar terjadi.

Rust tidak punya object dalam pengertian yang sama seperti bahasa lain, dan Rust juga tidak menyediakan fungsionalitas mock object bawaan di standard library seperti beberapa bahasa lain. Meski begitu, kamu tentu bisa membuat struct yang berfungsi sama seperti mock object.

Berikut skenario yang akan kita uji: Kita akan membuat library yang memantau sebuah nilai terhadap nilai maksimum dan mengirim pesan berdasarkan seberapa dekat nilai saat ini dengan nilai maksimum itu. Misalnya, library ini bisa dipakai untuk melacak kuota pengguna atas jumlah panggilan API yang boleh mereka lakukan.

Library kita hanya akan menyediakan fungsionalitas untuk memantau seberapa dekat sebuah nilai dengan nilai maksimum serta pesan apa yang harus dikirim pada waktu apa. Aplikasi yang memakai library kita diharapkan menyediakan mekanisme pengiriman pesannya: aplikasi bisa menampilkan pesan langsung ke pengguna, mengirim email, mengirim pesan teks, atau melakukan hal lain. Library tidak perlu tahu detail itu. Yang dibutuhkannya hanyalah sesuatu yang mengimplementasikan trait yang akan kita sediakan, bernama `Messenger`. Listing 15-20 menampilkan kode library itu.

<Listing number="15-20" file-name="src/lib.rs" caption="Sebuah library untuk memantau seberapa dekat sebuah nilai dengan nilai maksimum dan memberi peringatan ketika nilai mencapai level tertentu">

```rust,noplayground
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-20/src/lib.rs}}
```

</Listing>

Satu bagian penting dari kode ini adalah trait `Messenger` memiliki satu method bernama `send` yang menerima immutable reference ke `self` dan teks pesan. Trait ini adalah antarmuka yang harus diimplementasikan mock object kita agar mock bisa dipakai seperti object sungguhan. Bagian penting lainnya adalah kita ingin menguji perilaku method `set_value` pada `LimitTracker`. Kita bisa mengubah nilai yang kita berikan untuk parameter `value`, tetapi `set_value` tidak mengembalikan apa pun yang bisa kita jadikan dasar assertion. Kita ingin bisa menyatakan bahwa jika kita membuat `LimitTracker` dengan sesuatu yang mengimplementasikan trait `Messenger` dan nilai tertentu untuk `max`, messenger tersebut akan diperintahkan mengirim pesan yang tepat ketika kita memberikan angka berbeda untuk `value`.

Kita butuh mock object yang, alih-alih mengirim email atau pesan teks saat kita memanggil `send`, hanya mencatat pesan-pesan yang diperintahkan kepadanya. Kita bisa membuat instance baru mock object, membuat `LimitTracker` yang memakai mock itu, memanggil method `set_value` pada `LimitTracker`, lalu memeriksa bahwa mock object memiliki pesan yang kita harapkan. Listing 15-21 menunjukkan percobaan mengimplementasikan mock object untuk melakukan persis itu, tetapi borrow checker tidak mengizinkannya.

<Listing number="15-21" file-name="src/lib.rs" caption="Percobaan mengimplementasikan `MockMessenger` yang tidak diizinkan oleh borrow checker">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-21/src/lib.rs:here}}
```

</Listing>

Kode test ini mendefinisikan struct `MockMessenger` yang memiliki field `sent_messages` berupa `Vec` berisi nilai `String` untuk mencatat pesan-pesan yang diperintahkan kepadanya. Kita juga mendefinisikan fungsi asosiasi `new` agar mudah membuat nilai `MockMessenger` baru yang diawali dengan daftar pesan kosong. Lalu kita mengimplementasikan trait `Messenger` untuk `MockMessenger` supaya bisa memberikan `MockMessenger` kepada `LimitTracker`. Dalam definisi method `send`, kita mengambil pesan yang diterima sebagai parameter dan menyimpannya ke dalam daftar `sent_messages` milik `MockMessenger`.

Dalam test ini, kita menguji apa yang terjadi ketika `LimitTracker` diperintahkan menetapkan `value` ke sesuatu yang lebih dari 75 persen dari nilai `max`. Pertama, kita membuat `MockMessenger` baru, yang akan dimulai dengan daftar pesan kosong. Lalu, kita membuat `LimitTracker` baru dan memberinya reference ke `MockMessenger` baru itu serta nilai `max` sebesar `100`. Kita memanggil method `set_value` pada `LimitTracker` dengan nilai `80`, yang lebih dari 75 persen dari 100. Setelah itu, kita memastikan daftar pesan yang dicatat `MockMessenger` kini berisi satu pesan.

Namun, ada satu masalah dengan test ini, seperti yang terlihat di sini:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-21/output.txt}}
```

Kita tidak bisa mengubah `MockMessenger` untuk mencatat pesan, karena method `send` menerima immutable reference ke `self`. Kita juga tidak bisa mengikuti saran dari teks error untuk memakai `&mut self` baik pada method di `impl` maupun pada definisi trait. Kita tidak ingin mengubah trait `Messenger` hanya demi keperluan testing. Sebaliknya, kita perlu menemukan cara agar kode test kita bekerja dengan benar pada desain yang sudah ada.

Ini adalah situasi di mana interior mutability bisa membantu! Kita akan menyimpan `sent_messages` di dalam `RefCell<T>`, lalu method `send` bisa mengubah `sent_messages` untuk menyimpan pesan-pesan yang kita lihat. Listing 15-22 menunjukkan tampilannya.

<Listing number="15-22" file-name="src/lib.rs" caption="Memakai `RefCell<T>` untuk mengubah nilai dalam saat nilai luar dianggap immutable">

```rust,noplayground
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-22/src/lib.rs:here}}
```

</Listing>

Field `sent_messages` kini bertipe `RefCell<Vec<String>>`, bukan `Vec<String>`. Di fungsi `new`, kita membuat instance `RefCell<Vec<String>>` baru di sekitar vector kosong.

Untuk implementasi method `send`, parameter pertama tetap berupa immutable borrow dari `self`, yang sesuai dengan definisi trait. Kita memanggil `borrow_mut` pada `RefCell<Vec<String>>` di `self.sent_messages` untuk mendapatkan mutable reference ke nilai di dalam `RefCell<Vec<String>>`, yaitu vector itu. Lalu, kita bisa memanggil `push` pada mutable reference ke vector tersebut untuk mencatat pesan-pesan yang dikirim selama test.

Perubahan terakhir yang harus kita lakukan ada pada assertion: Untuk melihat berapa banyak item di dalam vector bagian dalam, kita memanggil `borrow` pada `RefCell<Vec<String>>` untuk mendapatkan immutable reference ke vector tersebut.

Setelah kamu melihat cara memakai `RefCell<T>`, mari kita pelajari lebih dalam cara kerjanya!

<!-- Old headings. Do not remove or links may break. -->

<a id="keeping-track-of-borrows-at-runtime-with-refcellt"></a>

#### Melacak Borrow saat Runtime

Saat membuat immutable dan mutable reference, kita memakai sintaks `&` dan `&mut`. Dengan `RefCell<T>`, kita memakai method `borrow` dan `borrow_mut`, yang merupakan bagian dari API aman yang dimiliki `RefCell<T>`. Method `borrow` mengembalikan tipe smart pointer `Ref<T>`, dan `borrow_mut` mengembalikan tipe smart pointer `RefMut<T>`. Kedua tipe itu mengimplementasikan `Deref`, sehingga kita bisa memperlakukannya seperti reference biasa.

`RefCell<T>` mencatat berapa banyak smart pointer `Ref<T>` dan `RefMut<T>` yang sedang aktif. Setiap kali kita memanggil `borrow`, `RefCell<T>` menambah hitungan borrow immutable yang aktif. Ketika nilai `Ref<T>` keluar dari scope, hitungan borrow immutable berkurang 1. Sama seperti aturan borrowing saat compile time, `RefCell<T>` membolehkan kita memiliki banyak borrow immutable atau satu borrow mutable pada waktu tertentu.

Jika kita mencoba melanggar aturan ini, alih-alih mendapat error dari compiler seperti yang terjadi pada reference, implementasi `RefCell<T>` akan panic saat runtime. Listing 15-23 menunjukkan modifikasi terhadap implementasi `send` di Listing 15-22. Kita sengaja mencoba membuat dua borrow mutable aktif dalam scope yang sama untuk mengilustrasikan bahwa `RefCell<T>` mencegah kita melakukan hal itu saat runtime.

<Listing number="15-23" file-name="src/lib.rs" caption="Membuat dua mutable reference dalam scope yang sama untuk melihat bahwa `RefCell<T>` akan panic">

```rust,ignore,panics
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-23/src/lib.rs:here}}
```

</Listing>

Kita membuat variabel `one_borrow` untuk smart pointer `RefMut<T>` yang dikembalikan dari `borrow_mut`. Lalu, kita membuat borrow mutable lain dengan cara yang sama di variabel `two_borrow`. Ini menghasilkan dua mutable reference dalam scope yang sama, yang tidak diizinkan. Ketika kita menjalankan test untuk library kita, kode di Listing 15-23 akan terkompilasi tanpa error, tetapi test-nya akan gagal:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-23/output.txt}}
```

Perhatikan bahwa kode panic dengan pesan `already borrowed: BorrowMutError`. Begitulah `RefCell<T>` menangani pelanggaran aturan borrowing saat runtime.

Memilih untuk menangkap error borrowing saat runtime, bukan saat compile time, seperti yang kita lakukan di sini, berarti kamu bisa menemukan kesalahan dalam kode lebih lambat dalam proses pengembangan: mungkin baru setelah kode kamu di-deploy ke produksi. Selain itu, kode kamu akan menanggung sedikit penalti performa runtime sebagai akibat dari melacak borrow saat runtime alih-alih saat compile time. Meski begitu, memakai `RefCell<T>` memungkinkan kita menulis mock object yang bisa mengubah dirinya sendiri untuk mencatat pesan-pesan yang dilihatnya, bahkan saat kamu menggunakannya dalam konteks yang hanya membolehkan nilai immutable. Kamu bisa memakai `RefCell<T>` meski ada trade-off-nya untuk mendapatkan fungsionalitas lebih daripada yang bisa diberikan reference biasa.

<!-- Old headings. Do not remove or links may break. -->

<a id="having-multiple-owners-of-mutable-data-by-combining-rc-t-and-ref-cell-t"></a>
<a id="allowing-multiple-owners-of-mutable-data-with-rct-and-refcellt"></a>

### Mengizinkan Beberapa Owner atas Data Mutable

Cara umum memakai `RefCell<T>` adalah menggabungkannya dengan `Rc<T>`. Ingat bahwa `Rc<T>` memungkinkan kamu memiliki beberapa owner atas suatu data, tetapi hanya memberi akses immutable ke data itu. Jika kamu punya `Rc<T>` yang berisi `RefCell<T>`, kamu bisa mendapatkan nilai yang dapat memiliki beberapa owner _dan_ bisa kamu ubah!

Misalnya, ingat contoh cons list di Listing 15-18, di mana kita memakai `Rc<T>` untuk membolehkan beberapa list berbagi ownership atas list lain. Karena `Rc<T>` hanya menyimpan nilai immutable, kita tidak bisa mengubah nilai apa pun di dalam list setelah membuatnya. Mari kita tambahkan `RefCell<T>` karena kemampuannya mengubah nilai di dalam list. Listing 15-24 menunjukkan bahwa dengan memakai `RefCell<T>` pada definisi `Cons`, kita bisa mengubah nilai yang tersimpan di semua list.

<Listing number="15-24" file-name="src/main.rs" caption="Memakai `Rc<RefCell<i32>>` untuk membuat `List` yang bisa kita ubah">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-24/src/main.rs}}
```

</Listing>

Kita membuat nilai yang merupakan instance dari `Rc<RefCell<i32>>` dan menyimpannya dalam variabel bernama `value` agar bisa kita akses langsung nanti. Lalu, kita membuat `List` di `a` dengan variant `Cons` yang memuat `value`. Kita perlu meng-clone `value` supaya `a` dan `value` sama-sama memiliki ownership atas nilai `5` di dalamnya, alih-alih mengalihkan ownership dari `value` ke `a` atau membuat `a` meminjam dari `value`.

Kita membungkus list `a` dalam `Rc<T>` supaya ketika kita membuat list `b` dan `c`, keduanya bisa merujuk ke `a`, seperti yang kita lakukan di Listing 15-18.

Setelah kita membuat list dalam `a`, `b`, dan `c`, kita ingin menambahkan 10 ke nilai di `value`. Kita melakukan ini dengan memanggil `borrow_mut` pada `value`, yang memakai fitur dereferensing otomatis yang kita bahas di [“Di Mana Operator `->`?”][wheres-the---operator]<!-- ignore --> di Bab 5 untuk mendereferensikan `Rc<T>` menjadi nilai `RefCell<T>` di dalamnya. Method `borrow_mut` mengembalikan smart pointer `RefMut<T>`, dan kita memakai operator dereference padanya untuk mengubah nilai di dalamnya.

Ketika kita mencetak `a`, `b`, dan `c`, kita bisa melihat bahwa semuanya memiliki nilai `15` yang sudah diubah, bukan `5`:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-24/output.txt}}
```

Teknik ini cukup keren! Dengan memakai `RefCell<T>`, kita memiliki nilai `List` yang tampak immutable dari luar. Tetapi kita bisa memakai method pada `RefCell<T>` yang memberi akses ke interior mutability-nya supaya bisa mengubah data kita saat diperlukan. Pemeriksaan aturan borrowing saat runtime melindungi kita dari data race, dan terkadang sepadan untuk mengorbankan sedikit kecepatan demi fleksibilitas dalam struktur data kita. Perhatikan bahwa `RefCell<T>` tidak bekerja untuk kode multithreaded! `Mutex<T>` adalah versi `RefCell<T>` yang aman terhadap thread, dan kita akan membahas `Mutex<T>` di Bab 16.

[wheres-the---operator]: ch05-03-method-syntax.html#wheres-the---operator
