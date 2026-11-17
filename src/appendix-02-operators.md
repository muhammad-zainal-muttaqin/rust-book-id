## Lampiran B: Operator dan Simbol

Lampiran ini berisi glosarium sintaks Rust, mencakup operator serta simbol lain
yang muncul sendirian atau dalam konteks path, generic, trait bound, macro,
atribut, komentar, tuple, dan kurung.

### Operator

Tabel B-1 memuat operator di Rust, contoh tampilan operator tersebut dalam
konteksnya, penjelasan singkat, serta apakah operator itu bisa dioverload. Jika
sebuah operator bisa dioverload, trait yang relevan untuk melakukannya ikut
dicantumkan.

<span class="caption">Tabel B-1: Operator</span>

| Operator                  | Contoh                                                  | Penjelasan                                                             | Bisa Dioverload? |
| ------------------------- | ------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------- |
| `!`                       | `ident!(...)`, `ident!{...}`, `ident![...]`             | Ekspansi macro                                                          |                  |
| `!`                       | `!expr`                                                 | Komplemen bitwise atau logika                                           | `Not`            |
| `!=`                      | `expr != expr`                                          | Perbandingan ketidak-samaan                                            | `PartialEq`      |
| `%`                       | `expr % expr`                                           | Sisa bagi aritmetika                                                    | `Rem`            |
| `%=`                      | `var %= expr`                                           | Sisa bagi aritmetika dan penugasan                                      | `RemAssign`      |
| `&`                       | `&expr`, `&mut expr`                                    | Borrowing                                                               |                  |
| `&`                       | `&type`, `&mut type`, `&'a type`, `&'a mut type`        | Tipe pointer borrowed                                                   |                  |
| `&`                       | `expr & expr`                                           | AND bitwise                                                             | `BitAnd`         |
| `&=`                      | `var &= expr`                                           | AND bitwise dan penugasan                                               | `BitAndAssign`   |
| `&&`                      | `expr && expr`                                          | AND logika short-circuit                                                |                  |
| `*`                       | `expr * expr`                                           | Perkalian aritmetika                                                    | `Mul`            |
| `*=`                      | `var *= expr`                                           | Perkalian aritmetika dan penugasan                                      | `MulAssign`      |
| `*`                       | `*expr`                                                 | Dereference                                                             | `Deref`          |
| `*`                       | `*const type`, `*mut type`                              | Pointer mentah                                                          |                  |
| `+`                       | `trait + trait`, `'a + trait`                           | Batasan tipe gabungan                                                   |                  |
| `+`                       | `expr + expr`                                           | Penjumlahan aritmetika                                                  | `Add`            |
| `+=`                      | `var += expr`                                           | Penjumlahan aritmetika dan penugasan                                    | `AddAssign`      |
| `,`                       | `expr, expr`                                            | Pemisah argumen dan elemen                                              |                  |
| `-`                       | `- expr`                                                | Negasi aritmetika                                                       | `Neg`            |
| `-`                       | `expr - expr`                                           | Pengurangan aritmetika                                                  | `Sub`            |
| `-=`                      | `var -= expr`                                           | Pengurangan aritmetika dan penugasan                                    | `SubAssign`      |
| `->`                      | `fn(...) -> type`, <code>&vert;...&vert; -> type</code> | Tipe pengembalian fungsi dan closure                                    |                  |
| `.`                       | `expr.ident`                                            | Akses field                                                             |                  |
| `.`                       | `expr.ident(expr, ...)`                                 | Pemanggilan method                                                      |                  |
| `.`                       | `expr.0`, `expr.1`, dan seterusnya                       | Pengindeksan tuple                                                      |                  |
| `..`                      | `..`, `expr..`, `..expr`, `expr..expr`                  | Literal range eksklusif di kanan                                        | `PartialOrd`     |
| `..=`                     | `..=expr`, `expr..=expr`                                | Literal range inklusif di kanan                                         | `PartialOrd`     |
| `..`                      | `..expr`                                                | Sintaks pembaruan literal struct                                        |                  |
| `..`                      | `variant(x, ..)`, `struct_type { x, .. }`               | Binding pola "dan sisanya"                                              |                  |
| `...`                     | `expr...expr`                                           | (Usang, gunakan `..=`.) Dalam pola: pola range inklusif                 |                  |
| `/`                       | `expr / expr`                                           | Pembagian aritmetika                                                    | `Div`            |
| `/=`                      | `var /= expr`                                           | Pembagian aritmetika dan penugasan                                      | `DivAssign`      |
| `:`                       | `pat: type`, `ident: type`                              | Batasan                                                                 |                  |
| `:`                       | `ident: expr`                                           | Inisialisasi field struct                                               |                  |
| `:`                       | `'a: loop {...}`                                        | Label loop                                                              |                  |
| `;`                       | `expr;`                                                 | Penutup statement dan item                                              |                  |
| `;`                       | `[...; len]`                                            | Bagian dari sintaks array berukuran tetap                               |                  |
| `<<`                      | `expr << expr`                                          | Geser ke kiri                                                           | `Shl`            |
| `<<=`                     | `var <<= expr`                                          | Geser ke kiri dan penugasan                                             | `ShlAssign`      |
| `<`                       | `expr < expr`                                           | Perbandingan kurang dari                                                | `PartialOrd`     |
| `<=`                      | `expr <= expr`                                          | Perbandingan kurang dari atau sama dengan                              | `PartialOrd`     |
| `=`                       | `var = expr`, `ident = type`                            | Penugasan/kesetaraan                                                    |                  |
| `==`                      | `expr == expr`                                          | Perbandingan kesetaraan                                                 | `PartialEq`      |
| `=>`                      | `pat => expr`                                           | Bagian dari sintaks match arm                                           |                  |
| `>`                       | `expr > expr`                                           | Perbandingan lebih besar dari                                           | `PartialOrd`     |
| `>=`                      | `expr >= expr`                                          | Perbandingan lebih besar dari atau sama dengan                         | `PartialOrd`     |
| `>>`                      | `expr >> expr`                                          | Geser ke kanan                                                          | `Shr`            |
| `>>=`                     | `var >>= expr`                                          | Geser ke kanan dan penugasan                                            | `ShrAssign`      |
| `@`                       | `ident @ pat`                                           | Binding pola                                                            |                  |
| `^`                       | `expr ^ expr`                                           | XOR bitwise                                                             | `BitXor`         |
| `^=`                      | `var ^= expr`                                           | XOR bitwise dan penugasan                                               | `BitXorAssign`   |
| <code>&vert;</code>       | <code>pat &vert; pat</code>                             | Alternatif pola                                                         |                  |
| <code>&vert;</code>       | <code>expr &vert; expr</code>                           | OR bitwise                                                              | `BitOr`          |
| <code>&vert;=</code>      | <code>var &vert;= expr</code>                           | OR bitwise dan penugasan                                                | `BitOrAssign`    |
| <code>&vert;&vert;</code> | <code>expr &vert;&vert; expr</code>                     | OR logika short-circuit                                                 |                  |
| `?`                       | `expr?`                                                 | Propagasi error                                                         |                  |

