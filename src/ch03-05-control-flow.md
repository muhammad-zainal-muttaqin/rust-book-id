<a id="control-flow"></a>
## Alur Kontrol

Kemampuan menjalankan kode tertentu tergantung pada apakah sebuah kondisi
bernilai `true`, serta kemampuan menjalankan kode berulang selama kondisi itu
`true`, adalah blok dasar di hampir semua bahasa pemrograman. Konstruksi yang
paling umum untuk mengontrol alur eksekusi kode Rust adalah ekspresi `if` dan
loop.

### Ekspresi `if`

Ekspresi `if` memungkinkan kamu bercabang dalam kode tergantung pada kondisi
tertentu. Kamu menyediakan sebuah kondisi, lalu menyatakan, “Jika kondisi ini
terpenuhi, jalankan blok kode ini. Jika kondisi tidak terpenuhi, jangan
jalankan blok kode ini.”

Buat proyek baru bernama _branches_ di direktori _projects_ kamu untuk
mengeksplorasi ekspresi `if`. Di file _src/main.rs_, masukkan kode berikut:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/src/main.rs}}
```

Semua ekspresi `if` diawali dengan keyword `if`, diikuti sebuah kondisi. Pada
kasus ini, kondisinya memeriksa apakah variabel `number` bernilai kurang dari 5.
Blok kode yang dieksekusi jika kondisi bernilai `true` kita letakkan tepat
setelah kondisi, di dalam kurung kurawal. Blok kode yang terkait dengan kondisi
pada ekspresi `if` kadang disebut _arms_, sama seperti arm pada ekspresi
`match` yang kita bahas di bagian [“Membandingkan Tebakan dengan Angka
Rahasia”][comparing-the-guess-to-the-secret-number]<!-- ignore --> di Bab 2.

Secara opsional, kita juga bisa menyertakan ekspresi `else`—yang memang kita
pilih di sini—untuk memberi program blok kode alternatif yang dieksekusi jika
kondisi bernilai `false`. Jika kamu tidak menyertakan ekspresi `else` dan
kondisinya `false`, program akan melewati blok `if` dan lanjut ke kode
berikutnya.

Coba jalankan kode ini; kamu akan melihat output berikut:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/output.txt}}
```

Mari kita ubah nilai `number` menjadi nilai yang membuat kondisinya `false`
untuk melihat apa yang terjadi:

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/src/main.rs:here}}
```

Jalankan program lagi, dan lihat outputnya:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/output.txt}}
```

Perlu diperhatikan juga bahwa kondisi pada kode ini _harus_ berupa `bool`.
Jika kondisinya bukan `bool`, kita akan mendapatkan error. Sebagai contoh,
coba jalankan kode berikut:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/src/main.rs}}
```

Kali ini kondisi `if` bernilai `3`, dan Rust melempar error:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/output.txt}}
```

Error tersebut menunjukkan bahwa Rust mengharapkan `bool` tetapi menerima
sebuah integer. Berbeda dengan bahasa seperti Ruby dan JavaScript, Rust tidak
akan mencoba mengonversi tipe non-Boolean menjadi Boolean secara otomatis.
Kamu harus eksplisit dan selalu memberikan `if` sebuah Boolean sebagai
kondisinya. Misalnya, jika kita ingin blok kode `if` hanya dijalankan ketika
sebuah angka tidak sama dengan `0`, kita bisa mengubah ekspresi `if` menjadi
berikut:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-29-if-not-equal-0/src/main.rs}}
```

Menjalankan kode ini akan mencetak `number was something other than zero`.

#### Menangani Beberapa Kondisi dengan `else if`

Kamu bisa menggunakan beberapa kondisi dengan menggabungkan `if` dan `else`
dalam ekspresi `else if`. Sebagai contoh:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/src/main.rs}}
```

Program ini punya empat kemungkinan jalur eksekusi. Setelah menjalankannya,
kamu akan melihat output berikut:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/output.txt}}
```

Saat program ini dieksekusi, program memeriksa setiap ekspresi `if` bergantian,
lalu mengeksekusi body pertama yang kondisinya bernilai `true`. Perhatikan
bahwa meskipun 6 habis dibagi 2, kita tidak melihat output
`number is divisible by 2`, juga tidak melihat teks
`number is not divisible by 4, 3, or 2` dari blok `else`. Itu karena Rust
hanya mengeksekusi blok untuk kondisi `true` pertama yang ditemukan; setelah
menemukannya, Rust tidak lagi memeriksa sisanya.

Terlalu banyak ekspresi `else if` bisa membuat kode kamu berantakan, jadi
kalau punya lebih dari satu, sebaiknya refactor kode kamu. Bab 6 menjelaskan
konstruksi bercabang Rust yang kuat bernama `match` untuk kasus seperti ini.

#### Menggunakan `if` dalam Statement `let`

Karena `if` adalah ekspresi, kita bisa menggunakannya di sisi kanan sebuah
statement `let` untuk menetapkan hasilnya ke sebuah variabel, seperti pada
Listing 3-2.

<Listing number="3-2" file-name="src/main.rs" caption="Menetapkan hasil ekspresi `if` ke sebuah variabel">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-02/src/main.rs}}
```

