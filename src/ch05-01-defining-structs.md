## Mendefinisikan dan Menginstansiasi Struct

Struct mirip dengan tuple, yang dibahas di bagian ["Tipe Tuple"][tuples]<!--
ignore -->, karena keduanya menyimpan beberapa nilai yang saling terkait. Seperti
tuple, bagian-bagian sebuah struct boleh bertipe berbeda. Bedanya dengan tuple,
dalam struct kamu memberi nama pada setiap bagian data sehingga jelas apa arti
nilai-nilai itu. Berkat nama inilah, struct lebih fleksibel daripada tuple:
kamu tidak perlu bergantung pada urutan data untuk menentukan atau mengakses
nilai sebuah instance.

Untuk mendefinisikan struct, kita menulis keyword `struct` dan memberi nama pada
keseluruhan struct itu. Nama struct sebaiknya menggambarkan arti dari
bagian-bagian data yang dikelompokkan. Kemudian, di dalam kurung kurawal, kita
mendefinisikan nama dan tipe dari bagian-bagian data tersebut, yang kita sebut
_field_. Sebagai contoh, Listing 5-1 menunjukkan struct yang menyimpan
informasi tentang akun pengguna.

<Listing number="5-1" file-name="src/main.rs" caption="Definisi struct `User`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-01/src/main.rs:here}}
```

</Listing>

Setelah sebuah struct didefinisikan, kita bisa memakainya dengan membuat
_instance_ dari struct tersebut. Caranya, tentukan nilai konkret untuk setiap
field. Kita membuat instance dengan menyebut nama struct, lalu menambahkan
kurung kurawal yang berisi pasangan _`key: value`_, di mana key adalah nama
field dan value adalah data yang ingin kita simpan di field tersebut. Urutan
field tidak harus sama dengan urutan deklarasinya di dalam struct. Singkatnya,
definisi struct ibarat template umum bagi sebuah tipe, dan instance mengisi
template itu dengan data tertentu untuk menghasilkan nilai bertipe demikian.
Sebagai contoh, kita bisa mendeklarasikan sebuah pengguna tertentu seperti
Listing 5-2.

<Listing number="5-2" file-name="src/main.rs" caption="Membuat instance struct `User`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-02/src/main.rs:here}}
```

</Listing>

Untuk mengambil nilai tertentu dari sebuah struct, kita memakai notasi titik.
Sebagai contoh, untuk mengakses alamat email pengguna ini, kita menulis
`user1.email`. Jika instance-nya mutable, kita bisa mengubah sebuah nilai
dengan notasi titik yang menempatkan nilai baru ke field tersebut. Listing 5-3
menunjukkan cara mengubah nilai pada field `email` sebuah instance `User` yang
mutable.

<Listing number="5-3" file-name="src/main.rs" caption="Mengubah nilai pada field `email` sebuah instance `User`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-03/src/main.rs:here}}
```

</Listing>

Perhatikan bahwa seluruh instance harus mutable; Rust tidak mengizinkan kita
menandai hanya sebagian field sebagai mutable. Sama seperti ekspresi lain, kita
bisa membentuk instance baru dari struct sebagai ekspresi terakhir di dalam
badan fungsi untuk mengembalikan instance baru itu secara implisit.

Listing 5-4 menunjukkan fungsi `build_user` yang mengembalikan sebuah instance
`User` dengan email dan username yang diberikan. Field `active` mendapat nilai
`true`, dan `sign_in_count` mendapat nilai `1`.

<Listing number="5-4" file-name="src/main.rs" caption="Fungsi `build_user` yang menerima email dan username lalu mengembalikan sebuah instance `User`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-04/src/main.rs:here}}
```

</Listing>

Wajar jika nama parameter fungsi sama dengan nama field struct, tapi harus
mengulang nama dan variabel `email` dan `username` terasa sedikit menyebalkan.
Kalau struct punya lebih banyak field, mengulang setiap nama akan semakin
merepotkan. Untungnya, ada shorthand yang praktis!

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-field-init-shorthand-when-variables-and-fields-have-the-same-name"></a>

### Memakai Field Init Shorthand

Karena nama parameter dan nama field struct persis sama di Listing 5-4, kita
bisa memakai sintaks _field init shorthand_ untuk menulis ulang `build_user`
agar perilakunya tetap sama persis, tapi tanpa mengulang `username` dan
`email`, seperti yang ditunjukkan Listing 5-5.

