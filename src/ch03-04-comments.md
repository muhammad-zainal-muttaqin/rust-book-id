## Komentar

Setiap programmer berusaha membuat kodenya mudah dipahami, tapi kadang
penjelasan ekstra memang diperlukan. Dalam kasus seperti itu, programmer
meninggalkan _komentar_ di kode surnya—yang akan diabaikan compiler, tetapi
biasanya berguna bagi orang yang membaca kode tersebut.

Berikut komentar sederhana:

```rust
// hello, world
```

Di Rust, gaya komentar yang lazim diawali dengan dua garis miring, dan
komentarnya berakhir di akhir baris. Untuk komentar yang meluas ke lebih dari
satu baris, kamu perlu menulis `//` di setiap baris, seperti ini:

```rust
// So we're doing something complicated here, long enough that we need
// multiple lines of comments to do it! Whew! Hopefully, this comment will
// explain what's going on.
```

Komentar juga bisa diletakkan di akhir baris yang berisi kode:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-24-comments-end-of-line/src/main.rs}}
```

Tapi lebih sering kamu akan menemukannya dalam format ini, dengan komentar
pada baris terpisah di atas kode yang ditandainya:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-25-comments-above-line/src/main.rs}}
```

Rust juga punya jenis komentar lain, yaitu komentar dokumentasi, yang akan
kita bahas di bagian [“Publishing a Crate to Crates.io”][publishing]<!-- ignore -->
pada Bab 14.

[publishing]: ch14-02-publishing-to-crates-io.html
