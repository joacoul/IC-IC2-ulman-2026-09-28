# IC-IC2-ulman-2026-09-28

## Cómo levantar el stack

```bash
docker compose up --build
```

Levanta la API (puerto 8000), PostgreSQL y Mosquitto (puerto 1883).

- Documentación de la API: http://127.0.0.1:8000/docs
- Chequeo de la base: http://127.0.0.1:8000/salud