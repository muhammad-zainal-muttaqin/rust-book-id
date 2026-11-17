## Lampiran C: Trait yang Bisa Di-derive

Di banyak bagian buku ini, kita sudah membahas atribut `derive` yang bisa kamu
terapkan pada definisi struct atau enum. Atribut `derive` menghasilkan kode yang
mengimplementasikan sebuah trait dengan implementasi defaultnya sendiri pada
tipe yang kamu beri anotasi sintaks `derive`.

Di lampiran ini, kami menyediakan referensi semua trait di standard library yang
bisa kamu gunakan bersama `derive`. Setiap bagian membahas:

- Operator dan metode apa saja yang aktif setelah trait ini di-derive
- Apa yang dilakukan implementasi trait yang disediakan oleh `derive`
- Apa arti mengimplementasikan trait tersebut bagi sebuah tipe
- Kondisi di mana kamu boleh atau tidak boleh mengimplementasikan trait itu
- Contoh operasi yang memerlukan trait tersebut

Jika kamu ingin perilaku yang berbeda dari yang disediakan atribut `derive`,
lihat [dokumentasi standard library](../std/index.html)<!-- ignore --> untuk
masing-masing trait guna mengetahui cara mengimplementasikannya secara manual.

Trait yang terdaftar di sini hanyalah trait yang didefinisikan oleh standard
library dan bisa diimplementasikan pada tipe milikmu menggunakan `derive`.
Trait lain yang didefinisikan di standard library tidak punya perilaku default
yang masuk akal, sehingga terserah kamu mengimplementasikannya dengan cara yang
masuk akal untuk tujuan yang sedang kamu kejar.

Contoh trait yang tidak bisa di-derive adalah `Display`, yang menangani
formatasi untuk pengguna akhir. Kamu selalu harus mempertimbangkan cara yang
tepat untuk menampilkan sebuah tipe kepada pengguna akhir. Bagian tipe mana yang
boleh dilihat pengguna akhir? Bagian mana yang relevan bagi mereka? Format data
seperti apa yang paling berguna bagi mereka? Compiler Rust tidak punya
wawasan ini, jadi tidak bisa menyediakan perilaku default yang tepat untukmu.

Daftar trait yang bisa di-derive di lampiran ini tidak lengkap: sebuah library
bisa mengimplementasikan `derive` untuk trait-nya sendiri, sehingga daftar trait
yang bisa kamu gunakan bersama `derive` benar-benar terbuka. Mengimplementasikan
`derive` melibatkan penggunaan macro prosedural, yang dibahas di bagian
[“Custom `derive` Macros”][custom-derive-macros]<!-- ignore --> di Bab 20.

### `Debug` untuk Output Programmer

Trait `Debug` mengaktifkan formatasi debug dalam format string, yang kamu
tandai dengan menambahkan `:?` di dalam placeholder `{}`.

Trait `Debug` memungkinkan kamu mencetak instance sebuah tipe untuk keperluan
debug, sehingga kamu dan programmer lain yang memakai tipe kamu bisa memeriksa
instance pada titik tertentu saat eksekusi program berjalan.

Trait `Debug` diperlukan, misalnya, saat menggunakan macro `assert_eq!`. Macro
ini mencetak nilai-nilai instance yang diberikan sebagai argumen jika asersi
kekesetaraan gagal, agar programmer bisa melihat mengapa kedua instance tidak
sama.

### `PartialEq` dan `Eq` untuk Perbandingan Kekesetaraan

Trait `PartialEq` memungkinkan kamu membandingkan instance sebuah tipe untuk
memeriksa kekesetaraan dan mengaktifkan penggunaan operator `==` dan `!=`.

Menderive `PartialEq` mengimplementasikan metode `eq`. Ketika `PartialEq`
di-derive pada struct, dua instance dianggap sama hanya jika _semua_ field
sama, dan kedua instance dianggap tidak sama jika _ada_ field yang tidak sama.
Ketika di-derive pada enum, setiap variant sama dengan dirinya sendiri dan
berbeda dengan variant lainnya.

Trait `PartialEq` diperlukan, misalnya, saat menggunakan macro `assert_eq!`,
yang perlu bisa membandingkan dua instance sebuah tipe untuk kekesetaraan.

