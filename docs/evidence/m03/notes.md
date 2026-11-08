# Catatan Evidence M03

Tanggal: 8 November 2026

## Ringkasan
- Aplikasi: Inventaris Bengkel Motor (Flask + Gunicorn)
- Service systemd: `inventaris` (enabled)
- Reverse proxy: Caddy :80 meneruskan ke 127.0.0.1:8000. nginx sudah dihentikan dan di-disable.
- Firewall: UFW aktif, hanya 22/tcp dan 80/tcp
- SSH: key-only, login root dinonaktifkan, AllowUsers satu akun
- Gunicorn: 1 worker, 2 thread, bind loopback

## Berkas
- os.txt, resources.txt: spesifikasi server
- ufw.txt, ports.txt: firewall dan port yang listen
- service.txt, caddy.txt, Caddyfile.txt: status service dan konfigurasi proxy
- health-internal.txt: tes langsung ke Gunicorn (127.0.0.1:8000)
- health-public.txt: tes lewat Caddy (port 80)

## Uji dari luar jaringan
Dibuka dari HP dengan data seluler: /health menjawab {"status":"ok"} pada 8 Nov 2026 pukul 14.23 WIB.

## Catatan
- IP publik disamarkan menjadi <PUBLIC_IP> karena repository bersifat publik.
- Aplikasi berada di ~/inventaris-bengkel-motor dan service bernama `inventaris`, berbeda dari contoh modul (/srv/cc-m03 dan cc-m03).
- Server semula memakai nginx, lalu diganti Caddy agar sesuai modul.