### Simbol Non-operator

Tabel berikut memuat semua simbol yang tidak berfungsi sebagai operator; yaitu,
simbol tersebut tidak berperilaku seperti pemanggilan fungsi atau method.

Tabel B-2 menampilkan simbol yang muncul sendirian dan valid di berbagai
tempat.

<span class="caption">Tabel B-2: Sintaks Berdiri Sendiri</span>

| Simbol                                                                  | Penjelasan                                                              |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `'ident`                                                                | Lifetime bernama atau label loop                                         |
| Angka yang langsung diikuti `u8`, `i32`, `f64`, `usize`, dan seterusnya  | Literal numerik bertipe tertentu                                         |
| `"..."`                                                                 | Literal string                                                          |
| `r"..."`, `r#"..."#`, `r##"..."##`, dan seterusnya                       | Literal string raw; karakter escape tidak diproses                      |
| `b"..."`                                                                | Literal string byte; membangun array byte, bukan string                 |
| `br"..."`, `br#"..."#`, `br##"..."##`, dan seterusnya                    | Literal string byte raw; gabungan literal string raw dan byte           |
| `'...'`                                                                 | Literal karakter                                                        |
| `b'...'`                                                                | Literal byte ASCII                                                      |
| <code>&vert;...&vert; expr</code>                                       | Closure                                                                 |
| `!`                                                                     | Tipe bawah yang selalu kosong untuk fungsi yang diverging               |
| `_`                                                                     | Binding pola yang "diabaikan"; juga dipakai agar literal integer mudah dibaca |

