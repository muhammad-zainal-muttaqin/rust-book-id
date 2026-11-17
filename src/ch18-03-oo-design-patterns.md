## Mengimplementasikan Pola Desain Berorientasi Objek

*State pattern* adalah sebuah pola desain berorientasi objek. Inti dari pola ini adalah kita mendefinisikan sekumpulan state yang bisa dimiliki sebuah nilai di dalam dirinya. State-state itu direpresentasikan oleh sekumpulan *state object*, dan perilaku nilai berubah berdasarkan state-nya. Kita akan membahas sebuah contoh struct pos blog yang punya field untuk menyimpan state-nya, yang akan berupa sebuah state object dari kumpulan “draft,” “review,” atau “published.”

State-state itu berbagi fungsionalitas: Di Rust, tentu saja, kita memakai struct dan trait alih-alih objek dan inheritance. Setiap state object bertanggung jawab atas perilakunya sendiri dan atas kapan ia harus berubah menjadi state lain. Nilai yang menyimpan sebuah state object tidak tahu apa-apa soal perilaku berbeda dari state-state itu maupun kapan transisi antar-state harus terjadi.

Keuntungan memakai state pattern adalah, saat kebutuhan bisnis program berubah, kita tidak perlu mengubah kode nilai yang menyimpan state maupun kode yang memakai nilai itu. Kita cuma perlu memperbarui kode di dalam salah satu state object untuk mengubah aturannya, atau mungkin menambah state object lain.

Pertama, kita akan mengimplementasikan state pattern dengan cara yang lebih tradisional berorientasi objek. Lalu, kita akan memakai pendekatan yang agak lebih alami di Rust. Mari kita mulai mengimplementasikan alur kerja pos blog secara bertahap memakai state pattern.

Fungsionalitas akhirnya akan terlihat seperti ini:

1. Sebuah pos blog dimulai sebagai draft kosong.
1. Saat draft selesai, review terhadap pos itu diminta.
1. Saat pos disetujui, pos itu dipublikasikan.
1. Hanya pos blog yang sudah dipublikasikan yang mengembalikan konten untuk dicetak, supaya pos yang belum disetujui tidak bisa terbit secara tidak sengaja.

Perubahan lain yang dicoba pada sebuah pos seharusnya tidak berpengaruh. Misalnya, jika kita mencoba menyetujui draft pos blog sebelum meminta review, pos itu harus tetap menjadi draft yang belum dipublikasikan.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-traditional-object-oriented-attempt"></a>

### Mencoba Gaya Berorientasi Objek Tradisional

Ada tak terhingga cara menyusun kode untuk memecahkan masalah yang sama, masing-masing dengan trade-off berbeda. Implementasi di bagian ini lebih berupa gaya berorientasi objek tradisional, yang memang bisa ditulis di Rust, tapi tidak memanfaatkan beberapa kekuatan Rust. Nanti, kita akan mendemonstrasikan solusi lain yang tetap memakai pola desain berorientasi objek, tetapi disusun dengan cara yang mungkin terasa kurang akrab bagi programmer yang berpengalaman dengan orientasi objek. Kita akan membandingkan kedua solusi itu untuk merasakan trade-off dari merancang kode Rust secara berbeda dari kode di bahasa lain.

Listing 18-11 menunjukkan alur kerja ini dalam bentuk kode: Ini adalah contoh penggunaan API yang akan kita implementasikan dalam sebuah library crate bernama `blog`. Kode ini belum bisa dikompilasi karena kita belum mengimplementasikan crate `blog`.

