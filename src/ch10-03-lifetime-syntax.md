<a id="validating-references-with-lifetimes"></a>
## Memvalidasi Reference dengan Lifetime

*Lifetime* adalah jenis generic lain yang sudah kita pakai. Alih-alih memastikan bahwa sebuah tipe punya perilaku yang kita inginkan, lifetime memastikan reference tetap valid selama kita membutuhkannya.

Satu detail yang tidak kita bahas di bagian ["References and Borrowing"][references-and-borrowing]<!-- ignore --> Bab 4 adalah bahwa setiap reference di Rust punya lifetime, yaitu scope di mana reference tersebut valid. Pada umumnya, lifetime bersifat implisit dan disimpulkan, sama seperti tipe yang juga kebanyakan disimpulkan. Kita hanya perlu menganotasi tipe ketika ada beberapa tipe yang memungkinkan. Dengan cara yang serupa, kita harus menganotasi lifetime ketika lifetime dari beberapa reference bisa saling berhubungan dalam beberapa cara yang berbeda. Rust meminta kita menganotasi hubungan tersebut menggunakan generic lifetime parameter untuk memastikan bahwa reference yang benar-benar dipakai saat runtime pasti valid.

Menganotasi lifetime bahkan bukan konsep yang dimiliki kebanyakan bahasa pemrograman lain, jadi ini akan terasa asing. Meski kita tidak akan membahas lifetime secara menyeluruh di bab ini, kita akan membahas cara-cara umum kamu akan menemui sintaks lifetime supaya kamu bisa nyaman dengan konsep ini.

<!-- Old headings. Do not remove or links may break. -->

<a id="preventing-dangling-references-with-lifetimes"></a>

### Dangling References

Tujuan utama *lifetime* adalah mencegah dangling reference, yaitu reference yang, jika boleh ada, akan membuat program merujuk ke data selain data yang seharusnya dirujuk. Perhatikan program di Listing 10-16, yang punya outer scope dan inner scope.

<Listing number="10-16" caption="Upaya memakai reference yang nilainya sudah keluar dari scope">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-16/src/main.rs}}
```

</Listing>

> Catatan: Contoh di Listing 10-16, 10-17, dan 10-23 mendeklarasikan variabel tanpa memberi nilai awal, sehingga nama variabel tersebut ada di outer scope. Sekilas, ini mungkin tampak bertentangan dengan Rust yang tidak punya nilai null. Namun, jika kita mencoba memakai variabel sebelum memberinya nilai, kita akan mendapat error saat kompilasi, yang menunjukkan bahwa Rust memang tidak mengizinkan nilai null.

Outer scope mendeklarasikan variabel bernama `r` tanpa nilai awal, dan inner scope mendeklarasikan variabel bernama `x` dengan nilai awal `5`. Di dalam inner scope, kita mencoba mengisi `r` dengan reference ke `x`. Lalu inner scope berakhir, dan kita mencoba mencetak nilai di `r`. Kode ini tidak akan dikompilasi, karena nilai yang dirujuk `r` sudah keluar dari scope sebelum kita memakainya. Berikut pesan error-nya:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-16/output.txt}}
```

Pesan error mengatakan bahwa variabel `x` "tidak hidup cukup lama." Alasannya, `x` akan keluar dari scope ketika inner scope berakhir di baris 7. Tapi `r` masih valid di outer scope; karena scope-nya lebih besar, kita bilang `r` "hidup lebih lama." Jika Rust mengizinkan kode ini berjalan, `r` akan merujuk ke memori yang sudah dibebaskan ketika `x` keluar dari scope, dan apa pun yang kita coba lakukan dengan `r` tidak akan bekerja dengan benar. Jadi, bagaimana Rust menentukan bahwa kode ini tidak valid? Ia memakai borrow checker.

### The Borrow Checker

Compiler Rust punya _borrow checker_ yang membandingkan scope untuk menentukan apakah semua borrowing valid. Listing 10-17 menunjukkan kode yang sama dengan Listing 10-16, tetapi dengan anotasi yang menampilkan *lifetime* dari variabel-variabel tersebut.

