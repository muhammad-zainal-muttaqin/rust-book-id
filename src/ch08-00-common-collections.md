# Koleksi Umum

Standard library Rust berisi sejumlah struktur data yang sangat berguna yang disebut
_koleksi_. Sebagian besar tipe data lain mewakili satu nilai tertentu, tetapi
koleksi bisa menampung banyak nilai. Berbeda dengan tipe array dan tuple bawaan,
data yang ditunjuk koleksi ini disimpan di heap, artinya jumlah datanya tidak
perlu diketahui saat kompilasi dan bisa bertambah atau berkurang selama program
berjalan. Setiap jenis koleksi punya kemampuan dan biaya yang berbeda, dan
memilih yang tepat untuk situasimu saat ini adalah keterampilan yang akan kamu
kembangkan seiring waktu. Di bab ini, kita akan membahas tiga koleksi yang sangat
sering dipakai dalam program Rust:

- _Vector_ memungkinkan kamu menyimpan sejumlah nilai yang bisa berubah di
  tempat yang berdekatan.
- _String_ adalah kumpulan karakter. Tipe `String` sudah kita sebutkan
  sebelumnya, tetapi di bab ini kita akan membahasnya secara mendalam.
- _Hash map_ memungkinkan kamu mengaitkan sebuah nilai dengan kunci tertentu.
  Hash map adalah implementasi khusus dari struktur data yang lebih umum
  bernama _map_.

Untuk mempelajari jenis koleksi lain yang disediakan oleh standard library, lihat
[dokumentasinya][collections].

Kita akan membahas cara membuat dan memperbarui vector, string, serta hash map,
juga hal yang membuat masing-masing istimewa.

[collections]: ../std/collections/index.html
