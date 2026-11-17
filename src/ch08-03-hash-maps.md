## Menyimpan Kunci dengan Nilai Terkait di Hash Map

Koleksi umum terakhir kita adalah hash map. Tipe `HashMap<K, V>` menyimpan pemetaan dari kunci bertipe `K` ke nilai bertipe `V` menggunakan sebuah _hashing function_ yang menentukan bagaimana kunci dan nilai tersebut diletakkan di memori. Banyak bahasa pemrograman mendukung struktur data seperti ini, tetapi sering kali dengan nama berbeda, misalnya _hash_, _map_, _object_, _hash table_, _dictionary_, atau _associative array_, dan masih banyak lagi.

Hash map berguna saat kamu ingin mencari data bukan lewat indeks seperti pada vector, melainkan lewat kunci yang bisa bertipe apa saja. Sebagai contoh, dalam sebuah game kamu bisa menyimpan skor tiap tim di sebuah hash map, dengan nama tim sebagai kunci dan skor tim sebagai nilainya. Dengan nama tim, kamu bisa mengambil skor tim tersebut.

Kita akan membahas API dasar hash map di bagian ini, tetapi masih banyak lagi fitur menarik yang tersembunyi di fungsi-fungsi yang didefinisikan standard library pada `HashMap<K, V>`. Seperti biasa, periksa dokumentasi standard library untuk informasi lebih lanjut.

### Membuat Hash Map Baru

Salah satu cara membuat hash map kosong adalah dengan memakai `new` dan menambahkan elemen menggunakan `insert`. Pada Listing 8-20, kita menyimpan skor dua tim yang bernama _Blue_ dan _Yellow_. Tim Blue mulai dengan 10 poin, dan tim Yellow mulai dengan 50.

<Listing number="8-20" caption="Creating a new hash map and inserting some keys and values">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-20/src/main.rs:here}}
```

</Listing>

Perhatikan bahwa kita perlu lebih dulu melakukan `use` terhadap `HashMap` dari bagian collections di standard library. Dari tiga koleksi umum kita, yang paling jarang dipakai adalah ini, sehingga tidak ikut masuk dalam fitur yang otomatis dibawa ke scope oleh prelude. Hash map juga mendapat dukungan lebih sedikit dari standard library; sebagai contoh, tidak ada macro bawaan untuk membuatnya.

Sama seperti vector, hash map menyimpan datanya di heap. `HashMap` ini punya kunci bertipe `String` dan nilai bertipe `i32`. Seperti vector, hash map bersifat homogen: semua kunci harus bertipe sama, dan semua nilai juga harus bertipe sama.

<a id="accessing-values-in-a-hash-map"></a>
### Mengakses Nilai di Hash Map

Kita bisa mengambil sebuah nilai dari hash map dengan memberikan kunci ke method `get`, seperti ditunjukkan pada Listing 8-21.

<Listing number="8-21" caption="Accessing the score for the Blue team stored in the hash map">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-21/src/main.rs:here}}
```

</Listing>

Di sini, `score` akan berisi nilai yang terkait dengan tim Blue, yaitu `10`. Method `get` mengembalikan `Option<&V>`; jika tidak ada nilai untuk kunci itu di hash map, `get` akan mengembalikan `None`. Program ini menangani `Option` tersebut dengan memanggil `copied` untuk mendapatkan `Option<i32>` alih-alih `Option<&i32>`, lalu `unwrap_or` untuk mengatur `score` menjadi nol jika `scores` tidak punya entri untuk kunci itu.

Kita bisa mengiterasi setiap pasangan kunci-nilai di hash map dengan cara yang mirip seperti pada vector, memakai loop `for`:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-03-iterate-over-hashmap/src/main.rs:here}}
```

Kode ini akan mencetak setiap pasangan dalam urutan sembarang:

```text
Yellow: 50
Blue: 10
```

<!-- Old headings. Do not remove or links may break. -->

<a id="hash-maps-and-ownership"></a>

### Mengelola Ownership di Hash Map

Untuk tipe yang mengimplementasikan trait `Copy`, seperti `i32`, nilainya disalin ke dalam hash map. Untuk nilai yang dimiliki seperti `String`, nilainya akan dipindahkan dan hash map menjadi pemilik nilai-nilai itu, seperti ditunjukkan pada Listing 8-22.

<Listing number="8-22" caption="Showing that keys and values are owned by the hash map once they’re inserted">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-22/src/main.rs:here}}
```

