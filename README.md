# HeroCTF Attendance certificates

Generate attendance certificates to make happy little flaggers.

## Getting started

Generate HTTPs certificates:

```bash
cd nginx/certs/
certbot certonly --manual --preferred-challenges dns -d 'certificates.heroctf.fr' --work-dir $(pwd) --logs-dir $(pwd) --config-dir $(pwd)
```

Run the `docker-compose`:

```bash
docker compose up -d
```