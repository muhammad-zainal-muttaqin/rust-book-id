## Memproses Serangkaian Item dengan Iterator

Pola iterator memungkinkan kamu melakukan suatu tugas pada serangkaian item satu per satu. Sebuah iterator bertanggung jawab atas logika untuk mengiterasi setiap item dan menentukan kapan rangkaian tersebut selesai. Saat memakai iterator, kamu tidak perlu menerapkan kembali logika itu sendiri.

Di Rust, iterator bersifat _lazy_, artinya tidak ada efek apa pun sampai kamu memanggil metode yang mengonsumsi iterator tersebut hingga habis. Misalnya, kode di Listing 13-10 membuat iterator atas item-item dalam vector `v1` dengan memanggil metode `iter` yang didefinisikan pada `Vec<T>`. Kode ini sendiri tidak melakukan apa pun yang berguna.

<Listing number="13-10" file-name="src/main.rs" caption="Membuat iterator">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-10/src/main.rs:here}}
```

</Listing>

Iterator disimpan dalam variabel `v1_iter`. Setelah iterator dibuat, kita bisa memakainya dengan berbagai cara. Di Listing 3-5, kita mengiterasi sebuah array memakai loop `for` untuk menjalankan sejumlah kode pada setiap itemnya. Di balik layar, hal ini secara implisit membuat lalu mengonsumsi sebuah iterator, tetapi sampai sekarang kita belum membahas secara rinci cara kerjanya.

Pada contoh di Listing 13-11, kita memisahkan pembuatan iterator dari pemakaian iterator di dalam loop `for`. Saat loop `for` dipanggil dengan iterator dalam `v1_iter`, setiap elemen dalam iterator dipakai dalam satu iterasi loop, yang mencetak setiap nilai.

<Listing number="13-11" file-name="src/main.rs" caption="Memakai iterator dalam loop `for`">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-11/src/main.rs:here}}
```

</Listing>

Pada bahasa yang tidak menyediakan iterator di library standarnya, kamu akan menulis fungsionalitas yang sama dengan memulai sebuah variabel pada indeks 0, memakai variabel itu untuk mengakses vector dan mengambil sebuah nilai, lalu menambah nilai variabel tersebut di dalam loop sampai mencapai total jumlah item di vector.

Iterator menangani semua logika itu untukmu, mengurangi kode berulang yang bisa saja membuatmu membuat kesalahan. Iterator memberi kamu lebih banyak fleksibilitas untuk memakai logika yang sama dengan berbagai macam rangkaian, tidak hanya struktur data yang bisa diakses lewat indeks seperti vector. Mari kita lihat bagaimana iterator melakukan itu.

<a id="the-iterator-trait-and-the-next-method"></a>
### Trait `Iterator` dan Metode `next`

Semua iterator mengimplementasikan trait bernama `Iterator` yang didefinisikan di library standar. Definisi trait itu terlihat seperti ini:

```rust
pub trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;

    // methods with default implementations elided
}
```

Perhatikan bahwa definisi ini memakai beberapa sintaks baru: `type Item` dan `Self::Item`, yang mendefinisikan sebuah tipe terasosiasi dengan trait tersebut. Kita akan membahas tipe terasosiasi secara mendalam di Bab 20. Untuk sekarang, yang perlu kamu tahu adalah kode ini menyatakan bahwa mengimplementasikan trait `Iterator` mengharuskanmu mendefinisikan juga sebuah tipe `Item`, dan tipe `Item` ini dipakai dalam tipe kembalian metode `next`. Dengan kata lain, tipe `Item` adalah tipe yang dikembalikan oleh iterator.

Trait `Iterator` hanya mewajibkan implementornya mendefinisikan satu metode: metode `next`, yang mengembalikan satu item iterator pada satu waktu, dibungkus dalam `Some`, dan ketika iterasi selesai, mengembalikan `None`.

