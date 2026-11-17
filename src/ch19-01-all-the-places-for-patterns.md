## Semua Tempat *Pattern* Bisa Digunakan

*Pattern* muncul di banyak tempat dalam Rust, dan kamu sudah sering menggunakannya tanpa sadar! Bagian ini membahas semua tempat yang membolehkan penggunaan pattern.

### Cabang-cabang `match`

Seperti yang kita bahas di Bab 6, kita memakai *pattern* pada cabang-cabang ekspresi `match`. Secara formal, ekspresi `match` terdiri dari keyword `match`, sebuah nilai yang akan dicocokkan, dan satu atau lebih cabang match yang berisi sebuah pattern serta ekspresi yang dijalankan jika nilai itu cocok dengan pattern cabang tersebut, seperti ini:

<!--
  Manually formatted rather than using Markdown intentionally: Markdown does not
  support italicizing code in the body of a block like this!
-->

<pre><code>match <em>VALUE</em> {
    <em>PATTERN</em> => <em>EXPRESSION</em>,
    <em>PATTERN</em> => <em>EXPRESSION</em>,
    <em>PATTERN</em> => <em>EXPRESSION</em>,
}</code></pre>

Misalnya, ini ekspresi `match` dari Listing 6-5 yang mencocokkan nilai `Option<i32>` dalam variabel `x`:

```rust,ignore
match x {
    None => None,
    Some(i) => Some(i + 1),
}
```

Pattern dalam ekspresi `match` ini adalah `None` dan `Some(i)` di sebelah kiri setiap panah.

Salah satu syarat ekspresi `match` adalah harus bersifat exhaustif, artinya semua kemungkinan nilai dalam ekspresi `match` harus tercakup. Salah satu cara untuk memastikan kamu telah mencakup semua kemungkinan adalah dengan menaruh pattern catch-all pada cabang terakhir. Misalnya, nama variabel yang mencocokkan nilai apa pun tidak akan pernah gagal, sehingga mencakup semua kasus yang tersisa.

Pattern khusus `_` akan mencocokkan apa pun, tetapi tidak pernah mengikat nilai ke sebuah variabel, jadi pattern ini sering dipakai pada cabang match terakhir. Pattern `_` bisa berguna, misalnya, ketika kamu ingin mengabaikan nilai apa pun yang tidak disebutkan. Kita akan membahas pattern `_` lebih lanjut di ["Mengabaikan Nilai dalam Pattern"][ignoring-values-in-a-pattern] nanti dalam bab ini.

### Statement `let`

Sebelum bab ini, kita baru secara eksplisit membahas penggunaan *pattern* bersama `match` dan `if let`, tetapi sebenarnya kita juga sudah memakai pattern di tempat lain, termasuk dalam statement `let`. Misalnya, perhatikan penugasan variabel sederhana dengan `let` ini:

```rust
let x = 5;
```

Setiap kali kamu memakai statement `let` seperti ini, kamu sebenarnya memakai pattern, meski mungkin tidak menyadarinya! Secara lebih formal, statement `let` terlihat seperti ini:

<!--
  Manually formatted rather than using Markdown intentionally: Markdown does not
  support italicizing code in the body of a block like this!
-->

<pre>
<code>let <em>PATTERN</em> = <em>EXPRESSION</em>;</code>
</pre>

Pada statement seperti `let x = 5;` yang memuat nama variabel di slot PATTERN, nama variabel itu hanyalah bentuk pattern yang sangat sederhana. Rust membandingkan ekspresi dengan pattern lalu menetapkan nama-nama yang ditemukannya. Jadi, pada contoh `let x = 5;`, `x` adalah pattern yang artinya "ikat apa yang cocok di sini ke variabel `x`." Karena nama `x` merupakan keseluruhan pattern, pattern ini pada dasarnya berarti "ikat semuanya ke variabel `x`, apa pun nilainya."

Untuk melihat sisi pencocokan pola dari `let` dengan lebih jelas, perhatikan Listing 19-1, yang memakai pattern bersama `let` untuk mendestrukturisasi sebuah tuple.


