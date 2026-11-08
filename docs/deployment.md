# Manual Deployment M03

## Application Path
`/home/rizki06/inventaris-bengkel-motor`

## Service
`inventaris.service`

## Backend
`127.0.0.1:8000`

## Public Endpoint
`http://103.193.177.228/`

## Update Procedure

```bash
cd ~/inventaris-bengkel-motor
git pull
source venv/bin/activate
python -m pip install -r requirements.txt
sudo systemctl restart inventaris
sudo systemctl status inventaris --no-pager
curl -fsS http://127.0.0.1:8000/health
curl -fsS http://127.0.0.1/health
```
