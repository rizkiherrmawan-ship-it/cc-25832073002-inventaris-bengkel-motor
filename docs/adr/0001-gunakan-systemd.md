# ADR-0001: Menjalankan Aplikasi dengan systemd

- Status: Diterima
- Tanggal: 2026-11-07

## Konteks
Aplikasi harus berjalan terus, start otomatis saat server menyala, dan restart bila gagal.

## Keputusan
Aplikasi dijalankan sebagai service systemd (inventaris.service).

## Konsekuensi
- Positif: tanpa tambahan software, log lewat journalctl, restart otomatis.
- Negatif: terikat pada sistem operasi Linux dengan systemd.
