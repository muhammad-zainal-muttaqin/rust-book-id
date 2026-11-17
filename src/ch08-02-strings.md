<a id="storing-utf-8-encoded-text-with-strings"></a>
## Menyimpan Teks Terkode UTF-8 dengan String

Kita sudah membahas string di Bab 4, tapi sekarang kita akan mempelajarinya
lebih dalam. Pemula Rust (Rustacean baru) sering tersandung pada string karena
tiga alasan sekaligus: kecenderungan Rust untuk menampilkan kemungkinan error,
string sebagai struktur data yang lebih rumit daripada yang disangka banyak
programmer, dan UTF-8. Kombinasi faktor ini bisa terasa sulit ketika kamu datang
dari bahasa pemrograman lain.

Kita membahas string dalam konteks koleksi karena string diimplementasikan
sebagai sekumpulan byte, ditambah beberapa method yang memberi perilaku berguna
ketika byte-byte itu ditafsirkan sebagai teks. Di bagian ini, kita akan
membahas operasi pada `String` yang dimiliki setiap tipe koleksi, seperti
membuat, memperbarui, dan membaca. Kita juga akan membahas perbedaan `String`
dari koleksi lainnya, yaitu bagaimana pengindeksan pada `String` menjadi rumit
karena perbedaan cara manusia dan komputer menafsirkan data `String`.

<!-- Old headings. Do not remove or links may break. -->

<a id="what-is-a-string"></a>

### Mendefinisikan String

Pertama, kita definisikan maksud istilah _string_. Rust hanya punya satu tipe
string di bahasa inti, yaitu string slice `str` yang biasanya muncul dalam
bentuk pinjaman, `&str`. Di Bab 4, kita membahas string slice, yaitu reference
ke data string terkode UTF-8 yang disimpan di tempat lain. Literal string,
misalnya, disimpan dalam binary program sehingga merupakan string slice.

Tipe `String`, yang disediakan oleh standard library Rust dan bukan bagian dari
bahasa inti, adalah tipe string yang bisa tumbuh, mutable, owned, dan terkode
UTF-8. Ketika Rustacean menyebut "string" di Rust, mereka mungkin merujuk pada
tipe `String` maupun string slice `&str`, bukan hanya salah satunya. Meski
bagian ini sebagian besar membahas `String`, kedua tipe itu sama-sama banyak
digunakan di standard library Rust, dan `String` serta string slice sama-sama
terkode UTF-8.

### Membuat String Baru

Banyak operasi yang tersedia pada `Vec<T>` juga tersedia pada `String`, karena
`String` sebenarnya diimplementasikan sebagai pembungkus di sekitar vector byte
dengan sejumlah jaminan, batasan, dan kemampuan tambahan. Contoh fungsi yang
berperilaku sama pada `Vec<T>` dan `String` adalah fungsi `new` untuk membuat
instance, seperti ditunjukkan Listing 8-11.

<Listing number="8-11" caption="Creating a new, empty `String`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-11/src/main.rs:here}}
```

</Listing>

Baris ini membuat string kosong baru bernama `s`, yang selanjutnya bisa kita
isi dengan data. Sering kali kita punya data awal yang ingin dipakai untuk
memulai string. Untuk itu, kita memakai method `to_string`, yang tersedia pada
tipe mana pun yang mengimplementasikan trait `Display`, seperti halnya literal
string. Listing 8-12 menunjukkan dua contoh.

<Listing number="8-12" caption="Using the `to_string` method to create a `String` from a string literal">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-12/src/main.rs:here}}
```

</Listing>

Kode ini membuat string yang berisi `initial contents`.

Kita juga bisa memakai fungsi `String::from` untuk membuat `String` dari
literal string. Kode di Listing 8-13 setara dengan kode di Listing 8-12 yang
memakai `to_string`.

