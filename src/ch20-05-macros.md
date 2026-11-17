<a id="macros"></a>
## Macro

Kita sudah memakai macro seperti `println!` di seluruh buku ini, tapi kita belum benar-benar menjelajahi apa itu macro dan cara kerjanya. Istilah _macro_ merujuk pada sekumpulan fitur di Rust—macro deklaratif dengan `macro_rules!` dan tiga jenis macro prosedural:

- Macro `#[derive]` kustom yang menentukan kode yang ditambahkan dengan atribut `derive` yang dipakai pada struct dan enum
- Macro seperti atribut yang mendefinisikan atribut kustom yang bisa dipakai pada item apa pun
- Macro seperti fungsi yang tampak seperti pemanggilan fungsi, tapi bekerja pada token yang ditentukan sebagai argumennya

Kita akan membahas masing-masing secara bergiliran, tapi pertama, mari kita lihat mengapa kita perlu macro sama sekali saat kita sudah punya fungsi.

### Perbedaan Antara Macro dan Fungsi

Pada dasarnya, macro adalah cara menulis kode yang menulis kode lain, yang dikenal sebagai _metaprogramming_. Di Lampiran C, kita membahas atribut `derive`, yang menghasilkan implementasi dari berbagai trait untukmu. Kita juga sudah memakai macro `println!` dan `vec!` di seluruh buku. Semua macro ini _diperluas_ menghasilkan lebih banyak kode daripada kode yang kamu tulis sendiri.

Metaprogramming berguna untuk mengurangi jumlah kode yang harus kamu tulis dan rawat, yang juga salah satu peran fungsi. Namun, macro punya kemampuan tambahan yang tidak dimiliki fungsi.

Tanda tangan fungsi harus mendeklarasikan jumlah dan tipe parameter yang dimiliki fungsi. Macro, di sisi lain, bisa menerima jumlah parameter yang berubah-ubah: Kita bisa memanggil `println!("hello")` dengan satu argumen atau `println!("hello {}", name)` dengan dua argumen. Selain itu, macro diperluas sebelum compiler menafsirkan makna kode, sehingga macro bisa, misalnya, mengimplementasikan trait pada tipe tertentu. Fungsi tidak bisa, karena fungsi dipanggil saat runtime sementara trait perlu diimplementasikan saat compile time.

Kelemahan memilih macro alih-alih fungsi adalah definisi macro lebih kompleks daripada definisi fungsi, karena kamu menulis kode Rust yang menulis kode Rust. Karena lapisan perantara ini, definisi macro umumnya lebih sulit dibaca, dipahami, dan dirawat daripada definisi fungsi.

Perbedaan penting lain antara macro dan fungsi adalah kamu harus mendefinisikan macro atau membawanya ke dalam scope _sebelum_ memanggilnya di sebuah file. Fungsi bisa kamu definisikan di mana saja dan panggil di mana saja.

<!-- Old headings. Do not remove or links may break. -->

<a id="declarative-macros-with-macro_rules-for-general-metaprogramming"></a>

### Macro Deklaratif untuk Metaprogramming Umum

Bentuk macro yang paling luas dipakai di Rust adalah _macro deklaratif_. Kadang ini juga disebut "macro berbasis contoh," "macro `macro_rules!`," atau cukup "macro" saja. Pada dasarnya, macro deklaratif memungkinkan kamu menulis sesuatu yang mirip dengan ekspresi `match` di Rust. Seperti dibahas di Bab 6, ekspresi `match` adalah struktur kontrol yang mengambil sebuah ekspresi, membandingkan nilai hasil ekspresi itu dengan pattern, lalu menjalankan kode yang terkait dengan pattern yang cocok. Macro juga membandingkan sebuah nilai dengan pattern yang terkait dengan kode tertentu: Dalam hal ini, nilainya adalah kode sumber Rust literal yang diberikan kepada macro; pattern dibandingkan dengan struktur kode sumber itu; dan kode yang terkait dengan setiap pattern, saat cocok, menggantikan kode yang diberikan kepada macro. Semua ini terjadi saat kompilasi.

