<a id="advanced-traits"></a>
## Trait Lanjutan

Kita pertama kali membahas trait di bagian [“Mendefinisikan Perilaku Bersama dengan Trait”][traits]<!-- ignore --> pada Bab 10, tetapi belum membahas detail yang lebih lanjut. Sekarang kamu sudah tahu lebih banyak tentang Rust, kita bisa masuk ke seluk-beluknya.

<!-- Judul lama. Jangan hapus atau tautan bisa rusak. -->

<a id="specifying-placeholder-types-in-trait-definitions-with-associated-types"></a>
<a id="associated-types"></a>

### Mendefinisikan Trait dengan Tipe Asosiasi

_Tipe asosiasi_ menghubungkan placeholder tipe dengan sebuah trait sehingga definisi metode trait bisa memakai placeholder tersebut dalam signature-nya. Implementor trait akan menentukan tipe konkret yang dipakai menggantikan placeholder untuk implementasi tertentu. Dengan begitu, kita bisa mendefinisikan trait yang memakai beberapa tipe tanpa perlu tahu persis tipe apa itu sampai trait diimplementasikan.

Kita sudah menyebut sebagian besar fitur lanjutan di bab ini sebagai hal yang jarang dibutuhkan. Tipe asosiasi ada di tengah-tengah: pemakaiannya lebih jarang daripada fitur yang dijelaskan di bagian lain buku ini, tetapi lebih umum daripada banyak fitur lain yang dibahas di bab ini.

Salah satu contoh trait dengan tipe asosiasi adalah trait `Iterator` yang disediakan pustaka standar. Tipe asosiasinya bernama `Item` dan mewakili tipe nilai yang diiterasi oleh tipe yang mengimplementasikan trait `Iterator`. Definisi trait `Iterator` ditunjukkan pada Listing 20-13.

<Listing number="20-13" caption="Definisi trait `Iterator` yang memiliki tipe asosiasi `Item`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-13/src/lib.rs}}
```

</Listing>

Tipe `Item` adalah placeholder, dan definisi metode `next` menunjukkan bahwa metode itu akan mengembalikan nilai bertipe `Option<Self::Item>`. Implementor trait `Iterator` akan menentukan tipe konkret untuk `Item`, lalu metode `next` akan mengembalikan `Option` yang berisi nilai bertipe konkret tersebut.

Tipe asosiasi mungkin tampak mirip dengan generic, karena generic juga memungkinkan kita mendefinisikan fungsi tanpa menentukan tipe apa yang bisa ditanganinya. Untuk melihat perbedaan kedua konsep ini, kita akan melihat implementasi trait `Iterator` pada tipe bernama `Counter` yang menentukan tipe `Item` sebagai `u32`:

<Listing file-name="src/lib.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-22-iterator-on-counter/src/lib.rs:ch19}}
```

</Listing>

Sintaks ini tampak mirip dengan sintaks generic. Jadi, kenapa tidak mendefinisikan saja trait `Iterator` dengan generic, seperti pada Listing 20-14?

