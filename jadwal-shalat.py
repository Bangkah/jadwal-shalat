#!/usr/bin/env python3
"""
CLI tool: jadwal-shalat

Fitur utama:
- Deteksi lokasi otomatis via GeoIP offline
- Override lokasi secara manual melalui argumen CLI
- Ambil jadwal shalat dari API Aladhan
- Tampilkan jadwal shalat di terminal
"""
import argparse
import json
import sys
from datetime import datetime, timedelta, time as dt_time
from pathlib import Path

import requests

try:
	import geoip2.database
	from geoip2.errors import AddressNotFoundError
	GEOIP_AVAILABLE = True
except ImportError:
	geoip2 = None
	AddressNotFoundError = None
	GEOIP_AVAILABLE = False

VERSION = '1.1.0'
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_GEOIP_DB = SCRIPT_DIR / 'GeoLite2-City.mmdb'
DEFAULT_USER_AGENT = f'jadwal-shalat/{VERSION} (+https://github.com/Bangkah/jadwal-shalat)'

CONFIG_DIR = Path.home() / '.config' / 'jadwal-shalat'
CONFIG_FILE = CONFIG_DIR / 'config.json'
CACHE_DIR = Path.home() / '.cache' / 'jadwal-shalat'

METHOD_MAP = {
	'mwl': 3,
	'isna': 2,
	'egypt': 5,
	'karachi': 1,
	'ummalqura': 4,
	'kemenag': 20,
	'dubai': 12,
	'moai': 14,
}


def resolve_method(name: str):
	key = (name or 'kemenag').lower()
	if key not in METHOD_MAP:
		raise ValueError(f'Metode "{name}" tidak dikenal. Pilihan valid: {", ".join(sorted(METHOD_MAP))}')
	return key, METHOD_MAP[key]


def ensure_app_dirs():
	CONFIG_DIR.mkdir(parents=True, exist_ok=True)
	CACHE_DIR.mkdir(parents=True, exist_ok=True)


def load_last_location():
	if not CONFIG_FILE.exists():
		return None
	try:
		with CONFIG_FILE.open('r', encoding='utf-8') as fh:
			data = json.load(fh)
	except Exception:
		return None
	return data.get('last_location')


def save_last_location(loc):
	if not loc:
		return
	ensure_app_dirs()
	payload = {'last_location': {
		'city': loc.get('city'),
		'country': loc.get('country'),
		'latitude': loc.get('latitude'),
		'longitude': loc.get('longitude'),
		'timezone': loc.get('timezone')
	}}
	with CONFIG_FILE.open('w', encoding='utf-8') as fh:
		json.dump(payload, fh, ensure_ascii=False, indent=2)



def _cache_file_name(lat, lon, method_key, date_key):
	safe_lat = f"{lat:.6f}"
	safe_lon = f"{lon:.6f}"
	return CACHE_DIR / f"{date_key}_{method_key}_{safe_lat}_{safe_lon}.json"


def load_cached_timings(lat, lon, method_key, date_key):
	cache_file = _cache_file_name(lat, lon, method_key, date_key)
	if not cache_file.exists():
		return None
	try:
		with cache_file.open('r', encoding='utf-8') as fh:
			data = json.load(fh)
		return data.get('timings')
	except Exception:
		return None


def save_cached_timings(lat, lon, method_key, date_key, timings):
	ensure_app_dirs()
	cache_file = _cache_file_name(lat, lon, method_key, date_key)
	payload = {
		'timings': timings,
		'meta': {
			'latitude': lat,
			'longitude': lon,
			'method': method_key,
			'date': date_key,
			'saved_at': datetime.utcnow().isoformat()
		}
	}
	with cache_file.open('w', encoding='utf-8') as fh:
		json.dump(payload, fh, ensure_ascii=False, indent=2)


def fetch_timings_for_date(lat, lon, method_key, method_code, target_dt, use_cache=True, verbose=True):
	cache_date = target_dt.strftime('%Y-%m-%d')
	if use_cache:
		cached = load_cached_timings(lat, lon, method_key, cache_date)
		if cached:
			if verbose:
				print('Info: Menggunakan jadwal dari cache lokal.')
			return cached
	api_date = target_dt.strftime('%d-%m-%Y')
	timings = get_jadwal_shalat(lat, lon, method_code, api_date)
	if use_cache:
		save_cached_timings(lat, lon, method_key, cache_date, timings)
	return timings