<Listing number="8-13" caption="Using the `String::from` function to create a `String` from a string literal">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-13/src/main.rs:here}}
```

</Listing>

Karena string dipakai untuk banyak hal, kita bisa memakai berbagai API generik
untuk string, sehingga kita punya banyak pilihan. Beberapa di antaranya terlihat
redundan, tapi semuanya punya tempat! Dalam kasus ini, `String::from` dan
`to_string` melakukan hal yang sama, jadi mana yang kamu pilih hanya soal gaya
dan keterbacaan.

Ingat bahwa string terkode UTF-8, sehingga kita bisa memasukkan data apa pun
yang terkode dengan benar ke dalamnya, seperti ditunjukkan Listing 8-14.

<Listing number="8-14" caption="Storing greetings in different languages in strings">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:here}}
```

</Listing>

Semua ini adalah nilai `String` yang valid.

### Memperbarui String

`String` bisa bertambah ukurannya dan isinya bisa berubah, sama seperti isi
`Vec<T>`, jika kamu menambahkan lebih banyak data ke dalamnya. Selain itu, kamu
bisa dengan nyaman memakai operator `+` atau macro `format!` untuk menggabungkan
nilai `String`.

<!-- Old headings. Do not remove or links may break. -->

<a id="appending-to-a-string-with-push_str-and-push"></a>

#### Menambahkan dengan `push_str` atau `push`

Kita bisa menumbuhkan `String` dengan memakai method `push_str` untuk menambahkan
string slice, seperti ditunjukkan Listing 8-15.

<Listing number="8-15" caption="Appending a string slice to a `String` using the `push_str` method">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-15/src/main.rs:here}}
```

</Listing>

Setelah dua baris ini, `s` akan berisi `foobar`. Method `push_str` menerima
string slice karena kita tidak selalu ingin mengambil ownership atas parameter
tersebut. Sebagai contoh, pada kode di Listing 8-16, kita ingin tetap bisa
memakai `s2` setelah isinya ditambahkan ke `s1`.

<Listing number="8-16" caption="Using a string slice after appending its contents to a `String`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-16/src/main.rs:here}}
```

</Listing>

Jika method `push_str` mengambil ownership atas `s2`, kita tidak akan bisa
mencetak nilainya di baris terakhir. Namun, kode ini bekerja sebagaimana
diharapkan!

Method `push` menerima satu karakter sebagai parameter dan menambahkannya ke
`String`. Listing 8-17 menambahkan huruf _l_ ke sebuah `String` dengan memakai
method `push`.

<Listing number="8-17" caption="Adding one character to a `String` value using `push`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-17/src/main.rs:here}}
```

</Listing>

Hasilnya, `s` akan berisi `lol`.

<!-- Old headings. Do not remove or links may break. -->

<a id="concatenation-with-the--operator-or-the-format-macro"></a>

<a id="concatenating-with--or-format"></a>
#### Menggabungkan dengan `+` atau `format!`

Sering kali kamu ingin menggabungkan dua string yang sudah ada. Salah satu cara
melakukannya adalah dengan memakai operator `+`, seperti ditunjukkan Listing
8-18.

<Listing number="8-18" caption="Using the `+` operator to combine two `String` values into a new `String` value">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-18/src/main.rs:here}}
```

</Listing>

String `s3` akan berisi `Hello, world!`. Alasan `s1` tidak lagi valid setelah
penjumlahan, dan alasan kita memakai reference ke `s2`, terkait dengan
signature method yang dipanggil ketika kita memakai operator `+`. Operator `+`
memakai method `add`, yang signature-nya kurang lebih seperti ini:

```rust,ignore
fn add(self, s: &str) -> String {
```

Di standard library, kamu akan melihat `add` didefinisikan dengan generic dan
associated type. Di sini kita sudah menggantinya dengan tipe konkret, yang
sebenarnya terjadi ketika kita memanggil method ini dengan nilai `String`. Kita
akan membahas generic di Bab 10. Signature ini memberi kita petunjuk yang kita
butuhkan untuk memahami bagian rumit dari operator `+`.