<Listing number="18-11" file-name="src/main.rs" caption="Kode yang mendemonstrasikan perilaku yang kita inginkan dari crate `blog` kami">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:all}}
```

</Listing>

Kita ingin mengizinkan pengguna membuat pos blog draft baru dengan `Post::new`. Kita ingin mengizinkan teks ditambahkan ke pos blog. Jika kita mencoba mendapatkan konten pos itu seketika, sebelum disetujui, kita seharusnya tidak mendapat teks apa pun karena pos itu masih berupa draft. Kita sudah menambahkan `assert_eq!` dalam kode untuk keperluan demonstrasi. Sebuah unit test yang bagus untuk ini adalah menegaskan bahwa draft pos blog mengembalikan string kosong dari method `content`, tapi kita tidak akan menulis test untuk contoh ini.

Selanjutnya, kita ingin mengaktifkan permintaan review terhadap pos, dan kita ingin `content` mengembalikan string kosong selagi menunggu review. Saat pos itu mendapat persetujuan, pos itu harus dipublikasikan, yang berarti teks pos akan dikembalikan saat `content` dipanggil.

Perhatikan bahwa satu-satunya tipe yang kita interaksi dari crate itu adalah tipe `Post`. Tipe ini akan memakai state pattern dan akan menyimpan sebuah nilai yang menjadi salah satu dari tiga state object yang mewakili berbagai state yang bisa dimiliki sebuah pos—draft, review, atau published. Perpindahan dari satu state ke state lain akan dikelola secara internal di dalam tipe `Post`. State berubah sebagai respons terhadap method yang dipanggil oleh pengguna library kita pada instance `Post`, tapi mereka tidak perlu mengelola perubahan state secara langsung. Juga, pengguna tidak bisa melakukan kesalahan pada state, misalnya mempublikasikan pos sebelum pos itu di-review.

<!-- Old headings. Do not remove or links may break. -->

<a id="defining-post-and-creating-a-new-instance-in-the-draft-state"></a>

#### Mendefinisikan `Post` dan Membuat Instance Baru

Mari mulai implementasi library ini! Kita tahu kita butuh struct `Post` publik yang menyimpan beberapa konten, jadi kita akan mulai dengan definisi struct dan sebuah fungsi `new` asosiasi yang publik untuk membuat instance `Post`, seperti pada Listing 18-12. Kita juga akan membuat trait `State` privat yang akan mendefinisikan perilaku yang harus dimiliki semua state object bagi `Post`.

Lalu, `Post` akan menyimpan sebuah trait object `Box<dyn State>` di dalam sebuah `Option<T>` pada field privat bernama `state` untuk menyimpan state object. Nanti kamu akan melihat mengapa `Option<T>` itu diperlukan.

<Listing number="18-12" file-name="src/lib.rs" caption="Definisi struct `Post` dan fungsi `new` yang membuat instance `Post` baru, sebuah trait `State`, dan struct `Draft`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-12/src/lib.rs}}
```

</Listing>

Trait `State` mendefinisikan perilaku yang dimiliki bersama oleh state-state pos yang berbeda. State object-nya adalah `Draft`, `PendingReview`, dan `Published`, dan semuanya akan mengimplementasikan trait `State`. Untuk sementara, trait itu belum punya method apa pun, dan kita akan mulai dengan mendefinisikan state `Draft` saja karena itu adalah state yang kita inginkan saat sebuah pos dimulai.

Saat kita membuat `Post` baru, kita menetapkan field `state`-nya ke sebuah nilai `Some` yang memegang sebuah `Box`. `Box` ini menunjuk ke instance baru dari struct `Draft`. Ini memastikan bahwa setiap kali kita membuat instance `Post` baru, pos itu akan dimulai sebagai draft. Karena field `state` dari `Post` bersifat privat, tidak ada cara untuk membuat `Post` dalam state lain! Dalam fungsi `Post::new`, kita menetapkan field `content` ke `String` baru yang kosong.

#### Menyimpan Teks Konten Pos

Di Listing 18-11 kita melihat bahwa kita ingin bisa memanggil method bernama `add_text` dan memberinya sebuah `&str` yang lalu ditambahkan sebagai teks konten pos blog. Kita mengimplementasikannya sebagai method, alih-alih mengekspos field `content` sebagai `pub`, supaya nanti kita bisa mengimplementasikan method yang mengontrol cara data field `content` dibaca. Method `add_text` cukup lurus, jadi mari tambahkan implementasinya di Listing 18-13 ke blok `impl Post`.

