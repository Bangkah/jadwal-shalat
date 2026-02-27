"""Entry point untuk `python -m jadwal_shalat`."""
import sys
from jadwal_shalat.cli import main

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Terjadi error: {e}")
        sys.exit(1)
