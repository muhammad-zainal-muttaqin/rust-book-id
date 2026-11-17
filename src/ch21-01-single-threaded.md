## Membangun Server Web Single-Threaded

Kita akan mulai dengan membuat server web single-threaded yang berfungsi. Sebelum mulai, kita lihat dulu sekilas gambaran tentang protokol-protokol yang terlibat dalam membangun server web. Detail dari protokol-protokol ini berada di luar cakupan buku ini, tetapi gambaran singkatnya akan memberi kamu informasi yang dibutuhkan.

Dua protokol utama yang terlibat dalam server web adalah _Hypertext Transfer Protocol_ _(HTTP)_ dan _Transmission Control Protocol_ _(TCP)_. Keduanya adalah protokol _request-response_, artinya _client_ memulai request dan _server_ mendengarkan request tersebut lalu memberikan response kepada client. Isi dari request dan response itu ditentukan oleh protokol-protokol tersebut.

TCP adalah protokol level rendah yang menjelaskan detail bagaimana informasi berpindah dari satu server ke server lain, tetapi tidak menentukan apa informasi itu. HTTP dibangun di atas TCP dengan mendefinisikan isi dari request dan response. Secara teknis mungkin saja menggunakan HTTP dengan protokol lain, tetapi dalam mayoritas kasus, HTTP mengirim datanya melalui TCP. Kita akan bekerja dengan byte-byte mentah dari request dan response TCP dan HTTP.

### Mendengarkan Koneksi TCP

Server web kita perlu mendengarkan koneksi TCP, jadi itu akan jadi bagian pertama yang kita kerjakan. Pustaka standar menyediakan module `std::net` yang memungkinkan kita melakukan ini. Mari buat proyek baru seperti biasa:

```console
$ cargo new hello
     Created binary (application) `hello` project
$ cd hello
```

Sekarang masukkan kode pada Listing 21-1 ke dalam _src/main.rs_ untuk memulai. Kode ini akan mendengarkan alamat lokal `127.0.0.1:7878` untuk menerima TCP stream yang masuk. Saat mendapat stream yang masuk, kode ini akan mencetak `Connection established!`.

<Listing number="21-1" file-name="src/main.rs" caption="Mendengarkan stream yang masuk dan mencetak pesan saat kita menerima stream">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-01/src/main.rs}}
```

</Listing>

Dengan `TcpListener`, kita bisa mendengarkan koneksi TCP di alamat `127.0.0.1:7878`. Pada alamat itu, bagian sebelum titik dua adalah alamat IP yang mewakili komputermu (ini sama di setiap komputer dan tidak secara khusus mewakili komputer para penulis), dan `7878` adalah port. Kita memilih port ini karena dua alasan: HTTP biasanya tidak diterima di port ini, jadi server kita kecil kemungkinannya bentrok dengan server web lain yang mungkin kamu jalankan di mesinmu, dan 7878 adalah _rust_ yang diketik di telepon.

Fungsi `bind` dalam kasus ini bekerja seperti fungsi `new`, yaitu mengembalikan instance `TcpListener` baru. Fungsi ini disebut `bind` karena, dalam jaringan, terhubung ke port untuk didengarkan dikenal sebagai "binding to a port."

Fungsi `bind` mengembalikan `Result<T, E>`, yang menunjukkan bahwa binding bisa gagal, misalnya jika kita menjalankan dua instance program sehingga ada dua program yang mendengarkan port yang sama. Karena kita menulis server dasar hanya untuk belajar, kita tidak akan repot menangani error seperti ini; sebagai gantinya, kita menggunakan `unwrap` untuk menghentikan program jika terjadi error.

Method `incoming` pada `TcpListener` mengembalikan iterator yang memberi kita urutan stream (lebih tepatnya, stream bertipe `TcpStream`). Sebuah _stream_ mewakili satu koneksi terbuka antara client dan server. _Connection_ adalah nama untuk keseluruhan proses request dan response di mana client terhubung ke server, server menghasilkan response, lalu server menutup koneksi. Dengan demikian, kita akan membaca dari `TcpStream` untuk melihat apa yang dikirim client, lalu menulis response kita ke stream tersebut untuk mengirim data kembali ke client. Secara keseluruhan, loop `for` ini akan memproses setiap koneksi bergiliran dan menghasilkan serangkaian stream untuk kita tangani.

Untuk sementara, penanganan stream kita hanya terdiri dari memanggil `unwrap` untuk menghentikan program jika stream mengalami error; jika tidak ada error, program mencetak pesan. Kita akan menambahkan fungsionalitas lebih untuk kasus sukses di listing berikutnya. Alasan kita bisa menerima error dari method `incoming` saat client terhubung ke server adalah kita sebenarnya tidak melakukan iterasi atas koneksi. Sebaliknya, kita melakukan iterasi atas _connection attempts_ (percobaan koneksi). Koneksi bisa gagal karena berbagai alasan, banyak di antaranya spesifik sesuai sistem operasi. Misalnya, banyak sistem operasi membatasi jumlah koneksi terbuka simultan yang bisa mereka dukung; percobaan koneksi baru di atas jumlah itu akan menghasilkan error sampai sebagian koneksi terbuka ditutup.

Coba jalankan kode ini! Panggil `cargo run` di terminal, lalu buka _127.0.0.1:7878_ di browser web. Browser seharusnya menampilkan pesan error seperti "Connection reset" karena server saat ini tidak mengirimkan data apa pun. Tetapi saat kamu melihat terminal, kamu seharusnya melihat beberapa pesan yang dicetak saat browser terhubung ke server!

```text
     Running `target/debug/hello`