<Listing number="18-13" file-name="src/lib.rs" caption="Mengimplementasikan method `add_text` untuk menambahkan teks ke `content` sebuah pos">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-13/src/lib.rs:here}}
```

</Listing>

Method `add_text` menerima reference mutable ke `self` karena kita mengubah instance `Post` yang kita panggil `add_text` padanya. Lalu kita memanggil `push_str` pada `String` di `content` dan meneruskan argumen `text` untuk ditambahkan ke `content` yang tersimpan. Perilaku ini tidak bergantung pada state pos itu, jadi bukan bagian dari state pattern. Method `add_text` tidak berinteraksi dengan field `state` sama sekali, tapi ia adalah bagian dari perilaku yang ingin kita dukung.

<!-- Old headings. Do not remove or links may break. -->

<a id="ensuring-the-content-of-a-draft-post-is-empty"></a>

#### Memastikan Konten Draft Pos Kosong

Bahkan setelah kita memanggil `add_text` dan menambahkan beberapa konten ke pos kita, kita tetap ingin method `content` mengembalikan string slice kosong karena pos itu masih dalam state draft, seperti ditunjukkan oleh `assert_eq!` pertama di Listing 18-11. Untuk sementara, mari implementasikan method `content` dengan hal paling sederhana yang memenuhi syarat ini: selalu mengembalikan string slice kosong. Nanti kita akan mengubahnya setelah mengimplementasikan kemampuan mengubah state pos agar bisa dipublikasikan. Sejauh ini, pos hanya bisa berada dalam state draft, jadi konten pos harus selalu kosong. Listing 18-14 menunjukkan implementasi sementara ini.

<Listing number="18-14" file-name="src/lib.rs" caption="Menambahkan implementasi sementara untuk method `content` pada `Post` yang selalu mengembalikan string slice kosong">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-14/src/lib.rs:here}}
```

</Listing>

Dengan method `content` yang ditambahkan ini, semua hal di Listing 18-11 sampai `assert_eq!` pertama bekerja seperti yang diharapkan.

<!-- Old headings. Do not remove or links may break. -->

<a id="requesting-a-review-of-the-post-changes-its-state"></a>
<a id="requesting-a-review-changes-the-posts-state"></a>

#### Meminta Review, yang Mengubah State Pos

Selanjutnya, kita perlu menambahkan fungsionalitas untuk meminta review terhadap sebuah pos, yang harus mengubah state-nya dari `Draft` menjadi `PendingReview`. Listing 18-15 menunjukkan kode ini.

