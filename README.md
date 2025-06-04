# Doner HUB

This project contains a FastAPI backend and several Telegram bots built with aiogram.

## Installation

1. Copy `.env.example` to `.env` and adjust values.
2. Initialize the database schema:
   ```bash
   alembic upgrade head
   ```
3. Build and start services with Docker Compose:
   ```bash
   docker compose up -d
   ```

This will launch PostgreSQL, Redis, the FastAPI application and bot containers.

## Local Development

Ensure dependencies are installed and run:

```bash
python run.py
```

Bots can be started similarly from their respective `main.py` files.

## Quick Start Diagram

![diagram](https://dbdiagram.io/embed/6644f127ac844320ae1e9a3e)

## k6 Load Test Example

Create a file `load.js`:
```javascript
import http from 'k6/http';
import { check } from 'k6';

export default function () {
  const res = http.get('http://localhost:8000/health');
  check(res, { 'status was 200': (r) => r.status === 200 });
}
```
Run the test:
```bash
k6 run load.js
```

## Checking Health

Use Docker compose logs to observe healthchecks:
```bash
docker compose logs -f fastapi
```
