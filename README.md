# Doner HUB

FastAPI backend and Telegram bots for food ordering.

## Quick start

```bash
git clone <repo-url>
cd Doner_HUB
cp .env.example .env
docker compose up -d
```

Run database migrations:

```bash
alembic -c database/alembic.ini upgrade head
```

Run tests and linters:

```bash
pytest --cov
pre-commit run --all-files
```

Optionally load test with [k6](https://k6.io).

Database schema diagram available at [dbdiagram.io](https://dbdiagram.io).
