## Memperluas Cargo dengan Perintah Kustom

Cargo dirancang agar kamu bisa memperluasnya dengan subcommand baru tanpa harus
memodifikasinya. Jika sebuah binary di `$PATH`-mu bernama `cargo-something`, kamu
bisa menjalankannya seolah-olah itu adalah subcommand Cargo dengan menjalankan
`cargo something`. Perintah kustom seperti ini juga tercantum saat kamu
menjalankan `cargo --list`. Karena kamu bisa memakai `cargo install` untuk memasang
ekstensi lalu menjalankannya persis seperti peralatan bawaan Cargo, itulah salah
satu keuntungan desain Cargo yang sangat praktis!

## Ringkasan

Berbagi kode dengan Cargo dan [crates.io](https://crates.io/)<!-- ignore -->
adalah salah satu hal yang membuat ekosistem Rust berguna untuk banyak tugas.
Standard library Rust kecil dan stabil, tetapi crate mudah dibagikan, dipakai,
dan dikembangkan dengan jadwal yang berbeda dari bahasanya. Jangan malu untuk
membagikan kode yang berguna bagimu di [crates.io](https://crates.io/)<!-- ignore
-->; besar kemungkinan kode itu juga berguna bagi orang lain!