Trait `Eq` tidak punya metode. Tujuannya adalah menandai bahwa setiap nilai
dengan tipe yang dianotasi selalu sama dengan dirinya sendiri. Trait `Eq`
hanya bisa diterapkan pada tipe yang juga mengimplementasikan `PartialEq`,
meskipun tidak semua tipe yang mengimplementasikan `PartialEq` bisa
mengimplementasikan `Eq`. Salah satu contohnya adalah tipe bilangan titik
ambang: implementasi bilangan titik ambang menyatakan bahwa dua instance nilai
bukan-angka (`NaN`) tidak saling sama.

Contoh saat `Eq` diperlukan adalah untuk key dalam `HashMap<K, V>` agar
`HashMap<K, V>` bisa menentukan apakah dua key tersebut sama.

### `PartialOrd` dan `Ord` untuk Perbandingan Urutan

Trait `PartialOrd` memungkinkan kamu membandingkan instance sebuah tipe untuk
keperluan pengurutan. Tipe yang mengimplementasikan `PartialOrd` bisa digunakan
bersama operator `<`, `>`, `<=`, dan `>=`. Kamu hanya bisa menerapkan trait
`PartialOrd` pada tipe yang juga mengimplementasikan `PartialEq`.

Menderive `PartialOrd` mengimplementasikan metode `partial_cmp`, yang
mengembalikan `Option<Ordering>` yang akan bernilai `None` ketika nilai yang
diberikan tidak menghasilkan suatu urutan. Contoh nilai yang tidak menghasilkan
urutan, meskipun sebagian besar nilai tipe itu bisa dibandingkan, adalah nilai
titik ambang `NaN`. Memanggil `partial_cmp` dengan bilangan titik ambang apa pun
dan nilai titik ambang `NaN` akan mengembalikan `None`.

Ketika di-derive pada struct, `PartialOrd` membandingkan dua instance dengan
membandingkan nilai di setiap field secara berurutan sesuai kemunculan field
dalam definisi struct. Ketika di-derive pada enum, variant enum yang dideklarasikan
lebih dulu dalam definisi enum dianggap lebih kecil daripada variant yang
dinyatakan belakangan.

Trait `PartialOrd` diperlukan, misalnya, untuk metode `gen_range` dari crate
`rand` yang menghasilkan nilai acak dalam rentang yang ditentukan oleh sebuah
ekspresi rentang.

Trait `Ord` memungkinkan kamu tahu bahwa untuk dua nilai apa pun dengan tipe
yang dianotasi, selalu ada urutan yang valid. Trait `Ord` mengimplementasikan
metode `cmp`, yang mengembalikan `Ordering` alih-alih `Option<Ordering>` karena
urutan yang valid selalu mungkin. Kamu hanya bisa menerapkan trait `Ord` pada
tipe yang juga mengimplementasikan `PartialOrd` dan `Eq` (dan `Eq`
memerlukan `PartialEq`). Ketika di-derive pada struct dan enum, `cmp`
berperilaku sama seperti implementasi hasil derive untuk `partial_cmp` pada
`PartialOrd`.

Contoh saat `Ord` diperlukan adalah saat menyimpan nilai dalam `BTreeSet<T>`,
sebuah struktur data yang menyimpan data berdasarkan urutan sort dari
nilai-nilainya.

### `Clone` dan `Copy` untuk Menduplikasi Nilai

Trait `Clone` memungkinkan kamu membuat salinan mendalam dari sebuah nilai
secara eksplisit, dan proses duplikasi tersebut bisa melibatkan menjalankan kode
sembarang serta menyalin data heap. Lihat bagian
[“Variables and Data Interacting with
Clone”][variables-and-data-interacting-with-clone]<!-- ignore --> di Bab 4
untuk informasi lebih lanjut tentang `Clone`.

Menderive `Clone` mengimplementasikan metode `clone`, yang ketika diimplementasikan
untuk seluruh tipe, memanggil `clone` pada setiap bagian tipe tersebut. Artinya
semua field atau nilai dalam tipe juga harus mengimplementasikan `Clone` agar
bisa di-derive `Clone`.

