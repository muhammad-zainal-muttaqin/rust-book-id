<a id="installation"></a>
## Instalasi

Langkah pertama adalah memasang Rust. Kita akan mengunduh Rust melalui
`rustup`, sebuah tool command line untuk mengelola versi Rust dan tool pendukung
nya. Kamu memerlukan koneksi internet untuk pengunduhan ini.

> Catatan: Jika karena alasan tertentu kamu tidak ingin memakai `rustup`, lihat
> [halaman metode instalasi Rust lainnya][otherinstall] untuk lebih banyak opsi.

Langkah-langkah berikut memasang versi stable terbaru dari compiler Rust.
Jaminan stabilitas Rust memastikan semua contoh di buku ini yang bisa
mengompilasi akan tetap bisa mengompilasi dengan versi Rust yang lebih baru.
Outputnya mungkin sedikit berbeda antar versi karena Rust sering memperbaiki
pesan error dan warning. Singkatnya, versi stable Rust yang lebih baru apa pun
yang kamu pasang dengan langkah-langkah ini seharusnya bekerja sebagaimana
diharapkan dengan isi buku ini.

> ### Notasi Command Line
>
> Di bab ini dan di seluruh buku, kita akan menampilkan beberapa perintah yang
> dipakai di terminal. Baris yang harus kamu masukkan di terminal selalu
> dimulai dengan `$`. Kamu tidak perlu mengetik karakter `$`; itu adalah
> prompt command line yang ditampilkan sebagai penanda awal setiap perintah.
> Baris yang tidak dimulai dengan `$` biasanya menampilkan output dari
> perintah sebelumnya. Selain itu, contoh khusus PowerShell akan memakai `>`
> alih-alih `$`.

### Memasang `rustup` di Linux atau macOS

Jika kamu memakai Linux atau macOS, buka sebuah terminal dan masukkan perintah
berikut:

```console
$ curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
```

Perintah ini mengunduh sebuah skrip dan memulai instalasi tool `rustup`,
yang akan memasang versi stable terbaru Rust. Kamu mungkin akan diminta
memasukkan password. Jika instalasinya berhasil, baris berikut akan muncul:

```text
Rust is installed now. Great!
```

Kamu juga memerlukan sebuah _linker_, yaitu program yang dipakai Rust untuk
menggabungkan hasil kompilasinya menjadi satu file. Kemungkinan besar kamu
sudah memilikinya. Jika kamu mendapat error linker, kamu harus memasang
compiler C, yang biasanya sudah menyertakan linker. Compiler C juga berguna
karena beberapa package Rust umum bergantung pada kode C dan memerlukan
compiler C.

Di macOS, kamu bisa mendapatkan compiler C dengan menjalankan:

```console
$ xcode-select --install
```

Pengguna Linux umumnya harus memasang GCC atau Clang, sesuai dokumentasi
distribusi mereka. Misalnya, jika kamu memakai Ubuntu, kamu bisa memasang
package `build-essential`.

### Memasang `rustup` di Windows

