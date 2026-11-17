# Pattern dan Pencocokan

Pattern adalah sintaks khusus di Rust untuk mencocokkan struktur tipe, baik yang
kompleks maupun sederhana. Memakai pattern bersama ekspresi `match` dan
konstruksi lainnya memberi kamu lebih banyak kendali atas alur kontrol program.
Sebuah pattern terdiri dari beberapa kombinasi berikut:

- Literal
- Array, enum, struct, atau tuple yang didestrukturisasi
- Variabel
- Wildcard
- Placeholder

Beberapa contoh pattern antara lain `x`, `(a, 3)`, dan `Some(Color::Red)`. Dalam
konteks di mana pattern valid, komponen-komponen ini menggambarkan bentuk data.
Program kita lalu mencocokkan nilai dengan pattern untuk menentukan apakah
datanya berbentuk tepat sehingga bisa menjalankan bagian kode tertentu.

Untuk memakai sebuah pattern, kita membandingkannya dengan suatu nilai. Jika
pattern cocok dengan nilai itu, kita memakai bagian-bagian nilai tersebut dalam
kode. Ingat ekspresi `match` di Bab 6 yang memakai pattern, seperti contoh mesin
pemilah koin. Jika nilai sesuai dengan bentuk pattern, kita bisa memakai
bagian-bagian yang diberi nama. Jika tidak, kode yang terkait dengan pattern itu
tidak akan dijalankan.

Bab ini adalah referensi untuk semua hal yang berkaitan dengan pattern. Kita
akan membahas tempat-tempat di mana pattern bisa dipakai, perbedaan antara
pattern yang dapat dibantah dan yang tidak dapat dibantah, serta berbagai macam
sintaks pattern yang mungkin kamu temui. Di akhir bab, kamu akan tahu cara
memakai pattern untuk mengungkapkan banyak konsep dengan jelas.