Connection established!
Connection established!
Connection established!
```

Terkadang kamu akan melihat beberapa pesan tercetak untuk satu request browser; alasannya bisa jadi browser sedang membuat request untuk halaman sekaligus request untuk sumber daya lain, seperti ikon _favicon.ico_ yang muncul di tab browser.

Bisa juga browser mencoba terhubung ke server berkali-kali karena server tidak merespons dengan data apa pun. Saat `stream` keluar dari scope dan di-drop di akhir loop, koneksi ditutup sebagai bagian dari implementasi `drop`. Browser kadang mengatasi koneksi yang tertutup dengan mencoba lagi, karena masalahnya mungkin bersifat sementara.

Browser juga kadang membuka beberapa koneksi ke server tanpa mengirim request apa pun, supaya jika mereka *memang* nanti mengirim request, request itu bisa berjalan lebih cepat. Saat ini terjadi, server kita akan melihat setiap koneksi, terlepas dari apakah ada request melalui koneksi itu atau tidak. Banyak versi browser berbasis Chrome melakukan ini, misalnya; kamu bisa menonaktifkan optimasi itu dengan memakai mode penjelajahan pribadi atau browser lain.

Yang penting adalah kita berhasil mendapatkan handle ke sebuah koneksi TCP!

Ingat untuk menghentikan program dengan menekan <kbd>ctrl</kbd>-<kbd>C</kbd> setelah selesai menjalankan suatu versi kode. Lalu, jalankan ulang program dengan memanggil perintah `cargo run` setelah setiap kali kamu mengubah kode, supaya kamu memang menjalankan kode yang terbaru.

### Membaca Request

Mari terapkan fungsionalitas untuk membaca request dari browser! Supaya terpisah antara urusan mendapatkan koneksi terlebih dahulu lalu melakukan sesuatu dengan koneksi itu, kita akan membuat fungsi baru untuk memproses koneksi. Dalam fungsi `handle_connection` yang baru ini, kita akan membaca data dari TCP stream dan mencetaknya agar kita bisa melihat data yang dikirim dari browser. Ubah kode menjadi seperti Listing 21-2.

<Listing number="21-2" file-name="src/main.rs" caption="Membaca dari `TcpStream` dan mencetak datanya">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-02/src/main.rs}}
```

