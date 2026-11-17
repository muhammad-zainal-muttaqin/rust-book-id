## Menyimpan Daftar Nilai dengan Vector

Jenis koleksi pertama yang kita bahas adalah `Vec<T>`, yang juga dikenal sebagai
*vector*. Vector memungkinkan kamu menyimpan lebih dari satu nilai dalam satu
struktur data yang menaruh semua nilai tersebut bersebelahan di memori. Vector
hanya bisa menyimpan nilai dengan tipe yang sama. Vector berguna saat kamu punya
daftar item, misalnya baris teks dalam sebuah file atau harga-harga barang dalam
troli belanja.

### Membuat Vector Baru

Untuk membuat vector baru yang kosong, kita memanggil fungsi `Vec::new`, seperti
ditampilkan pada Listing 8-1.

<Listing number="8-1" caption="Creating a new, empty vector to hold values of type `i32`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-01/src/main.rs:here}}
```

</Listing>

Perhatikan bahwa kita menambahkan anotasi tipe di sini. Karena kita belum
memasukkan nilai apa pun ke dalam vector ini, Rust tidak tahu jenis elemen yang
kita simpan. Ini poin penting. Vector diimplementasikan dengan generic; kita
akan membahas cara memakai generic dengan tipe buatanmu sendiri di Bab 10.
Untuk saat ini, cukup ketahui bahwa tipe `Vec<T>` yang disediakan standard
library bisa menampung tipe apa pun. Saat kita membuat vector untuk menampung
tipe tertentu, kita bisa menyebutkan tipe tersebut di dalam kurung siku. Pada
Listing 8-1, kita sudah memberi tahu Rust bahwa `Vec<T>` di `v` akan menampung
elemen bertipe `i32`.

Lebih sering, kamu akan membuat `Vec<T>` dengan nilai awal, dan Rust akan
menyimpulkan tipe nilai yang ingin kamu simpan, sehingga jarang sekali kamu
perlu menulis anotasi tipe seperti ini. Rust menyediakan macro `vec!` yang
praktis; macro itu akan membuat vector baru yang menampung nilai-nilai yang kamu
berikan. Listing 8-2 membuat `Vec<i32>` baru yang menampung nilai `1`, `2`, dan
`3`. Tipe integer-nya adalah `i32` karena itu adalah tipe integer bawaan, seperti
yang kita bahas di bagian [“Tipe Data”][data-types]<!-- ignore --> pada Bab 3.

<Listing number="8-2" caption="Creating a new vector containing values">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-02/src/main.rs:here}}
```

</Listing>

Karena kita sudah memberi nilai awal bertipe `i32`, Rust bisa menyimpulkan bahwa
tipe `v` adalah `Vec<i32>`, sehingga anotasi tipe tidak diperlukan. Selanjutnya,
kita akan melihat cara mengubah vector.

### Memperbarui Vector

Untuk membuat vector lalu menambahkan elemen ke dalamnya, kita bisa memakai
metode `push`, seperti ditampilkan pada Listing 8-3.

<Listing number="8-3" caption="Using the `push` method to add values to a vector">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-03/src/main.rs:here}}
```

</Listing>

Seperti variabel lain, jika kita ingin bisa mengubah nilainya, kita perlu
membuatnya mutable dengan kata kunci `mut`, seperti dibahas di Bab 3. Angka-angka
yang kita masukkan semuanya bertipe `i32`, dan Rust menyimpulkan hal itu dari
datanya, jadi kita tidak perlu anotasi `Vec<i32>`.

### Membaca Elemen Vector

Ada dua cara untuk mereferensikan nilai yang tersimpan di dalam vector: lewat
indeks atau dengan memakai metode `get`. Pada contoh-contoh berikut, kita
memberikan anotasi tipe pada nilai yang dikembalikan oleh fungsi-fungsi itu
agar lebih jelas.

Listing 8-4 menampilkan kedua cara mengakses sebuah nilai dalam vector, yaitu
sintaks indeks dan metode `get`.

<Listing number="8-4" caption="Using indexing syntax and using the `get` method to access an item in a vector">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-04/src/main.rs:here}}
```

</Listing>

Perhatikan beberapa hal di sini. Kita memakai nilai indeks `2` untuk mengambil
elemen ketiga karena vector diindeks berdasarkan angka, dimulai dari nol.
Memakai `&` dan `[]` memberikan kita reference ke elemen pada nilai indeks
tersebut. Saat kita memakai metode `get` dengan indeks yang diteruskan sebagai
argumen, kita mendapat `Option<&T>` yang bisa dipakai bersama `match`.

