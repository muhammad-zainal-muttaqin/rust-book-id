# Pendahuluan

> Catatan: Edisi buku ini sama dengan [The Rust Programming
> Language][nsprust] yang tersedia dalam format cetak dan ebook dari
> [No Starch Press][nsp].

[nsprust]: https://nostarch.com/rust-programming-language-3rd-edition
[nsp]: https://nostarch.com/

Selamat datang di _The Rust Programming Language_, buku pengantar tentang Rust.
Bahasa pemrograman Rust membantu kamu menulis perangkat lunak yang lebih cepat
dan lebih andal. Dalam desain bahasa pemrograman, ergonomis di tingkat tinggi
dan kendali di tingkat rendah sering saling bertentangan; Rust menantang
dilema tersebut. Dengan menyeimbangkan kemampuan teknis yang kuat dan
pengalaman pengembang yang menyenangkan, Rust memberi kamu pilihan untuk
mengendalikan detail tingkat rendah (seperti penggunaan memori) tanpa
kerepotan yang biasanya melekat pada kendali semacam itu.

## Rust Ditujukan untuk Siapa

Rust cocok untuk banyak orang karena berbagai alasan. Mari kita lihat
beberapa kelompok paling penting.

### Tim Pengembang

Rust terbukti menjadi alat yang produktif untuk kolaborasi di antara tim
pengembang besar dengan tingkat pengetahuan sistem yang bervariasi. Kode
tingkat rentan terhadap berbagai bug halus yang, di sebagian besar bahasa
lain, hanya bisa ditemukan lewat pengujian menyeluruh dan tinjauan kode
ketat oleh pengembang berpengalaman. Di Rust, compiler memegang peran
penjaga gerbang dengan menolak mengompilasi kode yang mengandung bug licik
seperti itu, termasuk bug concurrency. Dengan bekerja bersama compiler,
tim bisa menghabiskan waktu untuk fokus pada logika program, bukan mengejar
bug.

Rust juga membawa perkembangan alat pengembang modern ke dunia
pemrograman sistem:

- Cargo, dependency manager dan alat build yang disertakan, membuat
  penambahan, kompilasi, dan pengelolaan dependency menjadi mudah serta
  konsisten di seluruh ekosistem Rust.
- Alat format `rustfmt` memastikan gaya penulisan kode yang konsisten di
  antara pengembang.
- Rust Language Server menggerakkan integrasi integrated development
  environment (IDE) untuk pelengkapan kode dan pesan error inline.

Dengan memakai alat-alat ini dan alat lain di ekosistem Rust, pengembang bisa
tetap produktif saat menulis kode tingkat sistem.

### Mahasiswa

Rust ditujukan bagi mahasiswa dan siapa pun yang tertarik mempelajari konsep
sistem. Dengan memakai Rust, banyak orang mempelajari topik seperti
pengembangan sistem operasi. Komunitasnya sangat ramah dan senang menjawab
pertanyaan mahasiswa. Lewat usaha seperti buku ini, tim Rust ingin membuat
konsep sistem lebih mudah diakses oleh lebih banyak orang, terutama yang baru
belajar pemrograman.

### Perusahaan

Ratusan perusahaan, besar maupun kecil, memakai Rust dalam produksi untuk
berbagai tugas, termasuk tool command line, layanan web, tooling DevOps,
perangkat tertanam, analisis dan transkoding audio-video, mata uang
kriptografi, bioinformatika, mesin pencari, aplikasi Internet of Things,
machine learning, dan bahkan bagian-bagian utama dari web browser Firefox.

### Pengembang Open Source

Rust ditujukan bagi orang yang ingin membangun bahasa pemrograman Rust,
komunitas, alat pengembang, dan library. Kami senang sekali kalau kamu ikut
berkontribusi pada bahasa Rust.

### Orang yang Menghargai Kecepatan dan Stabilitas

Rust ditujukan bagi orang yang mendambakan kecepatan dan stabilitas dalam
sebuah bahasa. Kecepatan di sini mencakup dua hal: seberapa cepat kode Rust
bisa berjalan, dan seberapa cepat Rust membiarkan kamu menulis program.
Pemeriksaan compiler Rust menjamin stabilitas saat menambahkan fitur dan
melakukan refactoring. Ini berbeda dengan kode warisan yang rapuh di bahasa
tanpa pemeriksaan semacam itu, yang sering enggan diubah oleh pengembang.
Dengan berusaha mewujudkan abstraksi biaya nol—fitur tingkat tinggi yang
dikompilasi menjadi kode tingkat rendah secepat kode yang ditulis
manual—Rust berusaha membuat kode yang aman juga menjadi kode yang cepat.