</Listing>

Kita memasukkan `std::io::BufReader` dan `std::io::prelude` ke dalam scope untuk mendapatkan akses ke trait dan tipe yang memungkinkan kita membaca dan menulis ke stream. Di loop `for` dalam fungsi `main`, alih-alih mencetak pesan bahwa kita telah membuat koneksi, sekarang kita memanggil fungsi `handle_connection` yang baru dan meneruskan `stream` kepadanya.

Dalam fungsi `handle_connection`, kita membuat instance `BufReader` baru yang membungkus reference ke `stream`. `BufReader` menambahkan buffering dengan mengelola pemanggilan method trait `std::io::Read` untuk kita.

Kita membuat variabel bernama `http_request` untuk mengumpulkan baris-baris request yang dikirim browser ke server kita. Kita menandakan bahwa kita ingin mengumpulkan baris-baris ini dalam vector dengan menambahkan anotasi tipe `Vec<_>`.

`BufReader` mengimplementasikan trait `std::io::BufRead`, yang menyediakan method `lines`. Method `lines` mengembalikan iterator dari `Result<String, std::io::Error>` dengan membelah aliran data setiap kali menemukan byte baris baru. Untuk mendapatkan setiap `String`, kita `map` dan `unwrap` setiap `Result`. `Result` bisa berupa error jika datanya bukan UTF-8 yang valid atau jika ada masalah saat membaca dari stream. Sekali lagi, program produksi sebaiknya menangani error ini dengan lebih baik, tetapi kita memilih menghentikan program saat terjadi error demi kesederhanaan.

Browser menandai akhir dari request HTTP dengan mengirim dua karakter baris baru berturut-turut, jadi untuk mendapatkan satu request dari stream, kita mengambil baris sampai kita mendapat baris yang berupa string kosong. Setelah baris-baris itu terkumpul di vector, kita mencetaknya dengan format debug yang rapi agar bisa melihat instruksi yang dikirim browser web ke server kita.

Coba kode ini! Jalankan program dan buat request lagi di browser web. Perhatikan bahwa kita tetap akan mendapat halaman error di browser, tetapi keluaran program kita di terminal sekarang akan terlihat seperti ini:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-02
cargo run
make a request to 127.0.0.1:7878
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.42s
     Running `target/debug/hello`