Untuk mendefinisikan macro, kamu memakai konstruksi `macro_rules!`. Mari kita lihat cara memakai `macro_rules!` dengan meninjau bagaimana macro `vec!` didefinisikan. Bab 8 sudah membahas cara memakai macro `vec!` untuk membuat vector baru dengan nilai-nilai tertentu. Misalnya, macro berikut membuat vector baru yang berisi tiga bilangan bulat:

```rust
let v: Vec<u32> = vec![1, 2, 3];
```

Kita juga bisa memakai macro `vec!` untuk membuat vector berisi dua bilangan bulat atau vector berisi lima string slice. Kita tidak bisa melakukan hal yang sama dengan fungsi, karena kita tidak tahu jumlah atau tipe nilai di awal.

Listing 20-35 menunjukkan definisi macro `vec!` yang sedikit disederhanakan.

<Listing number="20-35" file-name="src/lib.rs" caption="Versi sederhana dari definisi macro `vec!`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-35/src/lib.rs}}
```

</Listing>

> Catatan: Definisi asli macro `vec!` di pustaka standar menyertakan kode untuk mengalokasikan memori secukupnya di awal. Kode itu adalah optimasi yang tidak kita sertakan di sini agar contohnya lebih sederhana.

Anotasi `#[macro_export]` menandakan bahwa macro ini harus tersedia setiap kali crate tempat macro didefinisikan dibawa ke dalam scope. Tanpa anotasi ini, macro tidak bisa dibawa ke dalam scope.

Lalu kita mulai definisi macro dengan `macro_rules!` dan nama macro yang kita definisikan _tanpa_ tanda seru. Nama itu, dalam hal ini `vec`, diikuti oleh kurung kurawal yang menandakan isi definisi macro.

Struktur di dalam isi `vec!` mirip dengan struktur ekspresi `match`. Di sini kita punya satu arm dengan pattern `( $( $x:expr ),* )`, diikuti oleh `=>` dan blok kode yang terkait dengan pattern ini. Jika pattern cocok, blok kode terkait akan dikeluarkan. Karena ini satu-satunya pattern dalam macro ini, hanya ada satu cara pencocokan yang valid; pattern lain akan menghasilkan error. Macro yang lebih kompleks punya lebih dari satu arm.

Sintaks pattern yang valid dalam definisi macro berbeda dengan sintaks pattern yang dibahas di Bab 19, karena pattern macro dicocokkan dengan struktur kode Rust, bukan dengan nilai. Mari kita telusuri arti bagian-bagian pattern di Listing 20-29; untuk sintaks pattern macro lengkap, lihat [Referensi Rust][ref].

Pertama, kita memakai sepasang tanda kurung untuk mencakup seluruh pattern. Kita memakai tanda dolar (`$`) untuk mendeklarasikan variabel dalam sistem macro yang akan berisi kode Rust yang cocok dengan pattern. Tanda dolar itu memperjelas bahwa ini adalah variabel macro, bukan variabel Rust biasa. Selanjutnya ada sepasang tanda kurung yang menangkap nilai-nilai yang cocok dengan pattern di dalam tanda kurung tersebut untuk dipakai dalam kode pengganti. Di dalam `$()` ada `$x:expr`, yang cocok dengan ekspresi Rust apa pun dan memberi ekspresi itu nama `$x`.

Koma setelah `$()` menandakan bahwa karakter pemisah koma literal harus muncul di antara setiap bagian kode yang cocok dengan kode di dalam `$()`. `*` menentukan bahwa pattern cocok dengan nol atau lebih dari apa pun yang mendahului `*`.

Saat kita memanggil macro ini dengan `vec![1, 2, 3];`, pattern `$x` cocok tiga kali dengan tiga ekspresi `1`, `2`, dan `3`.

Sekarang mari kita lihat pattern di dalam isi kode yang terkait dengan arm ini: `temp_vec.push()` di dalam `$()*` dihasilkan untuk setiap bagian yang cocok dengan `$()` dalam pattern, nol atau lebih kali tergantung seberapa sering pattern cocok. `$x` diganti dengan setiap ekspresi yang cocok. Saat kita memanggil macro ini dengan `vec![1, 2, 3];`, kode yang dihasilkan untuk mengganti pemanggilan macro itu adalah sebagai berikut:

```rust,ignore
{
    let mut temp_vec = Vec::new();
    temp_vec.push(1);
    temp_vec.push(2);
    temp_vec.push(3);
    temp_vec
}
```

Kita sudah mendefinisikan macro yang bisa menerima argumen dalam jumlah berapa pun dengan tipe apa pun, dan bisa menghasilkan kode untuk membuat vector yang berisi elemen-elemen yang ditentukan.

Untuk mempelajari lebih lanjut cara menulis macro, baca dokumentasi online atau sumber lain, seperti ["The Little Book of Rust Macros"][tlborm] yang dimulai oleh Daniel Keep dan dilanjutkan oleh Lukas Wirth.

### Macro Prosedural untuk Menghasilkan Kode dari Atribut

Bentuk macro kedua adalah macro prosedural, yang berlakunya lebih seperti fungsi (dan merupakan sejenis prosedur). _Macro prosedural_ menerima kode sebagai masukan, memproses kode itu, dan menghasilkan kode sebagai keluaran, alih-alih mencocokkan pattern dan mengganti kode dengan kode lain seperti yang dilakukan macro deklaratif. Ketiga jenis macro prosedural adalah `derive` kustom, seperti atribut, dan seperti fungsi; semuanya bekerja dengan cara yang mirip.

Saat membuat macro prosedural, definisinya harus berada di crate tersendiri dengan tipe crate khusus. Ini karena alasan teknis yang kompleks yang semoga bisa kita hilangkan di masa depan. Di Listing 20-36, kita menunjukkan cara mendefinisikan macro prosedural, di mana `some_attribute` adalah placeholder untuk jenis macro tertentu.

<Listing number="20-36" file-name="src/lib.rs" caption="Contoh mendefinisikan macro prosedural">

```rust,ignore
use proc_macro::TokenStream;

#[some_attribute]
pub fn some_name(input: TokenStream) -> TokenStream {
}
```

</Listing>

Fungsi yang mendefinisikan macro prosedural menerima `TokenStream` sebagai masukan dan menghasilkan `TokenStream` sebagai keluaran. Tipe `TokenStream` didefinisikan oleh crate `proc_macro` yang disertakan bersama Rust dan mewakili urutan token. Inilah inti macro tersebut: kode sumber yang diproses macro membentuk `TokenStream` masukan, dan kode yang dihasilkan macro adalah `TokenStream` keluaran. Fungsi itu juga memiliki atribut yang menentukan jenis macro prosedural apa yang kita buat. Kita bisa memiliki beberapa jenis macro prosedural dalam satu crate.

Mari kita lihat berbagai jenis macro prosedural. Kita mulai dengan macro `derive` kustom, lalu menjelaskan perbedaan kecil yang membedakan bentuk-bentuk lainnya.

<!-- Old headings. Do not remove or links may break. -->

<a id="how-to-write-a-custom-derive-macro"></a>

<a id="custom-derive-macros"></a>
### Macro `derive` Kustom

Mari kita buat crate bernama `hello_macro` yang mendefinisikan trait bernama `HelloMacro` dengan satu fungsi terkait bernama `hello_macro`. Alih-alih menyuruh pengguna kita mengimplementasikan trait `HelloMacro` untuk setiap tipe mereka, kita akan menyediakan macro prosedural agar pengguna bisa memberi anotasi pada tipe mereka dengan `#[derive(HelloMacro)]` untuk mendapatkan implementasi default dari fungsi `hello_macro`. Implementasi default itu akan mencetak `Hello, Macro! My name is TypeName!` di mana `TypeName` adalah nama tipe tempat trait ini didefinisikan. Dengan kata lain, kita akan menulis crate yang memungkinkan programmer lain menulis kode seperti Listing 20-37 memakai crate kita.

<Listing number="20-37" file-name="src/main.rs" caption="Kode yang bisa ditulis pengguna crate kita saat memakai macro prosedural kita">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-37/src/main.rs}}
```

</Listing>

Kode ini akan mencetak `Hello, Macro! My name is Pancakes!` setelah kita selesai. Langkah pertama adalah membuat crate library baru, seperti ini:

```console
$ cargo new hello_macro --lib
```

Selanjutnya, di Listing 20-38, kita akan mendefinisikan trait `HelloMacro` dan fungsi terkaitnya.

<Listing file-name="src/lib.rs" number="20-38" caption="Trait sederhana yang akan kita pakai dengan macro `derive`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-38/hello_macro/src/lib.rs}}
```

