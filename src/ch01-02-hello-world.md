## Hello, World!

Sekarang setelah kamu memasang Rust, saatnya menulis program Rust pertamamu.
Saat belajar bahasa baru, orang biasanya menulis program kecil yang mencetak
teks `Hello, world!` ke layar, jadi kita akan melakukan hal yang sama di sini!

> Catatan: Buku ini mengasumsikan kamu sudah cukup mengenal command line. Rust
> tidak menuntut apa pun secara khusus soal editor, perkakas, atau tempat kode
> kamu disimpan, jadi kalau kamu lebih suka memakai IDE alih-alih command line,
> silakan pakai IDE favoritmu. Banyak IDE kini punya semacam dukungan Rust;
> periksa dokumentasi IDE tersebut untuk detailnya. Tim Rust berfokus pada
> penyediaan dukungan IDE yang baik lewat `rust-analyzer`. Lihat
> [Lampiran D][devtools]<!-- ignore --> untuk lebih banyak detail.

<!-- Old headings. Do not remove or links may break. -->
<a id="creating-a-project-directory"></a>

### Penyiapan Direktori Proyek

Kamu akan mulai dengan membuat direktori untuk menyimpan kode Rust kamu. Bagi
Rust, kode kamu tersimpan di mana pun tidak masalah, tapi untuk latihan dan
proyek di buku ini, kita sarankan kamu membuat direktori _projects_ di
direktori home dan menyimpan semua proyekmu di sana.

Buka terminal dan masukkan perintah berikut untuk membuat direktori _projects_
serta direktori untuk proyek “Hello, world!” di dalam direktori _projects_.

Untuk Linux, macOS, dan PowerShell di Windows, masukkan ini:

```console
$ mkdir ~/projects
$ cd ~/projects
$ mkdir hello_world
$ cd hello_world
```

Untuk Windows CMD, masukkan ini:

```cmd
> mkdir "%USERPROFILE%\projects"
> cd /d "%USERPROFILE%\projects"
> mkdir hello_world
> cd hello_world
```

<!-- Old headings. Do not remove or links may break. -->
<a id="writing-and-running-a-rust-program"></a>

<a id="rust-program-basics"></a>
### Dasar-Dasar Program Rust

Selanjutnya, buat file sumber baru dan beri nama _main.rs_. File Rust selalu
berakhiran ekstensi _.rs_. Jika nama file kamu memakai lebih dari satu kata,
konvensinya adalah memisahkan kata itu dengan garis bawah. Sebagai contoh,
gunakan _hello_world.rs_ alih-alih _helloworld.rs_.

Sekarang buka file _main.rs_ yang baru saja kamu buat dan masukkan kode pada
Listing 1-1.

<Listing number="1-1" file-name="main.rs" caption="Program yang mencetak `Hello, world!`">

```rust
fn main() {
    println!("Hello, world!");
}
```

</Listing>

Simpan file itu lalu kembali ke jendela terminal kamu di direktori
_~/projects/hello_world_. Di Linux atau macOS, masukkan perintah berikut untuk
mengompilasi dan menjalankan file:

```console
$ rustc main.rs
$ ./main
Hello, world!
```

Di Windows, masukkan perintah `.\main` alih-alih `./main`:

```powershell
> rustc main.rs
> .\main
Hello, world!
```

Apa pun sistem operasi kamu, string `Hello, world!` seharusnya tercetak ke
terminal. Jika kamu tidak melihat keluaran ini, kembali ke bagian
[“Pemecahan Masalah”][troubleshooting]<!-- ignore --> di bagian Instalasi untuk
cara-cara mendapatkan bantuan.

Jika `Hello, world!` tercetak, selamat! Kamu sudah resmi menulis program Rust.
Dengan begitu, kamu seorang programmer Rust—selamat datang!

<!-- Old headings. Do not remove or links may break. -->

<a id="anatomy-of-a-rust-program"></a>

### Anatomi Sebuah Program Rust

Mari kita tinjau program “Hello, world!” ini secara detail. Ini bagian pertama
dari teka-teki:

```rust
fn main() {

}
```

Baris-baris ini mendefinisikan fungsi bernama `main`. Fungsi `main` istimewa:
fungsi ini selalu kode pertama yang berjalan di setiap program Rust yang bisa
dieksekusi. Di sini, baris pertama mendeklarasikan fungsi bernama `main` yang
tidak memiliki parameter dan tidak mengembalikan apa pun. Jika ada parameter,
parameter itu diletakkan di dalam tanda kurung (`()`).

Badan fungsi dibungkus oleh `{}`. Rust mewajibkan kurung kurawal di sekeliling
semua badan fungsi. Gaya yang baik adalah menempatkan kurung kurawal pembuka
pada baris yang sama dengan deklarasi fungsi, dengan satu spasi di antaranya.

