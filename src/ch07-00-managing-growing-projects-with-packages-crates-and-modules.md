<!-- Old headings. Do not remove or links may break. -->

<a id="managing-growing-projects-with-packages-crates-and-modules"></a>

# Package, Crate, dan Module

Semakin besar program yang kamu tulis, semakin penting pula cara kamu
mengorganisasi kode. Dengan mengelompokkan fungsi yang saling berkaitan dan
memisahkan kode berdasarkan fitur yang berbeda, kamu jadi lebih jelas di mana
menemukan kode yang mengimplementasikan suatu fitur dan ke mana harus menuju
ketika ingin mengubah cara kerja fitur tersebut.

Program yang kita tulis sejauh ini semuanya berada dalam satu module di satu
file. Saat sebuah proyek bertambah besar, kamu sebaiknya mengorganisasi kode
dengan memecahnya menjadi beberapa module, lalu beberapa file. Sebuah package
bisa berisi beberapa binary crate dan secara opsional satu library crate. Saat
package bertambah besar, kamu bisa mengekstrak bagian-bagiannya ke crate
terpisah yang kemudian menjadi dependency eksternal. Bab ini membahas semua
teknik tersebut. Untuk proyek yang sangat besar yang terdiri atas kumpulan
package saling terkait dan berkembang bersama, Cargo menyediakan workspace,
yang akan kita bahas di [“Cargo Workspaces”][workspaces]<!-- ignore --> pada
Bab 14.

Kita juga akan membahas cara mengenkapsulasi detail implementasi, yang
memungkinkan kamu menggunakan ulang kode pada tingkat yang lebih tinggi:
begitu kamu mengimplementasikan suatu operasi, kode lain bisa memanggil kode
kamu melalui interface publiknya tanpa perlu tahu bagaimana implementasinya
bekerja. Cara kamu menulis kode menentukan bagian mana yang publik untuk
digunakan kode lain dan bagian mana yang merupakan detail implementasi privat
yang kamu simpan hak untuk mengubahnya. Ini adalah cara lain untuk membatasi
jumlah detail yang harus kamu simpan di kepala.

Konsep yang berkaitan adalah scope: konteks bersarang tempat sebuah kode
ditulis punya sekumpulan nama yang didefinisikan sebagai "berada di scope".
Saat membaca, menulis, dan mengompilasi kode, programmer dan compiler perlu
tahu apakah nama tertentu di posisi tertentu merujuk ke variabel, fungsi,
struct, enum, module, konstanta, atau item lain, dan apa arti item tersebut.
Kamu bisa membuat scope dan mengubah nama mana yang masuk atau keluar dari
scope. Kamu tidak bisa punya dua item dengan nama yang sama di scope yang
sama; tersedia alat untuk menyelesaikan konflik nama.

Rust punya sejumlah fitur yang memungkinkan kamu mengelola organisasi kode,
termasuk detail mana yang diekspos, detail mana yang bersifat privat, dan nama
apa yang ada di setiap scope dalam programmu. Fitur-fitur ini, yang terkadang
secara kolektif disebut _module system_, meliputi:

* **Package**: fitur Cargo yang memungkinkan kamu membangun, menguji, dan
  berbagi crate
* **Crates**: pohon module yang menghasilkan library atau executable
* **Module dan use**: memungkinkan kamu mengendalikan organisasi, scope, dan
  privasi dari path
* **Path**: cara menamai sebuah item, seperti struct, fungsi, atau module

Di bab ini, kita akan membahas semua fitur tersebut, mendiskusikan bagaimana
fitur-fitur itu saling berinteraksi, dan menjelaskan cara menggunakannya untuk
mengelola scope. Di akhir bab, kamu seharusnya punya pemahaman yang solid
tentang module system dan bisa bekerja dengan scope layaknya seorang pro!

[workspaces]: ch14-03-cargo-workspaces.html
