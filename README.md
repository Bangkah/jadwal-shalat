# jadwal-shalat

CLI tool profesional untuk menampilkan jadwal shalat otomatis berdasarkan lokasi IP publik atau input manual. Output rapi, akurat, dan siap distribusi (AUR, pip, dsb).

---

## Fitur Utama

- Deteksi IP publik otomatis
- Deteksi lokasi otomatis (kota, negara, koordinat, timezone)
- Fallback API lokasi jika layanan utama gagal
- API Aladhan (method=20/Kemenag Indonesia)
- Jadwal shalat lengkap + waktu berikutnya & countdown
- Output terminal rapi (warna, alignment)
- Error handling & timeout protection
- Support timezone akurat
- Siap packaging AUR (auto update via GitHub Actions)

---

## Screenshot

![alt text](image.png)

## Instalasi

### Arch Linux/AUR (direkomendasikan)

```
yay -S jadwal-shalat
```

### Manual (pip)

```
pip install requests
```

Clone repo:
```
git clone https://github.com/Bangkah/jadwal-shalat.git
cd jadwal-shalat
chmod +x jadwal-shalat.py
./jadwal-shalat.py
```

---

## Cara Pakai

```
jadwal-shalat
```

Atau (manual):
```
python jadwal-shalat.py
```

---

## Cara Kerja

1. Ambil IP publik user
2. Deteksi lokasi & timezone
3. Ambil jadwal shalat dari API Aladhan
4. Tampilkan jadwal & waktu berikutnya

---

## Dependensi

- Python >= 3.9 (zoneinfo built-in)
- requests
- python-tzdata (opsional, untuk timezone di beberapa distro)

---

## Kompatibilitas

- Arch Linux (AUR) ✅
- Ubuntu/Debian/Fedora/macOS/Windows ✅

---

## Struktur Project

```
├── jadwal-shalat.py
├── PKGBUILD
├── .SRCINFO
├── LICENSE
├── README.md
└── .github/workflows/
```

---

## Roadmap

- [x] Auto update AUR via GitHub Actions
- [x] Output countdown waktu shalat berikutnya
- [x] Fallback API lokasi
- [x] Output terminal profesional
- [ ] Input manual kota/koordinat
- [ ] Output JSON
- [ ] Notifikasi waktu shalat
- [ ] Packaging PyPI

---

## Keamanan & Privasi

- Tidak menyimpan data user
- Tidak mengirim data sensitif
- Hanya menggunakan API publik

---

## Kontribusi

1. Fork repo
2. Buat branch baru
3. Commit perubahan
4. Pull request

---

## Lisensi

MIT License

---

## Author

Muhammad Dhiyaul Atha  
GitHub: https://github.com/Bangkah