<Listing number="18-15" file-name="src/lib.rs" caption="Mengimplementasikan method `request_review` pada `Post` dan trait `State`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-15/src/lib.rs:here}}
```

</Listing>

Kita memberi `Post` method publik bernama `request_review` yang menerima reference mutable ke `self`. Lalu, kita memanggil method internal `request_review` pada state `Post` saat ini, dan method `request_review` kedua ini mengonsumsi state saat ini serta mengembalikan state baru.

Kita menambahkan method `request_review` ke trait `State`; semua tipe yang mengimplementasikan trait itu sekarang perlu mengimplementasikan method `request_review`. Perhatikan bahwa alih-alih `self`, `&self`, atau `&mut self` sebagai parameter pertama method, kita memakai `self: Box<Self>`. Sintaks ini berarti method hanya valid saat dipanggil pada sebuah `Box` yang memegang tipe itu. Sintaks ini mengambil ownership atas `Box<Self>`, sehingga state lama jadi tidak valid agar nilai state dari `Post` bisa berubah menjadi state baru.

Untuk mengonsumsi state lama, method `request_review` perlu mengambil ownership nilai state. Di sinilah `Option` pada field `state` dari `Post` berperan: Kita memanggil method `take` untuk mengambil nilai `Some` keluar dari field `state` dan menyisakan `None` di tempatnya, karena Rust tidak mengizinkan field yang tidak terisi pada struct. Ini memungkinkan kita memindahkan nilai `state` keluar dari `Post`, alih-alih meminjamnya. Lalu, kita akan menetapkan nilai `state` pos ke hasil operasi ini.

Kita perlu menetapkan `state` ke `None` untuk sementara, alih-alih menetapkannya langsung dengan kode seperti `self.state = self.state.request_review();`, supaya mendapat ownership nilai `state`. Ini memastikan `Post` tidak bisa memakai nilai `state` lama setelah kita mengubahnya menjadi state baru.

Method `request_review` pada `Draft` mengembalikan instance baru yang di-box dari struct `PendingReview` baru, yang mewakili state saat sebuah pos menunggu review. Struct `PendingReview` juga mengimplementasikan method `request_review` tapi tidak melakukan transformasi apa pun. Alih-alih, ia mengembalikan dirinya sendiri karena saat kita meminta review pada pos yang sudah berada dalam state `PendingReview`, pos itu harus tetap dalam state `PendingReview`.

Sekarang kita mulai bisa melihat keuntungan state pattern: Method `request_review` pada `Post` sama saja tidak peduli nilai `state`-nya. Setiap state bertanggung jawab atas aturannya sendiri.

Kita akan membiarkan method `content` pada `Post` apa adanya, mengembalikan string slice kosong. Kita sekarang bisa punya `Post` dalam state `PendingReview` maupun dalam state `Draft`, tapi kita menginginkan perilaku yang sama dalam state `PendingReview`. Listing 18-11 sekarang bekerja sampai pemanggilan `assert_eq!` kedua!

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-the-approve-method-that-changes-the-behavior-of-content"></a>
<a id="adding-approve-to-change-the-behavior-of-content"></a>

#### Menambahkan `approve` untuk Mengubah Perilaku `content`

Method `approve` akan mirip dengan method `request_review`: Ia akan menetapkan `state` ke nilai yang dikatakan state saat ini sebagai nilai yang harus dimiliki saat state itu disetujui, seperti pada Listing 18-16.

<Listing number="18-16" file-name="src/lib.rs" caption="Mengimplementasikan method `approve` pada `Post` dan trait `State`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-16/src/lib.rs:here}}
```

</Listing>

Kita menambahkan method `approve` ke trait `State` dan menambahkan struct baru yang mengimplementasikan `State`, yaitu state `Published`.

Mirip dengan cara kerja `request_review` pada `PendingReview`, jika kita memanggil method `approve` pada sebuah `Draft`, itu tidak akan berpengaruh karena `approve` akan mengembalikan `self`. Saat kita memanggil `approve` pada `PendingReview`, ia mengembalikan instance baru yang di-box dari struct `Published`. Struct `Published` mengimplementasikan trait `State`, dan untuk method `request_review` maupun method `approve`, ia mengembalikan dirinya sendiri karena pos harus tetap dalam state `Published` dalam kasus-kasus itu.

Sekarang kita perlu memperbarui method `content` pada `Post`. Kita ingin nilai yang dikembalikan dari `content` bergantung pada state `Post` saat ini, jadi kita akan membuat `Post` mendelegasikan ke method `content` yang didefinisikan pada `state`-nya, seperti pada Listing 18-17.

