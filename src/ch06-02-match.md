<!-- Old headings. Do not remove or links may break. -->

<a id="the-match-control-flow-operator"></a>

<a id="the-match-control-flow-construct"></a>
## Konstruksi Alur Kontrol `match`

Rust punya konstruksi alur kontrol yang sangat powerful bernama `match`,
yang memungkinkan kamu membandingkan sebuah nilai terhadap serangkaian
pattern lalu mengeksekusi kode berdasarkan pattern mana yang cocok. Pattern
bisa terdiri dari nilai literal, nama variabel, wildcard, dan banyak hal
lain; [Bab 19][ch19-00-patterns]<!-- ignore --> membahas semua jenis
pattern dan apa gunanya. Kekuatan `match` berasal dari ekspresivitas
pattern serta fakta bahwa compiler memastikan semua kemungkinan kasus sudah
ditangani.

Bayangkan sebuah ekspresi `match` seperti mesin penghitung koin: koin
meluncur di lintasan yang berlubang-lubang dengan berbagai ukuran, dan
setiap koin jatuh lewat lubang pertama yang muat baginya. Begitu pula
dengan nilai: nilai melewati setiap pattern dalam sebuah `match`, dan pada
pattern pertama yang “muat,” nilai itu jatuh ke blok kode terkait untuk
dipakai saat eksekusi.

Soal koin, mari kita gunakan koin sebagai contoh penggunaan `match`! Kita
bisa menulis fungsi yang menerima koin AS yang jenisnya tidak diketahui
dan, dengan cara mirip mesin penghitung tadi, menentukan jenis koin itu
serta mengembalikan nilainya dalam sen, seperti pada Listing 6-3.

<Listing number="6-3" caption="Sebuah enum dan ekspresi `match` yang memakai varian-varian enum tersebut sebagai pattern-nya">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-03/src/main.rs:here}}
```

</Listing>

Mari kita bedah `match` di fungsi `value_in_cents`. Pertama, kita menulis
kata kunci `match` diikuti sebuah ekspresi, yang dalam hal ini adalah nilai
`coin`. Ini tampak sangat mirip dengan ekspresi kondisional yang dipakai
bersama `if`, tapi ada perbedaan besar: dengan `if`, kondisi harus
menghasilkan nilai Boolean, sedangkan di sini bisa bertipe apa pun. Tipe
`coin` pada contoh ini adalah enum `Coin` yang kita definisikan di baris
pertama.

Berikutnya adalah arm-arm `match`. Sebuah arm terdiri atas dua bagian:
sebuah pattern dan beberapa kode. Arm pertama di sini punya pattern berupa
nilai `Coin::Penny`, lalu operator `=>` yang memisahkan pattern dengan kode
yang akan dijalankan. Kode di sini hanyalah nilai `1`. Setiap arm dipisahkan
dari arm berikutnya dengan koma.

Saat ekspresi `match` dieksekusi, ia membandingkan nilai hasil terhadap
pattern setiap arm, secara berurutan. Jika sebuah pattern cocok dengan
nilai, kode yang terkait dengan pattern itu dijalankan. Jika pattern tidak
cocok, eksekusi berlanjut ke arm berikutnya, mirip seperti pada mesin
penghitung koin. Kita boleh punya arm sebanyak yang kita butuhkan: pada
Listing 6-3, `match` kita punya empat arm.

Kode pada setiap arm adalah sebuah ekspresi, dan nilai hasil ekspresi pada
arm yang cocok itulah yang menjadi nilai kembalian untuk seluruh ekspresi
`match`.

Biasanya kita tidak memakai kurung kurawal jika kode arm-nya pendek, seperti
pada Listing 6-3 yang tiap arm hanya mengembalikan sebuah nilai. Jika kamu
ingin menjalankan beberapa baris kode dalam sebuah arm, kamu harus memakai
kurung kurawal, dan koma setelah arm itu menjadi opsional. Sebagai contoh,
kode berikut mencetak “Lucky penny!” setiap kali method dipanggil dengan
`Coin::Penny`, tapi tetap mengembalikan nilai terakhir dari blok, yaitu
`1`:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-08-match-arm-multiple-lines/src/main.rs:here}}
```

<a id="patterns-that-bind-to-values"></a>
### Pattern yang Mengikat ke Nilai

Fitur berguna lain dari arm `match` adalah kemampuannya mengikat ke
bagian-bagian nilai yang cocok dengan pattern. Dengan inilah kita bisa
mengekstrak nilai dari varian-varian enum.

Sebagai contoh, mari ubah salah satu varian enum kita agar menyimpan data
di dalamnya. Mulai tahun 1999 sampai 2008, Amerika Serikat mencetak koin
quarter dengan desain berbeda untuk masing-masing dari 50 negara bagian di
satu sisinya. Koin lain tidak punya desain negara bagian, jadi hanya
quarter yang punya nilai tambahan ini. Kita bisa menambahkan informasi ini
ke `enum` kita dengan mengubah varian `Quarter` agar memuat sebuah nilai
`UsState` yang tersimpan di dalamnya, seperti yang kita lakukan pada
Listing 6-4.