<Listing number="19-1" caption="Memakai pattern untuk mendestrukturisasi tuple dan membuat tiga variabel sekaligus">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-01/src/main.rs:here}}
```

</Listing>

Di sini, kita mencocokkan sebuah tuple dengan sebuah pattern. Rust membandingkan nilai `(1, 2, 3)` dengan pattern `(x, y, z)` dan mendapati bahwa nilainya cocok dengan pattern itu—artinya, jumlah elemennya sama pada keduanya—lalu Rust mengikat `1` ke `x`, `2` ke `y`, dan `3` ke `z`. Kamu bisa membayangkan tuple pattern ini sebagai tiga pattern variabel tersendiri yang bersarang di dalamnya.

Jika jumlah elemen dalam pattern tidak sama dengan jumlah elemen dalam tuple, tipe secara keseluruhan tidak akan cocok dan kita akan mendapat error dari compiler. Misalnya, Listing 19-2 menunjukkan percobaan mendestrukturisasi tuple dengan tiga elemen menjadi dua variabel, yang tidak akan berhasil.

<Listing number="19-2" caption="Membuat pattern yang salah karena jumlah variabelnya tidak sama dengan jumlah elemen dalam tuple">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-02/src/main.rs:here}}
```

</Listing>

Mencoba mengompilasi kode ini menghasilkan error tipe berikut:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-02/output.txt}}
```

Untuk memperbaiki error ini, kita bisa mengabaikan satu atau lebih nilai dalam tuple memakai `_` atau `..`, seperti yang akan kamu lihat di bagian ["Mengabaikan Nilai dalam Pattern"][ignoring-values-in-a-pattern]. Jika masalahnya adalah terlalu banyak variabel dalam pattern, solusinya adalah menyamakan tipenya dengan menghapus variabel sampai jumlah variabel sama dengan jumlah elemen dalam tuple.

### Ekspresi `if let` Bersyarat

Di Bab 6, kita membahas cara memakai ekspresi `if let` terutama sebagai cara lebih singkat untuk menulis `match` yang hanya mencocokkan satu kasus. Secara opsional, `if let` bisa disertai `else` yang berisi kode untuk dijalankan jika *pattern* pada `if let` tidak cocok.

Listing 19-3 menunjukkan bahwa kita juga bisa mencampur ekspresi `if let`, `else if`, dan `else if let`. Dengan begitu, kita punya lebih banyak keluwesan dibanding ekspresi `match`, yang hanya bisa menyatakan satu nilai untuk dibandingkan dengan pattern-pattern tersebut. Selain itu, Rust tidak mensyaratkan agar kondisi dalam rangkaian cabang `if let`, `else if`, dan `else if let` saling berkaitan.

Kode di Listing 19-3 menentukan warna latar belakangmu berdasarkan serangkaian pemeriksaan terhadap beberapa kondisi. Untuk contoh ini, kita membuat variabel dengan nilai yang ditulis langsung di kode, padahal dalam program nyata nilainya bisa berasal dari input pengguna.

<Listing number="19-3" file-name="src/main.rs" caption="Mencampur `if let`, `else if`, `else if let`, dan `else`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-03/src/main.rs}}
```

</Listing>

Jika pengguna menentukan warna favorit, warna itulah yang dipakai sebagai latar. Jika tidak ada warna favorit yang ditentukan dan hari ini Selasa, warna latarnya hijau. Jika tidak, ketika pengguna memberikan usia sebagai string dan kita berhasil menguraikannya menjadi angka, warnanya ungu atau oranye, tergantung nilai angkanya. Jika tidak ada kondisi yang terpenuhi, warna latarnya biru.

Struktur bersyarat ini memungkinkan kita menangani kebutuhan yang kompleks. Dengan nilai yang ditulis langsung di kode seperti di sini, contoh ini akan mencetak `Using purple as the background color`.

Kamu bisa melihat bahwa `if let` juga bisa memperkenalkan variabel baru yang menutupi (shadow) variabel yang sudah ada, sama seperti yang bisa dilakukan cabang `match`: baris `if let Ok(age) = age` memperkenalkan variabel `age` baru yang berisi nilai di dalam variant `Ok`, sehingga menutupi variabel `age` yang lama. Ini berarti kita perlu menaruh kondisi `if age > 30` di dalam blok itu: kita tidak bisa menggabungkan kedua kondisi tersebut menjadi `if let Ok(age) = age && age > 30`. Variabel `age` baru yang ingin kita bandingkan dengan 30 belum berlaku sampai scope baru dimulai dengan kurung kurawal.