<Listing number="18-17" file-name="src/lib.rs" caption="Memperbarui method `content` pada `Post` untuk mendelegasikan ke method `content` pada `State`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-17/src/lib.rs:here}}
```

</Listing>

Karena tujuannya adalah menjaga semua aturan ini tetap berada di dalam struct yang mengimplementasikan `State`, kita memanggil method `content` pada nilai di `state` dan meneruskan instance pos (yaitu, `self`) sebagai argumen. Lalu, kita mengembalikan nilai yang dikembalikan dari pemakaian method `content` pada nilai `state` itu.

Kita memanggil method `as_ref` pada `Option` karena kita ingin sebuah reference ke nilai di dalam `Option`, alih-alih ownership nilai itu. Karena `state` adalah sebuah `Option<Box<dyn State>>`, saat kita memanggil `as_ref`, sebuah `Option<&Box<dyn State>>` dikembalikan. Jika kita tidak memanggil `as_ref`, kita akan mendapat error karena kita tidak bisa memindahkan `state` keluar dari `&self` yang dipinjam pada parameter fungsi.

Lalu kita memanggil method `unwrap`, yang kita tahu tidak akan pernah panic karena kita tahu method pada `Post` memastikan bahwa `state` akan selalu berisi nilai `Some` saat method-method itu selesai. Ini adalah salah satu kasus yang kita bahas di bagian [“Saat Kamu Punya Informasi Lebih Banyak daripada Compiler”][more-info-than-rustc]<!-- ignore --> di Bab 9, saat kita tahu bahwa nilai `None` tidak mungkin terjadi, meskipun compiler tidak bisa memahami hal itu.

Pada titik ini, saat kita memanggil `content` pada `&Box<dyn State>`, deref coercion akan berlaku pada `&` dan `Box` sehingga method `content` pada akhirnya akan dipanggil pada tipe yang mengimplementasikan trait `State`. Itu berarti kita perlu menambahkan `content` ke definisi trait `State`, dan di situlah kita akan menaruh logika untuk menentukan konten apa yang dikembalikan bergantung pada state yang kita miliki, seperti pada Listing 18-18.

<Listing number="18-18" file-name="src/lib.rs" caption="Menambahkan method `content` ke trait `State`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-18/src/lib.rs:here}}
```

</Listing>

Kita menambahkan implementasi default untuk method `content` yang mengembalikan string slice kosong. Itu berarti kita tidak perlu mengimplementasikan `content` pada struct `Draft` dan `PendingReview`. Struct `Published` akan meng-override method `content` dan mengembalikan nilai di `post.content`. Meski nyaman, membuat method `content` pada `State` yang menentukan konten `Post` mengaburkan batas antara tanggung jawab `State` dan tanggung jawab `Post`.

Perhatikan bahwa kita perlu anotasi lifetime pada method ini, seperti yang kita bahas di Bab 10. Kita mengambil sebuah reference ke `post` sebagai argumen dan mengembalikan sebuah reference ke bagian dari `post` itu, jadi lifetime dari reference yang dikembalikan berkaitan dengan lifetime dari argumen `post`.

Dan kita selesai—sekarang seluruh Listing 18-11 bekerja! Kita sudah mengimplementasikan state pattern dengan aturan alur kerja pos blog. Logika yang berkaitan dengan aturan itu hidup di state object, alih-alih tersebar di seluruh `Post`.

> ### Mengapa Bukan Enum?
>
> Mungkin kamu bertanya-tanya mengapa kita tidak memakai enum dengan state-state pos yang berbeda sebagai varian. Itu tentu saja solusi yang memungkinkan; cobalah dan bandingkan hasil akhirnya untuk melihat mana yang kamu sukai! Satu kelemahan memakai enum adalah setiap tempat yang memeriksa nilai enum akan membutuhkan ekspresi `match` atau sejenisnya untuk menangani setiap varian yang mungkin. Ini bisa jadi lebih berulang daripada solusi trait object ini.

<!-- Old headings. Do not remove or links may break. -->

<a id="trade-offs-of-the-state-pattern"></a>

#### Menilai State Pattern

Kita sudah menunjukkan bahwa Rust mampu mengimplementasikan state pattern berorientasi objek untuk mengenkapsulasi berbagai jenis perilaku yang harus dimiliki sebuah pos dalam setiap state. Method pada `Post` tidak tahu apa-apa soal berbagai perilaku itu. Berkat cara kita menyusun kode, kita hanya perlu melihat di satu tempat untuk mengetahui berbagai cara pos yang dipublikasikan bisa berperilaku: implementasi trait `State` pada struct `Published`.