Contoh saat `Clone` diperlukan adalah saat memanggil metode `to_vec` pada sebuah
slice. Slice tidak memiliki (own) instance tipe yang ada di dalamnya, tetapi
vector yang dikembalikan dari `to_vec` perlu memiliki instance-nya, sehingga
`to_vec` memanggil `clone` pada setiap item. Karena itu, tipe yang disimpan di
dalam slice harus mengimplementasikan `Clone`.

Trait `Copy` memungkinkan kamu menduplikasi nilai dengan hanya menyalin bit yang
tersimpan di stack; tidak ada kode sembarang yang diperlukan. Lihat bagian
[“Stack-Only Data: Copy”][stack-only-data-copy]<!-- ignore --> di Bab 4 untuk
informasi lebih lanjut tentang `Copy`.

Trait `Copy` tidak mendefinisikan metode apa pun untuk mencegah programmer
menimpa metode-metode itu dan melanggar asumsi bahwa tidak ada kode sembarang
yang dijalankan. Dengan begitu, semua programmer bisa berasumsi bahwa menyalin
sebuah nilai akan berjalan sangat cepat.

Kamu bisa menderive `Copy` pada tipe apa pun yang seluruh bagiannya mengimplementasikan `Copy`. Tipe yang mengimplementasikan `Copy` juga harus
mengimplementasikan `Clone`, karena tipe yang mengimplementasikan `Copy`
memiliki implementasi `Clone` yang sederhana dan melakukan tugas yang sama
dengan `Copy`.

Trait `Copy` jarang diperlukan; tipe yang mengimplementasikan `Copy` punya
optimasi yang tersedia, artinya kamu tidak perlu memanggil `clone`, sehingga
kode menjadi lebih ringkas.

Segala sesuatu yang bisa dilakukan dengan `Copy` juga bisa kamu capai dengan
`Clone`, tetapi kodenya mungkin lebih lambat atau harus memakai `clone` di
beberapa tempat.

### `Hash` untuk Memetakan Nilai ke Nilai Berukuran Tetap

Trait `Hash` memungkinkan kamu mengambil instance sebuah tipe berukuran sembarang
lalu memetakan instance tersebut ke nilai berukuran tetap menggunakan sebuah
fungsi hash. Menderive `Hash` mengimplementasikan metode `hash`. Implementasi
hasil derive dari metode `hash` menggabungkan hasil pemanggilan `hash` pada
setiap bagian tipe, artinya semua field atau nilai juga harus mengimplementasikan
`Hash` agar bisa di-derive `Hash`.

Contoh saat `Hash` diperlukan adalah saat menyimpan key dalam `HashMap<K, V>`
untuk menyimpan data secara efisien.

### `Default` untuk Nilai Bawaan

Trait `Default` memungkinkan kamu membuat nilai bawaan untuk sebuah tipe.
Menderive `Default` mengimplementasikan fungsi `default`. Implementasi hasil
derive dari fungsi `default` memanggil fungsi `default` pada setiap bagian tipe,
artinya semua field atau nilai dalam tipe juga harus mengimplementasikan
`Default` agar bisa di-derive `Default`.

Fungsi `Default::default` sering digunakan bersama dengan sintaks update struct
yang dibahas di bagian
[“Creating Instances from Other Instances with Struct Update
Syntax”][creating-instances-from-other-instances-with-struct-update-syntax]<!--
ignore --> di Bab 5. Kamu bisa menyesuaikan beberapa field sebuah struct, lalu
menetapkan dan menggunakan nilai bawaan untuk field sisanya dengan
`..Default::default()`.

Trait `Default` diperlukan saat kamu menggunakan metode `unwrap_or_default` pada
instance `Option<T>`, misalnya. Jika `Option<T>` bernilai `None`, metode
`unwrap_or_default` akan mengembalikan hasil `Default::default` untuk tipe `T`
yang tersimpan di dalam `Option<T>`.

[creating-instances-from-other-instances-with-struct-update-syntax]: ch05-01-defining-structs.html#creating-instances-from-other-instances-with-struct-update-syntax
[stack-only-data-copy]: ch04-01-what-is-ownership.html#stack-only-data-copy
[variables-and-data-interacting-with-clone]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-clone
[custom-derive-macros]: ch20-05-macros.html#custom-derive-macros