Di Windows, buka [https://www.rust-lang.org/tools/install][install]<!-- ignore
--> dan ikuti petunjuk untuk memasang Rust. Pada suatu tahap dalam proses
instalasi, kamu akan diminta memasang Visual Studio. Ini menyediakan linker
dan library native yang dibutuhkan untuk mengompilasi program. Jika kamu
memerlukan bantuan lebih lanjut untuk langkah ini, lihat
[https://rust-lang.github.io/rustup/installation/windows-msvc.html][msvc]<!--
ignore -->.

Sisa buku ini memakai perintah yang bisa jalan di _cmd.exe_ dan PowerShell.
Jika ada perbedaan tertentu, kita akan menjelaskan mana yang harus dipakai.

<a id="troubleshooting"></a>
### Pemecahan Masalah

Untuk memeriksa apakah Rust sudah terpasang dengan benar, buka sebuah shell
dan masukkan baris ini:

```console
$ rustc --version
```

Kamu akan melihat nomor versi, commit hash, dan tanggal commit dari versi
stable terbaru yang telah dirilis, dalam format berikut:

```text
rustc x.y.z (abcabcabc yyyy-mm-dd)
```

Jika kamu melihat informasi ini, berarti Rust berhasil kamu pasang! Jika kamu
tidak melihatnya, periksa apakah Rust sudah ada di variabel sistem `%PATH%`
kamu dengan cara berikut.

Di Windows CMD, gunakan:

```console
> echo %PATH%
```

Di PowerShell, gunakan:

```powershell
> echo $env:Path
```

Di Linux dan macOS, gunakan:

```console
$ echo $PATH
```

Jika semuanya sudah benar tetapi Rust tetap tidak bekerja, ada banyak tempat
di mana kamu bisa mendapatkan bantuan. Cari tahu cara menghubungi sesama
Rustacean (julukan konyol yang kita pakai untuk diri sendiri) di
[halaman komunitas][community].

### Memperbarui dan Menghapus Instalasi

Setelah Rust terpasang melalui `rustup`, memperbarui ke versi yang baru saja
rilis sangat mudah. Dari shell kamu, jalankan skrip pembaruan berikut:

```console
$ rustup update
```

Untuk menghapus Rust dan `rustup`, jalankan skrip penghapusan berikut dari
shell kamu:

```console
$ rustup self uninstall
```

<!-- Old headings. Do not remove or links may break. -->
<a id="local-documentation"></a>

### Membaca Dokumentasi Lokal

Instalasi Rust juga menyertakan salinan dokumentasi secara lokal sehingga kamu
bisa membacanya secara offline. Jalankan `rustup doc` untuk membuka dokumentasi
lokal di browser kamu.

Setiap kali ada tipe atau fungsi yang disediakan oleh standard library dan kamu
tidak yakin apa fungsinya atau cara menggunakannya, gunakan dokumentasi
application programming interface (API) untuk mencari tahu!

<!-- Old headings. Do not remove or links may break. -->
<a id="text-editors-and-integrated-development-environments"></a>

### Memakai Text Editor dan IDE

Buku ini tidak berasumsi apa pun tentang tool yang kamu pakai untuk menulis
kode Rust. Hampir semua text editor bisa menyelesaikan pekerjaannya! Namun,
banyak text editor dan integrated development environment (IDE) yang punya
dukungan bawaan untuk Rust. Kamu selalu bisa menemukan daftar yang cukup
terkini dari banyak editor dan IDE di [halaman tools][tools] pada situs Rust.

### Bekerja Offline dengan Buku Ini

Di beberapa contoh, kita akan memakai package Rust di luar standard library.
Untuk mengerjakan contoh-contoh itu, kamu perlu punya koneksi internet atau
telah mengunduh dependensi tersebut terlebih dahulu. Untuk mengunduh dependensi
terlebih dahulu, kamu bisa menjalankan perintah berikut. (Kita akan menjelaskan
apa itu `cargo` dan apa fungsi setiap perintah ini secara detail di kemudian
hari.)

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:

* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
* ch14-03-cargo-workspaces.md
-->

```console
$ cargo new get-dependencies
$ cd get-dependencies
$ cargo add rand@0.10.1 trpl@0.2.0
```

Ini akan menyimpan unduhan package-package tersebut ke cache sehingga kamu tidak
perlu mengunduhnya lagi nanti. Setelah kamu menjalankan perintah ini, kamu tidak
perlu menyimpan folder `get-dependencies`. Jika kamu sudah menjalankan perintah
ini, kamu bisa memakai flag `--offline` pada semua perintah `cargo` di sisa
buku ini untuk memakai versi yang tersimpan di cache ini alih-alih mencoba
mengakses jaringan.

[otherinstall]: https://forge.rust-lang.org/infra/other-installation-methods.html
[install]: https://www.rust-lang.org/tools/install
[msvc]: https://rust-lang.github.io/rustup/installation/windows-msvc.html
[community]: https://www.rust-lang.org/community
[tools]: https://www.rust-lang.org/tools