Jika kita membuat implementasi alternatif yang tidak memakai state pattern, kita mungkin justru memakai ekspresi `match` pada method di `Post` atau bahkan pada kode `main` yang memeriksa state pos dan mengubah perilaku di tempat-tempat itu. Itu berarti kita harus melihat di beberapa tempat untuk memahami semua implikasi dari sebuah pos yang berada dalam state published.

Dengan state pattern, method `Post` dan tempat-tempat kita memakai `Post` tidak memerlukan ekspresi `match`, dan untuk menambah state baru, kita hanya perlu menambah struct baru dan mengimplementasikan method-method trait pada struct itu di satu lokasi.

Implementasi yang memakai state pattern mudah diperluas untuk menambah fungsionalitas. Untuk melihat betapa sederhananya merawat kode yang memakai state pattern, cobalah beberapa saran ini:

- Tambahkan method `reject` yang mengubah state pos dari `PendingReview` kembali ke `Draft`.
- Wajibkan dua pemanggilan `approve` sebelum state bisa diubah menjadi `Published`.
- Izinkan pengguna menambahkan konten teks hanya saat pos berada dalam state `Draft`. Petunjuk: biarkan state object bertanggung jawab atas apa yang mungkin berubah pada konten, tapi bukan bertanggung jawab untuk memodifikasi `Post`.

Satu kelemahan state pattern adalah, karena state-state itulah yang mengimplementasikan transisi antar-state, sebagian state saling terhubung satu sama lain. Jika kita menambah state lain antara `PendingReview` dan `Published`, misalnya `Scheduled`, kita harus mengubah kode di `PendingReview` agar bertransisi ke `Scheduled` sebagai gantinya. Akan lebih ringan kalau `PendingReview` tidak perlu berubah dengan ditambahnya state baru, tapi itu berarti beralih ke pola desain lain.

Kelemahan lain adalah kita sudah menduplikasi sebagian logika. Untuk menghilangkan sebagian duplikasi, kita bisa mencoba membuat implementasi default untuk method `request_review` dan `approve` pada trait `State` yang mengembalikan `self`. Namun, ini tidak akan berhasil: Saat memakai `State` sebagai trait object, trait itu tidak tahu persis apa `self` konkretnya, jadi tipe kembaliannya tidak diketahui saat kompilasi. (Ini adalah salah satu aturan dyn compatibility yang disebut sebelumnya.)

Duplikasi lain mencakup implementasi yang serupa dari method `request_review` dan `approve` pada `Post`. Kedua method memakai `Option::take` pada field `state` dari `Post`, dan jika `state` adalah `Some`, mereka mendelegasikan ke implementasi method yang sama pada nilai yang dibungkus serta menetapkan nilai baru field `state` ke hasilnya. Seandainya kita punya banyak method pada `Post` yang mengikuti pola ini, kita bisa pertimbangkan mendefinisikan sebuah macro untuk menghilangkan pengulangan (lihat bagian [“Macros”][macros]<!-- ignore --> di Bab 20).

Dengan mengimplementasikan state pattern persis seperti yang didefinisikan untuk bahasa berorientasi objek, kita tidak memanfaatkan kekuatan Rust sepenuhnya seperti yang bisa kita lakukan. Mari kita lihat beberapa perubahan yang bisa kita buat pada crate `blog` yang bisa mengubah state dan transisi yang tidak valid menjadi error saat kompilasi.

<a id="encoding-states-and-behavior-as-types"></a>
### Mengodekan State dan Perilaku sebagai Tipe

Kita akan menunjukkan cara memikirkan ulang state pattern untuk mendapatkan sekumpulan trade-off yang berbeda. Alih-alih mengenkapsulasi state dan transisi sepenuhnya sehingga kode di luar tidak mengetahui keduanya, kita akan mengodekan state ke dalam tipe-tipe yang berbeda. Akibatnya, sistem pengecekan tipe Rust akan mencegah upaya memakai draft pos di tempat yang hanya mengizinkan pos yang dipublikasikan dengan mengeluarkan error compiler.

