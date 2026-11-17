<a id="variables-and-mutability"></a>
## Variabel dan Mutability

Seperti yang disebutkan di bagian [“Menyimpan Nilai dengan
Variabel”][storing-values-with-variables]<!-- ignore -->, secara default
variabel itu immutable. Ini salah satu dari banyak dorongan yang diberikan Rust
padamu untuk menulis kode dengan cara yang memanfaatkan kemudahan dan keamanan
yang ditawarkan Rust. Meski begitu, kamu tetap bisa membuat variabelmu mutable.
Mari kita telusuri bagaimana dan mengapa Rust mendorongmu memilih immutability,
serta mengapa terkadang kamu mungkin ingin menyimpang dari itu.

Ketika sebuah variabel immutable, begitu sebuah nilai terikat pada sebuah nama,
kamu tidak bisa mengubah nilai itu. Untuk mengilustrasikan hal ini, buat proyek
baru bernama _variables_ di direktori _projects_ kamu dengan menggunakan
`cargo new variables`.

Selanjutnya, di direktori _variables_ baru kamu, buka _src/main.rs_ dan
ganti isinya dengan kode berikut, yang belum akan terkompilasi:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/src/main.rs}}
```

Simpan dan jalankan program dengan `cargo run`. Kamu akan menerima pesan error
tentang error immutability, seperti pada output berikut:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/output.txt}}
```

Contoh ini menunjukkan bagaimana compiler membantumu menemukan error di
programmu. Error compiler bisa membuat frustrasi, tapi sebenarnya itu hanya
berarti programmu belum dengan aman melakukan apa yang kamu inginkan; itu
_bukan_ berarti kamu bukan programmer yang baik! Rustacean berpengalaman pun
masih mendapatkan error compiler.

Kamu menerima pesan error `` cannot assign twice to immutable variable `x` ``
karena kamu mencoba menetapkan nilai kedua pada variabel immutable `x`.

Penting bagi kita untuk mendapatkan error compile-time ketika mencoba mengubah
nilai yang ditetapkan immutable, karena situasi seperti ini bisa menimbulkan
bug. Jika satu bagian kode kita bekerja dengan asumsi sebuah nilai tidak akan
pernah berubah, sementara bagian kode lain mengubah nilai itu, maka bisa saja
bagian pertama tidak melakukan apa yang dirancang untuk dilakukan. Penyebab
bug semacam ini bisa sulit dilacak setelah kejadian, terutama ketika potongan
kode kedua mengubah nilai itu hanya _kadang-kadang_. Compiler Rust menjamin
bahwa saat kamu menyatakan sebuah nilai tidak akan berubah, nilai itu
benar-benar tidak berubah, jadi kamu tidak perlu melacaknya sendiri. Dengan
begitu, kode kamu lebih mudah direasoning.

Tapi mutability bisa sangat berguna dan bisa membuat kode lebih nyaman
ditulis. Meskipun variabel itu immutable secara default, kamu bisa membuatnya
mutable dengan menambahkan `mut` di depan nama variabel seperti yang kamu
lakukan di [Bab 2][storing-values-with-variables]<!-- ignore -->. Menambahkan
`mut` juga menyampaikan niat kepada pembaca kode di masa depan, karena
menunjukkan bahwa bagian kode lain akan mengubah nilai variabel tersebut.

Sebagai contoh, mari ubah _src/main.rs_ menjadi berikut:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/src/main.rs}}
```

Ketika kita jalankan programnya sekarang, kita dapat ini:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/output.txt}}
```

Kita diperbolehkan mengubah nilai yang terikat pada `x` dari `5` ke `6` saat
`mut` digunakan. Pada akhirnya, memutuskan apakah akan menggunakan mutability
atau tidak terserah padamu dan tergantung pada apa yang kamu anggap paling
jelas pada situasi tertentu.

<!-- Old headings. Do not remove or links may break. -->
<a id="constants"></a>

<a id="declaring-constants"></a>
### Mendeklarasikan Konstanta

Seperti variabel immutable, _konstanta_ adalah nilai yang terikat pada sebuah
nama dan tidak boleh berubah, tapi ada beberapa perbedaan antara konstanta dan
variabel.

Pertama, kamu tidak boleh menggunakan `mut` pada konstanta. Konstanta bukan
hanya immutable secara default—mereka selalu immutable. Kamu mendeklarasikan
konstanta menggunakan keyword `const` alih-alih keyword `let`, dan tipe nilai
itu _harus_ dianotasi. Kita akan membahas tipe dan anotasi tipe di bagian
selanjutnya, [“Data Types”][data-types]<!-- ignore -->, jadi jangan khawatir
tentang detailnya sekarang. Cukup ketahui bahwa kamu harus selalu menganotasi
tipenya.

Konstanta bisa dideklarasikan di scope mana pun, termasuk scope global, yang
membuatnya berguna untuk nilai yang perlu diketahui oleh banyak bagian kode.

Perbedaan terakhir adalah konstanta hanya boleh diset ke sebuah ekspresi
konstanta, bukan hasil dari nilai yang hanya bisa dihitung pada runtime.

Berikut contoh deklarasi konstanta:

```rust
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
```

Nama konstanta itu adalah `THREE_HOURS_IN_SECONDS`, dan nilainya diset ke hasil
perkalian 60 (jumlah detik dalam satu menit) dengan 60 (jumlah menit dalam satu
jam) dengan 3 (jumlah jam yang ingin kita hitung dalam program ini). Konvensi
penamaan Rust untuk konstanta adalah menggunakan huruf kapital semua dengan
garis bawah di antara kata-katanya. Compiler mampu mengevaluasi kumpulan operasi
terbatas saat compile time, yang memungkinkan kita memilih untuk menulis nilai
ini dengan cara yang lebih mudah dipahami dan diverifikasi, alih-alih menyetel
konstanta ini ke nilai 10.800. Lihat bagian [evaluasi konstanta di Rust
Reference][const-eval] untuk informasi lebih lanjut tentang operasi apa yang
bisa digunakan saat mendeklarasikan konstanta.

Konstanta berlaku selama program berjalan, di dalam scope tempat mereka
dideklarasikan. Sifat ini membuat konstanta berguna untuk nilai-nilai di
domain aplikasimu yang mungkin perlu diketahui oleh banyak bagian program, seperti
jumlah poin maksimum yang boleh diperoleh setiap pemain dalam sebuah game, atau
kecepatan cahaya.

Memberi nama pada nilai hardcoded yang digunakan di seluruh programmu sebagai
konstanta berguna untuk menyampaikan makna nilai tersebut kepada para
pemelihara kode di masa depan. Ini juga membantu untuk hanya punya satu tempat
di kode kamu yang perlu diubah jika nilai hardcoded itu perlu diperbarui di
masa depan.

<a id="shadowing"></a>
### Shadowing

Seperti yang kamu lihat di tutorial guessing game di [Bab
2][comparing-the-guess-to-the-secret-number]<!-- ignore -->, kamu bisa
mendeklarasikan variabel baru dengan nama yang sama dengan variabel sebelumnya.
Rustacean menyebut variabel pertama _di-shadowing_ oleh variabel kedua, yang
artinya variabel kedualah yang akan dilihat compiler ketika kamu menggunakan
nama variabel itu. Secara efektif, variabel kedua menaungi yang pertama,
mengambil setiap penggunaan nama variabel itu untuk dirinya sendiri sampai
dirinya ikut di-shadowing atau scope berakhir. Kita bisa men-shadow variabel
dengan menggunakan nama variabel yang sama dan mengulang penggunaan keyword
`let` seperti berikut:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/src/main.rs}}
```

Program ini pertama mengikat `x` ke nilai `5`. Lalu, ia membuat variabel baru
`x` dengan mengulang `let x =`, mengambil nilai awal dan menambahkan `1`
sehingga nilai `x` menjadi `6`. Kemudian, di dalam scope inner yang dibuat
dengan kurung kurawal, statement `let` ketiga juga men-shadow `x` dan membuat
variabel baru, mengalikan nilai sebelumnya dengan `2` sehingga `x` menjadi
`12`. Ketika scope itu berakhir, shadowing inner berakhir dan `x` kembali
menjadi `6`. Ketika kita jalankan program ini, outputnya sebagai berikut:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/output.txt}}
```

Shadowing berbeda dari menandai sebuah variabel sebagai `mut` karena kita akan
mendapatkan error compile-time jika secara tidak sengaja mencoba menetapkan
ulang variabel ini tanpa menggunakan keyword `let`. Dengan menggunakan `let`,
kita bisa melakukan beberapa transformasi pada sebuah nilai, tapi variabelnya
tetap immutable setelah transformasi itu selesai.

Perbedaan lain antara `mut` dan shadowing adalah karena kita efektifnya membuat
variabel baru ketika menggunakan keyword `let` lagi, kita bisa mengubah tipe
nilai itu tapi tetap memakai nama yang sama. Sebagai contoh, misalkan program
kita meminta pengguna menunjukkan berapa banyak spasi yang mereka inginkan
di antara teks tertentu dengan memasukkan karakter spasi, lalu kita ingin
menyimpan input itu sebagai angka:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-04-shadowing-can-change-types/src/main.rs:here}}
```

Variabel `spaces` pertama bertipe string, dan variabel `spaces` kedua bertipe
angka. Dengan begitu, shadowing membuat kita tidak perlu memikirkan nama
berbeda, seperti `spaces_str` dan `spaces_num`; sebagai gantinya, kita bisa
memakai ulang nama `spaces` yang lebih sederhana. Namun, jika kita mencoba
menggunakan `mut` untuk ini, seperti ditunjukkan di sini, kita akan mendapatkan
error compile-time:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/src/main.rs:here}}
```

Error itu mengatakan kita tidak boleh memutasi tipe sebuah variabel:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/output.txt}}
```

Sekarang setelah kita menelusuri cara kerja variabel, mari kita lihat lebih
banyak data types yang bisa dimilikinya.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[data-types]: ch03-02-data-types.html#data-types
[storing-values-with-variables]: ch02-00-guessing-game-tutorial.html#storing-values-with-variables
[const-eval]: ../reference/const_eval.html