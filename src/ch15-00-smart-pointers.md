# Smart Pointers

Pointer adalah konsep umum untuk variabel yang berisi alamat di memori. Alamat itu merujuk ke, atau “menunjuk”, data lain. Jenis pointer yang paling umum di Rust adalah reference, yang sudah kamu pelajari di Bab 4. Reference ditandai dengan simbol `&` dan meminjam nilai yang ditunjuknya. Selain merujuk ke data, reference tidak punya kemampuan khusus apa pun, dan tidak menimbulkan biaya tambahan.

Di sisi lain, _smart pointer_ adalah struktur data yang bertindak seperti pointer, tapi juga punya metadata dan kemampuan tambahan. Konsep smart pointer tidak eksklusif untuk Rust: smart pointer berasal dari C++ dan juga ada di bahasa lain. Rust punya beragam smart pointer di standard library yang menyediakan fungsionalitas lebih daripada yang bisa diberikan reference. Untuk memahami konsep umumnya, kita akan melihat beberapa contoh smart pointer yang berbeda, termasuk sebuah tipe smart pointer _reference counting_. Pointer ini memungkinkan kamu membuat data memiliki beberapa pemilik dengan mencatat jumlah pemiliknya, dan saat tidak ada pemilik yang tersisa, membersihkan data itu.

Di Rust, dengan konsep ownership dan borrowing, ada satu perbedaan lagi antara reference dan smart pointer: jika reference hanya meminjam data, dalam banyak kasus smart pointer _memiliki_ data yang ditunjuknya.

Smart pointer biasanya diimplementasikan dengan struct. Tidak seperti struct biasa, smart pointer mengimplementasikan trait `Deref` dan `Drop`. Trait `Deref` membuat instance struct smart pointer berperilaku seperti reference, sehingga kamu bisa menulis kode yang bekerja dengan reference maupun smart pointer. Trait `Drop` memungkinkan kamu menyesuaikan kode yang dijalankan saat instance smart pointer keluar dari scope. Di bab ini, kita akan membahas kedua trait itu dan menunjukkan alasan pentingnya bagi smart pointer.

Karena pola smart pointer adalah pola desain umum yang sering dipakai di Rust, bab ini tidak akan membahas setiap smart pointer yang ada. Banyak library punya smart pointer mereka sendiri, dan kamu bahkan bisa menulisnya sendiri. Kita akan membahas smart pointer yang paling umum di standard library:

- `Box<T>`, untuk mengalokasikan nilai di heap
- `Rc<T>`, tipe reference counting yang memungkinkan multiple ownership
- `Ref<T>` dan `RefMut<T>`, yang diakses lewat `RefCell<T>`, tipe yang menegakkan aturan borrowing saat runtime alih-alih saat compile time

Selain itu, kita akan membahas pola _interior mutability_, saat tipe immutable mengekspos API untuk mengubah nilai di dalamnya. Kita juga akan membahas reference cycle: bagaimana siklus itu bisa membocorkan memori dan cara mencegahnya.

Mari kita mulai!