Request: [
    "GET / HTTP/1.1",
    "Host: 127.0.0.1:7878",
    "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language: en-US,en;q=0.5",
    "Accept-Encoding: gzip, deflate, br",
    "DNT: 1",
    "Connection: keep-alive",
    "Upgrade-Insecure-Requests: 1",
    "Sec-Fetch-Dest: document",
    "Sec-Fetch-Mode: navigate",
    "Sec-Fetch-Site: none",
    "Sec-Fetch-User: ?1",
    "Cache-Control: max-age=0",
]
```

Tergantung browser yang kamu pakai, kamu mungkin mendapat keluaran yang sedikit berbeda. Sekarang kita mencetak data request, kita bisa melihat mengapa kita mendapat beberapa koneksi dari satu request browser dengan melihat path setelah `GET` di baris pertama request. Jika koneksi-koneksi berulang itu semuanya meminta _/_, kita tahu browser mencoba mengambil _/_ berulang kali karena tidak mendapat response dari program kita.

Mari kita bedah data request ini untuk memahami apa yang diminta browser kepada program kita.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-closer-look-at-an-http-request"></a>
<a id="looking-closer-at-an-http-request"></a>

### Melihat Lebih Dekat Request HTTP

HTTP adalah protokol berbasis teks, dan sebuah request memiliki format ini:

```text
Method Request-URI HTTP-Version CRLF
headers CRLF
message-body
```

Baris pertama adalah _request line_ yang berisi informasi tentang apa yang diminta client. Bagian pertama dari request line menunjukkan method yang digunakan, seperti `GET` atau `POST`, yang menjelaskan bagaimana client membuat request ini. Client kita menggunakan request `GET`, yang berarti ia meminta informasi.

Bagian berikutnya dari request line adalah _/_, yang menunjukkan _uniform resource identifier_ _(URI)_ yang diminta client: URI hampir, tetapi tidak persis, sama dengan _uniform resource locator_ _(URL)_. Perbedaan antara URI dan URL tidak penting untuk keperluan kita di bab ini, tetapi spesifikasi HTTP menggunakan istilah _URI_, jadi kita bisa saja menggantinya dalam pikiran dengan _URL_ di sini.

Bagian terakhir adalah versi HTTP yang digunakan client, lalu request line diakhiri dengan urutan CRLF. (_CRLF_ adalah singkatan dari _carriage return_ dan _line feed_, istilah-istilah dari zaman mesin tik!) Urutan CRLF juga bisa ditulis sebagai `\r\n`, di mana `\r` adalah carriage return dan `\n` adalah line feed. _CRLF sequence_ memisahkan request line dari sisa data request. Perhatikan bahwa saat CRLF dicetak, kita melihat baris baru dimulai, bukan `\r\n`.

Melihat data request line yang kita terima dari menjalankan program sejauh ini, kita melihat bahwa `GET` adalah method, _/_ adalah URI request, dan `HTTP/1.1` adalah versinya.

Setelah request line, baris-baris sisanya yang dimulai dari `Host:` dan seterusnya adalah header. Request `GET` tidak memiliki body.

Coba buat request dari browser lain atau minta alamat yang berbeda, seperti _127.0.0.1:7878/test_, untuk melihat bagaimana data request berubah.

Sekarang kita tahu apa yang diminta browser, mari kirimkan beberapa data kembali!

### Menulis Response

Kita akan menerapkan pengiriman data sebagai response terhadap request client. Response memiliki format berikut:

```text
HTTP-Version Status-Code Reason-Phrase CRLF
headers CRLF
message-body
```

Baris pertama adalah _status line_ yang berisi versi HTTP yang digunakan dalam response, kode status numerik yang merangkum hasil request, dan reason phrase yang memberikan deskripsi teks dari kode status tersebut. Setelah urutan CRLF ada header-header (jika ada), urutan CRLF lagi, lalu body dari response.

Berikut adalah contoh response yang menggunakan HTTP versi 1.1 dengan kode status 200, reason phrase OK, tanpa header, dan tanpa body:

```text
HTTP/1.1 200 OK\r\n\r\n
```

Kode status 200 adalah response sukses standar. Teks itu adalah response HTTP sukses yang sangat kecil. Mari tulis ini ke stream sebagai response kita terhadap request yang berhasil! Dari fungsi `handle_connection`, hapus `println!` yang mencetak data request dan ganti dengan kode pada Listing 21-3.

<Listing number="21-3" file-name="src/main.rs" caption="Menulis response HTTP sukses yang kecil ke stream">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-03/src/main.rs:here}}
```

</Listing>

Baris baru pertama mendefinisikan variabel `response` yang menyimpan data pesan sukses. Lalu, kita memanggil `as_bytes` pada `response` untuk mengubah data string menjadi byte. Method `write_all` pada `stream` menerima `&[u8]` dan mengirim byte-byte itu langsung melalui koneksi. Karena operasi `write_all` bisa gagal, kita menggunakan `unwrap` pada hasil error seperti sebelumnya. Sekali lagi, dalam aplikasi nyata, kamu akan menambahkan penanganan error di sini.

Dengan perubahan ini, mari jalankan kode kita dan buat request. Kita tidak lagi mencetak data apa pun ke terminal, jadi kita tidak akan melihat keluaran selain keluaran dari Cargo. Saat kamu membuka _127.0.0.1:7878_ di browser web, kamu seharusnya mendapat halaman kosong, bukan error. Kamu baru saja menulis secara manual penerimaan request HTTP dan pengiriman response!

### Mengembalikan HTML Sungguhan

