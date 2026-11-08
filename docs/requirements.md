# Requirements

## Problem Statement
Pemilik dan petugas bengkel motor mengalami kesulitan mencatat dan mencari data suku cadang pada pencatatan manual di bengkel.
Sistem akan menyediakan pencatatan suku cadang berbasis web dengan akun per bengkel sehingga data tiap bengkel tersimpan terpisah dan dapat diakses dari mana saja.

## Target Users
Pemilik dan petugas bengkel motor. Setiap bengkel memiliki akun sendiri.

Sebagai pemilik bengkel, saya ingin mencatat suku cadang beserta kategori, stok, dan harganya pada akun bengkel saya, sehingga stok mudah dipantau.

## Functional Requirements
- FR-01 Sistem menyediakan pendaftaran akun bengkel (`/daftar`).
- FR-02 Sistem menyediakan login dan logout (`/login`, `/logout`).
- FR-03 Sistem menampilkan daftar barang milik bengkel yang sedang login (`/`).
- FR-04 Sistem dapat menambah barang berisi nama, kategori, stok, dan harga (`/tambah`).
- FR-05 Sistem dapat mengubah barang (`/ubah/<id>`).
- FR-06 Sistem dapat menghapus barang (`/hapus/<id>`).
- FR-07 Ubah dan hapus hanya berlaku untuk barang milik bengkel yang sedang login.
- FR-08 Sistem menyediakan health endpoint (`/health`).

## Non-Functional Requirements
- NFR-01 Backend hanya listen pada loopback.
- NFR-02 Aplikasi dikelola systemd.
- NFR-03 Request publik masuk melalui reverse proxy.
- NFR-04 Secret tidak disimpan pada Git repository.
- NFR-05 Health endpoint mengembalikan HTTP 200 saat sehat.
- NFR-06 Deployment dapat direproduksi dari repository.
- NFR-07 Arsitektur sesuai VPS 2 vCPU/1.9Gi RAM.

## Constraints
- 2 vCPU
- 1.9Gi RAM
- 19G disk
- Ubuntu Server 24.04
- public IPv4

## Scope
### In Scope M03
- Aplikasi Flask dengan akun bengkel dan CRUD barang (SQLite)
- Deployment pertama pada VPS: Gunicorn, systemd, Caddy, UFW
- Repository, dokumentasi, evidence, dan backlog

### Out of Scope M03
- DNS dan HTTPS (M04)
- Data service terpisah (M05)
- Container (M06), IaC (M07), CI/CD (M09)

## Acceptance Criteria M03
- [ ] first deployment accessible
- [x] health endpoint works
