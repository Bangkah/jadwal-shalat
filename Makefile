# Jadwal Shalat Makefile

.PHONY: si

si:
	@echo "Tanggal: $(shell date '+%d %B %Y')"
	@echo "Workspace: jadwal-shalat"
	@echo "File utama: jadwal-shalat.py"
	@echo "PKGBUILD: PKGBUILD"
	@echo "README: README.md"
	@echo "aur-jadwal-shalat/PKGBUILD: aur-jadwal-shalat/PKGBUILD"
