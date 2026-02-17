
# jadwal-shalat

CLI tool profesional untuk menampilkan jadwal shalat berdasarkan lokasi otomatis (IP publik) atau manual. Dirancang ringan, cepat, akurat, dan siap untuk distribusi Linux (AUR, pip, dll).

---

## Fitur Utama

- Deteksi IP publik otomatis
- Deteksi lokasi otomatis (kota, negara, koordinat, timezone)
- Fallback API lokasi jika layanan utama gagal
- Menggunakan API Aladhan dengan metode Kemenag Indonesia (method=20)
- Menampilkan jadwal shalat lengkap
- Menampilkan waktu shalat berikutnya + countdown
- Output terminal rapi dan profesional
- Error handling lengkap
- Timeout protection untuk API
- Mendukung timezone akurat
- CLI ringan dan cepat
- Siap untuk packaging AUR

---

## Screenshot

```

# jadwal-shalat v1.0.0

=== Jadwal Shalat ===
Tanggal             : 18 Februari 2026
Lokasi              : Banda Aceh, Indonesia

Imsak               : 05:46
Subuh               : 05:56
Terbit              : 06:54
Dzuhur              : 12:53
Ashar               : 16:12
Maghrib             : 18:51
Isya                : 19:49

Shalat berikutnya   : Subuh (05:56) - 2 jam lagi

Info Tambahan:
Matahari Terbenam   : 18:51
Tengah Malam        : 00:53
Sepertiga Malam Awal: 22:52
Sepertiga Malam Akhir: 02:53

```

---

## Instalasi

### Prasyarat

- Python 3.9 atau lebih baru
- requests
- tzdata (untuk beberapa sistem Linux minimal)

---

### Install via pip (manual)

```
pip install requests
```

---

### Install dari GitHub

```
git clone https://github.com/Bangkah/jadwal-shalat.git
cd jadwal-shalat
chmod +x jadwal-shalat.py
```

Jalankan:

```
./jadwal-shalat.py
```

atau:

```
python jadwal-shalat.py
```

---

## Cara Kerja

1. Mengambil IP publik user
2. Mengubah IP menjadi lokasi geografis
3. Mengambil timezone akurat
4. Mengambil jadwal shalat dari API Aladhan
5. Menampilkan jadwal dan waktu shalat berikutnya

---

## Dependensi

Library Python:

```
requests
zoneinfo (built-in Python 3.9+)
```

---

## Kompatibilitas

- Linux ✅
- Arch Linux ✅ (AUR ready)
- Ubuntu ✅
- Debian ✅
- Fedora ✅
- macOS ✅
- Windows ✅

---

## Struktur Project

```
jadwal-shalat/
│
├── jadwal-shalat.py
├── README.md
├── LICENSE
└── .github/workflows/ci.yml
```

---

## Roadmap

Fitur yang direncanakan:

- [ ] Input manual kota
- [ ] Input manual koordinat
- [ ] Pilihan metode perhitungan
- [ ] Output JSON
- [ ] Mode minimal
- [ ] Notifikasi waktu shalat
- [ ] Packaging PyPI
- [ ] Packaging AUR

---

## Keamanan & Privasi

Tool ini:

- Tidak menyimpan data user
- Tidak mengirim data sensitif
- Hanya menggunakan API publik untuk lokasi dan jadwal

---

## Kontribusi

Kontribusi sangat diterima.

Langkah:

```
fork repo
buat branch baru
commit perubahan
buat pull request
```

---

## Lisensi

MIT License

Bebas digunakan, dimodifikasi, dan didistribusikan.

---

## Author

Muhammad Dhiyaul Atha  
GitHub: https://github.com/Bangkah