</Listing>

Variabel `number` akan terikat ke sebuah nilai berdasarkan hasil ekspresi
`if`. Jalankan kode ini untuk melihat apa yang terjadi:

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-02/output.txt}}
```

Ingat bahwa sebuah blok kode bernilai berupa ekspresi terakhir di dalamnya, dan
angka pun juga merupakan ekspresi. Pada kasus ini, nilai dari seluruh ekspresi
`if` tergantung pada blok kode mana yang dieksekusi. Artinya, nilai-nilai yang
berpotensi menjadi hasil dari setiap arm pada `if` harus bertipe sama; pada
Listing 3-2, hasil arm `if` dan arm `else` sama-sama integer `i32`. Jika
tipenya tidak cocok, seperti pada contoh berikut, kita akan mendapatkan error:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/src/main.rs}}
```

Ketika kita mencoba mengompilasi kode ini, kita akan mendapatkan error. Arm
`if` dan `else` bertipe nilai yang tidak kompatibel, dan Rust menunjukkan
dengan tepat di mana masalahnya berada dalam program:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/output.txt}}
```

Ekspresi di blok `if` bernilai sebuah integer, sedangkan ekspresi di blok
`else` bernilai sebuah string. Ini tidak akan bekerja, karena sebuah variabel
harus bertipe tunggal, dan Rust perlu mengetahui secara pasti saat kompilasi
tipe apa yang dimiliki variabel `number`. Dengan mengetahui tipe `number`,
compiler bisa memverifikasi bahwa tipe itu valid di setiap tempat kita
menggunakannya. Rust tidak akan bisa melakukan itu jika tipe `number` hanya
ditentukan saat runtime; compiler akan menjadi lebih rumit dan memberikan
jaminan yang lebih sedikit tentang kode jika harus melacak banyak tipe
hipotetis untuk setiap variabel.

### Pengulangan dengan Loop

Sering kali berguna untuk mengeksekusi sebuah blok kode lebih dari sekali.
Untuk tugas ini, Rust menyediakan beberapa _loop_, yang akan menjalankan kode
di dalam loop body sampai akhir, lalu langsung mulai lagi dari awal. Untuk
bereksperimen dengan loop, mari kita buat proyek baru bernama _loops_.

Rust punya tiga jenis loop: `loop`, `while`, dan `for`. Mari kita coba satu
per satu.

#### Mengulang Kode dengan `loop`

Keyword `loop` memberi tahu Rust untuk mengeksekusi sebuah blok kode
berulang-ulang, entah selamanya atau sampai kamu secara eksplisit menyuruhnya
berhenti.

Sebagai contoh, ubah file _src/main.rs_ di direktori _loops_ kamu menjadi
seperti berikut:

<span class="filename">Filename: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-loop/src/main.rs}}
```

Saat kita menjalankan program ini, kita akan melihat `again!` tercetak
terus-menerus sampai kita menghentikan program secara manual. Sebagian besar
terminal mendukung shortcut keyboard <kbd>ctrl</kbd>-<kbd>C</kbd> untuk
memutus program yang terjebak dalam loop tanpa henti. Coba saja:

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-32-loop
cargo run
CTRL-C
-->

```console
$ cargo run
   Compiling loops v0.1.0 (file:///projects/loops)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.08s
     Running `target/debug/loops`
again!
again!
again!
again!
^Cagain!
```

Simbol `^C` menunjukkan posisi di mana kamu menekan <kbd>ctrl</kbd>-<kbd>C</kbd>.

Kamu mungkin melihat, mungkin juga tidak, kata `again!` tercetak setelah `^C`,
tergantung pada posisi kode dalam loop saat menerima sinyal interrupt.

