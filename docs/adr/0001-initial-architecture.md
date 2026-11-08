# ADR-0001: Initial VPS Deployment Architecture

## Status
Accepted

## Context
VPS 2 vCPU, RAM 1.9Gi, disk 19G, Ubuntu Server 24.04.

## Decision
- Flask
- Gunicorn 1 worker
- systemd
- Caddy
- UFW
- SQLite
- GitHub

## Alternatives
1. Node.js + PM2
2. NGINX + Gunicorn
3. Docker
4. PHP-FPM

## Rationale
Flask dipilih karena ringan dan sesuai kebutuhan aplikasi CRUD dengan login. Gunicorn satu worker menjaga pemakaian RAM kecil pada VPS terbatas. systemd memberi start otomatis dan restart saat gagal. Caddy menjadi satu-satunya pintu masuk publik dengan konfigurasi singkat dan siap HTTPS otomatis pada M04. SQLite tidak membutuhkan service tambahan pada tahap awal. UFW membatasi port yang terbuka.

## Consequences
### Positive
- Sedikit komponen dan hemat RAM
- Start otomatis saat boot, restart otomatis saat gagal
- Backend tidak terekspos langsung ke internet

### Negative
- HTTP saja sampai M04, sehingga data login belum terenkripsi saat transit
- SQLite berbasis file dan terbatas untuk banyak penulis bersamaan
- Satu server tanpa redundansi
- Deployment masih manual

## Review Trigger
Review pada M06/M07.