<Listing number="10-17" caption="Anotasi lifetime dari `r` dan `x`, masing-masing bernama `'a` dan `'b`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-17/src/main.rs}}
```

</Listing>

Di sini, kita menganotasi lifetime `r` dengan `'a` dan lifetime `x` dengan `'b`. Seperti yang kamu lihat, blok `'b` di dalam jauh lebih kecil daripada blok lifetime `'a` di luar. Saat kompilasi, Rust membandingkan ukuran kedua lifetime dan melihat bahwa `r` punya lifetime `'a`, tetapi merujuk ke memori dengan lifetime `'b`. Program ditolak karena `'b` lebih pendek daripada `'a`: objek yang dirujuk tidak hidup selama reference-nya.

Listing 10-18 memperbaiki kode sehingga tidak punya dangling reference dan dapat dikompilasi tanpa error.

<Listing number="10-18" caption="Reference yang valid karena data punya lifetime lebih panjang daripada reference-nya">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-18/src/main.rs}}
```

</Listing>

Di sini, `x` punya lifetime `'b`, yang dalam kasus ini lebih besar daripada `'a`. Ini berarti `r` boleh merujuk `x` karena Rust tahu bahwa reference di `r` akan selalu valid selama `x` valid.

Sekarang kamu tahu di mana *lifetime* dari reference itu berada dan bagaimana Rust menganalisisnya untuk memastikan reference selalu valid, mari kita jelajahi generic lifetime pada parameter dan nilai kembalian fungsi.

### Generic Lifetime pada Fungsi

Kita akan menulis fungsi yang mengembalikan string slice yang lebih panjang dari dua string slice. Fungsi ini menerima dua string slice dan mengembalikan satu string slice. Setelah kita mengimplementasikan fungsi `longest`, kode di Listing 10-19 seharusnya mencetak `The longest string is abcd`.

<Listing number="10-19" file-name="src/main.rs" caption="Fungsi `main` yang memanggil fungsi `longest` untuk mencari string slice yang lebih panjang dari dua string slice">

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-19/src/main.rs}}
```

</Listing>

Perhatikan bahwa kita ingin fungsi menerima string slice, yang merupakan reference, bukan string, karena kita tidak ingin fungsi `longest` mengambil ownership atas parameternya. Lihat ["String Slices as Parameters"][string-slices-as-parameters]<!-- ignore --> di Bab 4 untuk pembahasan lebih lanjut mengapa parameter yang kita pakai di Listing 10-19 adalah parameter yang kita inginkan.

Jika kita coba mengimplementasikan fungsi `longest` seperti di Listing 10-20, kode itu tidak akan dikompilasi.

<Listing number="10-20" file-name="src/main.rs" caption="Implementasi fungsi `longest` yang mengembalikan string slice lebih panjang dari dua string slice, tetapi belum bisa dikompilasi">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/src/main.rs:here}}
```

</Listing>