</Listing>

Kita tidak bisa lagi memakai variabel `field_name` dan `field_value` setelah variabel itu dipindahkan ke dalam hash map lewat pemanggilan `insert`.

Jika kita menyisipkan reference ke nilai ke dalam hash map, nilainya tidak akan dipindahkan ke hash map. Nilai yang ditunjuk reference tersebut harus valid selama hash map masih valid. Kita akan membahas masalah ini lebih lanjut di [“Memvalidasi Reference dengan
Lifetimes”][validating-references-with-lifetimes]<!-- ignore --> pada Bab 10.

### Memperbarui Hash Map

Meskipun jumlah pasangan kunci dan nilai bisa bertambah, setiap kunci unik hanya boleh punya satu nilai terkait pada satu waktu (tetapi tidak sebaliknya: misalnya, tim Blue dan tim Yellow sama-sama boleh punya nilai `10` di hash map `scores`).

Saat kamu ingin mengubah data di hash map, kamu harus memutuskan bagaimana menangani kasus ketika sebuah kunci sudah punya nilai. Kamu bisa mengganti nilai lama dengan nilai baru tanpa peduli pada nilai lama. Kamu bisa menyimpan nilai lama dan mengabaikan nilai baru, hanya menambahkan nilai baru jika kunci itu _belum_ punya nilai. Atau kamu bisa menggabungkan nilai lama dengan nilai baru. Mari kita lihat caranya masing-masing!

#### Menimpa Sebuah Nilai

Jika kita menyisipkan sebuah kunci dan nilai ke dalam hash map, lalu menyisipkan kunci yang sama dengan nilai berbeda, nilai yang terkait dengan kunci itu akan diganti. Meskipun kode pada Listing 8-23 memanggil `insert` dua kali, hash map hanya akan berisi satu pasangan kunci-nilai karena kita menyisipkan nilai untuk kunci tim Blue pada kedua panggilan itu.

<Listing number="8-23" caption="Replacing a value stored with a particular key">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-23/src/main.rs:here}}
```

</Listing>

Kode ini akan mencetak `{"Blue": 25}`. Nilai awal `10` sudah ditimpa.

<!-- Old headings. Do not remove or links may break. -->

<a id="only-inserting-a-value-if-the-key-has-no-value"></a>

#### Menambahkan Kunci dan Nilai Hanya Jika Kunci Belum Ada

Sering kali kita memeriksa apakah sebuah kunci sudah ada di hash map dengan sebuah nilai, lalu melakukan tindakan berikut: jika kunci memang sudah ada di hash map, nilai yang ada dibiarkan apa adanya; jika kunci belum ada, kuncinya disisipkan berserta nilainya.

Hash map punya API khusus untuk ini bernama `entry` yang menerima kunci yang ingin kamu periksa sebagai argumen. Nilai kembalian method `entry` adalah sebuah enum bernama `Entry` yang mewakili nilai yang mungkin ada dan mungkin juga tidak. Misalnya kita ingin memeriksa apakah kunci tim Yellow sudah punya nilai terkait. Jika belum, kita ingin menyisipkan nilai `50`, dan hal yang sama untuk tim Blue. Dengan memakai API `entry`, kode akan terlihat seperti Listing 8-24.

<Listing number="8-24" caption="Using the `entry` method to only insert if the key does not already have a value">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-24/src/main.rs:here}}
```

</Listing>

Method `or_insert` pada `Entry` didefinisikan untuk mengembalikan reference mutable ke nilai untuk kunci `Entry` yang bersangkutan jika kunci itu ada, dan jika tidak ada, ia menyisipkan argumen sebagai nilai baru untuk kunci tersebut lalu mengembalikan reference mutable ke nilai baru itu. Teknik ini jauh lebih rapi daripada menulis logikanya sendiri dan, sebagai tambahan, lebih bersahabat dengan borrow checker.

Menjalankan kode pada Listing 8-24 akan mencetak `{"Yellow": 50, "Blue": 10}`. Panggilan `entry` pertama akan menyisipkan kunci tim Yellow dengan nilai `50` karena tim Yellow belum punya nilai. Panggilan `entry` kedua tidak akan mengubah hash map, karena tim Blue sudah punya nilai `10`.

#### Memperbarui Nilai Berdasarkan Nilai Lama

