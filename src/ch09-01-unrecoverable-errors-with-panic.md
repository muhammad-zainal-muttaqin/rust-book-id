## Error yang Tidak Dapat Dipulihkan dengan `panic!`

Kadang hal buruk terjadi dalam kode kamu, dan kamu tidak bisa berbuat apa-apa. Dalam situasi seperti ini, Rust menyediakan macro `panic!`. Ada dua cara untuk memicu panic dalam praktiknya: melakukan tindakan yang membuat kode kita panic (misalnya mengakses array melewati ujungnya) atau memanggil macro `panic!` secara eksplisit. Dalam kedua kasus, kita menyebabkan panic pada program kita. Secara default, panic seperti ini akan mencetak pesan gagal, melakukan unwind, membersihkan stack, lalu keluar. Lewat sebuah environment variable, kamu juga bisa meminta Rust menampilkan call stack saat panic terjadi agar lebih mudah melacak sumber panic-nya.

> ### Unwinding Stack atau Aborting saat Panic
>
> Secara default, saat panic terjadi, program mulai melakukan _unwinding_, yang berarti Rust menelusuri stack ke atas dan membersihkan data dari setiap fungsi yang ditemuinya. Namun, menelusuri dan membersihkan itu banyak kerjaan. Karena itu Rust memberi kamu pilihan alternatif berupa _aborting_ langsung, yang mengakhiri program tanpa pembersihan.
>
> Memori yang dipakai program lalu perlu dibersihkan oleh sistem operasi. Jika di proyek kamu perlu membuat binary hasil kompilasi sekecil mungkin, kamu bisa beralih dari unwinding ke aborting saat panic dengan menambahkan `panic = 'abort'` pada bagian `[profile]` yang sesuai di file _Cargo.toml_ kamu. Misalnya, jika kamu ingin abort saat panic dalam mode release, tambahkan ini:
>
> ```toml
> [profile.release]
> panic = 'abort'
> ```

Mari kita coba memanggil `panic!` dalam program sederhana:

<Listing file-name="src/main.rs">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-01-panic/src/main.rs}}
```

</Listing>

Saat kamu menjalankan program, kamu akan melihat seperti ini:

```console
{{#include ../listings/ch09-error-handling/no-listing-01-panic/output.txt}}
```

Panggilan ke `panic!` menghasilkan pesan error pada dua baris terakhir. Baris pertama menampilkan pesan panic kita dan lokasi di kode sumber tempat panic terjadi: _src/main.rs:2:5_ berarti baris kedua, karakter kelima dari file _src/main.rs_ kita.

Dalam kasus ini, baris yang ditunjuk adalah bagian dari kode kita, dan jika kita melihat ke baris itu, kita menemukan panggilan macro `panic!`. Dalam kasus lain, panggilan `panic!` mungkin ada di kode yang dipanggil kode kita, sehingga nama file dan nomor baris yang dilaporkan pesan error adalah milik kode orang lain tempat macro `panic!` dipanggil, bukan baris kode kita yang pada akhirnya menyebabkan panggilan `panic!` itu.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-a-panic-backtrace"></a>

Kita bisa memakai backtrace dari fungsi-fungsi yang menjadi asal panggilan `panic!` untuk mencari tahu bagian kode kita yang menyebabkan masalah. Agar paham cara memakai backtrace `panic!`, mari kita lihat contoh lain dan lihat seperti apa saat panggilan `panic!` datang dari library karena bug di kode kita, bukan dari kode kita yang memanggil macro secara langsung. Listing 9-1 berisi kode yang mencoba mengakses indeks vector di luar rentang indeks yang valid.

<Listing number="9-1" file-name="src/main.rs" caption="Mencoba mengakses elemen melewati ujung vector, yang akan menyebabkan panggilan ke `panic!`">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-01/src/main.rs}}
```

</Listing>

Di sini, kita mencoba mengakses elemen ke-100 dari vector kita (yang berada di indeks 99 karena indeks mulai dari nol), padahal vector itu hanya punya tiga elemen. Dalam situasi ini, Rust akan panic. Memakai `[]` seharusnya mengembalikan sebuah elemen, tetapi jika kamu memberikan indeks yang tidak valid, tidak ada elemen yang bisa dikembalikan Rust dengan benar di sini.

Di C, mencoba membaca melewati ujung suatu struktur data adalah perilaku yang tidak terdefinisi. Kamu bisa saja mendapat apa pun yang ada di lokasi memori yang seharusnya sesuai dengan elemen itu dalam struktur data, meski memori itu bukan milik struktur tersebut. Ini disebut _buffer overread_ dan bisa menimbulkan kerentanan keamanan jika penyerang bisa memanipulasi indeks sedemikian rupa sehingga bisa membaca data yang seharusnya tidak boleh dibacanya, yang tersimpan setelah struktur data itu.

Untuk melindungi program kamu dari kerentanan seperti ini, jika kamu mencoba membaca elemen pada indeks yang tidak ada, Rust akan menghentikan eksekusi dan menolak melanjutnya. Mari kita coba dan lihat:

```console
{{#include ../listings/ch09-error-handling/listing-09-01/output.txt}}
```

Error ini menunjuk baris 4 dari _main.rs_ kita tempat kita mencoba mengakses indeks 99 dari vector di `v`.

Baris `note:` memberi tahu kita bahwa kita bisa menyetel environment variable `RUST_BACKTRACE` untuk mendapatkan backtrace tentang apa persisnya yang menyebabkan error. _Backtrace_ adalah daftar semua fungsi yang telah dipanggil untuk sampai ke titik ini. Backtrace di Rust bekerja seperti di bahasa lain: kunci membacanya adalah mulai dari atas dan baca sampai kamu melihat file yang kamu tulis sendiri. Di situlah masalah berawal. Baris-baris di atas titik itu adalah kode yang dipanggil kode kamu; baris-baris di bawahnya adalah kode yang memanggil kode kamu. Baris-baris sebelum dan sesudah ini bisa berisi kode inti Rust, kode standard library, atau crate yang kamu pakai. Mari kita coba mendapatkan backtrace dengan menyetel environment variable `RUST_BACKTRACE` ke nilai apa pun selain `0`. Listing 9-2 menampilkan output yang mirip dengan yang akan kamu lihat.

<!-- manual-regeneration
cd listings/ch09-error-handling/listing-09-01
RUST_BACKTRACE=1 cargo run
copy the backtrace output below
check the backtrace number mentioned in the text below the listing
-->

<Listing number="9-2" caption="Backtrace yang dihasilkan oleh panggilan ke `panic!`, ditampilkan saat environment variable `RUST_BACKTRACE` disetel">

```console
$ RUST_BACKTRACE=1 cargo run
thread 'main' panicked at src/main.rs:4:6:
index out of bounds: the len is 3 but the index is 99
stack backtrace:
   0: rust_begin_unwind
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/std/src/panicking.rs:692:5
   1: core::panicking::panic_fmt
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/core/src/panicking.rs:75:14
   2: core::panicking::panic_bounds_check
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/core/src/panicking.rs:273:5
   3: <usize as core::slice::index::SliceIndex<[T]>>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/slice/index.rs:274:10
   4: core::slice::index::<impl core::ops::index::Index<I> for [T]>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/slice/index.rs:16:9
   5: <alloc::vec::Vec<T,A> as core::ops::index::Index<I>>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/alloc/src/vec/mod.rs:3361:9
   6: panic::main
             at ./src/main.rs:4:6
   7: core::ops::function::FnOnce::call_once
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/ops/function.rs:250:5
note: Some details are omitted, run with `RUST_BACKTRACE=full` for a verbose backtrace.
```

</Listing>

Itu output yang sangat banyak! Output persis yang kamu lihat bisa berbeda tergantung sistem operasi dan versi Rust kamu. Agar backtrace memuat informasi ini, debug symbol harus aktif. Debug symbol aktif secara default saat memakai `cargo build` atau `cargo run` tanpa flag `--release`, seperti yang kita lakukan di sini.

Pada output di Listing 9-2, baris 6 backtrace menunjuk ke baris di proyek kita yang menyebabkan masalah: baris 4 dari _src/main.rs_. Jika kita tidak ingin program kita panic, kita sebaiknya memulai penyelidikan dari lokasi yang ditunjuk baris pertama yang menyebut file yang kita tulis. Di Listing 9-1, tempat kita sengaja menulis kode yang akan panic, cara memperbaikinya adalah dengan tidak meminta elemen di luar rentang indeks vector. Saat kode kamu panic suatu hari nanti, kamu perlu mencari tahu tindakan apa yang dilakukan kode dengan nilai apa sehingga menyebabkan panic, dan apa yang seharusnya dilakukan kode sebagai gantinya.

Kita akan kembali ke `panic!` dan kapan kita sebaiknya memakai atau tidak memakai `panic!` untuk menangani kondisi error di bagian [“`panic!` atau Bukan `panic!`”][to-panic-or-not-to-panic]<!-- ignore --> nanti di bab ini. Berikutnya, kita akan melihat cara pulih dari error memakai `Result`.

[to-panic-or-not-to-panic]: ch09-03-to-panic-or-not-to-panic.html#to-panic-or-not-to-panic