Kita bisa memanggil metode `next` langsung pada iterator; Listing 13-12 menunjukkan nilai apa yang dikembalikan dari pemanggilan `next` berulang kali pada iterator yang dibuat dari vector tersebut.

<Listing number="13-12" file-name="src/lib.rs" caption="Memanggil metode `next` pada sebuah iterator">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-12/src/lib.rs:here}}
```

</Listing>

Perhatikan bahwa kita perlu membuat `v1_iter` menjadi mutable: Memanggil metode `next` pada sebuah iterator mengubah keadaan internal yang dipakai iterator untuk melacak posisinya dalam rangkaian. Dengan kata lain, kode ini _mengonsumsi_, atau menggunakan habis, iterator itu. Setiap pemanggilan `next` memakan satu item dari iterator. Kita tidak perlu membuat `v1_iter` mutable saat memakai loop `for`, karena loop itu mengambil ownership `v1_iter` dan membuatnya mutable di balik layar.

Perhatikan juga bahwa nilai yang kita dapat dari pemanggilan `next` adalah reference immutable terhadap nilai-nilai di dalam vector. Metode `iter` menghasilkan iterator atas reference immutable. Jika kita ingin membuat iterator yang mengambil ownership `v1` dan mengembalikan nilai-nilai yang dimiliki, kita bisa memanggil `into_iter` alih-alih `iter`. Begitu pula, jika kita ingin mengiterasi reference mutable, kita bisa memanggil `iter_mut` alih-alih `iter`.

### Metode yang Mengonsumsi Iterator

Trait `Iterator` memiliki sejumlah metode berbeda dengan implementasi default yang disediakan library standar; kamu bisa mempelajari metode-metode ini lewat dokumentasi API library standar untuk trait `Iterator`. Beberapa metode ini memanggil metode `next` dalam definisinya, itulah sebabnya kamu wajib mengimplementasikan metode `next` saat mengimplementasikan trait `Iterator`.

Metode yang memanggil `next` disebut _consuming adapter_ karena memanggilnya menggunakan habis iterator. Salah satu contohnya adalah metode `sum`, yang mengambil ownership iterator dan mengiterasi item-itemnya dengan berulang kali memanggil `next`, sehingga mengonsumsi iterator itu. Saat mengiterasi, metode ini menjumlahkan setiap item ke total yang terus bertambah dan mengembalikan total tersebut ketika iterasi selesai. Listing 13-13 berisi test yang menunjukkan penggunaan metode `sum`.

<Listing number="13-13" file-name="src/lib.rs" caption="Memanggil metode `sum` untuk mendapatkan total semua item dalam iterator">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-13/src/lib.rs:here}}
```

</Listing>

Kita tidak boleh memakai `v1_iter` setelah pemanggilan `sum`, karena `sum` mengambil ownership iterator yang dipanggil padanya.

### Metode yang Menghasilkan Iterator Lain

_Iterator adapter_ adalah metode yang didefinisikan pada trait `Iterator` yang tidak mengonsumsi iterator. Sebaliknya, metode ini menghasilkan iterator lain dengan mengubah suatu aspek dari iterator asal.

Listing 13-14 menunjukkan contoh pemanggilan metode iterator adapter `map`, yang menerima sebuah closure untuk dipanggil pada setiap item saat item-item diiterasi. Metode `map` mengembalikan iterator baru yang menghasilkan item-item yang telah diubah. Closure di sini membuat iterator baru di mana setiap item dari vector akan ditambah 1.

<Listing number="13-14" file-name="src/main.rs" caption="Memanggil iterator adapter `map` untuk membuat iterator baru">

```rust,not_desired_behavior
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-14/src/main.rs:here}}
```

</Listing>

Akan tetapi, kode ini menghasilkan sebuah warning:

```console
{{#include ../listings/ch13-functional-features/listing-13-14/output.txt}}
```

Kode di Listing 13-14 tidak melakukan apa pun; closure yang kita tentukan tidak pernah dipanggil. Warning itu mengingatkan kita alasannya: iterator adapter bersifat lazy, dan kita perlu mengonsumsi iterator di sini.