Bahasa Rust berharap bisa mendukung banyak pengguna lain; yang disebut di
sini hanyalah beberapa pihak paling penting. Secara keseluruhan, ambisi
terbesar Rust adalah menghilangkan trade-off yang sudah diterima programmer
selama puluhan tahun dengan menyediakan keamanan _sekaligus_ produktivitas,
kecepatan _sekaligus_ ergonomis. Cobalah Rust, dan lihat apakah pilihannya
cocok untuk kamu.

## Buku Ini Ditujukan untuk Siapa

Buku ini mengasumsikan kamu sudah menulis kode di bahasa pemrograman lain,
tetapi tidak berasumsi bahasa yang mana. Kami berusaha membuat materi ini
dapat diakses luas oleh orang dengan latar belakang pemrograman yang
beragam. Kami tidak menghabiskan banyak waktu membahas apa itu pemrograman
atau bagaimana cara berpikir tentangnya. Jika kamu benar-benar baru dalam
pemrograman, kamu akan lebih terbantu dengan membuka buku yang khusus
memberikan pengantar tentang pemrograman.

## Cara Memakai Buku Ini

Secara umum, buku ini mengasumsikan kamu membacanya secara berurutan dari
awal sampai akhir. Bab-bab belakang dibangun di atas konsep dari bab-bab
sebelumnya, dan bab-bab awal mungkin tidak membahas detail suatu topik
tertentu, tetapi akan membahasnya kembali di bab kemudian.

Kamu akan menemukan dua jenis bab dalam buku ini: bab konsep dan bab proyek.
Di bab konsep, kamu akan mempelajari aspek tertentu dari Rust. Di bab proyek,
kita akan membangun program kecil bersama, menerapkan apa yang sudah kamu
pelajari sejauh ini. Bab 2, Bab 12, dan Bab 21 adalah bab proyek; selebihnya
adalah bab konsep.

**Bab 1** menjelaskan cara memasang Rust, cara menulis program "Hello,
world!", dan cara memakai Cargo, package manager dan alat build milik Rust.
**Bab 2** adalah pengantar praktis untuk menulis program di Rust, di mana
kamu akan membangun sebuah permainan tebak-angka. Di sini kita membahas
konsep pada tingkat tinggi, dan bab-bab selanjutnya akan memberikan detail
tambahan. Jika kamu ingin langsung terjun sejak awal, Bab 2 adalah tempatnya.
Jika kamu tipe pembelajar yang sangat teliti dan ingin menguasai setiap
detail sebelum lanjut ke materi berikutnya, mungkin kamu ingin melompati Bab
2 dan langsung ke **Bab 3**, yang membahas fitur-fitur Rust yang mirip dengan
bahasa pemrograman lain; setelah itu, kamu bisa kembali ke Bab 2 kapan pun
ingin mengerjakan proyek yang menerapkan detail yang sudah kamu pelajari.

Di **Bab 4**, kamu akan mempelajari sistem ownership Rust. **Bab 5**
membahas struct dan method. **Bab 6** membahas enum, ekspresi `match`, serta
konstruk kontrol `if let` dan `let...else`. Kamu akan memakai struct dan enum
untuk membuat tipe kustom.

Di **Bab 7**, kamu akan mempelajari sistem module Rust dan aturan privasi
untuk mengorganisasi kode serta application programming interface (API)
publiknya. **Bab 8** membahas beberapa struktur data kumpulan yang disediakan
standard library: vector, string, dan hash map. **Bab 9** menjelajahi filosofi
dan teknik penanganan error Rust.

**Bab 10** membahas generic, trait, dan lifetime, yang memberimu kemampuan
mendefinisikan kode yang berlaku untuk banyak tipe. **Bab 11** sepenuhnya
tentang test, yang bahkan dengan jaminan keamanan Rust tetap diperlukan
untuk memastikan logika programmu benar. Di **Bab 12**, kita akan membangun
implementasi kita sendiri dari sebagian fungsi tool `grep` pada command line
yang mencari teks di dalam file. Untuk ini, kita akan memakai banyak konsep
yang sudah kita bahas di bab-bab sebelumnya.

