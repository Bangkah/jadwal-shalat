# bangkah-jadwal-shalat

CLI tool profesional untuk menampilkan jadwal shalat otomatis berdasarkan lokasi IP publik atau input manual. Output rapi, akurat, punya cache lokal, dan siap distribusi (AUR, Snap, dsb).

---


## Instalasi

### Arch Linux/AUR (Direkomendasikan)

Paket AUR lebih terintegrasi dengan sistem, auto update, dan dependensi otomatis.

```bash
yay -S jadwal-shalat
```

### pip (Alternatif)

Jika tidak menggunakan Arch Linux, bisa install via PyPI:

```bash
pip install bangkah-jadwal-shalat
```

Jika pip error (misal: ModuleNotFoundError: No module named 'pip'), jalankan:
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

---

## Penggunaan

Jalankan command:

```bash
jadwal-shalat
```

Contoh:

```bash
jadwal-shalat --city Surabaya
jadwal-shalat --lat -7.25 --lon 112.7 --timezone Asia/Jakarta
```

Untuk opsi dan bantuan:

```bash
jadwal-shalat --help
```

---

---

## Fitur Utama

- Deteksi IP publik otomatis atau input manual (`--city`, `--lat/--lon`, `--timezone`).
- GeoIP offline (opsional) dengan auto-scan file GeoLite2 di ~/.config, ~/.local/share/GeoIP, /usr/share/GeoIP, dsb. Fallback ipapi.co, ipwho.is, ip-api.com, dan ipapi.ipspeed.info (butuh API key) plus lokasi tersimpan terakhir. Koordinat dari IP otomatis diperkaya lewat reverse geocoding Nominatim agar nama kota lebih akurat.
- Cache lokal per-tanggal, bisa dimatikan via `--no-cache` saat butuh data baru.
- API Aladhan dengan dukungan pemilihan metode (`--method kemenag|mwl|...`).
- Jadwal lengkap + countdown shalat berikutnya, termasuk lintas hari.
- Timezone akurat berkat modul `zoneinfo` builtin Python 3.9+.
- Error handling & timeout agar CLI tetap responsif.
- Siap dikemas ke AUR, Snap, maupun instalasi manual.

---

## Screenshot

![alt text](image.png)

yay -S jadwal-shalat
git clone https://github.com/Bangkah/jadwal-shalat.git

## Instalasi

### pip (direkomendasikan)

```bash
pip install bangkah-jadwal-shalat
```

Jika pip error (misal: ModuleNotFoundError: No module named 'pip'), jalankan:
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### Arch Linux/AUR

```bash
yay -S jadwal-shalat
```

---

jadwal-shalat

## Penggunaan

Jalankan command:

```bash
jadwal-shalat
```

Contoh:

```bash
jadwal-shalat --city Surabaya
jadwal-shalat --lat -7.25 --lon 112.7 --timezone Asia/Jakarta
```

Untuk opsi dan bantuan:

```bash
jadwal-shalat --help
```

---

## Cara Kerja

1. Ambil IP publik user (GeoIP offline/ipapi.co/ipwho.is/ip-api.com/ipapi.ipspeed.info) atau gunakan input manual/cached, lalu lakukan reverse geocoding ke Nominatim untuk memastikan nama kota/kabupaten tepat.
2. Deteksi lokasi & timezone (GeoIP, Nominatim, atau lokasi terakhir).
3. Ambil jadwal shalat dari API Aladhan untuk tanggal terkait dan simpan ke cache.
4. Hitung countdown jadwal berikutnya; jika hari sudah berganti, ambil jadwal besok.
5. Tampilkan jadwal utama + info tambahan di terminal.

---

## Dependensi

- Python >= 3.9 (zoneinfo built-in)
- requests
- geoip2 (opsional, untuk deteksi lokasi offline)
- python-tzdata (opsional, untuk distro tertentu)

### API Key Opsional

- Atur variabel lingkungan `JADWAL_SHALAT_IPSPEED_KEY` atau gunakan `--ipspeed-key` untuk mengaktifkan fallback ipapi.ipspeed.info.
- File GeoLite2-City.mmdb dapat ditempatkan di `./GeoLite2-City.mmdb`, `~/.config/jadwal-shalat/`, `~/.local/share/GeoIP/`, `/usr/share/GeoIP/`, atau `/var/lib/GeoIP/` supaya mode GeoIP offline otomatis aktif.
- ip-api.com tidak butuh API key, tapi gratisnya dibatasi 45 permintaan/menit/IP. CLI akan memberi pesan jika limit tercapai.

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
- [x] Fallback API lokasi + simpan lokasi terakhir
- [x] Input manual kota/koordinat
- [x] Paket Snap (strict confinement)
- [ ] Output JSON
- [ ] Notifikasi waktu shalat
- [ ] Packaging PyPI
- [ ] Engine perhitungan offline

---


## Keamanan & Privasi

- Tidak menyimpan data user selain lokasi terakhir di `~/.config/jadwal-shalat/`
- Tidak mengirim data sensitif
- Hanya menggunakan API publik (Aladhan, Nominatim, ipify)

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