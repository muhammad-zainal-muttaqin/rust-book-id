# Menulis Test Otomatis

Dalam esai tahun 1972-nya, “The Humble Programmer,” Edsger W. Dijkstra berkata bahwa “menguji program bisa menjadi cara yang sangat efektif untuk menunjukkan adanya bug, tetapi sama sekali tidak memadai untuk membuktikan bahwa bug itu tidak ada.” Namun itu bukan berarti kita tidak boleh berusaha menguji sebanyak mungkin!

_Kebenaran_ dalam program kita adalah sejauh mana kode kita melakukan apa yang kita maksud. Rust dirancang dengan perhatian yang besar terhadap kebenaran program, tetapi kebenaran itu kompleks dan tidak mudah dibuktikan. Sistem tipe Rust menanggung bagian besar dari beban ini, tetapi sistem tipe tidak bisa menangkap semuanya. Oleh karena itu, Rust menyediakan dukungan untuk menulis test perangkat lunak otomatis.

Misalkan kita menulis fungsi `add_two` yang menambahkan 2 pada angka apa pun yang diberikan kepadanya. Signature fungsi ini menerima sebuah integer sebagai parameter dan mengembalikan integer sebagai hasil. Saat kita mengimplementasikan dan mengompilasi fungsi itu, Rust melakukan semua pengecekan tipe dan pengecekan borrowing yang sudah kamu pelajari sejauh ini untuk memastikan, misalnya, bahwa kita tidak memberikan nilai `String` atau reference yang tidak valid ke fungsi ini. Tetapi Rust _tidak bisa_ memeriksa apakah fungsi ini akan melakukan tepat apa yang kita maksud, yaitu mengembalikan parameter ditambah 2—bukan, misalnya, parameter ditambah 10 atau parameter dikurangi 50! Di sinilah test berperan.

Kita bisa menulis test yang menegaskan, misalnya, bahwa saat kita memberikan `3` ke fungsi `add_two`, nilai yang dikembalikan adalah `5`. Kita bisa menjalankan test-test ini kapan pun kita mengubah kode, untuk memastikan perilaku yang sudah benar tidak berubah.

Menguji adalah keterampilan yang kompleks: meski kita tidak bisa membahas dalam satu bab setiap detail tentang cara menulis test yang baik, dalam bab ini kita akan mendiskusikan mekanika fasilitas testing Rust. Kita akan berbicara tentang anotasi dan macro yang tersedia untukmu saat menulis test, perilaku default dan opsi yang disediakan untuk menjalankan test, serta cara mengorganisasi test menjadi unit test dan integration test.