Untungnya, Rust juga menyediakan cara untuk keluar dari loop menggunakan kode.
Kamu bisa menempatkan keyword `break` di dalam loop untuk memberi tahu program
kapan harus berhenti mengeksekusi loop. Ingat bahwa kita melakukan ini dalam
permainan tebak-tebakan di bagian [“Keluar Setelah Tebakan yang
Benar”][quitting-after-a-correct-guess]<!-- ignore --> di Bab 2 untuk keluar
dari program saat pengguna memenangkan permainan dengan menebak angka yang
benar.

Kita juga menggunakan `continue` dalam permainan tebak-tebakan; dalam loop,
`continue` memberi tahu program untuk melewati sisa kode pada iterasi loop ini
dan lanjut ke iterasi berikutnya.

#### Mengembalikan Nilai dari Loop

Salah satu kegunaan `loop` adalah mencoba ulang operasi yang kamu tahu mungkin
gagal, seperti memeriksa apakah sebuah thread sudah menyelesaikan tugasnya.
Kamu mungkin juga perlu mengeluarkan hasil operasi itu dari loop agar bisa
dipakai oleh sisa kode kamu. Untuk melakukannya, tambahkan nilai yang ingin
kamu kembalikan setelah ekspresi `break` yang kamu gunakan untuk menghentikan
loop; nilai itu akan dikembalikan keluar dari loop sehingga kamu bisa
menggunakannya, seperti ini:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-33-return-value-from-loop/src/main.rs}}
```

Sebelum loop, kita mendeklarasikan variabel bernama `counter` dan
menginisialisasinya dengan `0`. Lalu, kita mendeklarasikan variabel bernama
`result` untuk menyimpan nilai yang dikembalikan dari loop. Pada setiap iterasi
loop, kita menambahkan `1` ke variabel `counter`, lalu memeriksa apakah
`counter` sama dengan `10`. Jika ya, kita menggunakan keyword `break` dengan
nilai `counter * 2`. Setelah loop, kita menggunakan titik koma untuk mengakhiri
statement yang menetapkan nilai ke `result`. Terakhir, kita mencetak nilai
dalam `result`, yang pada kasus ini adalah `20`.

Kamu juga bisa `return` dari dalam loop. `break` hanya keluar dari loop saat
ini, sedangkan `return` selalu keluar dari fungsi saat ini.

<!-- Old headings. Do not remove or links may break. -->
<a id="loop-labels-to-disambiguate-between-multiple-loops"></a>

#### Membedakan dengan Loop Label

Jika kamu punya loop di dalam loop, `break` dan `continue` berlaku untuk loop
terdalam pada titik itu. Kamu bisa secara opsional memberi _loop label_ pada
sebuah loop, lalu menggunakannya bersama `break` atau `continue` untuk
menentukan bahwa keyword itu berlaku pada loop berlabel tersebut, bukan loop
terdalam. Loop label harus diawali kutip satu. Berikut contohnya dengan dua
loop bersarang:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/src/main.rs}}
```

Loop luar punya label `'counting_up`, dan akan menghitung naik dari 0 ke 2.
Loop dalam tanpa label menghitung turun dari 10 ke 9. `break` pertama yang
tidak menyebut label hanya akan keluar dari loop dalam. Statement
`break 'counting_up;` akan keluar dari loop luar. Kode ini mencetak:

```console
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/output.txt}}
```

<!-- Old headings. Do not remove or links may break. -->
<a id="conditional-loops-with-while"></a>

#### Menyederhanakan Loop Kondisional dengan while

Sering kali sebuah program perlu mengevaluasi sebuah kondisi di dalam loop.
Selama kondisi bernilai `true`, loop berjalan. Ketika kondisi tidak lagi
`true`, program memanggil `break` dan menghentikan loop. Perilaku seperti ini
bisa diimplementasikan dengan menggabungkan `loop`, `if`, `else`, dan `break`;
kamu boleh mencobanya sekarang dalam sebuah program kalau mau. Namun, pola ini
begitu umum sehingga Rust punya konstruksi bawaan dalam bahasanya untuk ini,
yaitu loop `while`. Pada Listing 3-3, kita menggunakan `while` untuk
menjalankan program tiga kali dengan hitungan mundur setiap kali, lalu setelah
loop, mencetak sebuah pesan dan keluar.

