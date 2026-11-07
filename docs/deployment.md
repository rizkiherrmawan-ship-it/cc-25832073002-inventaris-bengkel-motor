# Deployment

## Prasyarat
- Server Linux dengan systemd
- Git dan deploy key yang sudah terpasang

## Langkah
1. Ambil kode: `git clone git@github.com:rizkiherrmawan-ship-it/cc-25832073002-inventaris-bengkel-motor.git`
2. Salin unit service: `sudo cp inventaris.service /etc/systemd/system/`
3. Muat ulang systemd: `sudo systemctl daemon-reload`
4. Aktifkan dan jalankan: `sudo systemctl enable --now inventaris`
5. Periksa status: `systemctl status inventaris`

## Pembaruan
`git pull` lalu `sudo systemctl restart inventaris`.

## Keamanan
Jangan menyimpan password, secret, atau token di repository.