Mari terapkan fungsionalitas untuk mengembalikan lebih dari sekadar halaman kosong. Buat file baru _hello.html_ di direktori root proyekmu, bukan di direktori _src_. Kamu bisa memasukkan HTML apa pun yang kamu mau; Listing 21-4 menunjukkan salah satu pilihan.

<Listing number="21-4" file-name="hello.html" caption="Contoh file HTML untuk dikembalikan dalam response">

```html
{{#include ../listings/ch21-web-server/listing-21-05/hello.html}}
```

</Listing>

Ini adalah dokumen HTML5 minimal dengan sebuah heading dan beberapa teks. Untuk mengembalikannya dari server saat sebuah request diterima, kita akan memodifikasi `handle_connection` seperti ditunjukkan pada Listing 21-5 untuk membaca file HTML, menambahkannya ke response sebagai body, lalu mengirimnya.

<Listing number="21-5" file-name="src/main.rs" caption="Mengirim isi *hello.html* sebagai body dari response">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-05/src/main.rs:here}}
```

</Listing>

Kita telah menambahkan `fs` ke pernyataan `use` untuk memasukkan module filesystem dari pustaka standar ke dalam scope. Kode untuk membaca isi file menjadi string seharusnya terasa akrab; kita menggunakannya saat membaca isi file untuk proyek I/O kita di Listing 12-4.

Berikutnya, kita menggunakan `format!` untuk menambahkan isi file sebagai body dari response sukses. Untuk memastikan response HTTP yang valid, kita menambahkan header `Content-Length`, yang diatur sebesar ukuran body response kita—dalam hal ini, ukuran dari `hello.html`.

Jalankan kode ini dengan `cargo run` dan buka _127.0.0.1:7878_ di browser; kamu seharusnya melihat HTML-mu tampil!

Saat ini, kita mengabaikan data request di `http_request` dan hanya mengirim isi file HTML tanpa syarat. Artinya jika kamu mencoba meminta _127.0.0.1:7878/something-else_ di browser, kamu tetap akan mendapat response HTML yang sama. Saat ini server kita sangat terbatas dan tidak melakukan apa yang dilakukan kebanyakan server web. Kita ingin menyesuaikan response bergantung pada request dan hanya mengirim balik file HTML untuk request yang well-formed ke _/_.

### Memvalidasi Request dan Merespons Secara Selektif

Saat ini, server web kita akan mengembalikan HTML dalam file itu apa pun yang diminta client. Mari tambahkan fungsionalitas untuk memeriksa apakah browser meminta _/_ sebelum mengembalikan file HTML, dan mengembalikan error jika browser meminta hal lain. Untuk ini kita perlu memodifikasi `handle_connection`, seperti ditunjukkan pada Listing 21-6. Kode baru ini memeriksa isi request yang diterima terhadap apa yang kita tahu tentang bentuk request ke _/_, dan menambahkan blok `if` dan `else` untuk memperlakukan request secara berbeda.

<Listing number="21-6" file-name="src/main.rs" caption="Menangani request ke */* secara berbeda dari request lain">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-06/src/main.rs:here}}
```

</Listing>

Kita hanya akan melihat baris pertama dari request HTTP, jadi alih-alih membaca seluruh request ke dalam vector, kita memanggil `next` untuk mendapatkan item pertama dari iterator. `unwrap` pertama menangani `Option` dan menghentikan program jika iterator tidak punya item. `unwrap` kedua menangani `Result` dan memiliki efek yang sama seperti `unwrap` yang ada di `map` yang ditambahkan di Listing 21-2.

Berikutnya, kita memeriksa `request_line` untuk melihat apakah sama dengan request line dari request GET ke path _/_. Jika ya, blok `if` mengembalikan isi file HTML kita.

Jika `request_line` _tidak_ sama dengan request GET ke path _/_, itu berarti kita menerima request lain. Kita akan menambahkan kode ke blok `else` sebentar lagi untuk merespons semua request lainnya.