**Bab 13** menjelajahi closure dan iterator: fitur Rust yang berasal dari
bahasa pemrograman fungsional. Di **Bab 14**, kita akan mempelajari Cargo
lebih dalam dan membahas praktik terbaik untuk berbagi library-mu dengan
orang lain. **Bab 15** membahas smart pointer yang disediakan standard
library beserta trait yang memungkinkan fungsionalitasnya.

Di **Bab 16**, kita akan menelusuri berbagai model pemrograman konkurensi dan
membahas bagaimana Rust membantu kamu memprogram dengan banyak thread tanpa
takut. Di **Bab 17**, kita melanjutkan dari situ dengan menjelajahi sintaks
async dan await milik Rust, bersama dengan task, future, dan stream, serta
model konkurensi ringan yang mereka aktifkan.

**Bab 18** membahas bagaimana idioma Rust dibandingkan dengan prinsip
pemrograman berorientasi objek yang mungkin sudah kamu kenal. **Bab 19**
adalah referensi tentang pattern dan pencocokan pola, yang merupakan cara
kuat untuk mengekspresikan ide di seluruh program Rust. **Bab 20** berisi
beragam topik lanjutan yang menarik, termasuk unsafe Rust, macro, dan
penjelasan lebih lanjut tentang lifetime, trait, tipe, fungsi, dan closure.

Di **Bab 21**, kita akan menyelesaikan sebuah proyek di mana kita akan
mengimplementasikan web server multithreaded tingkat rendah!

Terakhir, beberapa lampiran memuat informasi berguna tentang bahasa ini dalam
format yang lebih menyerupai referensi. **Lampiran A** membahas keyword Rust,
**Lampiran B** membahas operator dan simbol Rust, **Lampiran C** membahas
trait yang bisa diturunkan yang disediakan standard library, **Lampiran D**
membahas beberapa alat pengembangan yang berguna, dan **Lampiran E**
menjelaskan edisi Rust. Di **Lampiran F**, kamu bisa menemukan terjemahan
buku ini, dan di **Lampiran G** kita akan membahas bagaimana Rust dibuat dan
apa itu Rust nightly.

Tidak ada cara yang salah untuk membaca buku ini: kalau kamu ingin
melompati sebagian isi, silakan! Kamu mungkin harus kembali ke bab-bab
sebelumnya jika mengalami kebingungan. Tapi lakukan apa pun yang paling
menolongmu.

<span id="ferris"></span>

Bagian penting dari proses belajar Rust adalah belajar membaca pesan error
yang ditampilkan compiler: pesan itu akan membawamu menuju kode yang
berfungsi. Karena itu, kita akan memberikan banyak contoh yang tidak bisa
dikompilasi beserta pesan error yang akan ditampilkan compiler pada
masing-masing situasi. Ingat bahwa jika kamu menyalin dan menjalankan contoh
acak, contoh itu mungkin tidak bisa dikompilasi! Pastikan kamu membaca teks
di sekitarnya untuk melihat apakah contoh yang coba kamu jalankan memang
sengaja dibuat error. Pada kebanyakan situasi, kita akan membawamu ke versi
yang benar dari kode yang tidak bisa dikompilasi. Ferris juga akan membantu
membedakan kode yang memang tidak dimaksudkan untuk berfungsi:

| Ferris                                                                                                           | Arti                                             |
| ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| <img src="img/ferris/does_not_compile.svg" class="ferris-explain" alt="Ferris dengan tanda tanya"/>               | Kode ini tidak bisa dikompilasi!                 |
| <img src="img/ferris/panics.svg" class="ferris-explain" alt="Ferris mengangkat kedua tangannya"/>                | Kode ini panics!                                |
| <img src="img/ferris/not_desired_behavior.svg" class="ferris-explain" alt="Ferris dengan satu cakar terangkat, bahu mengangkat"/> | Kode ini tidak menghasilkan perilaku yang diinginkan. |

Pada kebanyakan situasi, kita akan membawamu ke versi yang benar dari kode
yang tidak bisa dikompilasi.

## Kode Sumber

File sumber yang dipakai untuk menyusun buku ini bisa ditemukan di
[GitHub][book].

[book]: https://github.com/rust-lang/book/tree/main/src
