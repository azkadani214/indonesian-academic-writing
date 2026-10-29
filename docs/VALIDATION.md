# Catatan Validasi Versi 0.1.0

Tanggal: 30 Oktober 2026 (Asia/Jakarta).

## Pemeriksaan yang telah dilakukan

| Pemeriksaan | Hasil | Batas |
| --- | --- | --- |
| Validator bawaan skill-creator (`quick_validate.py`) | Lulus | Metadata dan struktur dasar; bukan pengujian mutu respons |
| Validator paket proyek | Lulus | Metadata sederhana, lisensi, tautan berkas, keterjangkauan referensi, portabilitas |
| Pengujian unit validator | 9 pengujian lulus | Termasuk tautan rusak, referensi di luar paket, path mesin, dan modul yang tidak dirujuk |
| Penemuan lokal melalui Skills CLI 1.7.4 | Satu skill ditemukan | Nama `indonesian-academic-writing` |
| Instalasi lokal melalui Skills CLI 1.7.4 | Berhasil dengan pilihan Codex, Claude Code, OpenCode, dan Cursor | Instalasi lingkup proyek terisolasi, mode salin; bukan pengujian inferensi keempat agen |
| Kelengkapan berkas terpasang | 20 berkas pada setiap salinan cocok dengan sumber menurut SHA-256 | Termasuk 17 modul referensi, profil pedoman, SKILL.md, dan LICENSE |
| Logo SVG | XML terbaca, tanpa skrip atau dependensi gambar eksternal; hash sama dengan berkas pengguna | Logo tidak diubah |

Uji CLI memakai Node.js 24.22.1. Salinan untuk agen yang berbagi direktori universal berada pada `.agents/skills/`; salinan Claude Code berada pada `.claude/skills/`. Tidak ada instalasi global yang dilakukan untuk pengujian ini.

## Yang belum dibuktikan oleh pengujian ini

- Mutu respons setiap agen/model pada seluruh jenis tugas akademik.
- Kelengkapan atau keberlakuan setiap pedoman kampus pada masa mendatang.
- Kebenaran sumber ilmiah yang kelak dimasukkan pengguna.
- Kepatuhan format DOCX/PDF tertentu; paket ini menyediakan pedoman, bukan mesin tata letak.
- Kemunculan dan peringkat pada direktori skills.sh.

Gunakan [skenario perilaku](../tests/scenarios.md) untuk penilaian lanjutan. Pemeriksaan manual isi memastikan ketentuan kampus dapat menggantikan kerangka umum, contoh data diberi label, dan bahan gambar tidak diperlakukan sebagai aturan universal; pemeriksaan manual tersebut bukan pengganti pengujian perilaku model.