Pertama, `s2` punya `&`, artinya kita menambahkan reference dari string kedua ke
string pertama. Ini karena parameter `s` pada fungsi `add`: kita hanya bisa
menambahkan string slice ke sebuah `String`; kita tidak bisa menambahkan dua
nilai `String` bersamaan. Tapi tunggu—tipe `&s2` adalah `&String`, bukan `&str`
sebagaimana ditentukan pada parameter kedua `add`. Lalu, mengapa Listing 8-18
bisa mengompilasi?

Alasan kita bisa memakai `&s2` dalam panggilan ke `add` adalah karena compiler
bisa mengubah argumen `&String` menjadi `&str`. Ketika kita memanggil method
`add`, Rust memakai deref coercion, yang di sini mengubah `&s2` menjadi
`&s2[..]`. Kita akan membahas deref coercion lebih lanjut di Bab 15. Karena `add`
tidak mengambil ownership atas parameter `s`, `s2` tetap menjadi `String` yang
valid setelah operasi ini.

Kedua, kita bisa melihat dari signature bahwa `add` mengambil ownership atas
`self` karena `self` _tidak_ punya `&`. Artinya `s1` di Listing 8-18 akan
di-move ke dalam panggilan `add` dan tidak lagi valid setelahnya. Jadi, meski
`let s3 = s1 + &s2;` terlihat seperti akan menyalin kedua string dan membuat
string baru, statement ini sebenarnya mengambil ownership atas `s1`, menambahkan
salinan isi `s2`, lalu mengembalikan ownership atas hasilnya. Dengan kata lain,
terlihat seperti melakukan banyak penyalinan, tapi sebenarnya tidak; implementasinya
lebih efisien daripada menyalin.

Jika kita perlu menggabungkan banyak string, perilaku operator `+` menjadi
rumit:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-01-concat-multiple-strings/src/main.rs:here}}
```

Pada titik ini, `s` akan menjadi `tic-tac-toe`. Dengan semua karakter `+` dan `"`
itu, sulit melihat apa yang sebenarnya terjadi. Untuk menggabungkan string dengan
cara yang lebih rumit, kita bisa memakai macro `format!`:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-02-format/src/main.rs:here}}
```

Kode ini juga mengatur `s` menjadi `tic-tac-toe`. Macro `format!` bekerja seperti
`println!`, tapi alih-alih mencetak keluaran ke layar, ia mengembalikan `String`
yang berisi keluaran tersebut. Versi kode yang memakai `format!` jauh lebih mudah
dibaca, dan kode yang dihasilkan oleh macro `format!` memakai reference sehingga
panggilan ini tidak mengambil ownership atas parameternya.

### Mengindeks String

Di banyak bahasa pemrograman lain, mengakses karakter individual dalam sebuah
string dengan merujuknya lewat indeks adalah operasi yang valid dan umum. Namun,
jika kamu mencoba mengakses bagian `String` dengan sintaks indeks di Rust, kamu
akan mendapatkan error. Perhatikan kode yang tidak valid di Listing 8-19.

<Listing number="8-19" caption="Attempting to use indexing syntax with a `String`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-19/src/main.rs:here}}
```

</Listing>

Kode ini akan menghasilkan error berikut:

```console
{{#include ../listings/ch08-common-collections/listing-08-19/output.txt}}
```

Error itu bercerita: string Rust tidak mendukung pengindeksan. Tapi mengapa
tidak? Untuk menjawab pertanyaan itu, kita perlu membahas bagaimana Rust
menyimpan string di memori.

#### Representasi Internal

`String` adalah pembungkus di atas `Vec<u8>`. Mari kita lihat beberapa contoh
string terkode UTF-8 yang benar dari Listing 8-14. Pertama, yang ini:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:spanish}}
```

Dalam kasus ini, `len` akan menjadi `4`, yang berarti vector yang menyimpan
string `"Hola"` panjangnya 4 byte. Setiap huruf ini memakai 1 byte ketika
dikodekan dalam UTF-8. Namun, baris berikut mungkin mengejutkanmu (perhatikan
bahwa string ini dimulai dengan huruf Cyrillic kapital _Ze_, bukan angka 3):

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:russian}}
```