<Listing number="5-5" file-name="src/main.rs" caption="Fungsi `build_user` yang memakai field init shorthand karena parameter `username` dan `email` bernama sama dengan field struct">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-05/src/main.rs:here}}
```

</Listing>

Di sini kita membuat instance baru dari struct `User` yang punya field bernama
`email`. Kita ingin mengisi nilai field `email` dengan nilai dari parameter
`email` fungsi `build_user`. Karena field `email` dan parameter `email` bernama
sama, kita cukup menulis `email` saja, bukan `email: email`.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-instances-from-other-instances-with-struct-update-syntax"></a>

### Membuat Instance dengan Struct Update Syntax

Sering kali kita ingin membuat instance struct baru yang memuat sebagian besar
nilai dari instance lain bertipe sama, tetapi dengan beberapa nilai yang
diubah. Kamu bisa melakukannya memakai struct update syntax.

Pertama, Listing 5-6 menunjukkan cara membuat instance `User` baru di `user2`
dengan cara biasa, tanpa update syntax. Kita menetapkan nilai baru untuk
`email`, tapi selain itu memakai nilai-nilai dari `user1` yang kita buat di
Listing 5-2.

<Listing number="5-6" file-name="src/main.rs" caption="Membuat instance `User` baru dengan memakai semua nilai dari `user1` kecuali satu">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-06/src/main.rs:here}}
```

</Listing>

Dengan struct update syntax, kita bisa mencapai efek yang sama dengan kode yang
lebih sedikit, seperti yang ditunjukkan Listing 5-7. Sintaks `..` menentukan
bahwa field-field yang tidak diisi secara eksplisit akan mendapat nilai yang
sama dengan field pada instance yang diberikan.

<Listing number="5-7" file-name="src/main.rs" caption="Memakai struct update syntax untuk menetapkan nilai `email` baru pada sebuah instance `User`, sambil memakai sisa nilai dari `user1`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-07/src/main.rs:here}}
```

</Listing>

Kode pada Listing 5-7 juga membuat instance di `user2` dengan nilai `email`
yang berbeda, tetapi nilai field `username`, `active`, dan `sign_in_count`
sama dengan milik `user1`. `..user1` harus diletakkan terakhir untuk
menandakan bahwa sisa field akan mengambil nilainya dari field yang
sepadan di `user1`, tapi kita boleh menentukan nilai untuk sebanyak mungkin
field yang kita mau, dalam urutan apa pun, tanpa peduli urutan field dalam
definisi struct.

Perhatikan bahwa struct update syntax memakai `=` seperti halnya assignment;
ini karena sintaks tersebut memindahkan data, seperti yang kita lihat di
bagian ["Variabel dan Data Berinteraksi dengan Move"][move]<!-- ignore -->.
Pada contoh ini, kita tidak bisa lagi memakai `user1` setelah membuat `user2`
karena `String` pada field `username` milik `user1` sudah dipindahkan ke
`user2`. Jika kita memberi `user2` nilai `String` baru untuk `email` dan
`username`, sehingga hanya nilai `active` dan `sign_in_count` yang diambil dari
`user1`, maka `user1` akan tetap valid setelah `user2` dibuat. Baik `active`
maupun `sign_in_count` bertipe yang mengimplementasikan trait `Copy`, jadi
perilaku yang kita bahas di bagian ["Data Khusus Stack: Copy"][copy]<!--
ignore --> akan berlaku. Kita juga masih bisa memakai `user1.email` pada contoh
ini, karena nilainya tidak dipindahkan keluar dari `user1`.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-tuple-structs-without-named-fields-to-create-different-types"></a>

<a id="creating-different-types-with-tuple-structs"></a>
### Membuat Tipe Berbeda dengan Tuple Struct

Rust juga mendukung struct yang mirip tuple, yang disebut _tuple struct_. Tuple
struct punya tambahan makna dari nama struct-nya, tetapi field-fieldnya tidak
punya nama; yang ada hanya tipe tiap field. Tuple struct berguna ketika kamu
ingin memberi nama pada keseluruhan tuple sehingga tuple itu menjadi tipe yang
berbeda dari tuple lain, dan ketika menamai setiap field seperti pada struct
biasa akan terlalu panjang atau berlebihan.

Untuk mendefinisikan tuple struct, mulailah dengan keyword `struct` dan nama
struct, lalu ikuti dengan tipe-tipe di dalam tuple. Sebagai contoh, di sini
kita mendefinisikan dan memakai dua tuple struct bernama `Color` dan `Point`:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-01-tuple-structs/src/main.rs}}
```

</Listing>

Perhatikan bahwa nilai `black` dan `origin` bertipe berbeda karena keduanya
adalah instance dari tuple struct yang berbeda. Setiap struct yang kamu
definisikan adalah tipe-nya sendiri, meski field-field di dalamnya boleh saja
bertipe sama. Sebagai contoh, fungsi yang menerima parameter bertipe `Color`
tidak bisa menerima `Point` sebagai argumen, meski kedua tipe tersusun atas
tiga nilai `i32`. Selain itu, instance tuple struct mirip tuple: kamu bisa
mendestruksinya menjadi bagian-bagian penyusunnya, dan kamu bisa memakai `.`
diikuti indeks untuk mengakses nilai tertentu. Bedanya dengan tuple, tuple
struct mengharuskan kamu menyebut nama struct-nya saat mendestruksi. Sebagai
contoh, kita akan menulis `let Point(x, y, z) = origin;` untuk mendestruksi
nilai di titik `origin` menjadi variabel bernama `x`, `y`, dan `z`.