Mari kita pertimbangkan bagian pertama dari `main` di Listing 18-11:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:here}}
```

</Listing>

Kita tetap mengaktifkan pembuatan pos baru dalam state draft memakai `Post::new` dan kemampuan menambahkan teks ke konten pos. Tapi alih-alih punya method `content` pada draft pos yang mengembalikan string kosong, kita akan membuat draft pos sama sekali tidak punya method `content`. Dengan begitu, jika kita mencoba mendapatkan konten draft pos, kita akan mendapat error compiler yang mengatakan method itu tidak ada. Hasilnya, kita tidak mungkin secara tidak sengaja menampilkan konten draft pos di produksi karena kode itu bahkan tidak akan dikompilasi. Listing 18-19 menunjukkan definisi struct `Post` dan struct `DraftPost`, beserta method pada masing-masing.

<Listing number="18-19" file-name="src/lib.rs" caption="Sebuah `Post` dengan method `content` dan sebuah `DraftPost` tanpa method `content`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-19/src/lib.rs}}
```

</Listing>

Struct `Post` maupun `DraftPost` punya field `content` privat yang menyimpan teks pos blog. Struct-structure itu tidak lagi punya field `state` karena kita memindahkan pengodean state ke tipe-tipe struct. Struct `Post` akan mewakili pos yang dipublikasikan, dan ia punya method `content` yang mengembalikan `content`.

Kita tetap punya fungsi `Post::new`, tapi alih-alih mengembalikan instance `Post`, fungsi itu mengembalikan instance `DraftPost`. Karena `content` bersifat privat dan tidak ada fungsi yang mengembalikan `Post`, saat ini tidak mungkin membuat instance `Post`.

Struct `DraftPost` punya method `add_text`, jadi kita bisa menambahkan teks ke `content` seperti sebelumnya, tapi perhatikan bahwa `DraftPost` tidak punya method `content` yang didefinisikan! Jadi sekarang program memastikan semua pos dimulai sebagai draft pos, dan draft pos tidak punya konten yang tersedia untuk ditampilkan. Setiap upaya mengakali batasan ini akan menghasilkan error compiler.

<!-- Old headings. Do not remove or links may break. -->

<a id="implementing-transitions-as-transformations-into-different-types"></a>

Jadi, bagaimana kita mendapat pos yang dipublikasikan? Kita ingin memberlakukan aturan bahwa draft pos harus di-review dan disetujui sebelum bisa dipublikasikan. Pos dalam state pending review tetap tidak boleh menampilkan konten apa pun. Mari implementasikan batasan ini dengan menambahkan struct lain, `PendingReviewPost`, mendefinisikan method `request_review` pada `DraftPost` untuk mengembalikan `PendingReviewPost`, serta mendefinisikan method `approve` pada `PendingReviewPost` untuk mengembalikan `Post`, seperti pada Listing 18-20.

