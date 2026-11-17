# Fitur Bahasa Fungsional: Iterator dan Closure

Desain Rust mengambil inspirasi dari banyak bahasa dan teknik yang sudah ada, dan salah satu pengaruh besarnya adalah _functional programming_. Pemrograman dengan gaya fungsional sering memakai fungsi sebagai nilai: meneruskannya sebagai argumen, mengembalikannya dari fungsi lain, menyimpannya dalam variabel untuk dijalankan nanti, dan sebagainya.

Di bab ini, kita tidak akan berdebat soal apa yang termasuk functional programming dan apa yang tidak. Sebaliknya, kita akan membahas beberapa fitur Rust yang mirip dengan fitur di banyak bahasa yang sering disebut fungsional.

Lebih spesifiknya, kita akan membahas:

- _Closure_, konstruksi seperti fungsi yang bisa kamu simpan dalam variabel
- _Iterator_, cara memproses serangkaian elemen
- Cara memakai closure dan iterator untuk memperbaiki proyek I/O di Bab 12
- Performa closure dan iterator (spoiler: keduanya lebih cepat dari yang kamu kira!)

Kita sudah membahas beberapa fitur Rust lain, seperti pencocokan pola dan enum, yang juga dipengaruhi gaya fungsional. Karena menguasai closure dan iterator adalah bagian penting untuk menulis kode Rust yang cepat dan idiomatik, kita akan mendedikasikan seluruh bab ini untuk keduanya.