<!-- Old headings. Do not remove or links may break. -->

<a id="unit-like-structs-without-any-fields"></a>

### Mendefinisikan Unit-Like Struct

Kamu juga bisa mendefinisikan struct yang tidak punya field sama sekali!
Struct ini disebut _unit-like structs_ karena perilakunya mirip `()`, tipe unit
yang kita sebut di bagian ["Tipe Tuple"][tuples]<!-- ignore -->. Unit-like
struct bisa berguna ketika kamu perlu mengimplementasikan sebuah trait pada
suatu tipe, tetapi tidak punya data yang ingin disimpan di tipe itu sendiri.
Kita akan membahas trait di Bab 10. Berikut contoh pendeklarasian dan
penginstansian sebuah unit struct bernama `AlwaysEqual`:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-04-unit-like-structs/src/main.rs}}
```

</Listing>

Untuk mendefinisikan `AlwaysEqual`, kita memakai keyword `struct`, nama yang
kita inginkan, lalu titik koma. Tidak perlu kurung kurawal maupun kurung
biasa! Setelah itu, kita bisa membuat instance `AlwaysEqual` di variabel
`subject` dengan cara serupa: memakai nama yang kita definisikan, tanpa kurung
kurawal maupun kurung biasa. Bayangkan kelak kita mengimplementasikan
perilaku untuk tipe ini sehingga setiap instance `AlwaysEqual` selalu sama
dengan setiap instance tipe lain mana pun, misalnya untuk mendapatkan hasil
yang diketahui saat testing. Kita tidak butuh data apa pun untuk
mengimplementasikan perilaku itu! Di Bab 10 kamu akan melihat cara
mendefinisikan trait dan mengimplementasikannya pada tipe mana pun,
termasuk unit-like structs.

> ### Ownership Data Struct
>
> Pada definisi struct `User` di Listing 5-1, kita memakai tipe `String` yang
> dimiliki (owned) alih-alih tipe string slice `&str`. Ini pilihan yang
> disengaja, karena kita ingin setiap instance struct memiliki seluruh datanya
> sendiri dan data itu valid selama struct-nya sendiri masih valid.
>
> Struct juga bisa menyimpan reference ke data yang dimiliki pihak lain,
> tetapi untuk melakukannya kita perlu memakai _lifetime_, fitur Rust yang akan
> kita bahas di Bab 10. Lifetime memastikan bahwa data yang direferensikan
> sebuah struct selalu valid selama struct itu sendiri valid. Misalnya kamu
> mencoba menyimpan sebuah reference di dalam struct tanpa menentukan lifetime,
> seperti berikut di *src/main.rs*; ini tidak akan berhasil:
>
> <Listing file-name="src/main.rs">
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore,does_not_compile
> struct User {
>     active: bool,
>     username: &str,
>     email: &str,
>     sign_in_count: u64,
> }
>
> fn main() {
>     let user1 = User {
>         active: true,
>         username: "someusername123",
>         email: "someone@example.com",
>         sign_in_count: 1,
>     };
> }
> ```
>
> </Listing>
>
> Compiler akan mengeluh bahwa ia membutuhkan spesifier lifetime:
>
> ```console
> $ cargo run
>    Compiling structs v0.1.0 (file:///projects/structs)
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:3:15
>   |
> 3 |     username: &str,
>   |               ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 ~     username: &'a str,
>   |
>
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:4:12
>   |
> 4 |     email: &str,
>   |            ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 |     username: &str,
> 4 ~     email: &'a str,
>   |
>
> For more information about this error, try `rustc --explain E0106`.
> error: could not compile `structs` (bin "structs") due to 2 previous errors
> ```
>
> Di Bab 10, kita akan membahas cara memperbaiki error tersebut agar kamu bisa
> menyimpan reference di dalam struct, tapi untuk sekarang, kita akan
> mengatasi error semacam ini dengan memakai tipe owned seperti `String`
> alih-alih reference seperti `&str`.

<!-- manual-regeneration
for the error above
after running update-rustc.sh:
pbcopy < listings/ch05-using-structs-to-structure-related-data/no-listing-02-reference-in-struct/output.txt
paste above
add `> ` before every line -->

[tuples]: ch03-02-data-types.html#the-tuple-type
[move]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-move
[copy]: ch04-01-what-is-ownership.html#stack-only-data-copy