def build_event_datetime(date_obj, time_str, tz):
	try:
		hour, minute = map(int, time_str.split(':'))
	except ValueError:
		raise ValueError(f'Format waktu tidak valid: {time_str}')
	if tz:
		return datetime(date_obj.year, date_obj.month, date_obj.day, hour, minute, tzinfo=tz)
	return datetime(date_obj.year, date_obj.month, date_obj.day, hour, minute)

def parse_args():
	parser = argparse.ArgumentParser(description='jadwal-shalat CLI')
	parser.add_argument('--city', help='Nama kota manual untuk geocoding')
	parser.add_argument('--lat', type=float, help='Latitude manual')
	parser.add_argument('--lon', type=float, help='Longitude manual')
	parser.add_argument('--timezone', help='Timezone manual, contoh Asia/Jakarta')
	parser.add_argument('--geoip-db', help='Lokasi file GeoLite2-City.mmdb kustom')
	parser.add_argument('--method', choices=sorted(METHOD_MAP.keys()), default='kemenag', help='Metode perhitungan jadwal shalat (default: kemenag)')
	parser.add_argument('--no-cache', action='store_true', help='Abaikan cache lokal dan paksa ambil data baru')
	return parser.parse_args()


def get_public_ip():
	resp = requests.get('https://api.ipify.org?format=json', timeout=5, headers={'User-Agent': DEFAULT_USER_AGENT})
	resp.raise_for_status()
	return resp.json()['ip']


def get_location_from_geoip(db_path: Path):
	if not GEOIP_AVAILABLE:
		raise RuntimeError('geoip2 tidak terpasang. Jalankan tanpa GeoIP atau instal dependensi ini.')
	if not db_path.exists():
		raise FileNotFoundError(
			f'Database GeoLite2-City.mmdb tidak ditemukan di {db_path}. Unduh dari MaxMind dan letakkan di lokasi tersebut.'
		)
	ip = get_public_ip()
	with geoip2.database.Reader(str(db_path)) as reader:
		try:
			response = reader.city(ip)
		except AddressNotFoundError as exc:
			raise RuntimeError(f'Alamat IP {ip} tidak ditemukan di database GeoLite2.') from exc
	return {
		'city': response.city.name or response.subdivisions.most_specific.name or 'Lokasi Tidak Dikenal',
		'country': response.country.name or 'Unknown',
		'latitude': response.location.latitude,
		'longitude': response.location.longitude,
		'timezone': response.location.time_zone
	}


def get_location_from_city(city: str):
	params = {
		'q': city,
		'format': 'json',
		'limit': 1,
		'addressdetails': 1
	}
	headers = {'User-Agent': DEFAULT_USER_AGENT}
	resp = requests.get('https://nominatim.openstreetmap.org/search', params=params, headers=headers, timeout=10)
	resp.raise_for_status()
	data = resp.json()
	if not data:
		raise RuntimeError(f'Gagal menemukan koordinat untuk kota "{city}".')
	item = data[0]
	address = item.get('address', {})
	return {
		'city': address.get('city') or address.get('town') or address.get('state') or city,
		'country': address.get('country', 'Unknown'),
		'latitude': float(item['lat']),
		'longitude': float(item['lon']),
		'timezone': None
	}


def get_location_from_ip_api():
	resp = requests.get('https://ipapi.co/json/', timeout=5, headers={'User-Agent': DEFAULT_USER_AGENT})
	resp.raise_for_status()
	data = resp.json()
	lat = data.get('latitude') or data.get('lat')
	lon = data.get('longitude') or data.get('lon')
	if lat is None or lon is None:
		raise RuntimeError('Respons ipapi.co tidak menyertakan koordinat.')
	return {
		'city': data.get('city') or 'Lokasi Tidak Dikenal',
		'country': data.get('country_name') or data.get('country') or 'Unknown',
		'latitude': float(lat),
		'longitude': float(lon),
		'timezone': data.get('timezone')
	}