Jalankan kode ini sekarang dan minta _127.0.0.1:7878_; kamu seharusnya mendapat HTML dari _hello.html_. Jika kamu membuat request lain, seperti _127.0.0.1:7878/something-else_, kamu akan mendapat error koneksi seperti yang kamu lihat saat menjalankan kode di Listing 21-1 dan Listing 21-2.

Sekarang mari tambahkan kode pada Listing 21-7 ke blok `else` untuk mengembalikan response dengan kode status 404, yang menandakan bahwa konten untuk request tidak ditemukan. Kita juga akan mengembalikan HTML untuk sebuah halaman yang ditampilkan di browser guna menunjukkan response tersebut kepada pengguna akhir.

<Listing number="21-7" file-name="src/main.rs" caption="Merespons dengan kode status 404 dan halaman error jika yang diminta selain */*">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-07/src/main.rs:here}}
```

</Listing>

Di sini, response kita memiliki status line dengan kode status 404 dan reason phrase `NOT FOUND`. Body dari response akan berupa HTML dalam file _404.html_. Kamu perlu membuat file _404.html_ di samping _hello.html_ untuk halaman error ini; sekali lagi, silakan pakai HTML apa pun yang kamu mau, atau gunakan contoh HTML di Listing 21-8.

<Listing number="21-8" file-name="404.html" caption="Contoh isi halaman untuk dikirim bersama response 404 apa pun">

```html
{{#include ../listings/ch21-web-server/listing-21-07/404.html}}
```

</Listing>

Dengan perubahan ini, jalankan servermu lagi. Meminta _127.0.0.1:7878_ seharusnya mengembalikan isi _hello.html_, dan request lain apa pun, seperti _127.0.0.1:7878/foo_, seharusnya mengembalikan HTML error dari _404.html_.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-touch-of-refactoring"></a>

### Refactoring

Saat ini, blok `if` dan `else` memiliki banyak pengulangan: keduanya sama-sama membaca file dan menulis isi file ke stream. Satu-satunya perbedaan adalah status line dan nama file. Mari buat kode lebih ringkas dengan memindahkan perbedaan itu ke baris-baris `if` dan `else` terpisah yang akan menetapkan nilai status line dan nama file ke variabel; lalu kita bisa memakai variabel itu tanpa syarat dalam kode untuk membaca file dan menulis response. Listing 21-9 menunjukkan kode hasilnya setelah blok `if` dan `else` yang besar diganti.

<Listing number="21-9" file-name="src/main.rs" caption="Me-refactor blok `if` dan `else` agar hanya berisi kode yang berbeda antara kedua kasus">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-09/src/main.rs:here}}
```

</Listing>

Sekarang blok `if` dan `else` hanya mengembalikan nilai yang sesuai untuk status line dan nama file dalam sebuah tuple; lalu kita memakai destructuring untuk menetapkan kedua nilai itu ke `status_line` dan `filename` menggunakan pattern di pernyataan `let`, seperti yang dibahas di Bab 19.

Kode yang sebelumnya duplikat sekarang berada di luar blok `if` dan `else` serta memakai variabel `status_line` dan `filename`. Ini membuat perbedaan antara kedua kasus lebih mudah dilihat, dan berarti kita hanya punya satu tempat untuk mengubah kode jika ingin mengubah cara pembacaan file dan penulisan response. Perilaku kode di Listing 21-9 akan sama seperti di Listing 21-7.

Keren! Sekarang kita punya server web sederhana dalam sekitar 40 baris kode Rust yang merespons satu request dengan sebuah halaman konten dan merespons semua request lain dengan response 404.

Saat ini, server kita berjalan dalam satu thread, artinya ia hanya bisa melayani satu request pada satu waktu. Mari lihat bagaimana hal itu bisa menjadi masalah dengan menyimulasikan beberapa request yang lambat. Setelah itu, kita akan memperbaikinya supaya server kita bisa menangani beberapa request sekaligus.