Sebaliknya, kita mendapat error berikut yang membahas lifetime:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/output.txt}}
```

Teks bantuan menunjukkan bahwa tipe kembalian perlu generic lifetime parameter, karena Rust tidak bisa tahu apakah reference yang dikembalikan merujuk ke `x` atau `y`. Sebenarnya, kita juga tidak tahu, karena blok `if` di badan fungsi ini mengembalikan reference ke `x` dan blok `else` mengembalikan reference ke `y`!

Saat mendefinisikan fungsi ini, kita tidak tahu nilai konkret yang akan diberikan, sehingga kita tidak tahu apakah kasus `if` atau `else` yang akan dijalankan. Kita juga tidak tahu lifetime konkret dari reference yang akan diberikan, jadi kita tidak bisa melihat scope seperti yang kita lakukan di Listing 10-17 dan 10-18 untuk menentukan apakah reference yang kita kembalikan akan selalu valid. Borrow checker juga tidak bisa menentukannya, karena ia tidak tahu bagaimana lifetime `x` dan `y` berhubungan dengan lifetime nilai kembalian. Untuk memperbaiki error ini, kita akan menambahkan generic lifetime parameter yang mendefinisikan hubungan antar reference sehingga borrow checker bisa melakukan analisisnya.

### Sintaks Anotasi Lifetime

Anotasi lifetime tidak mengubah berapa lama reference mana pun hidup. Sebaliknya, anotasi itu menggambarkan hubungan antar lifetime dari beberapa reference tanpa memengaruhi lifetime-nya sendiri. Sama seperti fungsi bisa menerima tipe apa pun ketika signature menentukan generic type parameter, fungsi bisa menerima reference dengan lifetime apa pun dengan menentukan generic lifetime parameter.

Anotasi lifetime punya sintaks yang agak tidak biasa: nama lifetime parameter harus diawali apostrof (`'`) dan biasanya semuanya huruf kecil serta sangat pendek, seperti generic type. Kebanyakan orang memakai nama `'a` untuk anotasi lifetime pertama. Kita menaruh anotasi lifetime parameter setelah `&` dari sebuah reference, dengan spasi untuk memisahkan anotasi dari tipe reference tersebut.

Berikut beberapa contoh—sebuah reference ke `i32` tanpa lifetime parameter, sebuah reference ke `i32` yang punya lifetime parameter bernama `'a`, dan sebuah mutable reference ke `i32` yang juga punya lifetime `'a`:

```rust,ignore
&i32        // a reference
&'a i32     // a reference with an explicit lifetime
&'a mut i32 // a mutable reference with an explicit lifetime
```

Satu anotasi lifetime saja tidak punya banyak makna, karena anotasi bertujuan memberi tahu Rust bagaimana generic lifetime parameter dari beberapa reference saling berhubungan. Mari kita lihat bagaimana anotasi lifetime saling berhubungan dalam konteks fungsi `longest`.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-function-signatures"></a>

### Pada Signature Fungsi

Untuk memakai anotasi lifetime di signature fungsi, kita perlu mendeklarasikan generic lifetime parameter di dalam tanda kurung sudut antara nama fungsi dan daftar parameter, sama seperti yang kita lakukan dengan generic type parameter.

Kita ingin signature menyampaikan batasan berikut: reference yang dikembalikan akan valid selama kedua parameter valid. Inilah hubungan antara lifetime parameter dan nilai kembalian. Kita akan menamai lifetime itu `'a`, lalu menambahkannya ke setiap reference, seperti ditunjukkan di Listing 10-21.

<Listing number="10-21" file-name="src/main.rs" caption="Definisi fungsi `longest` yang menentukan bahwa semua reference di signature harus punya lifetime `'a` yang sama">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-21/src/main.rs:here}}
```

</Listing>

Kode ini seharusnya dikompilasi dan menghasilkan hasil yang kita inginkan saat dipakai dengan fungsi `main` di Listing 10-19.

Signature fungsi sekarang memberi tahu Rust bahwa untuk suatu lifetime `'a`, fungsi menerima dua parameter, keduanya string slice yang hidup setidaknya selama lifetime `'a`. Signature fungsi juga memberi tahu Rust bahwa string slice yang dikembalikan fungsi akan hidup setidaknya selama lifetime `'a`. Praktiknya, ini berarti lifetime dari reference yang dikembalikan fungsi `longest` sama dengan lifetime yang lebih kecil dari nilai-nilai yang dirujuk oleh argumen fungsi. Hubungan-hubungan inilah yang ingin kita pakai Rust saat menganalisis kode ini.

Ingat, ketika kita menentukan lifetime parameter di signature fungsi ini, kita tidak mengubah lifetime nilai apa pun yang diberikan maupun dikembalikan. Sebaliknya, kita menentukan bahwa borrow checker harus menolak nilai apa pun yang tidak mematuhi batasan ini. Perhatikan bahwa fungsi `longest` tidak perlu tahu persis berapa lama `x` dan `y` akan hidup, cukup bahwa ada suatu scope yang bisa menggantikan `'a` dan memenuhi signature ini.