Jika kamu ditanya berapa panjang string itu, kamu mungkin menjawab 12. Kenyataannya,
jawaban Rust adalah 24: itulah jumlah byte yang dibutuhkan untuk mengkodekan
"Здравствуйте" dalam UTF-8, karena setiap Unicode scalar value dalam string itu
memakan 2 byte penyimpanan. Karena itu, indeks pada byte string tidak selalu
berkorespondensi dengan Unicode scalar value yang valid. Untuk mendemokannya,
perhatikan kode Rust yang tidak valid ini:

```rust,ignore,does_not_compile
let hello = "Здравствуйте";
let answer = &hello[0];
```

Kamu sudah tahu bahwa `answer` tidak akan menjadi `З`, huruf pertama. Ketika
dikodekan dalam UTF-8, byte pertama dari `З` adalah `208` dan byte kedua adalah
`151`, jadi tampaknya `answer` seharusnya menjadi `208`, tapi `208` bukan
karakter yang valid dengan sendirinya. Mengembalikan `208` mungkin bukan yang
diinginkan pengguna jika mereka meminta huruf pertama string ini; namun, itu
adalah satu-satunya data yang dimiliki Rust pada indeks byte 0. Pengguna umumnya
tidak ingin nilai byte yang dikembalikan, bahkan jika string hanya berisi huruf
Latin: Jika `&"hi"[0]` adalah kode valid yang mengembalikan nilai byte, kode itu
akan mengembalikan `104`, bukan `h`.

Jawabannya, untuk menghindari pengembalian nilai yang tidak terduga dan mencegah
bug yang mungkin tidak langsung ditemukan, Rust tidak mengompilasi kode ini
sama sekali dan mencegah kesalahpahaman sedini mungkin dalam proses pengembangan.

<!-- Old headings. Do not remove or links may break. -->

<a id="bytes-and-scalar-values-and-grapheme-clusters-oh-my"></a>

#### Byte, Scalar Value, dan Grapheme Cluster

Poin lain tentang UTF-8 adalah sebenarnya ada tiga cara relevan untuk melihat
string dari sudut pandang Rust: sebagai byte, scalar value, dan grapheme cluster
(yang paling mendekati apa yang kita sebut _huruf_).

Jika kita melihat kata Hindi "नमस्ते" yang ditulis dengan aksara Devanagari,
kata itu disimpan sebagai vector nilai `u8` yang tampak seperti ini:

```text
[224, 164, 168, 224, 164, 174, 224, 164, 184, 224, 165, 141, 224, 164, 164,
224, 165, 135]
```

Itu 18 byte dan itulah cara komputer pada akhirnya menyimpan data ini. Jika kita
melihatnya sebagai Unicode scalar value, yaitu tipe `char` milik Rust, byte-byte
tersebut tampak seperti ini:

```text
['न', 'म', 'स', '्', 'त', 'े']
```

Ada enam nilai `char` di sini, tapi yang keempat dan keenam bukan huruf: keduanya
diakritik yang tidak bermakna sendirian. Terakhir, jika kita melihatnya sebagai
grapheme cluster, kita akan mendapat apa yang disebut orang sebagai empat huruf
penyusun kata Hindi:

```text
["न", "म", "स्", "ते"]
```

Rust menyediakan cara-cara berbeda untuk menafsirkan data string mentah yang
disimpan komputer sehingga setiap program bisa memilih tafsiran yang ia butuhkan,
terlepas dari bahasa manusia mana data itu berasal.

Alasan terakhir Rust tidak mengizinkan kita mengindeks `String` untuk mendapatkan
karakter adalah karena operasi indeks diharapkan selalu berjalan dalam waktu
konstan (O(1)). Tapi mustahil menjamin performa itu dengan `String`, karena Rust
harus menelusuri isi dari awal sampai indeks untuk menentukan berapa banyak
karakter valid yang ada.