<Listing number="3-3" file-name="src/main.rs" caption="Menggunakan loop `while` untuk menjalankan kode selama kondisi bernilai `true`">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-03/src/main.rs}}
```

</Listing>

Konstruksi ini menghilangkan banyak nesting yang akan diperlukan jika kamu
memakai `loop`, `if`, `else`, dan `break`, dan hasilnya lebih jelas. Selama
kondisi bernilai `true`, kode berjalan; jika tidak, kode keluar dari loop.

<a id="looping-through-a-collection-with-for"></a>
#### Mengulang Melalui Koleksi dengan `for`

Kamu bisa memilih memakai konstruksi `while` untuk mengulang elemen-elemen
sebuah koleksi, seperti array. Sebagai contoh, loop pada Listing 3-4 mencetak
setiap elemen dalam array `a`.

<Listing number="3-4" file-name="src/main.rs" caption="Mengulang setiap elemen sebuah koleksi menggunakan loop `while`">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-04/src/main.rs}}
```

</Listing>

Di sini, kode menghitung naik melalui elemen-elemen dalam array. Kode mulai
dari indeks `0`, lalu berloop sampai mencapai indeks terakhir dalam array
(yaitu, ketika `index < 5` tidak lagi `true`). Menjalankan kode ini akan
mencetak setiap elemen dalam array:

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-04/output.txt}}
```

Kelima nilai array muncul di terminal, sesuai harapan. Meskipun `index` akan
mencapai nilai `5` pada suatu saat, loop berhenti mengeksekusi sebelum sempat
mengambil nilai keenam dari array.

Namun, pendekatan ini rawan error; kita bisa membuat program panic jika nilai
indeks atau kondisi ujinya salah. Sebagai contoh, jika kamu mengubah definisi
array `a` menjadi empat elemen tetapi lupa memperbarui kondisinya menjadi
`while index < 4`, kode akan panic. Pendekatan ini juga lambat, karena
compiler menambahkan kode runtime untuk melakukan pengecekan kondisional
apakah indeks masih dalam batas array pada setiap iterasi loop.

Sebagai alternatif yang lebih ringkas, kamu bisa memakai loop `for` dan
mengeksekusi kode untuk setiap item dalam sebuah koleksi. Loop `for` terlihat
seperti kode pada Listing 3-5.

<Listing number="3-5" file-name="src/main.rs" caption="Mengulang setiap elemen sebuah koleksi menggunakan loop `for`">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-05/src/main.rs}}
```

</Listing>

Saat kita menjalankan kode ini, kita akan melihat output yang sama seperti pada
Listing 3-4. Lebih penting lagi, kita kini meningkatkan keamanan kode dan
menghilangkan kemungkinan bug yang muncul karena melewati akhir array atau
berhenti terlalu cepat sehingga melewatkan beberapa item. Kode mesin yang
dihasilkan loop `for` juga bisa lebih efisien karena indeks tidak perlu
dibandingkan dengan panjang array pada setiap iterasi.

Dengan loop `for`, kamu tidak perlu ingat mengubah kode lain jika mengubah
jumlah nilai dalam array, seperti yang harus kamu lakukan dengan metode pada
Listing 3-4.

Sifat aman dan ringkas loop `for` menjadikannya konstruksi loop yang paling
umum dipakai di Rust. Bahkan dalam situasi di mana kamu ingin menjalankan kode
tertentu sejumlah kali, seperti contoh hitungan mundur dengan loop `while` pada
Listing 3-3, kebanyakan Rustacean akan memakai loop `for`. Caranya adalah
dengan memakai `Range` yang disediakan standard library, yang menghasilkan
semua angka berurutan mulai dari satu angka dan berhenti sebelum angka lain.

Begini tampilan hitungan mundur tersebut menggunakan loop `for` dan metode lain
yang belum kita bahas, `rev`, untuk membalik range:

<span class="filename">Filename: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-34-for-range/src/main.rs}}
```

Kode ini sedikit lebih rapi, bukan?

## Ringkasan

Kamu berhasil! Ini bab yang cukup besar: kamu sudah belajar tentang variabel,
tipe data skalar dan komposit, fungsi, komentar, ekspresi `if`, dan loop! Untuk
mempraktikkan konsep yang dibahas di bab ini, coba buat program untuk melakukan
hal berikut:

- Mengonversi suhu antara Fahrenheit dan Celsius.
- Menghasilkan bilangan Fibonacci ke-*n*.
- Mencetak lirik lagu Natal “The Twelve Days of Christmas,” dengan
  memanfaatkan pengulangan dalam lagu itu.

Kalau kamu siap lanjut, kita akan membahas konsep Rust yang _tidak_ umum ada
di bahasa pemrograman lain: *ownership*.

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[quitting-after-a-correct-guess]: ch02-00-guessing-game-tutorial.html#quitting-after-a-correct-guess