Saat menganotasi lifetime di fungsi, anotasi ditaruh di signature fungsi, bukan di badan fungsi. Anotasi lifetime menjadi bagian dari kontrak fungsi, mirip seperti tipe di dalam signature. Dengan signature fungsi yang memuat kontrak lifetime, analisis yang dilakukan compiler Rust jadi lebih sederhana. Jika ada masalah pada cara fungsi dianotasi atau cara fungsi dipanggil, error compiler bisa menunjuk ke bagian kode dan batasan yang bersangkutan dengan lebih tepat. Seandainya compiler Rust justru melakukan lebih banyak penyimpulan tentang hubungan lifetime yang kita maksud, compiler mungkin hanya bisa menunjuk ke pemakaian kode kita yang jauh dari penyebab masalahnya.

Saat kita memberikan reference konkret ke `longest`, lifetime konkret yang menggantikan `'a` adalah bagian dari scope `x` yang tumpang tindih dengan scope `y`. Dengan kata lain, generic lifetime `'a` akan mendapat lifetime konkret yang sama dengan lifetime `x` dan `y` yang lebih kecil. Karena kita menganotasi reference yang dikembalikan dengan lifetime parameter `'a` yang sama, reference yang dikembalikan juga akan valid selama lifetime `x` dan `y` yang lebih kecil.

Mari kita lihat bagaimana anotasi lifetime membatasi fungsi `longest` dengan memberikan reference yang punya lifetime konkret berbeda. Listing 10-22 adalah contoh yang sederhana.

<Listing number="10-22" file-name="src/main.rs" caption="Memakai fungsi `longest` dengan reference ke nilai `String` yang punya lifetime konkret berbeda">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-22/src/main.rs:here}}
```

</Listing>

Pada contoh ini, `string1` valid sampai akhir outer scope, `string2` valid sampai akhir inner scope, dan `result` merujuk ke sesuatu yang valid sampai akhir inner scope. Jalankan kode ini dan kamu akan melihat bahwa borrow checker menyetujuinya; kode akan dikompilasi dan mencetak `The longest string is long string is long`.

Berikutnya, mari kita coba contoh yang menunjukkan bahwa lifetime reference di `result` haruslah lifetime yang lebih kecil dari kedua argumen. Kita akan memindahkan deklarasi variabel `result` ke luar inner scope, tetapi tetap membiarkan pengisian nilainya di dalam scope bersama `string2`. Lalu, kita memindahkan `println!` yang memakai `result` ke luar inner scope, setelah inner scope berakhir. Kode di Listing 10-23 tidak akan dikompilasi.

<Listing number="10-23" file-name="src/main.rs" caption="Upaya memakai `result` setelah `string2` keluar dari scope">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/src/main.rs:here}}
```

</Listing>

Saat kita mencoba mengompilasi kode ini, kita mendapat error ini:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/output.txt}}
```

Error menunjukkan bahwa agar `result` valid untuk statement `println!`, `string2` perlu valid sampai akhir outer scope. Rust tahu hal ini karena kita menganotasi lifetime parameter fungsi dan nilai kembalian memakai lifetime parameter `'a` yang sama.

Sebagai manusia, kita bisa melihat kode ini dan tahu bahwa `string1` lebih panjang daripada `string2`, sehingga `result` akan berisi reference ke `string1`. Karena `string1` belum keluar dari scope, reference ke `string1` akan tetap valid untuk statement `println!`. Namun, compiler tidak bisa melihat bahwa reference itu valid dalam kasus ini. Kita sudah memberi tahu Rust bahwa lifetime reference yang dikembalikan fungsi `longest` sama dengan lifetime yang lebih kecil dari reference yang diberikan. Karena itu, borrow checker melarang kode di Listing 10-23 karena kemungkinan punya reference yang tidak valid.

Coba rancang lebih banyak percobaan yang memvariasikan nilai dan lifetime reference yang diberikan ke fungsi `longest`, serta cara reference yang dikembalikan dipakai. Buatlah dugaan apakah percobaanmu akan lolos borrow checker sebelum kamu mengompilasi; lalu, cek apakah dugaanmu benar!