> Catatan: Jika kamu ingin memakai gaya standar yang konsisten di semua proyek
> Rust, kamu bisa memakai tool formatter otomatis bernama `rustfmt` untuk
> memformat kode dengan gaya tertentu (lebih lanjut soal `rustfmt` di
> [Lampiran D][devtools]<!-- ignore -->). Tim Rust menyertakan tool ini dalam
> distribusi standar Rust, sama seperti `rustc`, jadi tool ini seharusnya sudah
> terpasang di komputer kamu!

Badan fungsi `main` berisi kode berikut:

```rust
println!("Hello, world!");
```

Baris inilah yang melakukan semua pekerjaan di program kecil ini: mencetak teks
ke layar. Ada tiga detail penting yang perlu kamu perhatikan.

Pertama, `println!` memanggil sebuah macro Rust. Jika yang dipanggil adalah
fungsi, penulisannya adalah `println` (tanpa `!`). Macro Rust adalah cara
menulis kode yang menghasilkan kode untuk memperluas sintaks Rust, dan kita
akan membahasnya lebih rinci di [Bab 20][ch20-macros]<!-- ignore -->. Untuk
sekarang, kamu hanya perlu tahu bahwa penggunaan `!` berarti kamu memanggil
macro, bukan fungsi biasa, dan macro tidak selalu mengikuti aturan yang sama
dengan fungsi.

Kedua, kamu melihat string `"Hello, world!"`. String itu kita oper sebagai
argumen ke `println!`, dan string dicetak ke layar.

Ketiga, kita mengakhiri baris dengan titik koma (`;`), yang menandai ekspresi
ini sudah selesai dan ekspresi berikutnya siap dimulai. Sebagian besar baris
kode Rust diakhiri dengan titik koma.

<!-- Old headings. Do not remove or links may break. -->
<a id="compiling-and-running-are-separate-steps"></a>

### Kompilasi dan Eksekusi

Kamu baru saja menjalankan program yang baru dibuat, jadi mari kita periksa
setiap langkah dalam prosesnya.

Sebelum menjalankan program Rust, kamu harus mengompilasinya memakai compiler
Rust: masukkan perintah `rustc` dan berikan nama file sumber kamu sebagai
argumennya, seperti ini:

```console
$ rustc main.rs
```

Jika kamu punya latar belakang C atau C++, kamu akan melihat ini mirip dengan
`gcc` atau `clang`. Setelah kompilasi berhasil, Rust menghasilkan executable
binary.

Di Linux, macOS, dan PowerShell di Windows, kamu bisa melihat executable-nya
dengan memasukkan perintah `ls` di shell:

```console
$ ls
main  main.rs
```

Di Linux dan macOS, kamu akan melihat dua file. Di PowerShell pada Windows, kamu
akan melihat tiga file yang sama seperti saat memakai CMD. Di CMD pada Windows,
kamu akan memasukkan ini:

```cmd
> dir /B %= the /B option says to only show the file names =%
main.exe
main.pdb
main.rs
```

Keluaran ini menunjukkan file kode sumber dengan ekstensi _.rs_, file
executable (_main.exe_ di Windows, tapi _main_ di platform lainnya), dan, saat
memakai Windows, file yang berisi informasi debugging dengan ekstensi _.pdb_.
Dari sini, kamu menjalankan file _main_ atau _main.exe_, seperti ini:

```console
$ ./main # or .\main on Windows
```

Jika _main.rs_ kamu adalah program “Hello, world!”, baris ini mencetak `Hello,
world!` ke terminal kamu.

Jika kamu lebih terbiasa dengan bahasa dinamis seperti Ruby, Python, atau
JavaScript, kamu mungkin belum terbiasa mengompilasi dan menjalankan program
sebagai dua langkah yang terpisah. Rust adalah bahasa yang _dikompilasi
ahead-of-time_, artinya kamu bisa mengompilasi program dan memberikan
executable-nya ke orang lain, dan orang itu bisa menjalankannya bahkan tanpa
memasang Rust. Jika kamu memberi seseorang file _.rb_, _.py_, atau _.js_,
mereka perlu memasang implementasi Ruby, Python, atau JavaScript
(masing-masing). Tapi di bahasa-bahasa itu, kamu hanya butuh satu perintah
untuk mengompilasi dan menjalankan program kamu. Segalanya adalah trade-off
dalam desain bahasa.

Mengompilasi dengan `rustc` saja sudah cukup untuk program sederhana, tapi
seiring proyek kamu bertumbuh, kamu akan perlu mengelola semua opsi dan
memudahkan proses berbagi kode. Selanjutnya, kita akan memperkenalkan kamu pada
tool Cargo, yang akan membantu kamu menulis program Rust yang dipakai di dunia
nyata.

[troubleshooting]: ch01-01-installation.html#troubleshooting
[devtools]: appendix-04-useful-development-tools.html
[ch20-macros]: ch20-05-macros.html
