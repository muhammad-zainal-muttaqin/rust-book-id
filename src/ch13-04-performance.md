<!-- Old headings. Do not remove or links may break. -->

<a id="comparing-performance-loops-vs-iterators"></a>

## Performa pada Loop vs. Iterator

Untuk menentukan apakah sebaiknya memakai loop atau iterator, kamu perlu tahu implementasi mana yang lebih cepat: versi fungsi `search` dengan `for` loop eksplisit atau versi dengan iterator.

Kami menjalankan benchmark dengan memuat seluruh isi _The Adventures of Sherlock Holmes_ karya Sir Arthur Conan Doyle ke dalam sebuah `String`, lalu mencari kata _the_ di dalamnya. Berikut hasil benchmark untuk versi `search` yang memakai `for` loop dan versi yang memakai iterator:

```text
test bench_search_for  ... bench:  19,620,300 ns/iter (+/- 915,700)
test bench_search_iter ... bench:  19,234,900 ns/iter (+/- 657,200)
```

Kedua implementasi punya performa yang mirip! Kita tidak akan menjelaskan kode benchmark di sini karena tujuannya bukan membuktikan bahwa kedua versi itu setara, melainkan memberi gambaran umum tentang bagaimana perbandingan performa kedua implementasi tersebut.

Untuk benchmark yang lebih menyeluruh, kamu bisa mencoba berbagai teks dengan berbagai ukuran sebagai `contents`, kata-kata berbeda dan kata dengan panjang berbeda sebagai `query`, serta segala macam variasi lainnya. Intinya begini: meski iterator adalah abstraksi tingkat tinggi, hasil kompilasinya kira-kira sama dengan kode yang kamu tulis sendiri secara manual di tingkat rendah. Iterator adalah salah satu _zero-cost abstractions_ milik Rust, yang maksudnya memakai abstraksi itu tidak menimbulkan biaya tambahan saat runtime. Ini mirip dengan cara Bjarne Stroustrup, perancang dan implementor awal C++, mendefinisikan zero-overhead dalam pidato utamanya di ETAPS 2012 yang berjudul “Foundations of C++”:

> Secara umum, implementasi C++ mengikuti prinsip zero-overhead: apa yang tidak
> kamu gunakan, tidak kamu bayar. Lebih jauh: apa yang kamu gunakan, kamu tidak
> mungkin menulisnya lebih baik dengan tangan.

Dalam banyak kasus, kode Rust yang memakai iterator dikompilasi menjadi assembly yang sama dengan yang akan kamu tulis sendiri. Optimisasi seperti loop unrolling dan menghilangkan bounds checking pada akses array tetap berlaku sehingga kode hasilnya jadi sangat efisien. Sekarang setelah kamu tahu ini, kamu bisa memakai iterator dan closure tanpa rasa khawatir! Keduanya membuat kode terasa lebih tinggi levelnya, tetapi tidak membebani performa runtime.

## Ringkasan

Closure dan iterator adalah fitur Rust yang terinspirasi dari ide-ide bahasa pemrograman fungsional. Keduanya membantu kemampuan Rust mengekspresikan ide tingkat tinggi dengan jelas sambil tetap menjaga performa setara kode tingkat rendah. Cara closure dan iterator diimplementasikan membuat performa runtime tidak terpengaruh. Ini bagian dari tujuan Rust untuk terus berusaha menyediakan zero-cost abstractions.

Sekarang setelah kita meningkatkan daya ekspresi proyek I/O kita, mari kita lihat beberapa fitur `cargo` lain yang akan membantu kita berbagi proyek ini dengan dunia.