Kasus penggunaan hash map yang umum lainnya adalah mencari nilai sebuah kunci, lalu memperbaruinya berdasarkan nilai lama. Sebagai contoh, Listing 8-25 menunjukkan kode yang menghitung berapa kali setiap kata muncul dalam sebuah teks. Kita memakai hash map dengan kata sebagai kunci dan menambah nilai tiap kunci untuk mencatat berapa kali kita menemukan kata itu. Jika ini kali pertama kita menemukan sebuah kata, kita akan lebih dulu menyisipkan nilai `0`.

<Listing number="8-25" caption="Counting occurrences of words using a hash map that stores words and counts">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-25/src/main.rs:here}}
```

</Listing>

Kode ini akan mencetak `{"world": 2, "hello": 1, "wonderful": 1}`. Kamu mungkin melihat pasangan kunci-nilai yang sama tercetak dengan urutan berbeda: ingat dari [“Mengakses Nilai di Hash Map”][access]<!-- ignore --> bahwa iterasi atas hash map terjadi dalam urutan sembarang.

Method `split_whitespace` mengembalikan iterator atas subslice yang dipisah whitespace dari nilai di `text`. Method `or_insert` mengembalikan reference mutable (`&mut V`) ke nilai untuk kunci yang ditentukan. Di sini kita menyimpan reference mutable itu ke variabel `count`, sehingga untuk menetapkan nilai tersebut kita harus lebih dulu dereference `count` dengan tanda asterisk (`*`). Reference mutable keluar dari scope di akhir loop `for`, sehingga semua perubahan ini aman dan diizinkan oleh aturan borrowing.

### Hashing Function

Secara bawaan, `HashMap` memakai hashing function bernama _SipHash_ yang memberi ketahanan terhadap serangan denial-of-service (DoS) yang melibatkan hash table[^siphash]<!-- ignore -->. Ini bukan algoritma hashing tercepat yang tersedia, tetapi pertukaran keamanan lebih baik yang datang dari penurunan performanya sepadan. Jika kamu mem-profil kode dan menemukan bahwa fungsi hash bawaan terlalu lambat untuk kebutuhanmu, kamu bisa beralih ke fungsi lain dengan menentukan hasher yang berbeda. Sebuah _hasher_ adalah tipe yang mengimplementasikan trait `BuildHasher`. Kita akan membahas trait dan cara mengimplementasikannya di [Bab 10][traits]<!-- ignore -->. Kamu tidak harus mengimplementasikan hasher sendiri dari nol; [crates.io](https://crates.io/)<!-- ignore --> punya library yang dibagikan pengguna Rust lain dan menyediakan hasher untuk banyak algoritma hashing yang umum dipakai.

[^siphash]: [https://en.wikipedia.org/wiki/SipHash](https://en.wikipedia.org/wiki/SipHash)

## Ringkasan

Vector, string, dan hash map akan memberikan banyak sekali fungsionalitas yang dibutuhkan dalam program saat kamu perlu menyimpan, mengakses, dan memodifikasi data. Berikut beberapa latihan yang seharusnya sudah bisa kamu kerjakan:

1. Dengan sebuah daftar bilangan bulat, gunakan vector dan kembalikan median (nilai di posisi tengah setelah diurutkan) dan modus (nilai yang paling sering muncul; hash map akan membantu di sini) dari daftar itu.
1. Ubah string ke bahasa Pig Latin. Konsonan pertama setiap kata dipindahkan ke akhir kata dan _ay_ ditambahkan, sehingga _first_ menjadi _irst-fay_. Kata yang diawali huruf vokal justru mendapat _hay_ di akhirnya (_apple_ menjadi _apple-hay_). Perhatikan detail tentang pengkodean UTF-8!
1. Dengan hash map dan vector, buat antarmuka teks yang memungkinkan pengguna menambahkan nama karyawan ke sebuah departemen di sebuah perusahaan; misalnya, “Add Sally to Engineering” atau “Add Amir to Sales.” Lalu, biarkan pengguna mengambil daftar semua orang di sebuah departemen atau semua orang di perusahaan per departemen, diurutkan secara alfabetis.

Dokumentasi API standard library menjelaskan method yang dimiliki vector, string, dan hash map dan akan membantu untuk latihan-latihan ini!

Kita mulai memasuki program yang lebih kompleks yang operasinya bisa gagal, jadi ini waktu yang tepat untuk membahas penanganan error. Itu yang akan kita lakukan berikutnya!

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[access]: #accessing-values-in-a-hash-map
[traits]: ch10-02-traits.html
