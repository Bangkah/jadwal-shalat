.PHONY: install

install:
	@echo "Menginstal jadwal-shalat ke /usr/bin..."
	sudo cp jadwal-shalat.py /usr/bin/jadwal-shalat
	sudo chmod +x /usr/bin/jadwal-shalat
	@echo "Instalasi selesai. Jalankan 'jadwal-shalat' di terminal."
# Jadwal Shalat Makefile

.PHONY: si

si:
	@echo "====================================="
	@echo "Ringkasan Workspace"
	@echo "====================================="
	@echo "Tanggal     : $(shell date '+%d %B %Y')"
	@echo "Workspace   : jadwal-shalat"
	@echo "File utama  : jadwal-shalat.py"
	@echo "PKGBUILD    : PKGBUILD"
	@echo "README      : README.md"
	@echo "AUR PKGBUILD: aur-jadwal-shalat/PKGBUILD"
	@echo "====================================="