def resolve_location(args):
	if args.lat is not None or args.lon is not None:
		if args.lat is None or args.lon is None:
			raise RuntimeError('Argumen --lat dan --lon harus digunakan bersamaan.')
		return {
			'city': args.city or 'Koordinat Manual',
			'country': 'Manual',
			'latitude': args.lat,
			'longitude': args.lon,
			'timezone': args.timezone
		}
	if args.city:
		loc = get_location_from_city(args.city)
		if args.timezone:
			loc['timezone'] = args.timezone
		return loc
	geoip_path = Path(args.geoip_db).expanduser() if args.geoip_db else DEFAULT_GEOIP_DB
	if GEOIP_AVAILABLE:
		try:
			loc = get_location_from_geoip(geoip_path)
			if args.timezone:
				loc['timezone'] = args.timezone
			return loc
		except Exception as exc:
			print(f'Peringatan: GeoIP offline gagal digunakan ({exc}).')
	else:
		print('Peringatan: Modul geoip2 tidak tersedia. Gunakan argumen manual atau lokasi tersimpan.')
	try:
		loc = get_location_from_ip_api()
		print('Info: Menggunakan deteksi lokasi via ipapi.co (online).')
		if args.timezone:
			loc['timezone'] = args.timezone
		return loc
	except Exception as exc:
		print(f'Peringatan: Deteksi lokasi via ipapi.co gagal ({exc}).')
	last_loc = load_last_location()
	if last_loc:
		print('Info: Menggunakan lokasi terakhir dari ~/.config/jadwal-shalat/config.json')
		if args.timezone:
			last_loc['timezone'] = args.timezone
		return last_loc
	raise RuntimeError('Gagal menentukan lokasi. Berikan --lat/--lon atau instal geoip2 + database GeoLite2.')


def get_jadwal_shalat(lat, lon, method_code, date_str):
	url = (
		f'https://api.aladhan.com/v1/timings/{date_str}'
		f'?latitude={lat}&longitude={lon}&method={method_code}'
	)
	resp = requests.get(url, timeout=5)
	resp.raise_for_status()
	data = resp.json()
	if data.get('code') != 200:
		raise RuntimeError("Gagal mengambil jadwal shalat.")
	return data['data']['timings']

def main():
	ensure_app_dirs()
	args = parse_args()
	method_key, method_code = resolve_method(args.method)
	loc = resolve_location(args)
	if loc['latitude'] is None or loc['longitude'] is None:
		raise RuntimeError('Koordinat lokasi tidak valid. Periksa argumen atau database GeoIP.')
	save_last_location(loc)
	tz_name = loc.get('timezone')
	tz = None
	if tz_name:
		try:
			from zoneinfo import ZoneInfo
			tz = ZoneInfo(tz_name)
		except Exception:
			print(f'Peringatan: timezone {tz_name} tidak dikenali, pakai waktu lokal sistem.')
	if tz:
		now = datetime.now(tz)
	else:
		now = datetime.now()
	jadwal = fetch_timings_for_date(
		loc['latitude'],
		loc['longitude'],
		method_key,
		method_code,
		now,
		use_cache=not args.no_cache,
		verbose=True
	)

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

	print(f'\njadwal-shalat v{VERSION}')
	print('====================')
	print('')
	print('=== Jadwal Shalat ===')
	print(f'Tanggal             : {tanggal_id}')
	print(f'Lokasi              : {loc["city"]}, {loc["country"]}')

	# Tampilkan jadwal utama
	waktu_utama = ['Imsak','Subuh','Terbit','Dzuhur','Ashar','Maghrib','Isya']
	today_date = now.date()
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
				event_dt = build_event_datetime(today_date, jadwal[eng_key], tz)
				waktu_shalat.append((k, event_dt, jadwal[eng_key]))
			except Exception:
				continue
	waktu_shalat.sort(key=lambda x: x[1])
	berikutnya = next(((k, t, jam) for k, t, jam in waktu_shalat if t > now), None)
	berasal_dari_besok = False
	if berikutnya is None:
		next_day = now + timedelta(days=1)
		jadwal_besok = fetch_timings_for_date(
			loc['latitude'],
			loc['longitude'],
			method_key,
			method_code,
			next_day,
			use_cache=not args.no_cache,
			verbose=False
		)
		waktu_besok = []
		for k in waktu_utama:
			eng_key = mapping_eng.get(k)
			if eng_key and eng_key in jadwal_besok:
				try:
					event_dt = build_event_datetime(next_day.date(), jadwal_besok[eng_key], tz)
					waktu_besok.append((k, event_dt, jadwal_besok[eng_key]))
				except Exception:
					continue
		waktu_besok.sort(key=lambda x: x[1])
		if waktu_besok:
			berikutnya = waktu_besok[0]
			berasal_dari_besok = True
	if berikutnya:
		k, t, jam = berikutnya
		delta = t - now
		jam_delta = int(delta.total_seconds() // 3600)
		menit_delta = int((delta.total_seconds() % 3600) // 60)
		sisa = f"{jam_delta} jam" if jam_delta else ""
		if menit_delta:
			sisa += f" {menit_delta} menit"
		sisa = sisa.strip()
		label_besok = ' (besok)' if berasal_dari_besok else ''
		print(f'\nShalat berikutnya   : {k} ({jam}) - {sisa} lagi{label_besok}')

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