<Listing number="6-4" caption="Enum `Coin` yang varian `Quarter`-nya juga menyimpan sebuah nilai `UsState`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-04/src/main.rs:here}}
```

</Listing>

Bayangkan seorang teman sedang berusaha mengumpulkan semua 50 koin quarter
negara bagian. Sementara kita memisahkan kembalian menurut jenis koin, kita
juga akan menyebutkan nama negara bagian yang terkait dengan setiap quarter,
sehingga jika ada yang belum dimiliki teman kita, ia bisa menambahkannya ke
koleksinya.

Dalam ekspresi match untuk kode ini, kita menambahkan variabel bernama
`state` ke pattern yang cocok dengan nilai varian `Coin::Quarter`. Saat
sebuah `Coin::Quarter` cocok, variabel `state` akan mengikat ke nilai
negara bagian dari quarter tersebut. Lalu, kita bisa memakai `state` di kode
arm itu, seperti ini:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-09-variable-in-pattern/src/main.rs:here}}
```

Jika kita memanggil `value_in_cents(Coin::Quarter(UsState::Alaska))`, `coin`
akan bernilai `Coin::Quarter(UsState::Alaska)`. Saat kita membandingkan
nilai itu dengan tiap arm match, tidak ada yang cocok sampai kita mencapai
`Coin::Quarter(state)`. Saat itu, binding untuk `state` akan bernilai
`UsState::Alaska`. Binding itu lalu bisa kita pakai dalam ekspresi
`println!`, sehingga nilai negara bagian di dalam varian enum `Coin` untuk
`Quarter` berhasil kita ambil.

<!-- Old headings. Do not remove or links may break. -->

<a id="matching-with-optiont"></a>

### Pattern `match` pada `Option<T>`


Di bagian sebelumnya, kita ingin mengambil nilai `T` di dalam kasus `Some`
saat memakai `Option<T>`; kita juga bisa menangani `Option<T>` dengan
`match`, seperti yang kita lakukan pada enum `Coin`! Alih-alih membandingkan
koin, kita akan membandingkan varian-varian `Option<T>`, tapi cara kerja
ekspresi `match` tetap sama.

Katakanlah kita ingin menulis fungsi yang menerima sebuah `Option<i32>` dan,
jika ada nilai di dalamnya, menambahkan 1 ke nilai itu. Jika tidak ada
nilai di dalamnya, fungsi harus mengembalikan nilai `None` dan tidak
mencoba melakukan operasi apa pun.

Fungsi ini sangat mudah ditulis berkat `match`, dan akan tampak seperti
Listing 6-5.

<Listing number="6-5" caption="Fungsi yang memakai ekspresi `match` pada sebuah `Option<i32>`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:here}}
```

</Listing>

Mari kita telusuri eksekusi pertama `plus_one` lebih rinci. Saat kita
memanggil `plus_one(five)`, variabel `x` di badan `plus_one` akan bernilai
`Some(5)`. Lalu kita bandingkan nilai itu dengan tiap arm match:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

Nilai `Some(5)` tidak cocok dengan pattern `None`, jadi kita lanjut ke arm
berikutnya:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:second_arm}}
```

Apakah `Some(5)` cocok dengan `Some(i)`? Cocok! Varian kita sama. `i`
mengikat ke nilai yang terkandung dalam `Some`, sehingga `i` bernilai `5`.
Kode di arm match lalu dijalankan, jadi kita menambahkan 1 ke nilai `i` dan
membuat nilai `Some` baru yang berisi total `6`.

Kini pertimbangkan panggilan kedua `plus_one` pada Listing 6-5, di mana `x`
adalah `None`. Kita masuk ke `match` dan bandingkan dengan arm pertama:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

Cocok! Tidak ada nilai untuk ditambahkan, jadi program berhenti dan
mengembalikan nilai `None` di sisi kanan `=>`. Karena arm pertama yang
cocok, tidak ada arm lain yang dibandingkan.

Kombinasi `match` dan enum berguna dalam banyak situasi. Kamu akan sering
melihat pola ini dalam kode Rust: `match` terhadap sebuah enum, mengikat
sebuah variabel ke data di dalamnya, lalu mengeksekusi kode berdasarkan
data itu. Awalnya sedikit membingungkan, tapi begitu terbiasa, kamu akan
berharap semua bahasa punya hal seperti ini. Ini memang konsisten jadi
favorit para pengguna.

### Match Bersifat Ekshaustif

Ada satu aspek lain dari `match` yang perlu kita bahas: pattern pada
arm-armnya harus menutupi semua kemungkinan. Pertimbangkan versi fungsi
`plus_one` kita berikut ini, yang punya bug dan tidak akan mengompilasi:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/src/main.rs:here}}
```

Kita tidak menangani kasus `None`, jadi kode ini akan menyebabkan bug.
Untungnya, Rust tahu cara menangkap bug semacam ini. Jika kita mencoba
mengompilasi kode ini, kita akan mendapatkan error berikut:

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/output.txt}}
```

