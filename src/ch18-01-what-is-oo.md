## Karakteristik Bahasa Berorientasi Objek

Tidak ada konsensus di komunitas pemrograman tentang fitur apa yang harus dimiliki sebuah bahasa agar dianggap berorientasi objek. Rust dipengaruhi oleh banyak paradigma pemrograman, termasuk OOP; misalnya, kita menjelajahi fitur-fitur yang berasal dari pemrograman fungsional di Bab 13. Bisa dibilang, bahasa OOP memiliki beberapa karakteristik umum—yaitu objek, enkapsulasi, dan pewarisan. Mari kita lihat apa arti masing-masing karakteristik itu dan apakah Rust mendukungnya.

### Objek Berisi Data dan Perilaku

Buku _Design Patterns: Elements of Reusable Object-Oriented Software_ karya Erich Gamma, Richard Helm, Ralph Johnson, dan John Vlissides (Addison-Wesley, 1994), yang biasa disebut buku _The Gang of Four_, adalah katalog pola desain berorientasi objek. Buku itu mendefinisikan OOP sebagai berikut:

> Program berorientasi objek terdiri dari objek-objek. Sebuah **objek**
> membungkus data dan prosedur yang beroperasi pada data itu. Prosedur tersebut
> biasanya disebut **method** atau **operasi**.

Dengan definisi ini, Rust adalah bahasa berorientasi objek: struct dan enum memiliki data, dan blok `impl` menyediakan method pada struct dan enum. Meski struct dan enum yang punya method tidak _disebut_ objek, keduanya memberikan fungsionalitas yang sama, sesuai definisi objek versi Gang of Four.

<a id="encapsulation-that-hides-implementation-details"></a>
### Enkapsulasi yang Menyembunyikan Detail Implementasi

Aspek lain yang biasanya diasosiasikan dengan OOP adalah gagasan _enkapsulasi_, yang berarti detail implementasi sebuah objek tidak bisa diakses oleh kode yang memakai objek itu. Dengan demikian, satu-satunya cara berinteraksi dengan objek adalah lewat API publiknya; kode yang memakai objek seharusnya tidak bisa masuk ke dalam internal objek dan mengubah data atau perilakunya secara langsung. Ini memungkinkan programmer mengubah dan merefaktor internal objek tanpa perlu mengubah kode yang memakainya.

Kita sudah membahas cara mengontrol enkapsulasi di Bab 7: kita bisa memakai keyword `pub` untuk memutuskan module, tipe, fungsi, dan method mana dalam kode kita yang boleh publik, dan secara default semuanya bersifat private. Misalnya, kita bisa mendefinisikan struct `AveragedCollection` yang memiliki field berisi vector nilai `i32`. Struct ini juga bisa punya field yang berisi rata-rata nilai-nilai dalam vector itu, sehingga rata-ratanya tidak perlu dihitung setiap kali ada yang membutuhkannya. Dengan kata lain, `AveragedCollection` akan menyimpan hasil rata-rata yang sudah dihitung untuk kita. Listing 18-1 berisi definisi struct `AveragedCollection`.

<Listing number="18-1" file-name="src/lib.rs" caption="Sebuah struct `AveragedCollection` yang menyimpan daftar bilangan bulat dan rata-rata item dalam koleksi">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-01/src/lib.rs}}
```

</Listing>

Struct ini ditandai `pub` agar kode lain bisa memakainya, tetapi field-field di dalamnya tetap private. Ini penting di sini karena kita ingin memastikan bahwa setiap kali sebuah nilai ditambahkan atau dihapus dari daftar, rata-ratanya juga ikut diperbarui. Kita melakukan ini dengan mengimplementasikan method `add`, `remove`, dan `average` pada struct, seperti yang terlihat di Listing 18-2.

<Listing number="18-2" file-name="src/lib.rs" caption="Implementasi method publik `add`, `remove`, dan `average` pada `AveragedCollection`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-02/src/lib.rs:here}}
```

</Listing>

Method publik `add`, `remove`, dan `average` adalah satu-satunya cara untuk mengakses atau mengubah data dalam sebuah instance `AveragedCollection`. Ketika sebuah item ditambahkan ke `list` dengan method `add` atau dihapus dengan method `remove`, masing-masing implementasinya memanggil method private `update_average` yang juga menangani pembaruan field `average`.

Kita membiarkan field `list` dan `average` tetap private agar tidak ada cara bagi kode eksternal untuk menambah atau menghapus item ke atau dari field `list` secara langsung; kalau tidak, field `average` bisa menjadi tidak sinkron ketika `list` berubah. Method `average` mengembalikan nilai di field `average`, sehingga kode eksternal bisa membaca `average` tetapi tidak bisa mengubahnya.

