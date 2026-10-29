# Instalasi dan Publikasi

## Bentuk paket

Repositori ini menyediakan satu skill pada `skills/indonesian-academic-writing/`. Nama direktori sesuai dengan `name` dalam frontmatter. Referensi, profil pedoman, dan lisensi berada di dalam direktori skill sehingga ikut tersedia pada instalasi yang menyalin direktori tersebut. README, logo, pengujian, dan panduan publikasi berada di tingkat repositori.

Instruksi dan referensi menggunakan bahasa Indonesia agar pemilik proyek dapat menelaahnya. Terjemahan instruksi ke bahasa Inggris dapat dibuat setelah penelaahan isi; contoh bahasa Indonesia dan kepekaan terhadap pedoman lokal tetap dipertahankan. Versi awal tidak mengklaim sudah diuji pada setiap model atau agen.

## Pemeriksaan sebelum rilis

Jalankan dari direktori repositori dengan Python 3.10 atau lebih baru:

```bash
python scripts/validate_package.py
python -m unittest discover -s tests -p "test_*.py"
```

Validator memeriksa format metadata sederhana yang digunakan paket, kesesuaian nama, tautan lokal, keterjangkauan referensi, lisensi, dan portabilitas direktori skill. Validator bukan parser YAML lengkap, tidak memeriksa semua fragmen judul Markdown, dan tidak memvalidasi kebenaran sumber web. Skenario perilaku di [tests/scenarios.md](../tests/scenarios.md) perlu dijalankan pada agen tujuan bila ingin menilai mutu respons.

## Memeriksa penemuan dan instalasi

Gunakan versi Node.js yang memenuhi persyaratan CLI. Versi CLI yang dipakai saat uji harus dicatat karena persyaratan dapat berubah.

```bash
npx skills add . --list
npx skills add . --skill indonesian-academic-writing
```

Untuk uji terisolasi, jalankan instalasi dari direktori sementara dan berikan path absolut repositori sebagai sumber. Pilih agen uji dan lingkup proyek. Setelah instalasi, periksa `SKILL.md`, seluruh folder `references`, profil pedoman, dan `LICENSE` pada salinan terpasang. Jangan menganggap penemuan nama skill sama dengan keberhasilan penyalinan seluruh berkas.

## GitHub dan skills.sh

Tujuan publikasi: `azkadani214/indonesian-academic-writing`.

1. Pastikan berkas yang akan dipublikasikan hanya berkas proyek yang dimaksud. Gambar sumber, data penelitian pengguna, kredensial, dan direktori uji lokal tidak menjadi isi paket publik.
2. Publikasikan repositori GitHub yang berisi paket, README, logo, dan lisensi.
3. Periksa penemuan skill dari sumber GitHub, kemudian lakukan instalasi nyata dari repositori tersebut.
4. Periksa kelengkapan salinan dan catat versi CLI serta agen yang dipilih.
5. Periksa halaman direktori bila sudah tersedia. Jangan menjanjikan waktu indeks, peringkat, atau jumlah pemasangan.

Perintah pengguna setelah publikasi:

```bash
npx skills add azkadani214/indonesian-academic-writing --skill indonesian-academic-writing
```

Menurut [FAQ skills.sh](https://skills.sh/docs/faq), repositori GitHub menjadi sumber skill dan telemetri instalasi membantu penemuannya pada direktori. Tidak diperlukan paket npm milik proyek ini atau perintah `npm publish` untuk membagikan skill melalui sumber GitHub. Pengaturan telemetri mengikuti pilihan pengguna dan [dokumentasi CLI](https://github.com/vercel-labs/skills).

## Batas kompatibilitas

Paket tidak mengunci nama alat penelusuran, API model, aplikasi dokumen, atau sistem operasi. Agen yang mendukung Agent Skills dapat membaca instruksi dan referensi; kemampuan melaksanakan penelusuran, mengolah berkas, atau mengekspor dokumen tetap bergantung pada lingkungan agen. Paket tidak membuat slash command khusus OpenCode secara otomatis.

## Rujukan teknis

- [Spesifikasi Agent Skills](https://agentskills.io/specification)
- [Referensi perintah Skills CLI](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)
- [Dokumentasi skills.sh](https://skills.sh/docs)

Dokumentasi teknis diperiksa pada 29–30 Oktober 2026. Baca ulang ketika mengubah cara distribusi.