<Listing number="18-20" file-name="src/lib.rs" caption="Sebuah `PendingReviewPost` yang dibuat dengan memanggil `request_review` pada `DraftPost` dan method `approve` yang mengubah `PendingReviewPost` menjadi `Post` yang dipublikasikan">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-20/src/lib.rs:here}}
```

</Listing>

Method `request_review` dan `approve` mengambil ownership `self`, sehingga mengonsumsi instance `DraftPost` dan `PendingReviewPost` serta mengubah keduanya menjadi `PendingReviewPost` dan `Post` yang dipublikasikan, berturut-turut. Dengan begitu, kita tidak akan punya instance `DraftPost` yang menggantung setelah kita memanggil `request_review` padanya, dan seterusnya. Struct `PendingReviewPost` tidak punya method `content` yang didefinisikan padanya, jadi upaya membaca kontennya menghasilkan error compiler, seperti halnya `DraftPost`. Karena satu-satunya cara mendapat instance `Post` yang dipublikasikan yang punya method `content` didefinisikan adalah dengan memanggil method `approve` pada `PendingReviewPost`, dan satu-satunya cara mendapat `PendingReviewPost` adalah dengan memanggil method `request_review` pada `DraftPost`, kita sekarang sudah mengodekan alur kerja pos blog ke dalam sistem tipe.

Tapi kita juga harus membuat beberapa perubahan kecil pada `main`. Method `request_review` dan `approve` mengembalikan instance baru, alih-alih memodifikasi struct yang dipanggil padanya, jadi kita perlu menambahkan lebih banyak penugasan `let post =` yang melakukan shadowing untuk menyimpan instance yang dikembalikan. Kita juga tidak bisa membuat penegasan bahwa konten draft pos dan pending review adalah string kosong, dan kita tidak memerlukannya: Kita tidak bisa mengompilasi kode yang mencoba memakai konten pos dalam state-state itu lagi. Kode yang diperbarui di `main` ditunjukkan pada Listing 18-21.

<Listing number="18-21" file-name="src/main.rs" caption="Perubahan pada `main` untuk memakai implementasi baru alur kerja pos blog">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-21/src/main.rs}}
```

</Listing>

Perubahan yang perlu kita buat pada `main` untuk menetapkan ulang `post` berarti implementasi ini tidak lagi sepenuhnya mengikuti state pattern berorientasi objek: Transisi antar-state tidak lagi terenkapsulasi seluruhnya di dalam implementasi `Post`. Namun, keuntungan kita adalah state yang tidak valid sekarang mustahil berkat sistem tipe dan pengecekan tipe yang terjadi saat kompilasi! Ini memastikan bahwa bug tertentu, seperti menampilkan konten pos yang belum dipublikasikan, akan ditemukan sebelum sampai ke produksi.

Cobalah tugas-tugas yang disarankan di awal bagian ini pada crate `blog` sebagaimana setelah Listing 18-21 untuk melihat apa pendapatmu tentang desain versi kode ini. Perhatikan bahwa sebagian tugas mungkin sudah selesai dalam desain ini.

Kita sudah melihat bahwa meskipun Rust mampu mengimplementasikan pola desain berorientasi objek, pola lain, seperti mengodekan state ke dalam sistem tipe, juga tersedia di Rust. Pola-pola ini punya trade-off berbeda. Meski kamu mungkin sangat akrab dengan pola berorientasi objek, memikirkan ulang masalah untuk memanfaatkan fitur-fitur Rust bisa memberi manfaat, misalnya mencegah beberapa bug saat kompilasi. Pola berorientasi objek tidak selalu menjadi solusi terbaik di Rust karena fitur-fitur tertentu, seperti ownership, yang tidak dimiliki bahasa berorientasi objek.

## Ringkasan

Terlepas dari apakah kamu menganggap Rust sebagai bahasa berorientasi objek setelah membaca bab ini atau tidak, sekarang kamu tahu bahwa kamu bisa memakai trait object untuk mendapatkan beberapa fitur berorientasi objek di Rust. Dynamic dispatch bisa memberi kode kamu sejumlah fleksibilitas dengan imbalan sedikit performa runtime. Kamu bisa memakai fleksibilitas itu untuk mengimplementasikan pola berorientasi objek yang bisa membantu maintainability kode kamu. Rust juga punya fitur lain, seperti ownership, yang tidak dimiliki bahasa berorientasi objek. Sebuah pola berorientasi objek tidak selalu menjadi cara terbaik untuk memanfaatkan kekuatan Rust, tapi itu tetap merupakan pilihan yang tersedia.

Selanjutnya, kita akan melihat pattern, yang merupakan salah satu fitur Rust lain yang memungkinkan fleksibilitas besar. Kita sudah melihatnya sekilas di seluruh buku ini, tapi belum melihat kemampuan penuhnya. Mari kita mulai!

[more-info-than-rustc]: ch09-03-to-panic-or-not-to-panic.html#cases-in-which-you-have-more-information-than-the-compiler
[macros]: ch20-05-macros.html#macros