Rust tahu kita belum menutupi setiap kemungkinan kasus, dan bahkan tahu
pattern mana yang kita lupakan! Match di Rust bersifat _ekshaustif_: kita
harus menghabiskan setiap kemungkinan terakhir agar kode itu valid.
Terutama pada kasus `Option<T>`, saat Rust mencegah kita lupa menangani
kasus `None` secara eksplisit, Rust melindungi kita dari asumsi bahwa kita
punya nilai padahal bisa jadi kita punya null, sehingga kesalahan senilai
satu miliar dolar yang dibahas sebelumnya menjadi mustahil terjadi.

### Pattern Catch-All dan Placeholder `_`

Dengan enum, kita juga bisa mengambil tindakan khusus untuk beberapa nilai
tertentu, tapi untuk semua nilai lain mengambil satu tindakan default.
Bayangkan kita sedang membuat sebuah game di mana, jika kamu melempar angka
3 pada dadu, pemainmu tidak bergerak tapi malah mendapat topi baru yang
bagus. Jika melempar 7, pemain kehilangan topi bagus. Untuk semua nilai
lain, pemain bergerak sebanyak angka itu di papan permainan. Berikut sebuah
`match` yang mengimplementasikan logika itu, dengan hasil lemparan dadu
ditulis mati alih-alih nilai acak, dan semua logika lain direpresentasikan
sebagai fungsi tanpa badan karena mengimplementasikannya di luar cakupan
contoh ini:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-15-binding-catchall/src/main.rs:here}}
```

Pada dua arm pertama, pattern-nya adalah nilai literal `3` dan `7`. Untuk
arm terakhir yang menutupi semua kemungkinan nilai lain, pattern-nya
adalah variabel yang kita beri nama `other`. Kode yang dijalankan untuk arm
`other` memakai variabel itu dengan meneruskannya ke fungsi `move_player`.

Kode ini mengompilasi meskipun kita belum mendaftar semua nilai yang
mungkin dimiliki sebuah `u8`, karena pattern terakhir akan cocok dengan
semua nilai yang tidak disebutkan secara khusus. Pattern catch-all ini
memenuhi syarat bahwa `match` harus ekshaustif. Perhatikan bahwa kita harus
menaruh arm catch-all di akhir karena pattern dievaluasi secara berurutan.
Jika kita menaruh arm catch-all lebih awal, arm-arm lain tidak akan pernah
dijalankan, jadi Rust akan memberi peringatan jika kita menambahkan arm
setelah sebuah catch-all!

Rust juga punya pattern yang bisa kita pakai saat menginginkan catch-all
tapi tidak ingin _memakai_ nilai dalam pattern catch-all itu: `_` adalah
pattern khusus yang cocok dengan nilai apa pun dan tidak mengikat nilai
tersebut. Ini memberi tahu Rust bahwa kita tidak akan memakai nilai itu,
sehingga Rust tidak akan memperingatkan kita tentang variabel yang tidak
terpakai.

Kita ubah aturan permainannya: Sekarang, jika kamu melempar angka selain 3
atau 7, kamu harus melempar lagi. Kita tidak perlu lagi memakai nilai
catch-all, jadi kita bisa mengubah kode untuk memakai `_` alih-alih variabel
bernama `other`:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-16-underscore-catchall/src/main.rs:here}}
```

Contoh ini juga memenuhi syarat ekshaustif karena kita secara eksplisit
mengabaikan semua nilai lain pada arm terakhir; tidak ada yang kita
lupakan.

Terakhir, kita akan mengubah aturan permainan sekali lagi agar tidak terjadi
apa pun pada giliranmu jika kamu melempar angka selain 3 atau 7. Kita bisa
mengungkapkan hal itu dengan memakai nilai unit (tipe tuple kosong yang kita
sebutkan di bagian [“Tipe Tuple”][tuples]<!-- ignore -->) sebagai kode yang
menyertai arm `_`:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-17-underscore-unit/src/main.rs:here}}
```

Di sini, kita secara eksplisit memberi tahu Rust bahwa kita tidak akan
memakai nilai lain yang tidak cocok dengan pattern pada arm sebelumnya, dan
kita tidak ingin menjalankan kode apa pun pada kasus ini.

Masih banyak lagi tentang pattern dan pencocokan pola yang akan kita bahas
di [Bab 19][ch19-00-patterns]<!-- ignore -->. Untuk sekarang, kita lanjut
ke sintaks `if let`, yang bisa berguna saat ekspresi `match` terasa terlalu
bertele-tele.

[tuples]: ch03-02-data-types.html#the-tuple-type
[ch19-00-patterns]: ch19-00-patterns.html