<!-- Old headings. Do not remove or links may break. -->

<a id="thinking-in-terms-of-lifetimes"></a>

### Hubungan

Cara kamu menentukan lifetime parameter bergantung pada apa yang dilakukan fungsimu. Misalnya, jika kita mengubah implementasi fungsi `longest` untuk selalu mengembalikan parameter pertama, bukan string slice terpanjang, kita tidak perlu menentukan lifetime pada parameter `y`. Kode berikut akan dikompilasi:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-08-only-one-reference-with-lifetime/src/main.rs:here}}
```

</Listing>

Kita sudah menentukan lifetime parameter `'a` untuk parameter `x` dan tipe kembalian, tetapi bukan untuk parameter `y`, karena lifetime `y` tidak punya hubungan apa pun dengan lifetime `x` maupun nilai kembalian.

Saat mengembalikan reference dari fungsi, lifetime parameter untuk tipe kembalian perlu cocok dengan lifetime parameter salah satu parameter. Jika reference yang dikembalikan _tidak_ merujuk ke salah satu parameter, reference itu harus merujuk ke nilai yang dibuat di dalam fungsi ini. Namun, itu akan menjadi dangling reference karena nilainya akan keluar dari scope di akhir fungsi. Perhatikan upaya implementasi fungsi `longest` ini yang tidak akan dikompilasi:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/src/main.rs:here}}
```

</Listing>

Di sini, meski kita sudah menentukan lifetime parameter `'a` untuk tipe kembalian, implementasi ini tetap gagal dikompilasi karena lifetime nilai kembalian sama sekali tidak berhubungan dengan lifetime parameter. Berikut pesan error yang kita dapatkan:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/output.txt}}
```

Masalahnya, `result` keluar dari scope dan dibersihkan di akhir fungsi `longest`. Kita juga mencoba mengembalikan reference ke `result` dari fungsi tersebut. Tidak ada cara kita menentukan lifetime parameter yang bisa mengubah dangling reference itu, dan Rust tidak akan membiarkan kita membuat dangling reference. Dalam kasus ini, perbaikan terbaik adalah mengembalikan tipe data yang dimiliki (owned), bukan reference, sehingga fungsi yang memanggilnya yang bertanggung jawab membersihkan nilainya.

Pada akhirnya, sintaks lifetime adalah soal menghubungkan lifetime dari berbagai parameter dan nilai kembalian fungsi. Setelah terhubung, Rust punya cukup informasi untuk mengizinkan operasi yang aman bagi memori dan melarang operasi yang akan membuat dangling pointer atau melanggar keamanan memori.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-struct-definitions"></a>

### Pada Definisi Struct

Sejauh ini, semua struct yang kita definisikan menyimpan tipe yang dimiliki (owned). Kita bisa mendefinisikan struct untuk menyimpan reference, tetapi dalam hal itu kita perlu menambahkan anotasi lifetime pada setiap reference di definisi struct tersebut. Listing 10-24 punya struct bernama `ImportantExcerpt` yang menyimpan sebuah string slice.

<Listing number="10-24" file-name="src/main.rs" caption="Struct yang menyimpan reference dan membutuhkan anotasi lifetime">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-24/src/main.rs}}
```

</Listing>

Struct ini punya satu field, `part`, yang menyimpan string slice, yaitu sebuah reference. Sama seperti generic data type, kita mendeklarasikan nama generic lifetime parameter di dalam tanda kurung sudut setelah nama struct supaya bisa memakai lifetime parameter itu di badan definisi struct. Anotasi ini berarti instance `ImportantExcerpt` tidak bisa hidup lebih lama daripada reference yang disimpannya di field `part`.

Fungsi `main` di sini membuat instance struct `ImportantExcerpt` yang menyimpan reference ke kalimat pertama dari `String` yang dimiliki variabel `novel`. Data di `novel` sudah ada sebelum instance `ImportantExcerpt` dibuat. Selain itu, `novel` tidak keluar dari scope sampai setelah `ImportantExcerpt` keluar dari scope, sehingga reference di instance `ImportantExcerpt` itu valid.

