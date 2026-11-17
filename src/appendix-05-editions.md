## Lampiran E: Edition

Di Bab 1, kamu sudah melihat bahwa `cargo new` menambahkan sedikit metadata ke file _Cargo.toml_ kamu soal sebuah edition. Lampiran ini membahas maksudnya!

Bahasa Rust dan compiler-nya punya siklus rilis enam minggu, artinya pengguna selalu mendapat aliran fitur baru secara terus-menerus. Bahasa pemrograman lain merilis perubahan besar lebih jarang; Rust merilis pembaruan kecil lebih sering. Seiring waktu, semua perubahan kecil itu terakumulasi. Namun antara rilis ke rilis, sulit untuk menengok ke belakang dan berkata, "Wah, antara Rust 1.10 dan Rust 1.31, Rust sudah berubah banyak!"

Setiap tiga tahun sekali, tim Rust menghasilkan sebuah _edition_ Rust baru. Setiap edition memadukan fitur-fitur yang sudah masuk menjadi satu paket yang jelas, lengkap dengan dokumentasi dan peralatan yang sepenuhnya diperbarui. Edition baru dirilis sebagai bagian dari proses rilis enam minggu yang biasa.

Edition punya tujuan berbeda bagi orang yang berbeda:

- Bagi pengguna Rust aktif, edition baru menggabungkan perubahan inkremental menjadi paket yang mudah dipahami.
- Bagi yang bukan pengguna, edition baru menandakan bahwa sejumlah kemajuan besar sudah masuk, sehingga Rust mungkin layak dilihat lagi.
- Bagi mereka yang mengembangkan Rust, edition baru menyediakan titik pemersatu bagi proyek secara keseluruhan.

Pada saat tulisan ini dibuat, empat edition Rust tersedia: Rust 2015, Rust 2018, Rust 2021, dan Rust 2024. Buku ini ditulis dengan idiom edition Rust 2024.

Kunci `edition` di _Cargo.toml_ menunjukkan edition mana yang harus dipakai compiler untuk kode kamu. Jika kunci itu tidak ada, Rust memakai nilai edition `2015` demi kompatibilitas ke belakang.

Setiap proyek bisa memilih edition selain edition bawaan 2015. Edition bisa memuat perubahan yang tidak kompatibel, misalnya menambahkan keyword baru yang bentrok dengan identifier di kode. Namun, kecuali kamu memilih perubahan tersebut, kode kamu tetap akan terkompilasi meskipun kamu menaikkan versi compiler Rust yang dipakai.

Semua versi compiler Rust mendukung edition apa pun yang sudah ada sebelum rilis compiler tersebut, dan mereka bisa menautkan crate dari edition yang didukung mana pun. Perubahan edition hanya memengaruhi cara compiler mem-parse kode untuk pertama kali. Karena itu, kalau kamu memakai Rust 2015 dan salah satu dependensi kamu memakai Rust 2018, proyek kamu tetap akan terkompilasi dan bisa memakai dependensi itu. Situasi sebaliknya, di mana proyek kamu memakai Rust 2018 dan sebuah dependensi memakai Rust 2015, juga berjalan baik.

Perlu ditegaskan: sebagian besar fitur tersedia di semua edition. Pengembang yang memakai edition Rust apa pun akan terus melihat peningkatan saat rilis stabil baru keluar. Namun, dalam beberapa kasus, terutama saat keyword baru ditambahkan, sebagian fitur baru mungkin hanya tersedia di edition-edition yang lebih baru. Kamu perlu berganti edition kalau ingin memanfaatkan fitur semacam itu.

Untuk detail lebih lanjut, lihat [_The Rust Edition Guide_][edition-guide]. Itu adalah buku lengkap yang memuat daftar perbedaan antar-edition serta menjelaskan cara memperbarui kode kamu ke edition baru secara otomatis lewat `cargo fix`.

[edition-guide]: https://doc.rust-lang.org/stable/edition-guide