Untuk memperbaiki warning ini dan mengonsumsi iterator, kita akan memakai metode `collect`, yang sudah kita pakai bersama `env::args` di Listing 12-1. Metode ini mengonsumsi iterator dan mengumpulkan nilai-nilai yang dihasilkan ke dalam sebuah tipe data koleksi.

Di Listing 13-15, kita mengumpulkan hasil iterasi atas iterator yang dikembalikan dari pemanggilan `map` ke dalam sebuah vector. Vector ini pada akhirnya akan berisi setiap item dari vector asal, yang telah ditambah 1.

<Listing number="13-15" file-name="src/main.rs" caption="Memanggil metode `map` untuk membuat iterator baru, lalu memanggil metode `collect` untuk mengonsumsi iterator baru itu dan membuat sebuah vector">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-15/src/main.rs:here}}
```

</Listing>

Karena `map` menerima sebuah closure, kita bisa menentukan operasi apa pun yang ingin kita lakukan pada setiap item. Ini adalah contoh yang bagus tentang bagaimana closure memungkinkan kamu menyesuaikan sebagian perilaku sambil tetap menggunakan kembali perilaku iterasi yang disediakan trait `Iterator`.

Kamu bisa merangkai beberapa pemanggilan iterator adapter untuk melakukan tindakan kompleks dengan cara yang mudah dibaca. Tetapi karena semua iterator bersifat lazy, kamu harus memanggil salah satu metode consuming adapter untuk mendapatkan hasil dari pemanggilan iterator adapter.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-closures-that-capture-their-environment"></a>

### Closure yang Menangkap Lingkungannya

Banyak iterator adapter menerima closure sebagai argumen, dan umumnya closure yang kita tentukan sebagai argumen iterator adapter adalah closure yang menangkap lingkungannya.

Untuk contoh ini, kita akan memakai metode `filter` yang menerima sebuah closure. Closure itu menerima satu item dari iterator dan mengembalikan sebuah `bool`. Jika closure mengembalikan `true`, nilai itu akan disertakan dalam iterator yang dihasilkan `filter`. Jika closure mengembalikan `false`, nilai itu tidak akan disertakan.

Di Listing 13-16, kita memakai `filter` dengan sebuah closure yang menangkap variabel `shoe_size` dari lingkungannya untuk mengiterasi koleksi instance struct `Shoe`. Fungsi ini akan mengembalikan hanya sepatu yang berukuran sesuai yang ditentukan.

<Listing number="13-16" file-name="src/lib.rs" caption="Memakai metode `filter` dengan closure yang menangkap `shoe_size`">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-16/src/lib.rs}}
```

</Listing>

Fungsi `shoes_in_size` mengambil ownership sebuah vector berisi sepatu dan sebuah ukuran sepatu sebagai parameter. Fungsi ini mengembalikan vector yang berisi hanya sepatu dengan ukuran yang ditentukan.

Di dalam tubuh `shoes_in_size`, kita memanggil `into_iter` untuk membuat iterator yang mengambil ownership vector tersebut. Lalu, kita memanggil `filter` untuk mengadaptasi iterator itu menjadi iterator baru yang hanya berisi elemen-elemen yang membuat closure mengembalikan `true`.

Closure itu menangkap parameter `shoe_size` dari lingkungannya dan membandingkan nilainya dengan ukuran setiap sepatu, hanya menyimpan sepatu dengan ukuran yang ditentukan. Terakhir, pemanggilan `collect` mengumpulkan nilai-nilai yang dikembalikan oleh iterator yang telah diadaptasi ke dalam sebuah vector yang dikembalikan oleh fungsi.

Test tersebut menunjukkan bahwa ketika kita memanggil `shoes_in_size`, kita mendapatkan kembali hanya sepatu yang ukurannya sama dengan nilai yang kita tentukan.
