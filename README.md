# jadwal-shalat

## Deskripsi
CLI tool untuk menampilkan jadwal shalat sesuai lokasi otomatis (berdasarkan IP publik) atau manual. Mendukung fallback API, timezone akurat, dan output profesional.

## Fitur
- Ambil IP publik user
- Deteksi lokasi otomatis (kota, negara, koordinat, timezone)
- Fallback API lokasi jika utama gagal
- Ambil jadwal shalat dari API Aladhan (method Kemenag Indonesia)
- Output terminal rapi, info waktu shalat berikutnya
- Error handling dan timeout
- Header versi CLI

## Instalasi

### Prasyarat
- Python 3.9+
- requests
- zoneinfo (Python 3.9+; untuk sistem minimal, install python-tzdata)

### Install dependencies
```
pip install requests
```

### Download
Clone repo:
```
git clone https://github.com/Bangkah/jadwal-shalat.git
cd jadwal-shalat
```

### Jalankan
```
python jadwal-shalat.py
```

## Penggunaan

Jalankan tanpa argumen:
```
./jadwal-shalat.py
```

Output:
```
jadwal-shalat v1.0.0
====================

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

## Opsi Manual (Opsional)

Untuk versi berikutnya, bisa ditambah:
- `--city` untuk input manual
- `--lat --lon` untuk koordinat manual
- `--method` untuk memilih metode jadwal

## Error Handling
- Timeout API: pesan error ramah
- Lokasi gagal: fallback otomatis
- Jadwal shalat gagal: pesan error

## Rilis

1. Pastikan semua dependensi terinstall.
2. Commit dan push ke GitHub.
3. Tambahkan PKGBUILD untuk AUR:
```
depends=('python' 'python-requests')
optdepends=('python-tzdata: timezone database (untuk beberapa sistem minimal)')
```
4. Tag rilis di GitHub:
```
git tag v1.0.0
```
5. Push tag:
```
git push --tags
```

## Kontribusi
Pull request dan issue dipersilakan.

## Lisensi
MIT
# jadwal-shalat
