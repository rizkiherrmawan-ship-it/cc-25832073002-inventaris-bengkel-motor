# Arsitektur

## Gambaran Umum
```text
Pengguna --> Aplikasi Inventaris (systemd: inventaris.service) --> Penyimpanan data
                         |
                         +--> GitHub (kode sumber, via deploy key)
```

## Komponen
- **Aplikasi inventaris**: logika pencatatan stok.
- **systemd**: menjalankan aplikasi sebagai service dan merestartnya bila berhenti.
- **Penyimpanan data**: menyimpan data suku cadang dan transaksi.
- **GitHub**: menyimpan kode dan dokumentasi, diakses dengan deploy key.

## Prinsip
- Konfigurasi sensitif disimpan di luar repository.
- Satu service untuk satu aplikasi.
