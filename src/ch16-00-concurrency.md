# Konkurensi Tanpa Rasa Takut

Menangani pemrograman konkuren dengan aman dan efisien adalah salah satu tujuan utama Rust lainnya. _Concurrent programming_, saat bagian-bagian berbeda dari sebuah program dieksekusi secara independen, dan _parallel programming_, saat bagian-bagian berbeda dieksekusi secara bersamaan, menjadi semakin penting seiring makin banyak komputer yang memanfaatkan banyak prosesor. Secara historis, pemrograman dalam konteks seperti ini sulit dan rawan error. Rust berharap bisa mengubahnya.

Awalnya, tim Rust mengira bahwa menjaga keamanan memori dan mencegah masalah concurrency adalah dua tantangan terpisah yang harus diselesaikan dengan metode berbeda. Seiring waktu, tim menemukan bahwa sistem ownership dan sistem tipe adalah sekumpulan alat yang ampuh untuk mengelola keamanan memori _dan_ masalah concurrency! Dengan memanfaatkan ownership dan pemeriksaan tipe, banyak error concurrency di Rust menjadi error saat kompilasi, bukan error saat runtime. Jadi, alih-alih menyuruhmu menghabiskan banyak waktu untuk mencoba mereproduksi keadaan persis ketika bug concurrency saat runtime muncul, kode yang salah akan menolak untuk dikompilasi dan menampilkan error yang menjelaskan masalahnya. Hasilnya, kamu bisa memperbaiki kode saat masih mengerjakannya, bukan nanti setelah kode itu dikirim ke produksi. Kita menyebut aspek Rust ini _fearless concurrency_. _Fearless concurrency_ memungkinkan kamu menulis kode yang bebas dari bug halus dan mudah di-refactor tanpa memunculkan bug baru.

> Catatan: Demi kesederhanaan, kita akan menyebut banyak masalah ini sebagai _concurrent_, alih-alih lebih tepat mengatakannya _concurrent and/or parallel_. Untuk bab ini, setiap kali kita memakai _concurrent_, bayangkanlah bahwa yang dimaksud adalah _concurrent and/or parallel_. Pada bab berikutnya, ketika perbedaannya lebih penting, kita akan lebih spesifik.

Banyak bahasa bersifat dogmatis tentang solusi yang mereka tawarkan untuk menangani masalah concurrency. Misalnya, Erlang punya fitur elegan untuk concurrency dengan message-passing, tetapi hanya punya cara yang kabur untuk berbagi state antar-thread. Mendukung hanya sebagian dari solusi yang mungkin adalah strategi yang masuk akal untuk bahasa tingkat tinggi, karena bahasa tingkat tinggi menjanjikan manfaat dengan melepaskan sebagian kontrol demi mendapatkan abstraksi. Namun, bahasa tingkat rendah diharapkan menyediakan solusi dengan performa terbaik dalam setiap situasi dan memiliki lebih sedikit abstraksi di atas perangkat keras. Karena itu, Rust menawarkan beragam alat untuk memodelkan masalah dengan cara apa pun yang sesuai dengan situasi dan kebutuhanmu.

Berikut topik yang akan kita bahas di bab ini:

- Cara membuat thread untuk menjalankan beberapa bagian kode secara bersamaan
- Concurrency _message-passing_, dengan channel yang mengirim pesan antar-thread
- Concurrency _shared-state_, dengan beberapa thread yang mengakses sebagian data
- Trait `Sync` dan `Send`, yang memperluas jaminan concurrency Rust ke tipe buatan pengguna maupun tipe yang disediakan oleh library standar