### Memotong String

Mengindeks string sering kali buruk karena tidak jelas seharusnya tipe kembalian
dari operasi indeks string berupa apa: nilai byte, karakter, grapheme cluster,
atau string slice. Karena itu, jika kamu benar-benar perlu memakai indeks untuk
membuat string slice, Rust meminta kamu lebih spesifik.

Alih-alih mengindeks dengan `[]` dan satu angka, kamu bisa memakai `[]` dengan
rentang untuk membuat string slice yang berisi byte tertentu:

```rust
let hello = "Здравствуйте";

let s = &hello[0..4];
```

Di sini, `s` akan menjadi `&str` yang berisi 4 byte pertama string. Tadi kita
menyebut setiap karakter ini berukuran 2 byte, yang berarti `s` akan menjadi
`Зд`.

Jika kita mencoba memotong hanya sebagian byte dari sebuah karakter dengan
sesuatu seperti `&hello[0..1]`, Rust akan panic di runtime dengan cara yang sama
seakan indeks tidak valid diakses pada sebuah vector:

```console
{{#include ../listings/ch08-common-collections/output-only-01-not-char-boundary/output.txt}}
```

Kamu harus berhati-hati ketika membuat string slice dengan rentang, karena
melakukannya bisa membuat programmu crash.

<!-- Old headings. Do not remove or links may break. -->

<a id="methods-for-iterating-over-strings"></a>

### Mengiterasi String

Cara terbaik untuk mengoperasikan potongan-potongan string adalah dengan
menyatakan secara eksplisit apakah kamu menginginkan karakter atau byte. Untuk
Unicode scalar value individual, gunakan method `chars`. Memanggil `chars` pada
"Зд" akan memisahkan dan mengembalikan dua nilai bertipe `char`, dan kamu bisa
mengiterasi hasilnya untuk mengakses setiap elemen:

```rust
for c in "Зд".chars() {
    println!("{c}");
}
```

Kode ini akan mencetak berikut:

```text
З
д
```

Sebagai alternatif, method `bytes` mengembalikan setiap byte mentah, yang mungkin
lebih sesuai untuk domain kamu:

```rust
for b in "Зд".bytes() {
    println!("{b}");
}
```

Kode ini akan mencetak 4 byte penyusun string ini:

```text
208
151
208
180
```

Tapi pastikan untuk selalu ingat bahwa Unicode scalar value yang valid bisa
terdiri dari lebih dari 1 byte.

Mendapatkan grapheme cluster dari string, seperti pada aksara Devanagari, adalah
hal yang rumit, sehingga fungsi ini tidak disediakan oleh standard library. Crate
tersedia di [crates.io](https://crates.io/)<!-- ignore --> jika itu adalah
fungsionalitas yang kamu butuhkan.

<!-- Old headings. Do not remove or links may break. -->

<a id="strings-are-not-so-simple"></a>

### Menangani Kerumitan String

Sebagai ringkasan, string itu rumit. Bahasa pemrograman yang berbeda membuat
pilihan berbeda tentang cara menyajikan kerumitan ini kepada programmer. Rust
memilih menjadikan penanganan `String` yang benar sebagai perilaku bawaan untuk
semua program Rust, yang berarti programmer harus berpikir lebih keras saat
menangani data UTF-8 sejak awal. Trade-off ini menampilkan lebih banyak kerumitan
string daripada yang terlihat di bahasa pemrograman lain, tapi mencegah kamu
dari kesulitan menangani error yang melibatkan karakter non-ASCII di kemudian
hari dalam siklus pengembanganmu.

Kabar baiknya, standard library menawarkan banyak fungsi yang dibangun di atas
tipe `String` dan `&str` untuk membantu menangani situasi yang rumit ini dengan
benar. Pastikan untuk memeriksa dokumentasi method berguna seperti `contains`
untuk mencari dalam string dan `replace` untuk mengganti bagian string dengan
string lain.

Mari kita beralih ke sesuatu yang sedikit lebih sederhana: hash map!