Karena kita sudah mengenkapsulasi detail implementasi struct `AveragedCollection`, kita bisa dengan mudah mengubah hal-hal seperti struktur data di kemudian hari. Misalnya, kita bisa memakai `HashSet<i32>` alih-alih `Vec<i32>` untuk field `list`. Selama signature method publik `add`, `remove`, dan `average` tetap sama, kode yang memakai `AveragedCollection` tidak perlu diubah. Seandainya kita justru membuat `list` menjadi publik, hal itu belum tentu berlaku: `HashSet<i32>` dan `Vec<i32>` punya method yang berbeda untuk menambah dan menghapus item, sehingga kode eksternal kemungkinan besar harus diubah kalau ia mengubah `list` secara langsung.

Jika enkapsulasi adalah aspek wajib agar sebuah bahasa dianggap berorientasi objek, maka Rust memenuhi syarat itu. Opsi untuk memakai `pub` atau tidak pada bagian-bagian kode yang berbeda memungkinkan enkapsulasi detail implementasi.

### Pewarisan sebagai Sistem Tipe dan sebagai Berbagi Kode

_Pewarisan_ adalah mekanisme yang memungkinkan sebuah objek mewarisi elemen dari definisi objek lain, sehingga mendapatkan data dan perilaku objek induk tanpa kamu harus mendefinisikannya lagi.

Jika sebuah bahasa harus punya pewarisan agar dianggap berorientasi objek, maka Rust bukanlah bahasa seperti itu. Tidak ada cara untuk mendefinisikan struct yang mewarisi field dan implementasi method struct induk tanpa memakai macro.

Namun, kalau kamu terbiasa punya pewarisan di kotak alat pemrogramanmu, kamu bisa memakai solusi lain di Rust, bergantung pada alasanmu meraih pewarisan sejak awal.

Kamu akan memilih pewarisan untuk dua alasan utama. Pertama adalah penggunaan ulang kode: kamu bisa mengimplementasikan perilaku tertentu untuk sebuah tipe, dan pewarisan memungkinkanmu memakai ulang implementasi itu untuk tipe lain. Kamu bisa melakukan ini secara terbatas dalam kode Rust dengan implementasi method default pada trait, yang sudah kamu lihat di Listing 10-14 ketika kita menambahkan implementasi default dari method `summarize` pada trait `Summary`. Tipe apa pun yang mengimplementasikan trait `Summary` akan memiliki method `summarize` tanpa perlu kode tambahan. Ini mirip dengan sebuah class induk yang punya implementasi sebuah method dan class anak yang mewarisinya juga punya implementasi method itu. Kita juga bisa mengganti implementasi default dari method `summarize` ketika mengimplementasikan trait `Summary`, yang mirip dengan class anak yang mengganti implementasi method yang diwariskan dari class induk.

Alasan lain memakai pewarisan berkaitan dengan sistem tipe: agar sebuah tipe anak bisa dipakai di tempat-tempat yang sama dengan tipe induknya. Ini juga disebut _polimorfisme_, yang berarti kamu bisa saling mengganti beberapa objek saat runtime kalau mereka memiliki karakteristik tertentu yang sama.

> ### Polimorfisme
>
> Bagi banyak orang, polimorfisme identik dengan pewarisan. Padahal,
> sebenarnya ini konsep yang lebih umum yang merujuk pada kode yang bisa
> bekerja dengan data dari berbagai tipe. Dalam pewarisan, tipe-tipe itu
> umumnya adalah subclass.
>
> Rust justru memakai generic untuk mengabstraksi berbagai kemungkinan tipe dan
> trait bound untuk membatasi apa yang harus disediakan tipe-tipe itu. Ini
> kadang disebut _polimorfisme parametrik terbatas_.

Rust memilih serangkaian kompromi yang berbeda dengan tidak menawarkan pewarisan. Pewarisan sering berisiko membagikan kode lebih dari yang diperlukan. Subclass seharusnya tidak selalu berbagi semua karakteristik class induknya, tetapi dengan pewarisan mereka akan melakukannya. Ini bisa membuat desain program kurang fleksibel. Pewarisan juga membuka kemungkinan memanggil method pada subclass yang tidak masuk akal atau yang menyebabkan error karena method itu tidak berlaku untuk subclass tersebut. Selain itu, beberapa bahasa hanya mengizinkan _pewarisan tunggal_ (artinya sebuah subclass hanya bisa mewarisi dari satu class), yang semakin membatasi fleksibilitas desain program.

Untuk alasan-alasan ini, Rust mengambil pendekatan berbeda dengan memakai trait object alih-alih pewarisan untuk mencapai polimorfisme saat runtime. Mari kita lihat cara kerja trait object.