<Listing number="20-14" caption="Definisi hipotetis trait `Iterator` menggunakan generic">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-14/src/lib.rs}}
```

</Listing>

Perbedaannya adalah saat memakai generic, seperti pada Listing 20-14, kita harus menuliskan anotasi tipe di setiap implementasi; karena kita juga bisa mengimplementasikan `Iterator<String> for Counter` atau tipe lain, kita bisa punya beberapa implementasi `Iterator` untuk `Counter`. Dengan kata lain, ketika sebuah trait memiliki parameter generic, trait itu bisa diimplementasikan berkali-kali untuk satu tipe, dengan mengubah tipe konkret parameter generic tersebut setiap kali. Saat memakai metode `next` pada `Counter`, kita harus memberikan anotasi tipe untuk menunjukkan implementasi `Iterator` mana yang ingin kita pakai.

Dengan tipe asosiasi, kita tidak perlu menganotasi tipe, karena kita tidak bisa mengimplementasikan sebuah trait berkali-kali pada satu tipe. Pada Listing 20-13 dengan definisi yang memakai tipe asosiasi, kita bisa memilih tipe `Item` hanya sekali karena hanya boleh ada satu `impl Iterator for Counter`. Kita tidak perlu menyebut bahwa kita menginginkan iterator bernilai `u32` di setiap tempat kita memanggil `next` pada `Counter`.

Tipe asosiasi juga menjadi bagian dari kontrak trait: implementor trait harus menyediakan sebuah tipe untuk menggantikan placeholder tipe asosiasi. Tipe asosiasi biasanya punya nama yang menggambarkan bagaimana tipe itu akan dipakai, dan mendokumentasikannya dalam dokumentasi API adalah kebiasaan yang baik.

<!-- Judul lama. Jangan hapus atau tautan bisa rusak. -->

<a id="default-generic-type-parameters-and-operator-overloading"></a>

### Memakai Parameter Generic Default dan Overloading Operator

Saat memakai parameter tipe generic, kita bisa menentukan tipe konkret default untuk tipe generic tersebut. Ini menghilangkan keharusan bagi implementor trait untuk menyebut tipe konkret jika tipe default sudah cocok. Kamu menentukan tipe default dengan mendeklarasikan tipe generic memakai sintaks `<PlaceholderType=ConcreteType>`.

Contoh bagus dari situasi teknik ini berguna adalah _overloading operator_, di mana kamu menyesuaikan perilaku sebuah operator (seperti `+`) dalam situasi tertentu.

Rust tidak membolehkan kamu membuat operator sendiri atau meng-overload operator sembarangan. Namun, kamu bisa meng-overload operasi dan trait terkait yang tercantum di `std::ops` dengan mengimplementasikan trait yang bersesuaian dengan operator itu. Misalnya, pada Listing 20-15, kita meng-overload operator `+` untuk menjumlahkan dua instance `Point`. Kita melakukan ini dengan mengimplementasikan trait `Add` pada struct `Point`.

<Listing number="20-15" file-name="src/main.rs" caption="Mengimplementasikan trait `Add` untuk meng-overload operator `+` bagi instance `Point`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-15/src/main.rs}}
```

</Listing>

Metode `add` menjumlahkan nilai `x` dari dua instance `Point` dan nilai `y` dari dua instance `Point` untuk membuat `Point` baru. Trait `Add` punya tipe asosiasi bernama `Output` yang menentukan tipe yang dikembalikan dari metode `add`.

Tipe generic default dalam kode ini ada di dalam trait `Add`. Berikut definisinya:

```rust
trait Add<Rhs=Self> {
    type Output;

    fn add(self, rhs: Rhs) -> Self::Output;
}
```

Kode ini seharusnya tampak cukup akrab: sebuah trait dengan satu metode dan satu tipe asosiasi. Bagian yang baru adalah `Rhs=Self`: sintaks ini disebut _parameter tipe default_. Parameter tipe generic `Rhs` (singkatan dari “right-hand side”, sisi kanan) menentukan tipe parameter `rhs` dalam metode `add`. Jika kita tidak menentukan tipe konkret untuk `Rhs` saat mengimplementasikan trait `Add`, tipe `Rhs` akan default ke `Self`, yaitu tipe tempat kita mengimplementasikan `Add`.

Saat mengimplementasikan `Add` untuk `Point`, kita memakai nilai default `Rhs` karena kita ingin menjumlahkan dua instance `Point`. Mari kita lihat contoh implementasi trait `Add` di mana kita ingin menyesuaikan tipe `Rhs`, bukan memakai nilainya yang default.

Kita punya dua struct, `Millimeters` dan `Meters`, yang menyimpan nilai dalam satuan berbeda. Pembungkusan tipis sebuah tipe yang sudah ada ke dalam struct lain ini dikenal sebagai _pola newtype_, yang kita jelaskan lebih rinci di bagian [“Mengimplementasikan Trait Eksternal dengan Pola Newtype”][newtype]<!-- ignore -->. Kita ingin menjumlahkan nilai dalam millimeter dengan nilai dalam meter dan membiarkan implementasi `Add` melakukan konversi dengan benar. Kita bisa mengimplementasikan `Add` untuk `Millimeters` dengan `Meters` sebagai `Rhs`, seperti pada Listing 20-16.

