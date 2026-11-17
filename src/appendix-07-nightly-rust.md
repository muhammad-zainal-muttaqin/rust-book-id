## Lampiran G - Bagaimana Rust Dibuat dan “Nightly Rust”

Lampiran ini membahas bagaimana Rust dibuat dan bagaimana hal itu berpengaruh pada kamu sebagai pengembang Rust.

### Stabilitas Tanpa Stagnasi

Sebagai sebuah bahasa, Rust _sangat_ peduli terhadap stabilitas kode kamu. Kita ingin Rust menjadi fondasi yang kokoh tempat kamu membangun sesuatu, dan kalau segalanya terus-menerus berubah, hal itu mustahil terjadi. Di saat yang sama, kalau kita tidak bisa bereksperimen dengan fitur baru, kita mungkin baru menemukan cacat penting setelah fitur itu dirilis, ketika kita sudah tidak bisa mengubah apa pun lagi.

Solusi kami untuk masalah ini adalah apa yang kami sebut “stabilitas tanpa stagnasi”, dan prinsip panduannya begini: kamu tidak perlu takut meningkatkan ke versi Rust stable yang baru. Setiap peningkatan seharusnya berjalan mulus, sekaligus membawa fitur baru, lebih sedikit bug, dan waktu kompilasi yang lebih cepat.

### Choo, Choo! Release Channel dan Naik Kereta

Pengembangan Rust berjalan dengan _jadwal kereta_. Artinya, semua pengembangan berlangsung di branch utama repo Rust. Rilis mengikuti model kereta rilis software (release train), yang pernah dipakai Cisco IOS dan proyek software lainnya. Ada tiga _release channel_ untuk Rust:

- Nightly
- Beta
- Stable

Sebagian besar pengembang Rust utamanya memakai channel stable, tetapi mereka yang ingin mencoba fitur eksperimental baru bisa memakai nightly atau beta.

Berikut contoh bagaimana proses pengembangan dan rilis ini bekerja: misalkan tim Rust sedang mengerjakan rilis Rust 1.5. Rilis itu sudah terjadi pada Desember 2015, tetapi angka versinya tetap realistis untuk dijadikan contoh. Sebuah fitur baru ditambahkan ke Rust: sebuah commit baru mendarat di branch utama. Setiap malam, versi nightly baru dari Rust dihasilkan. Setiap hari menjadi hari rilis, dan infrastruktur rilis kita membuat rilis-rilis ini secara otomatis. Jadi seiring waktu berjalan, rilis kita terlihat seperti ini, setiap malam:

```text
nightly: * - - * - - *
```

Setiap enam minggu, waktunya mempersiapkan rilis baru! Branch `beta` di repo Rust dibuat dari branch utama yang dipakai nightly. Kini ada dua rilis:

```text
nightly: * - - * - - *
                     |
beta:                *
```

Sebagian besar pengguna Rust tidak aktif memakai rilis beta, tetapi mengujinya terhadap beta di sistem CI mereka untuk membantu Rust menemukan kemungkinan regresi. Sementara itu, rilis nightly tetap terbit setiap malam:

```text
nightly: * - - * - - * - - * - - *
                     |
beta:                *
```

Katakanlah sebuah regresi ditemukan. Syukurlah kita sempat menguji rilis beta sebelum regresi itu menyelinap ke rilis stable! Perbaikannya diterapkan di branch utama sehingga nightly ikut terperbaiki, lalu perbaikan itu di-backport ke branch `beta`, dan rilis beta baru pun dihasilkan:

```text
nightly: * - - * - - * - - * - - * - - *
                     |
beta:                * - - - - - - - - *
```

Enam minggu setelah beta pertama dibuat, waktunya rilis stable! Branch `stable` dibuat dari branch `beta`:

```text
nightly: * - - * - - * - - * - - * - - * - * - *
                     |
beta:                * - - - - - - - - *
                                       |
stable:                                *
```

Hore! Rust 1.5 selesai! Namun, kita lupa satu hal: karena enam minggu sudah berlalu, kita juga butuh beta baru untuk versi Rust _berikutnya_, 1.6. Jadi setelah `stable` dibuat dari `beta`, versi `beta` berikutnya kembali dibuat dari `nightly`:

```text
nightly: * - - * - - * - - * - - * - - * - * - *
                     |                         |
beta:                * - - - - - - - - *       *
                                       |
stable:                                *
```

Inilah yang disebut “model kereta”, karena setiap enam minggu sebuah rilis “meninggalkan stasiun”, tetapi masih harus menempuh perjalanan lewat channel beta sebelum tiba sebagai rilis stable.

Rust merilis setiap enam minggu, teratur seperti jarum jam. Kalau kamu tahu tanggal satu rilis Rust, kamu bisa tahu tanggal rilis berikutnya: enam minggu kemudian. Sisi menyenangkan dari jadwal rilis tiap enam minggu adalah kereta berikutnya akan segera datang. Kalau sebuah fitur kehilangan kesempatan masuk rilis tertentu, tidak perlu khawatir: rilis lain datang tidak lama lagi! Ini membantu mengurangi tekanan untuk menyisipkan fitur yang mungkin belum matang menjelang tenggat rilis.

