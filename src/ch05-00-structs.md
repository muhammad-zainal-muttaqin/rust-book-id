# Menggunakan Struct untuk Menata Data yang Berkaitan

_struct_, atau _structure_, adalah tipe data kustom yang memungkinkan kamu
menggabungkan sekaligus memberi nama pada beberapa nilai yang saling berkaitan
sehingga membentuk satu kelompok bermakna. Jika kamu terbiasa dengan bahasa
berorientasi objek, struct mirip dengan atribut data sebuah objek. Di bab ini,
kita akan membandingkan tuple dengan struct untuk membangun di atas pengetahuan
yang sudah kamu punya, sekaligus menunjukkan kapan struct menjadi cara yang
lebih baik untuk mengelompokkan data.

Kita akan memperlihatkan cara mendefinisikan dan menginstansiasi struct. Kita
akan membahas cara mendefinisikan fungsi terkait, khususnya jenis fungsi terkait
yang disebut _methods_, untuk menentukan perilaku yang terkait dengan sebuah
tipe struct. Struct dan enum (dibahas di Bab 6) adalah batu bata pembangun
untuk membuat tipe baru di dalam domain programmu, sehingga kamu bisa
memanfaatkan sepenuhnya pemeriksaan tipe saat kompilasi dari Rust.