</Listing>

Kita sudah punya trait dan fungsinya. Pada titik ini, pengguna crate kita bisa mengimplementasikan trait itu untuk mendapatkan fungsionalitas yang diinginkan, seperti di Listing 20-39.

<Listing number="20-39" file-name="src/main.rs" caption="Tampilan jika pengguna menulis implementasi manual dari trait `HelloMacro`">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-39/pancakes/src/main.rs}}
```

</Listing>

Namun, mereka harus menulis blok implementasi untuk setiap tipe yang ingin dipakai dengan `hello_macro`; kita ingin membebaskan mereka dari pekerjaan ini.

Selain itu, kita belum bisa memberikan fungsi `hello_macro` implementasi default yang mencetak nama tipe tempat trait diimplementasikan: Rust tidak punya kemampuan refleksi, sehingga tidak bisa mencari nama tipe itu saat runtime. Kita butuh macro untuk menghasilkan kode saat compile time.

Langkah berikutnya adalah mendefinisikan macro prosedural. Saat buku ini ditulis, macro prosedural harus berada di crate tersendiri. Suatu hari nanti, pembatasan ini mungkin dicabut. Konvensi penyusunan crate dan crate macro adalah sebagai berikut: Untuk crate bernama `foo`, crate macro prosedural `derive` kustom bernama `foo_derive`. Mari kita buat crate baru bernama `hello_macro_derive` di dalam proyek `hello_macro` kita:

```console
$ cargo new hello_macro_derive --lib
```

Kedua crate kita saling terkait erat, jadi kita buat crate macro prosedural itu di dalam direktori crate `hello_macro`. Jika kita mengubah definisi trait di `hello_macro`, kita juga harus mengubah implementasi macro prosedural di `hello_macro_derive`. Kedua crate perlu diterbitkan secara terpisah, dan programmer yang memakainya perlu menambahkan keduanya sebagai dependensi serta membawa keduanya ke dalam scope. Kita juga bisa membuat crate `hello_macro` memakai `hello_macro_derive` sebagai dependensi dan mengekspor ulang kode macro proseduralnya. Namun, cara kita menyusun proyek ini memungkinkan programmer memakai `hello_macro` meski mereka tidak ingin fitur `derive`.

Kita perlu mendeklarasikan crate `hello_macro_derive` sebagai crate macro prosedural. Kita juga akan membutuhkan fungsionalitas dari crate `syn` dan `quote`, seperti yang akan kamu lihat sebentar lagi, jadi kita perlu menambahkannya sebagai dependensi. Tambahkan berikut ke file _Cargo.toml_ milik `hello_macro_derive`:

<Listing file-name="hello_macro_derive/Cargo.toml">

```toml
{{#include ../listings/ch20-advanced-features/listing-20-40/hello_macro/hello_macro_derive/Cargo.toml:6:12}}
```

</Listing>

Untuk mulai mendefinisikan macro prosedural, letakkan kode di Listing 20-40 ke file _src/lib.rs_ milik crate `hello_macro_derive`. Perhatikan bahwa kode ini belum akan dikompilasi sampai kita menambahkan definisi untuk fungsi `impl_hello_macro`.

<Listing number="20-40" file-name="hello_macro_derive/src/lib.rs" caption="Kode yang umumnya dibutuhkan kebanyakan crate macro prosedural untuk memproses kode Rust">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-40/hello_macro/hello_macro_derive/src/lib.rs}}
```

</Listing>

Perhatikan bahwa kita membagi kode menjadi fungsi `hello_macro_derive`, yang bertugas mengurai `TokenStream`, dan fungsi `impl_hello_macro`, yang bertugas mengubah pohon sintaks: Ini membuat penulisan macro prosedural lebih praktis. Kode di fungsi luar (`hello_macro_derive` dalam hal ini) akan sama untuk hampir setiap crate macro prosedural yang kamu lihat atau buat. Kode yang kamu tulis di dalam fungsi dalam (`impl_hello_macro` dalam hal ini) akan berbeda-beda tergantung tujuan macro proseduralmu.

Kita sudah memperkenalkan tiga crate baru: `proc_macro`, [`syn`][syn]<!-- ignore -->, dan [`quote`][quote]<!-- ignore -->. Crate `proc_macro` bawaan Rust, jadi kita tidak perlu menambahkannya ke dependensi di _Cargo.toml_. Crate `proc_macro` adalah API compiler yang memungkinkan kita membaca dan memanipulasi kode Rust dari kode kita.

Crate `syn` mengurai kode Rust dari string menjadi struktur data yang bisa kita olah. Crate `quote` mengubah struktur data `syn` kembali menjadi kode Rust. Crate-crate ini membuat penguraian berbagai kode Rust yang ingin kita tangani jauh lebih sederhana: Menulis parser lengkap untuk kode Rust bukan tugas yang mudah.

Fungsi `hello_macro_derive` akan dipanggil saat pengguna library kita menentukan `#[derive(HelloMacro)]` pada sebuah tipe. Ini mungkin karena kita memberi anotasi pada fungsi `hello_macro_derive` di sini dengan `proc_macro_derive` dan menentukan nama `HelloMacro`, yang cocok dengan nama trait kita; ini adalah konvensi yang diikuti kebanyakan macro prosedural.

Fungsi `hello_macro_derive` pertama-tama mengubah `input` dari `TokenStream` menjadi struktur data yang bisa kita artikan dan olah. Di sinilah `syn` berperan. Fungsi `parse` dalam `syn` menerima `TokenStream` dan mengembalikan struct `DeriveInput` yang mewakili kode Rust yang telah diurai. Listing 20-41 menunjukkan bagian-bagian relevan dari struct `DeriveInput` yang kita dapatkan setelah mengurai string `struct Pancakes;`.

<Listing number="20-41" caption="Instance `DeriveInput` yang kita dapatkan saat mengurai kode yang memiliki atribut macro di Listing 20-37">

```rust,ignore
DeriveInput {
    // --snip--

    ident: Ident {
        ident: "Pancakes",
        span: #0 bytes(95..103)
    },
    data: Struct(
        DataStruct {
            struct_token: Struct,
            fields: Unit,
            semi_token: Some(
                Semi
            )
        }
    )
}
```

</Listing>

Field-field struct ini menunjukkan bahwa kode Rust yang kita uri adalah unit struct dengan `ident` (_identifier_, artinya nama) `Pancakes`. Masih ada field lain pada struct ini untuk mendeskripsikan berbagai macam kode Rust; lihat [dokumentasi `syn` untuk `DeriveInput`][syn-docs] untuk informasi lebih lanjut.

Sebentar lagi kita akan mendefinisikan fungsi `impl_hello_macro`, yaitu tempat kita membangun kode Rust baru yang ingin kita sertakan. Tapi sebelum itu, perhatikan bahwa keluaran macro `derive` kita juga berupa `TokenStream`. `TokenStream` yang dikembalikan ditambahkan ke kode yang ditulis pengguna crate kita, sehingga saat mereka mengompilasi crate, mereka mendapatkan fungsionalitas tambahan yang kita sediakan dalam `TokenStream` yang telah diubah itu.

Kamu mungkin memperhatikan bahwa kita memanggil `unwrap` agar fungsi `hello_macro_derive` panic jika pemanggilan fungsi `syn::parse` gagal di sini. Macro prosedural kita memang perlu panic saat terjadi error, karena fungsi `proc_macro_derive` harus mengembalikan `TokenStream`, bukan `Result`, agar sesuai dengan API macro prosedural. Kita menyederhanakan contoh ini dengan memakai `unwrap`; pada kode produksi, kamu sebaiknya memberikan pesan error yang lebih spesifik tentang apa yang salah dengan memakai `panic!` atau `expect`.

Sekarang kita punya kode untuk mengubah kode Rust yang diberi anotasi dari `TokenStream` menjadi instance `DeriveInput`. Mari kita hasilkan kode yang mengimplementasikan trait `HelloMacro` pada tipe yang diberi anotasi itu, seperti ditunjukkan di Listing 20-42.

<Listing number="20-42" file-name="hello_macro_derive/src/lib.rs" caption="Mengimplementasikan trait `HelloMacro` memakai kode Rust yang telah diurai">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-42/hello_macro/hello_macro_derive/src/lib.rs:here}}
```

</Listing>

Kita mendapatkan instance struct `Ident` yang berisi nama (identifier) dari tipe yang diberi anotasi lewat `ast.ident`. Struct di Listing 20-41 menunjukkan bahwa saat kita menjalankan fungsi `impl_hello_macro` pada kode di Listing 20-37, `ident` yang kita dapatkan akan memiliki field `ident` dengan nilai `"Pancakes"`. Jadi, variabel `name` di Listing 20-42 akan berisi instance struct `Ident` yang, saat dicetak, berupa string `"Pancakes"`, yaitu nama struct di Listing 20-37.

Macro `quote!` memungkinkan kita menentukan kode Rust yang ingin kita kembalikan. Compiler mengharapkan sesuatu yang berbeda dari hasil langsung eksekusi macro `quote!`, jadi kita perlu mengubahnya menjadi `TokenStream`. Kita melakukan itu dengan memanggil metode `into`, yang mengonsumsi representasi antara ini dan mengembalikan nilai bertipe `TokenStream` yang dibutuhkan.

Macro `quote!` juga menyediakan mekanisme templating yang sangat keren: Kita bisa menulis `#name`, dan `quote!` akan menggantinya dengan nilai di variabel `name`. Kamu bahkan bisa melakukan pengulangan yang mirip dengan cara kerja macro biasa. Lihat [dokumentasi crate `quote`][quote-docs] untuk pengantar yang lengkap.

