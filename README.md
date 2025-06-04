# Doner HUB

This project contains a FastAPI backend and several Telegram bots built with aiogram.

## Installation

1. Copy `.env.example` to `.env` and adjust values.
2. Build and start services with Docker Compose:

```bash
docker compose up -d
```

This will launch PostgreSQL, Redis, the FastAPI application and placeholder bot container.

## Local Development

Ensure dependencies are installed and run:

```bash
python run.py
```

Bots can be started similarly from their respective `main.py` files.

