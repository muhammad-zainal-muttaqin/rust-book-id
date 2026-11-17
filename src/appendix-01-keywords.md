## Lampiran A: Kata Kunci

Daftar berikut memuat kata kunci yang dicadangkan oleh bahasa Rust untuk
penggunaan sekarang atau masa depan. Karena itu, kata kunci tersebut tidak
bisa dipakai sebagai identifier (kecuali sebagai raw identifier, seperti yang
kita bahas di bagian [“Raw Identifiers”][raw-identifiers]<!-- ignore -->).
_Identifier_ adalah nama untuk fungsi, variabel, parameter, field struct,
module, crate, konstanta, macro, nilai statis, atribut, tipe, trait, atau
lifetime.

[raw-identifiers]: #raw-identifiers

### Kata Kunci yang Sedang Digunakan

Berikut adalah daftar kata kunci yang sedang digunakan, beserta penjelasan
fungsinya.

- **`as`**: Melakukan casting primitif, memecah ambiguitas trait yang memuat
  sebuah item, atau mengganti nama item dalam statement `use`.
- **`async`**: Mengembalikan `Future` alih-alih memblokir thread saat ini.
- **`await`**: Menahan eksekusi sampai hasil dari sebuah `Future` siap.
- **`break`**: Langsung keluar dari loop.
- **`const`**: Mendefinisikan item konstanta atau raw pointer konstanta.
- **`continue`**: Lanjut ke iterasi loop berikutnya.
- **`crate`**: Dalam sebuah path module, merujuk ke akar crate.
- **`dyn`**: Dispatch dinamis ke sebuah trait object.
- **`else`**: Cadangan untuk konstruk alur kontrol `if` dan `if let`.
- **`enum`**: Mendefinisikan sebuah enumerasi.
- **`extern`**: Menautkan sebuah fungsi atau variabel eksternal.
- **`false`**: Literal boolean false.
- **`fn`**: Mendefinisikan sebuah fungsi atau tipe pointer fungsi.
- **`for`**: Melakukan loop atas item dari sebuah iterator, mengimplementasikan
  sebuah trait, atau menentukan lifetime higher-ranked.
- **`if`**: Membuat cabang berdasarkan hasil sebuah ekspresi kondisional.
- **`impl`**: Mengimplementasikan fungsionalitas inherent atau trait.
- **`in`**: Bagian dari sintaks loop `for`.
- **`let`**: Mengikat sebuah variabel.
- **`loop`**: Melakukan loop tanpa syarat.
- **`match`**: Mencocokkan sebuah nilai dengan pola.
- **`mod`**: Mendefinisikan sebuah module.
- **`move`**: Membuat sebuah closure mengambil ownership atas semua yang
  ditangkapnya.
- **`mut`**: Menandai sifat mutable pada reference, raw pointer, atau binding
  pola.
- **`pub`**: Menandai visibilitas publik pada field struct, blok `impl`, atau
  module.
- **`ref`**: Mengikat dengan reference.
- **`return`**: Keluar dari fungsi.
- **`Self`**: Alias tipe untuk tipe yang sedang kita definisikan atau
  implementasikan.
- **`self`**: Subjek method atau module saat ini.
- **`static`**: Variabel global atau lifetime yang berlangsung selama seluruh
  eksekusi program.
- **`struct`**: Mendefinisikan sebuah struct.
- **`super`**: Module induk dari module saat ini.
- **`trait`**: Mendefinisikan sebuah trait.
- **`true`**: Literal boolean true.
- **`type`**: Mendefinisikan alias tipe atau tipe asosiatif.
- **`union`**: Mendefinisikan sebuah [union][union]<!-- ignore -->; hanya
  menjadi kata kunci saat dipakai dalam deklarasi union.
- **`unsafe`**: Menandai kode, fungsi, trait, atau implementasi yang unsafe.
- **`use`**: Membawa simbol ke dalam scope.
- **`where`**: Menandai klausa yang membatasi sebuah tipe.
- **`while`**: Melakukan loop secara kondisional berdasarkan hasil sebuah
  ekspresi.

[union]: ../reference/items/unions.html

### Kata Kunci yang Dicadangkan untuk Masa Depan

Kata kunci berikut belum memiliki fungsi apa pun, tetapi dicadangkan oleh Rust
untuk kemungkinan penggunaan di masa depan:

- `abstract`
- `become`
- `box`
- `do`
- `final`
- `gen`
- `macro`
- `override`
- `priv`
- `try`
- `typeof`
- `unsized`
- `virtual`
- `yield`

### Raw Identifiers

_Raw identifier_ adalah sintaks yang memungkinkan kamu memakai kata kunci di
tempat yang biasanya tidak diizinkan. Kamu memakai raw identifier dengan
memberi prefiks `r#` pada sebuah kata kunci.

Sebagai contoh, `match` adalah sebuah kata kunci. Jika kamu mencoba
mengompilasi fungsi berikut yang memakai `match` sebagai namanya:

<span class="filename">Nama file: src/main.rs</span>

```rust,ignore,does_not_compile
fn match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}
```

kamu akan mendapatkan error berikut:

```text
error: expected identifier, found keyword `match`
 --> src/main.rs:4:4
  |
4 | fn match(needle: &str, haystack: &str) -> bool {
  |    ^^^^^ expected identifier, found keyword
```

Error itu menunjukkan bahwa kamu tidak bisa memakai kata kunci `match` sebagai
identifier fungsi. Untuk memakai `match` sebagai nama fungsi, kamu perlu
memakai sintaks raw identifier, seperti ini:

<span class="filename">Nama file: src/main.rs</span>

```rust
fn r#match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}

fn main() {
    assert!(r#match("foo", "foobar"));
}
```

Kode ini akan terkompilasi tanpa error apa pun. Perhatikan prefiks `r#` pada
nama fungsi di definisinya, maupun di tempat fungsi itu dipanggil dalam
`main`.

Raw identifier memungkinkan kamu memakai kata apa pun sebagai identifier,
bahkan jika kata itu kebetulan merupakan kata kunci yang dicadangkan. Dengan
begitu, kita punya kebebasan lebih besar untuk memilih nama identifier,
sekaligus bisa berintegrasi dengan program yang ditulis dalam bahasa di mana
kata-kata itu bukan kata kunci. Selain itu, raw identifier memungkinkan kamu
memakai library yang ditulis dengan edition Rust berbeda dari yang dipakai
crate kamu. Sebagai contoh, `try` bukan kata kunci di edition 2015, tetapi
menjadi kata kunci di edition 2018, 2021, dan 2024. Jika kamu memakai sebuah
library yang ditulis dengan edition 2015 dan punya fungsi `try`, kamu perlu
memakai sintaks raw identifier (dalam kasus ini, `r#try`) untuk memanggil
fungsi itu dari kode kamu di edition yang lebih baru. Lihat
[Lampiran E][appendix-e]<!-- ignore --> untuk informasi lebih lanjut tentang
edition.

[appendix-e]: appendix-05-editions.html