Kita ingin macro prosedural kita menghasilkan implementasi trait `HelloMacro` untuk tipe yang diberi anotasi pengguna, yang bisa kita dapatkan dengan memakai `#name`. Implementasi trait itu memiliki satu fungsi, `hello_macro`, yang isinya berisi fungsionalitas yang ingin kita sediakan: mencetak `Hello, Macro! My name is` lalu nama tipe yang diberi anotasi.

Macro `stringify!` yang dipakai di sini adalah bawaan Rust. Macro ini menerima ekspresi Rust, seperti `1 + 2`, dan saat compile time mengubah ekspresi itu menjadi literal string, seperti `"1 + 2"`. Ini berbeda dari `format!` atau `println!`, yang merupakan macro yang mengevaluasi ekspresi lalu mengubah hasilnya menjadi `String`. Ada kemungkinan masukan `#name` berupa ekspresi yang ingin dicetak apa adanya, jadi kita memakai `stringify!`. Memakai `stringify!` juga menghemat alokasi karena mengubah `#name` menjadi literal string saat compile time.

Pada titik ini, `cargo build` seharusnya berhasil di kedua `hello_macro` dan `hello_macro_derive`. Mari kita hubungkan crate-crate ini ke kode di Listing 20-37 untuk melihat macro prosedural beraksi! Buat proyek biner baru di direktori _projects_ kamu dengan `cargo new pancakes`. Kita perlu menambahkan `hello_macro` dan `hello_macro_derive` sebagai dependensi di _Cargo.toml_ milik crate `pancakes`. Jika kamu menerbitkan versi `hello_macro` dan `hello_macro_derive` milikmu ke [crates.io](https://crates.io/)<!-- ignore -->, keduanya akan menjadi dependensi biasa; jika tidak, kamu bisa menentukannya sebagai dependensi `path` seperti berikut:

```toml
{{#include ../listings/ch20-advanced-features/no-listing-21-pancakes/pancakes/Cargo.toml:6:8}}
```

Letakkan kode di Listing 20-37 ke _src/main.rs_, lalu jalankan `cargo run`: Seharusnya tercetak `Hello, Macro! My name is Pancakes!`. Implementasi trait `HelloMacro` dari macro prosedural ikut disertakan tanpa crate `pancakes` perlu mengimplementasikannya; `#[derive(HelloMacro)]` yang menambahkan implementasi trait itu.

Selanjutnya, mari kita lihat bagaimana jenis-jenis macro prosedural lainnya berbeda dari macro `derive` kustom.

### Macro Seperti Atribut

Macro seperti atribut mirip dengan macro `derive` kustom, tetapi alih-alih menghasilkan kode untuk atribut `derive`, macro ini memungkinkan kamu membuat atribut baru. Macro ini juga lebih fleksibel: `derive` hanya bekerja untuk struct dan enum; atribut bisa diterapkan pada item lain juga, seperti fungsi. Berikut contoh pemakaian macro seperti atribut. Misalkan kamu punya atribut bernama `route` yang memberi anotasi pada fungsi saat memakai framework aplikasi web:

```rust,ignore
#[route(GET, "/")]
fn index() {
```

Atribut `#[route]` ini akan didefinisikan oleh framework sebagai macro prosedural. Tanda tangan fungsi definisi macro itu akan terlihat seperti ini:

```rust,ignore
#[proc_macro_attribute]
pub fn route(attr: TokenStream, item: TokenStream) -> TokenStream {
```

Di sini kita punya dua parameter bertipe `TokenStream`. Yang pertama untuk isi atribut: bagian `GET, "/"` tadi. Yang kedua adalah isi item yang melekat padanya: dalam hal ini, `fn index() {}` dan sisa isi fungsi.

Selain itu, macro seperti atribut bekerja seperti macro `derive` kustom: Kamu membuat crate dengan tipe crate `proc-macro` dan mengimplementasikan fungsi yang menghasilkan kode yang kamu inginkan!

### Macro Seperti Fungsi

Macro seperti fungsi mendefinisikan macro yang tampak seperti pemanggilan fungsi. Sama seperti macro `macro_rules!`, macro ini lebih fleksibel daripada fungsi; misalnya, mereka bisa menerima jumlah argumen yang tidak diketahui. Namun, macro `macro_rules!` hanya bisa didefinisikan dengan sintaks mirip match yang kita bahas di bagian ["Macro Deklaratif untuk Metaprogramming Umum"][decl]<!-- ignore --> sebelumnya. Macro seperti fungsi menerima parameter `TokenStream`, dan definisinya memanipulasi `TokenStream` itu dengan kode Rust seperti dua jenis macro prosedural lainnya. Contoh macro seperti fungsi adalah macro `sql!` yang bisa dipanggil seperti ini:

```rust,ignore
let sql = sql!(SELECT * FROM posts WHERE id=1);
```

Macro ini akan mengurai pernyataan SQL di dalamnya dan memeriksa bahwa sintaksnya benar, yang jauh lebih kompleks daripada yang bisa dilakukan macro `macro_rules!`. Macro `sql!` akan didefinisikan seperti ini:

```rust,ignore
#[proc_macro]
pub fn sql(input: TokenStream) -> TokenStream {
```

Definisi ini mirip dengan tanda tangan macro `derive` kustom: Kita menerima token yang berada di dalam tanda kurung dan mengembalikan kode yang ingin kita hasilkan.

## Ringkasan

Wah! Sekarang kamu punya beberapa fitur Rust di kotak peralatanmu yang mungkin tidak akan sering kamu pakai, tapi kamu tahu fitur itu tersedia dalam situasi yang sangat khusus. Kita sudah memperkenalkan beberapa topik kompleks agar saat kamu menemukannya dalam saran pesan error atau dalam kode orang lain, kamu bisa mengenali konsep dan sintaks ini. Pakai bab ini sebagai referensi untuk membimbingmu menuju solusi.

Selanjutnya, kita akan mempraktikkan semua yang sudah kita bahas di seluruh buku dan mengerjakan satu proyek lagi!

[ref]: ../reference/macros-by-example.html
[tlborm]: https://veykril.github.io/tlborm/
[syn]: https://crates.io/crates/syn
[quote]: https://crates.io/crates/quote
[syn-docs]: https://docs.rs/syn/2.0/syn/struct.DeriveInput.html
[quote-docs]: https://docs.rs/quote
[decl]: #declarative-macros-with-macro_rules-for-general-metaprogramming