<Listing number="20-16" file-name="src/lib.rs" caption="Mengimplementasikan trait `Add` pada `Millimeters` untuk menjumlahkan `Millimeters` dan `Meters`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-16/src/lib.rs}}
```

</Listing>

Untuk menjumlahkan `Millimeters` dan `Meters`, kita menulis `impl Add<Meters>` guna menetapkan nilai parameter tipe `Rhs`, alih-alih memakai default-nya, `Self`.

Kamu akan memakai parameter tipe default dengan dua cara utama:

1. Untuk mengembangkan sebuah tipe tanpa merusak kode yang sudah ada
2. Untuk membolehkan penyesuaian dalam kasus tertentu yang kebanyakan pengguna tidak butuh

Trait `Add` dari pustaka standar adalah contoh tujuan kedua: biasanya kamu menjumlahkan dua tipe yang sama, tetapi trait `Add` menyediakan kemampuan untuk menyesuaikan lebih jauh. Memakai parameter tipe default dalam definisi trait `Add` berarti kamu tidak perlu menyebut parameter tambahan itu hampir sepanjang waktu. Dengan kata lain, sedikit boilerplate implementasi tidak diperlukan, sehingga trait lebih mudah dipakai.

Tujuan pertama mirip dengan yang kedua, tetapi terbalik: jika kamu ingin menambahkan parameter tipe ke trait yang sudah ada, kamu bisa memberinya nilai default agar fungsionalitas trait bisa dikembangkan tanpa merusak kode implementasi yang sudah ada.

<!-- Judul lama. Jangan hapus atau tautan bisa rusak. -->

<a id="fully-qualified-syntax-for-disambiguation-calling-methods-with-the-same-name"></a>
<a id="disambiguating-between-methods-with-the-same-name"></a>

### Membedakan Metode yang Bernama Sama

Tidak ada dalam Rust yang melarang sebuah trait punya metode dengan nama yang sama dengan metode trait lain, dan Rust juga tidak melarang kamu mengimplementasikan kedua trait pada satu tipe. Kamu juga bisa mengimplementasikan metode langsung pada tipe dengan nama yang sama dengan metode dari trait.

Saat memanggil metode yang bernama sama, kamu perlu memberi tahu Rust mana yang ingin kamu pakai. Perhatikan kode pada Listing 20-17, di mana kita mendefinisikan dua trait, `Pilot` dan `Wizard`, yang keduanya punya metode bernama `fly`. Lalu kita mengimplementasikan kedua trait itu pada tipe `Human` yang sudah punya metode bernama `fly` yang diimplementasikan langsung di dalamnya. Setiap metode `fly` melakukan hal yang berbeda.

<Listing number="20-17" file-name="src/main.rs" caption="Dua trait didefinisikan dengan metode `fly` dan diimplementasikan pada tipe `Human`, serta metode `fly` diimplementasikan langsung pada `Human`.">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-17/src/main.rs:here}}
```

</Listing>

Saat kita memanggil `fly` pada instance `Human`, compiler secara default memanggil metode yang diimplementasikan langsung pada tipe itu, seperti pada Listing 20-18.

<Listing number="20-18" file-name="src/main.rs" caption="Memanggil `fly` pada instance `Human`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-18/src/main.rs:here}}
```

</Listing>

Menjalankan kode ini akan mencetak `*waving arms furiously*`, yang menunjukkan bahwa Rust memanggil metode `fly` yang diimplementasikan langsung pada `Human`.

Untuk memanggil metode `fly` dari trait `Pilot` maupun trait `Wizard`, kita perlu memakai sintaks yang lebih eksplisit untuk menentukan metode `fly` yang kita maksud. Listing 20-19 mendemonstrasikan sintaks ini.

<Listing number="20-19" file-name="src/main.rs" caption="Menentukan metode `fly` dari trait mana yang ingin kita panggil">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-19/src/main.rs:here}}
```

</Listing>

Dengan menyebut nama trait sebelum nama metode, kita memperjelas pada Rust implementasi `fly` mana yang ingin kita panggil. Kita juga bisa menulis `Human::fly(&person)`, yang setara dengan `person.fly()` yang kita pakai pada Listing 20-19, tetapi penulisannya sedikit lebih panjang jika kita tidak perlu membedakannya.

Menjalankan kode ini mencetak hal berikut:

```console
{{#include ../listings/ch20-advanced-features/listing-20-19/output.txt}}
```

Karena metode `fly` menerima parameter `self`, jika kita punya dua _tipe_ yang sama-sama mengimplementasikan satu _trait_, Rust bisa mengetahui implementasi trait mana yang dipakai berdasarkan tipe `self`.

Namun, fungsi asosiasi yang bukan metode tidak punya parameter `self`. Ketika ada beberapa tipe atau trait yang mendefinisikan fungsi bukan-metode dengan nama yang sama, Rust tidak selalu tahu tipe apa yang kamu maksud kecuali kamu memakai sintaks fully qualified. Misalnya, pada Listing 20-20, kita membuat trait untuk tempat penampungan hewan yang ingin memberi semua anak anjing nama Spot. Kita membuat trait `Animal` dengan fungsi asosiasi bukan-metode `baby_name`. Trait `Animal` diimplementasikan untuk struct `Dog`, di mana kita juga menyediakan fungsi asosiasi bukan-metode `baby_name` secara langsung.

<Listing number="20-20" file-name="src/main.rs" caption="Sebuah trait dengan fungsi asosiasi dan sebuah tipe dengan fungsi asosiasi bernama sama yang juga mengimplementasikan trait itu">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-20/src/main.rs}}
```

</Listing>

Kita mengimplementasikan kode untuk menamai semua anak anjing Spot dalam fungsi asosiasi `baby_name` yang didefinisikan pada `Dog`. Tipe `Dog` juga mengimplementasikan trait `Animal`, yang menggambarkan ciri-ciri yang dimiliki semua hewan. Anak anjing disebut *puppy*, dan hal itu diungkapkan dalam implementasi trait `Animal` pada `Dog`, melalui fungsi asosiasi `baby_name` milik trait `Animal`.

Di `main`, kita memanggil fungsi `Dog::baby_name`, yang memanggil fungsi asosiasi yang didefinisikan langsung pada `Dog`. Kode ini mencetak hal berikut:

```console
{{#include ../listings/ch20-advanced-features/listing-20-20/output.txt}}
```

Hasil ini bukan yang kita inginkan. Kita ingin memanggil fungsi `baby_name` yang merupakan bagian dari trait `Animal` yang kita implementasikan pada `Dog`, agar kode mencetak `A baby dog is called a puppy`. Teknik menyebut nama trait yang kita pakai pada Listing 20-19 tidak membantu di sini; jika kita mengubah `main` menjadi kode pada Listing 20-21, kita akan mendapat error kompilasi.

<Listing number="20-21" file-name="src/main.rs" caption="Mencoba memanggil fungsi `baby_name` dari trait `Animal`, tetapi Rust tidak tahu implementasi mana yang dipakai">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-21/src/main.rs:here}}
```

</Listing>

Karena `Animal::baby_name` tidak punya parameter `self`, dan bisa ada tipe lain yang mengimplementasikan trait `Animal`, Rust tidak bisa mengetahui implementasi `Animal::baby_name` mana yang kita inginkan. Kita akan mendapat error compiler ini:

```console
{{#include ../listings/ch20-advanced-features/listing-20-21/output.txt}}
```

Untuk membedakan dan memberi tahu Rust bahwa kita ingin memakai implementasi `Animal` untuk `Dog`, bukan implementasi `Animal` untuk tipe lain, kita perlu memakai sintaks fully qualified. Listing 20-22 menunjukkan cara memakai sintaks fully qualified.

<Listing number="20-22" file-name="src/main.rs" caption="Memakai sintaks fully qualified untuk menentukan bahwa kita ingin memanggil fungsi `baby_name` dari trait `Animal` sebagaimana diimplementasikan pada `Dog`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-22/src/main.rs:here}}
```

</Listing>

Kita memberikan anotasi tipe di dalam tanda kurung sudut, yang menandakan kita ingin memanggil metode `baby_name` dari trait `Animal` sebagaimana diimplementasikan pada `Dog`, dengan menyatakan bahwa kita ingin memperlakukan tipe `Dog` sebagai `Animal` untuk pemanggilan fungsi ini. Sekarang kode ini akan mencetak apa yang kita inginkan:

```console
{{#include ../listings/ch20-advanced-features/listing-20-22/output.txt}}
```

Secara umum, sintaks fully qualified didefinisikan sebagai berikut:

```rust,ignore
<Type as Trait>::function(receiver_if_method, next_arg, ...);
```

Untuk fungsi asosiasi yang bukan metode, tidak akan ada `receiver`: hanya ada daftar argumen lainnya. Kamu bisa memakai sintaks fully qualified di mana pun kamu memanggil fungsi atau metode. Namun, kamu boleh menghilangkan bagian mana pun dari sintaks ini yang bisa diketahui Rust dari informasi lain dalam program. Kamu hanya perlu memakai sintaks yang lebih panjang ini ketika ada beberapa implementasi dengan nama yang sama dan Rust butuh bantuan untuk mengetahui implementasi mana yang ingin kamu panggil.

<!-- Judul lama. Jangan hapus atau tautan bisa rusak. -->

<a id="using-supertraits-to-require-one-traits-functionality-within-another-trait"></a>

### Memakai Supertrait

Kadang kamu bisa menulis definisi trait yang bergantung pada trait lain: agar sebuah tipe bisa mengimplementasikan trait pertama, kamu ingin mewajibkan tipe itu juga mengimplementasikan trait kedua. Kamu melakukan ini supaya definisi trait-mu bisa memakai item asosiasi dari trait kedua. Trait yang menjadi sandaran definisi trait-mu disebut _supertrait_ dari trait tersebut.

Misalnya, kita ingin membuat trait `OutlinePrint` dengan metode `outline_print` yang mencetak nilai tertentu yang sudah diformat agar berbingkai tanda bintang. Artinya, dengan sebuah struct `Point` yang mengimplementasikan trait `Display` dari pustaka standar sehingga menghasilkan `(x, y)`, ketika kita memanggil `outline_print` pada instance `Point` yang bernilai `1` untuk `x` dan `3` untuk `y`, hasilnya harus seperti ini:

```text
**********
*        *
* (1, 3) *
*        *
**********
```

Dalam implementasi metode `outline_print`, kita ingin memakai fungsionalitas trait `Display`. Oleh karena itu, kita perlu menentukan bahwa trait `OutlinePrint` hanya bekerja untuk tipe yang juga mengimplementasikan `Display` dan menyediakan fungsionalitas yang dibutuhkan `OutlinePrint`. Kita bisa melakukan itu dalam definisi trait dengan menulis `OutlinePrint: Display`. Teknik ini mirip dengan menambahkan trait bound pada trait. Listing 20-23 menunjukkan implementasi trait `OutlinePrint`.

<Listing number="20-23" file-name="src/main.rs" caption="Mengimplementasikan trait `OutlinePrint` yang membutuhkan fungsionalitas dari `Display`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-23/src/main.rs:here}}
```

</Listing>

Karena kita sudah menentukan bahwa `OutlinePrint` membutuhkan trait `Display`, kita bisa memakai fungsi `to_string` yang otomatis diimplementasikan untuk tipe apa pun yang mengimplementasikan `Display`. Jika kita mencoba memakai `to_string` tanpa menambahkan titik dua dan menyebut trait `Display` setelah nama trait, kita akan mendapat error yang mengatakan bahwa tidak ada metode bernama `to_string` untuk tipe `&Self` dalam scope saat ini.

Mari kita lihat apa yang terjadi saat kita mencoba mengimplementasikan `OutlinePrint` pada tipe yang tidak mengimplementasikan `Display`, seperti struct `Point`:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/src/main.rs:here}}
```

</Listing>

Kita mendapat error yang mengatakan bahwa `Display` dibutuhkan tetapi tidak diimplementasikan:

```console
{{#include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/output.txt}}
```

Untuk memperbaikinya, kita mengimplementasikan `Display` pada `Point` dan memenuhi batasan yang dibutuhkan `OutlinePrint`, seperti ini:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-03-impl-display-for-point/src/main.rs:here}}
```

</Listing>

Setelah itu, mengimplementasikan trait `OutlinePrint` pada `Point` akan berhasil dikompilasi, dan kita bisa memanggil `outline_print` pada instance `Point` untuk menampilkannya di dalam bingkai tanda bintang.

<!-- Judul lama. Jangan hapus atau tautan bisa rusak. -->

<a id="using-the-newtype-pattern-to-implement-external-traits-on-external-types"></a>
<a id="using-the-newtype-pattern-to-implement-external-traits"></a>

<a id="implementing-external-traits-with-the-newtype-pattern"></a>
### Mengimplementasikan Trait Eksternal dengan Pola Newtype

Di bagian [“Mengimplementasikan Trait pada Sebuah Tipe”][implementing-a-trait-on-a-type]<!--
ignore --> pada Bab 10, kita menyebut aturan orphan yang menyatakan bahwa kita hanya boleh mengimplementasikan sebuah trait pada sebuah tipe jika trait-nya, tipe-nya, atau keduanya, lokal terhadap crate kita. Kita bisa mengakali pembatasan ini memakai pola newtype, yang melibatkan pembuatan tipe baru dalam tuple struct. (Kita membahas tuple struct di bagian [“Membuat Tipe Berbeda dengan Tuple Struct”][tuple-structs]<!-- ignore --> pada Bab 5.) Tuple struct itu akan punya satu field dan menjadi pembungkusan tipis di sekitar tipe yang ingin kita beri implementasi trait. Dengan begitu, tipe pembungkusnya lokal terhadap crate kita, dan kita bisa mengimplementasikan trait pada pembungkus tersebut. _Newtype_ adalah istilah yang berasal dari bahasa pemrograman Haskell. Pola ini tidak menimbulkan penalti performa saat runtime, dan tipe pembungkusnya dihilangkan pada saat kompilasi.

Sebagai contoh, misalkan kita ingin mengimplementasikan `Display` pada `Vec<T>`, yang dicegah langsung oleh aturan orphan karena trait `Display` dan tipe `Vec<T>` didefinisikan di luar crate kita. Kita bisa membuat struct `Wrapper` yang menyimpan instance `Vec<T>`; lalu, kita bisa mengimplementasikan `Display` pada `Wrapper` dan memakai nilai `Vec<T>` tersebut, seperti pada Listing 20-24.

<Listing number="20-24" file-name="src/main.rs" caption="Membuat tipe `Wrapper` di sekitar `Vec<String>` untuk mengimplementasikan `Display`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-24/src/main.rs}}
```

</Listing>

Implementasi `Display` memakai `self.0` untuk mengakses `Vec<T>` di dalamnya karena `Wrapper` adalah tuple struct dan `Vec<T>` adalah item pada indeks 0 dalam tuple itu. Lalu, kita bisa memakai fungsionalitas trait `Display` pada `Wrapper`.

Kelemahan teknik ini adalah `Wrapper` merupakan tipe baru, jadi ia tidak punya metode-metode dari nilai yang disimpannya. Kita harus mengimplementasikan semua metode `Vec<T>` langsung pada `Wrapper` sehingga metode-metode itu mendelegasikan ke `self.0`, yang akan memungkinkan kita memperlakukan `Wrapper` persis seperti `Vec<T>`. Jika kita ingin tipe baru itu punya setiap metode yang dimiliki tipe di dalamnya, salah satu solusinya adalah mengimplementasikan trait `Deref` pada `Wrapper` untuk mengembalikan tipe dalam tersebut (kita membahas implementasi trait `Deref` di bagian [“Memperlakukan Smart Pointer seperti Reference Biasa”][smart-pointer-deref]<!-- ignore --> pada Bab 15). Jika kita tidak ingin tipe `Wrapper` punya semua metode tipe di dalamnya—misalnya, untuk membatasi perilaku tipe `Wrapper`—kita harus mengimplementasikan secara manual hanya metode yang memang kita inginkan.

Pola newtype ini juga berguna meskipun tidak melibatkan trait. Mari kita mengalihkan fokus dan melihat beberapa cara lanjutan untuk berinteraksi dengan sistem tipe Rust.

[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern
[implementing-a-trait-on-a-type]: ch10-02-traits.html#implementing-a-trait-on-a-type
[traits]: ch10-02-traits.html
[smart-pointer-deref]: ch15-02-deref.html#treating-smart-pointers-like-regular-references
[tuple-structs]: ch05-01-defining-structs.html#creating-different-types-with-tuple-structs
