## Refutability: Apakah Sebuah Pattern Bisa Gagal Cocok

Pattern hadir dalam dua bentuk: refutable dan irrefutable. Pattern yang akan cocok untuk nilai apa pun yang diberikan disebut _irrefutable_. Contohnya adalah `x` pada statement `let x = 5;`, karena `x` cocok dengan apa saja dan dengan demikian tidak bisa gagal cocok. Pattern yang bisa gagal cocok untuk beberapa nilai disebut _refutable_. Contohnya adalah `Some(x)` pada ekspresi `if let Some(x) = a_value`, karena jika nilai di dalam variabel `a_value` adalah `None` dan bukan `Some`, pattern `Some(x)` tidak akan cocok.

Parameter fungsi, statement `let`, dan loop `for` hanya bisa menerima pattern irrefutable, karena program tidak bisa melakukan apa pun yang bermakna saat nilai tidak cocok. Ekspresi `if let` dan `while let` serta statement `let...else` menerima pattern refutable maupun irrefutable, tetapi compiler memberi peringatan untuk pattern irrefutable karena, berdasarkan definisinya, pattern itu dimaksudkan untuk menangani kemungkinan kegagalan: fungsi dari kondisional terletak pada kemampuannya melakukan hal yang berbeda bergantung pada berhasil atau gagalnya.

Secara umum, kamu tidak perlu terlalu memikirkan perbedaan antara pattern refutable dan irrefutable; namun, kamu tetap perlu akrab dengan konsep refutability agar bisa merespons saat melihatnya dalam pesan error. Dalam kasus seperti itu, kamu perlu mengubah pattern atau konstruksi yang memakai pattern tersebut, bergantung pada perilaku yang diharapkan dari kode.

Mari kita lihat contoh apa yang terjadi saat kita mencoba memakai pattern refutable di tempat Rust membutuhkan pattern irrefutable, dan sebaliknya. Listing 19-8 menunjukkan sebuah statement `let`, tetapi untuk pattern-nya kita menentukan `Some(x)`, sebuah pattern refutable. Seperti yang mungkin kamu duga, kode ini tidak akan terkompilasi.

<Listing number="19-8" caption="Mencoba memakai pattern refutable dengan `let`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-08/src/main.rs:here}}
```

</Listing>

Jika `some_option_value` bernilai `None`, nilai itu akan gagal cocok dengan pattern `Some(x)`, yang berarti pattern tersebut refutable. Namun, statement `let` hanya bisa menerima pattern irrefutable karena tidak ada hal valid yang bisa dilakukan kode dengan nilai `None`. Saat mengompilasi, Rust akan mengeluh bahwa kita mencoba memakai pattern refutable di tempat yang membutuhkan pattern irrefutable:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-08/output.txt}}
```

Karena kita tidak mencakup (dan tidak bisa mencakup!) setiap nilai valid dengan pattern `Some(x)`, Rust dengan tepat menghasilkan error compiler.

Jika kita memiliki pattern refutable di tempat yang membutuhkan pattern irrefutable, kita bisa memperbaikinya dengan mengubah kode yang memakai pattern tersebut: Alih-alih memakai `let`, kita bisa memakai `let...else`. Dengan begitu, jika pattern tidak cocok, kode di dalam kurung kurawal akan menangani nilainya. Listing 19-9 menunjukkan cara memperbaiki kode di Listing 19-8.

<Listing number="19-9" caption="Memakai `let...else` dan sebuah blok dengan pattern refutable sebagai ganti `let`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-09/src/main.rs:here}}
```

</Listing>

Kita sudah memberi jalan keluar bagi kode ini! Kode ini sepenuhnya valid, meski berarti kita tidak bisa memakai pattern irrefutable tanpa mendapat peringatan. Jika kita memberi `let...else` pattern yang selalu cocok, seperti `x`, seperti yang ditunjukkan Listing 19-10, compiler akan memberi peringatan.

<Listing number="19-10" caption="Mencoba memakai pattern irrefutable dengan `let...else`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-10/src/main.rs:here}}
```

</Listing>

Rust mengeluh bahwa tidak masuk akal memakai `let...else` dengan pattern irrefutable karena `else` tidak akan pernah tercapai:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-10/output.txt}}
```

Untuk alasan ini, cabang match harus memakai pattern refutable, kecuali cabang terakhir, yang seharusnya cocok dengan nilai apa pun yang tersisa memakai pattern irrefutable. Rust mengizinkan kita memakai pattern irrefutable dalam `match` yang hanya punya satu cabang, tetapi sintaks ini tidak terlalu berguna dan bisa diganti dengan statement `let` yang lebih sederhana.

Sekarang setelah kamu tahu di mana memakai pattern dan perbedaan antara pattern refutable dan irrefutable, mari kita bahas semua sintaks yang bisa kita pakai untuk membuat pattern.