Terima kasih pada proses ini, kamu selalu bisa mencoba build Rust berikutnya dan memastikan sendiri bahwa upgrade-nya mudah: kalau rilis beta tidak bekerja sebagaimana mestinya, kamu bisa melaporkannya ke tim dan memperbaikinya sebelum rilis stable berikutnya datang! Kerusakan pada rilis beta relatif jarang, tetapi `rustc` tetap saja sebuah software, dan bug memang ada.

### Waktu Perawatan

Proyek Rust mendukung versi stable terbaru. Ketika versi stable baru dirilis, versi lama mencapai akhir masa hidupnya (EOL). Artinya, setiap versi didukung selama enam minggu.

<a id="unstable-features"></a>
### Fitur Unstable

Ada satu hal lagi yang perlu diperhatikan dari model rilis ini: fitur unstable. Rust memakai teknik bernama “feature flags” untuk menentukan fitur mana yang aktif di sebuah rilis. Kalau sebuah fitur baru sedang aktif dikembangkan, fitur itu mendarat di branch utama, dan karenanya masuk nightly, tetapi di balik sebuah _feature flag_. Sebagai pengguna, kamu boleh mencoba fitur yang masih dalam pengerjaan itu, tetapi kamu harus memakai rilis nightly Rust dan menandai kode sumber kamu dengan flag yang sesuai untuk ikut mengaktifkannya.

Kalau kamu memakai rilis beta atau stable Rust, kamu tidak bisa memakai feature flag sama sekali. Inilah kunci yang membuat kita bisa memakai fitur baru secara praktis sebelum menyatakannya stable selamanya. Mereka yang ingin berada di garis paling depan bisa melakukannya, dan mereka yang menginginkan pengalaman yang kokoh bisa bertahan di stable serta tahu bahwa kode mereka tidak akan rusak. Stabilitas tanpa stagnasi.

Buku ini hanya memuat informasi tentang fitur stable, karena fitur yang masih dalam pengerjaan terus berubah, dan pasti akan berbeda antara saat buku ini ditulis dan saat fitur itu diaktifkan di build stable. Kamu bisa menemukan dokumentasi untuk fitur yang hanya tersedia di nightly secara online.

### Rustup dan Peran Rust Nightly

Rustup memudahkan kamu berpindah antar release channel Rust, baik secara global maupun per proyek. Secara bawaan, kamu akan memiliki Rust stable terinstal. Sebagai contoh, untuk menginstal nightly:

```console
$ rustup toolchain install nightly
```

Kamu juga bisa melihat semua _toolchain_ (rilis Rust beserta komponen terkait) yang terinstal lewat `rustup`. Berikut contoh di komputer Windows salah satu penulis kami:

```powershell
> rustup toolchain list
stable-x86_64-pc-windows-msvc (default)
beta-x86_64-pc-windows-msvc
nightly-x86_64-pc-windows-msvc
```

Seperti yang kamu lihat, toolchain stable adalah bawaannya. Sebagian besar pengguna Rust memakai stable sebagian besar waktu. Kamu mungkin ingin memakai stable sebagian besar waktu, tetapi memakai nightly pada proyek tertentu karena kamu peduli pada fitur yang paling mutakhir. Untuk itu, kamu bisa memakai `rustup override` di direktori proyek tersebut untuk menetapkan toolchain nightly sebagai yang akan dipakai `rustup` saat kamu berada di direktori itu:

```console
$ cd ~/projects/needs-nightly
$ rustup override set nightly
```

Kini, setiap kali kamu memanggil `rustc` atau `cargo` di dalam _~/projects/needs-nightly_, `rustup` akan memastikan kamu memakai Rust nightly, bukan Rust stable bawaanmu. Ini sangat berguna ketika kamu punya banyak proyek Rust!

### Proses RFC dan Tim

Lalu, bagaimana kamu tahu tentang fitur-fitur baru ini? Model pengembangan Rust mengikuti _proses Request For Comments (RFC)_. Kalau kamu menginginkan perbaikan di Rust, kamu bisa menulis sebuah proposal yang disebut RFC.

Siapa pun bisa menulis RFC untuk memperbaiki Rust, dan proposal itu direview serta didiskusikan oleh tim Rust yang terdiri dari banyak subtim topik. Ada daftar lengkap tim [di situs Rust](https://www.rust-lang.org/governance), yang mencakup tim untuk setiap bidang proyek: desain bahasa, implementasi compiler, infrastruktur, dokumentasi, dan lainnya. Tim yang tepat membaca proposal beserta komentar-komentarnya, menulis komentar mereka sendiri, dan pada akhirnya tercapai konsensus untuk menerima atau menolak fitur itu.

Kalau fitur itu diterima, sebuah issue dibuka di repo Rust, dan siapa pun bisa mengimplementasikannya. Orang yang mengimplementasikannya bisa jadi bukan orang yang mengusulkan fitur itu sejak awal! Saat implementasinya siap, fitur itu mendarat di branch utama di balik feature gate, seperti yang kita bahas di bagian ["Fitur Unstable"](#unstable-features)<!-- ignore -->.

Setelah beberapa waktu, ketika pengembang Rust yang memakai rilis nightly sudah sempat mencoba fitur baru itu, anggota tim akan mendiskusikan fitur tersebut, bagaimana hasilnya di nightly, dan memutuskan apakah fitur itu layak masuk Rust stable atau tidak. Kalau keputusannya adalah melanjutkan, feature gate dihapus, dan fitur itu kini dianggap stable! Fitur itu menaiki kereta menuju rilis stable baru Rust.