Kelemahan memakai ekspresi `if let` adalah compiler tidak memeriksa apakah semua kasus tercakup (exhaustiveness), sedangkan pada ekspresi `match` compiler melakukannya. Jika kita menghilangkan blok `else` terakhir dan dengan demikian ada kasus yang tidak tertangani, compiler tidak akan memberi tahu kita tentang kemungkinan bug logika tersebut.

### Loop `while let` Bersyarat

Serupa dalam pembentukannya dengan `if let`, loop bersyarat `while let` memungkinkan loop `while` berjalan selama sebuah *pattern* terus cocok. Di Listing 19-4, kita menunjukkan loop `while let` yang menunggu pesan yang dikirim antar-thread, tetapi kali ini memeriksa `Result`, bukan `Option`.

<Listing number="19-4" caption="Memakai loop `while let` untuk mencetak nilai selama `rx.recv()` mengembalikan `Ok`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-04/src/main.rs:here}}
```

</Listing>

Contoh ini mencetak `1`, `2`, lalu `3`. Metode `recv` mengambil pesan pertama dari sisi penerima channel dan mengembalikan `Ok(value)`. Saat pertama kali kita melihat `recv` di Bab 16, kita membuka error-nya secara langsung, atau berinteraksi dengannya sebagai iterator memakai loop `for`. Namun, seperti yang ditunjukkan Listing 19-4, kita juga bisa memakai `while let`, karena metode `recv` mengembalikan `Ok` setiap kali ada pesan yang tiba, selama pengirim masih ada, lalu menghasilkan `Err` setelah sisi pengirim terputus.

### Loop `for`

Dalam loop `for`, nilai yang langsung mengikuti keyword `for` adalah sebuah *pattern*. Misalnya, pada `for x in y`, `x`-lah pattern-nya. Listing 19-5 menunjukkan cara memakai pattern dalam loop `for` untuk mendestrukturisasi, atau memecah, tuple sebagai bagian dari loop `for`.


<Listing number="19-5" caption="Memakai pattern dalam loop `for` untuk mendestrukturisasi tuple">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-05/src/main.rs:here}}
```

</Listing>

Kode di Listing 19-5 akan mencetak hal berikut:


```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-05/output.txt}}
```

Kita menyesuaikan sebuah iterator dengan metode `enumerate` agar menghasilkan nilai dan indeksnya, yang ditempatkan dalam sebuah tuple. Nilai pertama yang dihasilkan adalah tuple `(0, 'a')`. Saat nilai ini dicocokkan dengan pattern `(index, value)`, `index` akan bernilai `0` dan `value` akan bernilai `'a'`, sehingga mencetak baris pertama dari keluaran.


### Parameter Fungsi

Parameter fungsi juga bisa berupa *pattern*. Kode di Listing 19-6, yang mendeklarasikan fungsi bernama `foo` dengan satu parameter bernama `x` bertipe `i32`, pasti sudah terasa akrab bagimu sekarang.

<Listing number="19-6" caption="Tanda tangan fungsi yang memakai pattern pada parameternya">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-06/src/main.rs:here}}
```

</Listing>

Bagian `x` itu adalah sebuah pattern! Sama seperti yang kita lakukan dengan `let`, kita bisa mencocokkan tuple pada argumen fungsi dengan sebuah pattern. Listing 19-7 memecah nilai-nilai dalam tuple saat kita meneruskannya ke sebuah fungsi.

<Listing number="19-7" file-name="src/main.rs" caption="Fungsi dengan parameter yang mendestrukturisasi tuple">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-07/src/main.rs}}
```

</Listing>

Kode ini mencetak `Current location: (3, 5)`. Nilai `&(3, 5)` cocok dengan pattern `&(x, y)`, sehingga `x` bernilai `3` dan `y` bernilai `5`.

Kita juga bisa memakai pattern dalam daftar parameter closure dengan cara yang sama seperti pada daftar parameter fungsi, karena closure mirip dengan fungsi, seperti yang kita bahas di Bab 13.

Pada titik ini, kamu sudah melihat beberapa cara memakai pattern, tetapi pattern tidak bekerja dengan cara yang sama di semua tempat. Di beberapa tempat, pattern harus bersifat irrefutable (tidak bisa gagal); dalam situasi lain, pattern boleh bersifat refutable (bisa gagal). Kita akan membahas kedua konsep ini selanjutnya.

[ignoring-values-in-a-pattern]: ch19-03-pattern-syntax.html#ignoring-values-in-a-pattern