Rust menyediakan dua cara untuk mereferensikan sebuah elemen agar kamu bisa
memilih perilaku program saat kamu mencoba memakai nilai indeks yang berada di
luar rentang elemen yang ada. Sebagai contoh, mari kita lihat apa yang terjadi
saat kita punya vector berisi lima elemen lalu mencoba mengakses elemen pada
indeks 100 dengan masing-masing teknik, seperti ditampilkan pada Listing 8-5.

<Listing number="8-5" caption="Attempting to access the element at index 100 in a vector containing five elements">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-05/src/main.rs:here}}
```

</Listing>

Saat kita menjalankan kode ini, cara pertama dengan `[]` akan membuat program
panic karena mereferensikan elemen yang tidak ada. Cara ini paling tepat dipakai
jika kamu ingin program crash ketika ada upaya mengakses elemen melewati akhir
vector.

Saat metode `get` diberikan indeks yang berada di luar vector, metode itu
mengembalikan `None` tanpa panic. Kamu akan memakai metode ini jika akses ke
elemen di luar rentang vector mungkin terjadi sesekali dalam keadaan normal.
Kode kamu lalu punya logika untuk menangani kondisi `Some(&element)` maupun
`None`, seperti dibahas di Bab 6. Sebagai contoh, indeksnya bisa berasal dari
inputan angka seorang pengguna. Jika mereka tidak sengaja memasukkan angka yang
terlalu besar dan program mendapat nilai `None`, kamu bisa memberi tahu pengguna
berapa banyak item yang ada di vector saat ini lalu memberi mereka kesempatan
lain untuk memasukkan nilai yang valid. Itu akan lebih ramah pengguna daripada
membuat program crash gara-gara salah ketik!

Saat program punya reference yang valid, borrow checker menegakkan aturan
ownership dan borrowing (dibahas di Bab 4) untuk memastikan reference ini dan
reference lain ke isi vector tetap valid. Ingat aturan yang menyatakan bahwa kamu
tidak boleh punya reference mutable dan immutable dalam scope yang sama. Aturan
itu berlaku pada Listing 8-6, di mana kita menahan reference immutable ke elemen
pertama dalam sebuah vector lalu mencoba menambahkan elemen di akhir. Program
ini tidak akan bisa berjalan jika kita juga mencoba merujuk ke elemen tersebut
nanti di dalam fungsi.

<Listing number="8-6" caption="Attempting to add an element to a vector while holding a reference to an item">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-06/src/main.rs:here}}
```

</Listing>

Mengompilasi kode ini akan menghasilkan error berikut:

```console
{{#include ../listings/ch08-common-collections/listing-08-06/output.txt}}
```

Kode di Listing 8-6 mungkin terlihat seharusnya bisa bekerja: mengapa reference
ke elemen pertama harus peduli dengan perubahan di akhir vector? Error ini
muncul karena cara kerja vector: karena vector menaruh nilai-nilainya
bersebelahan di memori, menambahkan elemen baru di akhir vector mungkin
membutuhkan alokasi memori baru dan menyalin elemen-elemen lama ke ruang baru,
jika ruangnya tidak cukup untuk menaruh semua elemen bersebelahan di tempat
vector saat ini disimpan. Dalam kasus itu, reference ke elemen pertama akan
menunjuk ke memori yang sudah dialokasikan ulang. Aturan borrowing mencegah
program berada dalam kondisi seperti itu.

> Catatan: Untuk lebih jauh tentang detail implementasi tipe `Vec<T>`, lihat
> [“The Rustonomicon”][nomicon].

### Mengiterasi Nilai dalam Vector

Untuk mengakses setiap elemen dalam sebuah vector bergantian, kita akan
mengiterasi semua elemen tersebut alih-alih memakai indeks untuk mengaksesnya
satu per satu. Listing 8-7 menunjukkan cara memakai loop `for` untuk mendapatkan
reference immutable ke setiap elemen dalam sebuah vector berisi nilai `i32` lalu
mencetaknya.

<Listing number="8-7" caption="Printing each element in a vector by iterating over the elements using a `for` loop">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-07/src/main.rs:here}}
```

</Listing>

Kita juga bisa mengiterasi reference mutable ke setiap elemen dalam sebuah vector
mutable untuk mengubah semua elemennya. Loop `for` pada Listing 8-8 akan
menambahkan `50` ke setiap elemen.

<Listing number="8-8" caption="Iterating over mutable references to elements in a vector">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-08/src/main.rs:here}}
```