### Elisi Lifetime

Kamu sudah belajar bahwa setiap reference punya lifetime dan bahwa kamu perlu menentukan lifetime parameter untuk fungsi atau struct yang memakai reference. Namun, kita punya fungsi di Listing 4-9, ditampilkan lagi di Listing 10-25, yang bisa dikompilasi tanpa anotasi lifetime.

<Listing number="10-25" file-name="src/lib.rs" caption="Fungsi yang kita definisikan di Listing 4-9 yang bisa dikompilasi tanpa anotasi lifetime, meski parameter dan tipe kembaliannya adalah reference">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-25/src/main.rs:here}}
```

</Listing>

Alasan fungsi ini bisa dikompilasi tanpa anotasi lifetime bersifat historis: Pada versi awal Rust (sebelum 1.0), kode ini tidak akan dikompilasi, karena setiap reference membutuhkan lifetime eksplisit. Pada saat itu, signature fungsinya akan ditulis begini:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

Setelah menulis banyak kode Rust, tim Rust mendapati bahwa programmer Rust mengetik anotasi lifetime yang sama berulang kali dalam situasi tertentu. Situasi-situasi itu bisa diprediksi dan mengikuti beberapa pola yang pasti. Para pengembang memasukkan pola-pola ini ke dalam kode compiler sehingga borrow checker bisa menyimpulkan lifetime dalam situasi tersebut tanpa membutuhkan anotasi eksplisit.

Sejarah Rust ini relevan karena mungkin saja lebih banyak pola pasti akan muncul dan ditambahkan ke compiler. Di masa depan, mungkin anotasi lifetime yang dibutuhkan akan lebih sedikit lagi.

Pola-pola yang diprogramkan ke dalam analisis reference Rust disebut _aturan elisi lifetime_. Ini bukan aturan yang harus diikuti programmer; ini sekumpulan kasus tertentu yang akan dipertimbangkan compiler, dan jika kodemu cocok dengan kasus-kasus itu, kamu tidak perlu menulis lifetime secara eksplisit.

Aturan elisi tidak memberikan penyimpulan penuh. Jika masih ada ambiguitas tentang lifetime reference setelah Rust menerapkan aturan-aturan itu, compiler tidak akan menebak seperti apa lifetime reference yang tersisa. Alih-alih menebak, compiler akan memberi kamu error yang bisa kamu atasi dengan menambahkan anotasi lifetime.

Lifetime pada parameter fungsi atau method disebut _input lifetimes_, dan lifetime pada nilai kembalian disebut _output lifetimes_.

Compiler memakai tiga aturan untuk menentukan lifetime reference ketika tidak ada anotasi eksplisit. Aturan pertama berlaku untuk input lifetime, dan aturan kedua serta ketiga berlaku untuk output lifetime. Jika compiler sudah melewati ketiga aturan hingga akhir dan masih ada reference yang tidak bisa ditentukan lifetime-nya, compiler akan berhenti dengan error. Aturan-aturan ini berlaku untuk definisi `fn` maupun blok `impl`.

Aturan pertama adalah compiler menetapkan sebuah lifetime parameter untuk setiap parameter yang berupa reference. Dengan kata lain, fungsi dengan satu parameter mendapat satu lifetime parameter: `fn foo<'a>(x: &'a i32)`; fungsi dengan dua parameter mendapat dua lifetime parameter terpisah: `fn foo<'a, 'b>(x: &'a i32, y: &'b i32)`; dan seterusnya.

Aturan kedua adalah, jika hanya ada tepat satu input lifetime parameter, lifetime itu ditetapkan ke semua output lifetime parameter: `fn foo<'a>(x: &'a i32) -> &'a i32`.