Tabel B-3 menampilkan simbol yang muncul dalam konteks path melalui hierarki
module menuju sebuah item.

<span class="caption">Tabel B-3: Sintaks yang Berkaitan dengan Path</span>

| Simbol                                  | Penjelasan                                                                                                 |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `ident::ident`                          | Path namespace                                                                                             |
| `::path`                                | Path relatif terhadap root crate (yaitu path absolut yang eksplisit)                                       |
| `self::path`                            | Path relatif terhadap module saat ini (yaitu path relatif yang eksplisit)                                  |
| `super::path`                           | Path relatif terhadap induk dari module saat ini                                                           |
| `type::ident`, `<type as trait>::ident` | Konstanta, fungsi, dan tipe yang terkait                                                                    |
| `<type>::...`                           | Item terkait untuk tipe yang tidak bisa dinamai langsung (misalnya `<&T>::...`, `<[T]>::...`, dan seterusnya) |
| `trait::method(...)`                    | Menghilangkan ambiguitas pemanggilan method dengan menyebut trait yang mendefinisikannya                   |
| `type::method(...)`                     | Menghilangkan ambiguitas pemanggilan method dengan menyebut tipe tempat method itu didefinisikan           |
| `<type as trait>::method(...)`          | Menghilangkan ambiguitas pemanggilan method dengan menyebut trait sekaligus tipe                           |

Tabel B-4 menampilkan simbol yang muncul dalam konteks penggunaan parameter
tipe generic.

<span class="caption">Tabel B-4: Generic</span>

| Simbol                         | Penjelasan                                                                                                                                       |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `path<...>`                    | Menentukan parameter untuk sebuah tipe generic dalam sebuah tipe (misalnya `Vec<u8>`)                                                            |
| `path::<...>`, `method::<...>` | Menentukan parameter generic untuk tipe, fungsi, atau method dalam sebuah ekspresi; sering disebut _turbofish_ (misalnya `"42".parse::<i32>()`)   |
| `fn ident<...> ...`            | Mendefinisikan fungsi generic                                                                                                                    |
| `struct ident<...> ...`        | Mendefinisikan struct generic                                                                                                                    |
| `enum ident<...> ...`          | Mendefinisikan enum generic                                                                                                                      |
| `impl<...> ...`                | Mendefinisikan implementasi generic                                                                                                              |
| `for<...> type`                | Batasan lifetime higher-ranked                                                                                                                   |
| `type<ident=type>`             | Tipe generic tempat satu atau beberapa tipe terkait ditentukan nilainya (misalnya `Iterator<Item=T>`)                                            |

Tabel B-5 menampilkan simbol yang muncul dalam konteks memberi batasan pada
parameter tipe generic lewat trait bound.

<span class="caption">Tabel B-5: Batasan Trait Bound</span>

