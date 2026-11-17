# Generic Types, Traits, dan Lifetimes

Setiap bahasa pemrograman punya alat untuk menangani duplikasi konsep secara efektif. Di Rust, salah satu alat itu adalah _generics_: pengganti abstrak untuk tipe konkret atau properti lain. Kita bisa mengungkapkan perilaku generics atau bagaimana mereka berhubungan dengan generics lain tanpa perlu tahu apa yang akan mengisi tempat itu saat kode dikompilasi dan dijalankan.

Fungsi bisa menerima parameter bertipe generic, bukan tipe konkret seperti `i32` atau `String`, dengan cara yang sama seperti mereka menerima parameter bernilai tak dikenal untuk menjalankan kode yang sama pada beberapa nilai konkret. Sebenarnya, kita sudah memakai generics di Bab 6 dengan `Option<T>`, di Bab 8 dengan `Vec<T>` dan `HashMap<K, V>`, serta di Bab 9 dengan `Result<T, E>`. Di bab ini, kamu akan mempelajari cara mendefinisikan tipe, fungsi, dan metode buatanmu sendiri dengan generics!

Pertama, kita akan meninjau cara mengekstrak fungsi untuk mengurangi duplikasi kode. Lalu kita akan memakai teknik yang sama untuk membuat fungsi generic dari dua fungsi yang hanya berbeda pada tipe parameternya. Kita juga akan menjelaskan cara memakai tipe generic dalam definisi struct dan enum.

Selanjutnya, kamu akan belajar cara memakai trait untuk mendefinisikan perilaku secara generic. Kamu bisa menggabungkan trait dengan tipe generic untuk membatasi sebuah tipe generic agar hanya menerima tipe-tipe yang punya perilaku tertentu, bukan sembarang tipe.

Terakhir, kita akan membahas _lifetimes_: varian generics yang memberi compiler informasi tentang bagaimana reference saling berhubungan. Lifetime memungkinkan kita memberi compiler informasi yang cukup tentang nilai yang dipinjam, sehingga ia bisa memastikan reference tetap valid dalam lebih banyak situasi dibanding jika kita tidak membantu.

## Menghilangkan Duplikasi dengan Mengekstrak Fungsi

Generics memungkinkan kita mengganti tipe-tipe spesifik dengan placeholder yang mewakili banyak tipe guna menghilangkan duplikasi kode. Sebelum menyelami sintaks generics, mari kita lihat dulu cara menghilangkan duplikasi dengan cara yang tidak melibatkan tipe generic, yaitu dengan mengekstrak fungsi yang mengganti nilai-nilai spesifik dengan placeholder yang mewakili banyak nilai. Setelah itu, kita akan menerapkan teknik yang sama untuk mengekstrak fungsi generic! Dengan mempelajari cara mengenali kode duplikat yang bisa kamu ekstrak menjadi fungsi, kamu akan mulai mengenali kode duplikat yang bisa memakai generics.

Kita mulai dengan program pendek di Listing 10-1 yang mencari angka terbesar dalam sebuah daftar.

<Listing number="10-1" file-name="src/main.rs" caption="Finding the largest number in a list of numbers">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-01/src/main.rs:here}}
```

</Listing>

Kita menyimpan daftar bilangan bulat dalam variabel `number_list` dan menempatkan reference ke angka pertama dalam daftar itu ke dalam variabel bernama `largest`. Lalu kita mengiterasi semua angka dalam daftar, dan jika angka saat ini lebih besar dari angka yang tersimpan di `largest`, kita mengganti reference di variabel itu. Namun, jika angka saat ini lebih kecil atau sama dengan angka terbesar yang pernah terlihat sejauh ini, variabelnya tidak berubah, dan kode berpindah ke angka berikutnya dalam daftar. Setelah mempertimbangkan semua angka dalam daftar, `largest` seharusnya merujuk ke angka terbesar, yang dalam kasus ini adalah 100.

Sekarang kita diminta mencari angka terbesar dalam dua daftar angka yang berbeda. Untuk melakukannya, kita bisa memilih menduplikasi kode di Listing 10-1 dan memakai logika yang sama di dua tempat berbeda dalam program, seperti ditunjukkan Listing 10-2.

<Listing number="10-2" file-name="src/main.rs" caption="Code to find the largest number in *two* lists of numbers">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-02/src/main.rs}}
```

</Listing>

Meski kode ini berfungsi, menduplikasi kode itu melelahkan dan rawan error. Kita juga harus ingat untuk memperbarui kode di banyak tempat ketika ingin mengubahnya.

Untuk menghilangkan duplikasi ini, kita akan membuat abstraksi dengan mendefinisikan fungsi yang beroperasi pada daftar bilangan bulat apa pun yang diteruskan sebagai parameter. Solusi ini membuat kode kita lebih jelas dan memungkinkan kita mengungkapkan konsep mencari angka terbesar dalam sebuah daftar secara abstrak.

Di Listing 10-3, kita mengekstrak kode yang mencari angka terbesar menjadi sebuah fungsi bernama `largest`. Lalu kita memanggil fungsi itu untuk mencari angka terbesar dalam dua daftar dari Listing 10-2. Kita juga bisa memakai fungsi tersebut pada daftar `i32` lain apa pun yang mungkin kita punya nanti.

<Listing number="10-3" file-name="src/main.rs" caption="Abstracted code to find the largest number in two lists">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-03/src/main.rs:here}}
```

</Listing>

Fungsi `largest` punya parameter bernama `list`, yang mewakili slice `i32` konkret apa pun yang mungkin kita teruskan ke fungsi itu. Akibatnya, saat kita memanggil fungsi tersebut, kode berjalan pada nilai-nilai spesifik yang kita teruskan.

Ringkasnya, berikut langkah-langkah yang kita ambil untuk mengubah kode dari Listing 10-2 menjadi Listing 10-3:

1. Kenali kode yang duplikat.
1. Ekstrak kode duplikat itu ke dalam badan fungsi, dan tentukan input serta nilai kembalian dari kode itu dalam signature fungsi.
1. Perbarui dua tempat kode duplikat itu agar memanggil fungsi tersebut.

Selanjutnya, kita akan memakai langkah-langkah yang sama dengan generics untuk mengurangi duplikasi kode. Sama seperti badan fungsi yang bisa beroperasi pada `list` abstrak alih-alih nilai-nilai spesifik, generics memungkinkan kode beroperasi pada tipe-tipe abstrak.

Sebagai contoh, misalkan kita punya dua fungsi: satu yang mencari item terbesar dalam slice nilai `i32`, dan satu lagi yang mencari item terbesar dalam slice nilai `char`. Bagaimana kita menghilangkan duplikasi itu? Mari cari tahu!