Aturan ketiga adalah, jika ada beberapa input lifetime parameter, tetapi salah satunya adalah `&self` atau `&mut self` karena ini sebuah method, maka lifetime `self` ditetapkan ke semua output lifetime parameter. Aturan ketiga ini membuat method jauh lebih enak dibaca dan ditulis karena lebih sedikit simbol yang diperlukan.

Mari kita berpura-pura menjadi compiler. Kita akan menerapkan aturan-aturan ini untuk menentukan lifetime reference di signature fungsi `first_word` di Listing 10-25. Signature awalnya tanpa lifetime yang terkait dengan reference mana pun:

```rust,ignore
fn first_word(s: &str) -> &str {
```

Lalu, compiler menerapkan aturan pertama, yang menentukan bahwa setiap parameter mendapat lifetime sendiri. Kita menamainya `'a` seperti biasa, sehingga sekarang signature-nya begini:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &str {
```

Aturan kedua berlaku karena hanya ada tepat satu input lifetime. Aturan kedua menentukan bahwa lifetime dari satu parameter input itu ditetapkan ke output lifetime, sehingga signature sekarang begini:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

Sekarang semua reference di signature fungsi ini punya lifetime, dan compiler bisa melanjutkan analisisnya tanpa perlu programmer menganotasi lifetime di signature fungsi ini.

Mari kita lihat contoh lain, kali ini memakai fungsi `longest` yang belum punya lifetime parameter ketika kita mulai mengerjakannya di Listing 10-20:

```rust,ignore
fn longest(x: &str, y: &str) -> &str {
```

Mari terapkan aturan pertama: Setiap parameter mendapat lifetime sendiri. Kali ini kita punya dua parameter, bukan satu, jadi kita punya dua lifetime:

```rust,ignore
fn longest<'a, 'b>(x: &'a str, y: &'b str) -> &str {
```

Kamu bisa melihat bahwa aturan kedua tidak berlaku, karena ada lebih dari satu input lifetime. Aturan ketiga juga tidak berlaku, karena `longest` adalah fungsi, bukan method, jadi tidak ada parameter yang berupa `self`. Setelah melewati ketiga aturan, kita masih belum bisa menentukan seperti apa lifetime tipe kembalian itu. Inilah alasan kita mendapat error saat mencoba mengompilasi kode di Listing 10-20: compiler sudah melewati aturan elisi lifetime, tetapi tetap belum bisa menentukan semua lifetime reference di signature.

Karena aturan ketiga hanya benar-benar berlaku di signature method, berikutnya kita akan melihat lifetime dalam konteks itu untuk memahami mengapa aturan ketiga membuat kita jarang perlu menganotasi lifetime di signature method.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-method-definitions"></a>

### Pada Definisi Method

Saat kita mengimplementasikan method pada struct yang punya lifetime, kita memakai sintaks yang sama seperti generic type parameter, seperti ditunjukkan di Listing 10-11. Di mana kita mendeklarasikan dan memakai lifetime parameter bergantung pada apakah lifetime itu terkait dengan field struct ataupun parameter dan nilai kembalian method.

Nama lifetime untuk field struct selalu perlu dideklarasikan setelah kata kunci `impl`, lalu dipakai setelah nama struct, karena lifetime itu adalah bagian dari tipe struct.

Di signature method di dalam blok `impl`, reference mungkin terikat pada lifetime reference di field struct, atau bisa juga independen. Selain itu, aturan elisi lifetime sering kali membuat anotasi lifetime tidak diperlukan di signature method. Mari kita lihat beberapa contoh memakai struct bernama `ImportantExcerpt` yang kita definisikan di Listing 10-24.

Pertama, kita akan memakai method bernama `level` yang hanya punya satu parameter berupa reference ke `self` dan nilai kembalian berupa `i32`, yang bukan reference ke apa pun:

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:1st}}
```

Deklarasi lifetime parameter setelah `impl` dan pemakaiannya setelah nama tipe memang wajib, tetapi berkat aturan elisi pertama, kita tidak perlu menganotasi lifetime reference ke `self`.

Berikut contoh di mana aturan elisi lifetime ketiga berlaku:

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:3rd}}
```

Ada dua input lifetime, sehingga Rust menerapkan aturan elisi lifetime pertama dan memberi `&self` serta `announcement` masing-masing lifetime sendiri. Lalu, karena salah satu parameter adalah `&self`, tipe kembalian mendapat lifetime `&self`, dan semua lifetime sudah terpenuhi.

### Lifetime Statis

Satu lifetime khusus yang perlu kita bahas adalah `'static`, yang menandakan bahwa reference yang bersangkutan _bisa_ hidup selama program berjalan. Semua string literal punya lifetime `'static`, yang bisa kita anotasi seperti ini:

```rust
let s: &'static str = "I have a static lifetime.";
```

Teks string ini disimpan langsung di biner program, yang selalu tersedia. Karena itu, lifetime semua string literal adalah `'static`.

Kamu mungkin melihat saran di pesan error untuk memakai lifetime `'static`. Namun, sebelum menentukan `'static` sebagai lifetime sebuah reference, pikirkan apakah reference yang kamu punya benar-benar hidup selama program kamu berjalan, dan apakah kamu memang menginginkannya. Pada umumnya, pesan error yang menyarankan lifetime `'static` muncul karena upaya membuat dangling reference atau ketidaksesuaian lifetime yang tersedia. Dalam kasus seperti itu, solusinya adalah memperbaiki masalah tersebut, bukan menentukan lifetime `'static`.

<!-- Old headings. Do not remove or links may break. -->

<a id="generic-type-parameters-trait-bounds-and-lifetimes-together"></a>

## Generic Type Parameter, Trait Bound, dan Lifetime

Mari kita lihat sekilas sintaks menentukan generic type parameter, trait bound, dan lifetime semuanya dalam satu fungsi!

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-11-generics-traits-and-lifetimes/src/main.rs:here}}
```

Ini adalah fungsi `longest` dari Listing 10-21 yang mengembalikan string slice yang lebih panjang dari dua string slice. Tetapi sekarang fungsi itu punya parameter tambahan bernama `ann` bertipe generic `T`, yang bisa diisi oleh tipe apa pun yang mengimplementasikan trait `Display` seperti yang ditentukan klausa `where`. Parameter tambahan ini akan dicetak memakai `{}`, itulah sebabnya trait bound `Display` diperlukan. Karena lifetime adalah salah satu jenis generic, deklarasi lifetime parameter `'a` dan generic type parameter `T` ditaruh dalam daftar yang sama di dalam tanda kurung sudut setelah nama fungsi.