</Listing>

Untuk mengubah nilai yang dirujuk oleh reference mutable, kita harus memakai
operator dereference `*` untuk mencapai nilai di dalam `i` sebelum kita bisa
memakai operator `+=`. Kita akan membahas operator dereference lebih lanjut di
bagian [“Mengikuti Reference ke Nilai”][deref]<!-- ignore --> pada Bab 15.

Mengiterasi sebuah vector, baik secara immutable maupun mutable, aman berkat
aturan borrow checker. Jika kita mencoba menyisipkan atau menghapus item di
dalam badan loop `for` pada Listing 8-7 dan Listing 8-8, kita akan mendapat
error compiler yang mirip dengan yang kita dapat pada kode di Listing 8-6.
Reference ke vector yang dipegang oleh loop `for` mencegah perubahan terhadap
seluruh vector secara bersamaan.

### Memakai Enum untuk Menyimpan Beberapa Tipe

Vector hanya bisa menyimpan nilai dengan tipe yang sama. Hal ini bisa merepotkan;
memang ada kasus penggunaan yang membutuhkan penyimpanan daftar item dengan
tipe berbeda. Untungnya, varian-varian sebuah enum didefinisikan di bawah tipe
enum yang sama, jadi saat kita butuh satu tipe untuk mewakili elemen-elemen
dengan tipe berbeda, kita bisa mendefinisikan dan memakai sebuah enum!

Sebagai contoh, misalkan kita ingin mengambil nilai dari sebuah baris dalam
spreadsheet di mana sebagian kolom pada baris itu berisi integer, sebagian
angka floating-point, dan sebagian string. Kita bisa mendefinisikan sebuah enum
yang varian-variannya akan menampung tipe-tipe nilai berbeda tersebut, dan semua
varian enum akan dianggap bertipe sama, yaitu tipe enum-nya. Dengan begitu, kita
bisa membuat vector untuk menampung enum itu dan pada akhirnya menampung
tipe-tipe yang berbeda. Kita sudah mendemonstrasikannya pada Listing 8-9.

<Listing number="8-9" caption="Defining an enum to store values of different types in one vector">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-09/src/main.rs:here}}
```

</Listing>

Rust perlu mengetahui tipe-tipe apa yang akan ada di dalam vector pada waktu
compile agar Rust tahu persis berapa banyak memori di heap yang dibutuhkan untuk
menyimpan setiap elemen. Kita juga harus eksplisit soal tipe-tipe yang diizinkan
dalam vector ini. Jika Rust mengizinkan sebuah vector menampung tipe apa pun,
bisa jadi salah satu atau lebih dari tipe-tipe itu menimbulkan error saat
operasi-operandi dijalankan pada elemen-elemen vector. Memakai enum plus
ekspresi `match` berarti Rust akan menjamin pada waktu compile bahwa setiap
kemungkinan kasus tertangani, seperti dibahas di Bab 6.

Jika kamu tidak mengetahui kumpulan tipe lengkap yang akan diterima program saat
runtime untuk disimpan dalam sebuah vector, teknik enum tidak akan bekerja.
Sebagai gantinya, kamu bisa memakai trait object, yang akan kita bahas di Bab 18.

Setelah kita membahas beberapa cara paling umum memakai vector, pastikan kamu
meninjau [dokumentasi API][vec-api]<!-- ignore --> untuk semua metode berguna
yang didefinisikan pada `Vec<T>` oleh standard library. Sebagai contoh, selain
`push`, ada metode `pop` yang menghapus dan mengembalikan elemen terakhir.

### Membuang Vector Juga Membuang Elemen-nya

Seperti `struct` lainnya, sebuah vector dibebaskan saat keluar dari scope, seperti
ditandai pada Listing 8-10.

<Listing number="8-10" caption="Showing where the vector and its elements are dropped">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-10/src/main.rs:here}}
```

</Listing>

Saat vector dibuang, seluruh isinya juga dibuang, artinya integer yang ditampung
di dalamnya akan dibersihkan. Borrow checker memastikan bahwa reference apa pun
ke isi sebuah vector hanya dipakai selama vector itu sendiri masih valid.

Mari kita lanjut ke jenis koleksi berikutnya: `String`!

[data-types]: ch03-02-data-types.html#data-types
[nomicon]: ../nomicon/vec/vec.html
[vec-api]: ../std/vec/struct.Vec.html
[deref]: ch15-02-deref.html#following-the-pointer-to-the-value-with-the-dereference-operator
