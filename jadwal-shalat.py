#!/usr/bin/env python3
"""
CLI tool: jadwal-shalat

Fitur:
- Ambil IP publik user
- Ubah IP ke lokasi (kota, negara, koordinat)
- Ambil jadwal shalat dari API
- Tampilkan jadwal shalat di terminal
"""
import sys
import requests
from datetime import datetime, timedelta

def get_public_ip():
	resp = requests.get('https://api.ipify.org?format=json', timeout=5)
	resp.raise_for_status()
	return resp.json()['ip']

def get_location(ip):
	# Primary: ipwho.is
	try:
		resp = requests.get(f'https://ipwho.is/{ip}', timeout=5)
		resp.raise_for_status()
		data = resp.json()
		city = data.get('city')
		country = data.get('country')
		timezone = data.get('timezone', None)
		try:
			lat = float(data.get('latitude'))
			lon = float(data.get('longitude'))
		except (TypeError, ValueError):
			lat = lon = None
		if city and country and lat is not None and lon is not None:
			return {
				'city': city,
				'country': country,
				'latitude': lat,
				'longitude': lon,
				'timezone': timezone
			}
	except Exception:
		pass
	# Fallback: ipapi.co
	try:
		resp = requests.get('https://ipapi.co/json/', timeout=5)
		resp.raise_for_status()
		data = resp.json()
		city = data.get('city')
		country = data.get('country_name') or data.get('country')
		timezone = data.get('timezone', None)
		try:
			lat = float(data.get('latitude'))
			lon = float(data.get('longitude'))
		except (TypeError, ValueError):
			lat = lon = None
		if city and country and lat is not None and lon is not None:
			return {
				'city': city,
				'country': country,
				'latitude': lat,
				'longitude': lon,
				'timezone': timezone
			}
	except Exception:
		pass
	return {
		'city': None,
		'country': None,
		'latitude': None,
		'longitude': None,
		'timezone': None
	}

def get_jadwal_shalat(lat, lon):
	today = datetime.now().strftime('%d-%m-%Y')
	url = f'https://api.aladhan.com/v1/timings/{today}?latitude={lat}&longitude={lon}&method=20'
	resp = requests.get(url, timeout=5)
	resp.raise_for_status()
	data = resp.json()
	if data.get('code') != 200:
		raise RuntimeError("Gagal mengambil jadwal shalat.")
	return data['data']['timings']

def main():
	ip = get_public_ip()
	loc = get_location(ip)
	if (
		loc['city'] is None or
		loc['country'] is None or
		loc['latitude'] is None or
		loc['longitude'] is None
	):
		print('Gagal mendeteksi lokasi dari IP. Silakan cek koneksi atau gunakan VPN lain.')
		sys.exit(1)
	# Gunakan timezone dari API jika ada
	tz = None
	if loc.get('timezone'):
		try:
			from zoneinfo import ZoneInfo
			tz = ZoneInfo(loc['timezone'])
		except Exception:
			tz = None
	if tz:
		now = datetime.now(tz)
	else:
		now = datetime.now()
	jadwal = get_jadwal_shalat(loc['latitude'], loc['longitude'])

	mapping_id = {
		'Fajr': 'Subuh',
		'Sunrise': 'Terbit',
		'Dhuhr': 'Dzuhur',
		'Asr': 'Ashar',
		'Sunset': 'Matahari Terbenam',
		'Maghrib': 'Maghrib',
		'Isha': 'Isya',
		'Imsak': 'Imsak',
		'Midnight': 'Tengah Malam',
		'Firstthird': 'Sepertiga Malam Awal',
		'Lastthird': 'Sepertiga Malam Akhir'
	}
	mapping_eng = {v: k for k, v in mapping_id.items()}

	# Format tanggal Indonesia
	bulan_id = [
		'', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
		'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
	]
	tanggal_id = f"{now.day} {bulan_id[now.month]} {now.year}"

	print('\njadwal-shalat v1.0.0')
	print('====================')
	print('')
	print('=== Jadwal Shalat ===')
	print(f'Tanggal             : {tanggal_id}')
	print(f'Lokasi              : {loc["city"]}, {loc["country"]}')

	# Tampilkan jadwal utama
	waktu_utama = ['Imsak','Subuh','Terbit','Dzuhur','Ashar','Maghrib','Isya']
	for k in waktu_utama:
		eng_key = mapping_eng.get(k)
		if eng_key and eng_key in jadwal:
			print(f'{k:<20}: {jadwal[eng_key]}')

	# Fitur profesional: Penanda waktu shalat berikutnya
	waktu_shalat = []
	for k in waktu_utama:
		eng_key = mapping_eng.get(k)
		if eng_key and eng_key in jadwal:
			try:
				jam, menit = map(int, jadwal[eng_key].split(':'))
				waktu = now.replace(hour=jam, minute=menit, second=0, microsecond=0)
				if waktu < now:
					waktu = waktu + timedelta(days=1)
				waktu_shalat.append((k, waktu, jadwal[eng_key]))
			except Exception:
				continue
	waktu_shalat.sort(key=lambda x: x[1])
	berikutnya = next(((k, t, jam) for k, t, jam in waktu_shalat if t > now), None)
	if berikutnya:
		k, t, jam = berikutnya
		delta = t - now
		jam_delta = int(delta.total_seconds() // 3600)
		menit_delta = int((delta.total_seconds() % 3600) // 60)
		sisa = f"{jam_delta} jam" if jam_delta else ""
		if menit_delta:
			sisa += f" {menit_delta} menit"
		sisa = sisa.strip()
		print(f'\nShalat berikutnya   : {k} ({jam}) - {sisa} lagi')

	# Info tambahan
	print('\nInfo Tambahan:')
	for eng_key in ['Sunset','Midnight','Firstthird','Lastthird']:
		if eng_key in jadwal:
			print(f'{mapping_id.get(eng_key, eng_key):<20}: {jadwal[eng_key]}')

if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print(f"Terjadi error: {e}")
		sys.exit(1)