## Ringkasan

Kita sudah membahas banyak hal di bab ini! Sekarang kamu sudah tahu tentang generic type parameter, trait dan trait bound, serta generic lifetime parameter, kamu siap menulis kode tanpa pengulangan yang bekerja dalam banyak situasi berbeda. Generic type parameter memungkinkan kamu menerapkan kode ke tipe yang berbeda. Trait dan trait bound memastikan bahwa meski tipenya generic, tipe itu akan punya perilaku yang dibutuhkan kode. Kamu sudah belajar memakai anotasi lifetime untuk memastikan kode yang fleksibel ini tidak punya dangling reference. Dan semua analisis ini terjadi saat kompilasi, sehingga tidak memengaruhi performa runtime!

Percaya atau tidak, masih banyak lagi yang bisa dipelajari tentang topik yang kita bahas di bab ini: Bab 18 membahas trait object, cara lain memakai trait. Ada juga skenario yang lebih kompleks yang melibatkan anotasi lifetime, yang hanya akan kamu butuhkan dalam kasus yang sangat lanjutan; untuk itu, sebaiknya kamu membaca [Rust Reference][reference]. Tapi berikutnya, kamu akan belajar cara menulis test di Rust supaya bisa memastikan kodemu bekerja sebagaimana mestinya.

[references-and-borrowing]: ch04-02-references-and-borrowing.html#references-and-borrowing
[string-slices-as-parameters]: ch04-03-slices.html#string-slices-as-parameters
[reference]: ../reference/trait-bounds.html
