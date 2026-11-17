## Lampiran D: Perkakas Pengembangan yang Berguna

Di lampiran ini, kita membahas beberapa perkakas pengembangan berguna yang
disediakan oleh proyek Rust. Kita akan membahas format otomatis, cara cepat
menerapkan perbaikan atas peringatan, linter, dan integrasi dengan IDE.

### Format Otomatis dengan `rustfmt`

Tool `rustfmt` memformat ulang kode kamu sesuai gaya kode komunitas. Banyak
proyek kolaboratif memakai `rustfmt` untuk menghindari perdebatan soal gaya
penulisan Rust: semua orang memformat kodenya dengan tool yang sama.

Instalasi Rust sudah menyertakan `rustfmt` secara bawaan, jadi program
`rustfmt` dan `cargo-fmt` seharusnya sudah ada di sistem kamu. Dua perintah ini
setara dengan `rustc` dan `cargo`, di mana `rustfmt` memberi kendali yang
lebih granular dan `cargo-fmt` memahami konvensi proyek yang memakai Cargo. Untuk
memformat proyek Cargo mana pun, jalankan berikut:

```console
$ cargo fmt
```

Menjalankan perintah ini memformat ulang semua kode Rust di crate yang sedang
berada. Perintah ini seharusnya hanya mengubah gaya kode, bukan semantik
kodenya. Informasi lebih lanjut tentang `rustfmt` ada di [dokumentasinya][rustfmt].

### Perbaiki Kode dengan `rustfix`

Tool `rustfix` ikut disertakan dalam instalasi Rust dan bisa memperbaiki
peringatan compiler yang punya cara koreksi yang jelas—kemungkinan besar itulah
yang kamu inginkan. Kamu mungkin sudah pernah melihat peringatan compiler.
Sebagai contoh, perhatikan kode ini:

<span class="filename">Nama file: src/main.rs</span>

```rust
fn main() {
    let mut x = 42;
    println!("{x}");
}
```

Di sini kita mendefinisikan variabel `x` sebagai mutable, tetapi kita tidak
pernah benar-benar mengubahnya. Rust memberi kita peringatan tentang hal itu:

```console
$ cargo build
   Compiling myprogram v0.1.0 (file:///projects/myprogram)
warning: variable does not need to be mutable
 --> src/main.rs:2:9
  |
2 |     let mut x = 0;
  |         ----^
  |         |
  |         help: remove this `mut`
  |
  = note: `#[warn(unused_mut)]` on by default
```

Peringatan itu menyarankan kita menghapus keyword `mut`. Kita bisa menerapkan
saran tersebut secara otomatis dengan tool `rustfix` lewat perintah `cargo
fix`:

```console
$ cargo fix
    Checking myprogram v0.1.0 (file:///projects/myprogram)
      Fixing src/main.rs (1 fix)
    Finished dev [unoptimized + debuginfo] target(s) in 0.59s
```

Saat kita melihat _src/main.rs_ lagi, kita akan melihat bahwa `cargo fix` sudah
mengubah kodenya:

<span class="filename">Nama file: src/main.rs</span>

```rust
fn main() {
    let x = 42;
    println!("{x}");
}
```

Variabel `x` kini immutable, dan peringatan itu tidak lagi muncul.

Kamu juga bisa memakai perintah `cargo fix` untuk memindahkan kode kamu antar
edition Rust yang berbeda. Edition dibahas di [Lampiran E][editions]<!--
ignore -->.

### Lint Lainnya dengan Clippy

Tool Clippy adalah kumpulan lint untuk menganalisis kode kamu, sehingga kamu
bisa menangkap kesalahan umum dan memperbaiki kode Rust kamu. Clippy ikut
disertakan dalam instalasi Rust standar.

Untuk menjalankan lint Clippy pada proyek Cargo mana pun, jalankan berikut:

```console
$ cargo clippy
```

Sebagai contoh, misalkan kamu menulis program yang memakai perkiraan nilai
konstanta matematika, seperti pi, seperti program ini:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = 3.1415;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

Menjalankan `cargo clippy` pada proyek ini menghasilkan error berikut:

```text
error: approximate value of `f{32, 64}::consts::PI` found
 --> src/main.rs:2:13
  |
2 |     let x = 3.1415;
  |             ^^^^^^
  |
  = note: `#[deny(clippy::approx_constant)]` on by default
  = help: consider using the constant directly
  = help: for further information visit https://rust-lang.github.io/rust-clippy/master/index.html#approx_constant
```

Error ini memberi tahu kamu bahwa Rust sudah mendefinisikan konstanta `PI` yang
lebih presisi, dan program kamu akan lebih benar jika memakai konstanta itu.
Kamu lalu mengubah kode untuk memakai konstanta `PI`.

Kode berikut tidak menghasilkan error atau peringatan apa pun dari Clippy:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = std::f64::consts::PI;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

Informasi lebih lanjut tentang Clippy ada di [dokumentasinya][clippy].

### Integrasi IDE dengan `rust-analyzer`

Untuk membantu integrasi IDE, komunitas Rust menyarankan memakai
[`rust-analyzer`][rust-analyzer]<!-- ignore -->. Tool ini adalah kumpulan
utilitas berpusat pada compiler yang memakai [Language Server Protocol][lsp]<!--
ignore -->, yaitu spesifikasi agar IDE dan bahasa pemrograman bisa saling
berkomunikasi. Berbagai klien bisa memakai `rust-analyzer`, misalnya [plug-in
Rust analyzer untuk Visual Studio Code][vscode].

Kunjungi [halaman utama proyek `rust-analyzer`][rust-analyzer]<!-- ignore -->
untuk instruksi instalasi, lalu pasang dukungan language server di IDE yang kamu
pakai. IDE kamu akan mendapat kemampuan seperti autocompletion, lompat ke
definisi, dan error inline.

[rustfmt]: https://github.com/rust-lang/rustfmt
[editions]: appendix-05-editions.md
[clippy]: https://github.com/rust-lang/rust-clippy
[rust-analyzer]: https://rust-analyzer.github.io
[lsp]: http://langserver.org/
[vscode]: https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer
