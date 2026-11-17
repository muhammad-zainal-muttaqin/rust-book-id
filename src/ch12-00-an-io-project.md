# Proyek I/O: Membangun Program Command Line

Bab ini merangkum banyak keterampilan yang sudah kamu pelajari sejauh ini dan
mengeksplorasi beberapa fitur library standar lainnya. Kita akan membangun sebuah
tool command line yang berinteraksi dengan file serta input/output command line
untuk mempraktikkan beberapa konsep Rust yang sudah kamu kuasai.

Kecepatan, keamanan, keluaran berupa satu binary, dan dukungan lintas platform dari
Rust menjadikannya bahasa yang ideal untuk membuat tool command line. Maka, untuk
proyek kita, kita akan membuat versi sendiri dari tool pencarian command line klasik
`grep` (**g**lobally search a **r**egular **e**xpression and **p**rint). Pada
penggunaan paling sederhana, `grep` mencari string tertentu di dalam file tertentu.
Untuk melakukan itu, `grep` menerima path file dan string sebagai argumennya. Lalu,
ia membaca file tersebut, mencari baris-baris di dalamnya yang memuat argumen string
itu, dan menampilkan baris-baris tersebut.

Sambil berjalan, kita akan menunjukkan cara membuat tool command line kita memakai
fitur terminal yang juga dipakai banyak tool command line lain. Kita akan membaca
nilai sebuah environment variable agar pengguna bisa mengonfigurasi perilaku tool
kita. Kita juga akan menampilkan pesan error ke stream console standard error
(`stderr`) alih-alih ke standard output (`stdout`), sehingga misalnya pengguna bisa
mengalihkan keluaran yang berhasil ke file sambil tetap melihat pesan error di layar.

Salah satu anggota komunitas Rust, Andrew Gallant, sudah membuat versi `grep` yang
lengkap fiturnya dan sangat cepat, bernama `ripgrep`. Jika dibandingkan, versi kita
akan terbilang sederhana, tetapi bab ini akan memberimu sebagian pengetahuan dasar
yang kamu butuhkan untuk memahami proyek dunia nyata seperti `ripgrep`.

Proyek `grep` kita akan menggabungkan sejumlah konsep yang sudah kamu pelajari
sejauh ini:

- Mengatur kode ([Bab 7][ch7]<!-- ignore -->)
- Memakai vector dan string ([Bab 8][ch8]<!-- ignore -->)
- Menangani error ([Bab 9][ch9]<!-- ignore -->)
- Memakai trait dan lifetime di tempat yang tepat ([Bab 10][ch10]<!-- ignore -->)
- Menulis test ([Bab 11][ch11]<!-- ignore -->)

Kita juga akan memperkenalkan secara singkat closure, iterator, dan trait object,
yang akan dibahas lebih rinci di [Bab 13][ch13]<!-- ignore --> dan
[Bab 18][ch18]<!-- ignore -->.

[ch7]: ch07-00-managing-growing-projects-with-packages-crates-and-modules.html
[ch8]: ch08-00-common-collections.html
[ch9]: ch09-00-error-handling.html
[ch10]: ch10-00-generics.html
[ch11]: ch11-00-testing.html
[ch13]: ch13-00-functional-features.html
[ch18]: ch18-00-oop.html