| Simbol                        | Penjelasan                                                                                                                               |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `T: U`                        | Parameter generic `T` dibatasi pada tipe yang mengimplementasikan `U`                                                                     |
| `T: 'a`                       | Tipe generic `T` harus hidup lebih lama daripada lifetime `'a` (artinya tipe tersebut tidak boleh berisi reference dengan lifetime lebih pendek dari `'a`) |
| `T: 'static`                  | Tipe generic `T` tidak berisi reference borrowed selain `'static`                                                                         |
| `'b: 'a`                      | Lifetime generic `'b` harus hidup lebih lama daripada lifetime `'a`                                                                       |
| `T: ?Sized`                   | Mengizinkan parameter tipe generic berupa tipe berukuran dinamis                                                                          |
| `'a + trait`, `trait + trait` | Batasan tipe gabungan                                                                                                                    |

Tabel B-6 menampilkan simbol yang muncul dalam konteks memanggil atau
mendefinisikan macro serta menentukan atribut pada sebuah item.

<span class="caption">Tabel B-6: Macro dan Atribut</span>

| Simbol                                      | Penjelasan          |
| ------------------------------------------- | ------------------- |
| `#[meta]`                                   | Atribut luar        |
| `#![meta]`                                  | Atribut dalam       |
| `$ident`                                    | Substitusi macro    |
| `$ident:kind`                               | Metavariable macro  |
| `$(...)...`                                 | Pengulangan macro   |
| `ident!(...)`, `ident!{...}`, `ident![...]` | Pemanggilan macro   |

Tabel B-7 menampilkan simbol yang membuat komentar.

<span class="caption">Tabel B-7: Komentar</span>

| Simbol     | Penjelasan                |
| ---------- | ------------------------- |
| `//`       | Komentar baris            |
| `//!`      | Komentar dokumen baris dalam |
| `///`      | Komentar dokumen baris luar  |
| `/*...*/`  | Komentar blok             |
| `/*!...*/` | Komentar dokumen blok dalam  |
| `/**...*/` | Komentar dokumen blok luar   |

Tabel B-8 menampilkan konteks penggunaan tanda kurung.

<span class="caption">Tabel B-8: Kurung Bulat</span>

| Simbol                   | Penjelasan                                                                                |
| ------------------------ | ----------------------------------------------------------------------------------------- |
| `()`                     | Tuple kosong (juga dikenal sebagai unit), berupa literal maupun tipe                       |
| `(expr)`                 | Ekspresi dalam kurung                                                                      |
| `(expr,)`                | Ekspresi tuple satu elemen                                                                 |
| `(type,)`                | Tipe tuple satu elemen                                                                     |
| `(expr, ...)`            | Ekspresi tuple                                                                              |
| `(type, ...)`            | Tipe tuple                                                                                  |
| `expr(expr, ...)`        | Ekspresi pemanggilan fungsi; juga dipakai untuk menginisialisasi tuple `struct` dan varian tuple `enum` |

Tabel B-9 menampilkan konteks penggunaan kurung kurawal.

<span class="caption">Tabel B-9: Kurung Kurawal</span>

| Konteks      | Penjelasan          |
| ------------ | ------------------- |
| `{...}`      | Ekspresi blok       |
| `Type {...}` | Literal struct      |

Tabel B-10 menampilkan konteks penggunaan kurung siku.

<span class="caption">Tabel B-10: Kurung Siku</span>

| Konteks                                             | Penjelasan                                                                                                                  |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `[...]`                                             | Literal array                                                                                                               |
| `[expr; len]`                                       | Literal array berisi `len` salinan `expr`                                                                                   |
| `[type; len]`                                       | Tipe array berisi `len` instans `type`                                                                                      |
| `expr[expr]`                                        | Pengindeksan koleksi; bisa dioverload (`Index`, `IndexMut`)                                                                 |
| `expr[..]`, `expr[a..]`, `expr[..b]`, `expr[a..b]`  | Pengindeksan koleksi yang berpura-pura jadi pen-slice-an koleksi, memakai `Range`, `RangeFrom`, `RangeTo`, atau `RangeFull` sebagai "index" |
